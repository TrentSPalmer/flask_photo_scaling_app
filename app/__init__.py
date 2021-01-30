#!/usr/bin/env python3

import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
mail = Mail()


def init_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from app.sendxmpp_handler import SENDXMPPHandler

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
    from .auth import auth, totp, dis_totp, profile, register, reset_password
    from .photo_routes import proutes, photox, delete_download, photo_upload
    with app.app_context():
        app.register_blueprint(auth.auths)
        app.register_blueprint(totp.totps)
        app.register_blueprint(dis_totp.disabletotp)
        app.register_blueprint(profile.prof)
        app.register_blueprint(register.reg)
        app.register_blueprint(reset_password.pwd)
        app.register_blueprint(proutes.proute)
        app.register_blueprint(photox.p_route)
        app.register_blueprint(delete_download.d_d)
        app.register_blueprint(photo_upload.pupload)
        return app
