#######################################################################################################
##########   Program Name: Subset Elevation Raster data for Each US State   ################
###Project Name: Geodatabase Creation
##Purpose: Create subsets of the Contiguous US elevation raster dataset for each state and save as a new .tif
#   **
# 
##Programmer: Andy Dey
##Date Program Created:  12/25/24
##Notes:

##Datasets Used:
        #Contiguous US Elevation raster file
        
##Datasets Created:
        #the datasets in for each state ending in _elevation
##Results Locations:
##Date Last Updated: 12/27/24

######################################################################################################



import os 
import matplotlib.pyplot as plt
import pandas as pd
import shapely
import fiona
import numpy as np
import geopandas as gpd
import rasterio
import rioxarray as rio
import xarray



####Importing and Creating Objects used for the Loop
### Import the Raster file for the entire US  
us_elev_loc = 'Filepath/elev48i0100a.tif'
        
###this import code comes from corteva.github.io/rioxarray/stable/examples/clip_box.html under Load In Xarray Dataset
us_elevation = xarray.open_dataarray(us_elev_loc)

##Checking the Raster's CRS:
us_elevation.rio.crs 
    
statenames = ["Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland and Washington, D.C.", "Maine", "Michigan", "Minnesota", "Missouri", "Montana", "Mississippi", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
stateabbvs = ["AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD_DC", "ME", "MI", "MN", "MO", "MT", "MS", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

base_path='filepath'

##Quick QC: length of the lists 
len(statenames)#48
len(stateabbvs)#48

i=0
while i < len(statenames):
    statename = statenames[i]
    stateabbv = stateabbvs[i]
    
    ##Importing the State Boundary File: Using the projected one, because I want to add a 1km buffer and the state projected CRS is in meters
    statebound = gpd.read_file(f'{basepath}/{statename}/{stateabbv}_StateBoundsFileName.shp')
  
    
    ##Adding a 1km buffer to the state boundary shapefile
    statebound_bfrd = statebound
    statebound_bfrd['geometry'] = statebound_bfrd.geometry.buffer(1000)
    
    ##Changing the State Boundary file CRS to the Raster's CRS
    statebound_bfrd = statebound_bfrd.to_crs(us_elevation.rio.crs)  
    
    ##Cropping the Raster data to a box consisting of the min and max x and y coordinates of the state
        #this is important, or the dataset is too large to crop down to the state boundaries later
    state_clip_box = us_elevation.rio.clip_box(*statebound_bfrd.total_bounds)
    
    ##Cropping the new clip_box dataset to the state's actual boundaries
    state_clip_bounds = state_clip_box.rio.clip(statebound_bfrd['geometry'])
    
    
    ##Exporting the state boundnary file as a .tif
    state_clip_bounds.rio.to_raster(f'{base_path}/{statename}/{stateabbv}_elevation.tif')
       
            
    i += 1




