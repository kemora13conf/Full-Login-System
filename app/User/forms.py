from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from ..Models import Users

class RegistrationForm(FlaskForm):
    ''''
    This object render the form's input for Html
    '''
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Lastname ', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username ', validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=30), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    picture = FileField('Your Profile :', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError('This username is already taken!')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError('This email is already exist!')

class LoginForm(FlaskForm):
    ''''
    This object render the form's input for Html
    '''
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=30), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30, message="Must be between 6 and 30 characters")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class ResetReqForm(FlaskForm):
    ''''
    This object render the form's input for Html
    '''
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=30), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = Users.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('This email isn\'t exist!')


class ResetPasswordForm(FlaskForm):
    ''''
    This object render the form's input for Html
    '''
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Update')