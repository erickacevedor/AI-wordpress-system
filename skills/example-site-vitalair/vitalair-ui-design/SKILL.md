---
name: vitalair-ui-design
description: >
  UI/visual design system for building VitalAir HVAC pages in Elementor (Hello
  Elementor theme). Use whenever creating, styling, or reviewing a new VitalAir
  page, section, hero, card, or button so it matches the existing kit. Covers the
  brand color palette, typography scale, button styles, section rhythm, layout/
  container rules, and reusable templates. Triggers: "new VitalAir page", "style
  this section", "match the kit", "Elementor design", "brand colors/fonts".
---

# VitalAir — UI Design System

Apply this system when building or styling any VitalAir (vitalair.com) Elementor page so it stays visually consistent with the existing kit. VitalAir is an Atlanta-area HVAC company on **Hello Elementor 3.4.4 / Elementor Pro**.

**Critical rule:** the kit does **not** drive styling through Elementor global variables. `site-settings.json` still holds the generic Hello Elementor defaults (`#6EC1E4`, "Noto Sans Coptic"). Real brand styling is applied **inline on each widget**. So always set colors and fonts explicitly on the widget — never rely on global color/typography slots.

## Color palette

Set these as explicit hex values on widgets/sections.

| Role | Hex | Use for |
|------|-----|---------|
| Brand navy (dark) | `#16163F` | Header, hero backgrounds, dark feature bands |
| Deep navy variants | `#1C244B`, `#0D1B3E`, `#020101` | Overlays, alt dark sections |
| Brand blue | `#3E67AB` | Footer, gradient accents |
| Blue variants | `#1B4E8D`, `#324A6D` | Secondary accents |
| Primary green (CTA) | `#74BC2B` | Buttons, highlights |
| Green variants | `#8FD13E`, `#8BE035`, `#6ABF4B`, `#5A9421` | Eyebrow labels, button hover, accents |
| Light blue tint | `#EEF2FA`, `#C8D6E8` | Alternating content-section backgrounds |
| Dark text | `#212121` / `#222222` | Body + heading text on light bg |
| White | `#FFFFFF` | Text on dark, light section bg |
| Muted gray | `#555573` | Secondary/supporting text |
| Alert red | `#D72C2C` | Warnings, urgent emphasis |

**Section rhythm — always alternate backgrounds** down the page:
`navy #16163F hero` → `white #FFFFFF` → `light #EEF2FA` → `white` → (optional navy feature band) → footer. Never place two identical-background sections back to back.

## Typography

Use **Poppins** as the primary family (Montserrat / Manrope / Sora acceptable for accents). Do **not** use "Noto Sans Coptic".

| Level | Size | Weight | Notes |
|-------|------|--------|-------|
| Eyebrow / label | 11–12px | 700 | UPPERCASE, letter-spacing ~2.6px, color green `#8FD13E` |
| Body / small | 15–18px | 400 | color `#212121` on light, `#FFFFFF` on dark |
| Sub-heading (h3) | 22–26px | 600–700 | |
| Section heading (h2) | 40–44px | 600–700 | |
| Hero heading (h1) | 52–70px | 700 | up to 95px on large displays |

Standard heading pattern for a section: **green uppercase eyebrow → large h1/h2 → 15–18px supporting paragraph**.

## Buttons (primary CTA)

```
text color:        #FFFFFF
background:         #74BC2B      (brand green)
hover text:        #FFFFFF
hover background:   #5A9421      (darker green)
border-radius:     999px         (full pill)
padding:           16px / 30px   (top-bottom / left-right)
font:              15px, weight 700
hover animation:   NONE          (see rule below)
```

**Hover behavior — color only.** Buttons must NOT use any size or shape animation on hover (no grow, shrink, or scale). Only the background color and text color change. In Elementor, leave `hover_animation` empty/`none`; set only `button_background_hover_color` and `hover_color`.

Every major section should end with or contain a CTA. Keep buttons pill-shaped and green — this is the single strongest brand signal.

## Section structure (REQUIRED — every section)

Every section on the page must follow this exact two-tier nesting:

```
Section          (large outer container — full width)
└── Content Container   (inner — holds ALL padding)
    └── content         (headings, text, buttons, nested containers/grids)
```

Rules:

