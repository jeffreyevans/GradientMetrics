#-------------------------------------------------------------------------------
# Name:        devFromTrend.py
# Purpose:   Deviation from Trend
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
    inOrder = arcpy.GetParameterAsText(1)
    r = geomorph_routines_module.checkExt(inR)
    env.overwriteOutput = True

    # Getting info on raster
    dscRaster = arcpy.Describe(r)
    inSpRef = dscRaster.spatialReference
    spRefType = inSpRef.type
    cellSize = dscRaster.meanCellHeight

    ws = env.workspace
    wsDesc = arcpy.Describe(ws)
    wsType = wsDesc.workspaceType
    if wsType == "Filesystem":
        ptFile = "xxTrendPts.shp"
    else:
        ptFile = "xxTrendPts"

    arcpy.RasterToPoint_conversion(r,ptFile,"VALUE")
    outTrend = Trend(ptFile,"grid_code",cellSize,inOrder,"LINEAR")
    arcpy.Delete_management(ptFile)
    trendType = arcpy.GetParameterAsText(2)
    if trendType == "Trend":
        outraster = Minus(r,outTrend)
    else:
        outraster = Minus(outTrend,r)
    outRasterName = arcpy.GetParameterAsText(3)
    outraster.save (outRasterName)

except LicenseError:
    print "Spatial Analyst license is unavailable"










