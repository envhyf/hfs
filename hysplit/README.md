# Meteorological data

* gdas1 files are downloaded from ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1. They are stored in 7-day archives with size about 600 MB.  
* Hysplit allows run with maximum 12 meteorological files. That gives us rough maximum execution period of 84 days. This limit can be extended by concatenating meteo. Concatenation and it's performance was not tested and it's not implemeted in further scripts.
* Example of concatenation process using cat.

> cat metfile1 > metfile.all
> cat metfile2 >> metfile.all
> cat metfile3 >> metfile.all

## gdas_downloader.py

* TODO

# run
  * what does run need?t