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
