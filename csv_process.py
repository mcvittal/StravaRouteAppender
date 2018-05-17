#!/usr/bin/env python3

import os, sys, glob, json
from simplify import *
os.chdir("/users/ajmcvitt/strava")
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
        activityid = current_dataset_r[0].split(",").index("act_id")
        startdate = current_dataset_r[0].split(",").index("act_startDate")
        print(activityid)
        print(current_dataset_r[1].split(","))
        lastid = current_dataset_r[1].split(",")[activityid]
        startdates = {}
        startdates[lastid] = current_dataset_r[1].split(",")[startdate].split(" ")[0]
        print(lastid)
        poly_points = {}
        poly_points[lastid] = []
        for l in current_dataset_r[1:]:
                # Get the point info for the current polyline
                l = l.split(",")
                try:
                    lat, lon = [float(n) for n in l[-2:]]
                except:
                    continue
                id = l[activityid]
                if id != lastid:
                        lastid = id
                        # End this polyline and start a new polyline
                        poly_points[id] = []
                        startdates[id] = l[startdate].split(" ")[0]
                        poly_points[id].append({"x":lon, "y":lat})
                else:
                        poly_points[id].append({"x":lon, "y":lat})
        with open('strava.geojson') as strava_j:
            data = json.load(strava_j)
        flags = {}
        for an_id in poly_points.keys():
            yr,mn,dy =[ int(i) for i in startdates[an_id].split("-") ]
            if yr != 2018:
                continue
            elif mn < 5:
                continue
            elif mn == 5 and dy < 25:
                continue
            elif mn == 8 and dy > 16:
                continue
            elif mn > 8:
                continue
            #Simplify geometries
            #print(simplify(poly_points[an_id], 0.3, True))
            poly_points[an_id] = [[l['x'], l['y']] for l in simplify(poly_points[an_id], 0.01, True)]
            for f in data["features"]:
                if f["geometry"]["coordinates"] == poly_points[an_id]:
                    flags[an_id] = True
                    break
            if an_id not in flags.keys():
                data["features"].append({"type": "Feature",
                    "properties": { "id": "null"},
                    "geometry": { "type": "LineString", "coordinates": poly_points[an_id] }})
        with open('strava.geojson', 'w') as fp:
            json.dump(data, fp)

        # Write out that we have processed this CSV file so that
        # on next run, we do not have it repeat process.
        f = open(os.path.join(csv_dir, "processed.txt"), 'a')
        f.write(a_csv)
        f.write("\n")
        f.close()
# Simplify the strava geojson file
#os.system("cat strava.geojson | /users/ajmcvitt/node_modules/.bin/simplify-geojson > strava_simple.geojson")

#data = json.load(open('strava_simple.geojson'))
#with open('strava_simple2.geojson', 'w') as fp:
#        json.dump(data, fp)



# Put this json file into another one with a variable declaration
f = open('strava.geojson', 'r').read()
g = open('/users/ajmcvitt/www/blog/currently_ridden.geojson', 'w')
g.write('var ridden = ')
g.write(f)
g.write(";")
g.close()


