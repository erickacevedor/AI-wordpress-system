---
name: midlakes-ui-design
description: >
  UI/visual design system for building Mid Lakes Heating & Cooling (Loganville, GA
  HVAC) pages in Elementor. Use whenever creating, styling, or reviewing a Mid Lakes
  page, section, hero, card, or button so it matches the HTML prototype the port is
  copying. Covers the logo-sampled palette, the on-dark colour pairs, Manrope +
  Fraunces, the 27-step type census and the clamp() heads, the red pill button, the
  1200px boxed section structure, every signature component, the watermarks, and the
  nth-child alternations that must be restated by hand. Triggers: "style this Mid
  Lakes section", "match the prototype", "Mid Lakes brand colors/fonts/buttons".
---

# Mid Lakes — UI Design System

Apply this when building or styling any Mid Lakes Elementor page. Loganville, GA HVAC
contractor on the **`mid-lakes` child theme** (of Hello Elementor 3.5.1) with
**Elementor 4.2.3 + Pro 4.2.2**.

**Everything below is already implemented in `projects/midlakes/brand.py`.** Build
through it; this skill is the specification it satisfies, and the place to look when
something needs to change.

**Colour globals are NOT real here.** The kit's `system_colors` is deliberately still
Hello Elementor's defaults, so pointing a widget at a global colour slot silently
produces off-brand output. **Style colour inline, always** — `tokens.json` carries
`"global": null` on every colour on purpose.

**Font globals ARE real.** The kit's base typography is set to Manrope, so anything
that inherits (Pro form fields, accordion body copy, list items) is already correct.
The rule for this site: **fonts come from the kit, colours are written into the
page.**

The canonical model for any section is the prototype file itself:
`D:\laragon\www\midlakes\public\<page>\index.php` + the matching rules in
`styles.css`. When in doubt, open it and copy the values. Full reasoning:
`projects/midlakes/KIT-ANALYSIS.md`.

## Colour palette — sampled from the logo artwork

| Role | Token | Hex | Use for |
|---|---|---|---|
| **Brand primary** | `--blue` | `#2540af` | `.why-num`/`.step-num` numerals, even service-icon tiles, `--blue` spec bullets, `.rate-amount` |
| **CTA / action** | `--red` | `#c10a0a` | **all button fills**, eyebrow dot, active-nav underline, list markers, focus ring on light |
| Button hover | `--red-dark` | `#a30808` | the hover fill, nothing else |
| **Dark surface** | `--ink` | `#0f1f35` | the contact band and the footer |
| Raised on dark | `--ink-2` | `#17293f` | the quote-form card |
| Body text | `--text` | `#1a2436` | light bands |
| Muted text | `--muted` | `#5a6472` | `.lead`, card paragraphs, `.spec-label`, `.legal` |
| Hairline | `--gray-line` | `#dde3ec` | dividers, 1px card borders |
| Band | `--paper` | `#f4f6f9` | the alternating light band + page background |
| Band | `--white` | `#ffffff` | the other light band, card fills on paper |

**Tints** (icon tiles): `rgba(193,10,10,0.09)` red · `rgba(37,64,175,0.10)` blue.

### The on-dark pairs — the single easiest way to break this port

| On light | On the ink band |
|---|---|
| red text `#c10a0a` | **`#ff8b8b`** (`--red-on-dark`) — `#c10a0a` on navy is 2.62:1 |
| blue text `#2540af` | **`#6fb3ec`** (`--blue-on-dark`) |
| focus ring `#c10a0a` | **`#4a9be5`** (`--focus-dark`) |
| muted meta `#5a6472` | **`#8fb2d8`** (`--gray`) |

Never put `#c10a0a` text on `#0f1f35`. The contact band's phone link is `#ff8b8b`;
its `dt` eyebrows are `#6fb3ec`.

## Bands and section rhythm

| Class | Band |
|---|---|
| `.about`, `.why` | **white** `#ffffff` |
| `.services`, `.faq`, `.hero-compact`, `.legal` | **paper** `#f4f6f9` |
| `.contact`, `.site-footer` | **ink** `#0f1f35` |
| `.hero` / `.hero-page`, `.comfort` | **photo** + a navy overlay gradient |

