links_json = links_rest.json()
switches_json = switches_rest.json()
devices_json = devices_rest.json()

topology_nodes = []
switch_id = []
pop_id = []

for entry in switches_json:
	topology_nodes.append(Topology_Node(entry["dpid"]))
	switch_id.append(entry["dpid"])

leaf_nodes = []
for entry in devices_json:
	if entry["switch_dpid"] in switch_id:
		temp_id = switch_id.pop(switch_id.index(entry["switch_dpid"]))
		leaf_nodes.append(temp_id)
pop_id.append(leaf_nodes)

intermediate_nodes = []
for entry in pop_id[0]:
	pop_counter = 0
	for link_entry in links_json:
		if link_entry["dataLayerDestination"] == entry:
			temp_id = switch_id.pop(switch_id.index(link_entry["dataLayerSource"]))
			links_json.pop(pop_counter)
			intermediate_nodes.append(temp_id)
		pop_counter = pop_counter + 1
pop_id.append(intermediate_nodes)