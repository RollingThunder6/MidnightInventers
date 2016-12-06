"""
Entropy based Discretization

Author - Midnight Inventers
"""

# [ Static initialisation of hosts connected directly to switch ]
# switch_ip = ["10.0.0.1", "10.0.0.2"]

fh = open("dummy.txt")

i = 0
flows = []
rp_local = []
N = []

for line in fh:
	if i != 0:
		line = line.strip().split(",")

		# [ Filtering src ip and dst ip from flow table ]
		# src_ip = line[13].split("=")
		# dst_ip = line[14].split("=")

		# [ Adding rp_local to flow entry depending on whether host is present or not ]
		# if src_ip[1] in switch_ip and dst_ip[1] in switch_ip:	
		# 	rp_local.append(0)
		# else:
		# 	rp_local.append(-1)

		# [ rp_local attribute added without checking ]
		rp_local.append(0)
		flows.append(line)
	i = i + 1

# packet count calculation for delta_t
i = 0
for flow in flows:
	received_packets = flow[3].split("=")
	received_packets = int(received_packets[1])

	num_packets = received_packets - rp_local[i]
	rp_local[i] = received_packets
	i = i + 1
	N.append(num_packets)