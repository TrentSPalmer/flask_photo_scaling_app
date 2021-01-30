#!/usr/bin/env python3

from flask import Blueprint, redirect, url_for, current_app, render_template
from flask_login import current_user
from app.models import Photo
import psycopg2
import psycopg2.extras

p_route = Blueprint(
    "p_route", __name__, template_folder="templates"
)


@p_route.route('/photo/<int:photo_id>')
def photo(photo_id):
    photo = Photo.query.get(photo_id)
    if not current_user.is_authenticated or photo is None:
        return(redirect(url_for('proute.index')))
    find_next_previous(photo)
    calc_additional_data(photo)
    return render_template(
        'photo.html',
        title="Photo",
        photo=photo,
        photo_url=current_app.config['PHOTO_URL']
    )


def find_next_previous(photo):
    conn = psycopg2.connect(
        dbname=current_app.config['DATABASE_NAME'],
        user=current_app.config['DATABASE_USER'],
        host=current_app.config['DATABASE_HOST'],
        password=current_app.config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("SELECT count(id) FROM photo WHERE contributor_id=%s AND id > %s", (photo.contributor_id, photo.id))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s ORDER BY id", (photo.contributor_id, ))
    else:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s AND id > %s ORDER BY id", (photo.contributor_id, photo.id))
    photo.next_photo_id = cur.fetchone()[0]
    cur.execute("SELECT count(id) FROM photo WHERE contributor_id=%s AND id < %s", (photo.contributor_id, photo.id))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s ORDER BY id DESC", (photo.contributor_id, ))
    else:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s AND id < %s ORDER BY id DESC", (photo.contributor_id, photo.id))
    photo.previous_photo_id = cur.fetchone()[0]
    conn.close()


def calc_additional_data(photo):
    photo.UploadDate = photo.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if photo.photo_raw_size >= 1048576:
        photo.SizeOnDisc = str(round(photo.photo_raw_size / 1048576, 1)) + 'M'
    else:
        photo.SizeOnDisc = str(round(photo.photo_raw_size / 1024, 1)) + 'K'
    if photo.photo_1280_size >= 1048576:
        photo.SizeOnDisc1280 = str(round(photo.photo_1280_size / 1048576, 1)) + 'M'
    else:
        photo.SizeOnDisc1280 = str(round(photo.photo_1280_size / 1024, 1)) + 'K'
    if photo.photo_480_size >= 1048576:
        photo.SizeOnDisc480 = str(round(photo.photo_480_size / 1048576, 1)) + 'M'
    else:
        photo.SizeOnDisc480 = str(round(photo.photo_480_size / 1024, 1)) + 'K'
    if photo.GPSAltitude is not None:
        photo.GPSAltitudeFeet = round(photo.GPSAltitude * 3.28084, 1)
    else:
        photo.GPSAltitudeFeet = None
    if photo.GPSLatitude is not None and photo.GPSLongitude is not None:
        photo.LatLong = "{},{}".format(photo.GPSLatitude, photo.GPSLongitude)
        photo.MapUrl = "https://www.google.com/maps/search/?api=1&query={}".format(photo.LatLong)
    else:
        photo.LatLong, photo.MapUrl = None, None
