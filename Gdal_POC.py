from osgeo import ogr

# Input DWG file path
# dwg_path = "files\\dwg_from_web\\arc_2000.dwg" # working with this file (R2000 (AC1015))
dwg_path = "files\\Eyal_files\\kav only.dwg" # Error with this file (AC1027)

# Convert DWG to FileGDB
driver_dwg = ogr.GetDriverByName("CAD")
driver_geojson = ogr.GetDriverByName("GeoJSON")

# Open DWG
dwg_ds = driver_dwg.Open(dwg_path)

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
        output_dir = "files\\outputs"
        geojson_path = output_dir + "\\Gdal_" + dwg_path.split("\\")[-1][:-4] + ".geojson"

        # Create GeoJSON data source
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