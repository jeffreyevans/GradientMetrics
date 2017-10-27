#-------------------------------------------------------------------------------
# Name:        meanSlope.py
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
    inZUnits = arcpy.GetParameterAsText(1)
    zFactor = geomorph_routines_module.getZFactor(r,inZUnits)
    # Set overwrite option
    env.overwriteOutput = True

    analysisWindow = arcpy.GetParameterAsText(2)


     #Set message about running
    arcpy.AddMessage("Running Mean Slope ......")
    tmp1 = Slope(r,"DEGREE",zFactor)



    outRaster = FocalStatistics(tmp1,analysisWindow,"MEAN")


    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Mean Slope Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

