---
name: lenz-design-read
description: >
  Front-door skill for any Lenz Heating & Cooling (lenzheatingandcooling.com,
  staging lenz.mysites.io) page or component request. Use FIRST, before building,
  restyling or adding a section, to read the brief, state a one-line design read,
  pick the reference page and route to the other lenz-* skills. Triggers: "new Lenz
  page", "build a Lenz page", "add a section to Lenz", "Lenz component", "style
  this like Lenz", "service page for Lenz", "Lenz landing page".
---

# Lenz Heating & Cooling: Design Read

Lenz is a veteran and woman-owned, family-run HVAC company in **Urbandale, IA**
(main office) with a second location in **Waukee**, serving the Des Moines metro
and Central Iowa **since 2009**. Phone `(515) 225-6446`. The new site is
WordPress + Hello Elementor + Elementor 4.2.2 + PRO Elements 4.1.0 + the
`lenz-core` plugin.

## 1. How this site is built (read before anything else)

Lenz is **not** styled in the Elementor panel. It is the opposite of the kit-based
sites in this repo:

- The approved design is a static HTML prototype (**v6-1**, snapshot in
  `design-source/v6-1/`: `v6-1.html` for the home, `ac-repair.html` for service
  pages, `css/lenz-v6-1.css`, `css/lenz-service.css`, `tokens.css`).
- `tools/port-css.py` ports that CSS into `plugin/lenz-core/assets/css/lenz-core.css`.
  **The CSS owns every colour, size, spacing and layout decision.**
- The Elementor tree **mirrors the prototype's DOM and class names**: containers and
  native widgets carry the same classes the prototype uses (`section`,
  `service-help promo`, `symptom-grid`, `btn btn-gold`...). Text, links, images and
  order are editable in Elementor; the look is not.
- Every component already exists as Python: primitives and shared components in
  `brand.py`, page blocks in `service_page.py`. A page is a `build.py` with a
  `PAGE` dict and a `plan` of blocks.

So "make it look like Lenz" means **compose existing classes and blocks**. It never
means inline colours, Elementor style controls, or a new look per page.

## 2. Sources of truth, in order

1. **ClickUp decisions** (task 86bbfgdhr and the Page Build tasks, including
   threads). Where a copy doc disagrees with ClickUp, ClickUp wins. The settled
   ones are encoded in `service_page.py` (`FIXES`, `REGEX_FIXES`, `CARD_FIXES`).
2. **The v6-1 prototype** for anything visual.
3. **The page's copy doc** (`pages/<slug>/source.docx`) for text, verbatim.
4. `KIT-ANALYSIS.md` for the reasoning behind tokens and contrast. Parts of it
   describe the **v4** build (cream surfaces, lead cards, mega menu widget,
   "services as containers"); where it disagrees with v6-1 or these skills, v6-1
   and these skills win.

## 3. Read the room

- **Page kind** and its reference page (mirror it, do not invent a layout):

  | Kind | Reference (read its `build.py`) | Typical plan |
  |---|---|---|
  | Repair | `pages/ac-repair/`, `pages/heating-repair/` | checklist, cards, values, why, faq, reviews, close |
  | Installation / replacement | `pages/ac-installation/`, `pages/heating-installation/` | checklist, cards, values (or table + bullets), why, faq, reviews, close |
  | Maintenance | `pages/heating-maintenance/`, `pages/ac-maintenance/` | boldcards or checklist + cards, pair, bullets, plans, why, faq, close |
  | Indoor air quality service | `pages/humidity-control/`, `pages/air-purification/`, `pages/uv-light-purification/` | pair / checklist / table, promo (Breathe Easy), why, faq, close |
  | Service hub | `pages/heating/`, `pages/air-conditioning/`, `pages/indoor-air-quality/` | `is_hub: True`; services, table, promo, faq, close |
  | Company / offer page | `pages/financing/`, `pages/maintenance-plan/`, `pages/about-us/` | `is_hub: True`, `cat_label`, `cat_icon`; boldcards, promo, steps, faq, close |
  | Location page | `pages/urbandale/`, `pages/waukee/` | prose, services, cards, why, steps, faq, close |
  | Home | `pages/home/build.py` (hand-built, 15 sections) | do not clone; reuse its components |

  The plan always follows **the doc's sections**; the typical plan is a guide to
  which block fits which kind of section, not a template to force the doc into.
  Do not add a block the doc has no section for (no reviews if the doc has none).

- **Category tint** (`PAGE["cat"]`): `cool` (AC, blue), `warm` (heating, orange),
  `air` (indoor air quality, purple), `extra` (additional services, gold).
  Company pages use `cool` unless a ClickUp decision says otherwise.
- **Scope:** the signed scope is 26 pages. Pages in `brand.OUT_OF_SCOPE` are never
  linked and never added to menus. A new page outside the 26 needs Erick's yes
  before it is linked anywhere.

## 4. State a one-line design read

Before generating, declare it, for example:

> *"Reading this as: a Heat Pump service page, sibling of Heating Repair, `cat`
> warm. Hero with the heat pump photo and a 24/7 badge, trustbar, checklist
> (signs you need service), cards (what we fix) followed by the emergency band,
> values, why, faq, reviews, related services and the closing form."*

If the brief genuinely diverges from every reference page, ask **one** question.
Otherwise declare and proceed.

## 5. Route

- **`lenz-ui-design`**: the visual system and the component catalogue. Always.
- **`lenz-content-style`**: whenever writing or editing copy.
- **`lenz-page-builder`**: building a page end to end.
- **`lenz-page-audit`**: reviewing, and as the gate before delivery.
- **`full-output-enforcement`** (repo root): for completeness only (unique ids, no
  elisions, valid JSON). Its advice to style widgets inline does **not** apply to
  Lenz: here style lives in `lenz-core.css` and the builder writes the JSON.

## 6. Anti-generic discipline

The goal is a page that looks like it was always part of the approved prototype.
No new fonts, colours, gradients, shadows, radii or icon sets. No emoji icons (the
site uses its own SVG sprite on purpose). No extra trust chips or badges beyond
what the reference page has, no "modern" redesign. If the content needs a shape no block provides, follow "Adding a
component" in `lenz-ui-design`; do not improvise one inside a page.
