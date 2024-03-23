
##########   Program Name:  Listing Existing Geodatabase FileTypes by State  ################
###Project Name: Geodatabase Creation
##Purpose: To create a dataset that has a column for a state, and an indicator var for whether the state
#            has a file for each Geodatabase file type. This is a QC check for the Geodatabase Creation,
#            making sure all files exist that should
# 
##Programmer: Andy Dey
##Date Program Created:2/2/2024
##Notes:

##Datasets Used:
##Datasets Created:
##Date Last Updated: 2/2/24

#################################################################################



import pandas as pd
import csv
import os
import glob

filetypenames = ['StateName','SNAPRtlr_Projected.shp', '2011_DailyPM25.csv', '2012_DailyPM25.csv', '2013_DailyPM25.csv',  'Elevation.tif']

len(filetypenames)#6

statenames = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland and Washington, D.C.", "Maine", "Michigan", "Minnesota", "Missouri", "Montana", "Mississippi", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
stateabbvs = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD_DC", "ME", "MI", "MN", "MO", "MT", "MS", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "PR","RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]


basepath = 'filepath'


##Creating the initial pandas dataset
GeoFileStateus = pd.DataFrame(statenames,columns=['StateName'] )

##Adding in the additional columns, at first with NaN values
GeoFileStateus = GeoFileStateus.reindex(columns = filetypenames)
GeoFileStateus['StateAbbv'] = stateabbvs



#Loop Code
i=0
while i < len(GeoFileStateus['StateName']):
    statename = GeoFileStateus['StateName'][i]
    stateabbv = GeoFileStateus['StateAbbv'][i]
    
    for filetype in filetypenames:
      for file in glob.glob(f'{basepath}/{statename}/**/{stateabbv}_{filetype}',recursive=True):      
         if os.path.isfile(file):
            GeoFileStateus.loc[GeoFileStateus['StateName'] == statename,filetype] = 'Yes'
         if not os.path.isfile(file):
            GeoFileStateus.loc[GeoFileStateus['StateName'] == statename,filetype] = 'No' 
    i+=1          


GeoFileStateus.head()

##Exporting as csv to view it
GeoFileStateus.to_csv(f'{basepath}/Geofile_status_datecreated.csv')

GeoFileStateus[['State_Name','State_Geo']] 


###Checking which values are null
print(GeoFileStateus.loc[ : , [(GeoFileStateus[col] =='NA').any() for col in GeoFileStateus.columns]])

print(GeoFileStateus[GeoFileStateus.isnull().any(axis=1)])

GeoFileStateus.isna()




































