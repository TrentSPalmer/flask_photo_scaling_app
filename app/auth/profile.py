#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import current_user
from .. import db
from app.models import Contributor
from app.forms import EditProfile, ChangePassword

prof = Blueprint(
    "prof", __name__, template_folder="templates"
)


@prof.route("/change-password", methods=["GET", "POST"])
def change_password():
    if not current_user.is_authenticated:
        return(redirect(url_for('proute.index')))
    contributor = Contributor.query.get(current_user.id)
    form = ChangePassword()
    if form.validate_on_submit():
        if contributor.check_password(form.password.data):
            contributor.set_password(form.new_password.data)
            db.session.commit()
            flash("Thanks for the update!")
            return(redirect(url_for('proute.index')))
        else:
            flash("Error Invalid Password")
            return(redirect(url_for('prof.change_password')))
    return render_template('change_password.html', title='Change Password', form=form)


@prof.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if current_user.is_anonymous:
        return(redirect(url_for('proute.index')))
    contributor = Contributor.query.get(current_user.id)
    form = EditProfile()
    if request.method == 'GET':
        form.username.data = contributor.name
        form.email.data = contributor.email
    if form.validate_on_submit():
        if contributor.check_password(form.password.data):
            contributor.name = form.username.data
            contributor.email = form.email.data
            db.session.commit()
            flash("Thanks for the update!")
            return(redirect(url_for('proute.index')))
        else:
            flash("Error Invalid Password")
            return(redirect(url_for('prof.edit_profile')))
    return render_template(
        'edit_profile.html',
        title='Edit Profile', form=form,
        contributor_use_totp=contributor.use_totp
    )
