#-------------------------------------------------------------------------------
# Name:        Roughness.py
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
    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)

    # Set overwrite option
    env.overwriteOutput = True


    analysisWindow = arcpy.GetParameterAsText(1)

     #Set message about running
    arcpy.AddMessage("Running Roughness ......")
    tmp1 = FocalStatistics(r,analysisWindow,"STD")

    outRaster = Square(tmp1)



    outRasterName = arcpy.GetParameterAsText(2)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Roughness Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

