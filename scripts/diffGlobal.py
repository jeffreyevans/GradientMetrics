#-------------------------------------------------------------------------------
# Name:        Difference from Global
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
    #Modeling polygon --- roadless
    r = arcpy.GetParameterAsText(0)
    inRaster = geomorph_routines_module.checkExt(r)


    # Set overwrite option
    env.overwriteOutput = True

    analysisWindow = arcpy.GetParameterAsText(2)


     #Set message about running
    arcpy.AddMessage("Running Local Deviation Analysis ......")
    analysisType = arcpy.GetParameterAsText(1)
    zoneRaster = Int(Divide(inRaster,inRaster))

    if analysisType == "Mean":
        globalRas = ZonalStatistics(zoneRaster,"value",inRaster,"MEAN")
        fcMean = FocalStatistics(inRaster,analysisWindow,"MEAN")
        outRaster = Minus(globalRas,fcMean)

    elif analysisType == "Median":

        globalRas = ZonalStatistics(zoneRaster,"value",inRaster,"MEDIAN")
        fcMed = FocalStatistics(inRaster,analysisWindow,"MEDIAN")
        outRaster = Minus(globalRas,fcMed)






    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Local Deviation Analysis Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


