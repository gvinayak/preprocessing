import numpy as np
import pickle
import pdb
import sys, os
import glob, subprocess
from collections import defaultdict
read_order = ["BaseballPitch.txt", "BasketballBlock.txt", "BasketballDribble.txt", "BasketballDunk.txt", "BasketballGuard.txt", "BasketballPass.txt", "BasketballShot.txt", "VolleyballBlock.txt", "VolleyballBump.txt", "VolleyballServe.txt", "VolleyballSet.txt", "VolleyballSpiking.txt", "PoleVault.txt", "PoleVaultPlantPole.txt", "Shotput.txt", "ShotPutBend.txt", "HammerThrow.txt", "HammerThrowRelease.txt", "HammerThrowSpin.txt", "HammerThrowWindUp.txt", "CricketBowling.txt", "CricketShot.txt", "SoccerPenalty.txt", "CleanAndJerk.txt", "WeightliftingClean.txt", "WeightliftingJerk.txt", "CliffDiving.txt", "Diving.txt", "Billiards.txt", "ClapHands.txt", "DiscusRelease.txt", "DiscusWindUp.txt", "ThrowDiscus.txt", "HighJump.txt", "LongJump.txt", "FrisbeeCatch.txt", "OneHandedCatch.txt", "TwoHandedCatch.txt", "GolfSwing.txt", "JavelinThrow.txt", "CloseUpTalkToCamera.txt", "NoHuman.txt", "TalkToCamera.txt", "TennisSwing.txt", "HighFive.txt", "Hug.txt", "FistPump.txt", "OneRaisedArmCelebrate.txt", "TwoRaisedArmCelebrate.txt", "PatPerson.txt", "PickUp.txt", "BodyBend.txt", "BodyContract.txt", "BodyRoll.txt", "BodyTurn.txt", "Jump.txt", "Run.txt", "Sit.txt", "Squat.txt", "Stand.txt", "StandUp.txt", "Throw.txt", "Walk.txt", "Drop.txt", "Fall.txt"]

def act_func(activity_file):
	activity = defaultdict(int)
	for i in range(len(activity_file)):
		activity[activity_file[i, 1]] = int(activity_file[i, 0])
	return activity

def sorter(v):
	index = np.argsort(np.array(v[1]))
	min_time = min(v[1])
	tmp = []
	ttp = []
	for k in index:
		tmp.append(v[0][k])
		time = v[1][k] - min_time
		ttp.append(time)
	return tmp, ttp

def calc_goal(video, goal_dict, task):
	task = task.lower()
	if task.find("baseball")>=0:
		return 1
	elif task.find("basketball")>=0:
		return 2
	elif task.find("billiards")>=0 or task.find("tennis")>=0:
		return 3
	elif task.find("clean")>=0 or task.find("jerk")>=0:
		return 4
	elif task.find("diving")>=0:
		return 5
	elif task.find("cricket")>=0:
		return 6
	elif task.find("frisbee")>=0 or task.find("javelin")>=0:
		return 7
	elif task.find("highjump")>=0 or task.find("longjump")>=0:
		return 8
	elif task.find("pole")>=0:
		return 9
	elif task.find("hammer")>=0:
		return 10
	elif task.find("golf")>=0:
		return 11
	elif task.find("shotput")>=0:
		return 12
	elif task.find("soccer")>=0:
		return 13
	elif task.find("discus")>=0:
		return 14
	elif task.find("volleyball")>=0:
		return 15
	elif task.find("walk")>=0 or task.find("sit")>=0 or task.find("stand")>=0 or task.find("run")>=0 or task.find("jump")>=0 or task.find("fall")>=0 or task.find("throw")>=0 or task.find("drop")>=0:
		return 16
	elif task.find("hug")>=0 or task.find("patperson")>=0 or task.find("highfive")>=0 or task.find("fistpump")>=0 or task.find("clap")>=0:
		return 17
	elif task.find("celebrate")>=0:
		return 18
	elif task.find("body")>=0 or task.find("squat")>=0:
		return 19
	elif task.find("camera")>=0 or task.find("nohuman")>=0:
		return 20
	return 0

def extract_sequences(sequence, video_dict, mark, goal_dict, task):
	for i in range(len(sequence)):
		video = sequence[i, 0]
		if len(video_dict[video]) == 0:
			video_dict[video].append([])
			video_dict[video].append([])
		st_time = float(sequence[i, 1])
		end_time = float(sequence[i, 2])
		video_dict[video][0].append(mark)
		video_dict[video][1].append(st_time)
		if goal_dict[video] == 0:
			goal_dict[video] = calc_goal(video, goal_dict, task)

	return video_dict, goal_dict

video_dict = defaultdict(list)
goal_dict = defaultdict(int)
path = "Multithumos/Raw/annotations"
activity = np.genfromtxt("Multithumos/Raw/class_list.txt", dtype=str, delimiter=' ')
activity = act_func(activity)
for files in read_order:
	filename = path+"/"+files
	task = filename.split("/")[-1].replace(".txt", "")
	sequence = np.genfromtxt(filename, dtype=str, delimiter=' ')
	video_dict, goal_dict = extract_sequences(sequence, video_dict, activity[task], goal_dict, task)

for k,v in goal_dict.items():
	if v == 0 or v == None:
		print(k)
		for i in video_dict[k][0]:
			for j, r in activity.items():
				if r == i:
					print(j)

train_e = []
train_t = []
train_g = []
test_e = []
test_t = []
test_g = []

for k,v in video_dict.items():
	if len(v[0]) < 5:
		continue
	marks, times = sorter(v)
	if k.find("validation") >= 0:
		train_e.append(marks)
		train_t.append(times)
		train_g.append(goal_dict[k])

	elif k.find("test") >= 0:
		test_e.append(marks)
		test_t.append(times)
		test_g.append(goal_dict[k])

ev_train = open("Multithumos/Cleaned/train_ev.txt", "w")
ti_train = open("Multithumos/Cleaned/train_ti.txt", "w")
go_train = open("Multithumos/Cleaned/train_go.txt", "w")
ev_test = open("Multithumos/Cleaned/test_ev.txt", "w")
ti_test = open("Multithumos/Cleaned/test_ti.txt", "w")
go_test = open("Multithumos/Cleaned/test_go.txt", "w")

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