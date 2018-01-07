#-------------------------------------------------------------------------------
# Name:        siteExposure.py
# Purpose:   Site Exposure Index
#
# Authors:      Jeff Evans and Jim Oakleaf
#
# Created:     11/17/2014
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

    # Getting info on raster
    dscRaster = arcpy.Describe(r)
    inSpRef = dscRaster.spatialReference
    spRefType = inSpRef.type
    cellSize = dscRaster.meanCellHeight
    if spRefType == "Geographic":
        cellSize = cellSize/zFactor
    slope = Slope(r,"DEGREE",zFactor)
    aspect = Aspect(r)

    cosResult = Cos(Divide(Times(3.142,Minus(aspect,180)),180))
    outraster = Times(slope,cosResult)
    outRasterName = arcpy.GetParameterAsText(2)
    outraster.save (outRasterName)

except LicenseError:
    arcpy.AddError("Spatial Analyst license is unavailable")

