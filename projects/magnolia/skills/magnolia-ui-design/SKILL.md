---
name: magnolia-ui-design
description: >
  UI/visual design system for building Magnolia Air HVAC pages in Elementor (Astra
  theme). Use whenever creating, styling, or reviewing a Magnolia page, section,
  hero, card, or button so it matches the existing kit. Covers palette, typography,
  the gold pill button, the boxed section structure, emoji icons, layout, and a
  review checklist. Triggers: "new Magnolia page", "style this section", "match the
  kit", "Magnolia brand colors/fonts/buttons".
---

# Magnolia Air — UI Design System

Apply this when building or styling any Magnolia Air Elementor page. Central
Louisiana HVAC company on an **Astra** theme with Elementor Pro.

**Globals are REAL here.** Unlike some kits, Magnolia's Elementor globals hold the
true brand values, and the kit references them everywhere. Use the global refs
below (with an inline hex fallback where useful) rather than fighting them.

## Color palette

| Role | Global ref (`globals/colors?id=`) | Hex | Use for |
|------|-----------------------------------|-----|---------|
| Primary teal | `primary` | `#0C4F4D` | Headings on light, teal bands, button hover |
| Gold | `secondary` | `#D4B351` | Button bg, accents, some section bands |
| Gold (accent) | `accent` | `#D7B755` | Accent |
| Dark teal | `fc26636` | `#00333F` | Dark hero/CTA bands, dark headings |
| White | `1d0e19b5` | `#FFFFFF` | Text on dark, light bg |
| Black | `1225c831` / `text` | `#000000` | Body text on light |
| Cream tint | *(inline)* | `#F3EBD6` | Light alternating section band |

**Section rhythm — alternate backgrounds** down the page, e.g.
`dark #00333F hero → cream #F3EBD6 → white → cream → white → teal #0C4F4D → dark → cream → teal`.
Never place two identical backgrounds back to back. Heading color: teal `#0C4F4D` on
light bands, white on dark/teal bands.

## Typography

| Level | Family | Size | Weight |
|-------|--------|------|--------|
| Hero (h1) | **Como-ExtraBold** | ~46px (mobile ~29) | 800 |
| Section (h2) | Como-ExtraBold | ~33px (mobile ~24) | 800 |
| Sub / card (h3) | Como-ExtraBold | ~22px (mobile ~20) | 800 |
| Body | **BeVietnamPro-Light** | ~17px (mobile ~15), line-height 1.7 | 300 |
| Button / emphasis | **BeVietnamPro-ExtraBold** | ~20px | 500 |

Do not introduce other fonts (Roboto/Sora appear in theme chrome only; Corinthia is
a rare decorative script — avoid unless matching a specific block). Give **h1 and
every h2** explicit `typography_font_size_mobile`/`_tablet` (globals-only headings
don't shrink).

## Button — gold pill (match the site's hover)

```
text:        white (globals button_text_color = 1d0e19b5)
background:   gold  (globals background_color = secondary #D4B351)
border:       2px solid gold (globals border_color = secondary)
radius:       50px (full pill)
padding:      ~16px / 34px (top-bottom / left-right)
font:         BeVietnamPro-ExtraBold ~20px, weight 500, text-transform capitalize
HOVER:        background + border → teal (globals *_hover_color = primary #0C4F4D),
              text → white, hover_animation = "shrink"
```

**Note:** Magnolia's brand button uses `hover_animation: "shrink"` — keep it. (This
differs from Dolan/VitalAir which are color-only. Match *this* site.) Default CTA
link is `/request-service/`.

## Section structure (REQUIRED — every section)

```
Section                 (full-width 100% — background only, NO padding)
└── Content Container    (BOXED to the site width ~1140px — carries the padding)
    └── content          (headings, text, buttons, and multi-column rows/grids)
```

1. **Outer Section** — full-width, carries background (color via global/inline) and
   the section rhythm. No padding.
2. **Content Container** — one boxed container (`content_width:"boxed"`,
   `boxed_width: ~1140px` = the site's content width). The **only** padded element:
   desktop ~70px top/bottom / 20px sides; `padding_mobile` ~45/18.
3. **No excess containers** — a lone image or text sits directly in the boxed
   container; don't double-wrap it. Add a nested container only for a genuine
   two-column row, a card with its own background, or a repeated-item grid. Those
   nested containers get **zero padding**.
4. **Variety** — mix layouts (two-column text+image, card grids, accordions), not a
   stack of single-column blocks.

## Icons — mix emoji with widgets

Don't depend solely on icon fonts. Use **emoji as icons** for card headers, benefit
lists, and step markers (in a heading/text widget — large size for a card "icon",
inline for a list line). Save JSON as UTF-8. Keep some native styling where it fits.
Recurring choices: 🔧 repair · 🧰 maintenance · 📐 install · ♻️ replacement ·
⚙️ tune-up · 🚨 emergency · 🏠 home · 🏢 business · 📞 24/7 call-out.

## Signature components

- **24/7 call-out:** stacked "📞 24/7 Emergency Service" (BeVietnamPro-Light ~20px) +
  phone `(318) 233-9318` in Como-ExtraBold ~34px, **gold**, linked `tel:318-233-9318`.
  Use emoji rather than the kit's `moesalley.com` phone image to avoid a broken asset.
- **Service card:** white bg, thin gold-tint border (`#E4D9B8`), radius 14, padding
  26 → emoji icon + h3 (teal) + body + gold pill button linking to the service page.
- **FAQ:** `nested-accordion`, item titles in Como-ExtraBold.

## Layout & responsive

- Container/flex model (not legacy Section→Column).
- Multi-column **grids** set `grid_columns_grid_tablet` (~2) + `_mobile` (1);
  **flex rows** set `flex_direction_mobile:column`; **%-width columns** set
  `width_mobile:100%` (+`width_tablet`); fixed-height **images** set `height_mobile`.
- Run `scripts/responsive-audit.py <page>.json` before delivery (see page-audit).

## Reusable templates

`templates/*.json` holds the header, footer, and reusable blocks — reuse the header
and footer as-is rather than rebuilding chrome.

## Output completeness

Emit the **complete** JSON — never `// ...` or "other sections follow." Unique `id`
per element; required keys (`elType`/`widgetType`/`elements`/`settings`) intact; save
UTF-8. Wrap single pages as
`{"version":"0.4","title":"…","type":"page","content":[…],"page_settings":{"template":"default"}}`.

## Review checklist

Every section = full-width Section → one boxed (~1140px) Content Container → content;
padding only on the container (+ self-contained cards); alternating backgrounds;
gold pill CTAs with the `shrink` hover; Como-ExtraBold headings + BeVietnamPro body;
emoji icons mixed in; **no `display_condition_list` gates**; root-relative links;
one H1 → clean H2/H3; responsive audit passes; every image has alt text.
