from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import SubmitField, RadioField, PasswordField, StringField,EmailField ,SelectField , IntegerField,TextAreaField,FileField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    Username = StringField(validators=[InputRequired(), Length(min=0, max=50)],render_kw={"placeholder": "User name"})
    Password = PasswordField(validators=[InputRequired(), Length(min=0, max=50)],render_kw={"placeholder": "Password"})
    member = RadioField(choices=['student', 'teacher', 'admin'], validators=[InputRequired()])
    submit = SubmitField("Login")


class CreateMember(FlaskForm):
    Name = StringField(validators=[InputRequired(), Length(min=0, max=50)],render_kw={"placeholder": "Name"})
    SEM = StringField(validators=[InputRequired(), Length(min=0, max=2)],render_kw={"placeholder": "semester"})
    Course = SelectField(choices=[('Bcom(H)','Bcom(H)'),('BCA','BCA'),('BA.EPS','BA.EPS'),("BBA","BBA"),("BBA(H)","BBA(H)"),
                                  ("Bsc.CMS","Bsc.CMS"),("MBA","MBA"),("MCA","MCA"),('BPSYH','BPSYH')])
    Username = StringField(validators=[InputRequired(), Length(min=8, max=8)],render_kw={"placeholder": "RollNo/Username"})
    Email = EmailField(validators=[InputRequired(), Length(min=0, max=50)],render_kw={"placeholder": "Email"})
    Mobile = StringField(validators=[InputRequired(), Length(min=10, max=10)],render_kw={"placeholder": "Mobile Number"})
    Password = PasswordField(validators=[InputRequired(), Length(min=0, max=50)],render_kw={"placeholder": "Password"})
    Salary = StringField(validators=[Length(min=0, max=8)],render_kw={"placeholder": "Salary"})
    submit = SubmitField("Register")

class SearchAdminStudent(FlaskForm):
    Username_st = StringField(validators=[Length(min=0, max=8)],render_kw={"placeholder": "search"})
    submit = SubmitField("->")

class SearchAdminTeacher(FlaskForm):
    Username_th = StringField(validators=[Length(min=0, max=8)],render_kw={"placeholder": "search"})
    submit = SubmitField("->")

class SearchEngine(FlaskForm):
    search = StringField(validators=[InputRequired()],render_kw={"placeholder": "search"})
    submit = SubmitField("->")

class UpdateMember(FlaskForm):
    SEM = StringField(validators=[InputRequired(), Length(min=0, max=2)],render_kw={"placeholder": "semester"})
    Email = EmailField(validators=[InputRequired(), Length(min=0, max=50)], render_kw={"placeholder": "Email"})
    Mobile = StringField(validators=[InputRequired(), Length(min=10, max=10)],render_kw={"placeholder": "Mobile Number"})
    Salary = StringField(validators=[Length(min=0, max=10)],render_kw={"placeholder": "Salary"})
    submit = SubmitField("update")


class PersonalDetails(FlaskForm):
    Marks_10 = IntegerField(validators=[InputRequired()],render_kw={"placeholder": "10th Marks"})
    Marks_12 = IntegerField(validators=[InputRequired()],render_kw={"placeholder": "12th Marks"})
    Father_Name = StringField(validators=[InputRequired()],render_kw={"placeholder": "Father's Name"})
    Mother_Name = StringField(validators=[InputRequired()],render_kw={"placeholder": "Mother's Name"})
    City = StringField(validators=[InputRequired(), Length(min=0, max=20)],render_kw={"placeholder": "city"})
    State = StringField(validators=[InputRequired(), Length(min=0, max=20)],render_kw={"placeholder": "State"})
    Country = StringField(validators=[InputRequired(), Length(min=0, max=20)],render_kw={"placeholder": "country"})
    Local_Guardian = StringField(validators=[InputRequired()],render_kw={"placeholder": "Local Guardian"})
    submit = SubmitField("Submit")

class add_class(FlaskForm):
    SEM = StringField(validators=[Length(min=0, max=2)],render_kw={"placeholder": "semester"})
    Course = SelectField(choices=[('Bcom(H)','Bcom(H)'),('BCA','BCA'),('BA.EPS','BA.EPS'),("BBA","BBA"),("BBA(H)","BBA(H)"),
                                  ("Bsc.CMS","Bsc.CMS"),("MBA","MBA"),("MCA","MCA"),('BPSYH','BPSYH')])
    submit = SubmitField("Submit")

class announcement(FlaskForm):
    announcement = TextAreaField(validators=[InputRequired()])
    submit = SubmitField("Post")

class notes(FlaskForm):
    description = TextAreaField(validators=[InputRequired()])
    file=FileField()
    submit = SubmitField('Upload')