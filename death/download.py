from json import dump
from os import makedirs
import re
from typing import List
import mimetypes

from requests import get, post
from bs4 import BeautifulSoup

API_BASE = "http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G"

WWW_BASE = "https://www.scb.se"
BEFSTAT_PAGE = f"{WWW_BASE}/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/"

mimetypes.init()


def download_api(name, code: str, values: List[str]):
    resp = post(
        f"{API_BASE}/{name}",
        json={
            "query": [
                {
                    "code": code,
                    "selection": {"filter": "item", "values": values},
                }
            ],
            "response": {"format": "json-stat2"},
        },
    )

    resp.raise_for_status()

    with open(f"data/{name}.json", "wt", encoding="utf8") as f:
        dump(resp.json(), f, indent=4, ensure_ascii=False)


def download_prel():
    befstat_resp = get(f"{BEFSTAT_PAGE}")

    befstat_resp.raise_for_status()

    befstat_doc = BeautifulSoup(befstat_resp.text, "html.parser")

    href = befstat_doc.find(
        "a", href=True, text=re.compile("Preliminär statistik över döda")
    )["href"]

    xlsx_url = f"{WWW_BASE}{href}"

    xlsx_resp = get(xlsx_url)

    assert xlsx_resp.headers["Content-Type"] == mimetypes.types_map[".xlsx"]

    with open("data/prel-url", "wt") as f:
        f.write(xlsx_url)

    with open("data/prel.xlsx", "wb") as f:
        f.write(xlsx_resp.content)


makedirs("data", exist_ok=True)

download_api("BefUtvKon1749", "ContentsCode", ["000000LV", "0000001F"])
download_api("ManadBefStatRegion", "Forandringar", ["100", "130"])
download_prel()
