# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# # !pip install -e ../

# %%
from samruni.data import list_cases, collect_cases

# %%
import pandas as pd
from pathlib import Path

# %% [markdown]
# ## Old data
#
# TODO: If use a hash of case title as ID and Parquet datasets, then no need to read in old data to process new data

# %%
path_data = Path(__file__).resolve().parent.parent / "data"
df_cases = pd.read_parquet(path_data / "cases.parquet")
df_files = pd.read_parquet(path_data / "labels.parquet")

# %%
n_cases = int(df_cases["id"].max())

# %% [markdown]
# ## New cases

# %%
cases = list_cases()

# %%
# add index
for i in range(len(cases)):
    cases[i]["id"] = n_cases + i + 1

# %%
cases_updated, files = collect_cases(cases)

# %%
df_cases_new = pd.DataFrame(cases_updated)
df_cases_full = pd.concat([df_cases, df_cases_new])

# %%
df_files_new = pd.DataFrame(files)
df_files_full = pd.concat([df_files, df_files_new])

# %% [markdown]
# ## Update cases

# %%
df_cases_full.to_parquet("../data/cases.parquet")

# %%
df_files_full.to_parquet("../data/files.parquet")

# %%
