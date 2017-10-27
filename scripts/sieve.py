#-------------------------------------------------------------------------------
# Name:        sieve.py
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
    minCells = arcpy.GetParameterAsText(1)

    env.overwriteOutput = True


    arcpy.AddMessage("Running Sieve ......")

    tmp1 = RegionGroup(r,"EIGHT","WITHIN","ADD_LINK","")
    query = "COUNT >= " + minCells
    tmp2 = ExtractByAttributes(tmp1,query)
    tmp3 = SetNull(tmp2 == 0, tmp2)
    outRaster = Nibble(r,tmp3)

    outRasterName = arcpy.GetParameterAsText(2)
    outRaster.save (outRasterName)

    arcpy.AddMessage("Sieve Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


