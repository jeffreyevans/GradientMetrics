#-------------------------------------------------------------------------------
# Name:        angle.py
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
    cellSize = dscRaster.meanCellWidth
    ext = dscRaster.extent

#    if dscRaster.spatialReference.type != "Projected":
#        raise SpatialRefProjError
    rType = arcpy.GetParameterAsText(1)
    conversionType = arcpy.GetParameterAsText(2)

    # Set overwrite option
    env.overwriteOutput = True


    env.snapRaster = r

    if rType == "Slope":
        f = CreateConstantRaster(90,"FLOAT",cellSize,ext)
    else:
        f = CreateConstantRaster(180,"FLOAT",cellSize,ext)

    p = CreateConstantRaster(1.570796,"FLOAT",cellSize,ext)
    #Set message about running
    arcpy.AddMessage("Running Angle Conversion ......")
    if conversionType == "Radians to Degrees":
        outRaster = r * p / f
    else:
        #Degrees to radians
        outRaster = r * f / p


    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Angle Conversion Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


