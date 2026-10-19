---
name: lenz-ui-design
description: >
  The Lenz Heating & Cooling visual system and component catalogue for Elementor:
  tokens, contrast rules, buttons, section rhythm, every reusable block in
  brand.py and service_page.py, and how to add a new component without breaking
  visual consistency. Use whenever building, styling or reviewing any Lenz page,
  section, widget or component. Triggers: "Lenz styling", "Lenz component", "Lenz
  section", "add a block to Lenz", "make it match Lenz", "Lenz button", "Lenz
  colours".
---

# Lenz: UI Design

Read `lenz-design-read` first. The one rule behind everything here:

> **Style lives in `lenz-core.css`, not in Elementor.** A page is built from
> containers and native widgets that carry the prototype's class names. Changing a
> colour or size in the Elementor panel does nothing where the CSS sets it, and
> where it does work it creates a one-off that the next page will not match.

The only style values a build writes into Elementor settings are the ones the
gate or Elementor itself forces (section 7). Everything else is a class.

## 1. Tokens (`design-source/v6-1/tokens.css`, mirrored in `tokens.json`)

Always reference these through the existing classes. If you must name one (in a
new CSS rule, section 8), use the variable, never the hex.

| Role | Variable | Value | Use |
|---|---|---|---|
| Dark ground | `--blue-900` / `--color-dark-bg` | `#07113B` | hero, CTA band, promo box, reviews, close form, footer |
| CTA blue | `--color-cta-bg` (`--blue-600`) | `#1837BE` | `btn-primary` |
| Gold | `--gold-500` | `#FFC600` | `btn-gold`, accents on dark |
| Accent rust | `--color-accent` | `#D6410F` | eyebrows and icons on light surfaces |
| Display orange | `--color-accent-display` | `#F05A28` | large display type and gradients **only** |
| Mist band | `.section--mist` | `#F8F8FB` | light band |
| Cream band | `.section--cream` | `#FFFCF0` | warm light band (also the symptoms, bullets and steps blocks) |
| Text | `--color-text-primary` / `--color-text-secondary` | neutral-900 / neutral-600 | body copy |

Gradients: `--gradient-cool` (blue to navy), `--gradient-temperature` (orange to
purple), `--gradient-warm` (gold to orange, financing only), `--gradient-heading`
(the `.accent` span in the hero H1). Do not create new ones.

