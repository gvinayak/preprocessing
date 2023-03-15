import numpy as np
import pickle
import pdb
import datetime
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg

location_count = int(sys.argv[1])
checkins_count = int(sys.argv[2])
connection_count = int(sys.argv[3])
folder = sys.argv[4]
tr_ratio = 0.8

# ----------------------------------------------------------------------------------
# Format of Features: User, Location, No. of Visits, Lat, Long, Category, Time 
# ----------------------------------------------------------------------------------

def clean_up(unfiltered_checkins, unfiltered_connections):
	order = {}
	loc_dict = {}
	count = 0
	loc_count = 0
	for k in range(len(unfiltered_connections)):
		if(unfiltered_connections[k,0] not in order):
			order[unfiltered_connections[k,0]] = count
			count += 1

		if(unfiltered_connections[k,1] not in order):
			order[unfiltered_connections[k,1]] = count
			count += 1
		
		unfiltered_connections[k,0] = order[unfiltered_connections[k,0]]
		unfiltered_connections[k,1] = order[unfiltered_connections[k,1]]

	for k in range(len(unfiltered_checkins)):
		if(unfiltered_checkins[k,0] in order):
			unfiltered_checkins[k,0] = int(order[unfiltered_checkins[k,0]])

		if(unfiltered_checkins[k,1] not in loc_dict):
			loc_dict[unfiltered_checkins[k,1]] = loc_count
			loc_count += 1

		unfiltered_checkins[k,1] = loc_dict[unfiltered_checkins[k,1]]

	return [unfiltered_checkins, unfiltered_connections]

# Function to get the best graph
def get_soc_best(unfiltered_connections):
	inc = 1
	while(inc > 0):
		inc = 0
		unique, count = np.unique(unfiltered_connections[:,0], return_counts=True)
		unique_2, count_2 = np.unique(unfiltered_connections[:,1], return_counts=True)
		us1_dict = dict(zip(unique, count))
		us2_dict = dict(zip(unique_2, count_2))

		for k2,v2 in us2_dict.items():
			if k2 in us1_dict:
				us1_dict[k2] += v2
			else:
				us1_dict[k2] = v2

		for k,v in us1_dict.copy().items():
				if v < connection_count:
					del us1_dict[k]
					inc = 1

		del_vec = []
		for k in range(len(unfiltered_connections)):
			if(unfiltered_connections[k,0] not in us1_dict) or (unfiltered_connections[k,1] not in us1_dict):
				del_vec.append(k)
		if(len(del_vec) > 0):
			unfiltered_connections = np.delete(unfiltered_connections.copy(), np.asarray(del_vec), 0)

	return(unfiltered_connections)

# ========== Main code starts here ==========
# subprocess.run("rm -rf Cleaned/*", shell=True, check=True)
loc_set = set(["Aichi", "Baden-Wuerttemberg", "Bavaria", "Berlin", "California", "Hyogo", "Kyoto", 
	"Massachusetts", "North_Rhine-Westphalia", "Ohio", "Texas", "Tokyo", "Washington"])

