## Batch processing for HYSPLIT

![](http://i.imgur.com/CxtdTj7.png "Flow of batch processing")

HYSPLIT GUI does not feature batch model execution for defined runs. Following scripts allow to do so by simply define multiple runs as a comma-separated values (CSV) in this format:

| run name | lat | lon | height | start year | start month | start day | end year | end month | end day | run time | release hours |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|

Sample [file](https://github.com/dudko/hfs/blob/master/hysplit/sample_run.csv) with header, which is necessary to have as a first line of the CSV file, is provided. File can be prepared and further updated by major spreadsheet editors like MS Excel or OpenOffice/LibreOffice Calc. 

Current versions of HYSPLIT runs only on windows-like machines.

### Requirements

* >= Python 2.7
* for model execution latest version of HYSPLIT
* spatial analysis are requires >= ArcMap v.10

### Additional informations to individual scripts
#### Downloading meteorological data - gdas_downloader.py 

* download gdas1 files in batch based on entered time period
* gdas1 files are downloaded from ftp://arlftp.arlhq.noaa.gov/pub/archives/gdas1. They are stored in 7-day archives with size about 600 MB.  
* Hysplit allows run with maximum 12 meteorological files. That gives us rough maximum execution period of 84 days. This limit can be extended by concatenating meteo. Concatenation and it's performance was not tested and it's not implemeted in further scripts.
* Example of concatenation process using cat.

> cat metfile1 &gt; metfile.all; cat metfile2 &gt;&gt; metfile.all; cat metfile3 &gt;&gt; metfile.all;

#### Hysplit execution - run\_daily\_traj.py

* model execution is done with "hysplit4\exec\hyts_std.exe"
* output of the execution is a tdump file
* every run requires 3 configuration files
	1. **ASCDATA.CFG** defines the grid system and gives an optional directory location for the landuse and roughness length files
	2. **SETUP.CFG** defines trajectory or concentration configurations
	3. **CONTROL** configurations related to the model execution
	  * starting time
	  * release location
	  * total run time in hours| negative/posite number defines the direction of the run
	  * vertical limit of the internal meteorological grid
	  * list of meteo grids
	  * output directory where tdpum files are stored