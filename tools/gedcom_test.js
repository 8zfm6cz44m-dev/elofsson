// Testar GEDCOM-exporten i alla sex varianter (omfattning × dölj detaljer). Utskrift: JSON. Exit 0 = OK.
const G = require("../assets/gedcom.js"), fs = require("fs"), path = require("path");
const d = f => JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", f + ".json")));
const P = d("persons"), R = d("relations");
let errors = 0, variants = 0;
for (const scope of ["all", "nolead", "solid"]) for (const mask of [true, false]) {
  const { text } = G.buildGedcom(P, R, { scope, maskLiving: mask });
  const lines = text.replace(/^﻿/, "").split("\r\n").filter(Boolean);
  const defs = new Set(), refs = []; let prev = 0;
  lines.forEach(l => {
    const m = l.match(/^(\d+) (?:(@[^@]+@) )?([A-Z_]+)(?: (.*))?$/);
    if (!m) { errors++; return; }
    const lv = +m[1]; if (lv > prev + 1) errors++; prev = lv; if (l.length > 255) errors++;
    if (m[2]) defs.add(m[2]); if (m[4] && /^@[^@]+@$/.test(m[4])) refs.push(m[4]);
  });
  errors += refs.filter(r => !defs.has(r) && r !== "@U1@").length; variants++;
}
console.log(JSON.stringify({ variants, errors }));
process.exit(errors ? 1 : 0);
