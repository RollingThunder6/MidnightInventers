"""
Entropy based Discretization

Author - Midnight Inventers
"""

# [ Static initialisation of hosts connected directly to switch ]
# switch_ip = ["10.0.0.1", "10.0.0.2"]

fh = open("dummy.txt")

flows = []
N = []

flows_temp = {}

# Hash function by indexing based on src + dst + protocol
def hash_function(flow_entry):
	global flows_temp

	flow_entry = flow_entry.strip().split(",")
	
	src_ip = flow_entry[13].split("=")
	dst_ip = flow_entry[14].split("=")
	
	src_ip_val = src_ip[1].split(".")
	dst_ip_val = dst_ip[1].split(".")
	
	src = "".join(src_ip_val)
	dst = "".join(dst_ip_val)
	
	val = src + dst + flow_entry[8]	
	
	flows_temp[val] = flow_entry

def generate_flows():

	fh = open("dummy.txt")
	i = 0
	for line in fh:
		if i != 0:
			hash_function(line)


			# [ Filtering src ip and dst ip from flow table ]
			# src_ip = line[13].split("=")
			# dst_ip = line[14].split("=")

			# [ Adding rp_local to flow entry depending on whether host is present or not ]
			# if src_ip[1] in switch_ip and dst_ip[1] in switch_ip:	
			# 	rp_local.append(0)
			# else:
			# 	rp_local.append(-1)

			# [ rp_local attribute added without checking ]
			





			# if line[-1:][0] != True:

			# 	# rp_local added in flow entry
			# 	line.append(0)
			# 	line.append(True)

			# flows.append(line)
		i = i + 1			

def main():
	# packet count calculation for delta_t









	# global N
	# i = 0
	# m = 0
	# w = 5

	# while True:
	# 	generate_flows()

	# 	for flow in flows:
	# 		received_packets = flow[3].split("=")
	# 		received_packets = int(received_packets[1])

	# 		num_packets = received_packets - rp_local[i]
	# 		rp_local[i] = received_packets
	# 		i = i + 1
	# 		N.append(num_packets)








	global flows_temp


	generate_flows()

	print(flows_temp)


if __name__ == '__main__':
	main()