import pandas as pd
import streamlit as st 


def top_locations(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    """Return a dataframe of locations with $1,000 or more in total fines."""
    # Group by location and sum the fine amounts
    location_totals = violations_df.groupby('location')['amount'].sum().reset_index()
    # Filter for locations meeting the threshold
    top_locs = location_totals[location_totals['amount'] >= threshold]
    return top_locs.sort_values('amount', ascending=False)


def top_locations_mappable(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    """Return top locations with their coordinates and total fine amounts."""
    # Get the top locations
    top_locs = top_locations(violations_df, threshold)
    
    # Get the first occurrence of each location's coordinates
    location_coords = violations_df.drop_duplicates('location')[['location', 'lat', 'lon']]
    
    # Merge to add coordinates to the top locations
    mappable = pd.merge(top_locs, location_coords, on='location', how='left')
    return mappable


def tickets_in_top_locations(violations_df: pd.DataFrame, threshold=1000) -> pd.DataFrame:
    """Return tickets issued in top locations (those with $1,000+ in fines)."""
    # Get the list of top locations
    top_locs = top_locations(violations_df, threshold)['location']
    
    # Filter original dataframe for tickets in these locations
    return violations_df[violations_df['location'].isin(top_locs)]


if __name__ == '__main__':
    # Read the input data
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    
    # Generate and save the output files
    top_locs = top_locations(violations_df)
    top_locs.to_csv('./cache/top_locations.csv', index=False)
    
    top_mappable = top_locations_mappable(violations_df)
    top_mappable.to_csv('./cache/top_locations_mappable.csv', index=False)
    
    tickets_top = tickets_in_top_locations(violations_df)
    tickets_top.to_csv('./cache/tickets_in_top_locations.csv', index=False)