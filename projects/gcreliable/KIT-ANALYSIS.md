# KIT-ANALYSIS — G.C. Reliable Service (gcreliable.com)

What the exported Elementor kit in `current-theme/` actually contains, and why
`tokens.json` holds the values it does. Everything below was mined from the export
(manifest, `site-settings.json`, `content/`, `templates/`), not assumed.

- **Site:** https://gcreliable.com — HVAC contractor, New Rochelle, NY / Westchester County, serving since 1980.
- **Theme:** Hello Elementor Child 2.0.0 · Elementor 4.2.2 + Elementor Pro 4.2.1.
- **Kit exported:** 2026-08-14 by Mediagistic. 48 pages, 3 posts, 41 templates.
- **Notable plugins that affect page building:** ACF Pro (hero fields), Gravity Forms,
  Trustindex (Google-review widgets), Happy Addons (leaves a harmless
  `ha_cmc_text: "Happy Addons"` key on every element).

---

## 1. The palette is REAL

`site-settings.json` is **not** a Hello-Elementor default — the globals carry the true
brand and the kit references them widely (`__globals__` appears on nearly every styled
widget in the newest pages).

**System colors**

| Role | Global id | Hex |
|---|---|---|
| Primary | `primary` | `#0033CC` (brand blue) |
| Secondary | `secondary` | `#FF0000` (brand red — CTAs, accents) |
| Text | `text` | `#1A1A1A` |
| Accent/Links | `accent` | `#0033CC` |

**Custom colors** — `581507c` Dark Primary `#001E78` · `df060b8` Dark Secondary
`#AB0000` · `63acc82` White · `3ff4adf` Black · `4f0dee9` Off-White · `07e47d8`
Grey 1 `#C5C5C5` · `c460b15` Grey 2 · `4b3db79` Grey 3 `#1A1A1A` · `ae62a7e` Dark
Blue Overlay `#0033CCA8` · `98f7548` Full Transparent.

> **Gotcha — duplicated custom-color ids.** `custom_colors` contains the same ten
> `_id`s **twice**: an older palette (`#001E78`, `#AB0000`, Off-White `#F7F7F7`,
> Grey 2 `#3C3C3B`) followed by a newer one (`#0C4D86`, `#FFBE00`, Off-White
> `#EFF2F5`, Grey 2 `#6C757D`). The pages that actually ship use the **first**
> set's dark blue `#001E78` and the **second** set's Off-White `#EFF2F5`. Because a
> global id resolves ambiguously here, the newest page (AC Repair) writes the light
> band as an **inline `#EFF2F5`** and only uses `globals/colors?id=4f0dee9` where a
> mismatch would be invisible. Do the same: inline the band hexes, use globals for
> primary/secondary/white where the kit already does.

**Light-band tints seen in real pages:** `#EFF2F5` (alternating band), `#E6ECFA`
(photo placeholder tint), `#F8F8FB` (numbered-step card).

## 2. Typography

**One family, everywhere: `brandon-grotesque`** — 690 of 694 `typography_font_family`
occurrences in the kit. (Rubik / Montserrat / Figtree / Battambang appear once each in
dead theme chrome; ignore them.)

Global typography styles: *Sans Serif* (`secondary`), *Serif* (`primary`), *Normal
Text* (`text`, 18px / lh 1.5rem / ls 0.5px), *Uppercase* (`accent`), plus custom
*Widget Title* and *Page H1 Title*.

Scale mined from the reference page (all `rem`, all brandon-grotesque, letter-spacing
`0.5px` on headings):

| Level | Size | Weight | Mobile | Notes |
|---|---|---|---|---|
| H1 hero | 3.4 | 800 | 2.2 | `text-transform: uppercase`, lh 1.1 (mobile 1.05) |
| Hero sub-line | 1.5 | 400 | 1.2 | plain heading widget, no `header_size` |
| H2 section | 2.2 | 500 | — | `#1A1A1A`, `_margin` bottom 4px |
| H3 card title | 1.5 | 500 | — | red `#FF0000` when it is a warning card |
| H3 step title | 1.35 | 500 | — | prefixed `<span style="color:#0033CC;font-weight:700;">01.</span>&nbsp;` |
| H3 stat number | 2.4 | 800 | — | red |
| H4 stat label | 1.0 | 500 | — | lh 1.25 |

> **Body copy carries NO typography settings.** Every `text-editor` on the reference
> page is `{"editor": "<p>…</p>"}` and nothing else, so it inherits the global
> *Normal Text*. Keep it that way — styling body text locally is what breaks brand
> consistency here. Centered body copy is done with `<p style="text-align:center;">`
> inside the editor HTML, not with an `align` setting.

## 3. The button — square red, colour-only hover

