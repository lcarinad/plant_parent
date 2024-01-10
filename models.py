from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app=app
    db.init_app(app)

class User(db.Model):
    """User table"""

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email=db.Column(db.String,nullable=False, unique=True)
    password=db.Column(db.String, nullable=False)
    favorites = db.relationship('Plant', secondary='users_favorites', backref='users')

class Plant(db.Model):
    """Plant table"""

    __tablename__="plants"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, nullable=False, unique=True)   
    name=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String)

class Favorite(db.Model):
    """User favorite plants table"""

    __tablename__ = "users_favorites"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'),primary_key=True)

    