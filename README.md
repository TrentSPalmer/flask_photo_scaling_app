## deploy

works on Debian 10 using only distro python3 packages

## apache configs

the example apache configs don't include ssl support,
but if you user letsencrypt, cert-bot will automatically
create those, (and presumable you would select automatic
https redirection when creating the certs)

the photos are served from an entirely separate subdomain
outside of the flask app

## dns

login to your dns provider and add A and AAAA records for photo_app.example.com

or for LAN testing or deployment, if you are running dnsmasq on your router, you
can add something like the following to the `/etc/hosts` file, and then restart
dnsmasq

```conf
192.168.X.XXX         photos.example_host  photo_app.example_host
```
