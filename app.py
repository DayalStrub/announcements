"""
Main page with charts showing trends in cases
"""

import altair as alt
import pandas as pd
from pathlib import Path
import streamlit as st

st.title("CMA Cases: Overview")

file_path = Path(__file__).resolve().parent

data = pd.read_csv(file_path.parent / "data/cases.csv")

# Compute the year from the date_closed variable
data['year'] = pd.to_datetime(data['date_closed']).dt.year

# Group the data by 'toh' and count the number of cases
grouped_data = data.groupby(["year",'toh']).size().reset_index(name='count')

# Plot the chart using Altair
chart = alt.Chart(data).mark_bar().encode(
    y='count()',
    x='year:O',
    color='toh',
    tooltip=["name", "toh", "year"]
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)