Type: **Montserrat** 700/800 for headings, **Open Sans** 400/600/700 for body,
loaded by `lenz-core` (Elementor's own font loading is off). Scale (16px base):
`--text-2xs` 10, `xs` 13, `sm` 16, `md` 20, `lg` 25, `xl` 31, `2xl` 39, `3xl` 49,
`4xl` 61, `--text-hero` `clamp(39px, 4.6vw + 12px, 61px)`.

Spacing `--space-1..48` (4px steps up to 32, then 40, 48, 64, 80, 96...), radii
`--radius-xs 4 / sm 8 / md 12 / lg 18 / xl 28 / pill 999`, shadows `--shadow-1..4`.

Icons: the inline sprite in `lenz-core` (24 Lucide symbols): `i-phone i-star
i-check i-shield i-clock i-snow i-flame i-wrench i-wind i-droplet i-air i-heat
i-calendar i-card i-pin i-info i-mail i-tv i-award i-plus i-chevron i-arrow i-menu
i-close`. Use `brand.svg("i-name", "icon-sm")`. No emoji, no icon font, no new SVG
files unless added to the sprite (section 8).

### Contrast rules (deliberate, do not break)

1. Gold never carries white text. Gold takes `#121212` (`btn-gold` already does).
2. `--color-accent-display` (orange-500) is never body text.
3. Eyebrows are rust by default; only dark panels switch them (the CSS handles it).
4. Focus rings are CSS-owned two-ring outlines. Never remove an outline.

## 2. Buttons (`brand.button(label, url, classes, icon=None)`)

Pill, 2px border, 48px min height, Montserrat 700 16px. Hover is a `-1px` lift plus
a colour change, CSS-owned. **Never** set Elementor `hover_animation`, colours or
padding on a button.

| Class | Where |
|---|---|
| `btn btn-gold` | the main CTA on dark surfaces (hero, promo, CTA band, form submit) |
| `btn btn-primary` | the main CTA on light surfaces |
| `btn btn-outline` | secondary on light |
| `btn btn-outline-light` | secondary on dark (e.g. "Call (515) 225-6446" in the hero) |

Icons on buttons are CSS masks: `icon="phone"` (or `arrow`, `check`) adds
`lz-ico lz-ico-<name>`. Inline SVG in a button label is stripped by WordPress.
`tel:` buttons get `icon="phone"` automatically in the blocks.

## 3. Section rhythm and bands

- Every band is `B.section("<classes>", [...])`: a full-width section plus one boxed
  container at 1140px. Never nest another full-width section inside.
- **Each block owns its background**; the page does not. Measured on the rendered
  site (2026-10-18):

  | Background | Blocks |
  |---|---|
  | Navy `#07113B` | hero, trustbar, cta-band (emergency and `cta`), reviews, close-form; footer is a navy-to-black gradient |
  | Cream `#FFFCF0` | `cards` / `boldcards` (symptoms, even with `section--mist`), `bullets`, `steps`, any block given `bg: "section--cream"` |
  | Mist `#F8F8FB` | `checklist` (default), `pair`, `faq`, related services, `services` (hub), `table` (default), `values`, any block given `bg: "section--mist"` |
  | Mist to white gradient | `why` (creds) |
  | White | `plans`, `promo` (the navy box sits on white), `prose`, `people`, `roster`, `locations`, `area` by default |

- `bg` is accepted only by `checklist`, `boldcards`, `table`, `prose`, `people`,
  `roster`, `steps`, `video` and `locations` (values `section--mist`,
  `section--cream`, or `""` for white). Use it to avoid two identical light bands
  in a row **where it is available**. Where it is not (e.g. `faq` then related
  services, both mist, on every service page), the repetition is part of the built
  site: accept it, do not add CSS to fix one page. The gate's "same background"
  warnings cannot see these classes and are expected.
- Category tint: every block on a page gets `svc-page svc-page--<cat>` from
  `PAGE["cat"]`, which sets `--cat`, `--cat-soft`, `--cat-on-dark` for icons, hero
  badge and related cards. Never colour a single block by hand.
- Waves (`w-wave wave-1`, the `:before` wave in `.service-help`) are decorative and
  CSS-owned. Keep the padding that leaves room for them.

## 4. Shared components (`brand.py`)

| Function | Renders | Notes |
|---|---|---|
| `head(icon, label, title, lead=None, extra="")` | `.section__head`: eyebrow + H2 + lead | `extra="section__head--center"` to centre |
| `eyebrow(icon, label)` | rust uppercase label with icon | one per section, above the H2 |
| `heading(text, tag, classes, size=)` | native heading | H1/H2 need `size` (section 7) |
| `text(markup, classes)` | native text editor | pass `<p>` when the CSS targets `p` |
| `button(...)` | native button | section 2 |
| `image(key, alt, classes)` | native image from `media.json` | real alt text always |
| `raw(markup)` | html widget | only for markup Elementor cannot express (SVG, FAQ disclosure, iframes, lists inside cards) |
| `trustbar(items)` | five proofs, gold values on blue | trust proofs appear **once**, here |
| `cta_band(title, sub)` | navy emergency band, van photo, gold call button | auto-inserted after the first cards-like block |
| `plans_section()` | RED / WHITE / BLUE agreements, BLUE recommended | prices and perks are ClickUp-approved; do not edit inline |
| `reviews_grid()` | one feature + two side reviews | hardcoded quotes until the GBP Place ID exists |
| `faq_list(items)` | accessible disclosure driven by `lenz-site.js` | |
| `close_form(title, lead, button_text, preselect)` | navy band with the Elementor Pro estimate form, `#contact` | every CTA anchors here (`L["form"]`) |
| `service_card(cat, icon, name, blurb, key)` | linked card; static if out of scope | |

## 5. Page blocks (`service_page.py`, used in `PAGE["plan"]`)

Each block takes one doc section, in doc order. Pick by the **shape of the
content**, not by taste:

| Block | Use when the doc section is... | Look |
|---|---|---|
| `checklist` | intro copy + "We can help you:" + bullets | copy left, white check-list card right, CTA in the card |
| `cards` | several items, each with its own heading (problems, signs) | 3-col symptom cards + a navy "Not sure what's wrong?" tile with the phone |
| `boldcards` | paragraphs that start with `<b>Label:</b>` | 3 or 4-col cards |
| `pair` | two lists to compare (furnace vs heat pump) | two check-list cards side by side |
| `bullets` | one long list | wide card, check list in two columns |
| `values` | numbered reasons ("Why timely X matters") | photo + numbered list |
| `table` | a comparison table | responsive table (`data-label` on mobile) |
| `prose` | heading + paragraphs | reading column, optional list and buttons |
| `promo` | one offer or package with one action | navy box with waves, gold button **below** the copy |
| `plans` | anything about the RED / WHITE / BLUE service agreements (maintenance pages) | the home's plans block; its buttons go to `/maintenance-plan/`, a `promo` would send them to the form |
| `why` | 3 or 4 reasons to choose Lenz | credential cards |
| `steps` | numbered process | numbered step cards |
| `services` | hub list of child services | service cards with "Explore ..." links |
| `people` / `roster` | team bios / name lists | person cards with initials |
| `video` | WHO 13 segments | YouTube nocookie embeds |
| `locations` / `area` | offices / service area | map cards / city chips + map |
| `coupons` | specials | coupon images |
| `embed` | a third-party form (LeadConnector) | iframe card |
| `cta` | a closing band with buttons and no form | navy band |
| `faq` | Q&A | the home's FAQ |
| `reviews` | testimonials section | the home's reviews |
| `multi` | one doc section that holds several shapes | splits at bold sub-headings; `{"parts": [(block, opts), ...]}` |
| `close` | the doc's closing section | related services (non-hubs) + the estimate form |

Every page also gets, automatically: hero (breadcrumb, category eyebrow, H1 with an
optional gradient `accent`, sub, CTA pair, photo, badge), the trustbar, the
emergency band after the first `cards`/`boldcards`/`services` block, and related
services on non-hub pages.

### Component rules settled by feedback

- **Promo box** (`.service-help.promo`): copy first, button always underneath,
  copy up to 860px wide. Side by side it floated in the top corner on some pages
  and wrapped on others (Manuel, 2026-10-14; applied 2026-10-18, `d89c2e8`).
- **Help tile** (`.symptom-help`): text and phone stay together, centred as one
  block when a tall grid row stretches the tile.
- **Hero** keeps exactly what its reference has: on the home, the star line
  "Real reviews from Des Moines homeowners" (links to Google reviews); on service
  and company pages, the photo badge. No extra trust chips; the subhead stays at
  the CSS size.

### Hero media: which photo and badge

| Page kind | `hero_image` key | Badge pattern (`(bold line, small line)`) |
|---|---|---|
| Repair | `lenz-technician-service-call-webp` | `("24/7 emergency <x> repair", "Local team, real people, day or night.")` |
| Installation / replacement | `lenz-team-webp` | `("Free installation estimates", ...)` (estimates on new equipment are free) |
| Maintenance | `lenz-technician-service-call-webp` or `lenz-thermostat-ecobee` | `("Maintenance plans from $120 a year", "Priority dispatch and discounts on parts.")` |
| Indoor air quality | `lenz-comfort-webp` | `("Whole-home <service>", ...)` |
| Company / location | `lenz-team-webp` or `lenz-service-van-wrap-webp` | one fact from the page ("Two local offices", "Family-owned since 2009") |

Photos are temporary until the client shoot; keep the alt text specific to what
the photo shows.

## 6. Responsive

Verified widths: **1440, 1024, 768, 390**. The CSS owns breakpoints (mainly 600 and 904; some components also use 720,
1024 and 1100).
Grids stack (3 to 2 to 1), flex rows stack on mobile, nothing scrolls sideways. A
new or changed component is not done until it has been checked at all four widths
in a real browser, with no horizontal overflow.

## 7. Elementor gotchas this build already solved (keep them solved)

- **H1 and every H2 carry an explicit size at all breakpoints**, equal to the
  prototype's value (`size="var(--text-2xl)"` for section titles,
  `var(--text-hero)` for the H1, `var(--text-xl)` for the promo title). Element
  settings outrank the stylesheet, so a different value here wins over the CSS.