```
size:            xl            _element_width: auto      align: center | left
background:      #FF0000  (globals/colors?id=secondary)
text:            #FFFFFF  (globals/colors?id=63acc82)
border:          2px solid #FF0000 (globals/colors?id=secondary)
border-radius:   none — SQUARE corners
font:            brandon-grotesque 1rem / 600 / uppercase / letter-spacing 1.2px
icon:            far fa-calendar-check, icon_indent 10 (icon before the label)
HOVER:           background + border → #FF6464, text → #FFFFFF
transition:      0s  (button_hover_transition_duration)
```

**Hover convention: colour-only.** No `hover_animation` — do **not** add `shrink`
(that is Magnolia's convention, not this site's). Default CTA target
`/schedule-appointment`.

## 4. Section rhythm & structure

The current-generation page (AC Repair, id 225063) is built exactly to the repo
standard: full-width band → **one boxed container** → content.

- Outer band: `content_width: full`, `flex_align_items: center`, padding
  `64/20/64/20` (hero `90`, dark CTA band `68`), `padding_mobile` `40/16/40/16`.
- Boxed container: `boxed_width` **1280px**, `boxed_width_laptop` 92%,
  `_tablet`/`_mobile` 100%, `flex_gap` 22 (hero 16).
- Background sequence actually shipped:
  `gradient hero → white → #EFF2F5 → white → #EFF2F5 → white → gradient → #EFF2F5`.
  Never two identical bands in a row.
- Hero/CTA gradient: linear **135°**, `#0033CC → #001E78`. Hero also sets
  `min_height: 44vh` and centres its content.

## 4b. The Templates library — read these BEFORE any page

`templates/` holds 40 entries. Four matter for page building, and they are the
agency's own hand-off guides (created by *exploreweb*, 2026-07-22):

| id | Title | What it is |
|---|---|---|
| `227368` | **GC Reliable – AC Repair (New Rochelle) – Full Page** | The AC Repair page as a reusable template |
| `227376` | **GC Reliable – Cooling Services (New Rochelle) – Full Page** | The *hub* page template — a different section mix |
| `227364` | ExampleTemplateforAC | An earlier cut of the AC Repair layout |
| `225540` | Design Guide | ⚠️ **Unfilled boilerplate — do not mine** (see below) |

**`227368` ≡ the published AC Repair page** (`content/page/225063.json`), with two
deliberate differences: photo slots ship as **image placeholders** and the review
slot ships as a *"Google Reviews Slider"* placeholder instead of the live Trustindex
shortcode. Every setting difference beyond that is Elementor serializing empty
defaults (`background_video_fallback: {"url":"","id":"",…}`) in the template export.
So the two are the same design — the page is the filled-in copy.

**`227376` Cooling Services is the one to read for anything hub-shaped.** Its
8-section anatomy is: gradient hero → white intro row (photo+badge) → `#EFF2F5`
**service-card grid** → white 5-step process beside a photo+badge (steps in a 58%
column, photo at 42%) → **gradient trust band that ends in a CTA button** → white
reviews + stat trio → `#EFF2F5` FAQ → `#EFF2F5` closing CTA. Note it puts two
`#EFF2F5` bands back to back at the end — the rest of the kit alternates, so treat
that as a one-off, not the rule.

> ⚠️ **`225540` "Design Guide" is a Mediagistic boilerplate that was never filled in
> for this site.** Every global id its colour swatches and button hovers point at —
> `7c79b22`, `2cc7401`, `3952558`, `f396fdc`, `d9cf1a2`, `329b583`, `6d728d0` — is
> **absent from this kit's `site-settings.json`**, and it carries a stray `#745199`
> purple. It contains no G.C. Reliable brand values. Its only real content is a
> *vocabulary* of button variants (Ghost, Ghost on Dark, Button on Dark, Text + Icon)
> that neither shipped page uses. Take the CTA spec from §3 above, not from here.

## 5. Signature components (copy these, don't invent new ones)

- **Photo + floating stat badge.** A container with a `background_image`,
  `min_height` 380 (mobile 230), radius 12, shadow `0 16 40 -14 rgba(0,0,0,.30)`;
  under it a white badge card, `width` 62% (mobile 82%), `_flex_align_self:
  flex-start`, `margin-top: -72` (mobile `-40`), `margin-left: 26`, `z_index: 3`,
  **5px left border in red**, holding a big red number + a small label.
- **Icon list.** `icon-list` with `fad fa-check-circle` (Font Awesome **Duotone** —
  Pro is active on this site), `icon_size` 20, `text_indent` 8, `space_between`
  14–16; blue icons / `#1A1A1A` text on light bands, white/white on the gradient band.
