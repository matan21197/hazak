from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from DetectCarParking import detect_car

from image_utils import process_image
from models.models import db
from models.models import Parkinglot

IMAGE_DIR = os.path.abspath('./images')
TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

image_counter = 0

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
    return render_template('beta.html')


# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count'],  'parking_img': 'static/img/owl1.jpg'})

# @socket_.on('get-image')
# def getImage():
#     emit('get-image', 'static/img/owl1.jpg', broadcast = True)

@app.route("/uploadImage/<name>", methods=['POST'])
def getImage(name):
    global image_counter
    image_counter += 1

    image = request.data
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    print("received image ")
    save_image(img_np, name)
    # asd = cv2.imshow('frame', img_np)
    # cv2.waitKey()

    parking_lot = getParkingLot('admin')
    if parking_lot is None:
        create_parking_lot(name, image)
    else:
        if image_counter % 3 == 0:
            update_parking_lot(name, image)
            image_counter = 0
    # print(image)
    return "got image"


@app.route("/initImage/<name>", methods=['POST'])
def split_into_parking_spots(name):
    # todo: admin page + update db
    return ""


@app.route("/initImage/<name>", methods=['POST'])
def get_parkinglot(name):
    return


def create_parking_lot(name, image):
    path = save_image(image, name)
    p = Parkinglot(name=name, points="", description="desc2", location="location", img=path)
    db.session.add(p)
    db.session.commit()


# updates in the db the available parks
def get_availables(image, name):
    parking_lot = Parkinglot.query.filter_by(name=name).first()
    image = parking_lot.img
    for park in parking_lot.parks:
        park.available = is_available(image, park.points)
    db.session.commit()


def is_available(image, points):
    points = points.split("'")
    img_np = cv2.imread(image)
    processed_image = process_image(img_np, points)
    # todo: send processed_image to the ai thing
    # Note: image should be numpy array !!!!
    return detect_car.is_free_parking(image)


def update_parking_lot(name, image):
    parking_lot = Parkinglot.query.filter_by(name=name).first()
    parking_lot.img = image
    db.session.commit()
    get_availables(image, name)


"""
This function gets an image in !! bytes !!
and saves the image as a file and returns the path
"""
def save_image(image: bytes, name: str):
    path = str(IMAGE_DIR) + "\\" + str(image_counter) + "_" + str(name) + ".jpg"
    with open(path, "wb") as f:
        f.write(image)
    return path


def getParkingLot(name):
    return Parkinglot.query.filter_by(name=name).first()


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')
