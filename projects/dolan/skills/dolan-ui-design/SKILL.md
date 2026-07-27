---
name: dolan-ui-design
description: >
  UI/visual design system for building Dolan Design HVAC pages in Elementor (Divi
  child theme). Use whenever creating, styling, or reviewing a Dolan page, section,
  hero, card, or button so it matches the existing kit. Covers palette, typography,
  the square bordered button, the boxed section structure, emoji icons, layout, and a
  review checklist. Triggers: "new Dolan page", "style this section", "match the kit",
  "Dolan brand colors/fonts/buttons".
---

# Dolan Design HVAC — UI Design System

Apply this when building or styling any Dolan Design (dolandesignhvac.com) Elementor
page. Louisburg, NC HVAC & plumbing company on a **Divi child** theme with Elementor
Pro.

**Globals are REAL here.** Dolan's Elementor color globals are defined in
`site-settings.json` (custom colors) and the kit references them everywhere. Use the
global refs below (with inline hex fallbacks, as the kit does) rather than fighting
them.

## Color palette

| Role | Global ref (`globals/colors?id=`) | Hex | Use for |
|------|-----------------------------------|-----|---------|
| Brand blue | `408e485` | `#0C4096` | Headings, card titles, dark bands, overlays |
| White | `7f92ea2` | `#FFFFFF` | Text on dark, light bg |
| Black / text | `be5c055` / `text` | `#222222` | Body text, button text/border |
| Accent gold | `accent` | `#FEBE10` | Icon/spectre accents |
| Light-blue band | *(inline)* | `#EDF4FF` | Alternating section bands, cards |
| Gold check | *(inline)* | `#FAB914` | icon-list check marks |

**Section rhythm — alternate backgrounds**: `blue-overlay hero → white → light-blue
#EDF4FF → white → blue-overlay CTA`. Never place two identical backgrounds back to
back. Heading color: blue `#0C4096` / dark `#222222` on light, white on dark bands.

## Typography

**Ruda** everywhere. Global type slots: h1 3em bold (`80aa35e`), h2 2.2em bold
(`7549918`), h3 1.8em (`2113601`), headline/subhead 1.2em (`b279f6f`).

| Level | Size | Weight |
|-------|------|--------|
| Hero (h1) | 3em (mobile ~2.1em) | bold |
| Section (h2) | 2.2em (tablet 1.9 / mobile ~1.55em) | bold |
| Sub / card (h3) | 1.35–1.8em | bold |
| Subhead | 1.2em | 400 |
| Body | ~1em | 400 |

Give **h1 and every section h2** explicit mobile sizes. (A heading pointing at a
global type slot with no mobile size won't shrink — use self-contained responsive
sizes on section headings.)

## Button — square, bordered (match the kit)

```
text + border: black (globals button_text_color / border_color = be5c055 #222222)
border:        1px solid, border-radius: 0 (square — NOT a pill)
icon:          far fa-arrow-alt-circle-right, icon_align row-reverse
link:          #contact  (primary CTA anchor)
hover:         color change only (no size/shape animation)
```

Keep buttons **square** and bordered — that's the Dolan signal. Label: "Request
Service Online" / "Schedule Your Cooling Service Online."

## Section structure (REQUIRED — every section)

```
Section                 (full-width 100% — background only, NO padding)
└── Content Container    (BOXED to the site width ~1140px — carries the padding)
    └── content          (headings, text, buttons, and multi-column rows/grids)
```

1. **Outer Section** — full-width, carries background (color, or bg image + blue
   overlay at ~0.8 opacity for hero/CTA) and the rhythm. No padding.
2. **Content Container** — one boxed container (`content_width:"boxed"`,
   `boxed_width: ~1140px`). The **only** padded element (desktop ~70px top/bottom, or
   100px for hero; `padding_mobile` smaller).
3. **No excess containers** — a lone image/text sits directly in the boxed container.
   Add a nested container only for a genuine two-column row, a card with its own
   background, or a repeated-item grid. Nested containers get **zero padding**.
4. **Variety** — mix layouts (two-column text+image, icon-box card grids, numbered
   spectre-icon process/benefit grids, accordions).

## Icons — mix emoji with widgets

Don't depend solely on FontAwesome/Spectre. Use **emoji as icons** for card headers
and benefit lists (in a heading/text widget — large size for a card "icon", inline
for a list line). Save JSON as UTF-8. Keep native icons where they fit (button arrow,
`fas fa-check-circle` icon-lists, `spectrefa- spectre-fa-solid-N` numbered steps).

## Signature components

- **Hero / CTA band:** section background image + blue (`#0C4096`) overlay ~0.8, white
  H1/H2 + text + square CTA button.
- **Service/issue card:** light-blue `#EDF4FF` bg, radius 12, padding ~20–26 →
  emoji or check icon + h3 (blue) + body (+ optional button).
- **Process / benefits grid:** blue or light-blue grid container with numbered
  `spectre-fa-solid-1..5` icon-boxes.
- **icon-list:** gold `#FAB914` `fa-check-circle`, Ruda ~0.9em.
- **FAQ:** `nested-accordion`.

## Layout & responsive

- Container/flex model. Multi-column **grids** set `grid_columns_grid_tablet` (~2) +
  `_mobile` (1); **flex rows** set `flex_direction_mobile:column`; **%-width columns**
  set `width_mobile:100%` (+ `width_tablet`); fixed-height **images** set
  `height_mobile`.
- Run `scripts/responsive-audit.py <page>.json` before delivery (see page-audit).

## Output completeness

Emit the **complete** JSON — never `// ...`. Unique `id` per element; required keys
intact; save UTF-8. Single-page wrapper
`{"version":"0.4","title":"…","type":"page","content":[…],"page_settings":{"template":"default","hide_title":"yes"}}`
(the kit pages also carry a Divi-compat `custom_css` block — include it).

## Review checklist

Every section = full-width Section → one boxed (~1140px) Content Container → content;
padding only on the container (+ self-contained cards); alternating backgrounds;
square bordered CTAs (color-only hover); Ruda; blue/gold palette via real globals +
inline; emoji icons mixed in; root-relative links + `#contact` CTA; one H1 → clean
H2/H3; responsive audit passes; every image has alt text.
