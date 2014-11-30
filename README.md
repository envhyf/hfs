## Batch processing for HYSPLIT and FLEXPART

Following scripts allow batch processing for [HYSPLIT](http://ready.arl.noaa.gov/HYSPLIT.php) and [FLEXPART](http://transport.nilu.no/flexpart). Both models operate in a slightly different way and use different meteo datasets. In general, they can be described as follows:

1. download meteo files
2. prepare configuration files for the model run
3. execute model
4. post-process, interpret and visualize the output

Repository contains dedicated scripts for each model und processing phases. Used scripting language is Python, tested with the version 2.7.6. Any following manuals a guidelines assumes that, the a Python environment is correctly set up.