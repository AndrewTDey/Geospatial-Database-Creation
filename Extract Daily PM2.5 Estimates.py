

#######################################################################################################
##########   Program Name: Extract Daily PM2.5 Estimates   ################
###Project Name: Geodatabase Creation
##Purpose: To create datasets of Daily PM2.5 Estimates for each year for each   
#          state using the function created in the program #"Parallel+Functions+to+extract+Daily+PM2.5.py"
#   Each dataset will have: these columns: 
#   1. An ID value for that location
#   2. The latitude of the center point of the Raster pixel
#   3. The longitude of the center point of the Raster pixel
#   4. 365 raster value vars: each named for the date of the raster value, aka the US Raster datasetname; e.g. 20110101
#   
# 
##Programmer: Andy Dey
##Date Program Created: 2/1/24
##Notes:
##Datasets Used: All Daily PM2.5 raster datasets 
##Datasets Created: the Daily PM2.5 Datasets for each state
##Results Locations:
##Date Last Updated: 2/2/24

######################################################################################################

import os 
import pandas as pd
import shapely
from shapely import geometry
import fiona
import numpy as np
import geopandas as gpd
import rasterio as rio
from rasterio import plot
from rasterio.enums import Resampling
import rioxarray as rxr
import xarray
import multiprocessing as mp
import gis_lib.parallel_functions as pf


years = [2011, 2012, 2013] 

estimatebasepath = 'estimatefilepath'
finaloutputbasepath = 'outputfilepath'


##### Extracting the Raster values for each day for each state using the point shapefile for that state
if __name__ == "__main__":
    # Refactored from single process nested loops to two levels of parallelization
    # Found here, we run states in parallel. Large states will take a while, but several small states can finish while they run
    # For each daily tif, we use pandas map function rather than using iterrows
    #  - iterrows is much slower for vector operations than pandas built-in, optimized functionality
    #  - pandas is optimized for working with large data sets, especially 'do the same thing to every member of this group'
    statenames = ['California', 'Connecticut', 'Delaware', 'Massachusetts', 'Rhode Island', 'Vermont']
    pool = mp.Pool(processes=5)
    pool.map(pf.create_daily_fishnets, statenames)







