# Earth Bound

Interactive heat map that scores places on Earth against Mars and the Moon. (Formerly Earth Analog Finder; file names are unchanged.)

## Run it
Open `dist/earth_analog_finder.html` in a browser with internet access. If a browser blocks online data for files opened by double-click, run `python3 -m http.server 8000` in this folder and open `http://localhost:8000/dist/earth_analog_finder.html`.

Online, it loads:
- **NASA POWER** climate values for the 30 named sites (temperature, swing, aridity, solar, wind, dust/AOD).
- **Real Earth terrain** in 3D: AWS Terrain Tiles elevation draped with Sentinel-2 cloudless imagery (8 × 8 km).
- **Real image comparisons** at the same 100 × 100 km scale: Sentinel-2 (Earth) vs NASA Trek Viking colour mosaic (Mars, Jezero) or LRO WAC (Moon, Shackleton).
- **Real Mars/Moon elevation maps**: NASA Trek MOLA / LOLA colour-shaded relief (2D).

Offline or on the hosted preview, it falls back to published estimates and an illustrative 3D shape, clearly labelled.

## New in v2
- Real terrain and imagery (above) replace the placeholders.
- Light / dark mode toggle (top bar; remembered per browser). Light mode uses a blue ocean, near-white land and strong orange-to-red scores for projectors and bright rooms.
- Zoom: mouse wheel, drag to pan (flat map), +/− buttons, whole-world button, and a **QATAR** button that flies to Qatar on both the flat map and the globe. Zoomed views use 1:50m coastlines, finer heat-map cells and site labels.

## Qatar detail and Kids view
- Zooming onto Qatar (or pressing **QATAR**) switches to a Qatar-only layer: city labels, named sites with their match score, and a glow around each site. Other countries keep simple colour tiles. Site positions marked "approx. location" and all Qatar values are estimates.
- Qatar sites: Zekreet yardangs & Dohat Faishakh sabkha, Khor Al Adaid, Dukhan sabkha, Sealine dunes (Mesaieed), Al Zubarah coastal sabkha.
- Site summaries have an **EXPLORER / KIDS** switch. Kids view: star rating, "Just like Mars / Not like Mars" in plain language, why scientists go there, a fun fact and a "Try this!" activity. The choice is remembered.

## Spreadsheet sites (analog_sites.xlsx)
- All 12 sites in `data/analog_sites.xlsx` (M1–M6, L1–L6) are pinned on the map with the same round markers as the other sites. Where a spreadsheet site and an existing site are the same place, only one marker is shown, and it opens the spreadsheet site.
- Clicking one opens its summary with a **Site data** panel: region, terrain, matched target, confidence, the 5 spreadsheet factors (Earth value, target value, difference, range R, match), the overall match, the target's source note, expeditions/use cases, the basis for the Earth values, and the limits note. Buttons switch between the 5 targets; ★ marks the site's own matched target.
- In the main score box, values taken from the spreadsheet (temperature, wind) are tagged **sourced**; the rest are tagged est. or interp.
- `build.py` reads the spreadsheet fresh when openpyxl is installed, and otherwise uses the copy embedded in `template.html`. `lib/qatar-10m.json` gives the detailed Qatar outline.

## Cover page
The page opens on an EARTHBOUND cover with the tagline and an **OPEN MAP** button (or press Enter). The map loads behind it. Opening it plays a short transition: the planet rises and fills the screen, then dissolves into the map (a simple fade if the visitor has reduced motion turned on).

## Panels
- **Top named sites** can be minimised with the − button (+ to expand).
- The **i** button next to **Adjust weights** explains what the weights do.

## Hover
Every clickable marker (all sites and the Qatar sites) grows when the mouse is over it and shows a tooltip; click to open its summary.

## Edit it
1. Edit `template.html` (DATA MODEL block for factors, targets and sites; APP block for behaviour).
2. Rebuild: `python3 build.py`. With `pip install openpyxl`, it reads `data/analog_sites.xlsx` fresh, so you can edit the spreadsheet and rebuild; without it, the copy embedded in the template is used.

## Data status
- Real: NASA POWER site climate (when online), Earth elevation and imagery, Mars/Moon imagery and colour-shaded elevation, coastlines.
- Estimated: roughness index, site values when offline. Interpolated: heat map between named sites.
- Mars/Moon heights are shown as NASA colour-shaded relief maps, not 3D meshes (no raw-height tiles were confirmed for browser use).

## Credits and licences
Sentinel-2 cloudless 2020 by EOX IT Services GmbH (CC BY-NC-SA 4.0; contains modified Copernicus Sentinel data) · AWS Terrain Tiles (SRTM, GMTED2010, ETOPO1 and others) · NASA Mars Trek and Moon Trek (Viking MDIM 2.1, MGS MOLA, LRO WAC, LRO LOLA) · NASA POWER · D3 (ISC), topojson-client (ISC), three.js (MIT), world-atlas / Natural Earth (public domain).

## Folder
| Path | What it is |
| --- | --- |
| `template.html` | Source: HTML, CSS, data model and app code |
| `build.py` | Builds `dist/earth_analog_finder.html` |
| `data/analog_sites.xlsx` | Team spreadsheet (sites M1–L6, targets, ranges, notes) |
| `data-retr.py` | Team script: median LOLA slope/roughness for a south-pole window (needs rasterio and the LOLA GeoTIFFs) |
| `lib/` | D3, TopoJSON, three.js, world maps (110m, 50m), Qatar 10m outline |
| `dist/earth_analog_finder.html` | Built page: open this in a browser |



## AI tools were used in the creation of the website code, front-end and backend. Such as Claude and ChatGPT