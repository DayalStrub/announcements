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
from anthropic import AnthropicBedrock
import boto3
import fitz  # PyMuPDF
import instructor
import json
import numpy as np
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, field_validator
from tqdm.notebook import tqdm
from typing import List
import base64
import requests


# %%
# calude has a 200k context window
def return_text(urls, max_length=200_000):
    txt = ""
    for url in urls:
        response = requests.get(url)
        bytes_data = response.content
        try:
            document = fitz.Document(stream=bytes_data)
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text = page.get_text()
                txt += text
                if len(txt) > max_length:
                    return ""  # TODO decide what to do with "long cases"
        except:
            return ""  # TODO handle PDF errors
    return txt


# %%
class Merger(BaseModel):
    company_1: str
    company_2: str
    concern: str

    @field_validator("concern")
    @classmethod
    def check_allowed_values(cls, v):
        allowed_concerns = ["Competitors", "Consumers"]
        if v not in allowed_concerns:
            raise ValueError(f"Value must be one of {allowed_concerns}")
        return v


# %%
system_prompt = """
You are an AI assistant that helps competition lawyers to review and classify announcements about reviews of mergers between two companies.
You are an expert in UK merger control and consumer protection regulation. 
You can distinguish between mergers announcements where the concern is about:
* Competitors: the impact on competitors of the merging companies; 
* Consumers: the impacts to clients of the merging companies or consumers, even if indirectly, such as from increases in price, reduction in choice, or reduction in quality. 
"""


def generate_user_prompt(text):
    prompt = f"""
    Extract the company names.
    Classify the merger announcement concern using the categories: 
    * Competitors
    * Consumers
    Return only one label.
    Return an empty label if the merger concern is neither.

    Here is the merger announcement.

    <announcement>
    {text}
    </announcement>
    """
    # Please output the category label in <output></output> tags in your <response>.
    return prompt


# assistant_prompt="<response><output>"


# %%
def label_case(system_prompt, user_prompt):
    # note that client.chat.completions.create will also work
    resp = client.messages.create(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        response_model=Merger,
        max_retries=1,
    )
    _ = resp.__dict__.pop("_raw_response")
    return resp.__dict__


# %%
# client = boto3.client('bedrock', region_name="eu-west-2")
# response = client.list_foundation_models()
# models = response.get('modelSummaries', [])
# for model in models:
#     print(f"Model ID: {model['modelId']}, Model Name: {model['modelName']}")

# %%
file_path = Path("").resolve().parent / "data"

df_cases = pd.read_parquet(file_path / "cases.parquet")

df_files = pd.read_parquet(file_path / "files.parquet")

# %%
# filter to cases with less than 6 files - some have hundreds
small_cases = (
    df_files["id"].value_counts()[df_files["id"].value_counts() <= 5].index.values
)

# %%
df_files_filtered = df_files.loc[df_files["id"].isin(small_cases)]

# %%
client = instructor.from_anthropic(AnthropicBedrock())

# %%
import time

# %%
labels = []
for i in tqdm(small_cases):
    time.sleep(1)
    # print("Case:", i)
    urls = df_files.loc[df_files["id"] == i, "link"].to_list()
    text = return_text(urls)
    if len(text) == 0:
        # print("Too long, or errored")
        continue
    # print(len(text))
    user_prompt = generate_user_prompt(text)
    label = label_case(system_prompt, user_prompt)
    label["id"] = int(i)
    label["n_files"] = len(urls)
    label["n_chars"] = len(text)
    labels.append(label)
    # print("Labelled")


# %%
df_labels = pd.DataFrame(labels)

# %%
df_labels.head()

# %%
df_labels = df_labels.loc[df_labels["concern"].isin(["Competitors", "Consumers"]), :]

# %%
df_labels.value_counts("concern")

# %%
df_labels.to_parquet(file_path / "labels.parquet")

# %%
