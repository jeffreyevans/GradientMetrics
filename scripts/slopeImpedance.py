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

    r = arcpy.GetParameterAsText(0)
    demRaster = geomorph_routines_module.checkExt(r)
    dscRaster = arcpy.Describe(demRaster)


    zUnits = arcpy.GetParameterAsText(1)
    zFactor = geomorph_routines_module.getZFactor(demRaster,zUnits)
    t = arcpy.GetParameterAsText(2)
    s = arcpy.GetParameterAsText(3)




    # Set overwrite option
    env.overwriteOutput = True
    #Need to have appropriate extent, will not work in ArcMap if spRefs differ



     #Set message about running
    arcpy.AddMessage("Running Slope Impedance......")

    tmp1=Slope(demRaster,"PERCENT_RISE",zFactor)

    tRaster = CreateConstantRaster(t,"FLOAT",dscRaster.MeanCellHeight,dscRaster.extent)
    sRaster = CreateConstantRaster(s,"FLOAT",dscRaster.MeanCellHeight,dscRaster.extent)
    oneRaster = CreateConstantRaster(1,"FLOAT",dscRaster.MeanCellHeight,dscRaster.extent)

    #outRaster = oneRaster - oneRaster / (oneRaster + Exp(tmp1 - tRaster) / sRaster)

    expR = Exp(Minus(tmp1,tRaster))
    denom = Divide(Plus(oneRaster,expR),sRaster)
    outRaster = Minus(oneRaster,Divide(oneRaster,denom))


    outRasterName = arcpy.GetParameterAsText(4)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Slope Impedance Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")


