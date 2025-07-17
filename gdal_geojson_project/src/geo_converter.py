import os
import json
import logging
from osgeo import ogr # if was more pretty it should be in OsgeoConverter.py
from typing import Optional
from OsgeoConverter import OsgeoConverter
from SubprocessConverter import SubprocessConverter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GeoConverter:
    """
    High-level coordinator class to convert between DWG, DXF, GDB, and GeoJSON.
    Uses SubprocessConverter and OsgeoConverter internally.
    """

    def __init__(self, input_file: Optional[str] = None, output_dir: Optional[str] = None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg"
        self.output_dir = output_dir or "files/outputs"

        self.subprocess_converter = SubprocessConverter(self.input_file, self.output_dir)
        self.osgeo_converter = OsgeoConverter(self.input_file, self.output_dir)

    def convert_dwg_to_gdb(self, dwg_path: str, gdb_path: str):
        """
        Converts DWG to GDB using the best available method.
        Tries DWG->GDB if possible, else DWG->DXF->GDB.
        """
        # Check if DWG can be opened by GDAL CAD driver (R2000)
        cad_driver = ogr.GetDriverByName("CAD")
        dwg_ds = cad_driver.Open(dwg_path, 0) if cad_driver else None

        if dwg_ds:
            # DWG readable by CAD driver, so try DWG -> GDB -> GeoJSON
            logging.info(f"DWG file opened by CAD driver: {dwg_path}")
            gdb_path = os.path.splitext(geojson_path)[0] + ".gdb"
            self.osgeo_converter.convert_dwg_to_gdb(dwg_path, gdb_path)
        else:
            # Fallback to DWG -> DXF -> GeoJSON
            logging.info(f"DWG file NOT opened by CAD driver, fallback to subprocess method: {dwg_path}")
            self.subprocess_converter.convert_dwg_to_dxf(dwg_path, gdb_path.replace('.gdb', '.dxf'))
            self.osgeo_converter.convert_dxf_to_gdb(gdb_path.replace('.gdb', '.dxf'), gdb_path)  # fail because FGDB driver is not available

    def convert_dwg_to_geojson(self, dwg_path: str, geojson_path: str):
        """
        Converts DWG to GeoJSON using the best available method.
        Tries DWG->GDB->GeoJSON if possible, else DWG->DXF->GeoJSON.
        """
        # Check if DWG can be opened by GDAL CAD driver (R2000)
        cad_driver = ogr.GetDriverByName("CAD")
        dwg_ds = cad_driver.Open(dwg_path, 0) if cad_driver else None

        if dwg_ds:
            # DWG readable by CAD driver, so try DWG -> GDB -> GeoJSON
            logging.info(f"DWG file opened by CAD driver: {dwg_path}")
            gdb_path = os.path.splitext(geojson_path)[0] + ".gdb"
            self.osgeo_converter.convert_dwg_to_gdb(dwg_path, gdb_path)
            self.osgeo_converter.convert_gdb_to_geojson(gdb_path, geojson_path)
        else:
            # Fallback to DWG -> DXF -> GeoJSON
            logging.info(f"DWG file NOT opened by CAD driver, fallback to subprocess method: {dwg_path}")
            base = os.path.splitext(geojson_path)[0]
            temp_dxf = base + ".dxf"
            self.subprocess_converter.convert_dwg_to_dxf(dwg_path, temp_dxf)
            self.osgeo_converter.convert_dxf_to_geojson(temp_dxf, geojson_path)
            os.remove(temp_dxf)
            logging.info(f"Removed temporary file {temp_dxf}")
            # self.subprocess_converter.convert_dwg_to_geojson(dwg_path, geojson_path)