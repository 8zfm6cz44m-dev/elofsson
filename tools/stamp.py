#!/usr/bin/env python3
"""Skriver data/meta.json med aktuell tid (körs före varje commit)."""
import json, datetime, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / "data" / "meta.json"
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
p.write_text(json.dumps({"updated": now.isoformat().replace("+00:00", "Z")}, indent=1) + "\n")
print("Uppdateringstid:", now.isoformat())
