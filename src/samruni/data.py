"""
Model to collect data from CMA website
"""

from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import feedparser
import pandas as pd
import requests
from typing import List


def list_cases():
    "Get yesterday's cases from RSS feed"
    # TODO move URL to config file?
    url = "https://www.gov.uk/cma-cases.atom?case_type%5B%5D=mergers&case_state%5B%5D=closed"
    response = feedparser.parse(url)
    date_updated = datetime.strptime(
        response["feed"]["updated"], "%Y-%m-%dT%H:%M:%S%z"
    ).date()
    date_yesterday = datetime.now().date() - timedelta(days=1)
    cases = []
    if date_updated >= date_yesterday:
        for e in response.entries:
            date_case_update = datetime.strptime(
                e.updated, "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            if date_case_update > date_yesterday:
                tmp = {
                    "title": e.title,
                    # "date_updated": date_case_update,
                    "link": e.link,
                }
                cases.append(tmp)
    return cases


def collect_cases(cases):
    "Collect data about cases"
    cases_updated = cases.copy()
    files = []
    for i, c in enumerate(cases_updated):
        case = Case(c["link"])
        cases_updated[i].update(case.meta)
        for f in case.files:
            f["id"] = c["id"]
            files.append(f)
    return cases_updated, files


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
