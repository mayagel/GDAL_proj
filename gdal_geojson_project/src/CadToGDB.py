

import sys,os
import arcpy

# InDwg = arcpy.GetParameterAsText(0)
InDwg = r"C:\\Users\\yagelm\\Desktop\\software\\Gdal\\GDAL_proj\\files\\dwg_to_geojson\\complex_dwg\\Eyal-hiter-all.dwg"
scratchGDB = arcpy.env.scratchGDB
arcpy.env.workspace = scratchGDB

# Create a list to hold all fInDwgture classes
feature_classes = []

# Basic convert - create temporary feature classes
for lyr in ["polygon", "polyline", "point", "textpoint", "annotation"]:
    fullLyr = scratchGDB + os.sep + lyr 
    # Delete existing dataset if exists
    if arcpy.Exists(fullLyr):
        arcpy.Delete_management(fullLyr)
    arcpy.FeatureClassToFeatureClass_conversion(InDwg +  os.sep + lyr, scratchGDB, lyr)

    # arcpy.convertion.exportfeatures(fullLyr, fullLyr, "GDB", "CAD", lyr)
    # arcpy.exportFeatures_convertion(fullLyr, fullLyr, "GDB", "CAD", lyr)
    # Add geometry type field to identify source
    arcpy.AddField_management(fullLyr, "GeometryType", "TEXT", field_length=25)
    arcpy.CalculateField_management(fullLyr, "GeometryType", f"'{lyr}'", "PYTHON3")
    # Add WKT field and populate it
    arcpy.AddField_management(fullLyr, "WKT", "TEXT", field_length=1000000 )
    
    # Calculate WKT values using cursor
    with arcpy.da.UpdateCursor(fullLyr, ["SHAPE@", "WKT"]) as cursor:
        for row in cursor:
            if row[0] is not None:
                row[1] = row[0].WKT
                cursor.updateRow(row)
    
    feature_classes.append(fullLyr)

    # Check spatial reference from first feature class
    lyrPath = feature_classes[0]
    desc = arcpy.Describe(lyrPath)
    if(desc.spatialReference.factoryCode == 0):
        sr = arcpy.SpatialReference(2039)
        for fc in feature_classes:
            arcpy.DefineProjection_management(fc, sr)

print(feature_classes)

# Set single output parameter
arcpy.SetParameter(1, feature_classes)
