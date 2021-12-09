from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import json

class Point:
    def __init__(self):
        self.position = None
        self.x = ""
        self.y = ""

    def init(self, position, x, y):
        self.position = position
        self.x = x
        self.y = y

    def init_str(self, str):
        j = json.loads(str)
        self.position = j['position']
        self.x = j['x']
        self.y = j['y']

    def toJson(self):
        points_json = '"x":{}, "y":{}'.format(self.x, self.y)
        return '"{}": "{}"'.format(self.position, "{" + points_json + "}")
    
class Parkinglot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, index=True, unique=False)
    description = db.Column(db.Text, index=True, unique=False)
    location = db.Column(db.Text, index=True, unique=False)
    img = db.Column(db.Text, index=True, unique=False)
    parks = db.relationship('Park', backref='parkinglot', lazy=False)

class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Boolean, index=True, unique=False)
    last_updated = db.Column(db.DateTime, index=True, unique=False)
    points = db.Column(db.Text, index=False, unique=False)
    parkinglot_id = db.Column(db.Integer, db.ForeignKey('parkinglot.id'), nullable=False)