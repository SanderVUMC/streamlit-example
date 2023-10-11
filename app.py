import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Set page title and icon
from st_pages import Page, show_pages, add_page_title


st.set_page_config(
    page_title="Parcel Review Tool",
    page_icon="👋",
    layout="wide",
)

show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("pages/parcel_review.py", "Parcel Review","👉"),
        
    ]
)


st.title("Parcel Review Tool Homepage")

st.write("""
## Overview
The Parcel Review Tool homepage allows users to lookup details on a specific parcel ID, view any associated appeals data, analyze value changes compared to the neighborhood, and find similar parcels in the same neighborhood.
""")

st.write("""
## Data
The tool loads the following data:
""")

st.write("- `parcels` - Contains details on property parcels such as address, neighborhood, beds/baths, square footage, etc.")
st.write("- `appeals` - Contains data on property assessment appeals, including parcel ID, appeal reason, and case status.")
st.write("- `triennial` - Contains assessed values and value changes for the 2022 and 2023 tax years.")

st.write("""
## Usage
""")

st.write("""
### Selecting a Parcel ID  
On the left sidebar, select either "Input Parcel ID" or "Appealed Parcels":
""")

st.write("- **Input Parcel ID**: Manually enter a parcel ID number to lookup")
st.write("- **Appealed Parcels**: Select from a dropdown of parcel IDs that have associated appeal cases. This filters specifically for parcels with appeals cases marked as \"In Review\".")

st.write("Once a parcel ID is selected, details on that parcel will be displayed.")

st.write("""
### Viewing Parcel Details
The parcel details section shows information retrieved from the `parcels` dataframe for that specific parcel ID. This includes fields like:
""")

st.write("- PARID")
st.write("- Year Built")  
st.write("- Beds")
st.write("- Baths")
st.write("- Square Feet")
st.write("- Grade")
st.write("- Exterior Walls")
st.write("- and more...")

st.write("Any associated appeal cases for that parcel ID are also shown under \"Appeal Information\" if available.")


st.write("""
### Analyzing Value Changes
The value change analysis compares the current 2023 value to the prior 2022 value and calculates the net change, percent change, and estimated tax change per year.

This is also compared to summary statistics on value changes across the entire neighborhood, such as minimum, maximum, median, and average changes. A histogram visualizes the distribution of percent changes in the neighborhood with the current parcel's change highlighted.
""")

st.write("""
### Finding Similar Parcels
The "Find Similar Parcels" section allows the user to define criteria like year built, beds, baths, square feet, grade, and exterior walls to search for similar parcels within the same neighborhood.  

Sliders and dropdowns let the user refine the search criteria. Matching parcels are displayed in a table with core fields like year built, style, beds/baths, sale price, total value, and more. The target parcel is shown first, followed by the matched parcels.
""")

st.write("""
## Interpreting Results
The tool provides a quick way to see how a specific parcel compares to the broader neighborhood in terms of value changes. The similar parcels table helps identify other properties that may warrant closer comparison for appeals or analysis. Insights from the tool can help guide next steps and priorities for further investigation.
""")

st.write("""
---
**Last Data Update:** October 08, 2023

**Last Code Update:** October 10, 2023
""")