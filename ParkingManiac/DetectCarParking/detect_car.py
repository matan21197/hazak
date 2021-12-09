from keras.models import load_model
import numpy as np
import cv2 as cv


HEIGHT = 150
LOADED_MODEL = load_model("DetectCarParking/ResNet50_model_weights.h5")

"""
This function gets a image as a numpy array  
and return true if the parking in the image is free
"""
def is_free_parking(img) -> bool:
    class_names = ["busy", "free"]
    img = cv.resize(img, (HEIGHT, HEIGHT), cv.INTER_CUBIC)
    conv = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    conv = np.expand_dims(conv, 0)
    st = LOADED_MODEL.predict(conv)
    model = np.argmax(st)
    return class_names[model] == "free"
