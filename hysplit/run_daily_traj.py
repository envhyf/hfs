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
# Values are in the folowing order:
# OUTPUT FOLDER, LATITUDE, LONGTITUDE, HEIGHT, YEAR, MONTH, DAY, BACKWARD TIME IN HOURS
#
# Dušan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-10-19

"""Modules"""
import csv
import os
import subprocess
from datetime import date, timedelta
from timeit import time
from time import sleep
import pdb
import calendar

"""Constants"""
HYSPLIT_BIN = 'C:\\hysplit4\\exec\\hyts_std.exe'

months = [
    'jan', 'feb', 'mar', 'apr',
    'may', 'jun', 'jul', 'aug',
    'sep', 'oct', 'nov', 'dec'
]
# Default folder with meteo data. 
meteoDir = 'E:/meteo/'

RUNS.CSV = 'runs.csv'

# Start of calculations
print "Press Enter to start calculations"
raw_input()

# Execution start time stamp.
startTime = time.time()

# Source file for station coordinates and time ranges stored in CSV reader.
source = open(RUNS.CSV, 'r')
reader = csv.reader(source)

# ASCDATA.CFG
ASCDATA = """-90.0   -180.0  lat/lon of lower left corner
1.0     1.0     lat/lon spacing in degrees
180     360     lat/lon number of data points
2               default land use category
0.2             default roughness length (m)
'C:/hysplit4/bdyfiles/'  directory of files
"""

# SETUP.CFG
SETUP = """&SETUP\ntratio = 0.75,\nmgmin = 15,\nkhmax = 9999,\nkmixd = 0,\nkmsl = 0,
nstr = 0,\nmhrs = 9999,\nnver = 0,\ntout = 60,\ntm_tpot = 0,\ntm_tamb = 0,
tm_rain = 1,\ntm_mixd = 1,\ntm_relh = 0,\ntm_sphu = 0,\ntm_mixr = 0,
tm_dswf = 0,\ntm_terr = 0,\ndxf = 1.0,\ndyf = 1.0,\ndzf = 0.01,\n/
"""

# Create ASCDATA.CFG and SETUP.CFG
def createSetupAscdata():
    ascdataFile = open('ASCDATA.CFG', 'w')
    ascdataFile.write(ASCDATA)
    ascdataFile.close()

    setupFile = open('SETUP.CFG', 'w')
    setupFile.write(SETUP)
    setupFile.close()

# Return previous month from months list.
def monthBack(i):
    if i == 1:
        return months[11]
    else:
        return months[i-2]

# Create CONTROL file. Input is time and 
def createControl(currentTime, currentDate):
    control = open('CONTROL', 'w')

    if (calendar.monthrange(currentDate.year, 2)[1] == 28 and currentDate.month == 2):
        control.write(currentDate.strftime('%y' + ' ' + '%m' + ' ' + '%d') \
            + ' ' + currentTime + '\n1\n%s %s %s\n-240\n0\n10000.0\n7\n' \
            % (line[1], line[2], line[3]))
        for week in range(1,5):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 1], currentDate.strftime('%y'), week))
        for week in range(3,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 2], currentDate.strftime('%y'), week))
    elif (calendar.monthrange(currentDate.year, 2)[1] == 28 and currentDate.month == 3):
        control.write(currentDate.strftime('%y' + ' ' + '%m' + ' ' + '%d') \
            + ' ' + currentTime + '\n1\n%s %s %s\n-240\n0\n10000.0\n7\n' \
            % (line[1], line[2], line[3]))
        for week in range(1,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 1], currentDate.strftime('%y'), week))
        for week in range(3,5):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 2], currentDate.strftime('%y'), week))
    elif currentDate.month == 1:
        control.write(currentDate.strftime('%y' + ' ' + '%m' + ' ' + '%d') \
            + ' ' + currentTime + '\n1\n%s %s %s\n-240\n0\n10000.0\n8\n' \
            % (line[1], line[2], line[3]))
        for week in range(1,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 1], currentDate.strftime('%y'), week))
        # one year back
        currentYear = int(currentDate.strftime('%y')) - 1
        for week in range(3,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 2], currentYear, week))
    else:
        control.write(currentDate.strftime('%y' + ' ' + '%m' + ' ' + '%d') \
            + ' ' + currentTime + '\n1\n%s %s %s\n-240\n0\n10000.0\n8\n' \
            % (line[1], line[2], line[3]))
        for week in range(1,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 1], currentDate.strftime('%y'), week))
        for week in range(3,6):
            control.write('%s\ngdas1.%s%s.w%d\n' % \
                (meteoDir, months[currentDate.month - 2], currentDate.strftime('%y'), week))

    control.write(os.getcwd().replace('\\','/') + '/\n' + currentDate.strftime('%y%m%d') + \
        currentTime)
    control.close()
    
# Remove created configuration files.
def removeSetupAscdata():
        if os.path.exists("ASCDATA.CFG"):
            os.remove("ASCDATA.CFG")
        if os.path.exists("SETUP.CFG"):
            os.remove("SETUP.CFG")

# Main loop. Cycling throught the lines in csv file and for each
# day within period runs model in specified times.
for line in reader:

    workingPath = "%s/%s" & (line[0], line[1])

    print line[1]

    # Make dir for current period.
    if not os.path.exists(workingPath):
        os.mkdir(workingPath)

    os.chdir(workingPath)

    createSetupAscdata()

    startDate = date(int(line[4]), int(line[5]), int(line[6]))
    endDate = date(int(line[7]), int(line[8]), int(line[9]))

    while startDate <= endDate:
        for currentTime in {'06', '18'}:
            createControl(currentTime, startDate)
            
            os.system(HYSPLIT_BIN)

            # Remove CONTROL.
            #os.remove('CONTROL')
            raw_input()
        startDate += timedelta(days=1)
    os.chdir('../../')
    

print "Script time execution was:\n%d seconds or %d minutes" % (time.time() - startTime, (time.time() - startTime)/60)
raw_input()
