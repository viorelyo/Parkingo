from tinydb import TinyDB, Query
from utils import img_to_array
from PIL import Image
from config import *

import tensorflow as tf
import numpy as np
import time


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


def update(model_path, db_path):
    """
    Update data for all parking spots in the db
    """
    db = TinyDB(db_path)
    parkings = db.all()

    each = 0
    for parking in parkings:
        global test_dataset, weather_sunny
        camera_image = get_img(test_dataset + weather_sunny + parking['url'])

        print('processing image ' + parking['url'])

        # Process each parking spot
        parking_spots = parking['spots']
        updated_parking_spots = []

        total = 0
        for spot in parking_spots:
            model = tf.keras.models.load_model(model_path)

            spot_image = crop_img(camera_image, spot['crop'])
            spot_image = img_to_array(spot_image, path=False)
            
            start = time.time()
            prediction = model.predict(np.array([spot_image]))
            end = time.time()
            if prediction[0][0] > prediction[0][1]:
                spot['occupied'] = False
            else:
                spot['occupied'] = True
            updated_parking_spots.append(spot)

            tf.keras.backend.clear_session()
            print(str(end-start))
            total += end-start
        each += total   
        print(total)
        db.update({'spots': updated_parking_spots}, eids=[parking.eid])

    print("total: " + str(each / len(parkings)))
