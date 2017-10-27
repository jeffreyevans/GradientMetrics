#-------------------------------------------------------------------------------
# Name:        Transformation
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
    descR = arcpy.Describe(r)

    # Set overwrite option
    env.overwriteOutput = True


    try:
        std = arcpy.GetRasterProperties_management(r,"STD")
    except arcpy.ExecuteError:
        arcpy.CalculateStatistics_management(r)


    analysisType = arcpy.GetParameterAsText(1)


     #Set message about running

    if  analysisType == "Standardize":
        arcpy.AddMessage("Running Standardize Transformation ......")

        stdv = arcpy.GetRasterProperties_management(r,"STD")
        stdvRaster = CreateConstantRaster(stdv,"FLOAT",descR.MeanCellHeight,descR.extent)
        mean = arcpy.GetRasterProperties_management(r,"MEAN")
        meanRaster = CreateConstantRaster(mean,"FLOAT",descR.MeanCellHeight,descR.extent)
        outRaster = (r - meanRaster) / stdvRaster

    elif analysisType == "Stretch":
        arcpy.AddMessage("Running Stretch Transformation ......")
        maxVal = arcpy.GetRasterProperties_management(r,"MAXIMUM")
        maxRaster = CreateConstantRaster(maxVal,"FLOAT",descR.MeanCellHeight,descR.extent)

        minVal = arcpy.GetRasterProperties_management(r,"MINIMUM")
        minRaster = CreateConstantRaster(minVal,"FLOAT",descR.MeanCellHeight,descR.extent)
        
        
        inputMax = arcpy.GetParameterAsText(2)
        if not(arcpy.Exists(inputMax)):
            inputMax = 1
        inputMaxRaster = CreateConstantRaster(inputMax,"FLOAT",descR.MeanCellHeight,descR.extent)
        inputMin = arcpy.GetParameterAsText(3)
        if not(arcpy.Exists(inputMin)):
            inputMin = 0
        inputMinRaster = CreateConstantRaster(inputMin,"FLOAT",descR.MeanCellHeight,descR.extent)

        outRaster = (r - minRaster)*(inputMaxRaster-inputMinRaster) / (maxRaster - minRaster) + inputMinRaster


    elif analysisType == "Normalize":
        arcpy.AddMessage("Running Normalize Transformation ......")
        maxVal = arcpy.GetRasterProperties_management(r,"MAXIMUM")
        minVal = arcpy.GetRasterProperties_management(r,"MINIMUM")
        maxRaster = CreateConstantRaster(maxVal,"FLOAT",descR.MeanCellHeight,descR.extent)
        if minVal != 0:
            minRaster = CreateConstantRaster(minVal,"FLOAT",descR.MeanCellHeight,descR.extent)
            outRaster = (r - minRaster)/(maxRaster - minRaster)
        else:
            outRaster = r / maxRaster


    elif analysisType == "Log":
        arcpy.AddMessage("Running Log Transformation ......")
        outRaster = Ln(r)

    else:
        #Has to be Square-root
        arcpy.AddMessage("Running Square-root Transformation ......")
        outRaster = SquareRoot(r)




    outRasterName = arcpy.GetParameterAsText(4)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage(analysisType+" Transformation Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


