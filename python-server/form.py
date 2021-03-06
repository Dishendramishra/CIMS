from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PasswordChangeForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[InputRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()]) 
    submit = SubmitField('Submit')