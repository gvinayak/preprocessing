import random, pdb, pickle, sys
import numpy as np
import statistics, os

file = sys.argv[1]
data = np.loadtxt('Amazon/'+file+'.csv', delimiter =',', dtype=str)
data = data[:, 1:]

unique, count = np.unique(data[:,0], return_counts=True)
count_dict = dict(zip(unique, count))

for k,v in count_dict.copy().items():
	if v <= 8:
		del count_dict[k]

del_vec = []
for k in range(len(data)):
	item = data[k,0]
	if item not in count_dict:
		del_vec.append(k)
		continue
	else:
		if type(count_dict[item]) != list:
			count_dict[item] = []
	count_dict[item].append(k - len(del_vec))

# Deleting Unwanted Entries from Usage
if(len(del_vec) > 0):
	data = np.delete(data.copy(), np.asarray(del_vec), 0)

for k,v in count_dict.items():
	time_vec = []
	mark_vec = []
	
	for i in v:
		time_vec.append(int(float(data[i, 2])))
		mark_vec.append(int(float(data[i, 1])))
	time_vec = np.asarray(time_vec)/(60*60*6)
	mark_vec = np.asarray(mark_vec)

	# Sorting by time
	args = np.argsort(time_vec)
	time_vec = time_vec[args]
	mark_vec = mark_vec[args]

	time_vec = time_vec - np.min(time_vec)
	count_dict[k] = [mark_vec, time_vec]

test = int(0.8*len(count_dict))
count = 0

try:
	os.mkdir("Cleaned_Amazon/"+file)
except:
	print(file +" already there")

f1 = open('Cleaned_Amazon/'+file+'/Train_Cat', "w")
f2 = open('Cleaned_Amazon/'+file+'/Train_Time', "w")
f3 = open('Cleaned_Amazon/'+file+'/Test_Cat', "w")
f4 = open('Cleaned_Amazon/'+file+'/Test_Time', "w")

for k,v in count_dict.items():
	mark_vec = v[0]
	time_vec = v[1]
	
	if count < test:
		for i in range(len(mark_vec)):
			f1.write(str(mark_vec[i])+" ")
			f2.write(str(time_vec[i])+" ")
		f1.write("\n")
		f2.write("\n")
	
	else:
		for i in range(len(mark_vec)):
			f3.write(str(mark_vec[i])+" ")
			f4.write(str(time_vec[i])+" ")
		f3.write("\n")
		f4.write("\n")

	count += 1