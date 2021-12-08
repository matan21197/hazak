from keras.models import load_model
import numpy as np
import cv2 as cv

HEIGHT = 150
LOADED_MODEL = load_model("./ResNet50_model_weights.h5")

"""
This function gets a path to .jpg image 
and return true is the parking is free
"""
def is_free_parking(img_file: str, height: int = HEIGHT) -> bool:
    class_names = ["busy", "free"]
    img = cv.imread(img_file)
    img = cv.resize(img, (height, height), cv.INTER_CUBIC)
    conv = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    conv = np.expand_dims(conv, 0)
    st = LOADED_MODEL.predict(conv)
    model = np.argmax(st)
    return class_names[model] == "free"


if __name__ == "__main__":
    # f = round(time.time() * 1000)
    # for i in range(20):
    #     print(is_free_parking("hh.jpg"))
    #
    # s = t()
    # print("diff: " + str(s - f))
    pass
