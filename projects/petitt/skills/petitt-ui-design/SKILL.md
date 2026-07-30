---
name: petitt-ui-design
description: >
  UI/visual design system for building Petitt Heating & Cooling pages in Elementor
  (Hello Elementor theme, Container model). Use whenever creating, styling, or
  reviewing a Petitt page, section, hero, card grid, FAQ, or button so it matches the
  existing kit. Covers palette + roles, the Oswald uppercase type scale, the red pill
  button, the boxed section structure, the brand pattern overlays, emoji icons,
  responsive rules, and a review checklist. Triggers: "new Petitt page", "style this
  section", "match the Petitt kit", "Petitt brand colors/fonts/buttons".
---

# Petitt Heating & Cooling — UI Design System

Apply this when building or styling any Petitt Elementor page. Middle Tennessee
HVAC + plumbing contractor on **Hello Elementor** with Elementor Pro (Container model,
no legacy sections). Full evidence lives in `projects/petitt/KIT-ANALYSIS.md`; the
machine-readable values live in `projects/petitt/tokens.json`.

**Globals are REAL here.** The kit references `globals/colors?id=…` ~3,900 times and
its `site-settings.json` holds true brand values. Use the global refs (with an inline
hex alongside, which is what the kit's own pages do).

## 1. Palette + roles

| Role | Global | Hex | Use for |
|---|---|---|---|
| White | `a23a917` | `#FFFFFF` | text on dark bands, card fills |
| **Navy (working primary)** | `secondary` | `#2B2E81` | hero band, H3 card titles, phone button |
| Red (accent) | `accent` | `#EC2024` | link hover, icon-box icons |
| **CTA red** | — | `#D90000` | button background (inline, as the kit does) |
| CTA red hover | — | `#AF0000` | button hover background |
| Text | `text` | `#171925` | body + headings on light bands |
| Soft Gray | `fd5335f` | `#FAFAFA` | the alternating light band, card fill |
| Blue-2 | `bd6963d` | `#191C64` | deep-navy bands, icon-box titles |
| Tint | — | `#F1F2FF` | gradient partner in card fills |
| Glass | — | `#FFFFFFE6` / `#FFFFFFCF` | content card over a photo/pattern band |
| Light blue | `primary` | `#47A3DA` | **accent border only** — never a section color |

⚠️ The slot literally named `primary` is a 2px bottom-border accent (6 uses kit-wide).
Do not treat it as the brand color.

## 2. Type scale — Oswald, UPPERCASE

Headings: **Oswald**, `text-transform: uppercase`, letter-spacing −0.02em, color
`#171925` (white on dark bands). Body: **Montserrat 400 / 16px**, line-height 1.6.

| Tag | Desktop | Mobile | LH |
|---|---|---|---|
| h1 | 3.2em | 2.4em | 1.05 |
| h2 | 2.4em | 2.0em | 1.1 |
| h3 | 1.8em | 1.6em | 1.15 |
| h4 | 1.5em | 1.35em | 1.2 |
| h5 | 1.25em | 1.15em | 1.3 |
| lead | 1.35em bold | 1.2em | 1.4 |

Write headings in **sentence case** — the theme renders them uppercase. Emit the sizes
inline in `em` at exactly these values: it changes nothing visually and it satisfies the
responsive gate (a heading that only references a global will not shrink on mobile).

An eyebrow above an H2 uses the `uppercase-pre-title` treatment: bold, uppercase,
0.2em letter-spacing, red or navy.

## 3. Button spec (the one CTA shape)

```
background        #D90000              hover background  #AF0000
text              #FFFFFF              hover text        #FFFFFF (global a23a917)
typography        Montserrat bold, ~19px (1.2em)
radius            100px (full pill)    border            none
padding           15px 25px            box-shadow        global (0 4 12 rgba(0,0,0,.12))
icon              fas fa-chevron-circle-right, icon_align: row-reverse
hover animation   NONE
```

Phone variant: same shape, background = `globals/colors?id=secondary` (navy), icon
`fas fa-phone-alt`. Closing CTAs pair the two side by side (phone first).

**Never add `hover_animation`.** This brand is color-change only.

## 4. Section structure (repo standard + Petitt rhythm)

```
Section            (full-width 100% — background/overlay only, no padding)
  └─ Content Container   (BOXED to 1140px — carries padding 70/20; 980px for FAQ)
       └─ content        (headings, text, buttons, rows, grids, accordion)
```

Content widgets sit **directly** in the boxed container. Add a nested container only for
a real layout need (two-column row, card, grid). Nested rows/columns get zero padding.

**Band rhythm** for a service-area page:
`navy hero → soft-gray → navy or photo → soft-gray → white → soft-gray → photo + glass CTA`

**Pattern overlays are the brand signature.** Layer a divider PNG as
`background_overlay_image` over a flat band:
- hero → `Petitt_WebSectionDividers-03.png` (id 717) over navy
- light bands → `Petitt_WebSectionDividers-01.png` (id 715) over `#FAFAFA`
Over a photo band, put content in a **glass card**: `#FFFFFFE6`, radius 15, padding 20,
`css_classes: is-blurred-background`.

## 5. The patterns to reuse (don't invent new ones)

- **Hero** — navy band, `css_classes: hero-pages`, rating badge (`rating` widget, stars
  `#C9D323`) + "5.0 (1000+ Reviews)" in white bold, white H1, white lead paragraphs,
  one or two CTAs; optional right-hand image, height 400, radius 12.
- **Trust bar** — a thin strip directly under the hero: 3 short proof points, each an
  emoji or `icon-box` + one line, in a row that stacks on mobile. Navy or soft-gray.
- **Card Component Grid** — grid (3 cols desktop / 2 tablet / 1 mobile) of cards:
  `#FAFAFA` fill (or `#FAFAFA→#F1F2FF` gradient), radius 15, padding 15–20, shadow
  `0 4 16 rgba(0,0,0,.15)`; inside → white rounded box with the service icon SVG →
  **H3 (navy, centered)** → body → red button, centered. This is what the client means
  by "Card Component Grid".
- **Service icons** (already in the media library — reuse the IDs from `tokens.json`):
  AC 705 · Heat 707 · Plumbing 708 · Air Quality 706.
- **Icon-box strip** — `icon-box`, `position: inline-start`, icon 30px accent red,
  title h5, description `.9em`.
- **FAQ** — `nested-accordion`, `title_tag: h3`, `fas fa-chevron-down` / `-up`, 250ms,
  inside a 980px boxed container.
- **Closing CTA** — photo band → glass card → H2 + short text → row: navy `tel:` button
  + red schedule button.

## 6. Emoji icons (mix them in)

Where an icon accents content (benefit lists, step markers, trust points), use an
**emoji in a heading/text widget** so a page never depends entirely on Font Awesome —
⭐ 🔧 🔥 🚿 💨 🏠 ✅ 📞 💳 🛡️. Keep genuine icon widgets where the kit uses them (the
button chevron, icon-boxes, the accordion chevrons). Save JSON as **UTF-8**.

## 7. Images & media

- Reuse existing attachment IDs from `tokens.json` `media` so images resolve after
  import instead of needing a re-upload.
- Every image gets **alt text**. Fixed-height images get `height_mobile`.
- Hero/feature images: 400–440px height, radius 12–15, `object-fit: cover`.
- Live widgets (Google Maps iframe, review sliders) stay as an `html` widget — carry the
  existing markup over verbatim; don't rebuild them.

## 8. Responsive rules (the gate)

- grids: `grid_columns_grid_tablet` 2, `grid_columns_grid_mobile` 1
- flex rows: `flex_direction_mobile: column`
- %-width columns: `width_tablet` + `width_mobile` = 100%
- **H1 and every H2** carry `typography_font_size_mobile` (and tablet)
- boxed containers carry `padding_mobile` (≈45/18)
- fixed-height images carry `height_mobile`

## 9. Review checklist

- [ ] Exactly one H1; heading levels don't skip.
- [ ] Headings Oswald + uppercase at the scale in §2; body Montserrat 16px.
- [ ] CTA buttons `#D90000`/pill/chevron, **no hover animation**; phone button navy.
- [ ] Band rhythm alternates; pattern overlay on hero + at least one light band.
- [ ] Every section = full-width Section → one boxed 1140px container → content.
- [ ] Cards use the §5 spec; service icons reuse existing media IDs.
- [ ] Emoji mixed in with native icons.
- [ ] All §8 responsive settings present.
- [ ] No `display_condition_list`; no dead (`#`) or `localhost` links.
- [ ] JSON complete and UTF-8; unique element ids.
