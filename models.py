from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt=Bcrypt()

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
    pref_indoor = db.Column(db.Boolean)
    pref_sunlight= db.Column(db.String)
    pref_watering=db.Column(db.String)
    pref_edible=db.Column(db.Boolean)
    favorites = db.relationship('Plant', secondary='favorites', backref='users')

    def __repr__(self):
        """Show info about user."""
        u=self
        return f"<User {u.id} {u.username}>"
    
    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.  Hashes password and adds user to system"""

        hashed_pwd=bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username,password=hashed_pwd, email=email )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with un and hashed pwd. Returns user object if username and hashed pwd are found, else returns False."""
        user = cls.query.filter_by(username=username).first()

        if user:
            auth_check=bcrypt.check_password_hash(user.password, password)
            if auth_check:
                print(f"this user is authorized")
                return user
            return False

class Plant(db.Model):
    """Plant table"""

    __tablename__="plants"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, nullable=False, unique=True)   
    name=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String, default="https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png?20210219185637")

    def __repr__(self):
        """Show info about a plant"""
        p=self
        return f"<Plant_id:{p.id} Plant_api_id:{p.api_id} Name:{p.name}>"
    
    @classmethod
    def add_plant(cls, api_id, name, image_url):
        """Add plant to db"""
        plant = Plant(api_id=api_id, name=name, image_url=image_url)
        db.session.add(plant)
        return plant


class Favorite(db.Model):
    """Mapping a user to their favorited plants"""
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),primary_key=True)
    api_id=db.Column(db.Integer, db.ForeignKey('plants.api_id'), primary_key=True)

