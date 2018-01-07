import arcpy
from arcpy import env
from arcpy.sa import *
import geomorph_routines_module

class LicenseError(Exception):
    pass

try:
    #Check for spatial analyst license
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        raise LicenseError

    demRaster = arcpy.GetParameterAsText(0)

    inZUnits = arcpy.GetParameterAsText(1)

    zFactor = geomorph_routines_module.getZFactor(demRaster,inZUnits)
    # Set overwrite option
    env.overwriteOutput = True




     #Set message about running
    arcpy.AddMessage("Running Slope ......")
    sUnits = arcpy.GetParameterAsText(2)
    if sUnits == "DEGREE":
        slopeUnits = sUnits
    else:
        slopeUnits ="PERCENT_RISE"
    outRaster = Slope(demRaster,slopeUnits,zFactor)





    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)


    arcpy.AddMessage("Slope Complete")



except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable")

#finally:
    #arcpy.CheckInExtension("Spatial")
    # arcpy.Delete_management("forGettingLoc")
