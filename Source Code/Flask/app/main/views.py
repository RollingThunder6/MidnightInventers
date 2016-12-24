from flask import render_template, session, redirect, url_for, flash, request
from . import main
from .. import db
from ..models import Credentials
from .forms import NameForm, ChangeCredentials
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
		credential_query = Credentials.query.filter_by(username=form.name.data, password=form.password.data)
		credential = credential_query.first()
		credential_count = credential_query.count()

		if credential_count != 1:
			flash("Credentials Incorrect. Access denied.","error")
			return render_template("index.html", form=form, name=session.get("name")), 200					

		session["name"] = form.name.data
		form.name.data = ""
		flash("Succesfully logged in.", "success")
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

@main.route("/credentials", methods=['GET', 'POST'])
def credentials():
	form = ChangeCredentials()
	nameform = NameForm()
	if form.validate_on_submit():
		new_name = form.new_name.data
		new_pass = form.new_pass.data
		old_pass = form.old_pass.data

		credential_query = Credentials.query.filter_by(password=old_pass)
		if credential_query.count() == 1:
			credential = credential_query.first()
			credential.password = new_pass
			if new_name != "":
				credential.username = new_name
				session["name"] = new_name
				flash("Credentials changed successfully.","success")
			else:
				flash("Credentials changed successfully without changing username.","success")

			redirect(url_for("main.index"))
			return render_template("index.html", form=nameform, name=session.get("name")), 200
		else:
			flash("Incorrect old password. Access denied.","error")
			redirect(url_for("main.credentials"))

	return render_template("credentials.html", form=form, name=session.get("name")), 200