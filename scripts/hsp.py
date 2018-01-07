#-------------------------------------------------------------------------------
# Name:        hsp.py
# Purpose:     Hierarchical Slope Position
#
# Authors:      Jeffrey Evans, Jim Oakleaf and Jim Ellenwood 
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
    nmin = arcpy.GetParameter(1)
    nmax = arcpy.GetParameter(2)
    inc = arcpy.GetParameter(3)
    cnt = 0
    nbrWidth = int(nmin)

    while nbrWidth <= int(nmax) : #>
        nbrRec = NbrRectangle(nbrWidth,nbrWidth,"CELL")
        focalMean = FocalStatistics(r,nbrRec,"Mean","DATA")
        exprad = Int(r - focalMean)
        arcpy.CalculateStatistics_management(exprad)
        mean = float(arcpy.GetRasterProperties_management(exprad,"MEAN").getOutput(0))
        std = float(arcpy.GetRasterProperties_management(exprad,"STD").getOutput(0))
        expradnrm = Int(100*((exprad - mean)/std))
        nbrWidth+=int(inc)
        cnt+=1

    nbrWidth = nbrWidth

    #jre added these two lines of code to save raster Hierarchial_Raster
    outRasterName = arcpy.GetParameterAsText(4)
    expradnrm.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Hierarchical Slope Position Complete")

except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")