Order, page by page (`KIT-ANALYSIS.md` §4):

```
home                hero · white · paper · comfort · white · paper · ink
about-us            hero · white · paper · white · WHITE · comfort · paper · white · ink
services            hero · section-nav · white · paper · white · comfort · paper · white · ink
service-agreements  hero · white · paper · white · WHITE · paper · ink
service-area        hero · white · paper · white · paper · ink
financing           hero · white · paper · white · paper · white · paper · white · ink · paper(legal)
blog                hero-compact(paper) · PAPER · comfort
```

> **The capitalised doubles are deliberate.** The "never two identical bands adjacent"
> rule that applies on other sites **does not apply here**. Reproduce them.

### The two photo overlays Elementor cannot draw

Both are **three-stop** gradients; Elementor's control has two.

```css
.hero-overlay    linear-gradient(180deg, rgba(15,31,53,.55) 0%,
                                          rgba(15,31,53,.35) 40%,
                                          rgba(15,31,53,.85) 100%)
.comfort-overlay linear-gradient(100deg, rgba(15,31,53,.94) 0%,
                                          rgba(15,31,53,.80) 45%,
                                          rgba(15,31,53,.35) 100%)
```

**Shipped as two named child-theme rules** (`.ml-hero::after`, `.ml-comfort::after`)
carrying the exact gradients, with the container emitting the background *image* only
and the boxed container taking `z_index: 1` so the copy sits above them. Marked
`[cap CANDIDATE]` in `mid-lakes.css` and reversible without touching any `build.py`.
The fallback, if rejected: a native `background_overlay` gradient, 180°,
`rgba(15,31,53,.45)` → `rgba(15,31,53,.85)`. It is visibly flatter; say so in the
handoff note.

## Typography — Manrope, with Fraunces for three numerals

No `font-family` on `h1/h2/h3` — headings inherit `body`. **All headings: weight 800,
`line-height: 1.1`, `letter-spacing: -0.02em`.** Body `line-height: 1.6`.

**Fraunces is italic-only and appears in exactly three places** — `em`/`.serif`,
`.why-num`, `.step-num`. It carries the whole serif voice and is the first thing a
port loses silently. It loads on the `ital,opsz` **variable axis**, which Elementor's
font picker cannot express, so the child theme enqueues it and applies it by class
(`.ml-serif`, `.ml-why-num`, `.ml-step-num`).

### The scale is NOT collapsed

27 distinct sizes, kept exactly (PORT-DECISIONS decision 8 — `build.py` emits them
programmatically, so exactness costs nothing). The full census keyed by component is
`tokens.json → type_scale`. **Read the size out of the token, do not eyeball it.**

| rem | Owner |
|---|---|
| `clamp(2.4, 5.2vw, 4)` | `h1` |
| `clamp(1.8, 3.4vw, 2.75)` | `h2` |
| 2.2 | `.stat-num` (800, `-0.03em`, ink) |
| 1.7 / 1.6 | `.step-num` / `.why-num` — **Fraunces italic 500** |
| 1.55 · 1.5 · 1.35 · 1.3 · 1.2 · 1.15 · 1.08 | h3-class headings |
| 1.12 · 1.1 | `.hero-sub` · `.lead` |
| 1.05 · 1.02 · 0.98 · 0.96 · 0.95 · 0.94 · 0.92 · 0.9 · 0.88 · 0.85 · 0.82 · 0.78 · 0.72 | body, UI, labels |

### The h1/h2 recipe (memorise this one)

The child theme owns their **font-size** via `clamp()`. The responsive gate makes a
missing `typography_font_size_mobile` on any `h1`/`h2` an **error**, unconditionally.
Both are satisfied by emitting the **mobile size only**, set to the clamp's floor:

```python
brand.h1("Heating, Cooling &amp; Home Comfort in Loganville, GA")
# -> heading(tag="h1", size=None, mobile=2.4, unit="rem", weight="800",
#            lh=1.1, ls=-0.02,
#            extra={"typography_typography": "custom"})   # <- REQUIRED
```

`h2` uses `mobile=1.8`. No desktop size, no tablet size — above 767px the clamp is
unopposed and scales fluidly. h2's floor is exact below 767px; h1's is within 1.5px.

