#!/usr/bin/env python3

import os, sys, glob, json
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
        print(activityid)
        print(current_dataset_r[1].split(","))
        lastid = current_dataset_r[1].split(",")[activityid]
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
                        poly_points[id].append([lon, lat])
                else:
                        poly_points[id].append([lon, lat])
        with open('strava.geojson') as strava_j:
            data = json.load(strava_j)
        flags = {}
        for an_id in poly_points.keys():
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


# Put this json file into another one with a variable declaration
f = open('strava.geojson', 'r').read()
g = open('currently_ridden.geojson', 'w')
g.write('var ridden = ')
g.write(f)
g.write(";")
g.close()


