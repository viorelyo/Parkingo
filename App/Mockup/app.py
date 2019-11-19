from flask import Flask, jsonify, render_template, request, redirect, url_for
from controller.repository import Repository
import time
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spots', methods=['GET'])
def get_spots():
    repo = Repository()
    spots = repo.get_all()
    # time.sleep(5)
    return jsonify(spots)


@app.route('/upload', methods=['POST'])
def upload_frame():
    if request.files['file']:
        frame = request.files['file']
        filename = secure_filename(frame.filename)
        destination = os.path.join('.', filename)
        print(destination)
        frame.save(destination)
        return "done"


if __name__ == '__main__':
    app.run(debug=True, port=5000)