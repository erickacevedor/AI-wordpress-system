# HANDOFF — Mid Lakes: Financing (`/financing/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/financing/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `financing.json` |
| Page id on the install | **15** |
| Band order | `hero · white · paper · white · paper · white · paper · white · ink · paper(legal)` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — 4-item creds row |
| 2 | white | Intro — one lead paragraph |
| 3 | paper | Flexibility — copy + a 4:5 photo |
| 4 | white | Lending partner (`#financing-options`) — copy + a blue spec card |
| 5 | paper | Process — the 4-step track |
| 6 | white | Considerations — copy + a spec card |
| 7 | paper | FAQ — 5 items |
| 8 | white | Straight answers — copy + a 4:5 photo |
| 9 | ink | Contact |
| 10 | paper | Legal fine print |

## Page-specific notes

- ⚠️ **BOTH financing CTAs point at `#contact`, not at Service Finance.** That is a
  settled decision (PORT-DECISIONS, "Answered 2026-08-27"), **not a placeholder to
  chase**. Do not "fix" it to a lender URL.
- ⚠️ **The step numerals alternate** red / blue / red / blue
  (`.step:nth-child(odd)`), restated by `steps()` from the 1-based index.
- This is the only page with a closing `.legal` band, and the only one whose bands
  alternate perfectly the whole way down.
- **Zero validator warnings.**

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/financing/build.py
python3 scripts/validate-page.py projects/midlakes/pages/financing/financing.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/financing/financing.json" financing "Financing"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//financing/`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **15**) in place rather than creating a duplicate. Do not renumber the
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
| Slug | `/financing/` |
| Canonical | `https://<production-domain>/financing/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `HVAC Financing in Loganville, GA | Mid Lakes Heating & Cooling` |
| Meta description | `Flexible financing may be available for HVAC replacements and home comfort projects in Loganville, GA. Free estimates, no pressure. Ask about your options today.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 62 characters and the description 161; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (Flexible Financing for Your Home Comfort Needs), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

