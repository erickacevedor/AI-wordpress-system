# HANDOFF — Mid Lakes: Service Agreements (`/service-agreements/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/service-agreements/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `service-agreements.json` |
| Page id on the install | **13** |
| Band order | `hero · white · paper · white · WHITE · paper · ink` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — one CTA, no creds row |
| 2 | white | Comfort Club — copy + a 4:5 photo |
| 3 | paper | Pricing — **the rate table** |
| 4 | white | Included — a 6-up icon-less service grid |
| 5 | white | Inspections — the two tune-up checklists |
| 6 | paper | FAQ — accordion + captioned photo |
| 7 | ink | Contact — includes the GA licence number |

## Page-specific notes

- ⚠️ **The rate table is the only tabular data on the site.** It ships as ONE `html`
  widget carrying the prototype's `<table>` verbatim; every style comes from the child
  theme's `.ml-rate-table`. Below 620px the header row hides and each row becomes its
  own card — pure CSS, no Elementor equivalent. **If the child theme is missing, this
  section is an unstyled HTML table.**
- ⚠️ **Sections 4 and 5 are both white, back to back.** Expected warning; deliberate.
- ⚠️ **Section 5 is `.about.what-happens`** — watermarks suppressed.
- The contact details list carries a fourth row the other pages do not: the **GA State
  License #CR108663**.
- **1 validator warning**, the expected band double above.

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/service-agreements/build.py
python3 scripts/validate-page.py projects/midlakes/pages/service-agreements/service-agreements.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/service-agreements/service-agreements.json" service-agreements "Service Agreements"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//service-agreements/`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **13**) in place rather than creating a duplicate. Do not renumber the
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
| Slug | `/service-agreements/` |
| Canonical | `https://<production-domain>/service-agreements/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `HVAC Service Agreements in Loganville, GA | Mid Lakes HVAC` |
| Meta description | `Join 300+ Loganville homeowners with a Mid Lakes Service Agreement. Two annual tune-ups, priority 24/7 service, and member discounts on repairs. Sign up today.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 58 characters and the description 159; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (HVAC Service Agreements in Loganville, GA), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

