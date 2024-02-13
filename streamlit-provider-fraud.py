#GO TO POWERSHELL AND RUN COMMAND:  streamlit run data/CHHS_data/streamlit-provider-fraud.py
import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import folium_static



# Load data

df = pd.read_csv('banned_providers_final.csv')
merged_df = pd.read_csv('banned_providers_merged_lat.csv')

# Data preprocessing and visualization
st.title('Interactive Dashboard of Suspended and Ineligible California DHCS Providers')

# Display a slider for selecting a year range
year_range = st.slider(
    'Select a range of years',
    min_value=int(min(df['Year'].min(), merged_df['Year'].min())),
    max_value=int(max(df['Year'].max(), merged_df['Year'].max())),
    value=(1995, int(max(df['Year'].max(), merged_df['Year'].max())))  # Default range
)

# Filter both DataFrames based on the selected year range
df = df[df['Year'].between(year_range[0], year_range[1])]
merged_df = merged_df[merged_df['Year'].between(year_range[0], year_range[1])]


# Dynamically construct markdown text
markdown_text = f"""
## Suspended/Ineligible Providers by year of suspension ({year_range[0]} to {year_range[1]})

The line chart below shows the total counts of providers suspended by the California Department of Health Care Services providers by year of suspension. 

Use the slider above to adjust the range of years displayed.
"""

# Display the dynamic markdown
st.markdown(markdown_text)

yearly_counts = df.groupby('Year').size().reset_index(name='Total Counts')

# Altair chart for yearly counts
yearly_counts_chart = alt.Chart(yearly_counts).mark_line(point=True).encode(
    x=alt.X('Year:N', axis=alt.Axis(title='Year')),
    y=alt.Y('Total Counts:Q', axis=alt.Axis(title='Total Counts')),
    tooltip=['Year:N', 'Total Counts:Q']
).properties(
    width=800,
    height=400,
)

st.altair_chart(yearly_counts_chart, use_container_width=True)


# Dynamically construct markdown text
markdown_text = f"""
## Top Suspended/Ineligible Provider Types ({year_range[0]} to {year_range[1]})

This bar chart ranks the top suspended/ineligible provider types over the year range indicated above.

Change the number of provider types to compare by entering a new number in the field below, which will automatically update the following line chart.
"""

# Display the dynamic markdown
st.markdown(markdown_text)

# Display a numeric input for user to specify the number of top provider types
num_provider_types = st.number_input('Select the number of top provider types to display', min_value=1, value=10, step=1)

# Count the occurrences of each provider type and get the top 15
top_provider_types = df['Provider Type'].value_counts().reset_index().head(num_provider_types)
top_provider_types.columns = ['Provider Type', 'Counts']

# Create an Altair bar chart
provider_types_bar = alt.Chart(top_provider_types).mark_bar().encode(
    x=alt.X('Counts:Q', title='Counts'),
    y=alt.Y('Provider Type:N', title='Provider Type', sort='-x'),  # Sort bars by their counts
    color=alt.Color('Provider Type:N', legend=None),  # Color bars by provider type without a separate legend
    tooltip=['Provider Type:N', 'Counts:Q']
).properties(
    width=600,
    height=600,
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

st.altair_chart(provider_types_bar, use_container_width=True)


# Dynamically construct markdown text
markdown_text = f"""
    ## Interactive Comparison of Top {num_provider_types} Suspended/Ineligible Provider Types ({year_range[0]} to {year_range[1]})
    
    Remember, you can edit the number of provider types using the field above the previous bar chart.
    
    Hover over a line to view the counts for each provider type by year. Zoom in and out with your mouse's scroll wheel.
"""

# Display the dynamic markdown
st.markdown(markdown_text)


# Count the occurrences of each provider type and get the top N based on user input
top_provider_types = df['Provider Type'].value_counts().head(num_provider_types).index

# Filter the DataFrame for only the top N provider types
filtered_df = df[df['Provider Type'].isin(top_provider_types)]

# Aggregate data by year and provider type, then reset index to flatten for Altair
yearly_data = filtered_df.groupby(['Year', 'Provider Type']).size().reset_index(name='Counts')


# Create an interactive line chart
highlight = alt.selection(type='single', on='mouseover', fields=['Provider Type'], nearest=True)
base = alt.Chart(yearly_data).encode(
    x='Year:O',
    y='Counts:Q',
    color=alt.Color('Provider Type:N', legend = None),
    tooltip=['Year:O', 'Provider Type:N', 'Counts:Q']
).properties(
    width=800,
    height=400
).interactive()

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

points = base.mark_point().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
)

# Combine the charts
provider_types_line = lines + points

st.altair_chart(provider_types_line, use_container_width=True)


# Dynamically construct markdown text
markdown_text = f"""
    ##  Geographic Distribution of Banned/Suspended Providers ({year_range[0]} to {year_range[1]})
    The map below shows the geographical distribution of banned providers by zip code, 
    with circle sizes representing the count of banned providers for each zip code. 
    
    Zoom in and out with your mouse's scroll wheel, and click and drag to change location.
"""

# Display the dynamic markdown
st.markdown(markdown_text)

# Aggregate counts by zip code
zip_counts = merged_df.groupby(['postal code', 'province_or_county', 'latitude', 'longitude']).size().reset_index(name='counts')

# Folium map for California zip codes
ca_map = folium.Map(location=[36.7783, -119.4179], zoom_start=7, tiles='cartodbpositron')

# Add points for each zip code
for idx, row in zip_counts.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['counts'] * 0.5,
        color='blue',
        weight=0,
        fill=True,
        fill_color='blue',
        fill_opacity=0.2,
        tooltip=f"Postal Code: {row['postal code']}<br>City: {row['province_or_county']}<br>Counts: {row['counts']}"
    ).add_to(ca_map)

# Display the map in Streamlit
folium_static(ca_map)