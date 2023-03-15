import numpy as np
import pickle
import pdb
import datetime
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg

def initial_divide():
	# Load the Locations Data
	places = open("/home/vinayak/Desktop/My_Work/app/Data/Foursquare/raw_POIs.txt")
	main_vec = []
	line = places.readline()
	locs = []
	line_count = 0
	loc_hash = {}
	cat_dict = {}
	cat_count = 0
	while line:
		temp = []
		line = line.rstrip()
		arr = line.split('\t')
		if(len(arr) == 5):
			temp.append(arr[0])
			temp.append(float(arr[1]))
			temp.append(float(arr[2]))
			temp.append(arr[3])
			if arr[3] not in cat_dict:
				cat_dict[arr[3]] = cat_count
				cat_count += 1

			locs.append((arr[1], arr[2]))

			main_vec.append(temp)
			loc_hash[temp[0]] = line_count
			line_count += 1

		line = places.readline()

	places.close()
	main_vec = np.asarray(main_vec)

	results = rg.search(locs)

	loc_dict = {}

	for k in range(len(results)):
		if results[k]['cc'] != 'JP' and results[k]['cc'] != 'DE' and results[k]['cc'] != 'ES':
			continue

		if results[k]['admin1'] not in loc_dict:
			loc_dict[results[k]['admin1']] = set()

		loc_dict[results[k]['admin1']].add(main_vec[k,0])
	
	# loc_set = set(["California", "Texas"])
	# Removing unimportant cities
	# for k,v in loc_dict.copy().items():
	# 	if(k not in loc_set):
	# 		del loc_dict[k]

	# pickle.dump([loc_dict, loc_hash], open("Location_Dump.p", "wb"))
	# loc_dict, loc_hash = pickle.load(open("Location_Dump.p", "rb"))
	# print("Loaded")

	# Load and Store Checkins
	if '' in loc_dict.keys():
		del loc_dict['']

	check = open("/home/vinayak/Desktop/My_Work/app/Data/Foursquare/WWW_Checkins.txt")
	line = check.readline()
	unfiltered_checkins = []

	c = 0
	while line:
		if(c % 100000 ==0):
			print("Reached ", c)
		line = line.rstrip()
		arr = line.split('\t')
		if(len(arr) == 4):
			user = arr[0]
			location = arr[1]
			if(location in loc_hash):
				for k,v in loc_dict.items():
					if location in v:
						with open("EU/"+str(k)+".txt", 'a') as f:
							f.write(str(user))
							f.write(",")
							f.write(str(location))
							f.write(",")
							for i in range(1, len(main_vec[loc_hash[location]])- 1):
								f.write(str(main_vec[loc_hash[location], i]))
								f.write(",")
							f.write(str(cat_dict[main_vec[loc_hash[location], i+1]]))
							f.write(",")
						
							# Format Tue Apr 03 18:00:07 +0000 2012
							arr[2] = arr[2][:-11]+" "+arr[2][-4:]
							f.write(str(datetime.datetime.strptime(arr[2], '%a %b %d %H:%M:%S %Y')))
							f.write("\n")
		line = check.readline()
		c += 1
	check.close()

# ========== Main code starts here ==========
subprocess.run("rm -rf EU/*", shell=True, check=True)
initial_divide()