#-------------------------------------------------------------------------------
# Name:        imi.py
# Purpose:   Integrated Moisture Index
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
class CSError (Exception):
    pass

try:
	#Check for spatial analyst license
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        raise LicenseError


    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)
    inFd = arcpy.GetParameterAsText(1)
    inZUnits = arcpy.GetParameterAsText(2)
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


    #Set message about running
    arcpy.AddMessage("Running IMI ......")
    if arcpy.Exists(inFd):
        cDesc = arcpy.Describe(inFd)
        if inSpRef.name != cDesc.spatialReference.name:
            raise CSError
        fd = geomorph_routines_module.checkExt(inFd)
    else:
        fd = FlowDirection(r)

    flowAcc = FlowAccumulation(fd)
    xFlow = Times(flowAcc,0.35)
    curv = Curvature(r,zFactor)
    xcurv = Times(curv,0.15)
    hlshd = Hillshade(r,"#","#","#",zFactor)
    xhlshd = Times(hlshd,0.5)


    outraster = Plus(Plus(xFlow,xcurv),xhlshd)
    outRasterName = arcpy.GetParameterAsText(3)
    outraster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Integrated Moisture Index Complete")


except LicenseError:
    arcpy.AddError("Spatial Analyst license is unavailable")
except CSError:
    arcpy.AddError("Both DEM and Flow Direction datasets must use the same coordinate system.")

