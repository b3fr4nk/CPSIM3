from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from cpsim_app.models import User
import re
from cpsim_app.extensions import bcrypt



class ValidatePassword(object):
    def __init__(self, min=8, max=100) -> None:
        self.min = min
        self.max = max
        self.message = ['Password must contain at least one symbol, one uppercase letter, one lowercase letter, and one number', 'Password must be between 6 and 100 characters long']
    
    def __call__(self, form, field):
        l = len(field.data)
        if l < self.min or self.max != -1 and l > self.max:
            match = re.findall("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", field.data)
            if len(match) < 1:
                raise ValidationError(self.message[0])
            raise ValidationError(self.message[1])

class LoginForm(FlaskForm):
    
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self):
        user = User.query.filter_by(school_email=self.email.data).first()
        if not user:
            raise ValidationError('No user with that email. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(school_email=self.email.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')

class SignUpForm(FlaskForm):
    email = StringField("School Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), ValidatePassword()])
    class_code = StringField('Class Code', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        user = User.query.filter_by(school_email=self.email.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')