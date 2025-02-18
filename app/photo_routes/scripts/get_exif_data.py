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
        if exifdata is not None:
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
                        exif_data['DateTime'] = datetime.strptime(
                            exifdata[k],
                            date_format,
                        )
                    if v == "DateTimeOriginal":
                        exif_data['DateTimeOriginal'] = datetime.strptime(
                            exifdata[k],
                            date_format,
                        )
                    if v == "DateTimeDigitized":
                        exif_data['DateTimeDigitized'] = datetime.strptime(
                            exifdata[k],
                            date_format,
                        )
                    if v == "FNumber":
                        if type(exifdata[k]) == tuple:
                            x, y = exifdata[k][0], exifdata[k][1]
                        else:
                            x = exifdata[k].numerator
                            y = exifdata[k].denominator
                        exif_data['fnumber'] = round(x / y, 1)
                    if v == "DigitalZoomRatio":
                        if type(exifdata[k]) == tuple:
                            x, y = exifdata[k][0], exifdata[k][1]
                        else:
                            x = exifdata[k].numerator
                            y = exifdata[k].denominator
                        exif_data['DigitalZoomRatio'] = round(x / y, 2)
                    if v == "TimeZoneOffset":
                        exif_data['TimeZoneOffset'] = exifdata[k]
                    if v == "GPSInfo":
                        gpsinfo = {}
                        for h, i in GPSTAGS.items():
                            if h in exifdata[k]:
                                if i == 'GPSAltitudeRef':
                                    gpsinfo['GPSAltitudeRef'] = int.from_bytes(
                                        exifdata[k][h],
                                        "big",
                                    )
                                if i == 'GPSAltitude':
                                    if type(exifdata[k][h]) == tuple:
                                        x = exifdata[k][h][0]
                                        y = exifdata[k][h][1]
                                    else:
                                        x = exifdata[k][h].numerator
                                        y = exifdata[k][h].denominator
                                    gpsinfo['GPSAltitude'] = round(x / y, 3)
                                if i == 'GPSLatitudeRef':
                                    gpsinfo['GPSLatitudeRef'] = exifdata[k][h]
                                if i == 'GPSLatitude':
                                    gpsinfo['GPSLatitude'] = calc_coordinate(
                                        exifdata[k][h],
                                    )
                                if i == 'GPSLongitudeRef':
                                    gpsinfo['GPSLongitudeRef'] = exifdata[k][h]
                                if i == 'GPSLongitude':
                                    gpsinfo['GPSLongitude'] = calc_coordinate(
                                        exifdata[k][h],
                                    )
                        update_gpsinfo(gpsinfo, exif_data)


def update_gpsinfo(gpsinfo, exif_data):
    if 'GPSAltitudeRef' in gpsinfo and 'GPSLatitude' in gpsinfo:
        exif_data['GPSAltitude'] = gpsinfo['GPSAltitude']
        exif_data['GPSAboveSeaLevel'] = False
        if gpsinfo['GPSAltitudeRef'] == 0:
            exif_data['GPSAboveSeaLevel'] = True
    if 'GPSLatitudeRef' in gpsinfo and 'GPSLatitude' in gpsinfo:
        if gpsinfo['GPSLatitudeRef'] != 'S':
            exif_data['GPSLatitude'] = gpsinfo['GPSLatitude']
        else:
            exif_data['GPSLatitude'] = 0 - gpsinfo['GPSLatitude']
    if 'GPSLongitudeRef' in gpsinfo and 'GPSLongitude' in gpsinfo:
        if gpsinfo['GPSLongitudeRef'] != 'W':
            exif_data['GPSLongitude'] = gpsinfo['GPSLongitude']
        else:
            exif_data['GPSLongitude'] = 0 - gpsinfo['GPSLongitude']


def calc_coordinate(x):
    if type(x[0]) == tuple:
        degrees = x[0][0] / x[0][1]
    else:
        degrees = x[0].numerator / x[0].denominator
    if type(x[1]) == tuple:
        minutes = x[1][0] / x[1][1]
    else:
        minutes = x[1].numerator / x[1].denominator
    if type(x[2]) == tuple:
        seconds = x[2][0] / x[2][1]
    else:
        seconds = x[2].numerator / x[2].denominator
    result = round(degrees + minutes / 60 + seconds / 3600, 5)
    return result


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
