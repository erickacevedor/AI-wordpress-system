# Magnolia Air — Kit Analysis (onboarding output)

The design system extracted from `current-theme/`, and *why* the tokens are what
they are. This is the human-readable companion to `tokens.json` and the generated
`magnolia-*` skills.

- **Site:** Magnolia Air — Central Louisiana HVAC/electrical/plumbing (Dry Prong,
  Alexandria, Pineville, Woodworth, Forest Hill, Ball, Pollock). Astra theme +
  Elementor Pro. 109 pages.
- **Globals:** REAL. The kit's Elementor color/typography globals hold true brand
  values and are referenced across widgets — use the global refs (with hex fallback).

## Palette (from widget-styling frequency)
| Role | Global id | Hex | Evidence |
|---|---|---|---|
| Primary teal | `primary` | `#0C4F4D` | 268 uses; heading color + hover |
| Gold | `secondary` | `#D4B351` | 214 uses; button bg + section bands (95 bg uses) |
| Accent gold | `accent` | `#D7B755` | accent |
| Dark teal | `fc26636` | `#00333F` | 306 uses; dark hero/CTA bands |
| White | `1d0e19b5` | `#FFFFFF` | 434 uses |
| Black/text | `1225c831`/`text` | `#000000` | body |
| Cream band | (inline) | `#F3EBD6` | 19 uses; light section tint |

Heading colors observed: teal `#0C4F4D` (159), dark teal `#00333F` (82), gold, white.
**Section rhythm:** alternate dark `#00333F` / cream `#F3EBD6` / white / teal `#0C4F4D`.

## Typography
- Headings: **Como-ExtraBold** (230 uses). Body: **BeVietnamPro-Light** (230).
  Emphasis/buttons: **BeVietnamPro-ExtraBold** (151). Roboto/Sora appear in theme
  chrome only; Corinthia is a rare decorative script — avoid.
- Type scale (px): h1 ~46, h2 ~33, h3 ~22, body ~17.

## Button — gold pill (match the site's hover)
Gold bg (`secondary`), white text, 2px gold border, `border-radius:50`, BeVietnamPro-
ExtraBold ~20px/500, `text-transform:capitalize`; **hover → teal (`primary`) bg+border,
`hover_animation:"shrink"`.** Keep `shrink` — it is this brand's convention (differs
from Dolan/VitalAir which are color-only). CTA link `/request-service/`.

## Signature components
- **24/7 call-out:** "📞 24/7 Emergency Service" + phone `(318) 233-9318`
  (Como-ExtraBold, gold, `tel:318-233-9318`). Use emoji, not the kit's `moesalley.com`
  phone image, to avoid a broken asset.
- Widgets in use: text-editor, heading, image-box, button, image, divider, icon-box,
  nested-accordion, icon-list.

## ⚠️ Kit gotchas (must handle)
1. **`display_condition_list` subscriber gates** wrap every element in exported pages —
   they hide content from normal visitors. **Never replicate them.** (`validate-page.py`
   fails on any.)
2. **`localhost:10008` page URLs** (dev export) — use **root-relative** internal links.
3. **Media on `moesalley.com`** — treat kit image URLs as swap-me placeholders.

## Internal link slugs
`/ac-repair/`, `/ac-maintenance/`, `/ac-installation/`, `/ac-replacement/`,
`/request-service/` (+ `/request-service-em/`). No dedicated tune-up page → point
tune-up to `/ac-maintenance/`.

## Closest page to mirror
`content/page/13046.json` (AC Services In Alexandria) — but it (and its siblings) are
thin, text-only, and carry the subscriber gate; rebuild clean to the standards.
