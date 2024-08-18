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
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
import pandas as pd
import requests
from tqdm.notebook import tqdm
from typing import List


# %%
def get_soup(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# %%
def get_cases(soup):
    cases_list = soup.find("ul", class_="gem-c-document-list")
    if cases_list:
        for li in cases_list.find_all("li"):
            a_tag = li.find("a")
            if a_tag:
                title_and_url = {
                    "title": a_tag.get_text(strip=True),
                    "link": f"https://www.gov.uk{a_tag['href']}",
                }
                # cases defined in script/loop
                cases.append(title_and_url)
    pass


# %%
@dataclass
class Case:
    url: str = ""
    files: List[str] = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        soup = self._get_soup()
        self._extract_attributes(soup)
        self._extract_files(soup)

    def _get_soup(self) -> BeautifulSoup:
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def _extract_files(self, soup) -> None:
        pdf_links = []
        for a_tag in soup.find_all("a", href=True):
            if a_tag["href"].endswith(".pdf"):
                title_and_url = {
                    "title": a_tag.get_text(strip=True),
                    "link": a_tag["href"],
                }
                pdf_links.append(title_and_url)
        self.files = pdf_links

    def _extract_attributes(self, soup) -> None:
        dl_element = soup.find("dl", class_="app-c-important-metadata__list")
        metadata_dict = {}
        if dl_element:
            dt_elements = dl_element.find_all(
                "dt", class_="app-c-important-metadata__term"
            )
            dd_elements = dl_element.find_all(
                "dd", class_="app-c-important-metadata__definition"
            )
            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.get_text(strip=True).rstrip(":").lower().replace(" ", "_")
                value = dd.get_text(strip=True)
                metadata_dict[key] = value
        self.meta = metadata_dict


# %% [markdown]
# ## Parameters

# %%
url = "https://www.gov.uk/cma-cases?case_state%5B%5D=closed&case_type%5B%5D=mergers"

# %% [markdown]
# ## Get number of pages

# %%
soup = get_soup(url)

# %%
span_element = soup.find("span", class_="govuk-pagination__link-label")
if span_element:
    text = span_element.get_text(strip=True)
    parts = text.split(" of ")
    if len(parts) == 2:
        num_pages = int(parts[1])
    else:
        raise ("Text format is not as expected.")
num_pages

# %% [markdown]
# ## Get cases

# %%
cases = []

# %% [markdown]
# ### Page 1

# %%
get_cases(soup)

# %% [markdown]
# ### Other pages

# %%
for i in range(2, num_pages + 1):
    url_i = f"{url}&page={i}"
    soup = get_soup(url_i)
    get_cases(soup)

# %%
len(cases)

# %%
for index, item in enumerate(cases):
    item["id"] = index

# %% [markdown]
# ## Get case info

# %%
files = []

for c in tqdm(cases):
    # print(c)
    case = Case(c["link"])
    cases[c["id"]].update(case.meta)
    for f in case.files:
        f["id"] = c["id"]
        files.append(f)

# %%
df_cases = pd.DataFrame(cases)
df_cases.head()

# %%
len(df_cases)

# %%
df_files = pd.DataFrame(files)
df_files.head()

# %%
len(df_files)

# %% [markdown]
# ## Save data

# %%
df_cases.to_parquet("../data/cases.parquet")

# %%
df_files.to_parquet("../data/files.parquet")

# %%
