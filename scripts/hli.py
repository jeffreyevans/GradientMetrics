#-------------------------------------------------------------------------------
# Name:        HLI.py
# Purpose:   Heat Load Index
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

    analysisWindow = arcpy.GetParameterAsText(1)

    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)
    inZUnits = arcpy.GetParameterAsText(1)
    zFactor = geomorph_routines_module.getZFactor(r,inZUnits)
    # Set overwrite option
    env.overwriteOutput = True
    # Getting info on raster
    dscRaster = arcpy.Describe(r)
    ext = dscRaster.extent
    midLat = geomorph_routines_module.getMidLat(ext)



    #Set message about running
    arcpy.AddMessage("Running HLI ......")
    l = float(midLat) * 0.017453293
    cl = math.cos(float(l))
    sl = math.sin(l)

    tmp1 = Slope(r,"DEGREE",zFactor) * 0.017453293               # s
    tmp2 = Aspect(r) * 0.017453293              # a
    tmp3 = Abs(3.141593 - Abs(tmp2 - 3.926991))         # f
    tmp4 = Cos(tmp1)
    tmp5 = Sin(tmp1)
    tmp6 = Cos(tmp3)
    tmp7 = Sin(tmp3)

    outRaster = Exp( -1.467 +  1.582 * cl * tmp4  - 1.5 * tmp6 * tmp5 * sl - 0.262 * sl * tmp5  + 0.607 * tmp7 * tmp5)

    outRasterName = arcpy.GetParameterAsText(2)
    outRaster.save (outRasterName)
    #newExt = dscPrj.extent

    #Set message about running
    arcpy.AddMessage("HLI Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")



