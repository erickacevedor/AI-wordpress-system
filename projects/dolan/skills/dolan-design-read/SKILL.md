---
name: dolan-design-read
description: >
  Front-door / brief-inference skill for any Dolan Design HVAC page request. Use
  FIRST, before building or restyling, to read the brief, state a one-line design
  read, and route to the right Dolan skills. Keeps output on-brand for an established
  Elementor kit. Triggers: "new Dolan page", "build a Dolan Design page", "cooling/
  AC services page", "match the Dolan kit".
---

# Dolan Design HVAC — Design Read (brief inference)

Use this at the **start** of any Dolan Design page task. Dolan Design HVAC & Plumbing
is a local, family-owned company in Louisburg, NC serving Franklin & Wake County
(Louisburg, Raleigh, Wake Forest, Youngsville, Zebulon, Franklinton). Kit is
Elementor on a **Divi child** theme (`dolandesignhvac.com`).

## 1. Read the room first

- **Page kind** — service hub (Cooling Services), single service (AC Repair, Maint.,
  Install, Replacement, Mini-Splits), FAQ, promo landing, blog post.
- **Closest match in the kit?** Service pages already exist. The richest to mirror is
  `content/page/233246.json` (AC Repair). Prefer adapting the closest one over
  inventing structure.
- **What's fixed** — brand blue/gold palette, Ruda font, square bordered CTAs,
  light-blue `#EDF4FF` bands, the two-tier boxed section structure, `#contact` CTA
  anchor. Not up for reinterpretation.

## 2. State a one-line design read

Declare it before generating, e.g.:

> *"Reading this as: a new Cooling Services hub for Louisburg — blue-overlay photo
> hero + intro + CTA, a 3-card emoji service grid linking to each service page, a
> two-column 'why choose' block, FAQ accordion, blue-overlay closing CTA."*

If the brief genuinely diverges, ask **one** question. If you can infer confidently,
declare the read and proceed.

## 3. Route to the right skills

- **`dolan-ui-design`** — the visual system (colors, type, buttons, boxed section
  structure, emoji icons). Always applies.
- **`dolan-content-style`** — the copy voice. Applies whenever writing text.
- **`dolan-page-audit`** — when reviewing/restyling, and as the pre-delivery gate
  (incl. `scripts/responsive-audit.py`).
- **`full-output-enforcement`** — whenever emitting Elementor JSON, so it's complete.

## 4. Kit notes

Dolan's Elementor **globals are REAL** (defined in `site-settings.json` custom
colors) and the kit references them — use them (with inline fallbacks) rather than
inlining everything. Media lives on `dolandesignhvac.com`; internal links use
root-relative service slugs and `#contact` for the primary CTA.

## 5. Anti-generic discipline

Reach past LLM defaults toward the Dolan brand: local, family-owned, plain-English,
trust-building. Don't invent new fonts/accent colors; use blue + gold + Ruda. Don't
write hero copy in web-startup voice. The page should look like it already belonged
on this site.