⚠️ Without `typography_typography: "custom"`, Elementor writes **no CSS at all** for
that typography group. `responsive-audit.py` still passes, because it only checks the
key exists. Silent failure.

Every other heading gets a real desktop `size` in `unit="rem"`, and `heading()`
auto-derives its mobile step.

## Button — a red pill that lifts 2px

```
font        Manrope 0.95rem / 700 / no transform
radius      999px          border  1.5px solid
padding     14 / 26        gap     8        white-space nowrap
primary     bg #c10a0a  text #fff  border #c10a0a
            HOVER bg #a30808  border #a30808  text #fff
ghost       bg transparent  text #fff  border rgba(255,255,255,.5)
            HOVER bg rgba(255,255,255,.1)      <- photo bands only
block       width 100%                          <- the form submit
HOVER LIFT  transform: translateY(-2px)          <- CSS-OWNED, class .ml-btn
```

- **Do NOT add `hover_animation`.** No `grow`, no `float`, no `shrink`. The brand
  convention is the 2px lift on a 0.15s ease and the child theme already ships it.
- **The key is `background_color`, not `button_background_color`.** Wrong key → silent
  fall-through to `var(--e-global-color-accent)` → Hello's default.
- **`globals` stays `{}`.** The kit is stock.
- The class lands on the widget **wrapper**, so the stylesheet rule must be
  `.ml-btn .elementor-button:hover`, never `.ml-btn:hover` (that moves the wrapper).

## Section structure (REQUIRED — every section)

```
Section                 (full-width 100% — background only, NO padding)
└── Content Container    (BOXED to 1200px — carries the padding)
    └── content          (headings, text, buttons, rows, grids, cards)
```

1. **Outer Section** — `content_width: full`, carries the band background and any
   watermark overlay.
2. **Content Container** — one boxed container, `boxed_width` **1200px**,
   `flex_gap` 22. Padding `96/24/96/24`, `padding_mobile` `64/24/64/24`.
   (`.comfort` → `120/24/120/24` and `80/24/80/24`.)
3. **Hero** — `min_height` 640 (interior `.hero-page` 460, tablet 560), padding
   `120/24/64/24` (interior `104/24/56/24`), content bottom-aligned
   (`flex_align_items: flex-end`). `.hero-compact` is a paper band, `116/24/56/24`
   → `96/24/44/24`, with a bottom hairline.
4. **No excess containers** — a lone heading sits directly in the boxed container.
   Nest only for a genuine row, a self-contained card, or a grid.
5. **Section title block** — `max-width: 720px`, `margin-bottom: 48px`.

## Signature components — reuse, don't invent

**Eyebrow** — 0.72rem / 700 / `0.18em` / uppercase, `#c10a0a`, preceded by a 7px red
dot. Emit as one text widget whose HTML carries the dot inline:
`<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#c10a0a;margin-right:8px;"></span>ABOUT US`.
On the photo bands use `.eyebrow-light` — white label, red dot.

**Hero creds** — a flex-wrap list under a 1px `rgba(255,255,255,.18)` top rule,
`margin-top` 34 / `padding-top` 26, gap `12px 36px`. Each item is
`<strong>75+</strong> Years of Combined Team Experience` — strong is white 800, the
rest `rgba(255,255,255,.8)` at 0.95rem (0.88rem below 620px).

**Stats column** — 2.2rem/800 ink numeral + 0.9rem muted label per item, each with a
1px `#dde3ec` bottom rule. **The last item drops its rule.**

**Promise list** — each item is a container with a **3px `#c10a0a` left border** and
20px left padding, holding a 1.2rem/800 h3 + a muted paragraph.

**Service card** — white, radius 14, 1px `#dde3ec`, padding 32/28,
**`min_height: 350`**, holding a 52px icon tile (radius 12, `icon_size` 26,
`margin-bottom` 22) + 1.2rem/800 h3 + 0.96rem muted p. Hover: `translateY(-4px)` +
`0 18px 40px -24px rgba(15,31,53,.35)` + `border-color: transparent`.
**Tiles alternate red/blue — see "Alternations" below.**

