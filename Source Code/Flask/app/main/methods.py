"""External functions"""
def delete_link(links_json, rev_destination, rev_source):
	"""Delete link reversing source and destination"""
	link_counter = 0
	for entry in links_json:
		if rev_source == entry["dataLayerSource"] and rev_destination == entry["dataLayerDestination"]:
			return link_counter
		link_counter = link_counter + 1