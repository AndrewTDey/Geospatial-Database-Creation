
#######################################################################################################
##########   Program Name: Subset SNAP Benefit Retailer Locations by State   ################
###Project Name: GeoDatabase Creation
##Purpose: 
    #Part 1: Loop code that selects a subset of the US SNAP Benefit Retailers 
    #shapefile by State, and exports that subset as a shapefile with the CRS NAD 1983
#   **
# 
##Programmer: Andy Dey
##Date Program Created: 1/25/24 
##Notes:

##Datasets Used:
    #The dataset with all SNAP retailer locations for the entire US
##Datasets Created:
    #the shapefiles with names

##Date Last Updated: 1/26/24

######################################################################################################


from os import listdir
import pandas as pd
import geopandas as gpd
import pyproj
import fiona
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdalconst
import numpy as np

basepath = 'filepath'

###Step 1: Import the csv as a Geopandas dataset
##Step 1.a. Importing the dataset as a csv
US_SNAPcsv = pd.read_csv('{basepath}/Historical SNAP Retailer Locator Data.csv')

##testing that the dataset worked:
US_SNAPcsv.head()
for col in US_SNAPcsv.columns:
    print(col)

##Looking at the Lat and Lon columns:
US_SNAPcsv.loc[:,['Latitude', 'Longitude']].head()


##Step 1.b. Converting the Pandas dataset to a Geopanda
#Tutorial Source: geopandas.org/en/stable/gallery/create_geopandas_from_pandas.html
US_SNAP = gpd.GeoDataFrame(US_SNAPcsv, geometry=gpd.points_from_xy(US_SNAPcsv.Longitude, US_SNAPcsv.Latitude), crs="EPSG:4269")    

#making sure it worked:
US_SNAP.plot()
US_SNAP.crs #AD 1/21/24: It is correct
US_SNAP.geometry


###Restricting that dataset to within the US
#Importing the US bounds dataset
USBounds = gpd.read_file('{basepath}/US_Boundary_Shapefile.shp')
USBounds.plot()
USBounds.crs #WGS84
USBounds = USBounds.to_crs("EPSG:4269")

##Clipping the US SNAP dataset to within the US bounds
US_SNAP_Clipped  = gpd.clip(US_SNAP, USBounds)

US_SNAP_Clipped.plot()


##Looking at the rows that did not make it into US_SNAP_Clipped
#How many have Lat=0?
missing = US_SNAPcsv.loc[US_SNAPcsv['Latitude']==0]#334708

notin = NIC.loc[((NIC['Latitude']!=0) & (NIC['Exists']!='both'))]

Notinclipped = US_SNAPcsv[ ~US_SNAP_Clp_DF.index.isin(US_SNAPcsv.index)]


###List of states and abbrevaitions used in the loop
statenames = ["Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maine", "Michigan", "Minnesota", "Missouri", "Montana", "Mississippi", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
stateabbvs = ["AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "ME", "MI", "MN", "MO", "MT", "MS", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA","RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]


##Step 2: Testing the subset code:
CASubset = US_SNAP[US_SNAP["State"] == 'CA']
CASubset.plot()

##AD 1/26/24: some points were way outside the state boundaries, so I decided to restrict the state subset to what is within the bounds of the state
CABounds = gpd.read_file('{basepath}/CA_bounds.shp')
CABounds.plot()

#I found the clip function at www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-processing/clip-vector-data-in-python-shapely/
CA_Clipped = gpd.clip(CASubset,CABounds)
CA_Clipped.plot()


##Checking how many times the loop will run
len(statenames)#49


###Step 3: The loop code


i=0
while i < len(statenames):
    ###Creating the Geographic File
    
    statename = statenames[i]
    stateabbv = stateabbvs[i]
    
 
    #Subsetting the US file with the hospitals in that state
    StateSubset = US_SNAP_Clipped[US_SNAP_Clipped["State"] == f'{stateabbv}']
    
    #Testing showed some points were way outside the state boundaries, so I decided to restrict the state subset to what is within the bounds of the state
    StateBounds =  gpd.read_file(f'{basepath}/{stateabbv}_StateGIS.shp')
    StateBounds = StateBounds.to_crs("EPSG:4269")
    StateClip = gpd.clip(StateSubset, StateBounds)#this will restrict all points to be within the boundaries of that state
    
    ##Ensuring the CRS is NAD 1983    
    StateClip = StateSubset.to_crs("EPSG:4269")

    ##Outputting the Geographic file
    StateClip.to_file(f'{base_path}/{statename}/{stateabbv}_SNAPRtlr.shp')

   
    i += 1
    

