import sys,os
import arcpy

InDwg = arcpy.GetParameterAsText(0)
# InDwg = r"C:\Users\yagelm\Desktop\software\Gdal\GDAL_proj\gdal_geojson_project\files\DWG_from_hila\אחוזה-מסולד_עד_רמבם_מים.dwg"
scratchGDB = arcpy.env.scratchGDB
arcpy.env.workspace = scratchGDB

# Israel cor-sys
spatial_ref = arcpy.SpatialReference(2039) 
feature_dataset_name = "CADToGDB"
feature_dataset_path = os.path.join(scratchGDB, feature_dataset_name)

# Delete existing dataset if exists
if arcpy.Exists(feature_dataset_path):
    arcpy.Delete_management(feature_dataset_path)

feature_classes = []

# === CAD to GDB Conversion ===
arcpy.conversion.CADToGeodatabase(
    input_cad_datasets=InDwg,
    out_gdb_path=scratchGDB,
    out_dataset_name=feature_dataset_name,
    reference_scale=1000,
    spatial_reference=spatial_ref
)

for fc in arcpy.ListFeatureClasses(feature_dataset=feature_dataset_name):
    if not any(item in fc.lower() for item in ["polygon", "polyline", "point", "textpoint", "annotation", "multipatch"]):
        continue
    full_path = os.path.join(scratchGDB, feature_dataset_name, fc)
    # Add GeometryType field
    arcpy.AddField_management(full_path, "GeometryType", "TEXT", field_length=25)
    lyr_name = "'" + fc + "'"
    arcpy.CalculateField_management(full_path, "GeometryType", lyr_name, "PYTHON3")
    feature_classes.append(full_path)

# Set single output parameter
arcpy.SetParameter(1, feature_classes)
