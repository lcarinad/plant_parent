from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Optional, Email

class SignupForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired("A username is required")])
    email = StringField("Email", validators=[InputRequired(), Email("Email is required")])
    password = PasswordField("Password", validators=[InputRequired("A valid password is required")])

    pref_indoor=SelectField("Show me only indoor plants", choices=[(1, "Yes")],coerce=int, validators=[Optional()])
    pref_edible=SelectField("Show me only edible plants",choices=[(1, "Yes")], coerce=int,  validators=[Optional()])
    pref_sunlight=SelectField("Sunlight Amount", choices=[('full_shade', "Full Shade"), ('part_shade', "Part Shade"), ("sun-part_shade", "Mixed Sun & Shade"), ("full_sun", "Full Sun")], validators=[Optional()])
    pref_watering=SelectField("Watering Amount", choices=[("frequent", ("Frequent")), ("average", "Average"), ("minimum", "Minimum"), ("none", "None")], validators=[Optional()])