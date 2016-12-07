"""
Entropy based Discretization

Author - Midnight Inventers
"""

# [ Static initialisation of hosts connected directly to switch ]
# switch_ip = ["10.0.0.1", "10.0.0.2"]

fh = open("dummy.txt")

N = []

hash_flows = {}
# hash_flows = {'1000210001arp': ['cookie=0x0', ' duration=11.499s', ' table=0', ' n_packets=1', ' n_bytes=42', ' idle_timeout=60', ' idle_age=11', ' priority=65535', 'arp', 'in_port=2', 'vlan_tci=0x0000', 'dl_src=26:35:f9:6c:1e:14', 'dl_dst=b2:87:79:65:56:71', 'arp_spa=10.0.0.2', 'arp_tpa=10.0.0.1', 1, 0], '1000110002icmp': ['cookie=0x0', ' duration=15.511s', ' table=0', ' n_packets=10', ' n_bytes=980', ' idle_timeout=60', ' idle_age=7', ' priority=65535', 'icmp', 'in_port=1', 'vlan_tci=0x0000', 'dl_src=b2:87:79:65:56:71', 'dl_dst=26:35:f9:6c:1e:14', 'nw_src=10.0.0.1', 'nw_dst=10.0.0.2', 'nw_tos=0', 'icmp_type=8', 10, 0], '1000210001icmp': ['cookie=0x0', ' duration=16.512s', ' table=0', ' n_packets=10', ' n_bytes=980', ' idle_timeout=60', ' idle_age=7', ' priority=65535', 'icmp', 'in_port=2', 'vlan_tci=0x0000', 'dl_src=26:35:f9:6c:1e:14', 'dl_dst=b2:87:79:65:56:71', 'nw_src=10.0.0.2', 'nw_dst=10.0.0.1', 'nw_tos=0', 'icmp_type=0', 10, 0], '1000110002arp': ['cookie=0x0', ' duration=11.498s', ' table=0', ' n_packets=1', ' n_bytes=42', ' idle_timeout=60', ' idle_age=11', ' priority=65535', 'arp', 'in_port=1', 'vlan_tci=0x0000', 'dl_src=b2:87:79:65:56:71', 'dl_dst=26:35:f9:6c:1e:14', 'arp_spa=10.0.0.1', 'arp_tpa=10.0.0.2', 1, 0]}


# [ Hash function by indexing based on src + dst + protocol ]
def hash_function():
	global hash_flows	

	fh = open("dummy.txt")

	if hash_flows == {}:
		i = 0
		for flow_entry in fh:
			if i != 0:
				flow_entry = flow_entry.strip().split(",")
				
				src_ip = flow_entry[13].split("=")
				dst_ip = flow_entry[14].split("=")
				
				src_ip_val = src_ip[1].split(".")
				dst_ip_val = dst_ip[1].split(".")
				
				src = "".join(src_ip_val)
				dst = "".join(dst_ip_val)
				
				val = src + dst + flow_entry[8]	

				# [ Filtering src ip and dst ip from flow table ]
				# src_ip = line[13].split("=")
				# dst_ip = line[14].split("=")

				# [ Adding rp_local to flow entry depending on whether host is present or not ]
				# if src_ip[1] in switch_ip and dst_ip[1] in switch_ip:	
				# 	rp_local.append(0)
				# else:
				# 	rp_local.append(-1)

				# [ rp_local attribute added without checking ]
				flow_entry.append(0)
				
				hash_flows[val] = flow_entry		
			i = i + 1
	else:
		i = 0
		for flow_entry in fh:
			if i != 0:
				flow_entry = flow_entry.strip().split(",")
				
				src_ip = flow_entry[13].split("=")
				dst_ip = flow_entry[14].split("=")
				
				src_ip_val = src_ip[1].split(".")
				dst_ip_val = dst_ip[1].split(".")
				
				src = "".join(src_ip_val)
				dst = "".join(dst_ip_val)
				
				val = src + dst + flow_entry[8]	

				if val in hash_flows:
					received_packets = flow_entry[3].split("=")
					received_packets = int(received_packets[1])
					hash_flows[val][3] = "n_packets="+str(received_packets)
				else:
					flow_entry.append(0)
					hash_flows[val] = flow_entry

			i = i + 1	

	fh.close()

def main():
	# [ packet count calculation for delta_t ]

	global N
	global hash_flows
	i = 0
	m = 0
	w = 5
	program_counter = 0

	while program_counter != 2:
		if program_counter != 0:
			hash_function()

			for hash_value, flow in hash_flows.items():
				received_packets = flow[3].split("=")
				received_packets = int(received_packets[1])

				rp_local = int(flow[-1:][0])

				num_packets = received_packets - rp_local
				rp_local = received_packets
				hash_flows[hash_value].pop(hash_flows[hash_value].__len__() - 2)
				hash_flows[hash_value].insert(hash_flows[hash_value].__len__() - 1, rp_local)

				i = i + 1
				N.append(num_packets)

			print(hash_flows)

		program_counter = program_counter + 1

if __name__ == '__main__':
	main()