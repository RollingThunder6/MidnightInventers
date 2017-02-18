import numpy as np
import pandas as pd
import timeit

packet_data = pd.read_csv("200.csv", usecols=[0,1], names=["Nature","Interval"], header=0)
centroids = []
potential_max = None
cluster_count = None
membership = None

def membership_function(col):
	
	return 

def calculate_membership():
	global packet_data
	global centroids
	global cluster_count
	global membership

	membership = membership.apply(, axis=1)
	return

def rearrange_potential():
	global packet_data
	global centroids
	global potential_max

	entry_max = centroids[len(centroids)-1]
	packet_data["new_potential"] = packet_data.apply(lambda x:x[2] - potential_max*(np.exp((-4 * abs(x[1] - entry_max))/1.5)), axis=1)
	packet_data["Potential_gap"] = pd.Series()
	packet_data["Potential_gap"] = packet_data["new_potential"] < 1
	if (packet_data["Potential_gap"] == False).any():
		potential_max = packet_data["new_potential"].max()
		max_index = packet_data[packet_data["new_potential"] == potential_max].index.tolist()[0]
		packet_data["Potential"] = packet_data["new_potential"]
		packet_data = packet_data.drop("new_potential",1)
		packet_data = packet_data.drop("Potential_gap",1)
		centroids.append(packet_data.iloc[max_index]["Interval"])
		return 1
	else:
		return 0

def calculate_potential():
	global packet_data
	global centroids
	global potential_max

	packet_data["Potential"] = packet_data["Interval"].apply(lambda x: np.sum(np.exp(-4 * (x - packet_data.Interval).abs())))
	potential_max = packet_data["Potential"].max()
	max_index = packet_data[packet_data["Potential"] == potential_max].index.tolist()[0]    
	centroids.append(packet_data.iloc[max_index]["Interval"])
	return 

def subtractive_main():
	global packet_data
	calculate_potential()

	packet_data["Potential_gap"] = pd.Series()
	packet_data["Potential_gap"] = packet_data["Potential"] < 1
	if packet_data["Potential_gap"].all():
		packet_data = packet_data.drop("Potential_gap",1)
		return

	packet_data = packet_data.drop("Potential_gap",1)
	while True:
		return_val = rearrange_potential()
		if return_val == 0:
			return
		
def main():
	global packet_data
	global centroids
	global cluster_count
	global membership

	subtractive_main()
	cluster_count = len(centroids)
	membership = pd.DataFrame(columns=centroids)
	calculate_membership()
	return

if __name__ == '__main__':
	main()