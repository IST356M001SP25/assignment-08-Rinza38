'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('./cache/top_locations_mappable.csv')

def main():
    st.title('Syracuse Parking Ticket Hotspots')
    
    # Load the data
    data = load_data()
    
    # Create the map
    m = folium.Map(location=CUSE, zoom_start=ZOOM)
    
    # Add points to the map
    for idx, row in data.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=row['amount']/2,  # Scale the circle size
            color='red',
            fill=True,
            fill_opacity=0.6,
            tooltip=f"{row['location']}: ${row['amount']:,.2f}"
        ).add_to(m)
    
    # Display the map
    sf.folium_static(m)

if __name__ == '__main__':
    main()