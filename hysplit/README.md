## Downloading meteorological data - gdas_downloader.py 

* download gdas1 files in batch based on entered time period
* gdas1 files are downloaded from ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1. They are stored in 7-day archives with size about 600 MB.  
* Hysplit allows run with maximum 12 meteorological files. That gives us rough maximum execution period of 84 days. This limit can be extended by concatenating meteo. Concatenation and it's performance was not tested and it's not implemeted in further scripts.
* Example of concatenation process using cat.

> cat metfile1 &gt; metfile.all;

> cat metfile2 &gt;&gt; metfile.all;

> cat metfile3 &gt;&gt; metfile.all;

## Hysplit execution - run\_daily\_traj.py

* model execution is done with "hysplit4\exec\hyts_std.exe"
* output of the execution is a tdump file
* every run requires 3 configuration files
	1. **ASCDATA.CFG** defines the grid system and gives an optional directory location for the landuse and roughness length files
	2. **SETUP.CFG** defines trajectory or concentration configurations
	3. **CONTROL** configurations related to the model execution
	  * starting time
	  * release location
	  * total run time in hours, negative/posite number defines the direction of the run
	  * vertical limit of the internal meteorological grid
	  * list of meteo grids
	  * output directory where tdpum files are stored