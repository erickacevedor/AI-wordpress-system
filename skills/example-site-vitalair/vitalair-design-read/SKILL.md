---
name: vitalair-design-read
description: >
  Front-door / brief-inference skill for any VitalAir page request. Use first,
  before building or restyling, to read the brief, state a one-line design read,
  and route to the right VitalAir skills. Keeps output on-brand and anti-generic
  for an Elementor kit — not hand-coded landing pages.
---

# VitalAir Design Read (brief inference)

Use this at the **start** of any VitalAir page task. It replaces the generic web-design "taste" workflow, which was built for hand-coded landing pages and pushes fonts, motion dials, and aesthetics that don't apply to an established Elementor brand kit.

## 1. Read the room first

Before touching JSON, infer what the request actually needs:

- **Page kind** — service page, service-area page, FAQ, landing/promo, blog post, About/Contact.
- **Is there a close match in the kit?** Most page types already exist (AC Repair, Cooling Services, Service-Marietta, FAQ, etc.). Prefer adapting the closest existing page/template over inventing structure.
- **Container vs. Section** — match the newer Container model unless cloning a specific legacy page.
- **What's fixed** — brand colors, Poppins, green pill CTAs, section rhythm, header `10` / footer `181`. These are not up for reinterpretation.

## 2. State a one-line design read

Before generating, declare it in one line, e.g.:

> *"Reading this as: a new service-area page for the Woodstock market, matching the Service-Marietta pattern — navy hero, alternating white/#EEF2FA bands, FAQ accordion, green-pill CTA."*

If the brief genuinely diverges (e.g. unclear whether it's a service page or a promo landing), ask **one** question — not a multi-question dump. If you can infer confidently, don't ask; declare the read and proceed.

## 3. Route to the right skills

- **`vitalair-ui-design`** — the visual system (colors, type, buttons, layout, templates). Always applies.
- **`vitalair-content-style`** — the copy voice. Applies whenever writing text.
- **`vitalair-page-audit`** — when reviewing or restyling an existing page.
- **`full-output-enforcement`** — whenever emitting Elementor JSON, so it comes out complete.

## 4. Anti-generic discipline (kit-aware)

Reach past LLM defaults — but toward the VitalAir brand, not a generic "premium" look:

- Don't default to a blank minimalist/monochrome aesthetic. VitalAir is colored, warm, local, conversion-focused.
- Don't invent new fonts, motion systems, or accent colors. Use the kit's.
- Don't produce a symmetrical three-equal-cards wall by reflex — but do use the kit's icon-box grids where they fit.
- Don't write hero copy in web-startup voice ("Elevate your comfort"). Use the local, plain VitalAir voice.

The goal is a page that looks like it already belonged in this site — not a redesigned or "improved" one.