**Why card** — **paper** fill on the white band (inverted from the service card),
radius 14, padding 36/32, 1px border, `min_height: 350`, holding a Fraunces italic
numeral (1.6rem/500) + 1.3rem/800 h3 + muted p. `/about-us/` uses a **3-up** variant
because it lists three values; every other use is 2-up.

**Spec card** — white, radius 14, 1px border, padding 26/26/28, holding an uppercase
0.78rem/700/`0.14em` muted `.spec-label` + a check list. The `--blue` modifier only
changes the marker colour.

**Check list** — `icon-list` with `fas fa-check-circle` at 18px. Marker `#c10a0a` by
default, `#2540af` on a blue spec card. Text 0.96rem, `padding-left` ~30, gap 12.
This is the native stand-in for `.spec-list li::before` and `.perk-list li::before`
(a red disc with a knockout white check).

**Comfort card** — copy capped at 560px on the photo band: light eyebrow, h2,
`rgba(255,255,255,.82)` sub, the perk check list, one red CTA.

**Detail row** — `1.15fr / 1fr`, gap 48, `52px` vertical padding (36 on mobile), 1px
`#dde3ec` **top** border. The `--flip` variant reverses order — and on `/services/`
**the flipped rows are the ones carrying the blue spec card.** The **first** row drops
its top border and pads 8px top.

**Chips** — pill (999px), white, 1px `#dde3ec`, 0.92rem/600, padding 9/17, in a
wrapping flex row with gap 10.

**Steps** — 4-up grid (2-up ≤960px, 1-up ≤620px), gap 26, each with a **2px `#dde3ec`
top rule**, `padding-top` 26, a Fraunces italic numeral (1.7rem/500, tabular-nums),
1.08rem/800 h3, and 0.94rem muted paragraphs.

**Area list** — bordered rows, 13px vertical padding, 1.02rem/600, **last row drops
its border**.

**FAQ** — the **Accordion** widget (it already does "only one open"). Summary
1.05rem/700, body muted, 1px `#dde3ec` between items, 22px vertical padding. On the
home page the **first item is open**. Sits at ~1.3fr beside a 4:5 `.faq-media` photo
whose caption is a bottom-anchored `linear-gradient(180deg, transparent,
rgba(15,31,53,.9))` block with a 1.05rem white `<strong>` line + 0.9rem detail.

**Contact band** — ink, `1fr / 1.05fr`, gap 56. Left: h2 + `rgba(255,255,255,.75)`
sub capped at 460px + a definition list (uppercase 0.72rem/`0.16em` `#6fb3ec` label,
1.1rem/600 white value, `#ff8b8b` links, 0.85rem `#8fb2d8` sub-line). Right: the
form card.

**Quote form** — `#17293f`, radius 14, 1px `rgba(255,255,255,.08)`, padding 36 (26/22
mobile): 1.5rem/800 h3, 0.92rem `rgba(255,255,255,.65)` intro, two 2-up field rows
(1-up below 620px), a full-width textarea, a full-width red submit. Fields:
`rgba(255,255,255,.04)` fill, `rgba(255,255,255,.4)` border, radius 10, padding 13/15,
white text, **focus border `#4a9be5`**. **Every field keeps a real `<label>`.**
Build it **once** as a saved Elementor Pro Form template — it appears on all six pages.

**Rate table** — one `html` widget carrying the prototype's `<table>` markup verbatim,
plus the child theme's `.ml-rate-table` rule (including the `<620px` stacking that
hides `thead` and turns each row into a card). There is no table widget.

**Map** — Google Maps widget in a radius-14 container with a 1px `#dde3ec` border,
`min_height` 420 (320 mobile), at 1.3fr beside the area list.

**Legal** — paper band, 1px top border, padding `30/24/34/24`, 0.85rem muted text
capped at 90ch.

## Watermarks

Four wave SVGs (`1/2/4/6.svg`, all `viewBox="0 0 2000 500"`). **Ship them as
child-theme assets** — WordPress blocks SVG uploads by default, and this keeps them
in git.

⚠️ **These are CSS pseudo-elements, not Elementor backgrounds.** The
background-image route was tried and cannot work: every watermark is a
`width: 100%; height: <fixed>px` box offset OUTSIDE its parent with
`background-size: cover`, and Elementor's background controls paint the element's
**own box** — the layer's height is decoupled from both the element and the image's
4:1 ratio. The cap's conditional row covers exactly this. `build.py` emits only the
CLASS; the child theme does the rest.

