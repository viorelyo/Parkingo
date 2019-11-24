import threading

global CNNModel
global VGGModel
global lock

from model import Model
from config import *

lock = threading.Lock()

def get_cnn_model():
	global CNNModel
	with lock:
		if CNNModel is None:
			CNNModel = Model()
			CNNModel.load_model(cnn_model_path)
		return CNNModel


def get_vgg_model():
	global VGGModel
	with lock:
		if VGGModel is None:
			VGGModel = Model()
			VGGModel.load_model_with_weights(vgg_model_json_path, vgg_weights_h5_path)
		return VGGModel