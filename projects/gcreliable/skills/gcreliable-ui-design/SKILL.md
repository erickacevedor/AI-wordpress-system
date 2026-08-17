---
name: gcreliable-ui-design
description: >
  UI/visual design system for building G.C. Reliable Service (gcreliable.com) pages
  in Elementor (Hello Elementor Child). Use whenever creating, styling, or reviewing
  a GC Reliable page, section, hero, card, or button so it matches the existing kit.
  Covers palette, typography, the square red CTA, the boxed 1280px section
  structure, the signature components, and a review checklist. Triggers: "new GC
  Reliable page", "style this section", "match the kit", "GC Reliable brand
  colors/fonts/buttons".
---

# G.C. Reliable Service — UI Design System

Apply this when building or styling any G.C. Reliable Elementor page. Westchester
County, NY HVAC contractor on **Hello Elementor Child** with Elementor Pro 4.x.

**Globals are REAL here.** `site-settings.json` carries the true brand and the kit
references it. Use the global refs below with an inline hex alongside (which is what
the reference page does), *except* for the light band tints — see the ⚠️ below.

The canonical models are the agency's own hand-off templates —
`templates/227368.json` (*AC Repair – Full Page*) and `templates/227376.json`
(*Cooling Services – Full Page*) — plus the published page
`content/page/225063.json`, which is `227368` with real photos and the live
Trustindex shortcode in place of its placeholders. When in doubt, open them and copy
the pattern. **`templates/225540.json` "Design Guide" is an unfilled boilerplate
whose colour globals don't exist in this kit — never take brand values from it.**

## Color palette

| Role | Global ref (`globals/colors?id=`) | Hex | Use for |
|------|-----------------------------------|-----|---------|
| Primary blue | `primary` | `#0033CC` | Headings accents, icons, step bars, hero gradient start, link color |
| Brand red | `secondary` | `#FF0000` | **All CTAs**, stat numbers, warning-card titles, badge left border |
| Dark blue | `581507c` | `#001E78` | Hero / CTA gradient end |
| Text | `text` | `#1A1A1A` | Headings + body on light bands |
| White | `63acc82` | `#FFFFFF` | Cards, text on gradient bands |
| Grey 1 | `07e47d8` | `#C5C5C5` | Accordion + dashed review-band borders |

**Band tints — inline these, don't use globals** (two conflicting `custom_colors`
sets share ids in this kit):

| Tint | Hex | Use for |
|---|---|---|
| Mist | `#EFF2F5` | The alternating light band |
| Blue tint | `#E6ECFA` | Photo-container fallback fill |
| Step grey | `#F8F8FB` | Numbered process cards |

**Section rhythm — alternate backgrounds**, exactly as the reference page does:

```
gradient hero → white → #EFF2F5 → white → #EFF2F5 → white → gradient → #EFF2F5
```

Never two identical bands back to back. Gradient = **linear 135°, `#0033CC → #001E78`**.
Heading color `#1A1A1A` on light bands, `#FFFFFF` on gradient bands.

## Typography — one family: `brandon-grotesque`

690 of 694 font references in the kit. Do not introduce another family.
All headings carry `letter-spacing: 0.5px`.

| Level | Size | Weight | Mobile | Notes |
|-------|------|--------|--------|-------|
| H1 hero | 3.4rem | 800 | 2.2rem | `uppercase`, lh 1.1 / mobile 1.05, white |
| Hero sub-line | 1.5rem | 400 | 1.2rem | heading widget, no `header_size` |
| H2 section | 2.2rem | 500 | ~1.6rem | `#1A1A1A`, `_margin` bottom 4px |
| H3 card | 1.5rem | 500 | — | red when it's a warning card |
| H3 step | 1.35rem | 500 | — | prefixed with a blue `01.` span |
| H3 stat number | 2.4rem | 800 | — | red |
| H4 stat label | 1rem | 500 | — | lh 1.25 |

> **Body copy gets NO local typography.** Emit `text-editor` widgets as
> `{"editor": "<p>…</p>"}` and let them inherit the global *Normal Text*
> (brandon-grotesque 18px / lh 1.5). Centre body copy with
> `<p style="text-align:center;">` inside the HTML, not with an `align` setting.

Give **H1 and every H2** an explicit `typography_font_size_mobile` (globals-only
headings don't shrink).

## Button — square red, colour-only hover

```
size:          xl        _element_width: auto      align: center (or left in a row)
background:    #FF0000   (globals background_color = secondary)
text:          #FFFFFF   (globals button_text_color = 63acc82)
border:        2px solid #FF0000 (globals border_color = secondary)
radius:        NONE — square corners
font:          brandon-grotesque 1rem / weight 600 / uppercase / letter-spacing 1.2px
icon:          far fa-calendar-check, icon_indent 10 (icon sits BEFORE the label)
HOVER:         background + border → #FF6464, text → #FFFFFF
transition:    button_hover_transition_duration = 0s
```

**Do not add `hover_animation`.** This site's convention is colour-only (that
`shrink` bounce belongs to Magnolia). Default CTA link `/schedule-appointment`.

## Section structure (REQUIRED — every section)

```
Section                 (full-width 100% — background only, NO padding)
└── Content Container    (BOXED to 1280px — carries the padding)
    └── content          (headings, text, buttons, and multi-column rows/grids)
```

1. **Outer Section** — `content_width: full`, `flex_align_items: center`, carries the
   background and the rhythm. Padding `64/20/64/20` (hero `90`, gradient CTA `68`),
   `padding_mobile` `40/16/40/16`.
