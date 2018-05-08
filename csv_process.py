#!/usr/bin/env python3

import os, sys, glob
csv_dir = os.getcwd()
csvs = glob.glob(os.path.join(csv_dir, "*.csv"))
# Iterate through directory of csv files
for a_csv in csvs:
	# Check if this csv is in the list of csv files processed
	try:
		f = open(os.path.join(csv_dir, "processed.txt"), 'r')
		f = f.read().split("\n")
		if a_csv in f:
			del f
			continue
		del f
	except:
		pass
	current_dataset = open(a_csv, 'r')
	current_dataset_r = current_dataset.read().split("\n")
	activityid = current_dataset_r[0].index("act_id")
	try:
		lastid = current_dataset_r[1].split(",")[activityid]
	except:
		continue
	poly_points = {}
	poly_points[lastid] = []
	for l in current_dataset_r[1:]:
		# Get the point info for the current polyline
		l = l.split(",")
		lat, lon = l[-2:]
		id = l[activityid]
		if id != lastid:
			lastid = id
			# End this polyline and start a new polyline
			poly_points[id] = []
			poly_points[id].append([lat, lon, 0.0])
		else:
			poly_points[id].append([lat, lon, 0.0])
	existing_geojson = open("strava.geojson", "r")
	existing_geojson_r = existing_geojson.read()
	
	# Write out that we have processed this CSV file so that 
	# on next run, we do not have it repeat process.
	f = open(os.path.join(csv_dir, "processed.txt"), 'a')
	f.write(a_csv)
	f.write("\n")
	f.close()
