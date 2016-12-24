from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

class NameForm(FlaskForm):
	"""Class for configuring form"""
	name = StringField('Username :', validators=[Required()])
	password = PasswordField('Password :', validators=[Required()])
	submit = SubmitField('Submit')