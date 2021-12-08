import numpy as np
import cv2
import time
import requests
import base64

IMAGE_CAPTURE_INTERVAL = 1
SERVER_URL = "localhost:5000/uploadImage"

def process_image(frame):
    mock_points = np.array([[10,700],[700,700],[700,10],[10,30]])
    rect = cv2.boundingRect(mock_points)
    x,y,w,h = rect
    cropped = frame[y:y+h, x:x+w].copy()

    mock_points = mock_points - mock_points.min(axis=0)

    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [mock_points], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit-op
    dst = cv2.bitwise_and(cropped, cropped, mask=mask)

    ## (4) add the white background
    bg = np.ones_like(cropped, np.uint8)*255
    cv2.bitwise_not(bg,bg, mask=mask)
    dst2 = bg + dst

    return dst2

def capture_image_for_interval(seconds):
    prev_time = time.time()
    cap = cv2.VideoCapture()
    cap.open(1, cv2.CAP_DSHOW)
    while(True):
        if(time.time() - prev_time > seconds):
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post("http://localhost:5000/uploadImage", data=img_encoded.tostring())
            cv2.imshow('frame', img_encoded)
            prev_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

capture_image_for_interval(IMAGE_CAPTURE_INTERVAL)