#-------------------------------------------------------------------------------
# Name:        Guassian Smoothing
# Purpose:
#
# Authors:      Jeff Evans and Jim Oakleaf
#
# Created:     09/09/2014
# Copyright:   (c) Evans and Oakleaf 2014
# Licence:     Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#-------------------------------------------------------------------------------
import math
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

    script_path = sys.argv[0]
    guassian_file = os.path.dirname(script_path)+'\\kernel_files\\gaussian.txt'

    #Creating or opening guassian_file all info will be overwritten
    crs = open(guassian_file,'w')

    xVals = []
    yVals = []

    sig = float(arcpy.GetParameterAsText(1))
    n = int(arcpy.GetParameterAsText(2))


    CeilVal = math.ceil (float(n)/2)

    for i in range(1,n+1):
        for c in range(1,n+1):
            xVals.append(c-CeilVal)
            yVals.append(i-CeilVal)

    vals = []
    for i in range(0,n*n):
        x = xVals[i]
        y = yVals[i]
        val2Exp = (x*x+y*y)/(2*sig*sig)*-1
        expVal = math.exp(val2Exp)
        val = 1/(2*math.pi*sig*sig)*expVal
        vals.append(val)


    finalVals = []
    sumVal = 0
    for i in range(0,n*n):
     sumVal+= vals[i]

    for i in range(0,n*n):
        finalVal = vals[i] / sumVal
        finalVals.append(finalVal)

    crs.write(str(n)+" "+str(n)+"\n")

    nextLine = n - 1
    strLine = ""
    for j in range(0,n*n):
     strLine+=str(finalVals[j])+" "
     if j == nextLine:
        strLine = strLine.strip()
        strLine +="\n"
        crs.write(strLine)
        strLine = ""
        nextLine += n

    crs.close()
    nbrWt = NbrWeight(guassian_file)
    outRaster = FocalStatistics(r,nbrWt,"MEAN")

    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Guassian Smoothing Complete")


except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")
