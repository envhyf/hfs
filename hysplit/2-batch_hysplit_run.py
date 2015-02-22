# Script automates hysplit daily trajectory computations up to 8 weeks backwards.
# Trajectory model runs by executing binary "hyts_std.exe". Before execution,
# additional configuration files have to be prepared in the current working
# directory.
#
# Global configurations are stored in SETUP.CFG. ASCDATA.CFG holds default
# constant values for land use and roughness length. CONFIG file specifies
# the run and especially paths to to meteo GDAS files.
#
# Runs are defined in the file "runs.csv" in a comma-separated values format.
# Values are in the following order:
# OUTPUT FOLDER, LATITUDE, LONGTITUDE, HEIGHT, YEAR, MONTH, DAY, BACKWARD TIME IN HOURS
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-10-19

"""Modules"""
import csv
import os
import sys
import subprocess
from subprocess import Popen, PIPE
from datetime import date, timedelta
from timeit import time
from sets import Set
import calendar
import math


"""Constants"""
# Cross-platform clear screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

cls()

# User input and displayed script description
description = """\nbatch_hysplit_run.py

Batch hysplit execution. Runs are defined in csv file.
"""

print(description)

# Test if hysplit binary exists
hysplit_bin = 'C:\\hysplit4\\exec\\hyts_std.exe'

if not os.path.isfile(hysplit_bin): 
    print("Couldn't find hyts_std.exe. Please, check the hysplit installation or set\
      properly the script variable 'hysplit_bin'.")
    sys.exit()

print "Enter:"
meteo_dir = raw_input("Meteo directory (e.g. C:\\meteo): ")
output_dir = raw_input("Output directory (e.g. C:\\out): ")
csv_source = raw_input("Location of the csv file containing run specifications (e.g. C:\\runs.csv): ")

# Execution start time stamp
startTime = time.time()
# Load runs from csv file
csv_input = csv.reader(open(csv_source, 'r'))

# ASCDATA.CFG
ASCDATA = """-90.0   -180.0  lat/lon of lower left corner
1.0     1.0     lat/lon spacing in degrees
180     360     lat/lon number of data points
2               default land use category
0.2             default roughness length (m)
'C:/hysplit4/bdyfiles/'  directory of files
"""

# SETUP.CFG
SETUP = """&SETUP\ntratio = 0.75,\nmgmin = 15,\nkhmax = 9999,\nkmixd = 0,
kmsl = 0,\nnstr = 0,\nmhrs = 9999,\nnver = 0,\ntout = 60,\ntm_tpot = 0,
tm_tamb = 0,\ntm_rain = 1,\ntm_mixd = 1,\ntm_relh = 0,\ntm_sphu = 0,
tm_mixr = 0,\ntm_dswf = 0,\ntm_terr = 0,\ndxf = 1.0,\ndyf = 1.0,
dzf = 0.01,\n/
"""


"""Additional functions"""

# Calculate the week number of month
def week_of_month(current_date):
    return (current_date.day-1) / 7 + 1

# Create ASCDATA.CFG
def createASCDATA():
    ascdataFile = open('ASCDATA.CFG', 'w')
    ascdataFile.write(ASCDATA)
    ascdataFile.close()

# Create SETUP.CFG
def createSETUP():
    setupFile = open('SETUP.CFG', 'w')
    setupFile.write(SETUP)
    setupFile.close()


"""Main"""
# Main loop. Cycling through the lines in csv file and for each
# day within period runs model in specified hours.

# Omit the first line in csv
csv_input.next()

print "\n * starting batch run \n"

for line in csv_input:

    # Load values
    working_dir = line[0]
    lat = line[1]
    lon = line[2]
    height = line[3]
    start_date = date(int(line[4]), int(line[5]), int(line[6]))
    end_date = date(int(line[7]), int(line[8]), int(line[9]))
    runtime = int(line[10])
    runtime_weeks = math.ceil(runtime/(24.0*7))
    hours = line[11].split()
    top_model = "15000" # Constant, should be at least 1000
    
    # Make dir for current run
    if not os.path.exists(output_dir + "\\" + working_dir):
        os.makedirs(output_dir + "\\" + working_dir)

    os.chdir(output_dir + "\\" + working_dir)

    print("\t * running " + working_dir)

    # Create log file
    log = open('RUN.LOG', 'w')

    # ASCDATA.CFG
    createASCDATA()

    # SETUP.CFG
    createSETUP()

    while start_date <= end_date:
        for hour in hours:

            # Create control file, based on hysplit manual
            control = open('CONTROL', 'w')
            control.write(start_date.strftime('%y %m %d ') + hour + '\n')
            control.write('1\n')
            control.write(lat + ' ' + lon + ' ' + height + '\n')
            control.write(str(runtime) + '\n')
            control.write('0\n') # vertical motion
            control.write(top_model + '\n')

            # Add sufficient number of meteo files
            if runtime_weeks > 0:
                meteo_date_end = start_date + timedelta(weeks=runtime_weeks)
                meteo_date_start = start_date
            else:
                meteo_date_start = start_date - timedelta(weeks=abs(runtime_weeks))
                meteo_date_end = start_date

            # Set of all meteo files is created
            meteo_files = Set()

            while meteo_date_start <= meteo_date_end:

                meteo_files.add('gdas1.' + meteo_date_start.strftime('%b%y').lower() \
                    + '.w' + str(week_of_month(meteo_date_start)))
                meteo_date_start = meteo_date_start + timedelta(days=1)

            control.write(str(len(meteo_files)) + '\n')
		
            for meteo_file in meteo_files:
                if not os.path.isfile(meteo_dir + "\\" + meteo_file):
                   print "Missing " + meteo_dir + "\\" + meteo_file
                   raw_input()
                   break
                control.write(meteo_dir + '\\\n')
                control.write(meteo_file + '\n')

            # Output location
            control.write(output_dir + "\\" + working_dir + '\\\n')
            control.write(start_date.strftime('%y%m%d') + hour)
            control.close()

            # Run model and log it's output
            run = Popen(hysplit_bin, stdout=PIPE, stderr=PIPE)
            run_out = run.communicate()
            log.write(run_out[0])
            log.write(run_out[1])

        start_date += timedelta(days=1)
    os.chdir('../')
    log.close()

print "\n * DONE. Script time execution was:\n%d seconds or %d minutes" % (time.time() \
    - startTime, (time.time() - startTime)/60)
print "Please, press Enter to terminate the script."
raw_input()
