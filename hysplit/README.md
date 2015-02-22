## Batch processing for HYSPLIT

HYSPLIT GUI does not allow efficient batch model execution for defined runs. Following scripts allow to do so. The workflow diagram displays the whole process steps.

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/flow.png"  alt="Flow schema"/> </p>

### Requirements

* >= Python 2.7
* for model execution latest version of HYSPLIT (current versions run only on windows-like machines)
* spatial analysis require >= ArcMap v.10

### Setup
* clone the repository or download it as an [archive](https://github.com/dudko/hfs/archive/master.zip)

### Usage

#### 0 Defining runs

Runs executed in batch are defined in CSV file. Each file must start with header line with this format:

| run name | lat | lon | height | start year | start month | start day | end year | end month | end day | run time | release hours |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|

Sample [file](https://github.com/dudko/hfs/blob/master/hysplit/sample_run.csv) can be used as a base ground. CSV files can be prepared and further updated by major spreadsheet editors.

The direction of the run goes forward with positive value for runtime hours and backwards with negative one

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/0-spread_runs.png"  alt="Defining runs in CSV file"/> </p>

#### 1 gdas\_downloader.py - download meteorological data

Execute the script either by double clicking or from Python command-line prompt.

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/1-meteo_downloader.png"  alt="Downloading meteorological data"/> </p>

#### 2 run\_daily\_traj.py - batch execution

First, make sure, that the location of the HYSPLIT binary, used for model execution, is set correctly. Default setting is in the top part of the script. Availability of this executable file is checked before every run.

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/2-batch_hysplit_run.png"  alt="Batch execution"/> </p>

#### 3 tdump2shp.py - tdump to shp conversion

Convert all the tdump files inside of run directiries produces with [2-run_daily_traj.py](https://github.com/dudko/hfs/blob/master/hysplit/2-run_daily_traj.py).

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/3-tdump2shp.png"  alt="tdump to shp conversion"/> </p>

#### 4-merge_shp.py - merge all converted shapefiles

<p align="center"> <img src="https://raw.githubusercontent.com/dudko/hfs/master/hysplit/img/4-merge_shp.png"  alt="Merge all converted shapefiles"/> </p>

#### 5-1-spatial_grid_layer.py