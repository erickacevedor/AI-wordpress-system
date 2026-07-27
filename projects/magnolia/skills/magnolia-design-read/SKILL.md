---
name: magnolia-design-read
description: >
  Front-door / brief-inference skill for any Magnolia Air page request. Use FIRST,
  before building or restyling, to read the brief, state a one-line design read, and
  route to the right Magnolia skills. Keeps output on-brand for an established
  Elementor kit — not hand-coded landing pages. Triggers: "new Magnolia page",
  "build a Magnolia Air page", "AC services page", "match the Magnolia kit".
---

# Magnolia Air — Design Read (brief inference)

Use this at the **start** of any Magnolia Air page task. Magnolia Air is a Central
Louisiana HVAC/electrical/plumbing company (Dry Prong, Alexandria, Pineville,
Woodworth, Forest Hill, Ball, Pollock). Kit is Elementor on an **Astra** theme.

## 1. Read the room first

Before touching JSON, infer what the request needs:

- **Page kind** — service hub (AC Services), single service (AC Repair/Install/…),
  location service page, FAQ, request-service/landing.
- **Closest match in the kit?** Location service pages already exist by the dozen
  (e.g. `content/page/13046.json` "AC Services In Alexandria"). Prefer adapting the
  closest one's *content model* over inventing structure — but see the gotcha below.
- **What's fixed** — brand teal/gold palette, Como-ExtraBold + BeVietnamPro fonts,
  gold pill CTAs, alternating dark/cream/white/teal bands, root-relative links,
  the 24/7 call-out. These are not up for reinterpretation.

## 2. State a one-line design read

Declare it before generating, e.g.:

> *"Reading this as: a new AC Services hub for Dry Prong, LA — dark-teal hero with
> a 24/7 call-out + gold CTA, cream/white alternating bands, a 6-card emoji service
> grid, a two-column home/business split, FAQ accordion, teal closing CTA."*

If the brief genuinely diverges, ask **one** question — not a dump. If you can infer
confidently, declare the read and proceed.

## 3. ⚠️ Critical kit gotcha (do not skip)

The exported Magnolia pages wrap **every element** in a `display_condition_list`
set to `subscriber` — a visibility gate. **Never copy it into a new page**; it hides
content from normal visitors. Build clean elements without `display_condition_list`.
Also: page URLs in the kit are `localhost:10008` (dev export) and media is hosted on
`moesalley.com` — use **root-relative slugs** (`/ac-repair/`, `/request-service/`)
for internal links, and treat kit image URLs as swap-me placeholders.

## 4. Route to the right skills

- **`magnolia-ui-design`** — the visual system (colors, type, buttons, layout,
  boxed-1140 section structure). Always applies.
- **`magnolia-content-style`** — the copy voice. Applies whenever writing text.
- **`magnolia-page-audit`** — when reviewing or restyling an existing page, and as
  the pre-delivery gate (incl. `scripts/responsive-audit.py`).
- **`full-output-enforcement`** — whenever emitting Elementor JSON, so it's complete.

## 5. Anti-generic discipline (kit-aware)

Reach past LLM defaults, but toward the Magnolia brand: warm, local, practical,
conversion-focused. Don't invent new fonts/accent colors; use teal + gold. Don't
write hero copy in web-startup voice. The goal is a page that looks like it already
belonged on this site — not a redesigned one.
