"""
Page for single case review
"""

# import importlib
# import sys

# # requests doesn't run in pyodide
# # if importlib.util.find_spec("pyodide") is not None:
# if hasattr(sys, 'platform') and sys.platform == 'emscripten':
#     # import micropip
#     # micropip.install('')
#     import pyodide_http
#     pyodide_http.patch_all()  # Patch all libraries

import base64
from itables.streamlit import interactive_table
import pandas as pd
from pathlib import Path
import requests
import streamlit as st

st.title("CMA Cases: Data")

path_data = Path(__file__).resolve().parent.parent.parent / "data"

# Cases

st.markdown("## All cases")

df_cases = pd.read_parquet(path_data / "cases.parquet")
df_labels = pd.read_parquet(path_data / "labels.parquet")

df_cases = df_cases.merge(df_labels, how="left")

interactive_table(df_cases, maxBytes=0)

# Single Case

st.markdown("## Case information")

selected_case = st.selectbox("Select case", df_cases["title"].sort_values())
selected_case_id = df_cases.loc[df_cases["title"] == selected_case, "id"].item()
selected_case_toh = df_cases.loc[df_cases["title"] == selected_case, "concern"].item()


def update_toh(feedback):
    # TODO dicretly create PR?
    pass


col1, col2, col3 = st.columns([8, 1, 1])
with col1:
    st.markdown(f"Theory of harm type: **{selected_case_toh}**")
with col2:
    st.button(":thumbsup:", on_click=update_toh, args=("Positive",), key="thumbsup")
with col3:
    st.button(":thumbsdown:", on_click=update_toh, args=("Negative",), key="thumbsdown")

## Files

df_files = pd.read_parquet(path_data / "files.parquet")

df_files_filtered = df_files.loc[df_files["id"] == selected_case_id]

selected_file = st.selectbox("Select file", df_files_filtered["title"].sort_values())

url = df_files_filtered.loc[df_files_filtered["title"] == selected_file, "link"].values[
    0
]

response = requests.get(url)
bytes_data = response.content
base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
