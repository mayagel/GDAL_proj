import os
from osgeo import ogr

# Input DWG file path
# dwg_path = "../sample1.dwg" 
dwg_path = "..\\files\\dwg_from_web\\arc_2000.dwg"

# output directory
output_dir = "files\\outputs"

if not os.path.exists(dwg_path):
    raise FileNotFoundError(f"DWG file not found: {dwg_path}")

# Convert DWG to FileGDB
driver_dwg = ogr.GetDriverByName("CAD")
driver_geojson = ogr.GetDriverByName("GeoJSON")

# Open DWG
dwg_ds = driver_dwg.Open(dwg_path)
if not dwg_ds:
    raise RuntimeError("Failed to open DWG file.")

print("Layers in DWG:")
for i in range(dwg_ds.GetLayerCount()):
    layer = dwg_ds.GetLayerByIndex(i)
    print(f"Layer {i}: {layer.GetName()}")
    print(f"  Feature count: {layer.GetFeatureCount()}")
    layer_defn = layer.GetLayerDefn()
    print("  Fields:")
    for j in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(j)
        print(f"    {field_defn.GetName()} ({field_defn.GetTypeName()})")

        # Output GeoJSON file path
        geojson_path = output_dir + "\\Gdal" + dwg_path.split("\\")[-1][:-4] + ".geojson"

        # Create GeoJSON data source
        if os.path.exists(geojson_path):
            driver_geojson.DeleteDataSource(geojson_path)
        geojson_ds = driver_geojson.CreateDataSource(geojson_path)

        # Copy each layer from DWG to GeoJSON
        for i in range(dwg_ds.GetLayerCount()):
            layer = dwg_ds.GetLayerByIndex(i)
            # Create corresponding layer in GeoJSON
            srs = layer.GetSpatialRef()
            geojson_layer = geojson_ds.CreateLayer(layer.GetName(), srs, layer.GetGeomType())
            # Copy fields
            layer_defn = layer.GetLayerDefn()
            for j in range(layer_defn.GetFieldCount()):
                field_defn = layer_defn.GetFieldDefn(j)
                geojson_layer.CreateField(field_defn)
            # Copy features
            for feature in layer:
                geojson_feature = feature.Clone()
                geojson_layer.CreateFeature(geojson_feature)
                geojson_feature = None
            layer.ResetReading()

        geojson_ds = None
        print(f"GeoJSON file created: {geojson_path}")