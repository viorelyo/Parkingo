# Algorithms

<p align="center"><img src="./images/logo.jpg" width="500"></p>  

## CNN - Tensorflow
Deep Learning approach - Applying Convolutional Neural Networks to each parking spot.  
Keras model (with TensorFlow backend) was trained on `cnrpark.it` (patches) dataset.  
Predictions are made on images from 8th camera from `cnrpark.it`.

###### Run instructions
1. Download cnrpark dataset
    - dataset location is CNN-Tensorflow/dataset/free and CNN-Tensorflow/dataset/busy
2. Create venv and install all dependencies
    - virtualenv --system-site-packages -p python ./venv
    - ./venv/Scripts/activate
    - pip install tensorflow
    - pip install opencv-python
    - pip install pillow
    - pip install tinydb
    - pip install flask
    - pip install flask_cors
    - pip install matplotlib
    - pip install pafy
    - pip install youtube_dl
3. For training the model:
    - call train() from model.py
4. For testing the model:
    - Download cnrpark+ext dataset and select some images from the 8th camera taken in sunny weather.
    - Put those images in test_dataset/S
    - Put camera8_boxes.csv and camera8_labels.txt in test_dataset/
    - Run test.py and access test_output to see the results