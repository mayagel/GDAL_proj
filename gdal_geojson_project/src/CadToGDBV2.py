import os
import arcpy

# === User Inputs ===
InDwg = arcpy.GetParameterAsText(0)
InDwg = r"C:\\Users\\yagelm\\Desktop\\software\\Gdal\\GDAL_proj\\gdal_geojson_project\\files\\complex_dwg\\Eyal-hiter-all.dwg"
user_gdb = arcpy.GetParameterAsText(1)       # Optional output GDB
user_feature_name = arcpy.GetParameterAsText(2)  # Optional feature dataset name

arcpy.env.overwriteOutput = True

if not os.path.exists(InDwg):
    arcpy.AddError(f"Input DWG file does not exist: {InDwg}")
    raise FileNotFoundError(f"Input DWG file does not exist: {InDwg}")

# === Setup ===
output_gdb = user_gdb if user_gdb else arcpy.env.scratchGDB
arcpy.env.workspace = output_gdb

feature_dataset_name = user_feature_name if user_feature_name else "CADToGDB"
spatial_ref = arcpy.SpatialReference(2039)  # Israel grid

feature_dataset_path = os.path.join(output_gdb, feature_dataset_name)

# Delete existing dataset if exists
if arcpy.Exists(feature_dataset_path):
    arcpy.Delete_management(feature_dataset_path)

# === CAD to GDB Conversion ===
arcpy.conversion.CADToGeodatabase(
    input_cad_datasets=InDwg,
    out_gdb_path=output_gdb,
    out_dataset_name=feature_dataset_name,
    reference_scale=1000,
    spatial_reference=spatial_ref
)

# === Post-processing: Add WKT and GeometryType ===
feature_classes = []

for fc in arcpy.ListFeatureClasses(feature_dataset=feature_dataset_name):
    full_path = os.path.join(output_gdb, feature_dataset_name, fc)

    # Add GeometryType field
    arcpy.AddField_management(full_path, "GeometryType", "TEXT", field_length=25)
    arcpy.CalculateField_management(full_path, "GeometryType", f"'{fc}'", "PYTHON3")

    # Add WKT field and calculate it
    arcpy.AddField_management(full_path, "WKT", "TEXT", field_length=1000000)
    with arcpy.da.UpdateCursor(full_path, ["SHAPE@", "WKT"]) as cursor:
        for row in cursor:
            if row[0] is not None:
                row[1] = row[0].WKT
                cursor.updateRow(row)

    feature_classes.append(full_path)

# === Convert to GeoJSON ===
geojson_output_folder = r".\gdal_geojson_project\output_geojson"
os.makedirs(geojson_output_folder, exist_ok=True)

geojson_files = []

for fc in feature_classes:
    name = os.path.basename(fc)
    geojson_path = os.path.join(geojson_output_folder, f"{name}.geojson")

    arcpy.conversion.FeaturesToJSON(
        in_features=fc,
        out_json_file=geojson_path,
        format_json=True,
        geoJSON=True
    )

    geojson_files.append(geojson_path)

# === Set Output Parameters ===
arcpy.SetParameter(3, ";".join(feature_classes))
arcpy.SetParameter(4, ";".join(geojson_files))