2. **Content Container** — one boxed container: `boxed_width` **1280px**,
   `boxed_width_laptop` 92%, `_tablet`/`_mobile` 100%, `flex_gap` 22 (hero 16).
3. **No excess containers** — a lone heading/text sits directly in the boxed
   container. Nest only for a genuine row, a self-contained card, or a grid; those
   get zero padding of their own.
4. **Variety** — mix two-column rows, wrapping card rows, grids, and the accordion.
   Never a stack of single-column text blocks.

## Signature components — reuse, don't invent

**Photo + floating stat badge** (the page's hero-adjacent visual):
container with `background_image`, `min_height` 380 (mobile 230), radius 12,
shadow `0 16 40 -14 rgba(0,0,0,.30)`; beneath it a white badge card at `width` 62%
(mobile 82%), `_flex_align_self: flex-start`, `margin` top `-72` (mobile `-40`) /
left `26`, `z_index: 3`, **5px left border `#FF0000`**, holding a red H3 number
+ an H4 label.

**Icon list** — `icon-list`, `fad fa-check-circle` (Font Awesome Duotone),
`icon_size` 20, `text_indent` 8, `space_between` 14–16. Blue icon + `#1A1A1A` text on
light bands; white + white on the gradient band. Lead each item with
`<strong>Label:</strong>` when it's a benefit list.

**Numbered process card** — `#F8F8FB` fill, radius 10, **4px left border `#0033CC`**,
padding `6/0/6/20`, `width` 48% (mobile 100%) in a wrapping flex row with gap 20.
Title = `<span style="color:#0033CC;font-weight:700;">01.</span>&nbsp; Title`.

**White info card** — `#FFFFFF`, radius 12, padding 28, shadow
`0 10 30 -10 rgba(0,0,0,.18)`.

**Stat trio** — three 32%-wide (mobile 100%) white cards, centred, each an `icon`
widget (40px, `#0033CC`) + big H3 + small H4 label.

**Review band** — dashed 2px `#C5C5C5`, radius 20, padding 30/24, off-white fill,
wrapping a `shortcode` widget holding
`[trustindex data-widget-id=be35b8a27428268b9b962ab1e27]` on a white radius-15 inset.

**Service card** (`227376` §2 — use this whenever a card links to another page):
white, radius 12, padding 28, gap 10, 48% wide (mobile 100%) → media block →
`icon` widget at **38px in red** → **H3 1.4rem whose title is a blue `#0033CC`
link** → body → a text widget with
`<a … style="color:#FF0000;font-weight:700;">Learn more &rarr;</a>`.
`brand.service_card()` builds it; pass `emoji_ch` to swap the FA icon for an emoji.

**Image placeholder** (`brand.image_placeholder()`): the agency ships photo slots as a
`#E6ECFA` block, `min_height` 190 (mobile 230), radius 12, centred, holding
`▢  Image placeholder` (H4, `#7C8DB5`, 1.05rem) + a 0.8rem caption **describing the
intended photo** and telling the importer to set it as the container's Background →
Image. Use it whenever the right asset isn't already in the media library; use
`brand.photo_block()` when it is.

**Gradient trust band ends in a CTA.** `227376` closes its blue band with a red
`Learn More About G.C. Reliable` → `/about-us` button. Include it.

**FAQ** — Elementor **Pro `accordion`** widget with a `tabs` array (not
`nested-accordion`): `title_color #1A1A1A`, `tab_active_color #0033CC`,
`icon_color #FF0000`, `icon_active_color #0033CC`, titles brandon 1.25rem/500,
content brandon, 1px `#C5C5C5` border. Put it at `width` 62% in a row beside a
34%-wide white "Still have questions?" card with a CTA button.

## Icons — mix emoji with widgets

Font Awesome Pro is live, so `fad`/`fas`/`far` icons render — but never let a page
depend entirely on the icon font. Use **emoji as icons** (a heading/text widget) for
card headers and option cards, alongside the FA icon lists and icon widgets.
Save JSON as UTF-8. Recurring choices: 📐 sizing · 🧭 evaluation · 🧾 options ·
✅ verification · 🌀 cooling · 🔧 repair · 🧰 maintenance · 🏠 home · 🚨 emergency ·
❄️ ductless · 🗂️ zones.

## Layout & responsive

- Container/flex model (not legacy Section→Column).
- **Grids** set `grid_columns_grid_tablet` (~2) + `_mobile` (1); **flex rows** set
  `flex_direction_mobile: column` (the reference intro row uses `column-reverse` on
  tablet+mobile so copy leads); **%-width columns** set `width_mobile: 100%`
  (+ `width_tablet`); fixed-height **images** set `height_mobile`.
- Wrapping card rows use `flex_wrap: wrap` + `flex_gap_mobile` ~28.

## Page settings

`{"template": "elementor_header_footer", "hide_title": "yes"}` — the current
generation. (Legacy pages use `"default"` + an ACF hero; don't follow those.)

## Output completeness

Emit the **complete** JSON — never `// ...` or "other sections follow." Unique `id`
per element; required keys (`elType`/`widgetType`/`elements`/`settings`) intact; save
UTF-8. Wrap single pages as
`{"version":"0.4","title":"…","type":"page","content":[…],"page_settings":{…}}`.

## Review checklist

Every section = full-width Section → one boxed (1280px) Content Container → content;
padding only on the container (+ self-contained cards); the alternating band rhythm;
square red CTAs with the colour-only `#FF6464` hover and **no** hover animation;
brandon-grotesque throughout with unstyled body text; emoji mixed with FA icons;
**no `display_condition_list`**; root-relative `/systems/...` links; one H1 → clean
H2/H3; `scripts/validate-page.py` exits 0; every image has alt text.
