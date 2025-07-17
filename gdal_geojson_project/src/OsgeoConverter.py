import os
import json
import logging
import subprocess # if was more pretty it should be in SubprocessConverter.py
from typing import Optional
from osgeo import ogr, gdal

class OsgeoConverter:
    """
    Converter using OGR from GDAL Python bindings for reading and writing
    GDB, DXF, and GeoJSON formats.
    """

    def __init__(self, input_file: Optional[str] = None, output_dir: Optional[str] = None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg"
        self.output_dir = output_dir or "files/outputs"

    def convert_gdb_to_geojson2(self, gdb_path: str, output_geojson: str):
        """
        Convert OpenFileGDB to GeoJSON.
        """
        driver = ogr.GetDriverByName("OpenFileGDB")
        data_source = driver.Open(gdb_path, 0)  # Read-only
        if data_source is None:
            logging.error(f"Could not open GDB: {gdb_path}")
            return

        geojson_driver = ogr.GetDriverByName("GeoJSON")
        if os.path.exists(output_geojson):
            geojson_driver.DeleteDataSource(output_geojson)

        for i in range(data_source.GetLayerCount()):
            layer = data_source.GetLayerByIndex(i)
            layer_name = layer.GetName()

            out_ds = geojson_driver.CreateDataSource(output_geojson)
            out_ds.CopyLayer(layer, layer_name)
            out_ds = None
            logging.info(f"Exported layer {layer_name} to {output_geojson}")

        data_source = None

    def convert_dwg_to_gdb(self, dwg_path: str, gdb_output: Optional[str] = None):
        """
        Convert DWG to FileGDB by first converting to DXF, then DXF to GDB.
        """
        if gdb_output is None:
            base = os.path.splitext(dwg_path)[0]
            gdb_output = base + ".gdb"

        temp_dxf = os.path.splitext(gdb_output)[0] + "_temp.dxf"

        # Convert DWG to DXF first
        logging.info(f"Converting DWG to DXF: {dwg_path} -> {temp_dxf}")
        dwg_to_dxf_cmd = ["dwgread", dwg_path, "-o", temp_dxf]
        subprocess.run(dwg_to_dxf_cmd, check=True)

        # Convert DXF to GDB
        logging.info(f"Converting DXF to GDB: {temp_dxf} -> {gdb_output}")
        self.convert_dxf_to_gdb(temp_dxf, gdb_output)

        # Clean up temp DXF
        if os.path.exists(temp_dxf):
            os.remove(temp_dxf)
            logging.info(f"Removed temporary file {temp_dxf}")

    def convert_dxf_to_geojson(self, dxf_path: str, geojson_output: str):
        """
        Convert DXF to GeoJSON using OGR's built-in GeoJSON driver.
        """
        dxf_driver = ogr.GetDriverByName("DXF")
        dxf_ds = dxf_driver.Open(dxf_path, 0)
        if dxf_ds is None:
            logging.error(f"Failed to open DXF file: {dxf_path}")
            return

        geojson_driver = ogr.GetDriverByName("GeoJSON")
        if os.path.exists(geojson_output):
            geojson_driver.DeleteDataSource(geojson_output)

        geojson_ds = geojson_driver.CreateDataSource(geojson_output)
        if geojson_ds is None:
            logging.error(f"Failed to create GeoJSON file: {geojson_output}")
            return

        for i in range(dxf_ds.GetLayerCount()):
            layer = dxf_ds.GetLayerByIndex(i)
            layer_name = layer.GetName()
            geojson_ds.CopyLayer(layer, layer_name)
            logging.info(f"Copied layer '{layer_name}' to {geojson_output}")

        geojson_ds = None
        dxf_ds = None

        logging.info(f"DXF to GeoJSON conversion complete: {geojson_output}")

    def convert_dxf_to_gdb(self, dxf_path: str, gdb_output: Optional[str] = None):
        """
        Convert DXF file to FileGDB format using OGR.
        """
        if gdb_output is None:
            base = os.path.splitext(dxf_path)[0]
            gdb_output = base + ".gdb"

        dxf_driver = ogr.GetDriverByName("DXF")
        dxf_ds = dxf_driver.Open(dxf_path, 0)
        if dxf_ds is None:
            logging.error(f"Failed to open DXF file: {dxf_path}")
            return

        gdb_driver = ogr.GetDriverByName("FileGDB") #error with ogr.GetDriverByName("OpenFileGDB") on linux
        if gdb_driver is None:
            logging.error("FileGDB driver not available in GDAL build")
            return

        # Delete existing GDB if present
        if os.path.exists(gdb_output):
            logging.info(f"Deleting existing GDB at {gdb_output}")
            gdb_driver.DeleteDataSource(gdb_output)

        gdb_ds = gdb_driver.CreateDataSource(gdb_output)
        if gdb_ds is None:
            logging.error(f"Failed to create GDB datasource at {gdb_output}")
            return

        for i in range(dxf_ds.GetLayerCount()):
            layer = dxf_ds.GetLayerByIndex(i)
            layer_name = layer.GetName()
            logging.info(f"Copying layer '{layer_name}' to GDB")
            gdb_ds.CopyLayer(layer, layer_name)

        gdb_ds = None
        dxf_ds = None

        logging.info(f"DXF to GDB conversion complete: {gdb_output}")

    def convert_dxf_to_geojson2(self, dxf_path: str, geojson_output: str):
        """
        Convert DXF to GeoJSON by reading features and serializing geometry and attributes.
        """
        driver = ogr.GetDriverByName("DXF")
        data_source = driver.Open(dxf_path, 0)
        if data_source is None:
            logging.error(f"Failed to open DXF file: {dxf_path}")
            return

        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for i in range(data_source.GetLayerCount()):
            layer = data_source.GetLayerByIndex(i)
            for feature in layer:
                geom = feature.GetGeometryRef()
                if geom:
                    geojson_feature = {
                        "type": "Feature",
                        "geometry": json.loads(geom.ExportToJson()),
                        "properties": feature.items()
                    }
                    geojson["features"].append(geojson_feature)

        with open(geojson_output, "w") as f:
            json.dump(geojson, f, indent=2)

        logging.info(f"GeoJSON data written to {geojson_output}")

        data_source = None