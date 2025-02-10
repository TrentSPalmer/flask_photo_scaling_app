#!/usr/bin/env python3

from flask import current_app
from flask_login import current_user
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, abort
)
from app.forms import UploadPhotoForm
from .scripts.process_uploaded_photo import process_uploaded_photo
from werkzeug.utils import secure_filename

pupload = Blueprint(
    "pupload", __name__, template_folder="templates"
)


@pupload.route('/photo-upload', methods=['GET', 'POST'])
def photo_upload():
    if not current_user.is_authenticated:
        return(redirect(url_for('proute.index')))
    form = UploadPhotoForm()
    if request.method == 'POST' and form.validate_on_submit():
        f = request.files['image']
        filename = secure_filename(f.filename)
        if filename != '':
            import os
            file_ext = os.path.splitext(filename)[1]
            fe = file_ext
            if fe not in ['.jpg', '.png'] or fe != validate_image(f.stream):
                abort(400)
            f.save(
                os.path.join(
                    current_app.config['PHOTO_SAVE_PATH'],
                    'raw_' + filename,
                ),
            )
            photo_id = process_uploaded_photo(
                filename,
                current_user,
                current_app.config,
            )
            print(photo_id)
            flash("Thanks for the new photo!")
            return(redirect(url_for('p_route.photo', photo_id=photo_id)))
        return(redirect(url_for('proute.index')))
    return render_template('upload.html', title="Photo Upload", form=form)


def validate_image(stream):
    import imghdr
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
