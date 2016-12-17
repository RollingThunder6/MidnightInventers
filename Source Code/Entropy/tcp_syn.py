from scapy.all import *

src = "172.16.0.72"
dst = "172.16.0.86"

syn = IP(src=src, dst=dst) / TCP(dport=80, flags='S', seq=0, ack=0)
syn_ack = sr1(syn)

getStr = 'GET / HTTP/1.1\r\nHost: 172.16.0.86\r\n\r\n'

ack = IP(src=src, dst=dst) / TCP(dport=80, flags='A', seq=syn_ack.ack, ack=syn_ack.seq+1, options=[('MSS', 1460)]) / getStr
reply = send(ack)

fin = IP(src=src, dst=dst) / TCP(dport=80, flags='F', seq=5398, ack=syn_ack.seq+1, options=[('MSS', 1460)]) 
send(fin)