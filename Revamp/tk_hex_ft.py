import numpy as np
import pickle
import pdb
import datetime
from datetime import timezone
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg
import random

# Cleaning Thresholds
thresh_u = 5
thresh_l = 2
thresh_p = 0.8
# thresh_a = 20

def get_clean_apps():
	# Load Files
	app_data = np.genfromtxt("Data/Talkingdata/app_events.csv", dtype=str, delimiter=',')
	app_data = app_data[1:]

	app_cats = pickle.load(open("App_Cats.p", "rb"))

	app_set = set()
	for k in app_cats:
		app_set.add(k[0])

	# Deleting Unactive Apps
	del_vec = []
	for k in range(len(app_data)):
		if app_data[k,2] == 0 or app_data[k,3] == 0 or app_data[k,1] not in app_set:
			del_vec.append(k)

	if(len(del_vec) > 0):
		app_data = np.delete(app_data.copy(), np.asarray(del_vec), 0)
	app_data = np.delete(app_data, 3, 1)
	app_data = np.delete(app_data, 2, 1)
	return app_data

def clean_for_china_apps(usage, app_usage):
	# Making set of all events 
	event_set = set()
	unique = np.unique(app_usage[:,0])
	for k in unique:
		event_set.add(k)

	# Filter for China
	locs_china = []
	for k in range(len(usage)):
		time = datetime.datetime.strptime(str(usage[k,2]),'%Y-%m-%d %H:%M:%S')
		time = time.replace(tzinfo=timezone.utc).timestamp()
		usage[k,2] = time
		lat = round(float(usage[k,3]) * 2, 1) / 2
		lon = round(float(usage[k,4]) * 2, 1) / 2
		usage[k,3] = lat
		usage[k,4] = lon
		locs_china.append((lat, lon))

	# Getting Country by Locations
	results = rg.search(locs_china)

	# Cleaning Error Entries
	del_vec = []
	for k in range(len(results)):
		if (results[k]['cc'] !='CN') or (str(usage[k,0]) not in event_set):
			del_vec.append(k)

	# Deleting Unwanted Entries from Usage
	if(len(del_vec) > 0):
		usage = np.delete(usage.copy(), np.asarray(del_vec), 0)

	return usage

def cleaning_significant(usage):
	# Significant Users, Locations --> Completion based
	inc = 1
	while(inc > 0):
		inc = 0
		del_vec = []
		unique_u, count_u = np.unique(usage[:,1], return_counts=True)
		user_dict = dict(zip(unique_u, count_u))

		unique_l, count_l = np.unique(usage[:,3], return_counts=True)
		loc_dict = dict(zip(unique_l, count_l))

		for k,v in user_dict.copy().items():
			if v < thresh_u:
				del user_dict[k]
				inc = 1

		for k,v in loc_dict.copy().items():
			if v < thresh_l:
				del loc_dict[k]
				inc = 1

		for k in range(len(usage)):
			if (usage[k,3] not in loc_dict) or (usage[k,1] not in user_dict):
				del_vec.append(k)

		if(len(del_vec) > 0):
			usage = np.delete(usage.copy(), np.asarray(del_vec), 0)
		print(inc)

	return usage

def clean_app_usage(app_usage, event_dict):
	# Making Event File
	app_cats = pickle.load(open("App_Cats.p", "rb"))
	app_dict = {}
	app_usage_dict = {}
	
	for k in range(len(app_cats)):
		if (app_cats[k,0] not in app_dict):
			app_dict[app_cats[k,0]] = []
		app_dict[app_cats[k,0]].append(app_cats[k,1])

	# Get Clean Events
	del_vec = []

	for k in range(len(app_usage)):
		if app_usage[k,0] not in event_dict:
			del_vec.append(k)
		else:
			event = event_dict[app_usage[k,0]]
			app_usage[k,0] = event

			if event not in app_usage_dict:
				app_usage_dict[event] = []

			for val in app_dict[app_usage[k,1]]:
				app_usage_dict[event].append(val)
	
	# Deleting Unwanted Entries from App
	if(len(del_vec) > 0):
		app_usage = np.delete(app_usage.copy(), np.asarray(del_vec), 0)

	# Writing File
	f_1 = open("Cleaned/Tk/Event.txt", "w")
	for k,v in app_usage_dict.items():
		if len(v) > 1:
			for i in range(len(v)-1):
				f_1.write(str(v[i]) + " ")
		f_1.write(str(int(v[-1])))
		f_1.write("\n")
	f_1.close()

