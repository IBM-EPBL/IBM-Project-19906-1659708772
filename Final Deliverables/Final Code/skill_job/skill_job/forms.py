from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from skill_job.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    contact_no = StringField('Contact Number',
                           validators=[DataRequired(), Length(min=2, max=20)])
    gender = RadioField('Gender', choices=['Male', 'Female'])
    role = RadioField('Role', choices=['Seeker', 'Employer'])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class JobPost(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired(), Length(min=2, max=20)])
    skills_needed = StringField('Skills Required', validators=[DataRequired(), Length(min=2, max=200)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=200)])#FileField('Location Name', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class SeekerDetails(FlaskForm):
    location = StringField('Prefered Job Location', validators=[DataRequired(), Length(min=2, max=20)])
    skills = StringField('Enter your Skill Sets separated by comma', validators=[DataRequired(), Length(min=2, max=200)])
    company = StringField('Enter your Intrested Company separated by comma', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Save')

class SearchForm(FlaskForm):
    text = StringField('Search Text',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Search')

