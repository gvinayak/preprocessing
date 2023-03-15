import numpy as np
import pickle
import pdb
import datetime
import time, math
import sys, os
import glob, subprocess
import geopy.distance

def clean_up(un_check, un_con, check_t):
	order = {}
	cat_order = {}
	loc_dict = {}
	count = 0
	loc_count = 0
	cat_count = 0

	for k in range(len(un_con)):
		user1 = un_con[k,0]
		user2 = un_con[k,1]
		if(user1 not in order):
			order[user1] = count
			count += 1

		if(user2 not in order):
			order[user2] = count
			count += 1
		
		un_con[k,0] = order[un_con[k,0]]
		un_con[k,1] = order[un_con[k,1]]

	for k in range(len(un_check)):
		user = un_check[k,0]
		loc = un_check[k,1]
		cat = un_check[k,5]

		if(user not in order):
			order[user] = count
			count += 1

		if(loc not in loc_dict):
			loc_dict[loc] = loc_count
			loc_count += 1

		if(cat not in cat_order):
			cat_order[cat] = cat_count
			cat_count += 1

		un_check[k,0] = int(order[user])
		un_check[k,1] = int(loc_dict[loc])
		un_check[k,5] = int(cat_order[cat])

	for k in range(len(check_t)):
		user = check_t[k,0]
		loc = check_t[k,1]
		cat = check_t[k,5]

		if(user not in order):
			order[user] = count
			count += 1

		if(loc not in loc_dict):
			loc_dict[loc] = loc_count
			loc_count += 1

		if(cat not in cat_order):
			cat_order[cat] = cat_count
			cat_count += 1

		check_t[k,0] = int(order[user])
		check_t[k,1] = int(loc_dict[loc])
		check_t[k,5] = int(cat_order[cat])

	return un_check, un_con, check_t

def update_fsq(un_check, un_con, check_t):
	for k in range(len(un_check)):
		un_check[k,0] = un_check[k,0] +"_f"
		un_check[k,1] = un_check[k,1] +"_f"
		un_check[k,5] = un_check[k,5] +"_f"

	for k in range(len(un_con)):
		un_con[k,0] = un_con[k,0] +"_f"
		un_con[k,1] = un_con[k,1] +"_f"
	
	for k in range(len(check_t)):
		check_t[k,0] = check_t[k,0] +"_f"
		check_t[k,1] = check_t[k,1] +"_f"
		check_t[k,5] = check_t[k,5] +"_f"

	return un_check, un_con, check_t

def update_gow(un_check, un_con, check_t):
	for k in range(len(un_check)):
		un_check[k,0] = un_check[k,0] +"_g"
		un_check[k,1] = un_check[k,1] +"_g"
		un_check[k,5] = un_check[k,5] +"_g"

	for k in range(len(un_con)):
		un_con[k,0] = un_con[k,0] +"_g"
		un_con[k,1] = un_con[k,1] +"_g"
	
	for k in range(len(check_t)):
		check_t[k,0] = check_t[k,0] +"_g"
		check_t[k,1] = check_t[k,1] +"_g"
		check_t[k,5] = check_t[k,5] +"_g"

	return un_check, un_con, check_t

# place = sys.argv[1]
thresh_dist = 50
user_loc_norm = 10
loc_list = ["Aichi", "Baden-Wuerttemberg", "Bavaria", "Berlin", "California", "Hyogo", "Kyoto", 
	"Massachusetts", "North_Rhine-Westphalia", "Ohio", "Texas", "Tokyo", "Washington"]

