import numpy as np
import pdb, sys
from collections import defaultdict

def Reverse(lst): 
    return [ele for ele in reversed(lst)] 

file = sys.argv[1]

usage = np.genfromtxt(file+"/Usage.txt", dtype=int, delimiter=' ')
train_dict = defaultdict(list)
val_dict = defaultdict(list)
test_dict = defaultdict(list)

item_set = set()
for k in range(len(usage)):
	user = usage[k,0]
	item = usage[k,1]
	train_dict[user].append(item)
	item_set.add(item)

for k,v in train_dict.items():
	val_dict[k].append(v[-2:][0])
	test_dict[k].append(v[-1:])
	
	# if len(v) > 500:
	# 	x = v[-500:]
	# 	train_dict[k] = x[:-2]

	# else:
	# 	train_dict[k] = v[:-2]
	train_dict[k] = v[:-2]


f = open("Caser/"+file+"/train.txt", "a")

for k,v in train_dict.items():
	for i in Reverse(v):
		f.write(str(k+1)+" "+str(i+1)+" 1\n")
f.close()

f = open("Caser/"+file+"/test.txt", "a")

for k,v in test_dict.items():
	for i in Reverse(v):
		f.write(str(k+1)+" "+str(i[0]+1)+" 1\n")
f.close()
