## Little project to create an interactive Streamlit dashboard with data from providers who have been suspended by the California Department of Health Care Services.

View the Streamlit app here: https://chhs-suspended-providers.streamlit.app/

### Process
The original dataset downloaded from the state agency's open data portal (https://data.chhs.ca.gov/dataset/provider-suspended-and-ineligible-list-s-i-list) is the 'provider-suspended-and-ineligible-list-s-i-list.csv' file, which was cleaned by the suspended_provider_list_cleaning.ipynb Jupyter Notebook. Latitude and longitude coordinates based on zip code were merged into the datset from the zip_to_lat_lon_North America.csv file, resulting in two final datasets (banned_providers_final.csv and banned_providers_merged_lat.csv) that are read into the Streamlit app Python script streamlit-provider-fraud.py.

Carried out to showcase some of my skills for an interview for a data analyst position tasked with uncovering provider fraud with the California Department of Health Care Services. 

![image](https://github.com/rileyschenck/CHHS/assets/124864861/6e584cb5-f0ee-49c9-a620-4949018618e1)
![image](https://github.com/rileyschenck/CHHS/assets/124864861/f4ed9602-94a0-4bb6-a829-c3de9e3eda41)

