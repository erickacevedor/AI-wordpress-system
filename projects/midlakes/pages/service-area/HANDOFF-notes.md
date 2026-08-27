# HANDOFF — Mid Lakes: Service Areas (`/service-area/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/service-area/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `service-area.json` |
| Page id on the install | **14** |
| Band order | `hero · white · paper · white · paper · ink` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — no creds row |
| 2 | white | Local since 2018 — copy + a 4:5 photo |
| 3 | paper | Coverage — **the map** beside the 7-town list |
| 4 | white | What we offer — two promise columns |
| 5 | paper | FAQ — accordion + captioned photo |
| 6 | ink | Contact — four detail rows |

## Page-specific notes

- ⚠️ **The map is the Elementor Google Maps WIDGET** (PORT-DECISIONS decision 11), not
  the prototype's raw iframe, inside a radius-14 bordered frame at `min-height` 420
  (320 on mobile). It geocodes `2834 Horseshoe Rd, Loganville, GA 30052`. Confirm it
  renders on the target — some hosts need a Maps API key for the embed.
- ⚠️ **Section 4 nests h3 inside h3**: a column heading above a `.promise` list whose
  items are also h3. That is the prototype's own markup. Levels do not *skip*, so it is
  valid — **do not "fix" it to h4**, it would diverge from the prototype for no gain.
- **Zero validator warnings.**

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/service-area/build.py
python3 scripts/validate-page.py projects/midlakes/pages/service-area/service-area.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/service-area/service-area.json" service-area "Service Areas"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//service-area/`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **14**) in place rather than creating a duplicate. Do not renumber the
stubs.

## The page must not be imported alone

It depends on three things that are site-wide, not per-page:

| Dependency | Where it lives | Why |
|---|---|---|
| The **`mid-lakes` child theme** | `projects/midlakes/theme/`, deployed by `deploy-theme.sh` | Owns the `clamp()` heads, Fraunces, the hover transforms, the watermarks, the rate table, the focus rings and the header blur. Without it the page renders but loses all of them |
| **Header / footer templates** | `projects/midlakes/pages/_theme/` | Applied "Entire Site" |
| **`media.json` attachment ids** | `projects/midlakes/media.json` | The five photos. Ids are for THIS install |

## Post-import wiring

- [ ] Confirm the child theme is active and `wp elementor flush_css` has run.
- [ ] Set the SEO title + description below (**no SEO plugin is installed yet** —
      PORT-DECISIONS "Open #2"). They have nowhere to live until one is.
- [ ] Confirm the header and footer templates are applied.
- [ ] At go-live, run `wp elementor replace_urls http://localhost:10015 https://<domain>`
      — the image URLs in this JSON are this install's.

## SEO

| | |
|---|---|
| Slug | `/service-area/` |
| Canonical | `https://<production-domain>/service-area/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `HVAC Service Areas Near Loganville, GA | Mid Lakes HVAC` |
| Meta description | `HVAC service across Loganville, Snellville, Monroe, Grayson, Lawrenceville & surrounding Walton and Gwinnett Counties. 24/7 repair and Carrier installs. Call to confirm your area.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 55 characters and the description 179; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (HVAC Service Areas in Loganville, GA &amp; Surrounding Communities), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

