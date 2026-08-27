# HANDOFF — Mid Lakes: Services (`/services/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/services/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `services.json` |
| Page id on the install | **12** |
| Band order | `hero · section-nav · white · paper · white · comfort · paper · white · ink` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — 4-item creds row |
| 2 | paper | Sticky in-page anchor bar (6 links) |
| 3 | white | Intro — two lead paragraphs, no heading |
| 4 | paper | Heating &amp; Cooling — 3 detail rows |
| 5 | white | Whole-Home Comfort — 3 detail rows |
| 6 | photo | 24/7 emergency |
| 7 | paper | Comfort Club — 3 icon-less service cards |
| 8 | white | Coverage — 20 community chips |
| 9 | ink | Contact |

## Page-specific notes

- **The sticky anchor bar** sits at `top: 76px` — the header's height. If the header
  height ever changes, this offset changes with it.
- ⚠️ **The flipped detail rows are the ones carrying the BLUE spec card.** Rows run
  red / blue / red in each of sections 4 and 5. That pairing is the pattern, not a
  coincidence.
- ⚠️ **`.detail-row:first-of-type`** drops its top border and pads 8px instead of 52.
  Both bands restart the count, so each has its own first row.
- The comfort-club cards in section 7 carry **no icons** in the prototype, so there is
  no tile alternation on them.
- **Zero validator warnings.**

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/services/build.py
python3 scripts/validate-page.py projects/midlakes/pages/services/services.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/services/services.json" services "Services"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//services/`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **12**) in place rather than creating a duplicate. Do not renumber the
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
| Slug | `/services/` |
| Canonical | `https://<production-domain>/services/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `HVAC & Home Comfort Services in Loganville, GA | Mid Lakes` |
| Meta description | `HVAC repair, ductless, thermostats, insulation, crawl space encapsulation & humidity control in Loganville, GA. 24/7 service, licensed & insured, parts-and-labor guarantee.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 58 characters and the description 172; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (HVAC &amp; Home Comfort Services in Loganville, GA), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

