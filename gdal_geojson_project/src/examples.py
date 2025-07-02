from geo_converter import GeoConverter
import os
import glob

def main():
    # Example 1: Convert GDB to GeoJSON
    # gdb_path = r'files\\Eyal_files\\kav_sourceFgdb.gdb'
    # output_dir = r'files\\outputs'
    # geo_converter_gdb = GeoConverter(output_dir)
    # geo_converter_gdb.convert_gdb_to_geojson(gdb_path)

    # # Example 2: Convert DWG to GeoJSON using Aspose.CAD
    # dwg_path = r'files\\Eyal_files\\kav only.dwg'
    # geo_converter_dwg = GeoConverter(output_dir)
    # geo_converter_dwg.convert_dwg_to_geojson(dwg_path)

    def sanitize_output_name(input_path):
        # Remove extension, replace backslashes with underscores
        base = os.path.splitext(input_path)[0]
        return base.replace("\\", "__").replace("/", "__") + ".geojson"

    # Process all .gdb files in files\gdb_to_geojson (not directories)
    gdb_dir = r'files\\gdb_to_geojson'
    for root, dirs, files in os.walk(gdb_dir):
        for file in files:
            if file.lower().endswith('.gdb'):
                gdb_file_path = os.path.join(root, file)
                if os.path.isfile(gdb_file_path):
                    output_name = sanitize_output_name(os.path.relpath(gdb_file_path, start='files'))
                    # output_path = os.path.join('files', 'output', output_name)
                    geo_converter = GeoConverter()
                    geo_converter.convert_gdb_to_geojson(gdb_file_path, output_name)


    # Process all .dwg files in files\dwg_to_geojson
    dwg_dir = r'files\\dwg_to_geojson'
    for root, dirs, files in os.walk(dwg_dir):
        for file in files:
            if file.lower().endswith('.dwg'):
                dwg_file_path = os.path.join(root, file)
                if os.path.isfile(dwg_file_path):
                    output_name = sanitize_output_name(os.path.relpath(dwg_file_path, start='files'))
                    output_path = os.path.join('files', 'output', os.path.join('files', 'outputs', output_name))
                    geo_converter = GeoConverter()
                    geo_converter.convert_dwg_to_geojson(dwg_file_path, os.path.join('files', 'outputs', output_name))
if __name__ == "__main__":
    main()