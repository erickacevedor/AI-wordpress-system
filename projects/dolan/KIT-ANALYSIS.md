# Dolan Design HVAC — Kit Analysis (onboarding output)

The design system extracted from `current-theme/`, and *why* the tokens are what they
are. Companion to `tokens.json` and the generated `dolan-*` skills.

- **Site:** Dolan Design HVAC & Plumbing (`dolandesignhvac.com`) — Louisburg, NC,
  family-owned, serving Franklin & Wake County (Louisburg, Raleigh, Wake Forest,
  Youngsville, Zebulon, Franklinton). Divi child theme + Elementor Pro.
- **Globals:** REAL. Defined in `site-settings.json` custom colors and referenced
  across the kit — use the global refs (with inline hex fallbacks, as the kit does).

## Palette
| Role | Global id | Hex | Use |
|---|---|---|---|
| Brand blue | `408e485` | `#0C4096` | headings, card titles, dark bands, overlays |
| White | `7f92ea2` | `#FFFFFF` | text on dark, light bg |
| Black/text | `be5c055`/`text` | `#222222` | body, button text/border |
| Accent gold | `accent` | `#FEBE10` | spectre/icon accents |
| Light-blue band | (inline) | `#EDF4FF` | alternating section bands, cards |
| Gold check | (inline) | `#FAB914` | icon-list check marks |

**Section rhythm:** blue-overlay photo hero → white → light-blue `#EDF4FF` → white →
blue-overlay CTA. Heading color blue `#0C4096` / dark `#222222` on light, white on dark.

## Typography
**Ruda** everywhere. Global type slots: h1 3em bold (`80aa35e`), h2 2.2em bold
(`7549918`), h3 1.8em (`2113601`), subhead 1.2em (`b279f6f`). Give h1 + every section
h2 explicit mobile sizes (globals-only headings don't shrink).

## Button — square, bordered
Black text + 1px black border (`be5c055`), `border-radius:0` (square — NOT a pill),
icon `far fa-arrow-alt-circle-right` row-reverse, **color-only hover** (no
size/shape animation). Primary CTA links to `#contact`. Labels: "Request Service
Online" / "Schedule Your Cooling Service Online."

## Signature components
- **Hero/CTA:** section background image + blue (`#0C4096`) overlay ~0.8, white
  headings, square CTA.
- **Service/issue card:** light-blue `#EDF4FF` bg, radius 12, padding ~20–26.
- **Process/benefits grid:** numbered `spectre-fa-solid-1..5` icon-boxes on a blue or
  light-blue grid. **icon-list:** gold `#FAB914` `fa-check-circle`.
- **FAQ:** `nested-accordion`. Pages carry a Divi-compat `custom_css` + `hide_title:yes`.

## Internal link slugs
`/ac-repair/`, `/air-conditioner-maintenance/`, `/air-conditioner-installation/`,
`/ac-replacement/`, `/mini-splits/`; primary CTA `#contact`. Phone `(919) 896-8630`
(`tel:+19198968630`).

## Closest page to mirror
`content/page/233246.json` (AC Repair) — the richest existing service page.

## Voice
Local, family-owned, 25+ years, dual-trade (HVAC + plumbing), honest upfront pricing,
0% financing, plain-English, no hard-sell. Tagline "Better Air. Better Life."
