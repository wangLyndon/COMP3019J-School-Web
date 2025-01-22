from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField, SubmitField, StringField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
        DataRequired(message="You need to input password"),
        Length(min=8, max=16, message="Password needs to be 8 - 15 characters")
    ])
    newPassword = PasswordField("New Password", validators=[
        DataRequired(message="You need to input password"),
        Length(min=8, max=16, message="Password needs to be 8 - 15 characters")
    ])
    submit = SubmitField("Save")


class StudentProfileForm(FlaskForm):
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
    studentId = StringField("Student id", validators=[
        DataRequired(message="You need to input student id"),
        Length(max=20, message="Max is 20")
    ])
    dormBuilding = StringField("Dorm Building", validators=[
        DataRequired(message="You need to input dorm building number"),
        Length(max=50, message="Max is 50")
    ])
    dormRoom = StringField("Dorm room", validators=[
        DataRequired(message="You need to input dorm room number"),
        Length(max=10, message="Max is 10")
    ])
    submit = SubmitField("Save")


class TeacherProfileForm(FlaskForm):
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
    teacherId = StringField("Teacher id", validators=[
        DataRequired(message="You need to input Teacher id"),
        Length(max=20, message="Max is 20")
    ])
    officeLocation = StringField("Office location", validators=[
        DataRequired(message="You need to input office location"),
        Length(max=50, message="Max is 50")
    ])
    submit = SubmitField("Save")


class RestaurantStaffProfileForm(FlaskForm):
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
    workSchedule = StringField("Work schedule", validators=[
        DataRequired(message="You need to input work schedule"),
        Length(max=100, message="Max is 100")
    ])
    submit = SubmitField("Save")


class CreateModuleForm(FlaskForm):
    moduleName = StringField("Module Name", validators=[
        DataRequired(message="You need to input Module name"),
        Length(max=50, message="Max is 50")
    ])
    schedule = StringField("Schedule", validators=[
        DataRequired(message="You need to input schedule"),
        Length(max=50, message="Max is 50")
    ])
    location = StringField("Location", validators=[
        DataRequired(message="You need to input location"),
        Length(max=100, message="Max is 100")
    ])
    officeHours = StringField("Office Hours", validators=[
        DataRequired(message="You need to input office hours"),
        Length(max=100, message="Max is 100")
    ])
    submit = SubmitField("Save")


class EnrollForm(FlaskForm):
    submit = SubmitField("Enroll")


class CreateMenuForm(FlaskForm):
    date = DateField("Date", validators=[
        DataRequired("You need to input date")
    ])
    breakfast = StringField("Breakfast", validators=[
        DataRequired(message="You need to input breakfast"),
        Length(max=100, message="Max is 100")
    ])
    lunch = StringField("Lunch", validators=[
        DataRequired(message="You need to input lunch"),
        Length(max=100, message="Max is 100")
    ])
    dinner = StringField("Dinner", validators=[
        DataRequired(message="You need to input dinner"),
        Length(max=100, message="Max is 100")
    ])
    submit = SubmitField("Save")


class AnnouncementForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired(message="You need to input title"),
        Length(max=200, message="Max is 200")
    ])
    content = TextAreaField("Content", validators=[
        DataRequired(message="You need to input content"),
        Length(max=500, message="Max is 500")
    ])
    submit = SubmitField("Save")


class MenuReviewForm(FlaskForm):
    rating = IntegerField("Rating: 1-5", validators=[
        DataRequired(),
        NumberRange(min=1, max=5, message="Rating must be between 1 and 5")
    ])
    reviewContent = TextAreaField("Review Content", validators=[
        DataRequired(message="You need to input review content"),
        Length(max=500, message="Max is 500")
    ])
    submit = SubmitField("Save")
