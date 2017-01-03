from flask import render_template, session, redirect, url_for, flash, request
from . import main
from .. import db
from ..models import Credentials
from .forms import NameForm, ChangeCredentials
import requests, json
import logging, sys, os, socket

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

@main.route("/devices", methods=['GET', 'POST'])
def devices():
	resp = requests.get("http://localhost:8002/web/jsonrest/host_tracker/devices")

	# [ 'Logging functionality' ]
	# logger = logging.getLogger(__name__)
	# logger.setLevel(logging.DEBUG)
	# root = logging.getLogger()
	# root.setLevel(logging.DEBUG)
	
	# ch = logging.StreamHandler(sys.stdout)
	# ch.setLevel(logging.DEBUG)
	# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# ch.setFormatter(formatter)
	# root.addHandler(ch)
	# logger.info()

	return render_template("devices.html", resp=resp.json(), name=session.get("name")), 200

@main.route("/switches", methods=['GET'])
def switches():
	resp = requests.get("http://localhost:8002/web/jsonrest/of/switches")
	return render_template("switches.html", resp=resp.json(), name=session.get("name")), 200

@main.route("/links", methods=['GET'])
def links():
	links_rest = requests.get("http://localhost:8002/web/jsonrest/discovery/links")
	switches_rest = requests.get("http://localhost:8002/web/jsonrest/of/switches")
	devices_rest = requests.get("http://localhost:8002/web/jsonrest/host_tracker/devices")
	
	links_json = links_rest.json()
	switches_json = switches_rest.json()
	devices_json = devices_rest.json()

	json_data = {"nodes":[], "links":[]}
	for switch in switches_json:
		data = {}
		data["group"] = "1"
		data["id"] = switch["dpid"]
		json_data["nodes"].append(data)

	for devices in devices_json:
		data = {}
		data["group"] = "2"
		data["id"] = devices["networkAddresses"]
		json_data["nodes"].append(data)

		link = {}
		link["target"] = devices["networkAddresses"]
		link["source"] = devices["switch_dpid"]
		link["value"] = "2"
		json_data["links"].append(link)

	for links in links_json:
		data = {}
		data["target"] = links["dataLayerDestination"]
		data["source"] = links["dataLayerSource"]
		data["value"] = "1"
		json_data["links"].append(data)

	with open("app/static/json/topo.json", 'w') as outfile:
		json.dump(json_data, outfile)
		
	return render_template("links.html", json_data=json_data, name=session.get("name")), 200

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

@main.route("/ddos", methods=['GET', 'POST'])
def ddos():
	if request.method == "POST":
		fw = open("app/static/json/attack_topo.json","w")
		fw.close()
		
	if os.stat("app/static/json/attack_topo.json").st_size == 0:
		return render_template("ddos.html", flag=False, name=session.get("name")), 200
	else:
		return render_template("ddos.html", flag=True, name=session.get("name")), 200