from osgeo import gdal, ogr
import json
import subprocess
import os

class SubprocessConverter:
    def __init__(self, input_file=None, output_dir=None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg"
        self.output_dir = output_dir or 'files/outputs'

    def run_command(self, cmd):
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error output:", result.stderr)
            raise RuntimeError(f"Command failed: {' '.join(cmd)}")
        print(result.stdout)

    def convert_dwg_to_geojson(self, input_dwg, output_geojson):
        base = os.path.splitext(output_geojson)[0]
        temp_dxf = base + ".dxf"
        self.convert_dwg_to_dxf(input_dwg, temp_dxf)
        self.convert_dxf_to_geojson(temp_dxf, output_geojson)
        os.remove(temp_dxf)  # Clean up temporary DXF

    def convert_dwg_to_dxf(self, input_dwg, output_dxf):
        self.run_command(["dwgread", input_dwg, "-o", output_dxf])

    def convert_dxf_to_geojson(self, input_dxf, output_geojson):
        self.run_command(["ogr2ogr", "-f", "GeoJSON", output_geojson, input_dxf])

class OsgeoConverter:
    def __init__(self, input_file=None, output_dir=None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg"
        self.output_dir = output_dir or 'files/outputs'

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

    def convert_dwg_to_gdb(self, dwg_path, gdb_output=None):

        # Register all drivers (optional, but good practice)
        ogr.RegisterAll()

        # Open the input DWG file
        dwg_driver = ogr.GetDriverByName("CAD")
        dwg_datasource = dwg_driver.Open(dwg_path, 0) # 0 for read-only

        if dwg_datasource is None:
            print("Could not open DWG file.")
            return None
        else:
            # use dwg_driver to convert to GDB
            pass    
    
    def convert_dxf_to_GDB(self, dwg_path, GDB=None):
        #need to use dxf driver to convert to GDB
        pass

    def convert_dxf_to_geojson(self, dxf_path, geojson_output=None):
        driver = ogr.GetDriverByName("DXF")
        dataSource = driver.Open(dxf_path, 0)

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
        
class GeoConverter:
    def __init__(self, input_file=None, output_dir=None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg
        self.output_dir = output_dir or 'files/outputs'

# convert DWG to GDB (if its R2000 we won) (should use OsgeoConverter class)

# convert DWG to DXF (if its not R2000 should use this function first) (should use SubprocessConverter class)

# convert DXF to GDB (if its not R2000 should use this functions second) (should use OsgeoConverter class)

# convert GDB to GeoJSON (should work any time) (should use OsgeoConverter class)
