#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired, Email, Optional, Regexp, ValidationError, EqualTo, Length
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import Contributor, EmailWhiteList
from zxcvbn import zxcvbn


class ConfirmPhotoDelete(FlaskForm):
    submit = SubmitField('Delete')


class GetTotp(FlaskForm):
    totp_code = StringField(
        '6-Digit Code?',
        validators=[DataRequired(), Length(min=6, max=6, message="6 Digits")],
        render_kw={'autofocus': True},
    )
    submit = SubmitField('OK')


class ConfirmTotp(FlaskForm):
    totp_code = StringField(
        '6-Digit Code?',
        validators=[
            DataRequired(),
            Length(min=6, max=6, message="Rescan And Try Again"),
        ],
        render_kw={'autofocus': True},
    )
    submit = SubmitField('Enable 2FA')


class EditProfile(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                '^[a-zA-Z0-9]+$',
                message='letters and digits only (no spaces)',
            ),
        ],
        render_kw={'autofocus': True},
    )
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Name/Email')

    def validate_username(self, username):
        from flask_login import current_user
        if username.data != current_user.name:
            user = Contributor.query.filter_by(name=username.data).first()
            if user is not None:
                raise ValidationError('Please pick a different username.')

    def validate_email(self, email):
        from flask_login import current_user
        if email.data != current_user.email:
            user = Contributor.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please pick a different email address.')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[Optional()], render_kw={'autofocus': True},
    )
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=15, )],
        render_kw={'autofocus': True},
    )
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Request Password Reset')

    def validate_password(self, password):
        if zxcvbn(password.data)['score'] < 3:
            raise ValidationError('needs to be stronger')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                '^[a-zA-Z0-9]+$',
                message='letters and digits only (no spaces)',
            ),
        ],
        render_kw={'autofocus': True},
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=15, )],
    )
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Register')

    def validate_password(self, password):
        if zxcvbn(password.data)['score'] < 3:
            raise ValidationError('needs to be stronger')

    def validate_username(self, username):
        user = Contributor.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        white_listed_user = EmailWhiteList.query.filter_by(
            email=email.data,
        ).first()
        if white_listed_user is None:
            raise ValidationError('This email address is not authorized.')
        user = Contributor.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'autofocus': True},
    )
    submit = SubmitField('Request Password Reset')


class ChangePassword(FlaskForm):
    password = PasswordField(
        'Confirm Password',
        validators=[DataRequired()],
        render_kw={'autofocus': True},
    )
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=15, )],
    )
    new_password2 = PasswordField(
        'Repeat New Password',
        validators=[DataRequired(), EqualTo('new_password')],
    )
    submit = SubmitField('Save')

    def validate_password(self, password):
        if zxcvbn(password.data)['score'] < 3:
            raise ValidationError('needs to be stronger')


class UploadPhotoForm(FlaskForm):
    image = FileField('Upload (<=3M)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()
