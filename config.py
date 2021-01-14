#!/usr/bin/env python3

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

    LOGGING_XMPP_SERVER = os.environ.get('LOGGING_XMPP_SERVER')
    LOGGING_XMPP_SENDER = os.environ.get('LOGGING_XMPP_SENDER')
    LOGGING_XMPP_PASSWORD = os.environ.get('LOGGING_XMPP_PASSWORD')
    LOGGING_XMPP_RECIPIENT = os.environ.get('LOGGING_XMPP_RECIPIENT')
    LOGGING_XMPP_COMMAND = os.environ.get('LOGGING_XMPP_COMMAND')
    LOGGING_XMPP_USE_TLS = os.environ.get('LOGGING_XMPP_USE_TLS')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_ADMINS = [x for x in os.environ.get('MAIL_ADMINS').split(' ')]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    EXTERNAL_URL = os.environ.get('EXTERNAL_URL')

    PHOTO_SAVE_PATH = os.path.join(basedir, 'photos')

    PHOTO_URL = os.environ.get('PHOTO_URL')
