# Convert files to gis format and after that create shapefile.
# Script enters each folder in the current working directory.
# Output is stored inside of directory "shapes".
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-10-19

import os
import subprocess
import glob
import pdb

for run in os.walk('.').next()[1]:
    os.chdir(run)

    if not os.path.exists("shapes"):
        os.makedirs("shapes")

    # Filter tdump files
    files = glob.glob("./0*")
    files.extend(glob.glob("./1*"))

    for entry in files:

        hSource = open(entry, "r").readlines()
        out = open("shapes/%s.gis" % entry, "w")

        # Set the number of lines to be ommited. Based on the number of meteo files.
        offset = int(hSource[0].split()[0]) + 4
        
        if len(hSource) > offset:
            #pdb.set_trace()
            out.write("  1, %s %s\n" % (hSource[offset].split()[10], \
                hSource[offset].split()[9]))

            for line in hSource[offset:]:
                words = line.split()
                out.write("%s %s\n" % (words[10], words[9]))

            out.write("END")
            out.close()

            os.chdir("shapes")
    
            # Convert GIS file to shape file.
            subprocess.Popen("C:\\hysplit4\\exec\\ascii2shp.exe %s lines < %s.gis" % \
               (entry, entry), shell=True, stdout=subprocess.PIPE)
            os.chdir("..")

    os.chdir("..")