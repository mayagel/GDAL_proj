import os
from osgeo import ogr

# Input GDB and output directory
gdb_path = r'files\\Eyal_files\\kav_sourceFgdb.gdb'
output_dir = r'files\\outputs'

# Open the GDB
driver = ogr.GetDriverByName("OpenFileGDB")
dataSource = driver.Open(gdb_path, 0)

# Loop through layers and export each to GeoJSON
for i in range(dataSource.GetLayerCount()):
    layer = dataSource.GetLayerByIndex(i)
    layer_name = layer.GetName()
    output_geojson = os.path.join(output_dir, f"Gdal_{layer_name}_{i}.geojson")

    # Create GeoJSON
    geojson_driver = ogr.GetDriverByName("GeoJSON")
    if os.path.exists(output_geojson):
        geojson_driver.DeleteDataSource(output_geojson)
    out_ds = geojson_driver.CreateDataSource(output_geojson)
    out_layer = out_ds.CopyLayer(layer, layer_name)
    out_ds = None  # Close the file

    print(f"Exported {layer_name} to {output_geojson}")

dataSource = None  # Close the GDB