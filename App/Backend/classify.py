from tinydb import TinyDB, Query
from utils import img_to_array
from PIL import Image
import cv2
from config import *

import tensorflow as tf
import numpy as np
import time

from models import get_vgg_model, get_cnn_model

model = get_cnn_model()

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


def update(db_path):
    """
    Update data for all parking spots in the db
    """
    global model
    global test_dataset
    db = TinyDB(db_path)
    parkings = db.all()

    all_images_proc_time = 0
    for parking in parkings:
        camera_image = Image.open(test_dataset + parking['url'])

        print('processing image ' + parking['url'])

        # Process each parking spot
        parking_spots = parking['spots']
        updated_parking_spots = []

        single_img_proc_time = 0
        for spot in parking_spots:

            spot_image = crop_img(camera_image, spot['crop'])
            spot_image = img_to_array(spot_image, path=False)
            
            prediction = model.predict(np.array([spot_image]))
            if prediction[0][0] > prediction[0][1]:
                spot['occupied'] = False
            else:
                spot['occupied'] = True
            updated_parking_spots.append(spot)

            # tf.keras.backend.clear_session()
            print(str(end-start))
            single_img_proc_time += end-start
        tf.keras.backend.clear_session()
        all_images_proc_time += single_img_proc_time
        print("Total processing time: " + str(single_img_proc_time))
        db.update({'spots': updated_parking_spots}, eids=[parking.eid])

    print("Average processing time per image: " + str(all_images_proc_time / len(parkings)))


def draw_all_boxes():
    db = TinyDB(db_path)
    parkings = db.all()
    for parking in parkings:
        img_url = parking['url']
        draw_boxes_for_image(img_url)


def draw_boxes_for_image(img_path):
    """
    Draw a box around each parking spot from a full image: green for free, red for occupied
    """

    global test_dataset
    full_path = test_dataset + img_path
    img = image = cv2.imread(full_path)

    global db_path
    db = TinyDB(db_path)
    q = Query()
    spots = db.search(q.url == img_path)[0]['spots']
    for spot in spots:
        if spot["occupied"]:
            # create red box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 0, 255), 2)
        else:
            # create green box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 255, 0), 2)

    global test_output
    output_path = test_output + img_path
    cv2.imwrite(output_path, img)

if __name__ == "__main__":
    global db_path, model_path
    update(model_path, db_path)
