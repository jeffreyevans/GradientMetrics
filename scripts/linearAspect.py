#-------------------------------------------------------------------------------
# Name:        linearAspect.py
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


     #Set message about running
    arcpy.AddMessage("Running Linear Aspect ......")

    tmp1 = Aspect(r)

    tmp2 = SetNull(tmp1 < 0,(450.0 - tmp1) / 57.296)
    tmp3 = Sin(tmp2)
    tmp4 = Cos(tmp2)
    tmp5 = FocalStatistics(tmp3, NbrRectangle(3,3,"CELL"),"SUM","DATA")
    tmp6 = FocalStatistics(tmp4, NbrRectangle(3,3,"CELL"),"SUM","DATA")

    #The *100 and 36000(360*100) / 100 allow for two decimal points since Fmod appears to be gone
    tmpMod = Mod(((450 - (ATan2(tmp5, tmp6) * 57.296)) * 100), 36000) / 100
    outRaster = Con((tmp5 == 0) & (tmp6 == 0), -1, tmpMod)

    outRasterName = arcpy.GetParameterAsText(1)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Linear Aspect Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


