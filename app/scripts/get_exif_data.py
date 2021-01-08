#!/usr/bin/env python3

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from datetime import datetime


def get_exif_data(photo):
    exif_data = {}
    get_file_sizes(photo, exif_data)
    return(exif_data)


def get_exif(img_raw, exif_data):
    if hasattr(img_raw, '_getexif'):
        exifdata = img_raw._getexif()
        date_format = "%Y:%m:%d %H:%M:%S"
        for k, v in TAGS.items():
            if k in exifdata:
                if v == "Make":
                    exif_data['Make'] = exifdata[k]
                if v == "Model":
                    exif_data['Model'] = exifdata[k]
                if v == "Software":
                    exif_data['Software'] = exifdata[k]
                if v == "DateTime":
                    exif_data['DateTime'] = datetime.strptime(exifdata[k], date_format)
                if v == "DateTimeOriginal":
                    exif_data['DateTimeOriginal'] = datetime.strptime(exifdata[k], date_format)
                if v == "DateTimeDigitized":
                    exif_data['DateTimeDigitized'] = datetime.strptime(exifdata[k], date_format)
                if v == "FNumber":
                    exif_data['fnumber'] = round(exifdata[k][0] / exifdata[k][1], 1)
                if v == "DigitalZoomRatio":
                    exif_data['DigitalZoomRatio'] = round(exifdata[k][0] / exifdata[k][1], 2)
                if v == "TimeZoneOffset":
                    exif_data['TimeZoneOffset'] = exifdata[k]
                if v == "GPSInfo":
                    gpsinfo = {}
                    for h, i in GPSTAGS.items():
                        if h in exifdata[k]:
                            if i == 'GPSAltitudeRef':
                                gpsinfo['GPSAltitudeRef'] = int.from_bytes(exifdata[k][h], "big")
                            if i == 'GPSAltitude':
                                gpsinfo['GPSAltitude'] = round(exifdata[k][h][0] / exifdata[k][h][1], 3)
                            if i == 'GPSLatitudeRef':
                                gpsinfo['GPSLatitudeRef'] = exifdata[k][h]
                            if i == 'GPSLatitude':
                                gpsinfo['GPSLatitude'] = calc_coordinate(exifdata[k][h])
                            if i == 'GPSLongitudeRef':
                                gpsinfo['GPSLongitudeRef'] = exifdata[k][h]
                            if i == 'GPSLongitude':
                                gpsinfo['GPSLongitude'] = calc_coordinate(exifdata[k][h])
                    update_gpsinfo(gpsinfo, exif_data)


def update_gpsinfo(gpsinfo, exif_data):
    if 'GPSAltitudeRef' in gpsinfo and 'GPSLatitude' in gpsinfo:
        exif_data['GPSAltitude'] = gpsinfo['GPSAltitude']
        exif_data['GPSAboveSeaLevel'] = False if gpsinfo['GPSAltitudeRef'] != 0 else True
    if 'GPSLatitudeRef' in gpsinfo and 'GPSLatitude' in gpsinfo:
        exif_data['GPSLatitude'] = gpsinfo['GPSLatitude'] if gpsinfo['GPSLatitudeRef'] != 'S' else 0 - gpsinfo['GPSLatitude']
    if 'GPSLongitudeRef' in gpsinfo and 'GPSLongitude' in gpsinfo:
        exif_data['GPSLongitude'] = gpsinfo['GPSLongitude'] if gpsinfo['GPSLongitudeRef'] != 'W' else 0 - gpsinfo['GPSLongitude']


def calc_coordinate(x):
    degrees = x[0][0] / x[0][1]
    minutes = x[1][0] / x[1][1]
    seconds = x[2][0] / x[2][1]
    return round(degrees + minutes / 60 + seconds / 3600, 5)


def get_dimensions_and_format(photo, exif_data):
    img_raw = Image.open('raw_' + photo)
    img_1280 = Image.open('1280_' + photo)
    img_480 = Image.open('480_' + photo)
    exif_data['AspectRatio'] = round(img_raw.width / img_raw.height, 5)
    exif_data['photo_format'] = img_raw.format
    exif_data['photo_width'] = img_raw.width
    exif_data['photo_height'] = img_raw.height
    exif_data['photo_1280_width'] = img_1280.width
    exif_data['photo_1280_height'] = img_1280.height
    exif_data['photo_480_width'] = img_480.width
    exif_data['photo_480_height'] = img_480.height
    get_exif(img_raw, exif_data)


def get_file_sizes(photo, exif_data):
    exif_data['photo_raw_size'] = os.path.getsize('raw_' + photo)
    exif_data['photo_1280_size'] = os.path.getsize('1280_' + photo)
    exif_data['photo_480_size'] = os.path.getsize('480_' + photo)
    get_dimensions_and_format(photo, exif_data)
