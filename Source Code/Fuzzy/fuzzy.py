"""
Fuzzy C Means Algorithm

Author - Midnight Inventers
"""

import csv
import math

def generate_centroid(membership, entries, cluster_count):
	m = 2
	centroid_list = []

	for cluster in range(0, cluster_count):
		numerator = 0
		denominator = 0
		for count in range(0, entries.__len__()):
			value = (membership[cluster][count]**m)
			numerator = numerator + (value* float(entries[count][1]))
			denominator = denominator + value
		centroid_list.append(round(float(numerator/denominator), 3))
	return centroid_list

def main():
	entries = []
	with open("dummy.csv") as csvfile:
		reader = csv.reader(csvfile)
		for line in reader:
			entries.append([line[0], line[1]])
	# print(entries)

	cluster_count = 3
	membership = []
	for count in range(cluster_count):
		membership.append([])
	# print(membership)

	initial_membership_val = round(float(1/cluster_count),2)
	# print(initial_membership_val)

	for mem_val in range(0,membership.__len__()):
		for entry_count in range(0, entries.__len__()):
			membership[mem_val].append(initial_membership_val)

	initial_centroids = []
	initial_centroids = generate_centroid(membership, entries, cluster_count)
	print(initial_centroids)

if __name__ == '__main__':
	main()