path = folder+"/"
for filename in glob.glob(os.path.join(path, '*.txt')):
	search_file = filename.split("/")[1].replace(".txt", "")
	if(search_file not in loc_set):
		continue

	print("\n\n =====================================>")
	print(search_file)
	unfiltered_checkins = np.genfromtxt(filename, dtype=str, delimiter=',')
	unfiltered_checkins = np.asarray(unfiltered_checkins)

	if len(unfiltered_checkins) < 10:
		continue

	# Filter for minimum locations
	unique, counts = np.unique(unfiltered_checkins[:,1], return_counts=True)
	check_loc_temp = dict(zip(unique, counts))
	for key, value in check_loc_temp.copy().items():
		if(value < location_count):
			del check_loc_temp[key]

	check_del = [] #Checkins to be deleted
	for k in range(len(unfiltered_checkins)):
		if(unfiltered_checkins[k,1] not in check_loc_temp):
			check_del.append(int(k))

	check_del = np.asarray(check_del)
	if(len(check_del) > 0):
		unfiltered_checkins = np.delete(unfiltered_checkins, check_del, 0)

	# Get frequent user for checkins dictionary
	unique, counts = np.unique(unfiltered_checkins[:,0], return_counts=True)
	check_freq = dict(zip(unique, counts))
	for key, value in check_freq.copy().items():
		if(value < checkins_count):
			del check_freq[key]

	print("Level 1 Checkins Dictionary Done")

	# Get users for social dictionary
	con_dict = {}
	soc = open("/home/vinayak/Desktop/My_Work/app/Data/Foursquare/WWW_friendship_new.txt")
	unfiltered_connections = []
	for line in soc:
		temp = []
		line = line.rstrip()
		arr = line.split('\t')
		u1 = arr[0]
		u2 = arr[1]
		if(u1 in check_freq and u2 in check_freq):
			if (u1 not in con_dict):
				con_dict[u1] = set()
			if (u2 not in con_dict):
				con_dict[u2] = set()
			if(u2 not in con_dict[u1]):
				temp.append(u1)
				temp.append(u2)
				# temp.append(arr[3])
				unfiltered_connections.append(temp)

			con_dict[u1].add(u2)
			con_dict[u2].add(u1)

	soc.close()

	unfiltered_connections = np.asarray(unfiltered_connections)

	if len(unfiltered_connections) < 5:
		continue
	
	unfiltered_connections = get_soc_best(unfiltered_connections) #Call the social optimization function

	print("Social Connections Made")

	# Get the social dictionary
	unique, count = np.unique(np.append(unfiltered_connections[:,0], unfiltered_connections[:,1]), return_counts=True)
	soc_freq = dict(zip(unique, count))

	# Update the checkin dictionary with the social
	for key, value in check_freq.copy().items():
		if(key not in soc_freq):
			del check_freq[key]

	# Update the checkins file
	check_del = []
	for k in range(len(unfiltered_checkins)):
		if(unfiltered_checkins[k,0] not in check_freq):
			check_del.append(int(k))

	check_del = np.asarray(check_del)
	unfiltered_checkins = np.delete(unfiltered_checkins, check_del, 0)
	print("Final Checkins Made")

	# Final CleanUp
	[unfiltered_checkins, unfiltered_connections] = clean_up(unfiltered_checkins, unfiltered_connections)

	# Make all dumps
	unique, count = np.unique(unfiltered_connections[:,0], return_counts=True)
	unique_2, count_2 = np.unique(unfiltered_checkins[:,0], return_counts=True)
	unique_3, count_3 = np.unique(unfiltered_checkins[:,1], return_counts=True)

	print("Users (CH CO)",len(check_freq)," ", len(soc_freq))
	print("Locations ",len(unique_3))
	print("Checkins ",len(unfiltered_checkins))
	print("Connections ",len(unfiltered_connections))
	
	if len(unfiltered_checkins) < 10 or len(unfiltered_connections) < 3:
		continue

	# Divide into Train and Test Data
	checkin = unfiltered_checkins
	soc = unfiltered_connections

	checkin = checkin[np.asarray(checkin[:,5]).argsort(kind='mergesort')]

	# Bringing in the Checkin Count o make it similar to Gowalla
	main_vec = {}   # Reusing main vec to save space
	checkin = np.insert(checkin, 2, values=0, axis=1)
	for k in range(len(checkin)):
		user = checkin[k, 0]
		location = checkin[k, 1]
		if user not in main_vec:
			main_vec[user] = {}

		if location not in main_vec[user]:
			main_vec[user][location] = 0

		main_vec[user][location] += 1

		checkin[k, 2] = main_vec[user][location]

	split_index = int(len(checkin)*tr_ratio)
	split_time = checkin[split_index, 6]
	check_train = checkin[:split_index]
	check_test = checkin[split_index:]

	city = str(filename.split("/")[-1]).replace(".txt", "/")

	try:
		os.mkdir("Cleaned/"+city)
	except:
		print(city +" already there")

	np.savetxt("Cleaned/"+city+"CH_Train.txt", check_train, fmt='%s', delimiter=',')
	np.savetxt("Cleaned/"+city+"CH_Test.txt", check_test, fmt='%s', delimiter=',')
	np.savetxt("Cleaned/"+city+"CO_Train.txt", soc, fmt='%s', delimiter=',')
	# np.savetxt("Cleaned/"+city+"CO_Test.txt", soc_test, fmt='%s', delimiter=',')