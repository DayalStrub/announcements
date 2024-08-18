# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

# %%
df = pd.read_parquet("../data/files.parquet")

# %%
df_labels = pd.read_parquet("../data/labels.parquet")

# %%
df_labels.sort_values("company_1")

# %%
sorted([*list(df_labels["company_1"]), *df_labels["company_2"]])

# %%
# Count number of files per id
file_counts = df.groupby('id')['title'].count()

# Count number of ids with a certain number of files
id_counts = file_counts.value_counts()

# Sort the counts in descending order
id_counts = id_counts.sort_index(ascending=False)

# Print the counts
id_counts.tail(20)

# %%
file_counts.sort_values()

# %%
df.loc[df["id"]==586]

# %%
df_cases = pd.read_parquet("../data/cases.parquet")

# %%
df_cases.head()

# %%
df_cases.value_counts("market_sector")

# %%
df_cases.loc[df_cases["id"]==586]["link"].values

# %%
df.loc[file_counts <=5

# %%
df.loc[df["id"].isin(file_counts[file_counts<=5].reset_index()["id"]), :]

# %%
df_cases["year"] = df_cases["closed"].apply(lambda x: pd.to_datetime(x).year if x is not None else pd.NA)

# %%
df_cases.groupby("year")["title"].count()

# %%
df.merge(df_cases.loc[:, ["id", "year"]], how="inner").groupby("year")["title"].count()

# %%
