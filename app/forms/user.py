from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models.database import db
from models.user import User


def get_user(username):
    return db.session.query(User).filter_by(username=username).one_or_none()


class LogInForm(FlaskForm):
    username = StringField(
        'Username:', [DataRequired()])
    password = PasswordField(
        'Password:', [DataRequired()])

    def validate_password(self, field):
        user = get_user(self.username.data)
        if not user or user.password != User.hash_password(field.data):
            raise ValidationError('Invalid credentials!')


class SignUpForm(FlaskForm):
    username = StringField('Username:', [
        DataRequired(),
        Length(min=3, max=32)])
    password = PasswordField('Password:', [
        DataRequired(),
        Length(min=5, max=32),
        EqualTo('confirm', message='Passwords must match')]
    )
    confirm = PasswordField('Repeat Password:')

    def validate_username(self, field):
        user = get_user(field.data)
        if user:
            raise ValidationError(f'User with username {field.data!r} already exists!')
