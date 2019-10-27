# Algorithms

## CNN - Tensorflow
Deep Learning approach - Applying Convolutional Neural Networks to each parking spot.  
Keras model (with TensorFlow backend) was trained on `cnrpark.it` (patches) dataset.  
Predictions are made on images from 8th camera from `cnrpark.it`.

###### Run instructions
1. Download cnrpark dataset
2. Create venv and install all dependencies
3. Run filter_dataset.py
4. Run main.py  with model.train
5. Run main.py  with classify.update
6. Run show_spots.py