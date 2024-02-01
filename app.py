import os 

from flask import Flask, render_template, flash, redirect, g, session, url_for, request, jsonify
# from flask_mailman import Mail, EmailMessage
from helpers import fetch_random_plant_data, fetch_search_terms, fetch_plant_details, get_logout_msg, add_plant, get_random_plants
from sqlalchemy.exc import IntegrityError, NoResultFound
from models import db, connect_db, User, Plant, Favorite
from forms import SignupForm, LoginForm, EditProfileForm
# import socket
from confid import key

# mail=Mail()


CURR_USER_KEY = "curr_user"

app= Flask(__name__)

# mail.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI']=(os.environ.get('DATABASE_URL','postgresql:///plant_db'))
                                                      
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY','oh-so-secret')
# app.config["MAIL_SERVER"]="smtp.gmail.com"
# app.config["MAIL_PORT"]=465
# app.config["MAIL_USERNAME"]="delagomusic7305@gmail.com"
# app.config["MAIL_PASSWORD"]="klafladsjldafadlk12"
# app.config["MAIL_USE_TLS"]=False
# app.config["MAIL_USE_SSL"]=True

# Gmail SMTP port: 465 (SSL)/587 (TLS)



connect_db(app)
app.app_context().push()

preferences={}
args=["q", "indoor", "edible", "watering", "sunlight"]
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

def logout_user():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# @app.route('/mail')
# def index():
#     timeout = 10
#     try:
#         socket.create_connection(("smtp.gmail.com", 465), timeout)
#         msg = EmailMessage("Here's the Title", "Body of the email", "delagomusic7305@gmail.com", ["lcarinad@gmail.com"])
#         msg.send()
#         return '<h1>sent email...</h1>'
#     except socket.timeout:
#         return '<h1>Connection timed out. Unable to establish a connection.</h1>'
#     except Exception as e:
#         # Handle other connection errors
#         return f'<h1>Error occurred: {e}</h1>'





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
            return redirect("/")
        
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

@app.route('/users/profile/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Update profile for current user"""
    if not g.user:
        flash("You must login to edit your profile", "danger")
        return redirect(url_for(user_login))
    try:
        user=User.query.get(user_id)
        
        print(f"*************id:{user.id}")
        form = EditProfileForm(obj=g.user)
        if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                User.edit_profile(
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        pref_indoor=form.pref_indoor.data,
                        pref_sunlight=form.pref_sunlight.data,
                        pref_watering=form.pref_watering.data,
                        pref_edible=form.pref_edible.data
                )
                db.session.commit()
                flash("You updated your profile!", "success")
                return redirect(url_for("show_homepage"))
            else:
                flash("Invalid Password. Please enter your correct password", "danger")
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("show_homepage"))
    return render_template("edit.html", form=form, user_id=g.user.id)
####################################
@app.route("/")
def show_homepage():
    """Show landing page"""
    if not g.user:
          return render_template("homeanon.html")
    
    if g.user:
        preferences={
            "indoor": g.user.pref_indoor,
            "edible": g.user.pref_edible,
            "watering": g.user.pref_watering,
            "sunlight": g.user.pref_sunlight
        }
        user=User.query.get(g.user.id)

        if any(preferences.values()):
            pref_plants = fetch_search_terms(**preferences)

            if(len(pref_plants)==0):              
                flash("No plants were found matches your preferences.  Try different filters.", 'warning')
                return redirect(url_for("edit_profile", user_id=g.user.id))            
            plants=get_random_plants(pref_plants)

            return render_template('homeUser.html', plants=plants)

        plants=fetch_random_plant_data()
        return render_template('homeUser.html', plants=plants)
        
@app.route("/search")
def search():
    """Handle search query"""
    for arg in args:
        preferences[arg] = request.args.get(arg)
    results=fetch_search_terms(**preferences)

    if(len(results)==0):
        flash("No results found for that term. Try another term", 'warning')
        return redirect(url_for('show_homepage'))
   
    return render_template('search.html', results=results, search_term=preferences['q'])

@app.route("/details/<int:plant_id>")
def show_plant(plant_id):
    """Show details for specific plant.  Note plant_id is id property from Perenual Api."""
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
# ********************Favorite Routes**************************************
@app.route("/add_favorite/<int:plant_id>", methods=["POST"])
def add_favorite(plant_id):
    """Add plant to favorites list"""
    if not g.user:
        flash("You must login to favorite a plant.", "danger")
        return redirect(url_for("user_login"))
    try:
        plant= Plant.query.filter_by(api_id=plant_id).first()

        if not plant:
            """Add plant to db if not there"""
            plant_data=fetch_plant_details(plant_id)
            plant=add_plant(plant_data)      
            db.session.commit()     
        user_id=g.user.id
        Favorite.add_fave(user_id=user_id, plant_id=plant.id, plant_api_id=plant.api_id)
        db.session.commit()

        return jsonify({"msg":"Success"}), 201
    
    except IntegrityError:
        flash("You already favorited this plant.", "warning")
        return redirect(url_for("show_homepage"))
 
@app.route("/delete_favorite/<int:plant_id>", methods=["POST"])
def delete_favorite(plant_id):
    """Remove plant from users favorites. Plant_id is api id."""
    if not g.user:
        flash("Unauthorized access, please login.", "danger")
        return redirect(url_for("user_login")) 
    try:
        plant= Plant.query.filter(Plant.api_id == plant_id).first()
        faved_plant=Favorite.query.filter(Favorite.user_id==g.user.id, Favorite.plant_id==plant.id).one()
        db.session.delete(faved_plant)
        db.session.commit()
        return jsonify({"msg":"Success, object deleted"}, 200)
       
    except NoResultFound:
        flash("This plant is not in your favorites list.", "warning")
        return jsonify({"msg":"Error:Fave not found"}, 400)
    
@app.route("/users/<int:user_id>/favorites")    
def view_favorites(user_id):
    """Show list of user's favorited plants"""
    if not g.user:
        flash("You must login to view your favorite plant babies.", "danger")
        return redirect(url_for("user_login"))

    user=User.query.get_or_404(user_id)
    favorites=Favorite.query.filter(Favorite.user_id==user.id).all()
    if not favorites:
         flash("You do not have any plants favorited at this time.", "info")

    fave_plants=[]

    for fave in favorites:
        plant=Plant.query.get(fave.plant_id)
        fave_plants.append(plant)

    return render_template('/favorites.html', favorites=fave_plants)
