# coding=utf-8
import os

import flask
from flask import Flask
from flask_wtf.csrf import CsrfProtect

APP = Flask(__name__)
APP.config.from_object('config')

if os.environ.get('STORE_CONFIG') is not None:
    APP.config.from_envvar('STORE_CONFIG')
CsrfProtect(app=APP)

import model
from model import engine, Base
import forms

SESSION = model.create_session(APP.config['DB_URL'], engine, Base)

@APP.route("/", methods=['GET'])
def index():
    ''' Give out the form for preordering '''
    form = forms.DiscountForm()
    return flask.render_template('index.html', form=form)


@APP.route("/getcoupon", methods=['POST'])
@APP.route("/getcoupon/", methods=['POST'])
def get_coupon():
    ''' Verify the form and register the user for getting coupon '''
    form = forms.DiscountForm()
    if form.validate_on_submit():
        # add to the database
        print 'coming here bro'
        return "land raaj"
    for fieldName, errorMessages in form.errors.items():
        print "field: %s, error: %s" % (fieldName, errorMessages)
    return 'lauda'
