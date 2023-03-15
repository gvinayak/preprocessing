import numpy as np
import pickle
import pdb
import sys, os
import json
import glob, subprocess
from collections import defaultdict

def check_goal(mark, goal_dict):
	return goal_dict[mark]

f = open('ActivityNet/activity_net.v1-3.min.json',)
data = json.load(f)
f.close()
goal_dict = {}
mark_dict = {}
mark_count = 1
goal_index = {}

for k in data['taxonomy']:
	goal_dict[k['nodeName']] = k['parentName']

train_e = []
train_t = []
train_g = []
test_e = []
test_t = []
test_g = []

# for i in range(len(goal_dict)):
# 	name = goal_dict[i]['parentName']
# 	for j in range(len(goal_dict)):
# 		if name == goal_dict[j]['nodeName']:
# 			print(goal_dict[i]['nodeName'], goal_dict[i]['parentName'],  goal_dict[j]['nodeName'], goal_dict[j]['parentName'])
# 			print("HI")
# sum = 0

for k,v in data['database'].items():
	x = data['database'][k]['annotations']
	if len(x) < 5:
		continue
	tmp = []
	ttp = []
	for i in range(len(x)):
		time = x[i]['segment'][0]
		mark = check_goal(x[i]['label'], goal_dict)
		if mark not in mark_dict:
			mark_dict[mark] = mark_count
			mark_count += 1
		tmp.append(mark_dict[mark])
		ttp.append(time)

	train_e.append(tmp)
	train_t.append(ttp)

ev_train = open("ActivityNet/Cleaned/train_ev.txt", "w")
ti_train = open("ActivityNet/Cleaned/train_ti.txt", "w")

# Writing train
for i in range(len(train_e)):
	for j in range(len(train_e[i])):
		ev_train.write(str(int(train_e[i][j])))
		ev_train.write(" ")
		ti_train.write(str(float(train_t[i][j]) - float(train_t[i][0])))
		ti_train.write(" ")
	ev_train.write("\n")
	ti_train.write("\n")
ev_train.close()
ti_train.close()