| Class | File | Position | Opacity |
|---|---|---|---|
| `ml-wm-waves` (`::before`) | `2.svg` | `right:-200 bottom:-250`, 100%×400 | 1.0 |
| `ml-wm-waves` (`::after`) | `2-flip.svg` | `left:-200 top:-250`, 100%×400 | 1.0 |
| `ml-wm-card-1` | `1.svg` | `bottom:-50 left:0`, 100%×200 | 0.3 |
| `ml-wm-card-4` | `4.svg` | `bottom:-100 left:0`, 100%×200 | 0.3 |
| `ml-wm-contact` | `6.svg` | `top:0 left:0`, 100%×200 | 0.3 |
| `ml-footer` | `1.svg` | `bottom:0 left:0`, 100%×200 | 0.1 |

`2-flip.svg` is `2.svg` pre-rotated 180°, because Elementor cannot transform a
background and the cap should not grow a `transform` rule for dressing.

**Three traps:**

- ⚠️ **Only `.about` gets the wave pair.** `.why` is also white and has NONE — its
  decoration is on its cards. `brand.sec_about()` adds them; `brand.sec_why()` does
  not. Reaching for a generic "white band" helper is how this goes wrong.
- `.what-happens.about` suppresses them. Suppression is **by omission** —
  `sec_about(watermark=False)`, which renders identically to the prototype's
  `display: none`. `/about-us/` and `/service-agreements/` each carry one.
- `.site-footer { padding-bottom: 300px }` exists **only** to clear the footer
  watermark. Drop one and the other goes with it.

## Alternations — restated by hand, every time

Elementor has no positional selector. **This list is the source of truth; the pattern
breaks the first time someone adds a card without it.**

| Prototype rule | Restate as |
|---|---|
| `.service-card:nth-child(even) .service-icon` | tiles run **red, blue, red, blue, red, blue** across the 6-up grid |
| `.why-card:nth-child(odd) .why-num` | numerals run **red, blue, red, blue** (base is blue; odd overrides to red) |
| `.step:nth-child(odd) .step-num` | numerals run **red, blue, red, blue** |
| `.spec-card--blue` | on `/services/` the **flipped** detail rows carry the blue card: red, blue, red / red, blue, red |
| `:last-child` border removal | `.stats li`, `.area-list li`, `.rate-table tbody tr` |
| `.detail-row:first-of-type` | no top border, `padding-top: 8px` |

## Icons — a sprite, mixed with native and emoji

The six service icons are custom 24×24 stroke SVGs (`stroke-width: 1.8`,
`currentColor`). Ship them as an **inline sprite** in the child theme
(`assets/icons.svg`) and reference them from small `html` widgets — the §6B pattern.

Mix with native and emoji icons so no page depends entirely on one source:
`fas fa-check-circle` for check lists (FA Free Solid ships with Elementor), and emoji
where a decorative mark reads better — ❄️ cooling · 🔥 heating · 🚨 emergency ·
🏠 home · 🧰 tools · 🛡️ guarantee · ⏰ 24/7 · 💰 financing. Save JSON as UTF-8.

## Layout & responsive

Container/flex model, never legacy Section→Column.

The prototype's own breakpoints are **1400 / 1200 / 960 / 620**. Two of those now exist
in Elementor as real breakpoints, because the header needs them:
**laptop 1400** (tighten the nav) and **tablet_extra 1200** (collapse it). The page
grid still maps onto Elementor's native tablet/mobile:

| Prototype | Elementor |
|---|---|
| `≤960px` two-column → one | `flex_direction_mobile: column` + `width_tablet: 100%` |
| `≤960px` 3-up grid → 2-up | `grid_columns_grid_tablet: 2` |
| `≤620px` grid → 1-up | `grid_columns_grid_mobile: 1` |
| `≤620px` `.section` 96 → 64 | `padding_mobile` |

Gate requirements, always: grids set tablet **and** mobile column counts; flex rows
set `flex_direction_mobile: column`; %-width columns set `width_mobile: 100%` (and
`width_tablet`); fixed-height images set `height_mobile`; boxed containers set
`padding_mobile`; **H1 and every H2 carry a mobile size**.

