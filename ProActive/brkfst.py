import numpy as np
import pickle
import pdb
import sys, os
import glob, subprocess
from collections import defaultdict

read_order = ["cereals", "coffee", "friedegg", "juice", "milk", "pancake", "salat", "sandwich", "scrambledegg"]
counts = [108, 110, 21, 77, 23, 52, 78, 71, 71]
video_dict = defaultdict(list)
mark_dict = {}
mark_count = 1

train_e = []
train_t = []
train_g = []
test_e = []
test_t = []
test_g = []

for g in range(len(read_order)):
	goal = read_order[g]
	path = "Breakfast/Raw/segmentation_coarse/"+goal+"/"
	file_count = 1
	for filename in glob.glob(os.path.join(path, '*.txt')):
		sequence = np.genfromtxt(filename, dtype=str, delimiter=' ')
		tmp = []
		ttp = []
		for i in range(len(sequence)):
			mark = sequence[i][1]
			time = int(sequence[i][0].split("-")[0]) - 1
			if mark == 'SIL' and time==1:
				mark = 'SIL_Start'
			elif mark == 'SIL' and time!=1:
				mark = 'SIL_End'
			
			if mark not in mark_dict:
				mark_dict[mark] = mark_count
				mark_count += 1

			tmp.append(mark_dict[mark])
			ttp.append(time)
		if file_count <= 0.8*counts[g]:
			train_e.append(tmp)
			train_t.append(ttp)
			train_g.append(g+1)
		else:
			test_e.append(tmp)
			test_t.append(ttp)
			test_g.append(g+1)
		file_count += 1

ev_train = open("Breakfast/Cleaned/train_ev.txt", "w")
ti_train = open("Breakfast/Cleaned/train_ti.txt", "w")
go_train = open("Breakfast/Cleaned/train_go.txt", "w")
ev_test = open("Breakfast/Cleaned/test_ev.txt", "w")
ti_test = open("Breakfast/Cleaned/test_ti.txt", "w")
go_test = open("Breakfast/Cleaned/test_go.txt", "w")

# Writing train
for i in range(len(train_e)):
	for j in range(len(train_e[i])):
		ev_train.write(str(int(train_e[i][j])))
		ev_train.write(" ")
		ti_train.write(str(float(train_t[i][j])))
		ti_train.write(" ")
	ev_train.write("\n")
	ti_train.write("\n")
	go_train.write(str(int(train_g[i])))
	go_train.write("\n")
ev_train.close()
ti_train.close()
go_train.close()

# Writing test
for i in range(len(test_e)):
	for j in range(len(test_e[i])):
		ev_test.write(str(int(test_e[i][j])))
		ev_test.write(" ")
		ti_test.write(str(float(test_t[i][j])))
		ti_test.write(" ")
	ev_test.write("\n")
	ti_test.write("\n")
	go_test.write(str(int(test_g[i])))
	go_test.write("\n")
ev_test.close()
ti_test.close()
go_test.close()