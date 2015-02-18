# Merge all shapefiles inside of directories in the current working
# directory. Output is stored inside of "shapes" directory.
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-10-19
 
import glob
import os
import sys
import pdb
sys.path.append('./lib')
import shapefile

description = """\n4-merge_shp.py

This script merges all the shapefiles for each directory.

User is required to enter the location of directory containing directories with converted shape files.
"""

print(description)
working_dir = raw_input("Enter the location of directory containing directories with converted shape files : ")

# Create output dir if not exists
if not os.path.exists(working_dir):
    print("Entered directory is invalid.")
    sys.exit()

os.chdir(working_dir)

print "\n * starting to merge shape files\n"

for run in os.walk('.').next()[1]:
    os.chdir(run + "\\shapes")

    merged_shapes = shapefile.Writer()
    shape_files = glob.glob("*.shp")


    for shape_file in shape_files:
        reader = shapefile.Reader(shape_file)
        merged_shapes._shapes.extend(reader.shapes())
        merged_shapes.records.extend(reader.records())

    merged_shapes.fields = list(reader.fields)
    merged_shapes.save('%s.shp"'% run)

     # feedback
    print " * %s DONE" % run
    print "  %s\\%s.shp" % (os.getcwd(), run)

    os.chdir("../../")

print("\n * DONE. Please, press Enter to terminate the script.")
raw_input()