from multiprocessing import Pool, Process
from scapy.all import *

ip_addr = []

def send_packets():
	src_ip = "172.16.0.72"
	dst_ip = "172.16.0.73"
	syn = IP(src=src_ip, dst=dst_ip) / TCP(dport=80, flags='S')
	getStr = 'GET / HTTP/1.1\r\nHost: 172.16.0.73\r\n\r\n'

	syn_ack = sr1(syn)
	req_packet = IP() / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
	
	req_packet.src = src_ip
	req_packet.dst = dst_ip
	sr1(req_packet)

def main():
	global ip_addr
	pool = Pool(processes=30)
	
	ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="172.16.0.0/23"),timeout=2)
	ans.summary(lambda(sender,receiver): ip_addr.append(sender.pdst))

	while True:
		pool.apply_async(send_packets)
	return

if __name__ == '__main__':
	main()