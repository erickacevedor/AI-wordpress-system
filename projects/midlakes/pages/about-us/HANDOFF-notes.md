# HANDOFF — Mid Lakes: About (`/about-us/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/about-us/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `about-us.json` |
| Page id on the install | **11** |
| Band order | `hero · white · paper · white · WHITE · comfort · paper · white · ink` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — 4-item creds row |
| 2 | white | Who we are — copy + stats trio |
| 3 | paper | Our story — copy + a 4:5 photo |
| 4 | white | Ownership — John Jessup + a 4:5 photo |
| 5 | white | Our values — a **3-up** why-grid |
| 6 | photo | Beyond HVAC |
| 7 | paper | Credentials — two spec cards + a Comfort Club note |
| 8 | white | Community — copy + the 11 county chips |
| 9 | ink | Contact |

## Page-specific notes

- ⚠️ **Sections 4 and 5 are both white, back to back.** `validate-page.py` warns
  (`rhythm: sections 4 and 5 share the same background`). **This is the prototype and
  is deliberate** — do not "fix" it. It is on the *do NOT fix* list in
  `midlakes-page-audit`.
- ⚠️ **Section 8 is `.about.what-happens`** — the wave watermarks are suppressed there
  (`display: none` in the prototype). Built with `sec_about(watermark=False)`.
- **The why-grid is 3-up here**, not 2-up: the page lists three values and a 2-up grid
  would leave a hole (`.why-grid--three`).
- **This page's form heading is "Schedule Service Online"**, not "Get a Free Estimate".
- **1 validator warning**, the expected band double above.

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/about-us/build.py
python3 scripts/validate-page.py projects/midlakes/pages/about-us/about-us.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/about-us/about-us.json" about-us "About"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//about-us/`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **11**) in place rather than creating a duplicate. Do not renumber the
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
| Slug | `/about-us/` |
| Canonical | `https://<production-domain>/about-us/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `Loganville HVAC Company | About Mid Lakes Heating & Cooling` |
| Meta description | `Meet the family behind Mid Lakes HVAC—Loganville-based and serving the community since 2018 with honest heating, cooling & home comfort service. NATE-certified, licensed.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 59 characters and the description 170; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (About Mid Lakes Heating &amp; Cooling), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

