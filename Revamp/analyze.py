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
	loc = usage[k,1]

	if(user not in usage_dict):
		usage_dict[user] = {}

	if(loc not in usage_dict[user]):
		usage_dict[user][loc] = 0

	usage_dict[user][loc] += 1

max_len = 0
mean_len = []
plot_y = np.zeros((100000))
for k,v in usage_dict.items():
	val_list =  list(v.values())
	val_list.sort(reverse=True)
	usage_dict[k] = val_list
	mean_len.append(len(val_list))
	if len(val_list) > max_len:
		max_len = len(val_list)

	for k in range(len(val_list)):
		plot_y[k] += val_list[k]

max_len = 100
plot_x = np.arange(max_len)
plot_y = plot_y[:max_len]

x = [10, 10]
y = [0, np.amax(plot_y)]

plt.bar(plot_x, plot_y, width = 1)
plt.plot(x, y, 'r')
mean = round(statistics.mean(mean_len), 2)
plt.xlabel("Top K Location"+str(file)) 
plt.ylabel("Count") 
plt.title("Userwise Location Distributiom (Mean = "+str(mean)+")") 
# plt.show() 
plt.savefig(file+'_hist.png')
# pdb.set_trace()

# np.savetxt("SAS/"+file+".txt",usage, fmt='%s', delimiter=' ')