1. **Outer Section** — full-width container that carries the background (color/image/overlay) and the section rhythm. It has **no padding**. Its only job is width + background.
2. **Content Container** — a single container nested directly inside the Section. This is the **only** element that carries padding, and it **always** has the default padding. Constrain readable text here to the boxed ~1200–1240px width.
3. **Everything inside the Content Container** — headings, text, buttons, and any nested containers/columns/grids — has **zero padding**. Spacing between them comes from the Content Container's `flex_gap` and element margins, never from padding on children.
4. **Nested containers** (e.g. a 3-column feature row, map+list row, service grid) live inside the Content Container and also have **no padding** — only the Content Container is padded.

Default Content Container padding (apply consistently): desktop `80px` top/bottom, `24px` left/right; mobile `48px` top/bottom, `18px` left/right. Adjust the value if a design calls for it, but keep padding on the Content Container only.

## Layout rules

- **Prefer Containers (flex model)** for new pages — this is the newer, dominant pattern in the kit. Avoid the legacy Section→Column model unless matching a specific old page.
- **Content max-width:** ~1200–1240px (boxed) for text; 1600–1790px for full-bleed hero/footer bands.
- **Full-width layout** at the Section level; boxed Content Container for readable text.
- Use icon-box grids for feature/benefit lists; toggle/accordion for FAQs.
- Responsive spacing lives on the Content Container's padding + gap (heavier on mobile), never on child elements.

## Reusable templates (fastest starting points)

| ID | Name | Role |
|----|------|------|
| 10 | Elementor Header #10 | sticky navy header — **reuse as-is** |
| 181 | Elementor Footer #181 | blue footer w/ curve divider — **reuse as-is** |
| 1879 | Template-Service | service page base |
| 438 / 1422 | ServicePages / Services | service layout container |
| 624 / 772 / 769 | VAFAQ / Service-faq | FAQ block |
| 766 | Service-IMG | image section |
| 1979 | bannetemp | banner |

**Recommended build order for a new page:** header `10` → navy hero (eyebrow + h1 + intro + green CTA) → alternating white/`#EEF2FA` content bands (icon-box grids, images) → FAQ accordion (from `624`/`772`) → closing CTA band → footer `181`.

## Audit-first workflow (before building or restyling)

When starting from an existing page or template, audit before you change anything:

1. **Read the source** — open the page/template JSON, note its section order, backgrounds, widget types, and whether it uses Containers or legacy Sections.
2. **Diagnose against this system** — flag anything off-brand: wrong font (Noto Sans Coptic), non-pill or non-green CTAs, two same-colored sections in a row, colors pulled from global slots instead of inline, sub-1200px or unbounded text width.
3. **Fix in place** — apply targeted corrections working with the existing structure. Reuse header `10` / footer `181` and existing container templates rather than rebuilding from scratch.

Note: unlike generic web-redesign advice, VitalAir **intentionally** uses colored hero bands and alternating navy/light sections — that is on-brand here, not a mistake to "fix." Single accent color is also *not* the rule: navy + blue + green is the brand.

## Output completeness (Elementor JSON)

Elementor exports are long and deeply nested. When producing or editing page/template JSON:

- Emit the **complete** JSON — never abbreviate with `// ...`, `"... rest of widgets ..."`, or "the other sections follow the same pattern." A truncated Elementor JSON will not import.
- Every widget needs its full `settings` block with inline colors/typography, and every element needs a unique `id`.
- Preserve required structural keys (`elType`, `widgetType`, `elements`, `settings`) at every level.
- If a file is too large for one pass, stop at a clean section boundary and continue — do not compress or skip middle sections.

## Images & media placement

- **Hero / feature images:** use the two-column variant — content in one column, an
  image (or column background image) in the other. For full-bleed heroes, use a
  section background image with a dark navy overlay (~40-50%) so text stays legible.
- **Section feature images:** service/benefit grids can use an image above each
  heading, or icon-box icons where a photo isn't available.
- **Alt text is required** on every meaningful image (accessibility + SEO). Never
  ship `alt=""` or `alt="image"`.
- **Sizing/ratio:** heroes ~16:9 (or a 4:5 portrait for a side column); feature
  images consistent ratio across a row.
- **Live/dynamic media** (review sliders, advanced maps, forms) can't be embedded
  in template JSON — insert a labeled shortcode/placeholder and wire the real
  widget in after import.

## Review checklist

Before shipping a page, verify: **every section = Section → Content Container → content**; padding ONLY on the Content Container (children have zero padding); alternating section backgrounds; green pill CTAs with **no hover size/shape animation** (color-change only); Poppins (not Noto Sans Coptic); green uppercase eyebrows above headings; navy hero; colors set inline (not via global slots); Container-based; boxed text width ~1200px; JSON complete and valid (no truncation, unique ids, required keys intact); every image has alt text.
