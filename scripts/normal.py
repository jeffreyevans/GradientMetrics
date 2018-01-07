#-------------------------------------------------------------------------------
# Name:        Normal
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

    # Set overwrite option
    env.overwriteOutput = True
    inR = arcpy.GetParameterAsText(0)

    if inR:
        r = geomorph_routines_module.checkExt(inR)
        dscRaster = arcpy.Describe(r)
        spRef = dscRaster.spatialReference
        env.outputCoordinateSystem = spRef
        env.snapRaster = r
        env.extent = dscRaster.extent


    cellSize = arcpy.GetParameterAsText(1)
    meanVal = arcpy.GetParameterAsText(2)
    sdVal = arcpy.GetParameterAsText(3)

    outNorm = CreateNormalRaster(cellSize)

    meanRaster = CreateConstantRaster(meanVal,"FLOAT",cellSize,env.extent)
    sdRaster = CreateConstantRaster(sdVal,"FLOAT",cellSize,env.extent)
    outRaster = outNorm * sdRaster + meanRaster

    outRasterName = arcpy.GetParameterAsText(4)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Normal Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

