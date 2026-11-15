"""Build dist/earth_analog_finder.html from template.html + lib/ (+ data/analog_sites.xlsx).

Run:  python3 build.py
- Always inserts the libraries and map data from lib/.
- If lib/qatar-10m.json exists, it is used for the detailed Qatar outline.
- If data/analog_sites.xlsx exists and openpyxl is installed (pip install openpyxl),
  the spreadsheet is read fresh, so editing the Excel file and rebuilding updates the map.
  Otherwise the copy of the spreadsheet embedded in template.html is used.
"""
import json
from pathlib import Path

here = Path(__file__).parent


def excel_model(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=False)
    P, T, S, N = wb["Parameters"], wb["Targets"], wb["Sites"], wb["Notes"]
    factors = [dict(key=r[0].split()[0].lower(), name=r[0], unit=r[1], R=float(r[2]))
               for r in P.iter_rows(min_row=2, values_only=True) if r[0] and isinstance(r[2], (int, float))]
    nf = len(factors)
    targets = {r[0]: dict(values={f["key"]: r[1 + i] for i, f in enumerate(factors)}, confidence=r[1 + nf], basis=r[2 + nf])
               for r in T.iter_rows(min_row=2, values_only=True) if r[0]}
    hdr = [c.value for c in S[1]]; ix = {h: i for i, h in enumerate(hdr)}; v0 = ix["Matched target"] + 1
    notes, limits = {}, None
    for a, b in N.iter_rows(min_row=2, values_only=True):
        if a and a.startswith("Limits"): limits = b
        elif a: notes[a.split()[0]] = b
    footnote = next((c.value for row in S.iter_rows(min_row=2) for c in row if isinstance(c.value, str) and "ESTIMATED" in c.value), "")
    sites = [dict(id=r[0], site=r[1], country=r[2], region=r[3], terrain=r[4], lat=r[5], lon=r[6], native_target=r[7],
                  earth={f["key"]: r[v0 + i] for i, f in enumerate(factors)}, expeditions=r[ix["Expeditions"]],
                  confidence=r[ix["Confidence (Earth values)"]], notes=notes.get(r[0]))
             for r in S.iter_rows(min_row=2, values_only=True) if r[0]]
    return dict(factors=factors, targets=targets, sites=sites, footnote=footnote, limits=limits)


t = (here / "template.html").read_text(encoding="utf-8")
for placeholder, name in [("/*D3*/", "d3.min.js"), ("/*TOPO*/", "topojson-client.min.js"), ("/*THREE*/", "three.min.js"),
                          ("/*WORLD*/", "countries-110m.json"), ("/*WORLD50*/", "countries-50m.json")]:
    assert placeholder in t, f"missing {placeholder} in template.html"
    t = t.replace(placeholder, (here / "lib" / name).read_text(encoding="utf-8"), 1)

qatar = here / "lib" / "qatar-10m.json"
if qatar.exists():
    t = t.replace("/*QATAR*/", qatar.read_text(encoding="utf-8"), 1)
    print("Qatar outline: lib/qatar-10m.json")

xlsx = here / "data" / "analog_sites.xlsx"
try:
    if xlsx.exists():
        t = t.replace("/*EXCEL*/", json.dumps(excel_model(xlsx), ensure_ascii=False), 1)
        print("Spreadsheet: read fresh from data/analog_sites.xlsx")
except ImportError:
    print("Spreadsheet: openpyxl not installed, using the copy embedded in template.html (pip install openpyxl to read the Excel file)")

out = here / "dist" / "earth_analog_finder.html"
out.parent.mkdir(exist_ok=True)
out.write_text(t, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size/1e6:.2f} MB)")



