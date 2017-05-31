import socket
import json

s = socket.socket()
host = socket.gethostname()
port = 13411

s.connect((host, port))

while True:
	data = s.recv(1024).decode()
	fh = open("../Flask/app/static/json/topo.json")
	json_data = json.load(fh)
	for node in json_data["nodes"]:
		if node["id"] == data:
			node["group"] = "3"
	outfile = open("../Flask/app/static/json/attack_topo.json","w")
	json.dump(json_data, outfile)
	outfile.close()
	fh.close()