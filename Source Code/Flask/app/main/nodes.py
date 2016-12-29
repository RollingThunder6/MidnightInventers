class Node():
	"""Class definition for individual switch node"""
	def __init__(self, addr, port_num, datapath_id):
		self.address = addr
		self.port = port_num
		self.dpid = datapath_id
		self.children = []