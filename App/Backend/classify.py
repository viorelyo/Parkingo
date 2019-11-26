from tinydb import TinyDB, Query
from utils import img_to_array
from PIL import Image
import cv2
from config import *
from models import get_cnn_model, get_vgg_model

import tensorflow as tf
import numpy as np
import time

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

def get_crop_area(spot):
    left_corner_x = int(spot['crop'][0] // 1.58)
    left_corner_y = int(spot['crop'][1] // 1.45)
    right_corner_x = int(spot['crop'][2] // 1.58)
    right_corner_y = int(spot['crop'][3] // 1.45)

def get_active_model():
    return get_vgg_model()  # We should push this to a configuration file

def predict_vgg(image):
    model = get_vgg_model()
    prediction = model.predict(image)
    print(prediction)
    if round(prediction[0][0]) is 1:
        return True
    return False

def predict_cnn(image):
    model = get_cnn_model()
    prediction = model.predict(image)
    if prediction[0][0] > prediction[0][1]:
        return False
    return True

def update(db_path):
    """
    Update data for all parking spots in the db
    """
    global test_dataset
    db = TinyDB(db_path)
    parkings = db.all()

    for parking in parkings:
        camera_image = Image.open(test_dataset + parking['url'])

        # Process each parking spot
        parking_spots = parking['spots']
        updated_parking_spots = []
        for spot in parking_spots:
            crop_area = get_crop_area(spot)
            spot_image = crop_img(camera_image, crop_area)
            spot_image = img_to_array(spot_image, path=False)
            spot['occupied'] = predict_cnn(spot_image)
            updated_parking_spots.append(spot)
        tf.keras.backend.clear_session()
        db.update({'spots': updated_parking_spots}, eids=[parking.eid])


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
        crop = get_crop_area(spot)
        color = (0, 255, 0)
        if spot["occupied"]:
            color = (0, 0, 255)

        cv2.rectangle(img, (crop[0], crop[1]),
                        (crop[0] + crop[2], crop[1] + crop[3]), color, 2)

    global test_output
    output_path = test_output + img_path
    cv2.imwrite(output_path, img)

if __name__ == "__main__":
    global db_path, model_path
    update(db_path)
    draw_all_boxes()
