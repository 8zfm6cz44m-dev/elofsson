#!/usr/bin/env python3
"""Skriver data/meta.json (tid + status för validering och GEDCOM-test). Körs före varje commit."""
import json, datetime, pathlib, subprocess, shutil, re
root = pathlib.Path(__file__).resolve().parent.parent
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
v = subprocess.run(["python3", str(root / "tools" / "validate.py")], capture_output=True, text=True, cwd=root)
meta = {"updated": now.isoformat().replace("+00:00", "Z"), "validate": "OK" if v.returncode == 0 and v.stdout.strip().startswith("OK") else "FEL"}
m = re.search(r"(\d+) personer, (\d+) relationer", v.stdout)
if m: meta["persons"], meta["relations"] = int(m.group(1)), int(m.group(2))
if shutil.which("node"):
    g = subprocess.run(["node", str(root / "tools" / "gedcom_test.js")], capture_output=True, text=True, cwd=root)
    try: j = json.loads(g.stdout.strip().splitlines()[-1]); meta["gedcom"] = "OK" if g.returncode == 0 else "FEL"; meta["gedcom_variants"] = j.get("variants")
    except Exception: meta["gedcom"] = "ej testad"
else:
    meta["gedcom"] = "ej testad"
(root / "data" / "meta.json").write_text(json.dumps(meta, indent=1) + "\n")
print("Stämplat:", meta)
