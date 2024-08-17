import base64
import pandas as pd
import requests
import streamlit as st


st.title("CMA Cases: Data")

from pathlib import Path

file_path = Path(__file__).resolve().parent

# Cases

st.markdown("## All cases")

df_cases = pd.read_csv(file_path.parent.parent / "data/cases.csv")

st.dataframe(df_cases)

# Case

st.markdown("## Case information")

selected_case = st.selectbox("Select case", df_cases["name"].sort_values())
selected_case_id = df_cases.loc[df_cases["name"] == selected_case, "id"].item()
selected_case_toh = df_cases.loc[df_cases["name"] == selected_case, "toh"].item()

def update_toh(feedback):
    # TODO
    pass

col1, col2, col3 = st.columns([8,1,1])
with col1:
    st.markdown(f"Theory of harm type: **{selected_case_toh}**")
with col2:
    st.button(':thumbsup:', on_click=update_toh, args=('Positive',), key='thumbsup')
with col3:
    st.button(':thumbsdown:', on_click=update_toh, args=('Negative',), key='thumbsdown')

## Files

df_files = pd.read_csv(file_path.parent.parent / "data/files.csv")

df_files_filtered = df_files.loc[df_files["id"] == selected_case_id]

selected_file = st.selectbox("Select file", df_files_filtered["name"].sort_values())

# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

url = df_files_filtered.loc[df_files_filtered["name"] == selected_file, "url"].values[0]

response = requests.get(url)
bytes_data = response.content
base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
