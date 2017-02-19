import numpy as np
import pandas as pd
import timeit

training_data = pd.read_csv("1300000.csv", usecols=[0,1], names=["Nature","Interval"], header=0)
centroids = []
potential_max = None
cluster_count = None
membership = []
distance = []
membership_df = None

training_membership_df = None
training_membership = None

def generate_centroid():
	global membership
	global cluster_count
	global centroids
	global training_data
	global membership_df

	new_centroids = []
	for centroid in centroids:
		value_df = membership_df[centroid].apply(lambda x:x**2)
		numerator_df = value_df.multiply(training_data["Interval"])
		numerator = numerator_df.sum()
		denominator = value_df.sum()
		new_centroids.append(round(float(numerator/denominator),6))
	return new_centroids

def calculate_membership(data):
	global centroids
	global cluster_count
	global membership
	global distance 

	distance= [[abs(point[2] - cluster) for cluster in centroids] for point in data.itertuples()]
	membership = [[[] for i in centroids] for point in data.itertuples()]

	for cluster_j in range(cluster_count):
		for point in range(len(data)):
			dst = 0
			for cluster_k in range(cluster_count):
				dst = dst + ((distance[point][cluster_j] / distance[point][cluster_k])**2)
			membership[point][cluster_j] = 1/dst
	return

def rearrange_potential():
	global training_data
	global centroids
	global potential_max

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

def calculate_potential():
	global training_data
	global centroids
	global potential_max

	training_data["Potential"] = training_data["Interval"].apply(lambda x: np.sum(np.exp(-4 * (x - training_data.Interval).abs())))
	potential_max = training_data["Potential"].max()
	max_index = training_data[training_data["Potential"] == potential_max].index.tolist()[0]    
	centroids.append(training_data.iloc[max_index]["Interval"])
	return 

def subtractive_main():
	global training_data
	calculate_potential()

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
		
def main():
	global training_data
	global centroids
	global cluster_count
	global membership
	global membership_df
	global training_membership_df
	global training_membership

	subtractive_main()
	cluster_count = len(centroids)

	for point in training_data.itertuples():
		membership.append([[] for i in centroids])
	
	calculate_membership(training_data)
	membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
	centroids = generate_centroid()
	membership_df.columns = centroids
		
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
	
	while True:
		start = timeit.default_timer()
		testing_data = pd.read_csv("dummy.csv", usecols=[0,1], names=["Nature","Interval"], header=0)
		total_packets = len(testing_data)
		# testing_data = pd.read_csv("200.csv", usecols=[0], names=["Interval"], header=0)
		
		calculate_membership(testing_data)
		testing_membership_df = pd.DataFrame(membership, columns=centroids).fillna(1)
		packet_arrangement = pd.DataFrame(columns=centroids)
		for centroid in centroids:
			packet_arrangement[centroid] = (testing_membership_df[centroid] > 0.75)

		for values in attack_clusters:
			if (packet_arrangement[centroids[values]] == True).sum() > 0.6*total_packets:
				print("DDoS detected")
		end = timeit.default_timer()
		print(end-start)
		return

if __name__ == '__main__':
	main()