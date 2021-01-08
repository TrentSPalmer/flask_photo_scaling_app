#!/usr/bin/env python3

from pyotp import TOTP
from app import app, db
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, session, flash, request, abort, send_file
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ConfirmTotp
from app.forms import ResetPasswordForm, EditProfile, ChangePassword, DisableTotp
from app.forms import GetTotp, UploadPhotoForm, ConfirmPhotoDelete
from app.models import Contributor, Photo
from app.email import send_password_reset_email
from app.scripts.set_contributor_id_seq import set_contributor_id_seq
from app.scripts.totp_utils import get_totp_qr, validate_totp, disable_2fa
from app.scripts.process_uploaded_photo import process_uploaded_photo
from app.scripts.get_photo_list import get_photo_list, get_disk_stats, calc_additional_data, find_next_previous
from app.scripts.delete_photo import delete_photo
from werkzeug.utils import secure_filename


@app.route('/download')
def download():
    if current_user.is_authenticated:
        f = request.args['file']
        try:
            return send_file('/var/lib/photo_app/photos/{}'.format(f), attachment_filename=f)
        except Exception as e:
            return str(e)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    photo = Photo.query.get(request.args['photo_id'])
    if photo is None:
        return(redirect(url_for('index')))
    if not current_user.is_authenticated or photo.contributor_id != current_user.id:
        return(redirect(url_for('index')))
    form = ConfirmPhotoDelete()
    if request.method == 'POST' and form.validate_on_submit():
        return(redirect(url_for('photo', photo_id=delete_photo(photo, app.config))))
    return(render_template(
        'delete_photo.html',
        title="Delete Photo?",
        photo=photo,
        photo_url=app.config['PHOTO_URL'],
        form=form
    ))


@app.route('/photo-upload', methods=['GET', 'POST'])
def photo_upload():
    if not current_user.is_authenticated:
        return(redirect(url_for('index')))
    form = UploadPhotoForm()
    if request.method == 'POST' and form.validate_on_submit():
        f = request.files['image']
        filename = secure_filename(f.filename)
        if filename != '':
            import os
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.jpg', '.png'] or file_ext != validate_image(f.stream):
                abort(400)
            f.save(os.path.join(app.config['PHOTO_SAVE_PATH'], 'raw_' + filename))
            photo_id = process_uploaded_photo(filename, current_user, app.config)
            print(photo_id)
            flash("Thanks for the new photo!")
            return(redirect(url_for('photo', photo_id=photo_id)))
        return(redirect(url_for('index')))
    return render_template('upload.html', title="Photo Upload", form=form)


@app.route('/photo/<int:photo_id>')
def photo(photo_id):
    photo = Photo.query.get(photo_id)
    if not current_user.is_authenticated or photo is None:
        return(redirect(url_for('index')))
    find_next_previous(photo, app.config)
    calc_additional_data(photo)
    return render_template(
        'photo.html',
        title="Photo",
        photo=photo,
        photo_url=app.config['PHOTO_URL']
    )


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        photos = get_photo_list(current_user.id, app.config)
        flash(get_disk_stats())
        return(render_template(
            'index.html',
            title="Photos",
            photos=photos,
            photo_url=app.config['PHOTO_URL']
        ))
    return render_template('index.html', title="Photos")


