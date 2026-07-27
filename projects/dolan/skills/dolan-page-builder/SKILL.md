---
name: dolan-page-builder
description: >
  Orchestrates fast creation of a new Dolan Design HVAC Elementor page from a content
  brief or doc. Use whenever the user says "build/create a Dolan page", "make a page
  from this doc", "new AC/cooling/service page", or hands over copy to turn into an
  Elementor page. Runs the full pipeline: design-read → content → design → complete
  JSON → responsive audit, reusing the kit's brand.
---

# Dolan Design HVAC Page Builder

The one entry point for turning a content brief into an import-ready Dolan Design
Elementor page. Sequences the other Dolan skills so a page comes out on-brand,
complete, and responsive in one pass.

**Input:** a content doc/brief (page type, location, hero, sections, FAQ, CTA).
Missing pieces are inferred from the closest existing page or one focused question.

**Output:** a single-page Elementor JSON saved to `projects/dolan/pages/<slug>/<slug>.json`,
plus a `PREVIEW.html` and `HANDOFF-notes.md`. Import via Elementor → Templates →
Import Templates.

## Pipeline (run in order)

1. **Design read** — apply `dolan-design-read`: page kind, closest existing page
   (AC Repair `233246` is the richest), state the one-line read.
2. **Map content to sections** — turn the doc into the Dolan anatomy:
   blue-overlay photo hero (h1 + intro + CTA) → alternating white / light-blue
   `#EDF4FF` bands → **service card grid** (emoji cards linking to each service page)
   → **two-column** "why choose" (list + photo) → FAQ accordion → blue-overlay closing
   CTA. Drop sections the doc doesn't need; don't invent filler.
3. **Write/polish copy** — apply `dolan-content-style`: local Franklin & Wake framing,
   plain-English honesty, 25+ years / dual-trade / upfront pricing / 0% financing.
4. **Style to the system** — apply `dolan-ui-design`: **every section = full-width
   Section → one boxed (~1140px) Content Container → content**, padding only on the
   container; blue/gold palette via real globals; Ruda; square bordered CTAs
   (color-only hover); **emoji icons** mixed in; layout variety.
5. **Emit complete JSON** — apply `full-output-enforcement`: full tree, unique `id`s,
   all required keys, every repeated widget written out, valid braces/escaping, UTF-8.
   Single-page wrapper with `page_settings:{template:"default","hide_title":"yes"}`
   and the kit's Divi-compat `custom_css`.
6. **SEO, links & media** — one H1 + clean hierarchy; carry slug / meta title /
   meta description as a publish-time handoff note; root-relative internal links with
   descriptive anchors (`/ac-repair/`, `/air-conditioner-maintenance/`,
   `/air-conditioner-installation/`, `/ac-replacement/`, `/mini-splits/`) and
   `#contact` for the primary CTA; images with alt text.
7. **Audit** — apply `dolan-page-audit`, then run
   `python3 scripts/responsive-audit.py <page>.json` (must exit 0) and confirm the
   JSON parses.

## Fastest path (reuse over rebuild)

Prefer cloning the closest existing page (`content/page/233246.json`) and swapping
content, then rebuilding to the boxed standard. Regenerate all element `id`s. Keep the
brand palette/button/rhythm.

## Deliverable & handoff

Save JSON + PREVIEW.html + HANDOFF-notes.md into `projects/dolan/pages/<slug>/`. Tell the user
the import path and post-import wiring (confirm `#contact` anchor + service slugs,
header/footer, SEO meta). Note which existing page it was based on.

## Guardrails

- Match the kit; don't redesign it. Keep buttons **square** (not pills).
- If the brief lacks a hero headline, location, or CTA target, ask one question
  rather than guessing brand-critical facts.
