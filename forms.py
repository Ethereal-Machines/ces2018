from flask_wtf.recaptcha import RecaptchaField
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired
from flask_wtf import Form

class DiscountForm(Form):
    ''' The form to fill for getting pre-order discount '''

    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    address = TextAreaField("address", validators=[DataRequired()])
    cellphone= StringField("cellphone", validators=[DataRequired()])
