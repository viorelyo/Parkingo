import os
import numpy as np
import tensorflow as tf
from utils import img_to_array, unison_shuffled_copies
from config import *


def load_images(dataset_location):
	"""
	Prepare dataset for training
	"""
	global label_free, label_occupied
	samples_free = dataset_location + label_free
	samples_occupied = dataset_location + label_occupied

	images_free = os.listdir(samples_free)
	images_occupied = os.listdir(samples_occupied)
	global dataset_size, width, height, channels
	data_x = np.ndarray(shape=(dataset_size, width, height, channels), dtype=np.float32)
	data_y = np.ndarray(shape=(dataset_size), dtype=np.float32)

	i = 0
	errors = 0
	for img in images_free:
		img_path = samples_free + img

		try:
			img_arr = img_to_array(img_path)
			data_x[i] = img_arr
			data_y[i] = 0.
			i += 1
			print(i)
		except ValueError as e:
			print(e)
			print(img, '<--- Does not work')
			errors += 1
		if i == dataset_size / 2:
			break

	# Images containing occupied parking spots
	for img in images_occupied:
		img_path = samples_occupied + img

		try:
			img_arr = img_to_array(img_path)
			data_x[i] = img_arr
			data_y[i] = 1.
			i += 1
			print(i)
		except ValueError:
			print(img, '<--- Does not work')
			errors += 1
		if i == dataset_size:
			break

	data_x = np.array(data_x)
	data_y = np.array(data_y)

	if errors != 0:
		data_x = data_x[:-errors]
		data_y = data_y[:-errors]

	data_x, data_y = unison_shuffled_copies(data_x, data_y)

	return data_x, data_y


def train():
    global train_dataset
    data_x, data_y = load_images(train_dataset)
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(input_shape=(width, height, 3),filters=64,kernel_size=(3,3),padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2),strides=(2,2)),
        tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2),strides=(2,2)),
        tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2),strides=(2,2)),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2),strides=(2,2)),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2),strides=(2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=4096,activation="relu"),
        tf.keras.layers.Dense(units=4096,activation="relu"),
        tf.keras.layers.Dense(units=2, activation="softmax")
    ])

    checkpoint = tf.keras.callbacks.ModelCheckpoint("vgg16_1.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    early = tf.keras.callbacks.EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(data_x, data_y, steps_per_epoch=100, validation_split=0.33, validation_steps=10, epochs=100, callbacks=[checkpoint, early])
	# model.save('model.h5')
