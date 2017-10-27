#-------------------------------------------------------------------------------
# Name:        classifyAspect.py
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
    #Class aspect
    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)

    # Set overwrite option
    env.overwriteOutput = True

     #Set message about running
    arcpy.AddMessage("Classifying Aspect ......")

    offset=22.5
    tmp1=Aspect(r)
    remap = RemapRange([[0,offset,64],[offset,45+offset,128],[45+offset,90+offset,1],[90+offset,135+offset,2],[135+offset,180+offset,4], \
                        [180+offset,225+offset,8],[225+offset,270+offset,16],[270+offset,315+offset,32],[315+offset,360,64]])
    outRaster = Reclassify(tmp1,"Value",remap,"NODATA")


    outRasterName = arcpy.GetParameterAsText(1)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Aspect Classification Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

