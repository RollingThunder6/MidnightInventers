"""
Entropy based Discretization

Author - Midnight Inventers
"""

# [ Static initialisation of hosts connected directly to switch ]
# switch_ip = ["10.0.0.1", "10.0.0.2"]

fh = open("dummy.txt")
i = 0
flows = []
for line in fh:
	if i != 0:
		line = line.strip().split(",")

		# [ Filtering src ip and dst ip from flow table ]
		# src_ip = line[13].split("=")
		# dst_ip = line[14].split("=")

		# [ Adding rp_local to flow entry depending on whether host is present or not ]
		# if src_ip[1] in switch_ip and dst_ip[1] in switch_ip:	
		# 	line.append(0)
		# else:
		# 	line.append(-1)

		# [ rp_local attribute added to flow entry without checking ]
		line.append(0)
		flows.append(line)
	i = i + 1

for flow in flows:
	print(flow)