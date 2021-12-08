from flask import Flask, render_template, request, session, redirect, url_for,make_response
from datetime import timedelta, date
import os

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
	app.config['SESSION_TYPE'] = 'filesystem'

	app.run(debug=True, host='0.0.0.0')