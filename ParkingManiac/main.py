from flask import Flask, render_template,request, session, copy_current_request_context, redirect, url_for, make_response, send_file
from datetime import timedelta, date
import os
from threading import Lock
import datetime
import json
import cv2
import numpy as np
from image_utils import process_image

from models.models import db
from models.models import Park, Parkinglot, Point

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

async_mode = None
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

with app.app_context():
    db.create_all()

"""
    point = Point()
    point.init(position=1,x=1,y=1)

    p = Parkinglot(name='admin2', description="desc2", location="yara2", img="y2")
    park = Park(available=True, last_updated=datetime.datetime.now(), parkinglot=p)
    db.session.add(p)
    db.session.add(park)
    db.session.commit()

"""

@app.route('/')
def index():
    return render_template('index.html')

# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count'],  'parking_img': 'static/img/owl1.jpg'})

# @socket_.on('get-image')
# def getImage():
#     emit('get-image', 'static/img/owl1.jpg', broadcast = True)

@app.route("/uploadImage", methods=['POST'])    
def getImage():
    image = request.data
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr,cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1

    print("received image ")
    processed_image = process_image(img_np)
    
    cv2.imshow('frame',processed_image)
    cv2.waitKey()
	# print(image)
    return "got image"


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')
