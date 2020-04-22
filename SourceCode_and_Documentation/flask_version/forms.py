from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from models import User 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login') 

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up') 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None: 
            raise ValidationError('This username has already been used') 

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None: 
            raise ValidationError('This email address has already been used') 
        
class ReviewForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired(), Length(max=200)]) 
    landmark = HiddenField('Landmark')
    submit = SubmitField('Add review')

class PlannerForm(FlaskForm):
    start = StringField('Starting place', validators=[DataRequired()])
    landmark1 = StringField('Landmark 1', validators=[DataRequired()])
    landmark2 = StringField('Landmark 2', validators=[DataRequired()])
    landmark3 = StringField('Landmark 3')
    landmark4 = StringField('Landmark 4')
    submit = SubmitField('Plan trip')