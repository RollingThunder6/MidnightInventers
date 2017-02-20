"""
Fuzzy C Means Algorithm - Pandas 

Author - Midnight Inventers
"""
import numpy as np
import pandas as pd
import timeit

# [ Load training data into memory ]
training_data = pd.read_csv("normal.csv", usecols=[0,1], names=["Nature","Interval"], header=0)

# [ initialize global variables ]
centroids = []
potential_max = None
cluster_count = None
membership = []
distance = []
membership_df = None

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
	new_centroids = []
	for centroid in centroids:
		value_df = membership_df[centroid].apply(lambda x:x**2)
		numerator_df = value_df.multiply(training_data["Interval"])
		numerator = numerator_df.sum()
		denominator = value_df.sum()
		new_centroids.append(round(float(numerator/denominator),6))
	return new_centroids

"""
Method :- calculate_membership()
Return :- None

Calculate membership values using euclidean distances between centroid and each point
"""
def calculate_membership(data):
	global centroids
	global cluster_count
	global membership
	global distance

	distance= [[abs(point[2] - cluster) for cluster in centroids] for point in data.itertuples()]
	membership = [[[] for i in centroids] for point in data.itertuples()]

	# [ Time complexity :- O(c*c*n) ]
	for cluster_j in range(cluster_count):
		for point in range(len(data)):
			dst = 0
			for cluster_k in range(cluster_count):
				dst = dst + ((distance[point][cluster_j] / distance[point][cluster_k])**2)
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

	# [ Call to subtractive clustering algorithm to find centroids and number of clusters ]
	subtractive_main()
	cluster_count = len(centroids)

	for point in training_data.itertuples():
		membership.append([[] for i in centroids])
	
	# [ Calculate memberhship values ]
	calculate_membership(training_data)
	membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
	centroids = generate_centroid()
	membership_df.columns = centroids
		
	# [ Training phase of fuzzy c means algorithm using loaded training data ]
	counter = 0
	while True:
		old_membership = membership_df.as_matrix()
		old_membership_df = membership_df
		calculate_membership(training_data)
		membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)	
		centroids = generate_centroid()
		membership_df.columns = centroids
		epsilon_df = membership_df.subtract(old_membership)
		
		counter += 1
		if old_membership_df.equals(membership_df):
			print("Clustering complete in", counter, "steps")
			print(centroids)
			break

	# [ Identification of attack clusters ]
	attack_packets = (training_data["Nature"] == 1).sum()
	attack_membership = pd.DataFrame(columns=centroids)
	classes = []
	attack_clusters = []
	for centroid in centroids:
		attack_membership[centroid] = (membership_df[centroid] > 0.75) & (training_data.Nature == 1)
		classes.append((attack_membership[centroid] == True).sum())

	for value in range(len(classes)):
		if classes[value] > 0.75 * attack_packets:
			attack_clusters.append(value)
	
	# [ Detection phase ]
	while True:
		testing_data = pd.read_csv("5000_normal.csv", usecols=[0], names=["Interval"], header=0)
		# testing_data = pd.read_csv("5000_normal.csv", usecols=[0,1], names=["Nature","Interval"], header=0)
		total_packets = len(testing_data)
		
		calculate_membership(testing_data)
		testing_membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
		packet_arrangement = pd.DataFrame(columns=centroids)
		for centroid in centroids:
			packet_arrangement[centroid] = (testing_membership_df[centroid] > 0.75)

		for values in attack_clusters:
			if (packet_arrangement[centroids[values]] == True).sum() > 0.6*total_packets:
				print("DDoS detected")
		return

if __name__ == '__main__':
	main()	