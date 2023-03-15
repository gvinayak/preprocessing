import numpy as np
import pickle
import pdb
import datetime
from datetime import timezone
import time
import sys, os
import glob, subprocess
import random
# Cleaning Thresholds
thresh_u = 5
thresh_l = 5

def cleaning_significant(usage):
	# Significant Users, Locations --> Completion based
	inc = 1
	while(inc > 0):
		del_vec = []
		inc = 0
		# Significant Users, Locations, Apps
		unique_u, count_u = np.unique(usage[:,0], return_counts=True)
		user_dict = dict(zip(unique_u, count_u))
		unique_l, count_l = np.unique(usage[:,2], return_counts=True)
		loc_dict = dict(zip(unique_l, count_l))

		# Cleaning as per count 
		for k,v in user_dict.copy().items():
			if v < thresh_u:
				del user_dict[k]
				inc = 1

		for k,v in loc_dict.copy().items():
			if v < thresh_l:
				del loc_dict[k]
				inc = 1

		for k in range(len(usage)):
			if usage[k,0] not in user_dict or usage[k,2] not in loc_dict:
				del_vec.append(k)
		
		# Deleting Unwanted Entries from Usage
		if(len(del_vec) > 0):
			usage = np.delete(usage.copy(), np.asarray(del_vec), 0)

		print(inc)

	print("Done: Cleaned Dicts")
	return usage

# Read the files
app2cat = np.genfromtxt("Data/Li/App2Category.txt", dtype=int, delimiter='\t')
usage = np.genfromtxt("Data/Li/App_usage_trace.txt", dtype=str, delimiter=' ')
poi = np.genfromtxt("Data/Li/Base_poi.txt", dtype=str, delimiter='\t')
cats = np.genfromtxt("Data/Li/Categorys.txt", dtype=int, delimiter='\t')

print("Done Loading")
for k in range(len(usage)):
	hex_val = random.randint(1,12)
	usage[k,2] = usage[k,2]+"_"+str(hex_val)

usage = cleaning_significant(usage)

# Making the dicts again
unique_u, count_u = np.unique(usage[:,0], return_counts=True)
user_dict = dict(zip(unique_u, count_u))
unique_l, count_l = np.unique(usage[:,2], return_counts=True)
loc_dict = dict(zip(unique_l, count_l))
unique_a, count_a = np.unique(usage[:,3], return_counts=True)
app_dict = dict(zip(unique_a, count_a))

# Check if apps categories are missing
app_cat_dict = {}
all_cats = set(cats[:,0].flatten())
used_cats = set()

for k in app2cat:
	if(str(k[0]) in app_dict):
		used_cats.add(k[1])
del_cats = list(all_cats - used_cats)
if len(del_cats) > 0:
	print("Incorrect")

for k in app2cat:
	app_cat_dict[k[0]] = k[1]

# Making maps for all
user_map = {}
loc_map = {}

# Cleaning Usage
user_count = 0
loc_count = 0
app_count = 0

for k in range(len(usage)):
	if usage[k,0] not in user_map:
		user_map[usage[k,0]] = user_count
		user_count += 1
	usage[k,0] = user_map[usage[k,0]]

	if usage[k,2] not in loc_map:
		loc_map[usage[k,2]] = loc_count
		loc_count += 1
	usage[k,2] = loc_map[usage[k,2]]

print("Done: Cleaned Usage")

# Cleaning Locations
poi_cat = {}
for k in range(len(poi[0])-1):
	poi_cat[k] = poi[0,k+1]
poi = poi[1:]

poi_dump = []
del_vec = []
for k in range(len(poi)):
	for i in np.arange(1,7):
		look_str = str(poi[k,0])+"_"+str(i)

		if look_str in loc_map:
			temp = poi[k].copy()
			temp[0] = loc_map[look_str]
			poi_dump.append(temp)

# pdb.set_trace()
poi_dump = np.asarray(poi_dump)
poi_dump = poi_dump.astype(int)
poi_dump = poi_dump[poi_dump[:,0].argsort()]

print("Done: Cleaned Locs")
# New format by swapping time and loc
temp = np.copy(usage[:, 1])
usage[:, 1] = usage[:, 2]
usage[:, 2] = temp

# Replacing time to unix time
for k in range(len(usage)):
	time = datetime.datetime.strptime(str(usage[k,2]),'%Y%m%d%H%M%S')
	time = time.replace(tzinfo=timezone.utc).timestamp()
	usage[k,2] = time

usage = usage.astype(float)
usage = usage.astype(int)
# pdb.set_trace()

# Setting up Event No
event_dict = {}
event_num = -1
del_vec = []
k = 0
while (k < len(usage)):
	event_num += 1
	usage[k,4] = event_num

	if(event_num not in event_dict):
		event_dict[event_num] = []
	event_dict[event_num].append(app_cat_dict[usage[k,3]])

	if(k+1 < len(usage)):
		while usage[k+1,1] == usage[k,1] and usage[k+1,2] < (usage[k,2] + 1800):     #For time and location-wise
		# while usage[k+1,1] == usage[k,1]:       #For location-wise
			if(event_num not in event_dict):
				event_dict[event_num] = []
			event_dict[event_num].append(app_cat_dict[usage[k,3]])

			k += 1
			del_vec.append(k)
			if(k+1 >= len(usage)):
				break
	k += 1

print("Done: Setting Event")

if(len(del_vec) > 0):
	usage = np.delete(usage.copy(), np.asarray(del_vec), 0)

# Removing App Column
usage = np.delete(usage, 3, 1)

# pdb.set_trace()
f_1 = open("Cleaned/Li/Event.txt", "w")
f_2 = open("Cleaned/Li/Loc_Cat", "w")

# Writing Event Data
for k,v in event_dict.items():
	if len(v) > 1:
		for i in range(len(v)-1):
			f_1.write(str(v[i]) + " ")
	f_1.write(str(int(v[-1])))
	f_1.write("\n")
f_1.close()

# Writing Usage and Location Data
np.savetxt("Cleaned/Li/Usage.txt",usage, fmt='%s', delimiter=' ')
np.savetxt("Cleaned/Li/POI.txt", poi_dump, fmt='%s', delimiter=' ')

for k,v in poi_cat.items():
	f_2.write(str(k)+" "+str(v))
	f_2.write("\n")
f_2.close()