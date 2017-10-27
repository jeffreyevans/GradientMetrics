#-------------------------------------------------------------------------------
# Name:        Sobel Gradient
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

    script_path = sys.argv[0]
    sobelXFile = os.path.dirname(script_path)+'\\kernel_files\\sobelX.txt'
    sobelYFile = os.path.dirname(script_path)+'\\kernel_files\\sobelY.txt'

    Gx = FocalStatistics(Raster, NbrWeight(sobelXFile), "SUM")
    Gy = FocalStatistics(Raster, NbrWeight(sobelYFile), "SUM")
    method =arcpy.GetParameterAsText(0)
    if method == "Direction":
        outRaster = ATan2(Gy, Gx)
    else:
        outRaster = Sqrt(Square(Gx) + Square(Gy))

    outRasterName = arcpy.GetParameterAsText(2)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Sobel "+method+" Gradient Complete.")
