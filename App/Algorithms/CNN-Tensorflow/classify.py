from tinydb import TinyDB, Query
from utils import img_to_array
from PIL import Image
from config import *

import tensorflow as tf
import numpy as np
import cv2


db = TinyDB('db.json')

def get_img(image_path):
	img = Image.open(image_path)
	return img


def crop_img(img, crop_data):
    """
    Crop parking spot out of full-size image
    """
    global width, height
    x = crop_data[0]
    y = crop_data[1]
    w = crop_data[2]
    h = crop_data[3]
    cropped_img = img.crop((x, y, x + w, y + h))

    new_size = (width, height)
    cropped_img = cropped_img.resize(new_size)

    return cropped_img


def update():
    """
    Update data
    """
    parkings = db.all()

    for parking in parkings:
        camera_image = get_img(parking['url'])

		# Process each parking spot
        parking_spots = parking['spots']
        updated_parking_spots = []

        for spot in parking_spots:
            model = tf.keras.models.load_model('model.h5')

            spot_image = crop_img(camera_image, spot['crop'])
            spot_image = img_to_array(spot_image, path=False)
            
            prediction = model.predict(np.array([spot_image]))
            if prediction[0][0] > prediction[0][1]:
                spot['occupied'] = False
            else:
                spot['occupied'] = True
            updated_parking_spots.append(spot)

            tf.keras.backend.clear_session()

        db.update({'spots': updated_parking_spots}, eids=[parking.eid])
