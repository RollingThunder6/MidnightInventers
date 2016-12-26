from flask import render_template, session, redirect, url_for, flash, request
from . import main
from .. import db
from ..models import Credentials
from .forms import NameForm, ChangeCredentials
from .topology import Topology_Node
import requests

"""External functions"""
def delete_link(links_json, rev_destination, rev_source):
	"""Delete link reversing source and destination"""
	link_counter = 0
	for entry in links_json:
		if rev_source == entry["dataLayerSource"] and rev_destination == entry["dataLayerDestination"]:
			return link_counter
		link_counter = link_counter + 1

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
	links_rest = requests.get("http://localhost:8002/web/jsonrest/discovery/links")
	switches_rest = requests.get("http://localhost:8002/web/jsonrest/of/switches")
	devices_rest = requests.get("http://localhost:8002/web/jsonrest/host_tracker/devices")
	
	links_json = links_rest.json()
	switches_json = switches_rest.json()
	devices_json = devices_rest.json()

	topology_nodes = []
	switch_id = []
	switch_nodes = []

	for entry in switches_json:
		switch_id.append(entry["dpid"])

	for entry in devices_json:
		if entry["switch_dpid"] in switch_id:
			temp_id = switch_id.pop(switch_id.index(entry["switch_dpid"]))
			switch_nodes.append(temp_id)

	while links_json.__len__() != 0:
		new_switch_nodes = []
		for node in switch_nodes:
			link_counter = 0
			for entry in links_json:
				if node == entry["dataLayerDestination"]:
					destination = entry["dataLayerDestination"]
					source = entry["dataLayerSource"]
					links_json.pop(link_counter)
					index = delete_link(links_json, source, destination)
					links_json.pop(index)
					if source not in new_switch_nodes:
						new_switch_nodes.append(source)
					break

				link_counter = link_counter + 1
		
		switch_nodes = []
		switch_nodes.extend(new_switch_nodes)

	return render_template("links.html", switch_nodes=switch_nodes, resp=resp.json(), name=session.get("name")), 200

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