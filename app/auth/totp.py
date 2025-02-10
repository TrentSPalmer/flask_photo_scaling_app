#!/usr/bin/env python3

import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from app.models import Contributor
from app.forms import ConfirmTotp
from .. import db

totps = Blueprint(
    "totps", __name__, template_folder="templates"
)


@totps.route('/enable-totp', methods=['GET', 'POST'])
def enable_totp():
    if current_user.is_anonymous or current_user.use_totp:
        return(redirect(url_for('proute.index')))
    contributor = Contributor.query.get(current_user.id)
    form = ConfirmTotp()
    qr = get_totp_qr(contributor)
    if form.validate_on_submit():
        if contributor.use_totp:
            flash('2FA Already Enabled')
            return(redirect(url_for('prof.edit_profile')))
        if validate_totp(contributor, form.totp_code.data):
            flash('2FA Now Enabled')
            return(redirect(url_for('prof.edit_profile')))
        else:
            flash("TOTP Code didn't validate, rescan and try again")
            return(redirect(url_for('prof.edit_profile')))
    return render_template(
        'qr.html',
        qr=qr,
        form=form,
        title="Aunthentication Code",
    )


def get_totp_qr(contributor):
    if contributor.totp_key is None:
        contributor.totp_key = pyotp.random_base32()
        db.session.commit()

    totp_uri = pyotp.totp.TOTP(
        contributor.totp_key,
    ).provisioning_uri(name=contributor.email, issuer_name='Photo App')
    img = qrcode.make(totp_uri, image_factory=qrcode.image.svg.SvgPathImage)
    f = BytesIO()
    img.save(f)
    return(f.getvalue().decode('utf-8'))


def validate_totp(contributor, totp_code):
    if pyotp.TOTP(contributor.totp_key).verify(int(totp_code), valid_window=5):
        contributor.use_totp = True
        db.session.commit()
        return True
    else:
        return False
