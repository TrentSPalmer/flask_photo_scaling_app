#!/usr/bin/env python3

import psycopg2
from datetime import datetime
from time import time
from .crop_photo import crop_photo
from .get_exif_data import get_exif_data


def process_uploaded_photo(filename, current_user, app_config):
    crop_photo(filename, app_config['PHOTO_SAVE_PATH'])
    exif_data = get_exif_data(filename)
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        host="/var/run/postgresql",
        password=app_config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("SELECT setval('photo_id_seq', (SELECT MAX(id) FROM photo))")
    conn.commit()
    cur.execute("SELECT count(id) FROM photo WHERE photo_name=%s", (filename, ))
    if cur.fetchone()[0] == 0:
        sql_statement = "INSERT INTO photo("

        sql_statement += "photo_name,"
        sql_statement += "contributor_id,"
        sql_statement += "timestamp,"

        sql_statement += "photo_raw_size,"
        sql_statement += "photo_1280_size,"
        sql_statement += "photo_480_size,"

        sql_statement += "photo_format,"
        sql_statement += "photo_width,"
        sql_statement += "photo_height,"

        sql_statement += "photo_1280_width,"
        sql_statement += "photo_1280_height,"
        sql_statement += "photo_480_width,"

        sql_statement += "photo_480_height,"
        sql_statement += "\"Make\","
        sql_statement += "\"Model\","

        sql_statement += "\"Software\","
        sql_statement += "\"DateTime\","
        sql_statement += "\"DateTimeOriginal\","

        sql_statement += "\"DateTimeDigitized\","
        sql_statement += "fnumber,"
        sql_statement += "\"DigitalZoomRatio\","

        sql_statement += "\"AspectRatio\","
        sql_statement += "\"TimeZoneOffset\","
        sql_statement += "\"GPSAltitude\","

        sql_statement += "\"GPSAboveSeaLevel\","
        sql_statement += "\"GPSLatitude\","
        sql_statement += "\"GPSLongitude\","

        sql_statement += "timestamp_int) "

        sql_statement += "VALUES(%s,%s,%s,%s,%s,%s,"
        sql_statement += "%s,%s,%s,%s,%s,%s,"
        sql_statement += "%s,%s,%s,%s,%s,%s,"
        sql_statement += "%s,%s,%s,%s,%s,%s,"
        sql_statement += "%s,%s,%s,%s) RETURNING id"
        cur.execute(sql_statement, (
            filename,
            current_user.id,
            str(datetime.utcnow()),
            exif_data['photo_raw_size'],
            exif_data['photo_1280_size'],
            exif_data['photo_480_size'],
            exif_data['photo_format'],
            exif_data['photo_width'],
            exif_data['photo_height'],
            exif_data['photo_1280_width'],
            exif_data['photo_1280_height'],
            exif_data['photo_480_width'],
            exif_data['photo_480_height'],
            exif_data['Make'] if 'Make' in exif_data else None,
            exif_data['Model'] if 'Model' in exif_data else None,
            exif_data['Software'] if 'Software' in exif_data else None,
            exif_data['DateTime'] if 'DateTime' in exif_data else None,
            exif_data['DateTimeOriginal'] if 'DateTimeOriginal' in exif_data else None,
            exif_data['DateTimeDigitized'] if 'DateTimeDigitized' in exif_data else None,
            exif_data['fnumber'] if 'fnumber' in exif_data else None,
            exif_data['DigitalZoomRatio'] if 'DigitalZoomRatio' in exif_data else None,
            exif_data['AspectRatio'],
            exif_data['TimeZoneOffset'] if 'TimeZoneOffset' in exif_data else None,
            exif_data['GPSAltitude'] if 'GPSAltitude' in exif_data else None,
            exif_data['GPSAboveSeaLevel'] if 'GPSAboveSeaLevel' in exif_data else None,
            exif_data['GPSLatitude'] if 'GPSLatitude' in exif_data else None,
            exif_data['GPSLongitude'] if 'GPSLongitude' in exif_data else None,
            int(time() * 1000)
        ))
        photo_id = cur.fetchone()[0]
    else:
        cur.execute("SELECT id FROM photo WHERE photo_name=%s", (filename, ))
        photo_id = cur.fetchone()[0]
        sql_statement = "UPDATE photo SET "
        sql_statement += "contributor_id=%s, "
        sql_statement += "timestamp=%s, "
        sql_statement += "photo_raw_size=%s, "
        sql_statement += "photo_1280_size=%s, "
        sql_statement += "photo_480_size=%s, "
        sql_statement += "photo_format=%s, "
        sql_statement += "photo_width=%s, "
        sql_statement += "photo_height=%s, "
        sql_statement += "photo_1280_width=%s, "
        sql_statement += "photo_1280_height=%s, "
        sql_statement += "photo_480_width=%s, "
        sql_statement += "photo_480_height=%s, "
        sql_statement += "\"Make\"=%s, "
        sql_statement += "\"Model\"=%s, "
        sql_statement += "\"Software\"=%s, "
        sql_statement += "\"DateTime\"=%s, "
        sql_statement += "\"DateTimeOriginal\"=%s, "
        sql_statement += "\"DateTimeDigitized\"=%s, "
        sql_statement += "fnumber=%s, "
        sql_statement += "\"DigitalZoomRatio\"=%s, "
        sql_statement += "\"AspectRatio\"=%s, "
        sql_statement += "\"TimeZoneOffset\"=%s, "
        sql_statement += "\"GPSAltitude\"=%s, "
        sql_statement += "\"GPSAboveSeaLevel\"=%s, "
        sql_statement += "\"GPSLatitude\"=%s, "
        sql_statement += "\"GPSLongitude\"=%s, "
        sql_statement += "timestamp_int=%s WHERE photo_name=%s"
        cur.execute(sql_statement, (
            current_user.id,
            str(datetime.utcnow()),
            exif_data['photo_raw_size'],
            exif_data['photo_1280_size'],
            exif_data['photo_480_size'],
            exif_data['photo_format'],
            exif_data['photo_width'],
            exif_data['photo_height'],
            exif_data['photo_1280_width'],
            exif_data['photo_1280_height'],
            exif_data['photo_480_width'],
            exif_data['photo_480_height'],
            exif_data['Make'] if 'Make' in exif_data else None,
            exif_data['Model'] if 'Model' in exif_data else None,
            exif_data['Software'] if 'Software' in exif_data else None,
            exif_data['DateTime'] if 'DateTime' in exif_data else None,
            exif_data['DateTimeOriginal'] if 'DateTimeOriginal' in exif_data else None,
            exif_data['DateTimeDigitized'] if 'DateTimeDigitized' in exif_data else None,
            exif_data['fnumber'] if 'fnumber' in exif_data else None,
            exif_data['DigitalZoomRatio'] if 'DigitalZoomRatio' in exif_data else None,
            exif_data['AspectRatio'],
            exif_data['TimeZoneOffset'] if 'TimeZoneOffset' in exif_data else None,
            exif_data['GPSAltitude'] if 'GPSAltitude' in exif_data else None,
            exif_data['GPSAboveSeaLevel'] if 'GPSAboveSeaLevel' in exif_data else None,
            exif_data['GPSLatitude'] if 'GPSLatitude' in exif_data else None,
            exif_data['GPSLongitude'] if 'GPSLongitude' in exif_data else None,
            int(time() * 1000),
            filename
        ))
    conn.commit()
    conn.close()
    return(photo_id)
