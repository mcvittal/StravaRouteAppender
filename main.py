#!/usr/bin/env python3

## This program's main functionality is to auto fetch the newest Strava routes from your profile and append them to a GeoJSON file.
## Licensed under the GNU GPL v3.0.
## Written December 2016 by Alex McVittie
##
## Requires the Strava python API libraries and the Python port of ogr2ogr.
## Note - this software is in beta and may not work for your specific usecase. It is not written or intended for widespread use.


# Fetch API keys from external Python file. Not synced with Github repo
from api_keys import *

import ogr2ogr

from stravalib.client import Client

def main():
    pass

## update_geojson: String String --> None
## Purpose:
##      Takes in the path to an input GPX track file and appends the GPX track data to a target geoJSON file
def update_geojson(in_gpx, target_geojson):
    # Convert GPX to a temporary geojson file - will be appended in second step to target geojson
    ogr2ogr.main(["", "-f", "geoJSON", in_gpx,"tracks",   "tmp.geoJSON", "-fieldTypeToString", "DateTime"])


