"""
Fuzzy C Means Algorithm

Author - Midnight Inventers
"""

import csv
import math

centroids = []
entries = []
potential = []
prev_potential = None
prev_entry = None

with open("dummy.csv") as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		entries.append(line[1])

def rearrange_potential():
	global entries
	global centroids
	global prev_potential
	global potential
	global prev_entry

	for value_counter in range(0, potential.__len__()):
		value = float(entries[value_counter]) - prev_entry
		if value < 0:
			value = -value
		potential[value_counter] = potential[value_counter] - prev_potential*(math.exp(-(4*(value)/1.5)))

	flag = True
	for values in potential:
		if values > 1:
			flag = False
			break

	if flag == False:
		potential_index = potential.index(max(potential))
		prev_potential = max(potential)
		prev_entry = float(entries.pop(potential_index))
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

	for count_i in range(0, entries.__len__()):
		potential_sum = 0
		for count_j in range(0, entries.__len__()):
			distance = float(entries[count_i]) - float(entries[count_j])
			if distance < 0:
				distance = -distance

			exponent = -(4 * distance)
			val = math.exp(exponent)

			potential_sum = potential_sum + val

		potential.append(potential_sum)

	potential_index = potential.index(max(potential))
	prev_potential = max(potential)

	prev_entry = float(entries.pop(potential_index))
	potential.pop(potential_index)

	centroids.append(prev_entry)
	return

def main():
	global entries
	global centroids
	global prev_potential
	global potential
	global prev_entry

	flag = True
	calculate_potential()	
	for values in potential:
		if values > 1:
			flag = False

	if flag == True:
		print(centroids)
		print("Cluster Count :-", centroids.__len__())
		exit()
	
	while True:	
		return_val = rearrange_potential()
		if return_val == 0:
			print(centroids)
			print("Cluster Count :-", centroids.__len__())
			exit()

if __name__ == '__main__':
	main()