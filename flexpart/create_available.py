import glob
import os
import sys
from datetime import date

meteo_dir = raw_input("Enter the location of the directory containing meteo files (e.g. /mnt/meteo): ")

# test if dir exists
if os.path.isdir(meteo_dir):
  os.chdir(meteo_dir)
else:
  print("\nDirectory does not exist.")
  sys.exit()

meteo_files = glob.glob('EN*')
# check if any meteo files in dir
if not meteo_files:
  print("\nDirectory does not contains meteo files.")
  sys.exit()

AVAILABLE = open('AVAILABLE', 'w')
AVAILABLE.write("-\n-\n-\n")

for meteo_file in meteo_files:
	# line format to 20130802 000000      EN13080200
	AVAILABLE.write("20%s %s0000      %s\n" % (meteo_file[2:], meteo_file[8:10], meteo_file))

AVAILABLE.close()

print("\nAVAILABLE file created in %s.\nPress Enter to close the console." % meteo_dir)
raw_input()
