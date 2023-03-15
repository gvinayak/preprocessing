import numpy as np
import pickle
import pdb
import datetime
from datetime import timezone
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg

# Cleaning Thresholds
thresh_u = 5
thresh_l = 5
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
	# Significant Users, Locations
	loc_list = []
	for k in range(len(usage)):
		loc_list.append(str(float(usage[k,3]))+ " "+str(float(usage[k,4])))

	del_vec = []
	unique_u, count_u = np.unique(usage[:,1], return_counts=True)
	user_dict = dict(zip(unique_u, count_u))

	unique_l, count_l = np.unique(np.asarray(loc_list), return_counts=True)
	loc_dict = dict(zip(unique_l, count_l))

	for k,v in user_dict.copy().items():
		if v < thresh_u:
			del user_dict[k]

	for k,v in loc_dict.copy().items():
		if v < thresh_l:
			del loc_dict[k]

	for k in range(len(usage)):
		if (loc_list[k] not in loc_dict) or (usage[k,1] not in user_dict):
			del_vec.append(k)

	# Deleting Unwanted Entries from Usage
	if(len(del_vec) > 0):
		usage = np.delete(usage.copy(), np.asarray(del_vec), 0)

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
			look_str = str(lat) + " " + str(lon)
			if(look_str in loc_dict):
				loc_file[loc_dict[look_str], cat_dict[cat]] += 1

	# pdb.set_trace()
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


# Load Files
usage = np.genfromtxt("Data/Talkingdata/events.csv", dtype=str, delimiter=',')
usage = usage[1:]	

print("Done: Loading Usage")

# Reorganizing lat lon
temp = np.copy(usage[:, 3])
usage[:, 3] = usage[:, 4]
usage[:, 4] = temp

# Cleaning Major
app_usage = get_clean_apps()
print("Done: App_Usage Cleaning")

usage = clean_for_china_apps(usage, app_usage)
print("Done: Usage Cleaning for CN and Apps")

usage = cleaning_significant(usage)
print("Done: Usage Cleaning Sig")

# Updating loc and user maps
loc_list = []
for k in range(len(usage)):
	loc_list.append(str(float(usage[k,3]))+ " "+str(float(usage[k,4])))

unique_u = np.unique(usage[:,1])
count_u = np.arange(len(unique_u))
user_dict = dict(zip(unique_u, count_u))

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

app_usage = clean_app_usage(app_usage, event_dict)
print("Done: App_Usage Final Clean")

# Dropping Last Column
usage = np.delete(usage, 4, 1)
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

# # f_1 = open("Cleaned/Tk/Event.txt", "w")
# for k in app_usage:
# 	f_1.write(str())
# 	f_1.write("\n")
# f_1.close()