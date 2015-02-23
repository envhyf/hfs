# Convert tdumps to kmls. Output is written to direcotry kmls inside of
# each folder

import os
import subprocess
import glob

description = """\n3-2-tdump2kml.py

This script converts the tdump outputs from hysplit batch run to kml files. \
It walks throught all directories and stores the kml files inside of newly \
created kml folder.

User is required to enter the location of directory containing direcotries with \
tdump outputs from batch run.
"""

print(description)
working_dir = raw_input("Enter the location of directory containing directories with tdump outputs : ")

# Test working_dir
if not os.path.exists(working_dir):
    print("Entered directory is invalid.")
    sys.exit()

print "\n * starting to convert\n"

# Main loop
for run in os.walk(working_dir).next()[1]:

    os.chdir(run)

    print "\t * converting %s" % run

    # Filter tdump files
    files = glob.glob("./0*")
    files.extend(glob.glob("./1*"))

    # Conversion
    for entry in files:
    	subprocess.Popen("C:\\hysplit4\\exec\\trajplot.exe -i%s -o%s -a3 -v1 -l1" % \
                (entry, entry), shell=True, stdout=subprocess.PIPE)

    # Move all kmls into dir kmls
    kmls = glob.glob("./*.kml")

    if not os.path.exists("kmls"):
        os.makedirs("kmls")
    
    for kml in kmls:
        os.rename(kml, "./kmls/%s" % kml)
    
    # Remove redundant ps files
    pss = glob.glob("./*.ps")
    
    for ps in pss:
        os.remove(ps)

    os.chdir("../")

print("\n * DONE. Please, press Enter to terminate the script.")
raw_input()
