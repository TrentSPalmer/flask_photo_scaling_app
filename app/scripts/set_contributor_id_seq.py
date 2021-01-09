#!/usr/bin/env python3

import psycopg2


def set_contributor_id_seq(app_config):
    conn = psycopg2.connect(
        dbname=app_config['DATABASE_NAME'],
        user=app_config['DATABASE_USER'],
        host="/var/run/postgresql",
        password=app_config['DATABASE_PASSWORD']
    )

    cur = conn.cursor()
    cur.execute("SELECT setval('contributor_id_seq', (SELECT MAX(id) FROM contributor))")
    conn.commit()
    conn.close()
