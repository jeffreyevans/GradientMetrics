#-------------------------------------------------------------------------------
# Name:        noDataFill.py
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
    dscRaster = arcpy.Describe(r)
    ext = dscRaster.extent


    # Set overwrite option
    env.overwriteOutput = True


    analysisWindow = arcpy.GetParameterAsText(2)


     #Set message about running
    arcpy.AddMessage("Running No Data Fill ......")
    analysisType = arcpy.GetParameterAsText(1)

    if analysisType == "Mean":
        outRaster = Con(IsNull(r),FocalStatistics(r,analysisWindow,"MEAN"), r)
    elif analysisType == "Median":
        outRaster = Con(IsNull(r),FocalStatistics(r,analysisWindow,"MEDIAN"), r)
    else:
        #Has to be Majority
        outRaster = Con(IsNull(r),FocalStatistics(r,analysisWindow,"MAJORITY"), r)


    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("No Data Fill Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

