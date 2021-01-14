#!/usr/bin/env python3

import psycopg2
import os


def delete_photo(photo, app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        host=app_config['DATABASE_HOST'],
        password=app_config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("SELECT count(id) FROM photo WHERE contributor_id=%s AND id>%s", (photo.contributor_id, photo.id))
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s ORDER BY id", (photo.contributor_id, ))
    else:
        cur.execute("SELECT id FROM photo WHERE contributor_id=%s AND id>%s ORDER BY id", (photo.contributor_id, photo.id))
    next_photo_id = cur.fetchone()[0]
    os.chdir(app_config['PHOTO_SAVE_PATH'])
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
