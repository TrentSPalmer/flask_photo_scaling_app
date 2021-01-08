#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
from shutil import disk_usage


def find_next_previous(photo, app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        password=app_config['DATABASE_PASSWORD']
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


def get_photo_list(contributor_id, app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        password=app_config['DATABASE_PASSWORD']
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT photo_name,id FROM photo WHERE contributor_id=%s ORDER BY timestamp,\"DateTimeOriginal\" DESC", (contributor_id, ))
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
