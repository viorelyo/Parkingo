from tinydb import TinyDB, Query

import numpy as np
import config
import cv2
import sys
import os


def url_to_image(path):
	image = cv2.imread(path)
	return image


db = TinyDB('db.json')
q = Query()

path = "dataset\\2015-11-12_0709.jpg"
coord = []

img = url_to_image(path)

cv2.namedWindow('image')

spots = db.search(q.url == path)[0]['spots']
for spot in spots:
	if spot["occupied"]:
        # create red box
		cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]), (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 0, 255), 2)
	else:
        # create green box
		cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]), (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 255, 0), 2)

# while(True):
#     cv2.imshow('image', img)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break
cv2.imshow('image', img)
cv2.waitKey(0)