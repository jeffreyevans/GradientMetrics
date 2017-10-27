#-------------------------------------------------------------------------------
# Name:        Moments.py
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

    # Set overwrite option
    env.overwriteOutput = True



    analysisWindow = arcpy.GetParameterAsText(2)


     #Set message about running
    arcpy.AddMessage("Running Moments Analysis ......")
    analysisType = arcpy.GetParameterAsText(1)
    
    if analysisType == "Mean":
        outRaster = FocalStatistics(r,analysisWindow,"MEAN")
    elif analysisType == "Median":
        outRaster = FocalStatistics(r,analysisWindow,"MEDIAN")
    elif analysisType == "Mad":
        focal = FocalStatistics(r,analysisWindow,"MEDIAN")
        tmp1 = Minus(r,focal)
        outRaster = FocalStatistics(tmp1, analysisWindow, "MEDIAN")
    elif analysisType == "Variance":
        tmp1 = FocalStatistics(r,analysisWindow,"STD")
        outRaster = Square(tmp1)
    elif analysisType == "Standard Deviation":
        outRaster = FocalStatistics(r,analysisWindow,"STD")
    else:
        tmp1 = FocalStatistics(r,analysisWindow,"STD")
        tmp2 = FocalStatistics(r,analysisWindow,"MEAN")
        outRaster = Times(Divide(tmp1,tmp2 ),Float(100))





    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Moments Analysis Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


