from flask import Flask, request, render_template
from models import db, connect_db

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

@app.route("/signup",methods=['POST, GET'])
def signup():
    """Show landing page"""
    return render_template("signup.html")