- **Numbered process card.** `#F8F8FB` fill, radius 10, **4px left border in blue**,
  padding `6/0/6/20`, `width` 48% in a wrapping flex row, title prefixed with a blue
  `01.` span.
- **White info card.** `#FFFFFF`, radius 12, padding 28, shadow `0 10 30 -10
  rgba(0,0,0,.18)`.
- **Stat trio.** Three 32%-wide white cards, centred, each `icon` widget (40px,
  blue) + big H3 + small H4 label.
- **Review band.** Dashed 2px `#C5C5C5` border, radius 20, padding 30/24, off-white
  fill, wrapping a `shortcode` widget with the Trustindex Google-review widget
  `[trustindex data-widget-id=be35b8a27428268b9b962ab1e27]` on a white, radius-15 inset.
- **Service card** (template `227376` §2 — the kit's real card for a hub/grid):
  white, radius 12, padding 28, gap 10, `width` 48% (mobile 100%), containing, in
  order — a **media block** → an `icon` widget at **38px in red** (`fas fa-snowflake`
  etc.) → an **H3 at 1.4rem whose title is a blue `#0033CC` link** → body → a final
  text widget holding `<a … style="color:#FF0000;font-weight:700;">Learn more &rarr;</a>`.
- **Image placeholder** (the agency's hand-off convention, used throughout both
  full-page templates instead of shipping photos): a `#E6ECFA` container,
  `min_height` 190 (mobile 230), radius 12, padding 20, centred, holding an H4
  `▢  Image placeholder` in `#7C8DB5` at 1.05rem plus a 0.8rem caption in the same
  colour that **describes the photo that belongs there** and reminds the importer to
  set it as the container's Background → Image.
- **The gradient trust band ends in a CTA.** `227376` closes its blue band with a red
  `Learn More About G.C. Reliable` → `/about-us` button, and its stat trio uses
  `fas fa-user-shield` / `fas fa-clock` / `fas fa-calendar-check`. The AC Repair page
  omits the button; the hub template has it. Include it.
- **FAQ.** Elementor **Pro `accordion`** widget (`tabs` array) — *not*
  `nested-accordion`. `title_color #1A1A1A`, `tab_active_color #0033CC`,
  `icon_color #FF0000`, `icon_active_color #0033CC`, titles brandon 1.25rem/500,
  1px `#C5C5C5` border. Paired in a row with a 34%-wide white "Still have questions?"
  card carrying a CTA button.

## 6. URL scheme

The live structure is `/systems/<category>[/<service>]`:
`/systems/air-conditioning`, `/systems/air-conditioning/ac-repair`,
`/systems/air-conditioning/ac-installation`, `/systems/ductless-minisplits`,
`/systems/maintenance`, `/systems/heat-pumps`, `/systems/heating`,
`/systems/indoor-air-quality`, `/systems/commercial-hvac`; plus
`/schedule-appointment`, `/contact-us`, `/memberships-specials`, `/financing`,
`/specials`, `/service-area/<city>`, `/about-us`, `/faqs`, `/hvac-news`.

> **Legacy URLs in the kit are dead ends.** Older pages still link to
> `/amana/...` and `/services/...`. Do not copy those — use `/systems/...`, and
> write them **root-relative** (the reference page uses absolute
> `https://gcreliable.com/...`; root-relative is the repo standard and imports
> cleanly into any environment).

## 7. Page settings & the ACF hero

Legacy pages use `{"template": "default"}` and render their hero from ACF fields
(`page_h1_title`, `page_sub-title`, `lead_paragraph`) supplied by a theme template.
The current-generation page switches to
`{"template": "elementor_header_footer", "hide_title": "yes"}` and builds its own
hero inside the Elementor content. **New pages follow the current generation** — full
Elementor hero, `elementor_header_footer`, `hide_title`.

## 8. Other kit facts

- **Contact:** `(914) 326-0726` → `tel:+19143260726` (the newest header/CTA
  templates; an older `914-354-3320` also appears — do not use it).
- **Media with real attachment ids** (safe to reference directly): `227356`
  gc-reliable-technician.webp, `227360` -technician-2.webp, `227379`
  gc-reliable-cooling-services.webp, `227384` gc-reliable-3.webp. Topical stock for
  these services (`2025/03/AC-installation-…jpg`, `2025/03/Ductless-Mini-Split-…jpg`)
  exists in the library but is only referenced as a page thumbnail, so no id is
  exported — swap it in post-import.
- **No `display_condition_list` gates** were found on the pages we model from, but
  the kit's popup/template layer uses `display_settings`/`location` — never copy
  those into a page.
- `ha_cmc_text: "Happy Addons"` appears on every element in the export. It is inert;
  new pages do not need it.
