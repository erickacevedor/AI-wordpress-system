---
name: gcreliable-design-read
description: >
  Front-door / brief-inference skill for any G.C. Reliable Service (gcreliable.com)
  page request. Use FIRST, before building or restyling, to read the brief, state a
  one-line design read, and route to the right gcreliable-* skills. Keeps output
  on-brand for an established Elementor kit — not hand-coded landing pages.
  Triggers: "new GC Reliable page", "build a gcreliable page", "AC installation
  page", "ductless page", "match the GC Reliable kit".
---

# G.C. Reliable Service — Design Read (brief inference)

Use this at the **start** of any G.C. Reliable page task. G.C. Reliable Service is a
Westchester County, NY HVAC contractor based in **New Rochelle**, serving since
**1980** (Eastchester, Harrison, Irvington, Larchmont, Mamaroneck, Pelham, Rye Brook,
Scarsdale, Valhalla, White Plains, Hartsdale, Bronxville). Kit is Elementor Pro on
**Hello Elementor Child**.

## 1. Read the room first

- **Page kind** — system hub (`/systems/air-conditioning`), single service
  (AC Repair / AC Installation / Ductless / Maintenance / Heat Pumps), location page
  (`/service-area/<city>`), or a landing/thank-you page.
- **Read the agency's own hand-off templates first — they are the guide.**
  `templates/227368.json` (*GC Reliable – AC Repair – Full Page*) and
  `templates/227376.json` (*GC Reliable – Cooling Services – Full Page*), plus
  `227364` (*ExampleTemplateforAC*, an earlier cut). `227368` is the published
  AC Repair page (`content/page/225063.json`) with image/review **placeholders**
  instead of real assets — either is a valid model, but read `227376` too: the hub
  template carries the **service card**, the **image-placeholder convention**, and a
  **CTA button on the gradient trust band** that the AC Repair page does not.
- ⚠️ **`templates/225540.json` "Design Guide" is an unfilled boilerplate.** Every
  colour/hover global it references is absent from this kit's `site-settings.json`.
  Do not mine brand values from it.
- **The reference *page* is `content/page/225063.json` — "AC Repair".** It is the only
  current-generation, fully designed page in the kit and it was built to this repo's
  standards. Every new service page should be a sibling of it, not of the legacy
  text-blob pages.
- **What's fixed** — blue `#0033CC` / red `#FF0000` palette, `brandon-grotesque`
  everywhere, **square red CTA with colour-only hover**, the 1280px boxed container,
  the gradient hero / `#EFF2F5` alternating rhythm, `/systems/...` root-relative
  links, the Trustindex review band, "since 1980 / 24/7 / all makes and models".

## 2. State a one-line design read

Declare it before generating, e.g.:

> *"Reading this as: a new AC Installation service page, sibling of AC Repair —
> blue gradient hero with H1 + sub-line + red CTA, white intro row with photo +
> floating '40+' badge, `#EFF2F5` band with a two-column 'signs it's time' list +
> warning card, white 4-step process on numbered blue-bar cards, `#EFF2F5` FAQ
> accordion beside a 'still have questions' card, white review band, blue gradient
> 'why trust us' band, `#EFF2F5` closing CTA."*

If the brief genuinely diverges, ask **one** question. Otherwise declare and proceed.

## 3. ⚠️ Kit gotchas (do not skip)

1. **Two conflicting `custom_colors` sets share the same ids** in
   `site-settings.json`. Inline the band hexes (`#EFF2F5`, `#E6ECFA`, `#F8F8FB`,
   `#001E78`) and only use globals for `primary` / `secondary` / white
   (`63acc82`), the way the AC Repair page does.
2. **Legacy URLs** (`/amana/...`, `/services/...`) still appear in old pages. The
   live scheme is `/systems/...`. Write internal links **root-relative**.
3. **Legacy pages render their hero from ACF** (`page_h1_title`, `page_sub-title`,
   `lead_paragraph`) with `template: "default"`. New pages instead build the hero in
   Elementor and set `{"template":"elementor_header_footer","hide_title":"yes"}`.
4. **FAQ uses the Elementor Pro `accordion` widget** (a `tabs` array), *not*
   `nested-accordion` — match the reference page.
5. `ha_cmc_text: "Happy Addons"` litters the export. It's inert; don't reproduce it.
6. Font Awesome **Pro** is active — `fad fa-check-circle` (duotone) is the kit's
   list bullet and it does render. Still mix in emoji icons so a page never depends
   entirely on the icon font.

## 4. Route to the right skills

- **`gcreliable-ui-design`** — the visual system. Always applies.
- **`gcreliable-content-style`** — the copy voice. Whenever writing text.
- **`gcreliable-page-audit`** — reviewing/restyling, and as the pre-delivery gate.
- **`full-output-enforcement`** (repo-root) — whenever emitting Elementor JSON.

## 5. Anti-generic discipline (kit-aware)

Reach past LLM defaults, but toward *this* brand: local Westchester specificity,
decision-support rather than hard sell, plain language, no hype. Don't invent new
fonts or accent colors. The goal is a page that looks like it already belonged on
gcreliable.com — not a redesigned one.
