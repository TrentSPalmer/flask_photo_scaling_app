#!/usr/bin/env python3

from flask_login import UserMixin
from flask import current_app
from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt


@login.user_loader
def load_contributor(id):
    return Contributor.query.get(int(id))


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(120), unique=True, nullable=False)
    contributor_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime)
    timestamp_int = db.Column(db.BigInteger)
    photo_raw_size = db.Column(db.String(24))
    photo_1280_size = db.Column(db.String(24))
    photo_480_size = db.Column(db.String(24))
    photo_format = db.Column(db.String(12))
    photo_width = db.Column(db.Integer)
    photo_height = db.Column(db.Integer)
    photo_1280_width = db.Column(db.Integer)
    photo_1280_height = db.Column(db.Integer)
    photo_480_width = db.Column(db.Integer)
    photo_480_height = db.Column(db.Integer)
    Make = db.Column(db.Text)
    Model = db.Column(db.Text)
    Software = db.Column(db.Text)
    DateTime = db.Column(db.DateTime)
    DateTimeOriginal = db.Column(db.DateTime)
    DateTimeDigitized = db.Column(db.DateTime)
    fnumber = db.Column(db.Float)
    DigitalZoomRatio = db.Column(db.Float)
    AspectRatio = db.Column(db.Float)
    TimeZoneOffset = db.Column(db.Integer)
    GPSAltitude = db.Column(db.Float)
    GPSAboveSeaLevel = db.Column(db.Boolean)
    GPSLatitude = db.Column(db.Float)
    GPSLongitude = db.Column(db.Float)


class Contributor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    num_photos = db.Column(db.Integer)
    totp_key = db.Column(db.String(16))
    use_totp = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Contributor {}>'.format(self.name)

    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
            )['reset_password']
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
        return Contributor.query.get(id)


class EmailWhiteList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<EmailWhiteList {}>'.format(self.email)
