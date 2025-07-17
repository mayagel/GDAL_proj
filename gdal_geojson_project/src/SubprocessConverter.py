import os
import json
import subprocess
import logging
from typing import Optional

class SubprocessConverter:
    """
    Converter using external subprocess commands like 'dwgread' and 'ogr2ogr'
    to convert DWG and DXF files to GeoJSON.
    """
    def __init__(self, input_file: Optional[str] = None, output_dir: Optional[str] = None):
        self.input_file = input_file or "files/DWG_from_hila/copy.dwg"
        self.output_dir = output_dir or "files/outputs"

    def run_command(self, cmd: list[str]):
        """
        Run a shell command with subprocess and handle errors.
        """
        logging.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Command failed with exit code {result.returncode}")
            logging.error(f"stderr: {result.stderr}")
            raise RuntimeError(f"Command failed: {' '.join(cmd)}")
        logging.info(result.stdout)

    def convert_dwg_to_dxf(self, input_dwg: str, output_dxf: str):
        """
        Convert DWG file to DXF using 'dwgread' command.
        """
        self.run_command(["dwgread", input_dwg, "-o", output_dxf])

    def convert_dxf_to_geojson(self, input_dxf: str, output_geojson: str):
        """
        Convert DXF file to GeoJSON using 'ogr2ogr' command.
        """
        self.run_command(["ogr2ogr", "-f", "GeoJSON", output_geojson, input_dxf])

    def convert_dwg_to_geojson(self, input_dwg: str, output_geojson: str):
        """
        Convert DWG to GeoJSON by converting to DXF first, then to GeoJSON.
        Cleans up the temporary DXF file.
        """
        base = os.path.splitext(output_geojson)[0]
        temp_dxf = base + ".dxf"
        self.convert_dwg_to_dxf(input_dwg, temp_dxf)
        self.convert_dxf_to_geojson(temp_dxf, output_geojson)
        os.remove(temp_dxf)
        logging.info(f"Removed temporary file {temp_dxf}")