#!/usr/bin/env python3

from PIL import Image
import os


def crop_photo(photo, photo_save_path):
    photo_1280 = '1280_' + photo
    photo_480 = '480_' + photo
    processing_tuple = ((1280, photo_1280), (480, photo_480))
    os.chdir(photo_save_path)
    img = Image.open('raw_' + photo)
    if img.size[0] > img.size[1]:
        for x in processing_tuple:
            basewidth = x[0]
            wpercent = (basewidth / float(img.size[0]))
            hsize = int(float(img.size[1] * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(x[1])
    else:
        for x in processing_tuple:
            baseheight = x[0]
            hpercent = (baseheight / float(img.size[1]))
            wsize = int(float(img.size[0] * float(hpercent)))
            img = img.resize((wsize, baseheight), Image.ANTIALIAS)
            img.save(x[1])
