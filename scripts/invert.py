#-------------------------------------------------------------------------------
# Name:        Invert
# Purpose:
#
# Authors:      Jeff Evans and Jim Oakleaf
#
# Created:     09/09/2014
# Copyright:   (c) Evans and Oakleaf 2014
# Licence:     Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#-------------------------------------------------------------------------------



import arcpy
from arcpy import env
from arcpy.sa import *
import os
import geomorph_routines_module

class LicenseError(Exception):
    pass


try:
	#Check for spatial analyst license
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        raise LicenseError

    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)
    dscR = arcpy.Describe(r)

    if dscR.isInteger:
        type = "INTEGER"
    else:
        type ="FLOAT"

    # Set overwrite option
    env.overwriteOutput = True

     #Set message about running
    arcpy.AddMessage("Running Invert ......")
    try:
        maxVal = arcpy.GetRasterProperties_management(r,"MAXIMUM")
    except arcpy.ExecuteError:
        arcpy.CalculateStatistics_management(r)
        maxVal = arcpy.GetRasterProperties_management(r,"MAXIMUM")


    maxRaster = CreateConstantRaster(maxVal,type,dscR.MeanCellHeight,dscR.extent)

    minVal = arcpy.GetRasterProperties_management(r,"MINIMUM")
    minRaster = CreateConstantRaster(minVal,type,dscR.MeanCellHeight,dscR.extent)


    outRaster = Plus(Times(Minus(r,maxRaster),-1),minRaster)






    outRasterName = arcpy.GetParameterAsText(1)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Invert Completed")







except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


