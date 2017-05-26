import numpy as np
import csv
from time import sleep, ctime
import os
import codecs

class Support_Vector_Machine:
	def fit(self, data):
		self.data = data
		opt_dict = {}

		transforms = [[1,1],[-1,1],[-1,-1],[1,-1]]

		all_data = []
		[[[all_data.append(feature) for feature in featureset] for featureset in self.data[yi]] for yi in self.data]

		self.max_feature_value = max(all_data)
		self.min_feature_value = min(all_data)
		all_data = None

		

		step_sizes = [self.max_feature_value * 0.1,]

		
		
		b_range_multiple = 2
		b_multiple = 5
		latest_optimum = self.max_feature_value*10
		
		for step in step_sizes:
			w = np.array([latest_optimum,latest_optimum])
			optimized = False
			while not optimized:
				for b in np.arange(-1*(self.max_feature_value*b_range_multiple),
								   self.max_feature_value*b_range_multiple,
								   step*b_multiple):
					for transformation in transforms:
						w_t = w*transformation
						found_option = True

						for i in self.data:
							for xi in self.data[i]:
								yi=i
								if not yi*(np.dot(w_t,xi)+b) >= 1:
									found_option = False                                   
						if found_option:
							opt_dict[np.linalg.norm(w_t)] = [w_t,b]

				if w[0] < 0:
					optimized = True
				else:
					w = w - step

			norms = sorted([n for n in opt_dict])
			#||w|| : [w,b]
			opt_choice = opt_dict[norms[0]]
			self.w = opt_choice[0]
			self.b = opt_choice[1]
			latest_optimum = opt_choice[0][0]+step*2
	   

	def predict(self,features):
		classification = np.sign(np.dot(np.array(features),self.w)+self.b)
		# print classification
		return classification

def fileopen(filename):
	time = []
	protocol = []

	with open(filename,'r') as csvfile:
		# reader = csv.reader(codecs.open(csvfile,'rU','utf-16'))
		reader = csv.reader(csvfile)

		for row in reader:
			try:
				protocol.append(int(row[3]))
				time.append(float(row[0]))
			except:
				continue
	return time,protocol		

def convertTime(time):
	time_temp = []
	for i in range(0,len(time)):
		time_temp.append(int(time[i]*10000))
	return time_temp

def predictstuff(filename):
	global counter1
	global temp_counter
	time, protocol = [], []
	prediction = []
	temp_counter = temp_counter + 1
	count_total, count_negative, ratio = 0, 0, 0
	time, protocol = fileopen(filename)	
	time = convertTime(time)
	predict_data = zip(time,protocol)
	for p in predict_data:
		prediction.append(svm.predict(p))
	count_total = len(prediction)
	# print prediction
	for i in range(0,len(prediction)):
			if(prediction[i] == -1):
				count_negative = count_negative + 1
	try:
		ratio = float(count_negative)/count_total
	except:
		pass
	print "The ratio is: ",ratio

	if(ratio < 0.0008 and ratio > 0.0 and ratio!=0.25):
		counter1 = counter1 + 1 
	else:
		counter1 = 0
	if(temp_counter > 3):
		counter1 = 0
		temp_counter = 0
	if(counter1 >= 3):
		with open("/var/log/ddos_log", "a+") as fh:
			fh.write("DDoS Detected")
		print "DDoS detected"
	# print "The counter is: ",counter1


if __name__ == "__main__":
	counter = 0
	counter1 = 0
	temp_counter = 0
	count_total, count_negative = 0, 0
	prediction = []
	svm = Support_Vector_Machine()
	data_dict = {1:np.array([[1,7],[2,8],[3,8],]),-1:np.array([[5,1],[4,3],[7,3],])}
	svm.fit(data=data_dict)
	
# 	counter = 1

# while True:
# 	if counter % 2 == 1:
# 		os.system("tshark -i any -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > detectionA.csv &")
# 		sleep(2)
# 		predictstuff('detectionB.csv')

# 	else:
# 		os.system("tshark -i any -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > detectionB.csv &")
# 		sleep(2)
# 		predictstuff('detectionA.csv')
# 	os.system("pkill tshark")
# 	counter = counter + 1


	while True:
		os.system("tshark -i any -a duration:1 -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > detectionB.csv")
		predictstuff('detectionB.csv')

