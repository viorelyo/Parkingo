from flask import Flask, jsonify, render_template, request, redirect, url_for
from controller.repository import Repository
from controller.classify import predict
from controller.frame_capture import YoutubeVideoWrapper
from tinydb import TinyDB, Query
import time
from werkzeug.utils import secure_filename
import os
import json
import threading
import cv2
from PIL import Image

app = Flask(__name__)
start_time = None
configuration = None
yt_video_wrapper = None

@app.route('/')
def index():
    return render_template('index.html')

def update_prediction():
    while 1:
        yt_video_wrapper.set_seconds(int(time.time() - start_time))
        image = yt_video_wrapper.get_current_image()
        cv2.imwrite('frame.png', image)
        pil_image = Image.open('frame.png')
        predict('./controller/db.json', pil_image)
        time.sleep(configuration.get('timer'))

@app.route('/status', methods=['GET'])
def get_status():
    response = {}
    response['spots'] = TinyDB('./controller/db.json').all()
    response['elapsed'] = time.time() - start_time
    response['next_prediction'] = 30
    return jsonify(response)

if __name__ == '__main__':
    global configuration
    global repository
    global start_time
    global yt_video_wrapper
    start_time = time.time()
    with open('configuration.json', 'r') as file:
        configuration = json.load(file)
    yt_video_wrapper = YoutubeVideoWrapper(configuration.get('url'))
    update_thread = threading.Thread(target=update_prediction)
    update_thread.start()
    app.run(host= '0.0.0.0', port=5000)

