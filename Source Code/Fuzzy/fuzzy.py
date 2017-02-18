"""
Fuzzy C Means Algorithm

Author - Midnight Inventers
"""

import csv
import math
import time, timeit

from operator import add
from functools import reduce

# Common entity
entries = []

# Subtractive Clustering values
centroids = []
potential = []
prev_potential = None
prev_entry = None

# Fuzzy C Means Values
cluster_count = None
membership = []
new_centroids = []

with open("10000.csv") as csvfile:
	reader = csv.reader(csvfile)
	entries = [[line[0], line[1]] for line in reader]

def rearrange_potential():
	global entries
	global centroids
	global prev_potential
	global potential
	global prev_entry

	flag = True
	temp_potential = [potential[value_counter] - prev_potential*(math.exp(-(4*(abs(float(entries[value_counter][1]) - prev_entry))/1.5))) for value_counter in range(0, potential.__len__())]
	potential = temp_potential

	flag = all(i <= 1 for i in potential)

	if flag == False:
		potential_index = potential.index(max(potential))
		prev_potential = max(potential)
		value = entries.pop(potential_index)
		prev_entry = float(value[1])
		potential.pop(potential_index)
		centroids.append(prev_entry)
		return 1
	else:
		return 0

def calculate_potential():
	global entries
	global centroids
	global prev_potential
	global potential
	global prev_entry

	for entry_i in entries:
		potential_val = [math.exp(-(4 * (abs(float(entry_i[1]) - float(entry_j[1]))))) for entry_j in  entries]	
		potential_sum = reduce(add, potential_val)
		potential.append(potential_sum)
		
	potential_index = potential.index(max(potential))
	prev_potential = max(potential)

	value = entries.pop(potential_index)
	prev_entry = float(value[1])
	potential.pop(potential_index)

	centroids.append(prev_entry)
	return

def subtractive_main():
	global entries
	global centroids
	global prev_potential
	global potential
	global prev_entry

	flag = True
	calculate_potential()	
	flag = all(i <= 1 for i in potential)
	if flag == True:
		return
	
	while True:	
		return_val = rearrange_potential()
		if return_val == 0:
			return 

def generate_centroid():
	global membership
	global cluster_count
	global entries
	global centroids

	centroids = []
	for cluster in range(0, cluster_count):
		numerator = 0
		denominator = 0
		for count in range(0, entries.__len__()):
			value = (membership[cluster][count]**2)
			numerator = numerator + (value * float(entries[count][1]))
			denominator = denominator + value
		centroids.append(round(float(numerator/denominator),6))

def calculate_membership():
	global membership
	global entries
	global centroids

	for j in range(0, cluster_count):
		membership[j] = []
		for i in range(0, entries.__len__()):
			num_distance = 0
			den_distance = 0
			
			den_distance = abs(float(entries[i][1])	- float(centroids[j]))
			distance_sum = 0

			for k in range(0, cluster_count):
				num_distance = abs(float(entries[i][1])	- float(centroids[k]))
				try:
					value = float(num_distance/den_distance)
				except ZeroDivisionError as e:
					value = 100000000

				value = value ** 2
				distance_sum = distance_sum + value

			membership[j].append(float(1/distance_sum))
	return

def list_duplicates(seq):
	global centroids
	seen = set()
	seen_add = seen.add
	return [idx for idx,item in enumerate(seq) if item in seen or seen_add(item)]

def main():
	global entries
	global centroids
	global cluster_count
	global new_centroids
	global membership

	subtractive_main()
	cluster_count = centroids.__len__()

	membership = []
	for count in range(cluster_count):
		membership.append([])

	calculate_membership()
	generate_centroid()

	# initial_membership = membership.copy()

	# [ Calculate difference of membership values ]
	# while True:
	# 	calculate_membership()
	# 	generate_centroid()
	# 	flag = True

	# 	check_list = []
	# 	values = []
	# 	for cluster_counter in range(0, cluster_count):
	# 		value = [x[0] - x[1] for x in zip(membership[cluster_counter], initial_membership[cluster_counter])]
	# 		check_value = all(i < 0.7 for i in value)
	# 		check_list.append(check_value)
	# 		values.append(value)
			
	# 	print(values)

	# 	if False in check_list:
	# 		flag = False

	# 	if flag == True:
	# 		break
	# 	else:
	# 		initial_membership = None
	# 		initial_membership = membership.copy()
	# 		print("repeat")
	# 	time.sleep(1)

	iterations = 0
	while iterations < 10:
		calculate_membership()
		generate_centroid()
		iterations = iterations + 1
	print(centroids)
	club_list = list_duplicates(centroids)
	print(club_list)

if __name__ == '__main__':
	start = timeit.default_timer()
	main()
	end = timeit.default_timer()
	print(end-start)