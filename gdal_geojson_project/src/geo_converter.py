from osgeo import ogr
import os

class GeoConverter:
    # def __init__(self):
        # self.output_dir = output_dir

    def convert_gdb_to_geojson(self, gdb_path, output_geojson=None):
        driver = ogr.GetDriverByName("OpenFileGDB")
        dataSource = driver.Open(gdb_path, 0)

        for i in range(dataSource.GetLayerCount()):
            layer = dataSource.GetLayerByIndex(i)
            layer_name = layer.GetName()
            output_geojson = output_geojson

            geojson_driver = ogr.GetDriverByName("GeoJSON")
            if os.path.exists(output_geojson):
                geojson_driver.DeleteDataSource(output_geojson)
            out_ds = geojson_driver.CreateDataSource(output_geojson)
            out_layer = out_ds.CopyLayer(layer, layer_name)
            out_ds = None

            print(f"Exported {layer_name} to {output_geojson}")

        dataSource = None

    def convert_dwg_to_geojson(self, dwg_path, geojson_output=None):
        from aspose.cad import Image
        from osgeo import ogr
        import json

        image = Image.load(dwg_path)
        dxf_output = os.path.join('files', 'outputs', "temp.dxf")
        image.save(dxf_output)

        driver = ogr.GetDriverByName("DXF")
        dataSource = driver.Open(dxf_output, 0)

        geojson_output = geojson_output

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

            with open(geojson_output, "w") as f:
                json.dump(geojson, f, indent=2)
            print(f"GeoJSON data written to {geojson_output}")

            dataSource = None
        else:
            print("Failed to open DXF file for GeoJSON export.")