- A class on a native widget lands on the **wrapper**. `brand.py` records it in
  `widget-classes.json` and `port-css.py` re-targets the selector to the inner
  element. A class must be used on one widget kind only (the builder raises if not).
- Containers cannot be `ul`, `li`, `figure`, `blockquote`, `span` or `p`: use
  `tag="li"` and the builder adds `lz-li`; the porter rewrites the selector.
- Bands carry `e-no-lazyload` (added by `B.section`), or Elementor hides their
  background images.
- Site settings required: Elementor "Disable Default Colors" and "Disable Default
  Fonts" = yes, or the kit paints headings blue.
- The estimate form's submit colours are set in the widget (element CSS outranks
  the stylesheet); everything else about the form is in `overrides.css`.
- Never emit `display_condition_list`. Page settings are
  `{"template": "elementor_header_footer", "hide_title": "yes"}`.

## 8. Adding a component (the only way to add new style)

When no block in section 5 fits:

1. **Design it in the prototype language first**: add the markup to a design-source
   page and the CSS to `design-source/v6-1/css/lenz-service.css`, using tokens and
   existing patterns (card radius, shadows, eyebrow, buttons). Never a new hex,
   font or gradient.
2. Add a helper to `brand.py` (shared) or a `block_<name>` to `service_page.py`
   (registered in `BLOCKS`) that emits the same DOM and classes.
3. `python3 projects/lenz/tools/port-css.py`, then rebuild the pages that use it.
   Run the porter once before editing: an unchanged run must reproduce
   `lenz-core.css` byte for byte, or someone edited the output by hand.
4. Check at 1440 / 1024 / 768 / 390 (headless browser is fine), then deploy
   `lenz-core.css` and commit source + output together.
5. **Never hand-edit `lenz-core.css`.** Hand-written exceptions go in
   `plugin/lenz-core/assets/css/src/overrides.css` with a comment saying why.

A one-page visual fix is a site-wide change: the same class is on every page. Check
every page that uses the class before calling it done.
