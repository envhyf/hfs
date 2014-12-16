import glob
import os
from datetime import date

os.chdir('.')

meteo_files = glob.glob('EN*')

AVAILABLE = open('AVAILABLE', 'w')
AVAILABLE.write("-\n-\n-\n")

for meteo_file in meteo_files:
	# line format to 20130802 000000      EN13080200
	AVAILABLE.write("20%s %s0000      %s\n" % (meteo_file[2:], meteo_file[8:10], meteo_file))

AVAILABLE.close()