#!/usr/bin/env python3

import psycopg2
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO


def get_totp_qr(contributor, app_config):
    totp_key = pyotp.random_base32() if contributor.totp_key is None else contributor.totp_key
    if contributor.totp_key is None:
        conn = psycopg2.connect(
            dbname=app_config['DATABASE_NAME'],
            user=app_config['DATABASE_USER'],
            password=app_config['DATABASE_PASSWORD']
        )
        cur = conn.cursor()
        cur.execute("UPDATE contributor SET totp_key=%s WHERE id=%s", (totp_key, contributor.id))
        conn.commit()
        conn.close()

    totp_uri = pyotp.totp.TOTP(totp_key).provisioning_uri(name=contributor.email, issuer_name='Photo App')
    img = qrcode.make(totp_uri, image_factory=qrcode.image.svg.SvgPathImage)
    f = BytesIO()
    img.save(f)
    return(f.getvalue().decode('utf-8'))


def validate_totp(contributor, totp_code, app_config):
    if pyotp.TOTP(contributor.totp_key).verify(int(totp_code)):
        conn = psycopg2.connect(
            dbname=app_config['DATABASE_NAME'],
            user=app_config['DATABASE_USER'],
            password=app_config['DATABASE_PASSWORD']
        )
        cur = conn.cursor()
        cur.execute("UPDATE contributor SET use_totp='1' WHERE id=%s", (contributor.id, ))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def disable_2fa(contributor, app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        password=app_config['DATABASE_PASSWORD']
    )
    cur = conn.cursor()
    cur.execute("UPDATE contributor SET use_totp='0', totp_key=Null WHERE id=%s", (contributor.id, ))
    conn.commit()
    conn.close()
    return True