def make_loc_file(loc_dict):
	locs = pickle.load(open('CN_locs.p', 'rb'))
	unique, count = np.unique(locs[:,2], return_counts=True)
	cat_dict = dict(zip(unique, count))
	cnt = 0

	for k,v in cat_dict.copy().items():
		if v < 5:
			del cat_dict[k]
		else:
			cat_dict[k] = cnt
			cnt += 1
	loc_file = np.zeros((len(loc_dict.keys()), len(cat_dict.keys())))

	cnt = 0
	for k in range(len(locs)):
		cat = locs[k,2]
		if(cat in cat_dict):		
			cnt += 1
			lat = round(float(locs[k,0]) * 2, 1) / 2
			lon = round(float(locs[k,1]) * 2, 1) / 2
			locs[k,0] = lat
			locs[k,1] = lon
			for i in np.arange(1,7):
				look_str = str(lat)+"_"+str(lon)+"_"+str(i)
				if(look_str in loc_dict):
					# print("Hi")
					loc_file[loc_dict[look_str], cat_dict[cat]] += 1

	# Writing File
	f_1 = open("Cleaned/Tk/Loc_Cat.txt", "w")
	for k,v in cat_dict.items():
		f_1.write(str(int(v))+" "+str(k))
		f_1.write("\n")
	f_1.close()

	f_2 = open("Cleaned/Tk/POI.txt", "w")
	for k in range(len(loc_file)):
		f_2.write(str(int(k))+" ")
		row = loc_file[k]
		if len(row) > 1:
			for i in range(len(row)-1):
				f_2.write(str(int(row[i])) + " ")
		f_2.write(str(int(row[-1])))
		f_2.write("\n")
	f_2.close()

def update_locs_hex(usage):
	lat_dict = {}
	loc_list = []
	for k in range(len(usage)):
		lat = float(usage[k,3])
		lon = float(usage[k,4])
		val = str(lat)+"_"+str(lon)
		loc_list.append(val)

		if lat not in lat_dict:
			lat_dict[lat] = []

		app_val = len(loc_list) - 1
		lat_dict[lat].append(app_val)

	lat_keys = np.asarray(sorted(lat_dict))

	for k in range(len(usage)):
		arr = loc_list[k].split("_")
		lat = float(arr[0])
		lon = float(arr[1])
		lat_ind = int(np.where(lat_keys == lat)[0])
		# Generating the inside/outside probability
		p = random.uniform(0, 1)
		if p < thresh_p:
			usage[k,3] = loc_list[k]+"_"+str(random.randint(1,6))

		else:
			usage[k,3] = loc_list[k]+"_"+str(random.randint(7,12))

		# # We divide into 6 axis: 00, 0+, 0-, +0, -0, ++
		# else:
		# 	hex_val = random.randint(1,6)
		# 	# For 0+ >>
		# 	if (hex_val == 1):
		# 		div = 100
		# 		ind_key = lat_keys[lat_ind]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp > 0:
		# 				div = np.abs(comp)
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)

		# 	# For 0- >>
		# 	elif (hex_val == 4):
		# 		div = 100
		# 		ind_key = lat_keys[lat_ind]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp < 0:
		# 				div = comp
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)

		# 	# For -+ >>
		# 	elif (hex_val == 2):
		# 		div = 100
		# 		if(lat_ind == 0):
		# 			usage[k,3] = loc_list[k]+"_5"
		# 			continue
		# 		ind_key = lat_keys[lat_ind-1]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp > 0:
		# 				div = comp
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)
			
		# 	# For -- >>
		# 	elif (hex_val == 3):
		# 		div = 100
		# 		if(lat_ind == 0):
		# 			usage[k,3] = loc_list[k]+"_6"
		# 			continue
		# 		ind_key = lat_keys[lat_ind-1]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp < 0:
		# 				div = comp
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)

		# 	# For ++ >>
		# 	elif (hex_val == 6):
		# 		div = 100
		# 		if(lat_ind == len(lat_keys)-1):
		# 			usage[k,3] = loc_list[k]+"_3"
		# 			continue
		# 		ind_key = lat_keys[lat_ind+1]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp > 0:
		# 				div = comp
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)

		# 	# For +- >>
		# 	elif (hex_val == 5):
		# 		div = 100
		# 		if(lat_ind == len(lat_keys)-1):
		# 			usage[k,3] = loc_list[k]+"_3"
		# 			continue
		# 		ind_key = lat_keys[lat_ind+1]
		# 		matched_index = lat_dict[ind_key][0]
		# 		for i in lat_dict[ind_key]:
		# 			arr = loc_list[i].split("_")
		# 			lat_c = float(arr[0])
		# 			lon_c = float(arr[1])
		# 			comp = lon_c - lon
		# 			if np.abs(comp) < div and comp < 0:
		# 				div = comp
		# 				matched_index = i
		# 		usage[k,3] = loc_list[matched_index]+"_"+str(hex_val)
	
	# Dropping Last Column
	usage = np.delete(usage, 4, 1)
	return usage

