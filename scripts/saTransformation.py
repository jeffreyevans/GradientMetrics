#-------------------------------------------------------------------------------
# Name:        meanSlope.py
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
    inZUnits = arcpy.GetParameterAsText(1)
    zFactor = geomorph_routines_module.getZFactor(r,inZUnits)
    # Set overwrite option
    env.overwriteOutput = True


    analysisType = arcpy.GetParameterAsText(2)


     #Set message about running
    arcpy.AddMessage("Running Transformation ......")
    if  analysisType == "COS" or analysisType == "SIN":
        aspect = Aspect(r)
        nullSet = SetNull(aspect==-1,aspect)
        slope = Slope(r,"PERCENT_RISE",zFactor)
        con = Con(slope>100,101,slope)
        tmp4 = con / 100
        if analysisType == "COS":
            outRaster = Cos(nullSet/57.296)*tmp4
        else:
            #sin selected
            outRaster = Sin(nullSet/57.296)*tmp4

    else:
        #Has to be TRASP
        aspect = Aspect(r)
        #tmp2 = SetNull(aspect < 0, aspect)
        tmp2 = 1 - Cos((3.142/180)*(aspect - 30))
        tmp3 = tmp2/2
        outRaster = Con(aspect<0,0.5,tmp3)




    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage(analysisType+" Transformation Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

