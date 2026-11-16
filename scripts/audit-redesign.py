"""Compare generated pages with the content and links before the redesign."""

import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BASELINE = ROOT / "qa" / "redesign-baseline.json"


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def snapshot():
    pages = {}
    for path in sorted(DIST.rglob("index.html")):
        relative = path.relative_to(DIST).as_posix()
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for node in soup.select("script, style"):
            node.decompose()
        text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True)).strip()
        headings = [node.get_text(" ", strip=True) for node in soup.select("main h1, main h2, main h3")]
        links = sorted(node.get("href", "") for node in soup.select("a[href]"))
        images = sorted(node.get("src", "") for node in soup.select("img[src]"))
        frames = sorted(node.get("src", "") for node in soup.select("iframe[src]"))
        head = soup.head
        seo = {
            "title": head.title.get_text(strip=True) if head.title else "",
            "canonical": [node.get("href", "") for node in head.select('link[rel="canonical"]')],
            "meta": sorted([node.get("name", node.get("property", "")), node.get("content", "")] for node in head.select("meta[name], meta[property]")),
        }
        pages[relative] = {
            "text_hash": digest(text),
            "text_length": len(text),
            "headings": headings,
            "links": links,
            "images": images,
            "iframes": frames,
            "seo": seo,
        }
    return {
        "pages": pages,
        "sitemap_hash": digest((DIST / "sitemap.xml").read_text(encoding="utf-8")),
        "robots_hash": digest((DIST / "robots.txt").read_text(encoding="utf-8")),
    }


current = snapshot()
if sys.argv[1:] == ["--snapshot"]:
    BASELINE.parent.mkdir(exist_ok=True)
    BASELINE.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Inventoried {len(current['pages'])} pages in {BASELINE}")
elif sys.argv[1:] == ["--compare"]:
    original = json.loads(BASELINE.read_text(encoding="utf-8"))
    if original != current:
        differences = []
        for key in ("sitemap_hash", "robots_hash"):
            if original[key] != current[key]:
                differences.append(key)
        for page in sorted(set(original["pages"]) | set(current["pages"])):
            before = original["pages"].get(page, {})
            after = current["pages"].get(page, {})
            for key in sorted(set(before) | set(after)):
                old_value, new_value = before.get(key), after.get(key)
                if key == "seo" and old_value and new_value:
                    # Browser chrome color intentionally follows the visual palette.
                    old_value = {**old_value, "meta": [item for item in old_value["meta"] if item[0] != "theme-color"]}
                    new_value = {**new_value, "meta": [item for item in new_value["meta"] if item[0] != "theme-color"]}
                if old_value != new_value:
                    differences.append(f"{page}: {key}")
        if differences:
            raise SystemExit("Changed content or functionality:\n" + "\n".join(differences))
    print(f"Preserved content, links, images, SEO metadata (except theme-color), sitemap and robots across {len(current['pages'])} pages.")
else:
    raise SystemExit("Usage: python scripts/audit-redesign.py --snapshot|--compare")
