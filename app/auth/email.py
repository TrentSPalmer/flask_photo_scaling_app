#!/usr/bin/env python3

from flask import render_template, current_app
from flask_mail import Message
from .. import mail
from threading import Thread


def send_password_reset_email(contributor, external_url):
    token = contributor.get_reset_password_token()
    send_email('Photo App Reset Your Password',
               sender=current_app.config['MAIL_ADMINS'][0],
               recipients=[contributor.email],
               text_body=render_template('email/reset_password_email_text.txt',
                                         contributor=contributor, token=token, external_url=external_url),
               html_body=render_template('email/reset_password_email_html.html',
                                         contributor=contributor, token=token, external_url=external_url))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
