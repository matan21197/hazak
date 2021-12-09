import json

import cv2
import numpy as np
from models.models import Point


def process_image(frame, points):
    mock_points = json_points_to_numpy_points(points)
    rect = cv2.boundingRect(mock_points)
    x, y, w, h = rect
    cropped = frame[y:y + h, x:x + w].copy()

    mock_points = mock_points - mock_points.min(axis=0)

    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [mock_points], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit-op
    dst = cv2.bitwise_and(cropped, cropped, mask=mask)

    ## (4) add the white background
    bg = np.ones_like(cropped, np.uint8) * 255
    cv2.bitwise_not(bg, bg, mask=mask)
    dst2 = bg + dst

    return dst2


def json_points_to_numpy_points(points):
    points = "{" + points + "}"
    points_json = json.loads(points)
    a = [
        [points_json['1']['x'], points_json['1']['y']],
        [points_json['2']['x'], points_json['2']['y']],
        [points_json['3']['x'], points_json['3']['y']],
        [points_json['4']['x'], points_json['4']['y']]
    ]

    return a
