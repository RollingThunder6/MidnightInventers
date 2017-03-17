"""
Fuzzy C Means Algorithm - Pandas 

Author - Midnight Inventers
"""
import numpy as np
import pandas as pd
import timeit, os, time

# [ Load training data into memory ]
training_data = None

# [ initialize global variables ]
centroids = []
potential_max = None
cluster_count = None
membership = []
distance = []
membership_df = None

"""
Method :- find_membership_value(membership_df, attack_clusters)
Return :- minimum membership value

Find minimum membership value to be checked for an attack packet to belong 
to attack cluster
"""
def find_membership_value(membership_df, attack_clusters):
	min_values = []
	for column in membership_df:
		min_values.append(membership_df[column].min())

	return min(min_values)

"""
Method :- generate_centroid()
Return :- list of centroid values

Calculate centroid values using membership values of each point
"""
def generate_centroid():
	global centroids
	global training_data
	global membership_df

	# [ Time complexity :- O(c*n) ]
	m = 2
	new_centroids = []
	for centroid in centroids:
		value_df = membership_df[centroid].apply(lambda x:x**m)
		numerator_df = value_df.multiply(training_data["Interval"])
		numerator = numerator_df.sum()
		denominator = value_df.sum()
		new_centroids.append(round(float(numerator/denominator),6))
	return new_centroids

"""
Method :- calculate_membership_test()
Return :- None

Calculate membership values for testing data using euclidean distances between centroid and each point
"""
def calculate_membership_test(data):
	global centroids
	global cluster_count
	global membership
	global distance

	distance= [[abs(point[1] - cluster) for cluster in centroids] for point in data.itertuples()]
	membership = [[[] for i in centroids] for point in data.itertuples()]

	# [ Time complexity :- O(c*c*n) ]
	m = 2
	for cluster_j in range(cluster_count):
		for point in range(len(data)):
			dst = 0
			for cluster_k in range(cluster_count):
				dst = dst + ((distance[point][cluster_j] / distance[point][cluster_k])**(2/(m-1)))
			membership[point][cluster_j] = 1/dst
	return

"""
Method :- calculate_membership_train()
Return :- None

Calculate membership values for training data using euclidean distances between centroid and each point
"""
def calculate_membership_train(data):
	global centroids
	global cluster_count
	global membership
	global distance

	distance= [[abs(point[2] - cluster) for cluster in centroids] for point in data.itertuples()]
	membership = [[[] for i in centroids] for point in data.itertuples()]

	# [ Time complexity :- O(c*c*n) ]
	m = 2
	for cluster_j in range(cluster_count):
		for point in range(len(data)):
			dst = 0
			for cluster_k in range(cluster_count):
				dst = dst + ((distance[point][cluster_j] / distance[point][cluster_k])**(2/(m-1)))
			membership[point][cluster_j] = 1/dst
	return

"""
Method :- rearrange_potential()s
Return :- 0 if values not normalized else 1 

Calculate new potential values based on previous max potential value and find next centroid 
and check if more rearrangement needs to be done.
"""
def rearrange_potential():
	global training_data
	global centroids
	global potential_max

	# [ Time complexity :- O(n) ]
	entry_max = centroids[len(centroids)-1]
	training_data["new_potential"] = training_data.apply(lambda x:x[2] - potential_max*(np.exp((-4 * abs(x[1] - entry_max))/1.5)), axis=1)
	training_data["Potential_gap"] = pd.Series()
	training_data["Potential_gap"] = training_data["new_potential"] < 1
	if (training_data["Potential_gap"] == False).any():
		potential_max = training_data["new_potential"].max()
		max_index = training_data[training_data["new_potential"] == potential_max].index.tolist()[0]
		training_data["Potential"] = training_data["new_potential"]
		training_data = training_data.drop("new_potential",1)
		training_data = training_data.drop("Potential_gap",1)
		centroids.append(training_data.iloc[max_index]["Interval"])
		return 1
	else:
		return 0

"""
Method :- calculate_potential()
Return :- None

Calculate potential values for each point to decide which point is most viable to be a centroid
"""
def calculate_potential():
	global training_data
	global centroids
	global potential_max

	# [ Time Complexity :- O(n*n) ]
	training_data["Potential"] = training_data["Interval"].apply(lambda x: np.sum(np.exp(-4 * (x - training_data.Interval).abs())))
	potential_max = training_data["Potential"].max()
	max_index = training_data[training_data["Potential"] == potential_max].index.tolist()[0]    
	centroids.append(training_data.iloc[max_index]["Interval"])
	return 

