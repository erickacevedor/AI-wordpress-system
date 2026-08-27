# HANDOFF — Mid Lakes: Home (`/`)

**Built 2026-08-27** from the prototype at
`D:\laragon\www\midlakes\public/` — a **1:1 port**. All copy is the
prototype's, verbatim, entities included.

| | |
|---|---|
| Source | `source.php` (a copy of the prototype page) |
| Build | `build.py` → `home.json` |
| Page id on the install | **10** |
| Band order | `hero(photo) · white · paper · comfort(photo) · white · paper · ink` |
| Gate | `validate-page.py` exits **0** |

## What is on this page

| # | Band | Section |
|---|------|---------|
| 1 | photo | Hero — H1 + sub + Call/Estimate buttons + a 3-item creds row |
| 2 | white | About — 1.4fr/1fr copy + stats trio, then the gallery + the 3-item promise list |
| 3 | paper | Services — the 6-up service-card grid with the sprite icons |
| 4 | photo | Comfort Club — perk list + one red CTA |
| 5 | white | Why Mid Lakes — 2×2 why-cards with the Fraunces numerals |
| 6 | paper | FAQ — accordion beside a captioned 4:5 photo |
| 7 | ink | Contact — details list + the shared quote form |

## Page-specific notes

- **The FAQ's first item ships OPEN.** `<details class="faq-item" open>` on this page
  only; every other page's accordion starts fully collapsed.
- **All three alternations appear here** and are restated widget by widget: the six
  icon tiles run red/blue/red/blue/red/blue, and the four why-numerals run
  red/blue/red/blue. Verified in the rendered CSS.
- The service icons come from the child theme's inline SVG sprite
  (`assets/icons.svg`), referenced as `<use href="#ml-icon-…">`.
- **Zero validator warnings.**

## Import

```bash
# from the repo root
python3 projects/midlakes/pages/home/build.py
python3 scripts/validate-page.py projects/midlakes/pages/home/home.json   # must exit 0
projects/midlakes/wp.sh eval-file scripts/import-page.php \
    "$(pwd)/projects/midlakes/pages/home/home.json" home "Home"
```

Or `./projects/midlakes/build-all.sh --deploy` to do the whole site at once.

Through the UI instead: Elementor → Templates → Import Templates → upload the JSON →
open the imported page → publish at `//`.

`import-page.php` is **idempotent by slug**, so this updates the existing stub
(page **10**) in place rather than creating a duplicate. Do not renumber the
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
| Slug | `/` |
| Canonical | `https://<production-domain>/` — the domain is still open (PORT-DECISIONS "Open #1") |
| Meta title | `Heating & Air Conditioning in Loganville, GA | Mid Lakes HVAC` |
| Meta description | `Family-owned Loganville HVAC since 2018. Carrier installs, repairs, insulation & crawl space encapsulation. 24/7 emergency service, free estimates & a parts-and-labor guarantee.` |

> **Both are the prototype's own hand-written strings, kept verbatim.** The title is
> 61 characters and the description 177; Google typically truncates around 60
> and 155. `validate-page.py` warns about this. **It has not been shortened**, because
> these are existing locality-targeted content decisions and rewriting them is a
> client call, not a port decision. Raise it when the SEO plugin is chosen.

## Accessibility

One H1 (Heating, Cooling &amp; Home Comfort in Loganville, GA), clean H2/H3 below it, no skipped levels. Every image carries the
prototype's alt text verbatim. Every CTA has a visible descriptive label — none are
icon-only. Nothing auto-plays. The form's fields all keep real `<label>`s. Focus rings
are the design's own, and switch colour on the navy bands (brand red is 2.62:1 there).

