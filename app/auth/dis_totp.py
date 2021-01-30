#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from app.models import Contributor
from flask_wtf import FlaskForm
from wtforms import SubmitField
from .. import db

disabletotp = Blueprint(
    "disabletotp", __name__, template_folder="templates"
)


@disabletotp.route('/disable-totp', methods=['GET', 'POST'])
def disable_totp():
    if current_user.is_anonymous or not current_user.use_totp:
        return(redirect(url_for('proute.index')))
    contributor = Contributor.query.get(current_user.id)
    form = DisableTotp()
    if form.validate_on_submit():
        if disable_2fa(contributor):
            flash('2FA Now Disabled')
            return(redirect(url_for('prof.edit_profile')))
        else:
            flash('2FA Not Disabled')
            return(redirect(url_for('prof.edit_profile')))
    return render_template('disable_2fa.html', form=form, title="Disable 2FA")


def disable_2fa(contributor):
    contributor.use_totp = False
    contributor.totp_key = None
    db.session.commit()
    return True


class DisableTotp(FlaskForm):
    submit = SubmitField('Disable 2FA')
