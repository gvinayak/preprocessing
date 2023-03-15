import numpy as np
import pickle
import pdb
import datetime
import time
import sys, os
import glob, subprocess
import reverse_geocoder as rg

# Load the Locations Data and Make Dump
places = "Data/Foursquare/raw_POIs.txt"
file = np.loadtxt(places, delimiter ='\t', dtype=str)

locs = []
for k in file:
	locs.append((k[1], k[2]))
results = rg.search(locs)

real_vals = []

for k in range(len(results)):
	if results[k]['cc'] =='CN':
		real_vals.append(k)

real_vals = np.asarray(real_vals)
file = file[real_vals]
file = file[:,1:]
file = file[:,:-1]

pickle.dump(file, open('CN_locs.p', 'wb'))