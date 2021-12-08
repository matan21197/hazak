import numpy as np
import cv2
import time



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
    cv2.imwrite("cropped.png", cropped)
    cv2.imwrite("mask.png", mask)
    cv2.imwrite("dst.png", dst)
    cv2.imwrite("dst2.png", dst2)
    return dst2

def capture_image_for_interval(seconds):
    prev_time = time.time()
    cap = cv2.VideoCapture()
    cap.open(1, cv2.CAP_DSHOW)
    while(True):
        if(time.time() - prev_time > seconds):
            ret, frame = cap.read()
            frame = process_image(frame)
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            cv2.imshow('frame', frame)
            prev_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

capture_image_for_interval(1)