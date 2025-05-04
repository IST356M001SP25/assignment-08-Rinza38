'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
st.set_page_config(layout="wide")

# Load data functions
@st.cache_data
def load_top_locations():
    return pd.read_csv('./cache/top_locations.csv')

@st.cache_data
def load_tickets():
    return pd.read_csv('./cache/tickets_in_top_locations.csv')

def main():
    st.title('Syracuse Parking Ticket Analysis by Location')
    
    # Load data
    top_locs = load_top_locations()
    tickets = load_tickets()
    
    # Location selection
    selected_loc = st.selectbox(
        'Select a location:',
        options=top_locs['location'].sort_values(),
        index=0
    )
    
    # Filter tickets for selected location
    loc_tickets = tickets[tickets['location'] == selected_loc]
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total Tickets', len(loc_tickets))
    with col2:
        st.metric('Total Fines', f"${loc_tickets['amount'].sum():,.2f}")
    
    # Charts
    st.subheader('Ticket Distribution')
    
    # Day of week distribution
    fig1, ax1 = plt.subplots()
    sns.countplot(data=loc_tickets, x='dayofweek', ax=ax1, 
                 order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    ax1.set_title('Tickets by Day of Week')
    ax1.set_xlabel('Day of Week')
    ax1.set_ylabel('Count')
    
    # Hour of day distribution
    fig2, ax2 = plt.subplots()
    sns.countplot(data=loc_tickets, x='hourofday', ax=ax2)
    ax2.set_title('Tickets by Hour of Day')
    ax2.set_xlabel('Hour of Day (24h)')
    ax2.set_ylabel('Count')
    
    # Display charts in columns
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
    with col2:
        st.pyplot(fig2)
    
    # Map of selected location
    st.subheader('Location Map')
    loc_data = tickets[tickets['location'] == selected_loc].iloc[0]
    m = folium.Map(location=[loc_data['lat'], loc_data['lon']], zoom_start=17)
    folium.Marker(
        [loc_data['lat'], loc_data['lon']],
        tooltip=selected_loc
    ).add_to(m)
    folium_static(m)

if __name__ == '__main__':
    main()