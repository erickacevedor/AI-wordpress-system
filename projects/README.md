# projects/ — one folder per site

Each site the system has worked on lives here. See `../AGENTS.md` for the full
process. Standard layout per site:

```
projects/<site>/
├── current-theme/   ← the unzipped Elementor kit export
├── new-content/     ← source doc(s)/brief for the new page(s)
├── tokens.json      ← brand tokens (colors/fonts/button/links) → feeds build.py
├── build.py         ← reproducible page build (imports ../../scripts/elementor_builder.py)
├── skills/          ← generated per-site skills (<site>-design-read/-ui-design/-content-style/-page-builder/-page-audit)
├── KIT-ANALYSIS.md  ← design-system analysis onboarding produced (the "why")
└── output/          ← built page JSON + PREVIEW.html + HANDOFF-notes.md
```

## Sites

| Site | Status | Notes |
|---|---|---|
| `dolan` | ✅ full | Louisburg, NC HVAC. Skills + tokens + build.py + KIT-ANALYSIS. Page: `output/cooling-services.json`. |
| `magnolia` | ✅ full | Central LA HVAC. Skills + tokens + build.py + KIT-ANALYSIS. Page: `output/air-conditioning-services.json`. |
| `air-comfort` | ⚠️ legacy | Built before the skills/tokens pattern — has `current-theme/` + `output/` only. Reference example; would need onboarding to reach the full layout. |

## Reproduce / rebuild a page
```
python3 projects/<site>/build.py
python3 scripts/validate-page.py projects/<site>/output/<page>.json   # must exit 0
```
