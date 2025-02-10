#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, session, flash, render_template
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, GetTotp
from app.models import Contributor
from pyotp.totp import TOTP

auths = Blueprint(
    "auths", __name__, template_folder="templates"
)


@auths.route("/two-factor-input", methods=["GET", "POST"])
def two_factor_input():
    if current_user.is_authenticated or 'id' not in session:
        return redirect(url_for('proute.index'))
    contributor = Contributor.query.get(session['id'])
    if contributor is None:
        return redirect(url_for('proute.index'))
    form = GetTotp()
    if form.validate_on_submit():
        if TOTP(
            contributor.totp_key,
        ).verify(int(form.totp_code.data), valid_window=5):
            login_user(contributor, remember=session['remember_me'])
            flash("Congratulations, you are now logged in!")
            return redirect(url_for('proute.index'))
        else:
            flash("Oops, the pin was wrong")
            form.totp_code.data = None
            return render_template(
                'two_factor_input.html',
                form=form,
                inst="Code was wrong, try again?",
            )
    return render_template(
        'two_factor_input.html',
        form=form,
        inst="Enter Auth Code",
    )


@auths.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('proute.index'))
    form = LoginForm()
    if form.validate_on_submit():
        contributor_by_name = Contributor.query.filter_by(
            name=form.username.data,
        ).first()
        contributor_by_email = Contributor.query.filter_by(
            email=form.email.data,
        ).first()
        cbn, cbe = contributor_by_name, contributor_by_email
        if cbn is not None and cbn.check_password(form.password.data):
            if contributor_by_name.use_totp:
                session['id'] = contributor_by_name.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('auths.two_factor_input'))
            else:
                login_user(contributor_by_name, remember=form.remember_me.data)
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('proute.index'))
        elif cbe is not None and cbe.check_password(form.password.data):
            if contributor_by_email.use_totp:
                session['id'] = contributor_by_email.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('auths.two_factor_input'))
            else:
                login_user(
                    contributor_by_email,
                    remember=form.remember_me.data,
                )
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('proute.index'))
        else:
            flash("Error Invalid Contributor (Username or Email) or Password")
            return(redirect(url_for('auths.login')))
    return render_template('login.html', title='Sign In', form=form)


@auths.route("/logout")
def logout():
    is_authenticated = current_user.is_authenticated
    logout_user()
    if is_authenticated:
        flash("Congratulations, you are now logged out!")
    return redirect(url_for('proute.index'))
