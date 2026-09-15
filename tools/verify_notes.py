"""Kontrollerar att data/notes.json innehåller exakt samma text som den
arkiverade exporten (blanksteg ignoreras). Kör: python3 tools/verify_notes.py"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parent.parent
s = BeautifulSoup((ROOT/"arkiv/Slakttrad_export_2026-08-25.html").read_text(encoding="utf-8"), "html.parser")
w = s.select_one("section.notes-wrap")
for x in w.select(".toolbar,h2"): x.decompose()
a = re.sub(r"\s+", "", w.get_text(" "))
d = json.loads((ROOT/"data/notes.json").read_text(encoding="utf-8"))
LAB = {"master": "Släktforskningsmaster", "logg": "Forskningslogg", "bild": "Bildregister"}
R = {"strong": "KANDIDATVERIFIERAD", "verified": "VERIFIERAD", "candidate": "KANDIDAT", "excluded": "UTESLUTEN"}
parts, prev = [], None
for sec in d["sections"]:
    if sec["doc"] != prev: parts.append(LAB[sec["doc"]]); prev = sec["doc"]
    parts.append(sec["title"])
    for it in sec["items"]:
        if "table" in it: parts += [c for r in it["table"] for c in r]
        else: parts.append(re.sub(r"\{\{(\w+)\}\}", lambda m: R[m.group(1)], it["t"]))
b = re.sub(r"\s+", "", " ".join(parts))
print("OK – ingen text saknas" if a == b else "FEL – texten skiljer sig", len(a), len(b))
sys.exit(0 if a == b else 1)
