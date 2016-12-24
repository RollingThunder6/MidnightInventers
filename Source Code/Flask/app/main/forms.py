from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

class NameForm(FlaskForm):
	"""Class for configuring login form"""
	name = StringField('Username :', validators=[Required()])
	password = PasswordField('Password :', validators=[Required()])
	submit = SubmitField('Submit')

class ChangeCredentials(FlaskForm):
	"""Class for configuring change credentials form"""
	new_name = StringField('New Username :')
	old_pass = PasswordField('Old Password :', validators=[Required()])
	new_pass = PasswordField('New Password :', validators=[Required()])
	submit = SubmitField('Update')