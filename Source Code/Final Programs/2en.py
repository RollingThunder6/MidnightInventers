# ENTROPY BASED DISCRETIZATION
# AUTHOR: MIDNIGHT INVENTOR

from math import log, sqrt
from time import sleep, ctime
from os import system

# dictionary key: dest. IP Addr, Value: ([new packet count], [prev. packet count])
hash_flows = {}
# list to store normal entropy values
entropy = []
prob = []
# alpha values for weighted mean
wt_alpha = [0.04, 0.11, 0.19, 0.28, 0.38]

total_pac = 0
total_entropy = 0
# entropy of network during normal traffic flow
normal_entropy = 0.8
# max. allowable diff bet entropies
threshold = 0.285   # initial normal 0.09
prog_counter = 0
ddos_counter = 0
window = 4
min_ddos_counter = 3
# sleep time
delta_t = 1
diff = 0
const_k = 5
std_dev = 1
mul_factor = 1.0000000000001

d=0

# flow Aggregation based on dest IP Addr and storing in dictionary.
def collect_flow():
	global hash_flows, total_pac 

	total_pac = 0

	# print "Collecting Flows"

	for key, value in hash_flows.items():	
		hash_flows[key][0] = 0			

	system("sudo ovs-ofctl dump-flows br0 > dummy.txt")

	try:
		fh=open("dummy.txt")
	except:
		print "File not found"

	i = 0
	for flow_entry in fh: 
		flow = []

		if i != 0:
			flow_entry=flow_entry.strip().split(",")
			# print flow_entry

			try:
				dest_ip = flow_entry[14].split("=")
			except Exception as e:
				# print "dest ip does not exist !!!"
				continue


			no_pac = flow_entry[3].split("=")

			dest_val = dest_ip[1].split(".")

			dest = "".join(dest_val)
			pac = no_pac[1]

			key = dest 
			# print key

			if key in hash_flows:
				# print "makad"
				new = int(hash_flows[key][0])
				new = new + int(pac)
				hash_flows[key][0] = str(new)
				# print "new: ", new
			else:
				# print "gila chammach"
				flow.append(pac)
				flow.append("0")
				# print flow

				hash_flows[key] = flow

		i = i + 1


	# print "Calculating total packets: "
	for key, value in hash_flows.items():
		new = int(hash_flows[key][0])
		prev = int(hash_flows[key][1])

		hash_flows[key][1] = str(new)

		if new > prev:
			new = new - prev
			hash_flows[key][0] = str(new)

			# print "key: pac  ",key, "\t:\t", new 

			total_pac = total_pac + new
			# print "total pac: ", total_pac

		else:
			# print "key: pac  ",key, "\t:\t", new 

			total_pac = total_pac + new
			# print "total pac: ", total_pac
			

	#for key, value in hash_flows.items():
		# print key, value

	print "Total Packets: ", total_pac



# calculating Entropy of network and checking whether it is normal or not. If it is normal then storing it in entropy list.
def calc_entropy():
	global prob, entropy, hash_flows, total_pac, total_entropy, normal_entropy, threshold, diff
	total_entropy = 0
	prob = []

	fh = open("nor_ent.text", "a+")

	i = 0
	for key, value in hash_flows.items():

		try:
			prob_val = float(hash_flows[key][0])/total_pac
		except ZeroDivisionError as e:
			prob_val = 1

		prob.append(prob_val)
		
		try:
			entropy_val = prob_val * log(prob_val, 10)
			# print key
		except ValueError as e:
			# print "exception caught !!!!: ", key
			continue

		# print "ent: ", entropy_val
		total_entropy = total_entropy + entropy_val

		i = i + 1

	total_entropy = -(total_entropy)

	fh.write("\n\nTotal No. of packets: " + str(total_pac))
	fh.write("\nEntropy: " + str(total_entropy))

	try:
		total_entropy = total_entropy / log(i, 10)
		fh.write("\nNormalized Entropy: " + str(total_entropy))
	except (ZeroDivisionError, ValueError) as e:
		print

	diff = abs(normal_entropy - total_entropy)
	# print "diff: ", diff
	fh.write("\nDifference is: " + str(diff))

	# print "threshold is: ", threshold
	# print "normal entropy: ", normal_entropy

	if diff < threshold:
		# print "normal traffic!!!"
		entropy.append(total_entropy)
	
	# print prob
	# print entropy
		

# Detecting whether incoming traffic is normal or not.
def ddos_detection():
	global diff, threshold, ddos_counter, prog_counter, window, min_ddos_counter, d, total_pac

	if diff > threshold:
		# print "Inside ddos checking..."
		ddos_counter = ddos_counter + 1
		# print 


		if (prog_counter + 1) % window == 0:
			ddos_counter = 0

		if ddos_counter == min_ddos_counter:
			d += 1
			print "-------------------DDoS Detected------------------\n\n\n\n\n"
			with open("/var/log/ddos_log", "a+") as fh:
				fh.write("DDoS detected")

			# print
	else:
		if (prog_counter + 1) % window == 0:
			ddos_counter = 0

		# print "ddos count: ", ddos_counter
		# print


# Adaption of normal entropy val and threshold on the basis of previously measured normal entropy values
def adapt_entropy():
	global threshold, diff, wt_alpha, const_k, normal_entropy, entropy, std_dev, mul_factor
	sum = 0

	if diff < threshold:
		if len(entropy) > const_k:
			entropy = []
			# print "List Entropy cleared !!!"

		for i in range(0, len(entropy)):
			normal_entropy = normal_entropy + (wt_alpha[i] * entropy[i])

		# print "Adapted: ", normal_entropy

		for i in range(0, len(entropy)):
			sum = sum + ((entropy[i] - normal_entropy) ** 2)

		try:
			std_dev = sqrt(sum / len(entropy))
		except Exception as e:
			print "length of entropy list is 0 !!!"

		threshold = mul_factor * std_dev

		# print "new threshold: ", threshold



# Start


while 1:
	collect_flow()
	calc_entropy()
	ddos_detection()
	#adapt_entropy()

	prog_counter = prog_counter + 1
	sleep(delta_t)


# collect_flow()
# calc_entropy()
# ddos_detection()
# adapt_entropy()

# prog_counter = prog_counter + 1

# # print "\nSleeping\n\n"