for place in loc_list:
	print(place)
	if(place == "Aichi"):
		place_2 = "AI_JP"
	
	if(place == "Baden-Wuerttemberg"):
		place_2 = "BW_DE"
		
	if(place == "Bavaria"):
		place_2 = "BV_DE"
		
	if(place == "Berlin"):
		place_2 = "BE_DE"
		
	if(place == "California"):
		place_2 = "CA_US"
		
	if(place == "Hyogo"):
		place_2 = "HY_JP"
		
	if(place == "Kyoto"):
		place_2 = "KY_JP"
		
	if(place == "Massachusetts"):
		place_2 = "MA_US"
		
	if(place == "North_Rhine-Westphalia"):
		place_2 = "NR_DE"
		
	if(place == "Ohio"):
		place_2 = "OH_US"
		
	if(place == "Texas"):
		place_2 = "TX_US"
		
	if(place == "Tokyo"):
		place_2 = "TY_JP"
		
	if(place == "Washington"):
		place_2 = "WA_US"


	path = "Cleaned/"+place+"/"
	# Load Fsq
	fsq_un_check = np.genfromtxt("Fsq/"+path+"CH_Train.txt", dtype=str, delimiter=',')
	fsq_un_con = np.genfromtxt("Fsq/"+path+"CO_Train.txt", dtype=str, delimiter=',')
	fsq_check_t = np.genfromtxt("Fsq/"+path+"CH_Test.txt", dtype=str, delimiter=',')

	# Load Gow
	gow_un_check = np.genfromtxt("Gowalla/"+path+"CH_Train.txt", dtype=str, delimiter=',')
	gow_un_con = np.genfromtxt("Gowalla/"+path+"CO_Train.txt", dtype=str, delimiter=',')
	gow_check_t = np.genfromtxt("Gowalla/"+path+"CH_Test.txt", dtype=str, delimiter=',')

	# Removing the time from Gowalla
	gow_un_con = gow_un_con[:, :-1]

	fsq_un_check, fsq_un_con, fsq_check_t = update_fsq(fsq_un_check, fsq_un_con, fsq_check_t)
	gow_un_check, gow_un_con, gow_check_t = update_gow(gow_un_check, gow_un_con, gow_check_t)

	un_check = np.concatenate((fsq_un_check, gow_un_check), axis = 0)
	un_con = np.concatenate((fsq_un_con, gow_un_con), axis = 0)
	check_t = np.concatenate((fsq_check_t, gow_check_t), axis = 0)

	un_check, un_con, check_t = clean_up(un_check, un_con, check_t)
	# pdb.set_trace()

	# Saving the locations
	us_dict = {}
	loc_coord = {}
	loc_cat = {}
	usr_loc_dict = {}
	for k in range(len(un_check)):
		user = un_check[k,0] 
		loc = un_check[k,1]

		if user not in us_dict:
			us_dict[user] = []
			usr_loc_dict[user] = {}
		
		us_dict[user].append(k)

		if(un_check[k,1] in usr_loc_dict[user]):
			if(usr_loc_dict[user][un_check[k,1]] <= float(un_check[k,2])):
				usr_loc_dict[user][un_check[k,1]] = float(un_check[k,2])

		else:
			usr_loc_dict[user][un_check[k,1]] = float(un_check[k,2])

		if int(loc) not in loc_coord:
			loc_coord[int(loc)] = [float(un_check[k,3]), float(un_check[k,4])]
			loc_cat[int(loc)] = float(un_check[k,5])

	# Since the checkins are in sorted order
	loc_set = set()
	for k, v in us_dict.items():
		for i in range(len(v)-1):
			loc_set.add(frozenset((int(un_check[v[i],1]), int(un_check[v[i+1], 1]))))

	loc_set = [list(k) for k in list(loc_set)]

	dist = []
	for k in loc_set:
		if(len(k) >= 2):
			dist.append(geopy.distance.geodesic(loc_coord[k[0]], loc_coord[k[1]]).km)
		else:
			dist.append(0)

	dist = np.asarray(dist)

	var = np.var(dist[dist <= thresh_dist])
	dist = [np.exp(-(k**2)/var) if k <= thresh_dist else 0 for k in dist]

	try:
		os.mkdir("Graphs/"+place_2)
	except:
		print(place_2 +" already there")

	f_1 = open("Graphs/"+place_2+"/"+place_2+"_Loc", "w")
	f_2 = open("Graphs/"+place_2+"/"+place_2+"_Cat", "w")
	f_3 = open("Graphs/"+place_2+"/"+place_2+"_Pref", "w")
	f_4 = open("Graphs/"+place_2+"/"+place_2+"_User", "w")
	f_5 = open("Graphs/"+place_2+"/"+place_2+"_Test", "w")

	for k in range(len(dist)):
		if(dist[k] != 0 and (len(loc_set[k]) >= 2)):
			f_1.write(str(loc_set[k][0])+","+str(loc_set[k][1])+","+str(np.round(dist[k], 5)))
			f_1.write("\n")
	f_1.close()

	for k,v in loc_cat.items():
		f_2.write(str(k)+","+str(v))
		f_2.write("\n")
	f_2.close()

	for k,v in usr_loc_dict.items():
		temp = []
		for k_2,v_2 in usr_loc_dict[k].items():
			temp.append(v_2)
		temp = np.asarray(temp)
		denm = np.mean(temp) + np.var(temp)
		for k_2,v_2 in usr_loc_dict[k].items():
			if(v_2 > denm):
				label = 10
			else:
				label = math.ceil((v_2/denm)*user_loc_norm)
			usr_loc_dict[k][k_2] = label
			f_3.write(str(k)+","+str(k_2)+","+str(label))
			f_3.write("\n")
	f_3.close()

	for k in range(len(un_con)):
		f_4.write(un_con[k,0]+","+un_con[k,1]+",1")
		f_4.write("\n")
	f_4.close()

	for k in range(len(check_t)):
		user = check_t[k,0] 
		loc = check_t[k,1]
		if user in usr_loc_dict and int(loc) in loc_coord and loc in usr_loc_dict[user]:
			f_5.write(check_t[k,0]+","+check_t[k,1]+","+str(usr_loc_dict[user][loc]))
			f_5.write("\n")
	f_5.close()

