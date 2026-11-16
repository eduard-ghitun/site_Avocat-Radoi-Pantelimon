"""Snapshot public service descriptions from avocatpantelimonradoi.ro."""

import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "accidente-rutiere", "drept-civil", "drept-imobiliar", "dreptul-familiei",
    "drept-administrativ", "zboruri-intarziate", "drept-penal",
    "drept-comercial", "dreptul-muncii",
]

data = {}
for slug in SLUGS:
    url = f"https://avocatpantelimonradoi.ro/services/{slug}/"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    block = soup.select_one(".attorney_desc_box")
    if block is None:
        raise RuntimeError(f"Service content not found: {url}")
    for unwanted in block.select("script, style, iframe, form, nav, .attorney_feature-box"):
        unwanted.decompose()
    data[slug] = {"url": url, "html": block.decode_contents().strip()}
    print(f"Captured {slug}: {len(data[slug]['html'])} characters")

(ROOT / "src" / "service-content.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
)
