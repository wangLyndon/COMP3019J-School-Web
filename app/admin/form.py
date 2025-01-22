from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.models import User


class EditModuleForm(FlaskForm):
    teacher = StringField("Teacher' userId", validators=[
        DataRequired(message="You need to input id")
    ])
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