def validate_image(stream):
    import imghdr
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.route("/two-factor-input", methods=["GET", "POST"])
def two_factor_input():
    if current_user.is_authenticated or 'id' not in session:
        return redirect(url_for('index'))
    contributor = Contributor.query.get(session['id'])
    if contributor is None:
        return redirect(url_for('index'))
    form = GetTotp()
    if form.validate_on_submit():
        if TOTP(contributor.totp_key).verify(int(form.totp_code.data), valid_window=5):
            login_user(contributor, remember=session['remember_me'])
            flash("Congratulations, you are now logged in!")
            return redirect(url_for('index'))
        else:
            flash("Oops, the pin was wrong")
            form.totp_code.data = None
            return render_template('two_factor_input.html', form=form, inst="Code was wrong, try again?")
    return render_template('two_factor_input.html', form=form, inst="Enter Auth Code")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        contributor_by_name = Contributor.query.filter_by(name=form.username.data).first()
        contributor_by_email = Contributor.query.filter_by(email=form.email.data).first()
        if contributor_by_name is not None and contributor_by_name.check_password(form.password.data):
            if contributor_by_name.use_totp:
                session['id'] = contributor_by_name.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('two_factor_input'))
            else:
                login_user(contributor_by_name, remember=form.remember_me.data)
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('index'))
        elif contributor_by_email is not None and contributor_by_email.check_password(form.password.data):
            if contributor_by_email.use_totp:
                session['id'] = contributor_by_email.id
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('two_factor_input'))
            else:
                login_user(contributor_by_email, remember=form.remember_me.data)
                flash("Congratulations, you are now logged in!")
                return redirect(url_for('index'))
        else:
            flash("Error Invalid Contributor (Username or Email) or Password")
            return(redirect(url_for('login')))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/disable-totp', methods=['GET', 'POST'])
def disable_totp():
    if current_user.is_anonymous or not current_user.use_totp:
        return(redirect(url_for('index')))
    contributor = Contributor.query.get(current_user.id)
    form = DisableTotp()
    if form.validate_on_submit():
        if disable_2fa(contributor, app.config):
            flash('2FA Now Disabled')
            return(redirect(url_for('edit_profile')))
        else:
            flash('2FA Not Disabled')
            return(redirect(url_for('edit_profile')))
    return render_template('disable_2fa.html', form=form, title="Disable 2FA")


@app.route('/enable-totp', methods=['GET', 'POST'])
def enable_totp():
    if current_user.is_anonymous or current_user.use_totp:
        return(redirect(url_for('index')))
    contributor = Contributor.query.get(current_user.id)
    form = ConfirmTotp()
    qr = get_totp_qr(contributor, app.config)
    if form.validate_on_submit():
        if contributor.use_totp:
            flash('2FA Already Enabled')
            return(redirect(url_for('edit_profile')))
        if validate_totp(contributor, form.totp_code.data, app.config):
            flash('2FA Now Enabled')
            return(redirect(url_for('edit_profile')))
        else:
            flash("TOTP Code didn't validate, rescan and try again")
            return(redirect(url_for('edit_profile')))
    return render_template('qr.html', qr=qr, form=form, title="Aunthentication Code")


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if not current_user.is_authenticated:
        return(redirect(url_for('index')))
    contributor = Contributor.query.get(current_user.id)
    form = ChangePassword()
    if form.validate_on_submit():
        if contributor.check_password(form.password.data):
            contributor.set_password(form.new_password.data)
            db.session.commit()
            flash("Thanks for the update!")
            return(redirect(url_for('index')))
        else:
            flash("Error Invalid Password")
            return(redirect(url_for('change_password')))
    return render_template('change_password.html', title='Change Password', form=form)


@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if current_user.is_anonymous:
        return(redirect(url_for('index')))
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
            return(redirect(url_for('index')))
        else:
            flash("Error Invalid Password")
            return(redirect(url_for('edit_profile')))
    return render_template('edit_profile.html', title='Edit Profile', form=form, contributor_use_totp=contributor.use_totp)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    contributor = Contributor.verify_reset_password_token(token)
    if not contributor:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        contributor.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title="New Password?", form=form)


@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    else:
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            contributor = Contributor.query.filter_by(email=form.email.data).first()
            if contributor:
                send_password_reset_email(contributor, app.config['EXTERNAL_URL'])
                flash('Check your email for the instructions to reset your password')
                return redirect(url_for('login'))
            else:
                flash('Sorry, invalid email')
                return redirect(url_for('login'))
        return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        set_contributor_id_seq(app.config)
        contributor = Contributor(name=form.username.data, num_photos=0, email=form.email.data)
        contributor.set_password(form.password.data)
        db.session.add(contributor)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    is_authenticated = current_user.is_authenticated
    logout_user()
    if is_authenticated:
        flash("Congratulations, you are now logged out!")
    return redirect(url_for('index'))
