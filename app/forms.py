import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.models import Users

class Registration(FlaskForm):
    username = StringField('Username', 
                            validators=[
                                DataRequired(), 
                                Length(min=2, max=20, message="Must be between 2 and 20 characters"),
                                Regexp('^\w+$', message="Please use only letters, numbers, or underscore")
                            ])
    email = StringField('Email', 
                        validators=[
                            DataRequired(),
                            Email()
                        ])                            
    password = PasswordField('Password',
                            validators=[
                                DataRequired(),
                                Length(min=6),
                                Regexp('^\w+$', message="Please use only letters, numbers, or underscore")
                            ])
    password_confirm = PasswordField('Confirm Password', 
                                    validators=[
                                        DataRequired(),
                                        EqualTo('password')
                                    ])                            
    submit = SubmitField('Sign Up')    

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken. Please choose another.")

    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is already in use. Please use another.")            


class Login(FlaskForm):
    email = StringField('Email', 
                        validators=[
                            DataRequired(),
                            Email()
                        ])    
    password = PasswordField('Password', 
                            validators=[
                                DataRequired()
                            ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')                                                    
