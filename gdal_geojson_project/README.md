# gdal_geojson_project

## Overview
This project provides functionality to convert DWG and GDB files into GeoJSON format using the `GeoConverter` class. It encapsulates methods for loading files, exporting to DXF, and converting to GeoJSON.

## Project Structure
```
gdal_geojson_project
├── src
│   ├── geo_converter.py
│   └── examples.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gdal_geojson_project
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the examples provided in the project, execute the `examples.py` script:

```
python src/examples.py
```

This will demonstrate the conversion processes from DWG and GDB files to GeoJSON format.

## Dependencies
- osgeo
- aspose-cad (if applicable)

Make sure to have the necessary libraries installed as specified in `requirements.txt`.