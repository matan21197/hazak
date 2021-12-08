from flask import Flask, render_template, session, copy_current_request_context, redirect, url_for, make_response, send_file
from datetime import timedelta, date
import os
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import datetime
import json

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

socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

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
    return render_template('index.html', async_mode=socket_.async_mode)

@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
	#ARAD TODO: try Print
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'],  'parking_img': 'static/img/owl1.jpg'})

@socket_.on('get-image')
def getImage():
    emit('get-image', 'static/img/owl1.jpg', broadcast = True)

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')
