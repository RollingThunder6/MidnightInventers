"""
Entropy based Discretization

Author - Midnight Inventers

Program for calculation of standard entropy values.
"""

from time import sleep
from math import log, sqrt
from os import system

N = {}
hash_flows = {}

# [ Hash function by indexing based on src + dst + protocol ]
def hash_function():
	global hash_flows	

	system("sudo ovs-ofctl dump-flows tcp:127.0.0.1:6634 > dummy.txt")
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
	delta_t = 2

	while True:
		N = {}
		X = {}
		entropy = 0
		total_packet_count = 0

		if program_counter != 0:
			hash_function()
			print("Program Counter :",program_counter)
			print("")

			for hash_value, flow in hash_flows.items():
				received_packets = flow[3].split("=")
				received_packets = int(received_packets[1])

				rp_local = int(flow[-1:][0])

				num_packets = received_packets - rp_local
				rp_local = received_packets
				hash_flows[hash_value].pop(hash_flows[hash_value].__len__() - 1)
				hash_flows[hash_value].insert(hash_flows[hash_value].__len__(), rp_local)

				N[hash_value] = num_packets
			
			print("N Dictionary :")
			print(N)
			print("")

			# [ Clubbing similar keys into a single unit ]
			for hash_value, packet_count in N.items():
				hash_key = hash_value.split("/")
				club_key = hash_key[1]
				if club_key in X:
					X[club_key] = X[club_key] + packet_count
				else:
					X[club_key] = packet_count
				total_packet_count = total_packet_count + X[club_key]

			print("X Dictionary :")
			print(X)
			print("")

			# [ Calculating entropy ]
			for club_key, club_value in X.items():
				try:
					probability_val = float(club_value/total_packet_count)
				except ZeroDivisionError as e:
					probability_val = 1
				
				try:
					entropy = entropy + (-(probability_val * log(probability_val, 10)))					
				except ValueError as e:
					print("No packets for flow with key :- ", club_key)
					print("")

			print("Entropy before normalization :")
			print(entropy)
			print("")

			# [ Normalising entropy ]
			try:
				entropy = entropy / (log(N.__len__(), 10))
			except (ZeroDivisionError, ValueError) as e:
				print("Flow Table empty")
				print("")

			print("Entropy after normalization :")
			print(entropy)
			print("")

			print("----------------------------------------------------------------------------")
			print("")

		# [ Waiting for delta_t time ]
		sleep(delta_t)
		program_counter = program_counter + 1

if __name__ == '__main__':
	main()