Specific mobile values from the prototype: `.gallery-tall` goes 3/5 → **16/10**;
`.hero-actions` becomes full-width with `flex: 1` buttons; `.field-row` goes 1-up;
`.quote-form` padding 26/22; `.footer-inner` 3-col → 2-col (≤960) → 1-col (≤620);
`.hero-creds` font 0.88rem.

## The header — three things that are not obvious

1. **Every widget in the bar carries `_element_width: "auto"`.** A widget in an
   Elementor flex row defaults to `width: 100%`, so the nav, the phone and the CTA
   otherwise split the bar into thirds — the nav wraps onto three lines and the phone
   is clipped under the button.
2. **The CTA's "hide below 1200" classes go on the BUTTON, not a wrapper.** A wrapper
   container would default to full width and squeeze the row for the same reason.
3. **`.ml-nav` forces `flex-wrap: nowrap`.** Elementor's horizontal nav-menu ships
   `flex-wrap: wrap` with no control to change it; the prototype's `.main-nav` is a
   plain `display: flex`, i.e. nowrap. Without this the menu silently restacks under
   width pressure instead of staying one row.

## Accessibility — the design already decided these

Heading levels never skip (H1 → H2 → H3; change the *size*, not the level). Every CTA
carries a visible descriptive label — never icon-only. Nothing auto-plays. Every form
field keeps a real `<label>`, not a placeholder standing in for one. Inline prose
links stay underlined and coloured (`#c10a0a`, or `#ff8b8b` on the comfort band),
because the base rule is `color: inherit`. Every image keeps its alt text — copy it
from the prototype verbatim.

## What the child theme owns — and therefore what build.py must NOT emit

`theme/mid-lakes/assets/mid-lakes.css` is a **cap**, not a stylesheet. One owner per
property, no `!important`:

| Owned by the child theme | Class |
|---|---|
| `h1`/`h2` desktop font-size (the `clamp()` ramps) | `.ml-h1` / `.ml-h2` |
| Fraunces family + style + weight | `.ml-serif` / `.ml-why-num` / `.ml-step-num` |
| The button's hover `transform` + transition | `.ml-btn` |
| The card's hover `transform` **only** | `.ml-card` |
| The two 3-stop photo overlays | `.ml-hero` / `.ml-comfort` |
| The six watermark pseudo-elements | `.ml-wm-*`, `.ml-footer` |
| The rate table, including its `<620px` stacking | `.ml-rate-table` |
| The `:focus-visible` rings | (pseudo-class) |
| The header's `backdrop-filter: blur(10px)` | `.ml-header` |

Everything else is Elementor's. Note the deliberate per-property splits: the card's
hover **shadow and border-colour** are native container controls and stay in
`build.py`; only the transform is CSS. Same for the header — Elementor owns the
translucent fill, the hairline and the sticky behaviour; the child theme owns only
the blur, because Elementor's CSS Filters group emits `filter:`, which would blur the
header's own contents.

## Page settings

`{"template": "elementor_header_footer", "hide_title": "yes"}`. Header and footer are
Theme Builder templates in `pages/_theme/`, which validate as `type: "header"` /
`"footer"` and must **not** contain an H1.

## Output completeness

Emit the **complete** JSON — never `// ...` or "the rest follows the same pattern."
Unique `id` per element; required keys (`elType`/`widgetType`/`elements`/`settings`)
intact; UTF-8. Wrap single pages as
`{"version":"0.4","title":"…","type":"page","content":[…],"page_settings":{…}}`.
**No `display_condition_list`.**

## Review checklist

Every section = full-width Section → one boxed 1200px container → content; padding on
the container and on self-contained cards only; the band order matches the page's row
in the table above **including its deliberate double**; blue `#2540af` primary / red
`#c10a0a` CTA / navy `#0f1f35` surface with the on-dark pairs used on the ink band;
Manrope everywhere and Fraunces on exactly the numerals; **no global colour refs**;
the red pill with `background_color` and **no** `hover_animation`; the alternations
restated; watermarks placed and `.what-happens` suppressed; `validate-page.py` exits
0; every image has alt text.
