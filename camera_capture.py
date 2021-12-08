import numpy as np
import cv2
import time
import requests



def capture_image_for_interval(seconds):
    prev_time = time.time()
    cap = cv2.VideoCapture()
    cap.open(1, cv2.CAP_DSHOW)
    while(True):
        if(time.time() - prev_time > seconds):
            ret, frame = cap.read()
            # frame = process_image(frame)
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:5000/uploadImage", data=img_encoded.tostring())
            print(response.status_code)
            # cv2.imshow('frame', frame)
            prev_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

capture_image_for_interval(1)