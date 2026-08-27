---
name: midlakes-design-read
description: >
  Front-door / brief-inference skill for any Mid Lakes Heating & Cooling (Loganville,
  GA HVAC) page request. Use FIRST, before building or restyling, to read the brief,
  name the page kind, state a one-line design read, and route to the right midlakes-*
  skills. Keeps output faithful to the HTML prototype the port is copying — this is a
  1:1 port, not a redesign. Triggers: "build a Mid Lakes page", "port the Mid Lakes
  home page", "midlakes services page", "match the Mid Lakes prototype".
---

# Mid Lakes — Design Read (brief inference)

Use this at the **start** of any Mid Lakes page task.

Mid Lakes Heating & Cooling, LLC is a family-owned, veteran-owned HVAC contractor in
**Loganville, GA**, founded **2018**, serving Walton / Gwinnett and nine more counties.
The Elementor build is a **port of an existing HTML prototype**, not a new design.

| | |
|---|---|
| **The reference** | `D:\laragon\www\midlakes\public\<page>\index.php` + `styles.css` — the page template IS the spec |
| **The analysis** | `projects/midlakes/KIT-ANALYSIS.md` |
| **The seam** | `projects/midlakes/tokens.json` |
| **The decisions** | `projects/midlakes/PORT-DECISIONS.md` |
| **The install** | `projects/midlakes/ENVIRONMENT.md` — Local, `localhost:10015`, `mid-lakes` child theme + Elementor Pro |
| **The vocabulary** | `projects/midlakes/brand.py` — every component, built once. Pages supply copy and section order, nothing else |
| **The child theme** | `projects/midlakes/theme/mid-lakes/assets/mid-lakes.css` — the capped rule list |

## 0. The mandate, stated once so nobody relitigates it

> *"We need to build the Elementor version of the site exactly as it is (lo más
> parecido posible) so the colors and stuff should match exactly."*

**Fidelity beats editability.** Every property the child theme ships stops responding
to the Elementor editor — change a button colour in the UI and nothing happens,
because the class wins. The editor stays a **layout** tool and stops being a
**styling** tool for capped properties. The client was told and chose fidelity.

So: **match the prototype; do not improve it.** If something looks like a mistake
(two white bands in a row, a CTA pointing at `#contact` instead of a lender's site,
27 font sizes), check §12 of `KIT-ANALYSIS.md` and the *do NOT fix* list in
`midlakes-page-audit` before touching it. Most of them are already answered.

## 1. Read the room first

- **Page kind** — one of the six real pages (`/`, `/about-us/`, `/services/`,
  `/service-agreements/`, `/service-area/`, `/financing/`), a theme template
  (`pages/_theme/header`, `footer`), the blog **archive**, or a new page the
  prototype does not have.
- **Open the prototype page.** For an existing page, the source of truth is the
  `index.php`, section by section, plus the rules in `styles.css` for each class it
  uses. Do not build from memory or from another Mid Lakes page.
- **`/blog/` is not a page.** Page 16 is the WP posts page; the grid is an archive
  template. Six real pages, not seven.
- **What's fixed** — blue `#2540af` primary / red `#c10a0a` CTA / navy `#0f1f35`
  dark surface, Manrope everywhere with Fraunces italic numerals, the 1200px boxed
  container, the white↔paper alternation with an ink closing band, the 999px red pill
  that lifts 2px, root-relative links, and the wave watermarks.

## 2. State a one-line design read

Declare it before generating, e.g.:

> *"Reading this as: the `/service-agreements/` port — photo hero (technician.webp,
> H1 + sub + one red CTA, no creds row), white about-grid with a 4:5 photo, paper
> pricing band with the rate table as an `html` widget, white 6-up service-card grid,
> white `what-happens` band with the two checklist spec-cards (watermarks
> suppressed), paper FAQ accordion beside a captioned 4:5 photo, ink contact band
> with the `dl` + the shared quote-form template. Note the deliberate white→white
> double at sections 3→4."*

If the brief genuinely diverges from the prototype, ask **one** question. Otherwise
declare and proceed.

## 3. ⚠️ Gotchas (do not skip)

1. **Fonts come from the kit; COLOURS are written into the page.** The Default Kit
   (post 6) now sets Manrope as the base typography — because everything that
   *inherits* (Pro form fields, accordion body, list items) was otherwise rendering in
   Hello's Roboto. But **`system_colors` was deliberately left stock**, so a global
   colour ref still resolves to Hello's default and silently renders off-brand.
   **Never point a widget at a global colour slot.** `tokens.json` carries
   `"global": null` on every colour for exactly this reason.
2. **The button background key is `background_color`, NOT
   `button_background_color`.** A wrong key does not error; it falls through to
   `var(--e-global-color-accent)` and renders Hello's default with no warning.
3. **`heading(size=2.4)` defaults to `unit="px"`.** A heading meant to be `2.4rem`
   renders at 2.4 *pixels*. Pass `unit="rem"` explicitly.
4. **`typography_font_size_mobile` alone does nothing** without
   `typography_typography: "custom"`. It matters for `h1`/`h2`, which carry a mobile
   size and no desktop size — see the recipe in `midlakes-page-builder`.
5. **`#c10a0a` is unreadable on `#0f1f35`** (2.62:1). On the ink band use
   `--red-on-dark` `#ff8b8b` and `--blue-on-dark` `#6fb3ec`.
6. **Two identical bands adjacent is correct on three pages.** `/about-us/`,
   `/service-agreements/` and `/blog/` each ship one deliberately. Do not alternate
   them "properly".
7. **`.what-happens.about` suppresses its watermarks** (`display: none`). Two pages
   carry such a section.
8. **`.site-footer { padding-bottom: 300px }` exists only to clear a watermark.**
   Drop one and the other goes with it.
9. **`.e-con::before` is already Elementor's** (the container background overlay), and
   it sets `top`/`left`/`width`/`height`. Any CSS layer anchored with `bottom`/`right`
   gets silently pinned to the top-left instead. **Use `::after`.**

## 4. Route to the right skills

- **`midlakes-ui-design`** — the visual system. Always applies.
- **`midlakes-content-style`** — the copy voice. Whenever writing or adapting text.
- **`midlakes-page-builder`** — the pipeline, from source doc to validated JSON.
- **`midlakes-page-audit`** — reviewing/restyling, and as the pre-delivery gate.
- **`projects/midlakes/brand.py`** — read it before writing any `build.py`. Every
  component in `midlakes-ui-design` is already implemented there, with the
  alternations and the three footguns handled.
- **`full-output-enforcement`** (repo-root) — whenever emitting Elementor JSON.

## 5. Anti-generic discipline (port-aware)

There is nothing to invent here. The prototype already made every choice, and it made
them deliberately — the palette is sampled from the logo artwork, every foreground /
background pair is contrast-checked in a source comment, and the focus rings switch
colour band by band. Reach for the prototype, not for LLM defaults. The goal is a page
indistinguishable from `midlakes/public` at 1440px and at 390px.
