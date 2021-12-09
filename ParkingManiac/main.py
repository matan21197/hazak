from datetime import datetime
from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
#from DetectCarParking import detect_car
import json
from datetime import datetime


from ParkingManiac.DetectCarParking import detect_car

from image_utils import process_image, json_points_to_numpy_points
from models.models import db, Point, Park
from models.models import Parkinglot

STATIC_DIR = os.path.abspath('./static')
IMAGE_DIR = os.path.abspath('./static/images')
TEMPLATE_DIR = os.path.abspath('./templates')

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

@app.route('/points')
def points():
    r = json_points_to_numpy_points('"1": {"x":0, "y":0}, "2": {"x":0, "y":100}, "3": {"x":100, "y":100}, "4": {"x":100, "y":0}')
    print(r)
    return ""
    # return jsonify([
	# 		{
	# 			"available": "true",
	# 			"1": {'x': 0, 'y': 0},
	# 			"2": {'x': 0, 'y': 100},
	# 			"3": {'x': 100, 'y': 100},
	# 			"4": {'x': 100, 'y': 0}
	# 		}, {
	# 			"available": "false",
	# 			"1": {'x': 100, 'y': 100},
	# 			"2": {'x': 100, 'y': 200},
	# 			"3": {'x': 200, 'y': 200},
	# 			"4": {'x': 200, 'y': 100}
	# 		}
	# 	]
	# )

# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count'],  'parking_img': 'static/img/owl1.jpg'})

# @socket_.on('get-image')
# def getImage():
#     emit('get-image', 'static/img/owl1.jpg', broadcast = True)

@app.route("/uploadImage/<name>", methods=['POST'])
def uploadImage(name):
    global image_counter
    image_counter += 1

    image = request.data
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    print("received image ")
    newPath = save_image(img_np, name)
    # asd = cv2.imshow('frame', img_np)
    # cv2.waitKey()

    parking_lot = getParkingLot(name)

    if parking_lot is None:
        createParkinglot(image, name)
    else:
        update_parking_lot(name, newPath)
        if image_counter % 3 == 0:
            #update_parks(name, newPath)
            image_counter = 0

    return "got image"


@app.route("/initImage/<name>", methods=['POST'])
def split_into_parking_spots(name):
    # todo: admin page + update db
    return ""


@app.route("/getParks/<name>/parks")
def get_parkinglot_parks(name):
    parkinglot = Parkinglot.query.filter_by(name=name).first()
    parks_jsons = []
    for park in parkinglot.parks:
        a = '{"available":'
        a += '"{}",{}'.format(park.available, park.points)
        a += "}"
        parks_jsons.append(a)
    final_json = '[{}]'.format(",".join(parks_jsons))
    print(final_json)
    return jsonify(final_json)

@app.route("/getParks/<name>/img")
def get_parkinglot_image(name):
    parkinglot = Parkinglot.query.filter_by(name=name).first()
    print(parkinglot.img)
    return jsonify(image='static/images/' + parkinglot.img.split("\\static\\images\\", 1)[1])

@app.route("/getParks/<name>")
def get_parks(name):
    # select from db
    parkinglot = Parkinglot.query.filter_by(name=name).first()
    parks_jsons = []
    print("name!!!!!!!!1"+name)
    image = '"image: "' + parkinglot.img + '"'
    parks_jsons.append(image)
    for park in parkinglot.parks:
        print(park.points)
        a = '"m": {"available":'
        a += '"{}",{}'.format(park.available, park.points)
        a += "}"
        parks_jsons.append(a)

    final_json = '[{}]'.format(",".join(parks_jsons))
    print(final_json)
    return json.dumps(final_json)


# updates in the db the available parks
def get_availables(name):
    parking_lot = Parkinglot.query.filter_by(name=name).first()
    image = parking_lot.img
    for park in parking_lot.parks:
        park.available = is_available(image, park.points)
    db.session.commit()


def is_available(image, points):
    img_np = cv2.imread(image)
    processed_image = process_image(img_np, points)
    # Note: image should be numpy array !!!!
    return detect_car.is_free_parking(processed_image)



def update_parking_lot(name, newPath):
    parking_lot = Parkinglot.query.filter_by(name=name).first()
    parking_lot.img = newPath
    db.session.commit()
    get_availables(name)


"""
This function gets an image in !! bytes !!
and saves the image as a file and returns the path
"""
def save_image(image: bytes, name: str):
    now = datetime.now().time()  # time object

    path = str(IMAGE_DIR) + "\\" + str(now) + "_" + str(name) + ".jpg"
    # with open(path, "wb") as f:
    #     f.write(image)
    #
    cv2.imwrite(path, image)

    return path


def getParkingLot(name):
    return Parkinglot.query.filter_by(name=name).first()

def createParkinglot(image, name):
    randomdb(image, name)


def randomdb(image, name):
    point1 = Point()
    point2 = Point()
    point3 = Point()
    point4 = Point()
    point1.init(position=1, x=2, y=1)
    point2.init(position=2, x=1, y=1)
    point3.init(position=3, x=3, y=1)
    point4.init(position=4, x=4, y=1)

    points1 = [point1.toJson(), point2.toJson(), point3.toJson(), point4.toJson()]

    path = save_image(image, name)
    p = Parkinglot(name=name, description="desc2", location="location", img=path)
    db.session.add(p)
    park1 = Park(available=True, last_updated=datetime.now(), parkinglot=p, points=",".join(points1))

    db.session.add(park1)
    #db.session.add(park2)
    db.session.commit()



    """
    parks_jsons = []

    for park in parkinglot.parks:
        print(park.points)
        a = '{"available":'
        a += '"{}",{}'.format(park.available, park.points)
        a += "}"
        parks_jsons.append(a)
    final_json = '[\n{}\n]'.format(",".join(parks_jsons))
    """
    #print("jhjhdgjsfghds"+final_json)




if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')
