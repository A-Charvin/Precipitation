"""
This script performs spatial interpolation on precipitation data using the Inverse Distance Weighting (IDW) method.

The script follows these steps:
1. Sets up the environment and checks out the Spatial Analyst extension.
2. Retrieves unique dates from the 'Date' field of the input point features.
3. Sets the extent to the clip boundary.
4. Loops over each unique date and performs the following steps for each date:
    a. Creates a feature layer for the current date.
    b. Executes IDW on the feature layer to interpolate the precipitation data.
    c. Clips the output of the IDW to the specified boundary.
    d. Deletes the temporary feature layer.
5. Prints the end time after all dates have been processed.

The input point features should have a 'Date' field and a field for the values to be interpolated (specified by 'zField'). 
The output is a set of rasters named "IDW" followed by the date, clipped to the specified boundary.

Note: This script requires the ArcGIS Spatial Analyst extension.
"""

import arcpy
from arcpy import env
from arcpy.sa import *
import time

currentTime = time.asctime(time.localtime())        
print('Start Time: ' + str(currentTime))

# Set environment settings
env.workspace = r"C:\Users\an\Documents\ArcGIS\Projects\Climate\Climate.gdb" # Change to your environment
arcpy.env.overwriteOutput = True

# Set local variables
inPointFeatures = "XYPrecipitation" # Change to your Point data input layer.
zField = "Value"
power = 3
clipBoundary = "KRCAB" # Boundary File

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
print("Spatial Analyst extension checked out.")

# Get dates from the 'Date' field
dates = sorted({row[0] for row in arcpy.da.SearchCursor(inPointFeatures, 'Date')})
print("Dates retrieved.")

# Set the extent to the clip boundary
arcpy.env.extent = arcpy.Describe(clipBoundary).extent
print("Feature dataset created.")

# Loop over each unique date
for date in dates:
    # Create a feature layer for each date
    arcpy.MakeFeatureLayer_management(inPointFeatures, "temp_layer", where_clause="Date = DATE '{}'".format(date))
    print("Processing date: {}".format(date))
    print("Feature layer created.")

    # Execute IDW on the feature layer
    outIDW = Idw("temp_layer", zField, power)
    print("IDW interpolation completed.")
    
    # Clip the output to the boundary using arcpy.management.Clip
    out_raster = "IDW{}".format(date.strftime('%m%d'))
    arcpy.management.Clip(outIDW, "#", out_raster, clipBoundary, "#", "NONE", "NO_MAINTAIN_EXTENT") # Clipping does not seems to be working. Modify it as needed. May be using Mask Raster or something else.
    # print("Output clipped to boundary.")
    
    # Delete the temporary layer
    arcpy.Delete_management("temp_layer")
    print("Temporary layer deleted.")

print('End Time: ' + str(currentTime))
