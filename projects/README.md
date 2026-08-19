# projects/ — one folder per site

Each site the system has worked on lives here. See `../AGENTS.md` for the full
process. Standard layout per site:

```
projects/<site>/
├── current-theme/     ← the unzipped Elementor kit export             [SITE-WIDE]
├── tokens.json        ← brand tokens (colors/fonts/button/links)      [SITE-WIDE]  → feeds every page build
├── brand.py           ← the site's component vocabulary               [SITE-WIDE]  → extract before page 3
├── KIT-ANALYSIS.md    ← design-system analysis onboarding produced    [SITE-WIDE]  (the "why")
├── skills/            ← generated per-site skills                     [SITE-WIDE]  (<site>-design-read/-ui-design/-content-style/-page-builder/-page-audit)
└── pages/             ← one self-contained folder PER PAGE
    └── <page-slug>/
        ├── source.<ext>        ← the page's source doc/brief
        ├── build.py            ← reproducible build (imports ../../../../scripts/elementor_builder.py, reads ../../tokens.json)
        ├── <page-slug>.json    ← built import-ready page
        ├── PREVIEW.html        ← browser design-review
        └── HANDOFF-notes.md    ← import + SEO handoff
```

**Site-wide vs. per-page:** the kit, `tokens.json`, `KIT-ANALYSIS.md`, and `skills/`
are the brand — shared by every page, so they stay at the site root. Everything
specific to one page lives together in its own `pages/<page-slug>/` container, so a
site can hold many pages without collisions. Each `build.py` finds the repo root by
walking up to `AGENTS.md`, so it runs from anywhere.

## Sites

| Site | Status | Pages |
|---|---|---|
| `dolan` | ✅ full | `pages/cooling-services/` |
| `magnolia` | ✅ full | `pages/air-conditioning-services/` |
| `petitt` | ✅ full | `pages/white-house/` |
| `gcreliable` | ✅ full + `brand.py` | `pages/ac-installation/`, `pages/ductless-mini-split/` — the reference for the component-vocabulary tier |
| `lenz` | ⚠️ no skills | Onboarded from an HTML design repo rather than a kit, so the skill-generation step never ran — it has `tokens.json` + `KIT-ANALYSIS.md` but no `skills/`, and its `pages/home/build.py` carries the brand vocabulary inline. Also holds `plugin/`, `tools/` and `pages/_theme/` (header + footer templates). Generate the `lenz-*` skills and extract `brand.py` before building its service pages. |
| `air-comfort` | ⚠️ legacy | Built before the skills/tokens/pages pattern — has `current-theme/` + a flat `output/` (3 pages sharing one PREVIEW/HANDOFF). This is exactly the collision the `pages/<slug>/` layout fixes; onboard + migrate it if it becomes active. |

## Add a new page to an existing site
```
mkdir -p projects/<site>/pages/<page-slug>          # drop the source doc in here
# author pages/<page-slug>/build.py on the site's brand.py (or directly on
# scripts/elementor_builder.py if the site has none yet); brand values come from ../../tokens.json
python3 projects/<site>/pages/<page-slug>/build.py
python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json   # must exit 0
```
