#!/usr/bin/env python
#
# Count how many trajectories per station entered the area around points of
# interest. Stations need to be specified in CVS file in format (station, lat,
# lon). CSV file used for batch run definition can be used as well. Points are
# define in this script a tripple (point name, lat, lon).

"""Modules"""
import math
import csv
import glob
import os
from numpy import *

"""Constants"""
# Reader csv file with station coordinates
source = open("runs.csv", "r")

# point tripples
points = [("Oki", 36.288333, 133.184722),\
          ("Tsushima", 34.233889, 129.275),\
          ("Hedo", 26.866944, 128.248611)]

# radius around point in meters
r = 50000

def distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two locations.
    dist = arccos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * \
           cos(lon1 - lon2)) * R
    R = spherical approximationa of the figure of the Earth with \
        radius R=6371 km 
    Coordinates are in radians. 
    """
        
    r = 6373

    # Convert to radians.
    degreesToRadians = math.pi/180.0
        
    lat1 = (90.0 - lat1)*degreesToRadians
    lon1 = lon1*degreesToRadians

    lat2 = (90.0 - lat2)*degreesToRadians
    lon2 = lon2*degreesToRadians

    dist = math.acos(math.sin(lat1)*math.sin(lat2)*math.cos(lon1 - lon2) \
        + math.cos(lat1)*math.cos(lat2))*r

    # Return in meters.
    return dist*1000

   
# Main loop
for point in points:
    source.seek(0, 0)
    stations = csv.reader(source)
    for station in stations:
     
        total = 0
        hit = 0

        os.chdir(station[0]+"/shapes")

        for gisFile in glob.glob("*.gis"):
            gsource = open(gisFile, "r")
            total += 1
            # omit the first line

            line = gsource.readline()

            while(True):
                line = gsource.readline().split()   
                
                if line[0] == "END":
                    break
                
                d = distance(float(point[1]), float(point[2]), float(line[1]), float(line[0]))

                if d <= r:
                    hit += 1
                    break

            gsource.close()

        print "%s %s %s %s" % (point, station[0], total, hit)
            
        os.chdir("../../")

print "Done"