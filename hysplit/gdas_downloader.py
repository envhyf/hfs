#!/usr/bin/env python
#
# Download GDAS data from ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1/ for
# specified period of time. Period is set in the format "MM YY" at the
# beginning of the script execution. Data is downloaded to entered directory.
#
# Dusan Lago <dusan.lago at gmail.com>
# Tested with Python 2.7.6
# 2014-11-15

"""Modules"""
from ftplib import FTP
from datetime import date
import ftplib
import os

"""Globals"""
# Could be done with datetime.strftime("%b")
months = [
    'jan', 'feb', 'mar', 'apr',
    'may', 'jun', 'jul', 'aug',
    'sep', 'oct', 'nov', 'dec'
]

ftp_address = 'arlftp.arlhq.noaa.gov'
working_dir = 'pub/archives/gdas1'

# Cross-platform clear screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

cls()

# User input and displayed script description
description = """gdas_downloader.py

This scripts downloads gdas1 data from ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1/. \
User is required to set the desired period and directory used to store downloaded files.
"""

print(description)
d1 = tuple(map(int, raw_input("Starting date (MM YEAR) : ").split(' ')))
d2 = tuple(map(int, raw_input("End date (MM YEAR) : ").split(' ')))
outdir = raw_input("Output directory (e.g. C:\\meteo_dir\\) : ")

# Create output dir if not exists
if not os.path.exists(outdir):
    os.makedirs(outdir)

# Set date objects
start_date = date(d1[1], d1[0], 1)
end_date= date(d2[1], d2[0], 1)

months_delta = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1 #
current_year = start_date.year
current_month = start_date.month - 1

# Load all months
months_all = []

for i in range(months_delta):
    months_all.append(str(months[current_month]) + str(current_year).zfill(2))
    if current_month == 11:
        current_month = 0
        current_year += 1
    else:
        current_month += 1

# Download data
print "\nStarting to download data."

ftp = FTP(ftp_address)
ftp.login ()
ftp.cwd(working_dir)

for i in months_all:
    for j in range(1, 6):
        filename = outdir + "gdas1." + i + ".w" + str(j)
        print "\t * " + filename
        output_file = open(filename, 'wb')

        try:
            ftp.retrbinary("RETR %s" % filename, output_file.write)
        except ftplib.all_errors:
            print "File \"%s\" does not exists." % filename

        output_file.close()
