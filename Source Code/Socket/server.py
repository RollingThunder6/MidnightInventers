import socket               
from time import sleep

s = socket.socket()         
host = socket.gethostname() 
port = 1341
s.bind((host, port))        

s.listen(5)
c = None
# counter = 0                
# while True:
# 	try:
# 		if c == None:
# 			c, addr = s.accept()
# 			print('Got connection from', addr)

# 		if counter % 5 == 0:
# 			msg = '10.0.0.3'
# 			c.send(msg.encode())
# 			sleep(10)
# 		counter = counter + 1
# 	except KeyboardInterrupt as e:
# 		s.close()
# 		c.close()

while True:
	try:
		if c == None:
			c, addr = s.accept()
			print('Got connection from', addr)
		msg = '10.0.0.3'
		c.send(msg.encode())
		
	except KeyboardInterrupt as e:
		s.close()
		c.close()	