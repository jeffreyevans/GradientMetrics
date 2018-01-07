#-------------------------------------------------------------------------------
# Name:        Covariance
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
    #
    inR = arcpy.GetParameterAsText(0)
    r = geomorph_routines_module.checkExt(inR)

    rOne = arcpy.GetParameterAsText(0)
    rasterOne = geomorph_routines_module.checkExt(rOne)
    rasterOneDesc = arcpy.Describe(rasterOne)
    rTwo = arcpy.GetParameterAsText(1)
    rasterTwo = geomorph_routines_module.checkExt(rTwo)
    rasterTwoDesc = arcpy.Describe(rasterTwo)



    # Set overwrite option
    env.overwriteOutput = True

    analysisWindow = arcpy.GetParameterAsText(3)


     #Set message about running
    arcpy.AddMessage("Calculating Statistics......")
    tmpXY = Times(rasterOne,rasterTwo)

    xBar = FocalStatistics(rasterOne,analysisWindow,"MEAN")
    yBar = FocalStatistics(rasterTwo,analysisWindow,"MEAN")
    xyBar =FocalStatistics(tmpXY,analysisWindow,"MEAN")


    OutType = arcpy.GetParameterAsText(2)
    coVar = Minus(xyBar,Times(xBar,yBar))
    outRasterName = arcpy.GetParameterAsText(4)
    if OutType == "Covariance":
        coVar.save(outRasterName)
        arcpy.AddMessage("Covariance Complete")
    else:
        xStd = FocalStatistics(rasterOne,analysisWindow,"STD")
        yStd = FocalStatistics(rasterTwo,analysisWindow,"STD")
        xyStd = Times(xStd,yStd)
        corr = Divide(coVar,xyStd)
        corr.save(outRasterName)
        arcpy.AddMessage("Correlation Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