# Uncomment for all
# # Load Files
# usage = np.genfromtxt("Data/Talkingdata/events.csv", dtype=str, delimiter=',')
# usage = usage[1:]

# print("Done: Loading Usage")

# # Reorganizing lat lon
# temp = np.copy(usage[:, 3])
# usage[:, 3] = usage[:, 4]
# usage[:, 4] = temp

# # Cleaning Major China Based
# app_usage = get_clean_apps()
# print("Done: App_Usage Cleaning")

# usage = clean_for_china_apps(usage, app_usage)
# print("Done: Usage Cleaning for CN and Apps")

# usage = update_locs_hex(usage)
# print("Done: Making Hex Maps")

# pickle.dump([usage, app_usage], open("Usage_Dump.p", "wb"))

usage, app_usage = pickle.load(open("Tk_Clean/Usage_Dump.p", "rb"))

usage = cleaning_significant(usage)
print("Done: Cleaning Sig")

# pdb.set_trace()
unique_u = np.unique(usage[:,1])
count_u = np.arange(len(unique_u))
user_dict = dict(zip(unique_u, count_u))

loc_list = usage[:,3]
unique_l = np.unique(np.asarray(loc_list))
count_l = np.arange(len(unique_l))
loc_dict = dict(zip(unique_l, count_l))

ec = 0
event_dict = {}
for k in range(len(usage)):
	if(usage[k,0] not in event_dict):
		event_dict[usage[k,0]] = ec
		ec += 1
	usage[k,0] = event_dict[usage[k,0]]
	usage[k,1] = user_dict[usage[k,1]]
	usage[k,3] = loc_dict[loc_list[k]]

print("Done: Usage Final Clean")
# pdb.set_trace()

app_usage = clean_app_usage(app_usage, event_dict)
print("Done: App_Usage Final Clean")

# Dropping Last Column
usage = usage.astype(float)
usage = usage.astype(int)

make_loc_file(loc_dict)
# Reorganizing Usage 
temp = np.copy(usage[:, 0])
usage[:, 0] = usage[:, 1]
usage[:, 1] = temp

temp = np.copy(usage[:, 1])
usage[:, 1] = usage[:, 3]
usage[:, 3] = temp

usage = usage[np.lexsort((usage[:,2], usage[:,0]))]
np.savetxt("Cleaned/Tk/Usage.txt",usage, fmt='%s', delimiter=' ')
del usage
print("Done: Usage Dump")