#!/usr/bin/env python3

from flask import (
    Blueprint, request, redirect, url_for,
    render_template, current_app, send_file,
)
from flask_login import current_user
from app.models import Photo
from app.forms import ConfirmPhotoDelete
import psycopg2
import os

d_d = Blueprint(
    "d_d", __name__, template_folder="templates"
)


@d_d.route('/download')
def download():
    if current_user.is_authenticated:
        f = request.args['file']
        try:
            return send_file(
                '/var/lib/photo_app/photos/{}'.format(f),
                attachment_filename=f,
            )
        except Exception as e:
            return str(e)


@d_d.route('/delete', methods=['GET', 'POST'])
def delete():
    photo = Photo.query.get(request.args['photo_id'])
    if photo is None:
        return(redirect(url_for('proute.index')))
    cu = current_user
    if not cu.is_authenticated or photo.contributor_id != cu.id:
        return(redirect(url_for('proute.index')))
    form = ConfirmPhotoDelete()
    if request.method == 'POST' and form.validate_on_submit():
        return(
            redirect(url_for('p_route.photo', photo_id=delete_photo(photo))),
        )
    return(render_template(
        'delete_photo.html',
        title="Delete Photo?",
        photo=photo,
        photo_url=current_app.config['PHOTO_URL'],
        form=form
    ))


def delete_photo(photo):
    conn = psycopg2.connect(
        dbname=current_app.config['DATABASE_NAME'],
        user=current_app.config['DATABASE_USER'],
        host=current_app.config['DATABASE_HOST'],
        password=current_app.config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT count(id) FROM photo WHERE contributor_id=%s AND id>%s",
        (photo.contributor_id, photo.id),
    )
    if cur.fetchone()[0] == 0:
        cur.execute(
            "SELECT id FROM photo WHERE contributor_id=%s ORDER BY id",
            (photo.contributor_id, ),
        )
    else:
        my_statement = "SELECT id FROM photo WHERE contributor_id=%s "
        my_statement += "AND id>%s ORDER BY id"
        cur.execute(my_statement, (photo.contributor_id, photo.id))
    next_photo_id = cur.fetchone()[0]
    os.chdir(current_app.config['PHOTO_SAVE_PATH'])
    if os.path.exists('raw_' + photo.photo_name):
        os.remove('raw_' + photo.photo_name)
    if os.path.exists('1280_' + photo.photo_name):
        os.remove('1280_' + photo.photo_name)
    if os.path.exists('480_' + photo.photo_name):
        os.remove('480_' + photo.photo_name)
    cur.execute("DELETE FROM photo WHERE id=%s", (photo.id, ))
    conn.commit()
    conn.close()
    return next_photo_id
