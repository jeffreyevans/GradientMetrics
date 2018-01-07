#-------------------------------------------------------------------------------
# Name:        classPercent.py
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

    env.snapRaster = r

    analysisWindow = arcpy.GetParameterAsText(2)

    classVal = arcpy.GetParameterAsText(1)
     #Set message about running
    arcpy.AddMessage("Running Class Percent ......")
    classValRas = CreateConstantRaster(classVal,"INTEGER",cellSize,ext)

    tmp1 = Con(r == classValRas,1,0)
    tmp2 = Con(r != classValRas,1,0)

    tmp3 = FocalStatistics(tmp1,analysisWindow,"SUM")
    tmp4 = FocalStatistics(tmp2,analysisWindow,"SUM")
    tmp5 = tmp3 + tmp4

    outRaster = Float( Float(tmp3) / Float(tmp5))

    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)


    #Set message about running
    arcpy.AddMessage("Class Percent Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


