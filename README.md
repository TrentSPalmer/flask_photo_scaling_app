![](https://github.com/TrentSPalmer/flask_photo_scaling_app/blob/master/examples/1280_Screenshot_at_2021-01-08_21-44-19.png)

This application allows you to upload photos, where are then automatically
scaled down, using python3-pillow, and saved into an adjacent directory
which is served from a different subdomain.

There is also dashboard functionality, showing you information about the photos
such as size-on-disc, and exif data such as gps coordinates.

## features
* upload, download, delete, photos
* automatically scales down photos
* 2fa with authenticator app
* XMPP error logging
* separate static subdomain for hosting the photos
* dashboard with photo stats

## deploy

works on Debian 10 using only distro python3 packages, examples for
deployment in the examples directory

## apache configs

the example apache configs don't include ssl support,
but if you user letsencrypt, cert-bot will automatically
create those, (and presumable you would select automatic
https redirection when creating the certs)

the photos are served from an entirely separate subdomain
outside of the flask app

## dns

login to your dns provider and add A and AAAA records for **photo_app.example.com**
and add A and AAAA records for **photos.example.com**

or for LAN testing or deployment, if you are running dnsmasq on your router, you
can add something like the following to the `/etc/hosts` file, and then restart
dnsmasq

```conf
192.168.X.XXX         photos.example_host  photo_app.example_host
```

## email white list
in order to register, login to the psql command line and insert
your email address into the email_white_list table

## error logging
The configured logging handler in `__init__.py` requires setting up some
xmpp accounts, i.e. setting up an Prosody server.

If this isn't possible, you could use a different logging handler,
such as SMTPHandler, or just look in the systemd-journal.

## requirements on Debian 10
### apache modules
* `a2enmod proxy_http`
* `a2enmod expires`
* `a2enmod headers`
* `a2enmod userdir`
### debian packages
```shell
apt-get install apache2 postgresql postgresql-contrib
apt-get install python3-gunicorn gunicorn3
apt-get install python3-qrcode python3-pil sendxmpp python3-wtforms python3-dotenv
apt-get install python3-flask python3-flask-sqlalchemy python3-psycopg2
apt-get install python3-flask-login python3-jwt python3-flaskext.wtf
apt-get install python3-flask-mail python3-zxcvbn python3-pyotp
```

For 2fa, you can use an authenticator application such as
*Google Authenticator* or *andOTP* on your smartphone.

## installation instructions
1. clone the git repo
2. create nologin unix user `useradd -r -s /sbin/nologin <app_user>`
2. create all necessary deploy_script target directories `/var/lib/<app_user>/*`
2. adjust and then run the deploy script
2. set up database (see examples)
2. populate `/var/lib/<app_user>/.env` file
2. populate email_white_list from psql command line
2. enable and start two apache virtual hosts
2. install certbot and get certs for each of the two subdomains
2. install service file in `/etc/systemd/system`
2. enable and start systemd service

## Debian 12 Upgrade
2. wtforms.validators now requires `python3-wtforms-components` for the email validator
