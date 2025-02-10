#!/usr/bin/env python3

from flask import Blueprint, flash, render_template, current_app
from flask_login import current_user
from shutil import disk_usage
import psycopg2

proute = Blueprint(
    "proute", __name__, template_folder="templates"
)


@proute.route("/")
@proute.route("/index")
def index():
    if current_user.is_authenticated:
        photos = get_photo_list(current_user.id)
        flash(get_disk_stats())
        return(render_template(
            'index.html',
            title="Photos",
            photos=photos,
            photo_url=current_app.config['PHOTO_URL']
        ))
    return render_template('index.html', title="Photos")


def get_photo_list(contributor_id):
    conn = psycopg2.connect(
        dbname=current_app.config['DATABASE_NAME'],
        user=current_app.config['DATABASE_USER'],
        host=current_app.config['DATABASE_HOST'],
        password=current_app.config['DATABASE_PASSWORD']
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    my_sql = "SELECT photo_name,id FROM photo WHERE contributor_id=%s "
    my_sql += "ORDER BY timestamp,\"DateTimeOriginal\" DESC"
    cur.execute(my_sql, (contributor_id, ))
    photos = cur.fetchall()
    conn.close()
    return photos


def get_disk_stats():
    disk_stats = disk_usage('/')
    return("Used {}GB of {}GB, {}GB free".format(
        round(disk_stats.used / 1073741824, 1),
        round(disk_stats.total / 1073741824, 1),
        round(disk_stats.free / 1073741824, 1)
    ))
