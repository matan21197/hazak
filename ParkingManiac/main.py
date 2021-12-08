from flask import Flask, render_template, request, session, redirect, url_for,make_response
from datetime import timedelta, date
import os
import datetime
import json

from models.models import db
from models.models import Park, Parkinglot, Point

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    point = Point()
    point.init(position=1,x=1,y=1)

    p = Parkinglot(name='admin2', description="desc2", location="yara2", img="y2")
    park = Park(available=True, last_updated=datetime.datetime.now(), parkinglot=p)
    db.session.add(p)
    db.session.add(park)
    db.session.commit()

    return render_template("index.html")

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')