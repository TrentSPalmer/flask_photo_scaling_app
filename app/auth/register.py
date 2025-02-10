#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from app.forms import RegistrationForm
from app.models import Contributor
from .. import db

reg = Blueprint(
    "reg", __name__, template_folder="templates"
)


@reg.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('proute.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        my_sql = "SELECT setval('contributor_id_seq', "
        my_sql += "(SELECT MAX(id) FROM contributor))"
        db.engine.execute(my_sql)
        db.session.commit()
        contributor = Contributor(
            name=form.username.data,
            num_photos=0,
            email=form.email.data,
        )
        contributor.set_password(form.password.data)
        db.session.add(contributor)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('auths.login'))
    return render_template('register.html', title='Register', form=form)
