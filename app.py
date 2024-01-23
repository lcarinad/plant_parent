from flask import Flask, render_template, flash, redirect, g, session, url_for, request, jsonify
from helpers import fetch_random_plant_data, fetch_search_terms, fetch_plant_details, get_logout_msg, add_plant, get_random_plants
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Plant, Favorite
from forms import SignupForm, LoginForm, EditProfileForm

CURR_USER_KEY = "curr_user"
FAVES="curr_user_faves"

app= Flask(__name__)

app.config['SECRET_KEY']='oh-so-secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///plant_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
app.app_context().push()
################################################################
#user signup/login/logout
@app.before_request
def add_user_to_global():
    """If user logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def add_user_to_sess(user):
    """Add login user to session"""
    session[CURR_USER_KEY]=user.id

    if user.favorites:
        session[FAVES] = [plant.id for plant in user.favorites]
def logout_user():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/signup",methods=['POST', 'GET'])
def signup():
    """Sign Up form; handle user signup by creating new user and adding to DB.  Redirect to landing page.  If form not valid, present form.  If there already is user with that username, flash message and reload form."""
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user=User.signup(
            username=form.username.data,
            email = form.email.data,
            password=form.password.data)
            db.session.commit()
            flash ("Registration successful", 'success')

            add_user_to_sess(user)
            add_user_to_global()
            return redirect(url_for("show_homepage"))
        
        except IntegrityError as e:
            error_message = str(e)
            if 'unique constraint "users_email_key"' in error_message:
                flash("That email address is already registered.  Please sign in to your existing account", 'warning')
            elif 'unique constraint "users_username' in error_message:
                flash("That username is already taken.  Choose another username.", 'warning')
            else:
                flash("An error occured. Please try again", 'warning')
            return redirect('/signup')  
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def user_login():
    """Handles user login for Users with existing account."""
    form = LoginForm()

    if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)

            if user:
                add_user_to_sess(user)
                return redirect('/')         
            flash("Password or username incorrect.", 'danger')

    return render_template('login.html', form = form)

@app.route('/logout')
def user_logout():
    """Handles user logout"""
    logout_user()
    flash(get_logout_msg(), "success")
    return redirect(url_for('show_homepage'))
####################################
@app.route("/")
def show_homepage():
    """Show landing page"""
    if not g.user:
          return render_template("homeanon.html")
    
    if g.user:
        if g.user.pref_indoor or g.user.pref_sunlight or g.user.pref_watering or g.user.pref_edible:

            pref_plants=fetch_search_terms(pref_indoor=g.user.pref_indoor, pref_edible=g.user.pref_edible, pref_watering=g.user.pref_watering, pref_sunlight=g.user.pref_sunlight)

            if(len(pref_plants)==0):
                # find other plants
                flash("No results found for that term. Try another term", 'warning')
            
            plants=get_random_plants(pref_plants)
        
            return render_template('homeUser.html', plants=plants)

        plants=fetch_random_plant_data()
        return render_template('homeUser.html', plants=plants)

       
    
@app.route("/search")
def search():
    """Handle search query"""
    term=request.args.get("q")
    pref_indoor=request.args.get("indoor")
    pref_edible=request.args.get("edible")
    pref_watering=request.args.get("watering")
    pref_sunlight=request.args.get("sunlight")
    results=fetch_search_terms(term, pref_indoor, pref_edible, pref_watering,pref_sunlight)
  
    if(len(results)==0):
        flash("No results found for that term. Try another term", 'warning')
        return redirect(url_for('show_homepage'))
    return render_template('search.html', results=results, search_term=term)

@app.route("/details/<int:plant_id>")
def show_plant(plant_id):
    """Show details for specific plant"""

    plant_data = fetch_plant_details(plant_id)
    if(plant_data) == None:
        flash("Details on that plant are not available at the moment.", 'warning')
        return redirect(url_for('search'))
    return render_template('plant.html', plant=plant_data)

@app.route("/plantlist/<int:p_num>")
def show_all_plants(p_num=1):
    """Show a list of all plants"""
    
    plant_data=fetch_search_terms(order='asc', page=p_num)
    return render_template('list.html', plants=plant_data, page=p_num)

@app.route("/add_favorite/<int:plant_id>", methods=["POST"])
def add_favorite(plant_id):
    """Check to see if plant is in db.  If not add plant to db.  Add plant to favorite"""

    if g.user:

        user_id=g.user.id
        user = User.query.get(user_id)
        plant= Plant.query.filter_by(api_id=plant_id).first()

        if plant:
            user.favorites.append(plant) 
            
        else:
            plant_data=fetch_plant_details(plant_id)
            plant=add_plant(plant_data)           
            db.session.commit()
            user.favorites.append(plant)

        db.session.commit()
        
        add_fave_to_session(plant)
        return jsonify({"msg":"Success"}), 201
    else:
        flash("You must login to favorite a plant.", "danger")
        return jsonify({"error":"User is not logged in"}), 401

@app.route("/delete_favorite/<int:plant_id>", methods=["POST"])
def delete_favorite(plant_id):
    """Delete previously faved plant from db"""
    if g.user:
        curr_user_id=g.user.id
        plant=Plant.query.filter_by(api_id=plant_id).one()
        faved_plant=Favorite.query.filter(Favorite.user_id==curr_user_id, Favorite.plant_id==plant.id).one()
        db.session.delete(faved_plant)
        db.session.commit()
        remove_fave_from_session(plant)

        return jsonify({"msg":"Success, object deleted"}, 200)
    
@app.route("/users/<int:user_id>/favorites")    
def view_favorites(user_id):
    """Show list of user's favorited plants"""
    if not g.user:
        flash("You must login to view your favorite plant babies.", "danger")
        return redirect(url_for(user_login))
    user=User.query.get_or_404(user_id)
    favorites=user.favorites
    fave_info_list=[]
    for fave in favorites:
        fave_info={
             'id':fave.api_id,
              'name':fave.name,
              'image':fave.image_url
         }
        fave_info_list.append(fave_info)

    return render_template('/favorites.html', favorites=fave_info_list)
     
@app.route('/users/profile/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Update profile for current user"""
    if not g.user:
        flash("You must login to edit your profile", "danger")
        return redirect(url_for(user_login))
    
    form = EditProfileForm(obj=g.user)
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
                user.username=form.username.data
                user.email=form.email.data
                user.pref_indoor=form.pref_indoor.data
                user.pref_edible=form.pref_edible.data
                user.pref_sunlight=form.pref_sunlight.data
                user.pref_watering=form.pref_watering.data

                db.session.commit()
                flash("You updated your profile!", "success")
                return redirect(url_for("show_homepage"))
        else:
             flash("Invalid Password. Please enter your correct password", "danger")
    return render_template("edit.html", form=form)

def add_fave_to_session(plant):
    """Add a favorited plan to the users favorites in the session"""
    if FAVES not in session:
        session[FAVES]=[]
    
    session[FAVES].append(plant.id)

def remove_fave_from_session(plant):
    """Remove and unfavorited plant from the user's favorites in the session"""
    if FAVES in session:
        if plant.id in session[FAVES]:
                               session[FAVES].remove(plant.id)