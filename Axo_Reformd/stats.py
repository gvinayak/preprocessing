import numpy as np
import pickle
import pdb
import datetime
import time, math
import sys, os
import glob, subprocess
import geopy.distance

path = "Graphs/"
print("(#Users, #Location)")
# for folder in glob.glob(os.path.join(path, '*.txt')):
for folder in os.walk(path):
	split = folder[0].split("/") 
	if split[1] == '':
		continue
	place = split[1]
	# print(place)

	un_check = np.genfromtxt("Graphs/"+place+"/"+place+"_Pref", dtype=str, delimiter=',')
	un_loc = np.genfromtxt("Graphs/"+place+"/"+place+"_Loc", dtype=str, delimiter=',')
	un_con = np.genfromtxt("Graphs/"+place+"/"+place+"_User", dtype=str, delimiter=',')
	un_tst = np.genfromtxt("Graphs/"+place+"/"+place+"_Test", dtype=str, delimiter=',')
	
	num_user = max([np.max(un_check[:,0].astype(int)), np.max(un_tst[:,0].astype(int))])
	num_loc = np.max(un_check[:,1].astype(int))
	print(str(place)+" ("+str(num_user)+","+str(num_loc)+str(")"))
	# pdb.set_trace()
	# Finding no. of users



# 	fsq_un_con = np.genfromtxt("Fsq/"+path+"CO_Train.txt", dtype=str, delimiter=',')
# 	fsq_check_t = np.genfromtxt("Fsq/"+path+"CH_Test.txt", dtype=str, delimiter=',')

# 	# Load Gow
# 	gow_un_check = np.genfromtxt("Gowalla/"+path+"CH_Train.txt", dtype=str, delimiter=',')
# 	gow_un_con = np.genfromtxt("Gowalla/"+path+"CO_Train.txt", dtype=str, delimiter=',')
# 	gow_check_t = np.genfromtxt("Gowalla/"+path+"CH_Test.txt", dtype=str, delimiter=',')

# 	# Removing the time from Gowalla
# 	gow_un_con = gow_un_con[:, :-1]

# 	fsq_un_check, fsq_un_con, fsq_check_t = update_fsq(fsq_un_check, fsq_un_con, fsq_check_t)
# 	gow_un_check, gow_un_con, gow_check_t = update_gow(gow_un_check, gow_un_con, gow_check_t)

# 	un_check = np.concatenate((fsq_un_check, gow_un_check), axis = 0)
# 	un_con = np.concatenate((fsq_un_con, gow_un_con), axis = 0)
# 	check_t = np.concatenate((fsq_check_t, gow_check_t), axis = 0)

# 	un_check, un_con, check_t = clean_up(un_check, un_con, check_t)
# 	# pdb.set_trace()

# 	# Saving the locations
# 	us_dict = {}
# 	loc_coord = {}
# 	loc_cat = {}
# 	usr_loc_dict = {}
# 	for k in range(len(un_check)):
# 		user = un_check[k,0] 
# 		loc = un_check[k,1]

# 		if user not in us_dict:
# 			us_dict[user] = []
# 			usr_loc_dict[user] = {}
		
# 		us_dict[user].append(k)

# 		if(un_check[k,1] in usr_loc_dict[user]):
# 			if(usr_loc_dict[user][un_check[k,1]] <= float(un_check[k,2])):
# 				usr_loc_dict[user][un_check[k,1]] = float(un_check[k,2])

# 		else:
# 			usr_loc_dict[user][un_check[k,1]] = float(un_check[k,2])

# 		if int(loc) not in loc_coord:
# 			loc_coord[int(loc)] = [float(un_check[k,3]), float(un_check[k,4])]
# 			loc_cat[int(loc)] = float(un_check[k,5])

# 	# Since the checkins are in sorted order
# 	loc_set = set()
# 	for k, v in us_dict.items():
# 		for i in range(len(v)-1):
# 			loc_set.add(frozenset((int(un_check[v[i],1]), int(un_check[v[i+1], 1]))))

# 	loc_set = [list(k) for k in list(loc_set)]

# 	dist = []
# 	for k in loc_set:
# 		if(len(k) >= 2):
# 			dist.append(geopy.distance.geodesic(loc_coord[k[0]], loc_coord[k[1]]).km)
# 		else:
# 			dist.append(0)

# 	dist = np.asarray(dist)

# 	var = np.var(dist[dist <= thresh_dist])
# 	dist = [np.exp(-(k**2)/var) if k <= thresh_dist else 0 for k in dist]

# 	try:
# 		os.mkdir("Graphs/"+place_2)
# 	except:
# 		print(place_2 +" already there")

	# f_1 = open("Graphs/"+place_2+"/"+place_2+"_Loc", "w")
# 	f_2 = open("Graphs/"+place_2+"/"+place_2+"_Cat", "w")
# 	f_3 = open("Graphs/"+place_2+"/"+place_2+"_Pref", "w")
# 	f_4 = open("Graphs/"+place_2+"/"+place_2+"_User", "w")
# 	f_5 = open("Graphs/"+place_2+"/"+place_2+"_Test", "w")

# 	for k in range(len(dist)):
# 		if(dist[k] != 0 and (len(loc_set[k]) >= 2)):
# 			f_1.write(str(loc_set[k][0])+","+str(loc_set[k][1])+","+str(np.round(dist[k], 5)))
# 			f_1.write("\n")
# 	f_1.close()

# 	for k,v in loc_cat.items():
# 		f_2.write(str(k)+","+str(v))
# 		f_2.write("\n")
# 	f_2.close()

# 	for k,v in usr_loc_dict.items():
# 		temp = []
# 		for k_2,v_2 in usr_loc_dict[k].items():
# 			temp.append(v_2)
# 		temp = np.asarray(temp)
# 		denm = np.mean(temp) + np.var(temp)
# 		for k_2,v_2 in usr_loc_dict[k].items():
# 			if(v_2 > denm):
# 				label = 10
# 			else:
# 				label = math.ceil((v_2/denm)*user_loc_norm)
# 			usr_loc_dict[k][k_2] = label
# 			f_3.write(str(k)+","+str(k_2)+","+str(label))
# 			f_3.write("\n")
# 	f_3.close()

# 	for k in range(len(un_con)):
# 		f_4.write(un_con[k,0]+","+un_con[k,1]+",1")
# 		f_4.write("\n")
# 	f_4.close()

# 	for k in range(len(check_t)):
# 		user = check_t[k,0] 
# 		loc = check_t[k,1]
# 		if user in usr_loc_dict and int(loc) in loc_coord and loc in usr_loc_dict[user]:
# 			f_5.write(check_t[k,0]+","+check_t[k,1]+","+str(usr_loc_dict[user][loc]))
# 			f_5.write("\n")
# 	f_5.close()

