##########   Program Name: Parallel Functions to extract Daily PM2.5 Values  ################
###Project Name: Geodatabase Creation
##Purpose: Creating a parallel function to extract Daily PM2.5 Values for a series of points for a given year,
#          to be called in the program "Extracting the Daily PM2.5 Estimates using the parallel function.py
#   **
# 
##Programmer: Andy Dey
##Date Program Created: 1/30/24
##Notes:

##Datasets Used: 
##Datasets Created:
##Results Locations:
##Date Last Updated: 1/31/24

###################################################################################

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
from timeit import default_timer


statenames = {'California': 'CA', 'Connecticut': 'CT', 'Delaware': 'DE', 'Massachusetts': 'MA', 'Montana': 'MT', 'Texas': 'TX', 'Rhode Island': 'RI', 'Vermont': 'VT'}
years = [2011, 2012, 2013]
estimatebasepath = 'filepath1'
finaloutputbasepath = 'pathpath2'

def create_daily_fishnets(statename):
    f = open(f'{statename} loop times.txt', mode='w')
    stateabbv = statenames[statename]
    
    fishnet = gpd.read_file(f'filepath/{stateabbv}_fishnet.shp')
    fishnet['X'] = fishnet['geometry'].x #fishnet['geometry'].map(lambda g: g.x)
    fishnet['Y'] = fishnet['geometry'].y
    first = True

    state_time = default_timer()
    f.write(f'Start: {statename}\n')
    for year in years:
        year_time = default_timer()
        f.write(f'\tStart: {year}\n')

        i = 0
        ##Create a list of the Raster files for that year
        filelist = [f for f in os.listdir(f'filepath/{year}/') if f.endswith('.tif')]

        def map_index(r):
            rowIndex, colIndex = temp_raster.index(r.x, r.y) 
            return temp_data[rowIndex, colIndex]

        ##Extract the Raster values
        for file in filelist: 
            day_time = default_timer()
            temp_raster = rio.open(f'{estimatebasepath}/{year}/{file}') 
            temp_data = temp_raster.read(1)

            if first: # have we created these columns?
                first = False
                fishnet['points'] = fishnet['geometry'].map(lambda g: temp_raster.index(g.x, g.y))
            
            fishnet[f'd{file[0:8]}'] = fishnet['points'].map(lambda p: temp_data[p[0],p[1]])

            i += 1
            if i % 30 == 0:
                fishnet2 = fishnet.copy()
                del fishnet
                fishnet = fishnet2
                del fishnet2

            f.write(f'\t\t{file[0:8]}: {default_timer() - day_time}\n')
            print(f'{stateabbv}: {file} done')
            if i == 50:
                break
        f.write(f'\t{year}: {default_timer() - year_time}\n') 

        del fishnet['geometry'], fishnet['points']

        fishnet.to_csv(f'{finaloutputbasepath}/{statename}/{stateabbv}_{year}_DailyPM25.csv', index=False)
    f.write(f'{statename}: {default_timer() - state_time}\n')
    f.close()
