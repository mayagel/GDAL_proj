from geo_converter import GeoConverter
import os
import glob

def main():
    def sanitize_output_name(input_path):
        # Remove extension, replace backslashes with underscores
        base = os.path.splitext(input_path)[0]
        return base.replace("\\", "__").replace("/", "__") + ".json"

    # Process all .gdb files in files\gdb_to_geojson (not directories)
    gdb_dir = r'files\\gdb_to_geojson'
    for root, dirs, files in os.walk(gdb_dir):
        for file in dirs:
            if file.lower().endswith('.gdb'):
                gdb_file_path = os.path.join(root, file)
                # if os.path.isfile(gdb_file_path):
                # Replace the .gdb extension with .geojson and prefix with "output"
                # Insert 'output' after 'files' in the path and change extension to .json
                rel_path = os.path.relpath(gdb_file_path, start='files')
                output_name = os.path.join('files', 'outputs', rel_path).replace('.gdb', '.geojson')
                # output_path = os.path.join('files', 'output', output_name)
                geo_converter = GeoConverter()
                geo_converter.convert_gdb_to_geojson(gdb_file_path,  output_name)


    # Process all .dwg files in files\dwg_to_geojson
    dwg_dir = r'files\\dwg_to_geojson'
    for root, dirs, files in os.walk(dwg_dir):
        for file in files:
            if file.lower().endswith('.dwg'):
                dwg_file_path = os.path.join(root, file)
                if os.path.isfile(dwg_file_path):
                    # output_name = sanitize_output_name(os.path.relpath(dwg_file_path, start='files'))
                    rel_path = os.path.relpath(dwg_file_path, start='files')
                    output_name = os.path.join('files', 'outputs', rel_path).replace('.dwg', '.geojson')
                    # output_path = os.path.join('files', 'output', os.path.join('files', 'outputs', output_name))
                    geo_converter = GeoConverter()
                    geo_converter.convert_dwg_to_geojson(dwg_file_path, output_name)
if __name__ == "__main__":
    main()