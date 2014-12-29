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

# Location containing directories with tdump files
working_dir = 'F:\\test\\'
os.chdir(working_dir)

for run in os.walk('.').next()[1]:

    # Print info about current run
    print run
    os.chdir(run)

    # Filter tdump files
    files = glob.glob("./0*")
    files.extend(glob.glob("./1*"))

    files_content = []
    gdas_set = set()
    first_lines = []

    for entry in files:

        hSource = open(entry, "r").readlines()
        gdas_number = int(hSource[0].split()[0])
        offset = gdas_number + 4

        if not first_lines:
            first_lines = hSource[:offset]
        
        files_content.append(hSource[offset:])

        for gdas in hSource[1:(gdas_number+1)]:
            gdas_set.add(gdas)

    mixed_tdump = open('mixed_tdump', 'w')
    mixed_tdump.write(" " + str(len(gdas_set)) + " " + str(len(files_content)) + "\n")

    for gdas in gdas_set:
        mixed_tdump.write(gdas[4:])

    if any("BACKWARD" in s for s in first_lines):
        mixed_tdump.write(" %s BACKWARD OMEGA\n" % str(len(files_content)))
    else:
        mixed_tdump.write(" %s FORWARD OMEGA\n" % str(len(files_content)))

    for entry in files_content:
        first_line = entry[0].split()
        mixed_tdump.write("%s %s\n" % (' '.join(first_line[2:6]), ' '.join(first_line[9:12])))

    mixed_tdump.write(first_lines[-1])

    files_number = len(files_content)
    
    while files_content[0][0]:
        for i in xrange(1, files_number+1):         
            mixed_tdump.write("%s %s\n" % (i, " ".join(files_content[i-1][0].split()[1:])))
            files_content[i-1].pop(0)

    mixed_tdump.close()
    pdb.set_trace()
raw_input()
