"""
Entropy based Discretization

Author - Midnight Inventers
"""

from time import sleep
from math import log, sqrt
from os import system

# [ Static initialisation of hosts connected directly to switch ]
# switch_ip = ["10.0.0.1", "10.0.0.2"]

N = {}
hash_flows = {}
# hash_flows = {'1000210001arp': ['cookie=0x0', ' duration=11.499s', ' table=0', 'n_packets=1', ' n_bytes=42', ' idle_timeout=60', ' idle_age=11', ' priority=65535', 'arp', 'in_port=2', 'vlan_tci=0x0000', 'dl_src=26:35:f9:6c:1e:14', 'dl_dst=b2:87:79:65:56:71', 'arp_spa=10.0.0.2', 'arp_tpa=10.0.0.1', 'arp_op=1 actions=output:1', 1], '1000110002icmp': ['cookie=0x0', ' duration=15.511s', ' table=0', 'n_packets=30', ' n_bytes=980', ' idle_timeout=60', ' idle_age=7', ' priority=65535', 'icmp', 'in_port=1', 'vlan_tci=0x0000', 'dl_src=b2:87:79:65:56:71', 'dl_dst=26:35:f9:6c:1e:14', 'nw_src=10.0.0.1', 'nw_dst=10.0.0.2', 'nw_tos=0', 'icmp_type=8', 'icmp_code=0 actions=output:2', 30], '1000110002arp': ['cookie=0x0', ' duration=11.498s', ' table=0', 'n_packets=1', ' n_bytes=42', ' idle_timeout=60', ' idle_age=11', ' priority=65535', 'arp', 'in_port=1', 'vlan_tci=0x0000', 'dl_src=b2:87:79:65:56:71', 'dl_dst=26:35:f9:6c:1e:14', 'arp_spa=10.0.0.1', 'arp_tpa=10.0.0.2', 'arp_op=2 actions=output:2', 1], '1000210001icmp': ['cookie=0x0', ' duration=16.512s', ' table=0', 'n_packets=30', ' n_bytes=980', ' idle_timeout=60', ' idle_age=7', ' priority=65535', 'icmp', 'in_port=2', 'vlan_tci=0x0000', 'dl_src=26:35:f9:6c:1e:14', 'dl_dst=b2:87:79:65:56:71', 'nw_src=10.0.0.2', 'nw_dst=10.0.0.1', 'nw_tos=0', 'icmp_type=0', 'icmp_code=0 actions=output:1', 30], '1000110002tcp': ['cookie=0x0', ' duration=7.173s', ' table=0', 'n_packets=20970', ' n_bytes=1384040', ' idle_timeout=60', ' idle_age=6', ' priority=0', 'tcp', 'in_port=1', 'vlan_tci=0x0000', 'dl_src=ae:68:a4:1e:33:98', 'dl_dst=c2:78:90:88:16:b6', 'nw_src=10.0.0.1', 'nw_dst=10.0.0.2', 'nw_tos=0', 'tp_src=5001', 'tp_dst=51289 actions=output:2', 20970]}

# [ Hash function by indexing based on src + dst + protocol ]
def hash_function():
	global hash_flows	

	system("sudo ovs-ofctl dump-flows s1 > dummy.txt")
	try:
		fh = open("dummy.txt")
	except FileNotFoundError as e:
		print("Flow table file not found. Exiting application with code -1")
		exit(-1)

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
				
				val = src + "/" + dst + flow_entry[8]

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
				
				val = src + "/" + dst + flow_entry[8]

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
	X = {}
	program_counter = 0
	entropy = 0
	total_packet_count = 0
	prev_entropy = []

	# Variables that need to be adjusted based on working environment
	m = 3
	w = 5
	ddos_detect_counter = 0
	delta_t = 2
	threshold = 0
	standard_entropy = 0.5
	alpha = [0.04, 0.11, 0.19, 0.28, 0.38]
	deviation = 0
	multiplication_factor = 1

	while True:
		N = {}
		X = {}
		entropy = 0
		total_packet_count = 0

		if program_counter != 0:
			hash_function()

			for hash_value, flow in hash_flows.items():
				received_packets = flow[3].split("=")
				received_packets = int(received_packets[1])

				rp_local = int(flow[-1:][0])

				num_packets = received_packets - rp_local
				rp_local = received_packets
				hash_flows[hash_value].pop(hash_flows[hash_value].__len__() - 1)
				hash_flows[hash_value].insert(hash_flows[hash_value].__len__(), rp_local)

				N[hash_value] = num_packets
				
			# [ Clubbing similar keys into a single unit ]
			for hash_value, packet_count in N.items():
				hash_key = hash_value.split("/")
				club_key = hash_key[1]
				if club_key in X:
					X[club_key] = X[club_key] + packet_count
				else:
					X[club_key] = packet_count
				total_packet_count = total_packet_count + X[club_key]

			# [ Calculating entropy ]
			for club_key, club_value in X.items():
				try:
					probability_val = float(club_value/total_packet_count)
				except ZeroDivisionError as e:
					probability_val = 1
				
				try:
					entropy = entropy + (-(probability_val * log(probability_val, 10)))					
				except ValueError as e:
					print("-1")

			# [ Normalising entropy ]
			try:
				entropy = entropy / (log(N.__len__(), 10))
			except (ZeroDivisionError, ValueError) as e:
				print("-2")

			prev_entropy.append(entropy)

			# [ Detection of DDoS ]
			if standard_entropy - entropy > threshold:
				ddos_detect_counter = ddos_detect_counter + 1

				if (program_counter + 1) % w == 0:
					ddos_detect_counter = 0

				if ddos_detect_counter == m:
					print("DDoS detected")

			# [ Standard entropy adaptation ]
			if prev_entropy.__len__() > 5:
				prev_entropy.pop(0)
				standard_entropy = 0
				deviation = 0
				deviation_sum = 0

				# [ Calculating mean entropy ]
				for entropy_index in range(0,prev_entropy.__len__()):
					standard_entropy = standard_entropy + (alpha[entropy_index] * prev_entropy[entropy_index])

				# [ Calculating standard deviation ]
				for entropy_index in range(0,prev_entropy.__len__()):
					deviation_sum = deviation_sum + ((prev_entropy[entropy_index] - standard_entropy) ** 2)
					deviation = sqrt(deviation_sum/prev_entropy.__len__())
					threshold = deviation * multiplication_factor

		# [ Waiting for delta_t time ]
		print("Sleeping - 2s")
		sleep(delta_t)
		program_counter = program_counter + 1

if __name__ == '__main__':
	main()
