#-------------------------------------------------------------------------------
# Name:        SurfaceAreaRatio.py
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
    inZUnits = arcpy.GetParameterAsText(1)
    zFactor = geomorph_routines_module.getZFactor(r,inZUnits)
    # Getting info on raster
    dscRaster = arcpy.Describe(r)
    inSpRef = dscRaster.spatialReference
    spRefType = inSpRef.type
    cellSize = dscRaster.meanCellHeight

  # Set overwrite option
    env.overwriteOutput = True

    env.cellSize = cellSize
    if spRefType == "Geographic":
        SizeEstimate = cellSize/zFactor
        c = SizeEstimate * SizeEstimate
    else:
        c = cellSize * cellSize
    v = math.pi/180
    tmp1 = Slope(r,"DEGREE",zFactor) * v



    outRaster =  Float(c) / Cos(tmp1)



    outRasterName = arcpy.GetParameterAsText(2)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Surface Area Ratio Complete")

except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


