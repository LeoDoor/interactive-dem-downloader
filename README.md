# Interactive DEM Downloader

A Streamlit web application for downloading Digital Elevation Model (DEM) data from OpenTopography with both manual coordinate entry and interactive map selection.

## Features

- **Manual Coordinate Entry**: Enter bounding box coordinates directly
- **Interactive Map Selection**: Draw rectangles on an interactive map to select your area of interest
- **Real-time Preview**: Visualize your selected area before downloading
- **Automatic Download**: Downloads high-resolution SRTM data as GeoTIFF files

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/interactive-dem-downloader.git
cd interactive-dem-downloader
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Create a `.env` file in the project directory
   - Add your OpenTopography API key:
   ```
   OPENTOPOGRAPHY_API_KEY=your_api_key_here
   ```
   - Get a free API key from [OpenTopography](https://portal.opentopography.org/requestService)

4. Run the application:
```bash
streamlit run DEM_python.py
```

## Usage

### Method 1: Manual Coordinates
1. Enter the bounding box coordinates in the sidebar
2. Click "Show Bounds" to preview your selection
3. Click "Download DEM" to download the data

### Method 2: Interactive Map
1. Switch to the "Interactive Map Selection" tab
2. Use the rectangle drawing tool to select your area of interest
3. The coordinates will be automatically extracted
4. Click "Download DEM" to download the data

## API Information

This application uses the [OpenTopography Global DEM API](https://portal.opentopography.org/apidocs/) to download SRTM GL3 (30m resolution) data.

## License

This project is licensed under the MIT License.

## Credits

- **Original concept and basic implementation**: [Mining Geologist YouTube Channel](https://www.youtube.com/@MiningGeologist)
- **Interactive map functionality and UI improvements**: Enhanced by [Your Name]
- **Data source**: [OpenTopography](https://portal.opentopography.org/)

## Acknowledgments

- Special thanks to the Mining Geologist YouTube channel for the original tutorial and code foundation
- OpenTopography for providing free access to global DEM data
- The Streamlit and Folium communities for excellent documentation and examples
