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

# Location containing directories with tdump files
working_dir = 'F:\\out\\'
os.chdir(working_dir)

for run in os.walk('.').next()[1]:
    os.chdir(run + "\\shapes")

    merged_shapes = shapefile.Writer()
    shape_files = glob.glob("*.shp")

    # Print info about current run
    print run

    for shape_file in shape_files:
        reader = shapefile.Reader(shape_file)
        merged_shapes._shapes.extend(reader.shapes())
        merged_shapes.records.extend(reader.records())

    merged_shapes.fields = list(reader.fields)
    merged_shapes.save('%s.shp"'% run)

    os.chdir("../../")

raw_input()
