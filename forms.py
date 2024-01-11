from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Optional, Email

class SignupForm(FlaskForm):
    """User registration form."""
    username = StringField("User Name", validators=[InputRequired("A username is required")])
    password = PasswordField("Password", validators=[InputRequired("A valid password is required")])
    email = StringField("Email", validators=[InputRequired(), Email("Email is required")])

class EditProfileForm(SignupForm):
    """Edit profile form."""

    pref_indoor=BooleanField("Show me only indoor plants", validators=[Optional()])
    pref_edible=BooleanField("Show me only edible plants",  validators=[Optional()])
    pref_sunlight=RadioField("Sunlight Amount", choices=[('full_shade', "Full Shade"), ('part_shade', "Part Shade"), ("sun-part_shade", "Mixed Sun & Shade"), ("full_sun", "Full Sun")], validators=[Optional()])
    pref_watering=RadioField("Watering Amount",choices=[ ("frequent", ("Frequent")), ("average", "Average"), ("minimum", "Minimum"), ("none", "None")], validators=[Optional()])
