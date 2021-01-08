#!/usr/bin/env python3

import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
mail = Mail(app)

from app.sendxmpp_handler import SENDXMPPHandler
from app import routes

if app.debug:
    print("flask app 'photo_app' is in debug mode")
else:
    print("flask app 'photo_app' is not in debug mode")

if app.config['LOGGING_XMPP_SERVER']:
    sendxmpp_handler = SENDXMPPHandler(
        logging_xmpp_server=(app.config['LOGGING_XMPP_SERVER']),
        logging_xmpp_sender=(app.config['LOGGING_XMPP_SENDER']),
        logging_xmpp_password=(app.config['LOGGING_XMPP_PASSWORD']),
        logging_xmpp_recipient=(app.config['LOGGING_XMPP_RECIPIENT']),
        logging_xmpp_command=(app.config['LOGGING_XMPP_COMMAND']),
        logging_xmpp_use_tls=(app.config['LOGGING_XMPP_USE_TLS']),
    )
    sendxmpp_handler.setLevel(logging.ERROR)
    app.logger.addHandler(sendxmpp_handler)
