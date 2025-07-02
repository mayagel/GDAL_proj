# This is a conceptual example as Aspose.CAD is a commercial library.
# The exact usage may vary based on the library's documentation.
from aspose.cad import Image
from osgeo import ogr
import json

output_dir = "files\\outputs"

# Input DWG file path
# dwg_path = "files\\dwg_from_web\\arc_2000.dwg" # working with this file (R2000 (AC1015))
# dwg_path = "files\\Eyal_files\\kav only.dwg" # wotks now! with this file (AC1027)
# dwg_path = "files\\dwg_to_geojson\\dwg_from_web\\architectural_-_annotation_scaling_and_multileaders.dwg" # works partially (errors and the files create anyway) with this file (AC1021)
dwg_path = "files\\dwg_to_geojson\\Eyal-hiter-all.dwg" # works partially (errors and the files create anyway) with this file (AC1032)



# Load the DWG file
image = Image.load(dwg_path)

# Export the DWG as DXF
dxf_output = output_dir + "\\kav_only.dxf"
image.save(dxf_output)

# Now use GDAL to read the DXF file

driver = ogr.GetDriverByName("DXF")
dataSource = driver.Open(dxf_output, 0)  # 0 means read-only


# Output GeoJSON file path
geojson_output = output_dir + "\\Gdal_" + dwg_path.split("\\")[-1][:-4] + "_using_apose.geojson"

# Re-open the DXF file to extract features
dataSource = driver.Open(dxf_output, 0)
if dataSource is not None:
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for i in range(dataSource.GetLayerCount()):
        layer = dataSource.GetLayerByIndex(i)
        for feature in layer:
            geom = feature.GetGeometryRef()
            if geom is not None:
                geojson_feature = {
                    "type": "Feature",
                    "geometry": json.loads(geom.ExportToJson()),
                    "properties": feature.items()
                }
                geojson["features"].append(geojson_feature)
    # Write to GeoJSON file
    with open(geojson_output, "w") as f:
        json.dump(geojson, f, indent=2)
    print(f"GeoJSON data written to {geojson_output}")

    # Print the data from the GeoJSON file
    with open(geojson_output, "r") as f:
        data = json.load(f)
        json.dumps(data, indent=2)
    dataSource = None
else:
    print("Failed to open DXF file for GeoJSON export.")

