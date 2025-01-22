from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="You need to input username")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="You need to input password")
    ])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
		DataRequired(message="You need to input username"),
		Length(min=3, max=20, message="Username needs to be 3 - 20 characters")
	])
    password = PasswordField("Password", validators=[
        DataRequired(message="You need to input password"),
        Length(min=8, max=16, message="Password needs to be 8 - 15 characters")
    ])
    passwordAgain = PasswordField("Password Again", validators=[
        DataRequired(message="You need to input password"),
        EqualTo("password", message="The passwords must be the same")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="You need to input email")
    ])
    phoneNumber = StringField("Phone number", validators=[
        DataRequired(message="You need to input phone number"),
        Length(max=11, message="The max of number needs to be 11 characters")
    ])
    address = StringField("Address", validators=[
        DataRequired(message="You need to input address"),
        Length(max=200, message="The max of address needs to be 200 characters")
    ])
    role = SelectField("Role", choices=[("student", "student"), ("teacher", "teacher"), ("restaurantStaff", "restaurantStaff")], validators=[
        DataRequired(message="You need to choice one of those")
    ])
    submit = SubmitField("Register")




