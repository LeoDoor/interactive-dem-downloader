import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Interactive DEM Downloader")

# Create two tabs - one for manual input, one for map selection
tab1, tab2 = st.tabs(["Manual Coordinates", "Interactive Map Selection"])

with tab1:
    st.header("Enter Coordinates Manually")
    
    # Sidebar for input controls
    with st.sidebar:
        south_input = st.text_input('South Boundary', '40.0')
        north_input = st.text_input('North Boundary', '41.0')
        west_input = st.text_input('West Boundary', '-74.0')
        east_input = st.text_input('East Boundary', '-73.0')
        show_bounds_clicked = st.button('Show Bounds (Manual)')
    
    # Main area for map display
    if show_bounds_clicked:
        try:
            south = float(south_input)
            north = float(north_input)
            west = float(west_input)
            east = float(east_input)
            
            # Create corner points for visualization
            corner_points = [
                [south, west], [south, east], 
                [north, east], [north, west], 
                [south, west]  # Close the rectangle
            ]
            
            df = pd.DataFrame({
                'lat': [point[0] for point in corner_points[:-1]], 
                'lon': [point[1] for point in corner_points[:-1]]
            })
            
            st.subheader("Selected Area Preview")
            st.map(df)
            
            # Store coordinates in session state
            st.session_state.coords = {
                'south': south, 'north': north, 
                'west': west, 'east': east
            }
            
            # Show coordinate summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("South", f"{south:.4f}")
            with col2:
                st.metric("North", f"{north:.4f}")
            with col3:
                st.metric("West", f"{west:.4f}")
            with col4:
                st.metric("East", f"{east:.4f}")
                
        except ValueError:
            st.error("Please enter valid numeric coordinates")

with tab2:
    st.header("Select Area on Interactive Map")
    
    # Create a folium map centered on a default location
    center_lat = 40.5
    center_lon = -73.5
    
    # Create the map
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=8,
        tiles="OpenStreetMap"
    )
    
    # Add drawing tools - specifically rectangle
    draw = folium.plugins.Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "polygon": False,
            "circle": False,
            "marker": False,
            "circlemarker": False,
            "rectangle": True  # Only allow rectangles
        }
    )
    draw.add_to(m)
    
    # Display the map and capture user interactions
    map_data = st_folium(m, width=700, height=500, returned_objects=["last_object_clicked_tooltip", "all_drawings"])
    
    # Process the drawn rectangle
    if map_data['all_drawings']:
        if len(map_data['all_drawings']) > 0:
            # Get the last drawn rectangle
            last_drawing = map_data['all_drawings'][-1]
            
            if last_drawing['geometry']['type'] == 'Polygon':
                coords = last_drawing['geometry']['coordinates'][0]
                
                # Extract bounding box from the rectangle coordinates
                lats = [point[1] for point in coords]
                lons = [point[0] for point in coords]
                
                south = min(lats)
                north = max(lats)
                west = min(lons)
                east = max(lons)
                
                # Display the extracted coordinates
                st.success("Rectangle drawn! Extracted coordinates:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("South", f"{south:.4f}")
                with col2:
                    st.metric("North", f"{north:.4f}")
                with col3:
                    st.metric("West", f"{west:.4f}")
                with col4:
                    st.metric("East", f"{east:.4f}")
                
                # Store coordinates in session state
                st.session_state.coords = {
                    'south': south, 'north': north, 
                    'west': west, 'east': east
                }

# Download section (works with coordinates from either method)
st.header("Download DEM")

if 'coords' in st.session_state:
    coords = st.session_state.coords
    st.info(f"Current selection: S={coords['south']:.4f}, N={coords['north']:.4f}, W={coords['west']:.4f}, E={coords['east']:.4f}")
    
    if st.button('Download DEM'):
        try:
            # Get the directory where your script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'raster.tif')
            
            # Get API key from environment variable
            # Get API key from environment variable
            api_key = os.getenv('OPENTOPOGRAPHY_API_KEY')
            if not api_key:
                st.error("API key not found. Please set OPENTOPOGRAPHY_API_KEY in your .env file.")
                st.stop()
            
            # Construct the API URL
            url = f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={coords['south']}&north={coords['north']}&west={coords['west']}&east={coords['east']}&outputFormat=GTiff&API_Key={api_key}"
            
            # Show progress
            with st.spinner('Downloading DEM data...'):
                response = requests.get(url)
                
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    st.success(f'Download complete! The DEM file has been saved as: {file_path}')
                    st.info(f"File size: {len(response.content) / 1024:.1f} KB")
                else:
                    st.error(f"Download failed. Status code: {response.status_code}")
                    
        except Exception as e:
            st.error(f"Error during download: {str(e)}")
else:
    st.warning("Please select an area using either manual coordinates or the interactive map first.")