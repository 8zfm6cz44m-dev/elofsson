"""Extraherar Master, Forskningslogg och Bildregister ur den arkiverade
HTML-exporten till data/notes.json.  Kör från repo-roten:
    python3 tools/extract_notes.py
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "arkiv" / "Slakttrad_export_2026-08-25.html"
OUT = ROOT / "data" / "notes.json"
DOCS = {"Släktforskningsmaster": "master", "Forskningslogg": "logg", "Bildregister": "bild"}

MAP = {"green": "verified", "yellow": "candidate", "amber": "candidate", "red": "excluded"}
# I originalet betyder KANDIDAT+VERIFIERAD bredvid varandra "mycket stark kandidat" -> {{strong}}

def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    wrap = soup.select_one("section.notes-wrap")
    doc, sections, n = None, [], 0
    for el in wrap.children:
        if not isinstance(el, Tag): continue
        if el.name == "h3":
            doc = DOCS[el.get_text(strip=True)]; continue
        if el.name != "details": continue
        n += 1
        title = el.summary.get_text(" ", strip=True)
        items = []
        for child in el.select_one("div.notes").children:
            if not isinstance(child, Tag): continue
            if child.name == "p":
                # Statusmärken behålls på sin plats i texten som {{status}}.
                for s in child.select("span.tag"):
                    s.replace_with("\u27e6" + [c for c in s.get("class", []) if c != "tag"][0] + "\u27e7")
                text = re.sub(r"[ \t]+", " ", child.get_text("")).strip()
                text = text.replace("\u27e6yellow\u27e7\u27e6green\u27e7", "{{strong}}")
                for k, v in MAP.items():
                    text = text.replace("\u27e6" + k + "\u27e7", "{{" + v + "}}")
                item = {"t": text}
                found = re.findall(r"\{\{(\w+)\}\}", text)
                if found: item["s"] = found[0]
                items.append(item)
            elif child.name == "table":
                items.append({"table": [[td.get_text(" ", strip=True) for td in tr.find_all("td")] for tr in child.find_all("tr")]})
            else:
                raise SystemExit(f"Okänt element {child.name} i {title}")
        sections.append({"id": f"{doc}-{n:03d}", "doc": doc, "title": title, "items": items})
    OUT.write_text(json.dumps({"source": SRC.name, "sections": sections}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(sections), "avsnitt,", sum(len(s["items"]) for s in sections), "poster")

if __name__ == "__main__":
    main()
