""" 
Todo :- 
1. Include moment.js after adding user authentication
"""

# [ Import statements ]
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
import requests

app = Flask(__name__)
# [ Security against CSRF attacks using flask-wtf ]
app.config['SECRET_KEY'] = "rollingthunder6"
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
	"""Form element to be included"""
	name = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Submit')


# [ Application routes ]
@app.route("/", methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()

	param = request.args.get("redirect")
	if param == "True":
		session["name"] = False
		redirect(url_for("index"))

	if form.validate_on_submit():
		if form.password.data != "admin":
			flash("Password incorrect","error")
			return render_template("index.html", form=form, name=session.get("name")), 200		

		session["name"] = form.name.data
		form.name.data = ''
		flash("Succesfully logged in", "success")
		redirect(url_for("index"))
	return render_template("index.html", form=form, name=session.get("name")), 200

@app.route("/devices", methods=['GET'])
def devices():
	resp = requests.get("http://localhost:8002/web/jsonrest/host_tracker/devices")
	return render_template("devices.html", resp=resp.json(), name=session.get("name")), 200

@app.route("/switches", methods=['GET'])
def switches():
	resp = requests.get("http://localhost:8002/web/jsonrest/of/switches")
	return render_template("switches.html", resp=resp.json(), name=session.get("name")), 200

@app.route("/links", methods=['GET'])
def links():
	resp = requests.get("http://localhost:8002/web/jsonrest/discovery/links")
	return render_template("links.html", resp=resp.json(), name=session.get("name")), 200

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
	return render_template("500.html"), 500


		

# [ Start server ]
if __name__ == '__main__':
	app.run(debug=True)