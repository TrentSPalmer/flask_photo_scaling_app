#!/usr/bin/env python3

from flask import (
    Blueprint, redirect, url_for, flash, render_template, current_app
)
from flask_login import current_user
from app.models import Contributor
from app.forms import ResetPasswordForm, ResetPasswordRequestForm
from .email import send_password_reset_email
from .. import db

pwd = Blueprint(
    "pwd", __name__, template_folder="templates"
)


@pwd.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('proute.index'))
    contributor = Contributor.verify_reset_password_token(token)
    if not contributor:
        return redirect(url_for('proute.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        contributor.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auths.login'))
    return render_template(
        'reset_password.html',
        title="New Password?",
        form=form,
    )


@pwd.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return(redirect(url_for('proute.index')))
    else:
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            contributor = Contributor.query.filter_by(
                email=form.email.data,
            ).first()
            if contributor:
                send_password_reset_email(
                    contributor,
                    current_app.config['EXTERNAL_URL'],
                )
                my_flash = 'Check your email for the instructions '
                my_flash += 'to reset your password'
                flash(my_flash)
                return redirect(url_for('auths.login'))
            else:
                flash('Sorry, invalid email')
                return redirect(url_for('auths.login'))
        return render_template(
            'reset_password_request.html',
            title='Reset Password',
            form=form,
        )
