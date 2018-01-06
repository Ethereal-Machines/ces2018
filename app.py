# coding=utf-8
import flask
from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def index():
    ''' Give out the form for preordering '''
    return flask.render_template('index.html')
