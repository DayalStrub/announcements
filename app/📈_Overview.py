"""
Main page with charts showing trends in cases
"""

import altair as alt
import pandas as pd
from pathlib import Path
import streamlit as st

st.set_page_config(layout="wide")

st.title("CMA Cases: Overview")

path_data = Path(__file__).resolve().parent.parent / "data"

# prepare data
data_cases = pd.read_parquet(path_data / "cases.parquet")
data_labels = pd.read_parquet(path_data / "labels.parquet")

data = data_cases.merge(data_labels, how="left")

data["year"] = pd.to_datetime(data["closed"]).dt.year

grouping = st.selectbox("Select grouping", ["concern", "market_sector"])

# plot counts over time by toh
chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        y="count()",
        x="year:O",
        color=grouping,
        tooltip=["title", "concern", "market_sector", "year"],
    )
    .properties(height=700)
    .interactive()
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
