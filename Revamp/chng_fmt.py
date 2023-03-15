import numpy as np
import pdb, sys
from collections import defaultdict

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
	
	if len(v) > 200:
		x = v[-200:]
		train_dict[k] = x[:-2]

	else:
		train_dict[k] = v[:-2]

dataset = [train_dict, val_dict, test_dict, len(train_dict.keys()), len(item_set)]
np.save('Baselines/'+file+'Partitioned.npy', dataset)