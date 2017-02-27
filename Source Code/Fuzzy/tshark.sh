while [[ 1 ]]; do
	tshark -i any -a duration:3 -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > capture.csv
	cp capture.csv detection.csv
done