"""
Method :- subtractive_main()
Return :- None

Starting point for subtractive clustering algorithm used for calculating optimum number of 
clusters along with respective centroid values which would be provided as input for
fuzzy c means algorithm to reduce iterations.
"""
def subtractive_main():
	global training_data
	calculate_potential()

	# [ Time complexity :- O(n) ]
	training_data["Potential_gap"] = pd.Series()
	training_data["Potential_gap"] = training_data["Potential"] < 1
	if training_data["Potential_gap"].all():
		training_data = training_data.drop("Potential_gap",1)
		return

	training_data = training_data.drop("Potential_gap",1)
	while True:
		return_val = rearrange_potential()
		if return_val == 0:
			return

"""
Method :- main()
Return :- None

Starting point of Fuzzy C Means algorithm
"""		
def main():
	global training_data
	global centroids
	global cluster_count
	global membership
	global membership_df

	normal_centroids = []
	attack_centroids = []
	normal_data = None
	attack_data = None

	training_files = ["normal_new.csv", "attack_new.csv"]

	for files in training_files:
		cluster_count = 0
		centroids = []
		training_data = pd.read_csv(files, usecols=[0,1], names=["Nature","Interval"], header=0)
		training_data["Interval"] = training_data["Interval"]

		# [ Call to subtractive clustering algorithm to find centroids and number of clusters ]
		subtractive_main()
		cluster_count = len(centroids)

		for point in training_data.itertuples():
			membership.append([[] for i in centroids])
		
		# [ Calculate memberhship values ]
		calculate_membership_train(training_data)
		membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
		centroids = generate_centroid()
		membership_df.columns = centroids
			
		# [ Training phase of fuzzy c means algorithm using loaded training data ]
		counter = 0
		while True:
			old_membership = membership_df.as_matrix()
			old_membership_df = membership_df
			calculate_membership_train(training_data)
			membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)	
			centroids = generate_centroid()
			membership_df.columns = centroids
			
			counter += 1
			if old_membership_df.equals(membership_df):
				print("Clustering complete in", counter, "steps")
				print(centroids)
				break

		if files == "normal_new.csv":
			normal_centroids.extend(centroids)
			# normal_centroids.pop(0)
		else:
			attack_centroids.extend(centroids)

	attack_clusters = [x for x in range(len(attack_centroids))]
	attack_centroids.extend(normal_centroids)
	centroids = attack_centroids
	cluster_count = len(centroids)

	min_membership = find_membership_value(membership_df, attack_clusters)

	# [ Detection phase ]
	program_counter = 0
	window = 5
	counter = 0
	ddos_attack_counter = 3

	while True:
		program_counter += 1
		if (program_counter % window) == 0:
			counter = 0

		testing_data = None
		if program_counter % 2 == 0:
			os.system("tshark -i any -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > detection_a.csv &")
			time.sleep(1.5)
			testing_data = pd.read_csv("detection_b.csv", usecols=[0], names=["Interval"], header=None)
			testing_data["Interval"] = testing_data["Interval"]
		else:
			os.system("tshark -i any -f 'icmp or udp or tcp' -T fields -E separator=, -e frame.time_delta_displayed -e ip.addr -e ip.proto > detection_b.csv &")
			time.sleep(1.5)
			testing_data = pd.read_csv("detection_a.csv", usecols=[0], names=["Interval"], header=None)
			testing_data["Interval"] = testing_data["Interval"]

		# testing_data = pd.read_csv("attack_test.csv", usecols=[0], names=["Interval"], header=0)
		total_packets = len(testing_data)
		if total_packets > 1:
			start = timeit.default_timer()
			calculate_membership_test(testing_data)
			testing_membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
			packet_arrangement = pd.DataFrame(columns=centroids)
			for centroid in centroids:
				packet_arrangement[centroid] = (testing_membership_df[centroid] >= 0.999)

			for values in attack_clusters:
				if (packet_arrangement[centroids[values]] == True).sum() >= (0.9 * total_packets):
					print("Inside DDoS")
					counter += 1
					if counter == ddos_attack_counter:
						print("DDoS detected")
						os.system("notify-send 'DDoS Detected "+str(counter)+"'")
						counter = 0
			end = timeit.default_timer()
			print("Testing time :", end-start)
		os.system("pkill tshark")

if __name__ == '__main__':
	main()