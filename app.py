from flask import Flask, request, render_template, flash, redirect
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from forms import SignupForm
app= Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY']='oh-so-secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///plant_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

@app.route("/")
def show_homepage():
    """Show landing page"""
    return render_template("home.html")

@app.route("/signup",methods=['POST', 'GET'])
def signup():
    """Sign Up form; handle adding new user"""
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user=User.signup(
            username=form.username.data,
            email = form.email.data,
            password=form.password.data)
            db.session.commit()

            flash(f"Welcome to the family {user.username}", 'success')
            return redirect("/")
        
        except IntegrityError:
            flash("Username already taken", 'danger')
    else:
        return render_template('signup.html', form=form)
