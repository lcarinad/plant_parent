from flask import Flask, request, render_template, flash, redirect, g, session, url_for
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from forms import SignupForm

curr_user_sess_key = "curr_user"

app= Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY']='oh-so-secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///plant_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
########################################################################
#user signup/login/logout
def login_user(user):
    """Add login user to session"""
    session['curr_user_sess_key']=user.id
    print(f"{session}")

@app.route("/")
def show_homepage():
    """Show landing page"""
    return render_template("home.html")

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

            login_user(user)
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
