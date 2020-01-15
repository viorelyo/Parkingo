from PIL import Image
import tensorflow as tf
import numpy as np
import cv2
import time
import os
from CNNTensorflow.utils import img_to_array
from config import model_path, width, height


# full = Image.open("full.jpg")
# size = (700, 400)
# full = full.resize(size)
# full.save("fullmin.jpg")

model = tf.keras.models.load_model(model_path)

parent_path = "patchFromVideo/"
#path = "patchFromVideo/Screenshot_2.jpg"

for path in os.listdir(parent_path):
    spot_image = Image.open(parent_path + path)

    new_size = (width, height)
    spot_image = spot_image.resize(new_size)
    spot_image = img_to_array(spot_image, path=False) 

    start = time.time()
    prediction = model.predict(np.array([spot_image]))
    end = time.time()

    if prediction[0][0] > prediction[0][1]:
        print(path + "    free")
    else:
        print(path + "    busy")