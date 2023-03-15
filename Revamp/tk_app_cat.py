import numpy as np
import pickle
import pdb
import datetime
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg

TopK = 30
# Load Files
app_cats = np.genfromtxt("Data/Talkingdata/app_labels.csv", dtype=str, delimiter=',')
app_cats = app_cats[1:]

unique, count = np.unique(app_cats[:,1], return_counts=True)
ac_dict = dict(zip(unique, count))
count = np.sort(count)
count = count[-TopK:]
count = count[0]

app_cnt = 0
for k,v in ac_dict.copy().items():
	if v < count:
		del ac_dict[k]

	else:
		ac_dict[k] = app_cnt
		app_cnt += 1

del_vec = []
for k in range(len(app_cats)):
	if(app_cats[k,1] not in ac_dict):
		del_vec.append(k)

	else:
		app_cats[k,1] = ac_dict[app_cats[k,1]]

# Deleting Unwanted Entries from Usage
if(len(del_vec) > 0):
	app_cats = np.delete(app_cats.copy(), np.asarray(del_vec), 0)

pickle.dump(app_cats, open("App_Cats.p", "wb"))

f_1 = open("Cleaned/Tk/Label_Map.txt", "w")
# Writing Event Data
for k,v in ac_dict.items():
	f_1.write(str(k)+" "+str(v))
	f_1.write("\n")
f_1.close()

print("Done: App Step 1")
# pdb.set_trace()