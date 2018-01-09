# coding=utf-8
import os
import logging
from logging.handlers import RotatingFileHandler

import flask
import sendgrid
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from sendgrid.helpers.mail import Email, Content, Mail

# flask extensions
from flask_wtf.csrf import CsrfProtect
from flask_sendgrid import SendGrid

APP = Flask(__name__)
APP.config.from_object('config')

if os.environ.get('STORE_CONFIG') is not None:
    APP.config.from_envvar('STORE_CONFIG')

# Logging
handler = RotatingFileHandler(
    APP.config['LOG_FILE'], maxBytes=10000, backupCount=1)
if APP.config['DEBUG'] is not True:
    handler.setLevel(logging.INFO)
else:
    handler.setLevel(logging.DEBUG)
APP.logger.addHandler(handler)


# wtforms csrf
CsrfProtect(app=APP)

# import the modules to be used
import model
from model import engine, Base
import forms

SESSION = model.create_session(APP.config['DB_URL'], engine, Base)
EMAIL_BODY = APP.config['EMAIL_BODY']


@APP.route("/", methods=['GET', 'POST'])
def index():
    ''' Give out the form for preordering '''
    form = forms.DiscountForm()
    out = {'status': False, 'msg': ''}
    if form.validate_on_submit():
        # check if there is a user with the given email
        user = model.User.get_user_by_email(
            session=SESSION,
            emailid=form.data.get('email')
        )
        if user is not None:
            out['msg'] = (
                "There is already a user registered for "
                "discount with this email")
            APP.logger.warn(
                "Another attempt for discount of user: %s", user.email)
            return flask.jsonify(out)

        # add to the database
        user = model.User(
            name=form.data.get('name'),
            email=form.data.get('email'),
            contact=form.data.get('cellphone'),
            address=form.data.get('address'),
            token_used=False,
        )
        SESSION.add(user)
        try:
            SESSION.commit()
        except SQLAlchemyError as e:
            out['msg'] = 'Could not insert in database, some problem'
            APP.logger.error(
                "Problem inserting in database for user: %s", user.email)
            return flask.jsonify(out), 500
        out['status'] = True
        # get the user token from database and show it to the user
        user = model.User.get_user_by_email(
            session=SESSION,
            emailid=form.data.get('email')
        )
        # try sending the email
        try:
            sg = sendgrid.SendGridAPIClient(
                apikey=APP.config['SENDGRID_API_KEY'])
            from_email = Email(APP.config['SENDGRID_DEFAULT_FROM'])
            to_email = Email(form.data.get('email'))
            subject = 'Ethereal Ray: Discount Coupon Code'
            content = Content("text/html", EMAIL_BODY % (user, user.token))
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
        except Exception as e:
            APP.logger.error(
                'Failed sending email for %s', form.data.get('email'))
            APP.logger.error("The error was: %s", e)
            out['msg'] = (
                    'Failed to send email but, registered for discount'
                    'token is %s' % user.token)
        if response.status_code >= 300:
            out['msg'] = (
                    'Failed to send email but, registered for discount'
                    'token is %s' % user.token)
            return flask.jsonify(out), int(response.status_code)
        out['msg'] = 'Successfully stored the token and email sent'
        return flask.jsonify(out), 200
    if flask.request.is_xhr:
        out['success'] = False
        out['msg'] = 'Form Validation Failed'
        for fieldName, errorMessages in form.errors.items():
            APP.logger.debug("field: %s, error: %s", fieldName, errorMessages)
            out[fieldName] = errorMessages
        return flask.jsonify(out), 400
    return flask.render_template('index.html', form=form)

