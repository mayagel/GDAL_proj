from osgeo import ogr
import os

class GeoConverter:
    # def __init__(self):
        # self.output_dir = output_dir

    def convert(self, input_dwg, output_dxf=None):
        import subprocess
        import os

        def run_command(cmd):
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("Error output:", result.stderr)
                raise RuntimeError(f"Command failed: {' '.join(cmd)}")
            print(result.stdout)

        def convert_dwg_to_dxf(input_dwg, output_dxf):
            run_command(["dwgread", input_dwg, "-o", output_dxf])

        def convert_dxf_to_geojson(input_dxf, output_geojson):
            run_command(["ogr2ogr", "-f", "GeoJSON", output_geojson, input_dxf])

        def convert_dwg_to_geojson(input_dwg, output_geojson):
            base = os.path.splitext(output_geojson)[0]
            temp_dxf = base + ".dxf"
            convert_dwg_to_dxf(input_dwg, temp_dxf)
            convert_dxf_to_geojson(temp_dxf, output_geojson)
            os.remove(temp_dxf)  # Clean up temporary DXF

        # Example usage
        input_dwg = "files/DWG_from_hila/copy.dwg"
        output_geojson = "new.geojson"

        convert_dwg_to_geojson(input_dwg, output_geojson)
        # convert_dwg_to_geojson(input_dwg, output_geojson)
        print("Conversion complete!")

    def convert_gdb_to_geojson(self, gdb_path, output_geojson=None):
        driver = ogr.GetDriverByName("OpenFileGDB")
        dataSource = driver.Open(gdb_path, 0)

        for i in range(dataSource.GetLayerCount()):
            layer = dataSource.GetLayerByIndex(i)
            layer_name = layer.GetName()
            geojson_driver = ogr.GetDriverByName("GeoJSON")
            if os.path.exists(output_geojson):
                geojson_driver.DeleteDataSource(output_geojson)
            out_ds = geojson_driver.CreateDataSource(output_geojson)
            out_layer = out_ds.CopyLayer(layer, layer_name)
            out_ds = None

            print(f"Exported {layer_name} to {output_geojson}")

        dataSource = None

    def convert_dwg_to_geojson(self, dwg_path, geojson_output=None):
        from osgeo import gdal, ogr
        import json

        self.convert(dwg_path, geojson_output)

        # # Register all drivers (optional, but good practice)
        # ogr.RegisterAll()

        # # Open the input DWG file
        # dwg_driver = ogr.GetDriverByName("CAD")
        # dwg_datasource = dwg_driver.Open(dwg_path, 0) # 0 for read-only

        # if dwg_datasource is None:
        #     print("Could not open DWG file.")
        # else:
        #     # Create the DXF driver
        #     dxf_driver = ogr.GetDriverByName("DXF")

        #     # Create the output DXF datasource (overwrite if it exists)
        #     dxf_datasource = dxf_driver.CreateDataSource("output.dxf")

        #     if dxf_datasource is None:
        #         print("Could not create DXF file.")
        #     else:
        #         # Iterate through layers in the DWG and copy them to the DXF
        #         for i in range(dwg_datasource.GetLayerCount()):
        #             dwg_layer = dwg_datasource.GetLayerByIndex(i)
        #             # Create a new layer in the DXF datasource with the same name and spatial reference
        #             dxf_layer = dxf_datasource.CreateLayer(dwg_layer.GetName(),
        #                                                 dwg_layer.GetSpatialRef(),
        #                                                 dwg_layer.GetGeomType())
        #             # Add fields from the DWG layer to the DXF layer
        #             for j in range(dwg_layer.GetLayerDefn().GetFieldCount()):
        #                 field_defn = dwg_layer.GetLayerDefn().GetFieldDefn(j)
        #                 dxf_layer.CreateField(field_defn)

        #             # Copy features from the DWG layer to the DXF layer
        #             for feature in dwg_layer:
        #                 dxf_layer.CreateFeature(feature)

        #         print("DWG converted to DXF successfully.")

        #     # Close datasources
        #     dwg_datasource = None
        #     dxf_datasource = None

        # image = Image.load(dwg_path)
        # dxf_output = os.path.join('files', 'outputs', "temp.dxf")
        # image.save(dxf_output)

        # driver = ogr.GetDriverByName("DXF")
        # dataSource = driver.Open(dxf_output, 0)

        # if dataSource is not None:
        #     geojson = {
        #         "type": "FeatureCollection",
        #         "features": []
        #     }
        #     for i in range(dataSource.GetLayerCount()):
        #         layer = dataSource.GetLayerByIndex(i)
        #         for feature in layer:
        #             geom = feature.GetGeometryRef()
        #             if geom is not None:
        #                 geojson_feature = {
        #                     "type": "Feature",
        #                     "geometry": json.loads(geom.ExportToJson()),
        #                     "properties": feature.items()
        #                 }
        #                 geojson["features"].append(geojson_feature)

        #     with open(geojson_output, "w") as f:
        #         json.dump(geojson, f, indent=2)
        #     print(f"GeoJSON data written to {geojson_output}")

        #     dataSource = None
        # else:
        #     print("Failed to open DXF file for GeoJSON export.")