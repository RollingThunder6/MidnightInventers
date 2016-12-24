from flask import render_template, session, redirect, url_for, flash, request
from . import main
from .forms import NameForm
import requests

@main.route("/", methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()

	param = request.args.get("redirect")
	if param == "True":
		session["name"] = False
		redirect(url_for("main.index"))

	if form.validate_on_submit():
		if form.password.data != "admin":
			flash("Password incorrect","error")
			return render_template("index.html", form=form, name=session.get("name")), 200		

		session["name"] = form.name.data
		form.name.data = ''
		flash("Succesfully logged in", "success")
		redirect(url_for("main.index"))
	return render_template("index.html", form=form, name=session.get("name")), 200

@main.route("/devices", methods=['GET'])
def devices():
	resp = requests.get("http://localhost:8002/web/jsonrest/host_tracker/devices")
	return render_template("devices.html", resp=resp.json(), name=session.get("name")), 200

@main.route("/switches", methods=['GET'])
def switches():
	resp = requests.get("http://localhost:8002/web/jsonrest/of/switches")
	return render_template("switches.html", resp=resp.json(), name=session.get("name")), 200

@main.route("/links", methods=['GET'])
def links():
	resp = requests.get("http://localhost:8002/web/jsonrest/discovery/links")
	return render_template("links.html", resp=resp.json(), name=session.get("name")), 200