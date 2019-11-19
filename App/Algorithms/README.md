# Algorithms

## CNN - Tensorflow
Deep Learning approach - Applying Convolutional Neural Networks to each parking spot.  
Keras model (with TensorFlow backend) was trained on `cnrpark.it` (patches) dataset.  
Predictions are made on images from 8th camera from `cnrpark.it`.

###### Run instructions
1. Download cnrpark dataset
    - dataset location is CNN-Tensorflow/dataset/free and CNN-Tensorflow/dataset/busy
2. Create venv and install all dependencies
    - virtualenv --system-site-packages -p python ./venv
    - pip install tensorflow
    - pip install opencv-python
    - pip install pillow
    - pip install tinydb
3. Run train.py to train the model
4. Run test.py to classify parking spots from /test_dataset (see output in /test_output)