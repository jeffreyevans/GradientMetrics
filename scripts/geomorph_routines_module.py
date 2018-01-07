#-------------------------------------------------------------------------------
# Name:        Module to support Geomorphometrics_V2 toolbox
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
import time
import traceback
import sys
import tempfile
import math

def deleteTempFiles(hdr):
    dataList = arcpy.ListDatasets(hdr+"_*")
    for d in dataList:
        try:
            arcpy.Delete_management(d)
        except:
            arcpy.AddWarning("Could not delte "+d)
            continue
    fcList = arcpy.ListFeatureClasses(hdr+"_*")
    for fc in fcList:
        try:
            arcpy.Delete_management(fc)
        except:
            arcpy.AddWarning("Could not delte "+fc)
            continue

    tableList = arcpy.ListTables(hdr+"_*")
    for t in tableList:
        try:
            arcpy.Delete_management(t)
        except:
            arcpy.AddWarning("Could not delte "+t)
            continue


def checkExt(inDem):
    #arcpy.AddWarning("here = "+env.extent)
    if (env.extent):
        outRaster = Times(inDem,1)
        return outRaster
    else:
        outRaster = inDem
        if isArcMap():
            mapSRef = returnCurrentSRefOfMap()
            desc = arcpy.Describe(inDem)
            if mapSRef and mapSRef.name != desc.spatialReference.name:
                env.outputCoordinateSystem = mapSRef
                outRaster = Times(inDem,1)
        return outRaster





def getZFactor(dem,inZUnits):
    #inDem =checkExt(dem)
    descR = arcpy.Describe(dem)
    inSpRef = descR.spatialReference
    spRefType = inSpRef.type

    if spRefType == "Geographic":
        #arcpy.AddWarning("Data using a Geographic Spatial Reference.  For more accurate results project your DEM using the appropriate projection with matching XY and Z units and re-run tool")
        medianLat = getMidLat(descR.extent)
        rLat = math.radians(medianLat)
        meters2Degree = 111412.84 * math.cos(rLat) - 93.5*math.cos(3*rLat)
        if inZUnits == "Meter":
        #using 1 deg long is 111.412 kms at equator
            numerator = meters2Degree
        else:
        #Using 1 deg long is 69.172 miles at equator
            numerator = meters2Degree*3.28084
        zFactor = 1/numerator
    else:
        inUnits = inSpRef.linearUnitName
        if inUnits != inZUnits:
            if inUnits == "Meter":
                #Since they don't equal this means xyUnits == Meter and zUnits == Feet
                zFactor = 0.3048
            else:
                #Means xyUnits == Feet and  zUnits == Meters (not common)
                zFactor = 3.28084
        else:
            zFactor = 1.0

    return zFactor

def getMidLat (rExt):
    spRefType = rExt.spatialReference.type
    if spRefType == "Geographic":
        rYMax = rExt.YMax
        rYMin = rExt.YMin
        medianLat = abs((float(rYMax)- float(rYMin))/2+rYMin)
    else:
        wgs84 = arcpy.SpatialReference(4326)
        prjExt = rExt.projectAs(wgs84)
        rYMax = prjExt.YMax
        rYMin = prjExt.YMin
        medianLat = abs((float(rYMax)- float(rYMin))/2+rYMin)
    return medianLat

def isArcMap():
	try:
		mxd = arcpy.mapping.MapDocument("CURRENT")
		return True
	except:
		return False

def returnCurrentSRefOfMap():
    mxd = arcpy.mapping.MapDocument("CURRENT")
    sRef = mxd.activeDataFrame.spatialReference
    if sRef.factoryCode == 0:
        sRef = None
    return sRef

