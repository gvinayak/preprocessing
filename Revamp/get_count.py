import numpy as np
import pdb, sys
import matplotlib.pyplot as plt  
import statistics

file = sys.argv[1]

usage = np.genfromtxt(file+"/Usage.txt", dtype=int, delimiter=' ')
usage = usage[:,:2]

usage_dict = {}
for k in range(len(usage)):
	user = usage[k,0]
	# loc = usage[k,1]

	if(user not in usage_dict):
		usage_dict[user] = 0
	
	usage_dict[user] += 1

for k,v in usage_dict.items():
	if v < 2:
		print(k)