import os
from classify import *
from config import *
from fill_db import fill_db
from utils import resize_img

if __name__ == "__main__":
    # global test_dataset
    # images = os.listdir(test_dataset)
    # for img in images:
    #     path = test_dataset + img
    #     resize_img(path)

    global test_boxes, db_path
    fill_db(db_path, test_boxes)

    # specify path to the model you want to test
    global model_path
    update(model_path, db_path)

    draw_all_boxes()
