class Topology_Node():
	"""Class definition for individual node in a given topology"""
	def __init__(self, addr):
		self.addr = addr
		self.parent = []