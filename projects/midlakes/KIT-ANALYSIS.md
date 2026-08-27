# KIT-ANALYSIS — Mid Lakes Heating & Cooling, LLC

**Origin: an HTML/CSS prototype, not an Elementor kit.** `D:\laragon\www\midlakes\public`
(repo `em-midlakes`, level with `origin/main` at `f45edfc`). Seven `index.php` files with
zero `<?php` tags, one 1832-line `styles.css`, one `script.js`.

Written 2026-08-27 from `scripts/analyze-prototype.py` plus a hand read of every page.
The counting is the script's; the judgement below is not. Companions:
`STATUS.md` (where the port is), `ENVIRONMENT.md` (how to reach the install),
`PORT-DECISIONS.md` (what was settled and the Elementor behaviour verified on the
real install). This file folds in what used to be §11's "Open decisions — Mid Lakes"
block in `docs/Elementor-Output-Anatomy.md`, which has been deleted.

**The governing trade-off is fidelity over editability.** The client asked for the
Elementor version to look *exactly* like the prototype, knowing that every property
shipped in the child theme stops responding to the Elementor editor. Read
`PORT-DECISIONS.md` before arguing with anything here.

---

## 0. The one-line summary

Manrope everywhere, Fraunces italic for three decorative numerals, a royal-blue brand
primary with a red CTA, three flat bands (white / paper / navy) plus two photo bands,
a 1200px boxed container, a 14px card radius, a 999px pill button that lifts 2px on
hover, and four wave SVG watermarks bleeding out of six different surfaces.

---

## 1. The palette is real, and it comes from the logo

`styles.css` opens by sampling the five fills out of `MidLakesLogo_*.svg` and then
layers semantic roles over them. Every pairing carries a measured WCAG ratio in a
comment — this design was contrast-checked by hand, so **do not "fix" the ratios
below.**

### Raw brand colours (the logo artwork)

| Token | Hex | In the logo |
|---|---|---|
| `--brand-navy` | `#0f1f35` | "MID LAKES" wordmark |
| `--brand-royal` | `#2540af` | secondary wordmark strokes |
| `--brand-red` | `#c10a0a` | flame accent |
| `--brand-sky` | `#4a9be5` | wave graphic |
| `--brand-pale` | `#8fb2d8` | wave graphic, background lockup |

### The roles that matter

| Role | Token | Hex | What it is FOR |
|---|---|---|---|
| **Brand primary** | `--blue` | `#2540af` | `.why-num` / `.step-num` numerals, even service icons, `.spec-card--blue` bullets, `.rate-amount` |
| **CTA / action** | `--red` | `#c10a0a` | button fill, eyebrow dot, active-nav underline, list markers, focus ring on light |
| Button hover | `--red-dark` | `#a30808` | the hover fill, nothing else |
| Dark **surface** | `--ink` | `#0f1f35` | the contact band and the footer — the dominant dark area |
| Raised on dark | `--ink-2` | `#17293f` | the quote form's card |
| Body text | `--text` | `#1a2436` | light bands |
| Muted text | `--muted` | `#5a6472` | `.lead`, card paragraphs, `.spec-label`, `.legal` |
| Hairline | `--gray-line` | `#dde3ec` | dividers and 1px card borders |
| Band | `--paper` | `#f4f6f9` | the alternating light band, plus the page background |

> **Blue is the primary; red is the CTA. They are separate token slots and there is
> no conflict.** §11 of `Elementor-Output-Anatomy.md` used to claim
> `analyze-prototype.py` inferring `primary: blue` "must be corrected by hand" to the
> red. **That was wrong**, the client confirmed blue, and the claim is gone.

### The two colour pairs a port loses silently

Red and blue each have a **separate on-dark variant**, because the light-band values
fail on navy:

| On light | On navy | Why |
|---|---|---|
| `--red-text` `#c10a0a` | `--red-on-dark` `#ff8b8b` | `#c10a0a` on navy is **2.62:1** — unreadable |
| `--blue` `#2540af` | `--blue-on-dark` `#6fb3ec` | same problem |
| `--focus` `#c10a0a` | `--focus-dark` `#4a9be5` | the focus ring switches band by band |

**Never put `#c10a0a` text on `#0f1f35`.** The contact band's phone link is
`#ff8b8b`; the `.contact-details dt` eyebrows are `#6fb3ec`. If a new section lands on
the ink band, use the on-dark pair.

### One inference the script got wrong

`site_tokens.py` infers the canonical `muted` role by trying key names in order, and
`gray` comes before `muted`. On this site `--gray` is `#8fb2d8` — **meta text on
navy**, 2.20:1 on white. The real light-band muted is `--muted` `#5a6472`.
`tokens.json` now pins `_roles.muted = "muted"` explicitly. It also binds
`accent → red`, which the inference left as `None` because no key is called
`accent`/`cta`/`highlight`.

---

## 2. Typography

Two families. **Manrope** (400/500/600/700/800) does everything —
there is no `font-family` on `h1/h2/h3`, so headings inherit `body`. **Fraunces**
appears only as an italic accent, from three rules, and carries the entire serif
voice of the design:

- `em, .serif` — a general italic utility
- `.why-num` — the `01 02 03 04` value numerals
- `.step-num` — the `1 2 3 4` process numerals

**Fraunces is the first thing this port loses silently.** It is loaded on the
`ital,opsz,wght@1,9..144,400;1,9..144,500` **variable `opsz` axis**, which Elementor's
font picker cannot express. The child theme enqueues the exact Google Fonts URL and
applies it by class. See the cap in §7.

### The type scale is not collapsed — on purpose

27 distinct sizes. §11.7 of the anatomy doc recommends collapsing a drifted census to
6–8 steps; **that recommendation is declined here** (PORT-DECISIONS decision 8). The
sizes are emitted programmatically by `build.py`, so exactness costs nothing, and the
collapse was a *maintainability* trade — fidelity outranks it on this job.

The full census lives in `tokens.json` → `type_scale`, keyed by the component that
owns each size. Headline shape:

| rem | Owner |
|---|---|
| `clamp(2.4, 5.2vw, 4)` | `h1` |
| `clamp(1.8, 3.4vw, 2.75)` | `h2` |
| 2.2 | `.stat-num` (800, `-0.03em`) |
| 1.7 / 1.6 | `.step-num` / `.why-num` — **Fraunces italic 500** |
| 1.55 / 1.5 / 1.35 / 1.3 / 1.2 / 1.15 / 1.08 | h3-class headings, largest → smallest |
| 1.12 / 1.1 | `.hero-sub` / `.lead` |
| 1.05 / 1.02 / 0.98 / 0.96 / 0.95 / 0.94 / 0.92 / 0.9 / 0.88 / 0.85 / 0.82 / 0.78 / 0.72 | body, UI and label sizes |

All headings: **weight 800, `line-height: 1.1`, `letter-spacing: -0.02em`.** Body:
`line-height: 1.6`.

### The `clamp()` heads, and how the responsive gate is satisfied

`clamp()` is continuous; Elementor has three fixed breakpoints. The child theme owns
`h1`/`h2` **font-size** — but `responsive-audit.py` makes a missing
`typography_font_size_mobile` on any `h1`/`h2` an **error**, unconditionally.

Both facts are satisfiable at once, because the clamp's mobile value *is* its floor:

| | clamp resolves to (≤767px) | emit |
|---|---|---|
| `h1` | 38.4–39.9px | `typography_font_size_mobile: 2.4rem` (38.4px) |
| `h2` | exactly 28.8px | `typography_font_size_mobile: 1.8rem` (28.8px) |

So: **emit the mobile size only, and no desktop or tablet size.** Elementor writes a
`@media (max-width:767px)` rule that reproduces the floor; above that the child
theme's `clamp()` is unopposed and scales fluidly. h2 is exact; h1 is within 1.5px at
the very top of the mobile range.

⚠️ **This needs `typography_typography: "custom"` passed explicitly** — see the third
footgun in `midlakes-page-builder`.

Weight, tracking and line-height on headings are **Elementor-owned** (the child
theme's `h1,h2,h3` rule carries font-size only), so `build.py` emits them normally.

---

## 3. The button — a red pill that lifts

```
.btn         inline-flex, gap 8, padding 14/26, radius 999px, weight 700,
             font-size 0.95rem, border 1.5px solid transparent, nowrap
.btn:hover   transform: translateY(-2px)              <- CSS-owned
.btn-primary background #c10a0a / color #fff
             :hover     #a30808
.btn-ghost   transparent / #fff / border rgba(255,255,255,.5)
             :hover     background rgba(255,255,255,.1)     <- photo bands only
.btn-block   width: 100%                                    <- the form submit
```

Two rules that bite:

1. **The lift is CSS-owned.** Do **not** substitute an Elementor `hover_animation`
   (`grow`, `float`, `shrink`). The brand convention is a 2px lift on a 0.15s ease,
   and the child theme already ships it. This mirrors lenz's `_hover_note` precedent.
2. **The Elementor key is `background_color`, not `button_background_color`.** A
   wrong key name does not error — it falls through to `var(--e-global-color-accent)`,
   which on this stock kit is Hello Elementor's default. The button renders off-brand
   with no warning anywhere.

---

## 4. Section rhythm — and the three places it deliberately doubles

Bands, by class:

| Class | Band |
|---|---|
| `.about`, `.why` | **white** `#ffffff` |
| `.services`, `.faq`, `.hero-compact`, `.legal` | **paper** `#f4f6f9` |
| `.contact`, `.site-footer` | **ink** `#0f1f35` |
| `.hero` / `.hero-page`, `.comfort` | **photo** + a navy overlay gradient |

Vertical rhythm: `.section` is `96px 0`, dropping to `64px 0` below 620px. `.comfort`
is `120/80`. The hero is `min-height: 640px` with `padding-top: 120px` (an interior
`.hero-page` is `460px` / `104px`). The container is `1200px` with `24px` of its own
side padding.

### Band order, page by page — this is the anatomy to build to

```
home                hero · white · paper · comfort · white · paper · ink
about-us            hero · white · paper · white · WHITE · comfort · paper · white · ink
services            hero · section-nav · white · paper · white · comfort · paper · white · ink
service-agreements  hero · white · paper · white · WHITE · paper · ink
service-area        hero · white · paper · white · paper · ink
financing           hero · white · paper · white · paper · white · paper · white · ink · paper(legal)
blog                hero-compact(paper) · PAPER · comfort
```

> **The three capitalised doubles are real and deliberate** — `about` then `why`
> (both white) on `/about-us/`, `about` then `about what-happens` (both white) on
> `/service-agreements/`, and `hero-compact` then `services` (both paper) on `/blog/`.
> The usual "never two identical bands adjacent" rule **does not apply to this site**.
> They are in the page-audit's *do NOT fix* list.

---

## 5. Component vocabulary

What each one is, and whether Elementor can draw it. "Native" means it stays editable
in the Elementor UI; "class" means the child theme owns it.

| Component | Structure | Elementor? |
|---|---|---|
| **Eyebrow** | `.eyebrow` — 0.72rem/700/`0.18em`/uppercase red, preceded by a 7px red dot | Native. Emit as a text widget whose HTML carries an inline-styled `<span>` for the dot |
| **Hero** | photo + 3-stop overlay, `min-height` 640, copy bottom-aligned, H1 + sub + two buttons + `.hero-creds` rule-topped list | Native **except the overlay** (§6) |
| **Hero creds** | flex-wrap list, `<strong>` value + label, 1px top rule `rgba(255,255,255,.18)` | Native |
| **Stats column** | `.stats` — 2.2rem/800 numeral + 0.9rem muted label, each `li` with a bottom hairline, last one without | Native. Restate the last-child border removal |
| **Promise list** | `.promise` — a 3px red **left border** + 20px left padding per item, h3 + muted p | Native (container `border-left`) |
| **Service card** | white, radius 14, 1px `#dde3ec`, pad 32/28, `min-height: 350`, 52px tinted icon tile (radius 12) + h3 + muted p; **hover** lift −4px + `0 18px 40px -24px rgba(15,31,53,.35)` + `border-color: transparent` | Native except the hover **transform** — a cap candidate (§7) |
| **Why card** | paper fill on the white band, radius 14, pad 36/32, 1px border, Fraunces italic numeral + h3 + muted p | Native except Fraunces |
| **Spec card** | white, radius 14, pad 26, uppercase `.spec-label` + check list; `--blue` modifier swaps the marker colour | Native. Use `fas fa-check-circle` for the marker |
| **Comfort band** | photo + 100° 3-stop overlay, copy capped at 560px, `.perk-list` with red disc + white check | Native except the overlay |
| **FAQ** | `<details>` list, JS forces one-open, plus/minus pseudo-element mark, beside a 4:5 photo with a gradient caption | **Accordion widget** (decision 10 — it already does one-open) |
| **Contact band** | ink, `dl` of uppercase blue-on-dark `dt` + 1.1rem `dd`, beside the `.quote-form` card on `#17293f` | Native |
| **Quote form** | 5 fields, two 2-up rows + a full-width textarea, real `<label>`s, sky focus border | **Elementor Pro Form**, built **once** as a saved template (decision 1) |
| **Detail row** | 1.15fr/1fr, 52px vertical padding, top hairline, `--flip` reverses order; copy + spec card | Native. First row drops its top border and pads 8px |
| **Section nav** | sticky at `top: 76px`, horizontally scrolling anchor bar, red underline on hover | Native-ish (sticky container + a link row); the `76px` offset is a one-liner if it drifts |
| **Chips** | pill, white, 1px border, 0.92rem/600 | Native |
| **Steps** | 4-up, 2px top rule, Fraunces italic numeral, h3 + two muted paragraphs | Native except Fraunces |
| **Area list** | bordered rows, 1.02rem/600, last without a border | Native |
| **Map** | Google Maps iframe in a radius-14 bordered frame, `min-height` 420 / 320 mobile | **Google Maps widget** (decision 11) |
| **Rate table** | 3 columns, `min-width: 620px` with a scrolling wrapper; below 620px `thead` hides and each row becomes a card | **One `html` widget** + the cap's `.ml-rate-table` rule. No table widget exists and the stacking is pure CSS |
| **Post grid** | 3-up cards, 16:9 thumb, body flex-column with a `margin-top:auto` "Read more" | **Archive template**, not a page (decision 7) |
| **Legal** | paper, top hairline, 0.85rem muted, 90ch | Native |

---

## 6. Two gradients Elementor cannot draw

Both photo bands use a **three-stop** overlay. Elementor's gradient control offers
two stops:

```css
.hero-overlay    linear-gradient(180deg, rgba(15,31,53,.55) 0%,
                                          rgba(15,31,53,.35) 40%,
                                          rgba(15,31,53,.85) 100%)
.comfort-overlay linear-gradient(100deg, rgba(15,31,53,.94) 0%,
                                          rgba(15,31,53,.80) 45%,
                                          rgba(15,31,53,.35) 100%)
```

The hero's middle stop is the design's whole trick: it *lightens* through the upper
third so the photo reads, then darkens hard behind the copy. A two-stop
approximation flattens exactly that.

**This is not in the CSS cap.** Two ways out, and it needs a call:

- **(a) Approximate natively** — `background_overlay` gradient, 180°,
  `rgba(15,31,53,.45)` → `rgba(15,31,53,.85)`. Free, editable, visibly flatter.
- **(b) Add two named rules to the cap** — `.ml-hero::after` and
  `.ml-comfort::after` carrying the exact gradients, with the containers emitting
  the background image only. Exact, and consistent with "fidelity beats editability".

**Recommendation: (b).** It is two rules, it matches the mandate, and the cap already
exists as a container for precisely this. Recorded as a *candidate* in
`tokens.json → css_cap.candidates` rather than a settled rule — confirm before the
hero is built, because every page has one.

---

## 7. The CSS cap

A `hello-elementor` **child theme** named `mid-lakes` (decision 2 — not a companion
plugin; the site stays on Hello, so a child theme is the simpler container). Capped to
a named rule list. **Nothing else goes in it without a decision recorded in
`PORT-DECISIONS.md`. No `!important`.**

As built (`theme/mid-lakes/assets/mid-lakes.css`):

| Rule | Why Elementor cannot |
|---|---|
| `.ml-btn .elementor-button:hover { transform: translateY(-2px) }` | no transform-on-hover control for buttons |
| Fraunces italic (`.ml-serif`, `.ml-why-num`, `.ml-step-num`) | the `opsz` **variable axis** has no font-picker support |
| `.ml-h1` / `.ml-h2 { font-size: clamp(...) }` | continuous fluid scaling vs. three fixed breakpoints |
| `.ml-rate-table` (the whole table + its `<620px` card stacking) | no table widget; the stacking is pure CSS |
| **The six watermark pseudo-elements** | the conditional row **fired** — see below |
| **`:focus-visible` rings** | a pseudo-class, and the design's WCAG compliance, not decoration |
| **`.ml-header { backdrop-filter: blur(10px) }`** | no backdrop-filter control anywhere; Elementor's CSS Filters group emits `filter:`, which would blur the header's own contents. Verified: `css_filters_*` generated no CSS at all |
| `.ml-card:hover { transform: translateY(-4px) }` | **cap CANDIDATE, shipped** — the button's twin |
| `.ml-hero::after` / `.ml-comfort::after` | **cap CANDIDATE, shipped** — the two 3-stop overlays from §6 |

### The watermark condition fired

The cap's conditional row read *"only if the background-image route cannot place
`1/2/4/6.svg` exactly."* **It cannot.** Every watermark is a
`width: 100%; height: <fixed>px` box offset OUTSIDE its parent with
`background-size: cover`; Elementor's background controls paint the element's **own
box**, so the layer's height is decoupled from both the element and the image's 4:1
ratio. Approximating puts a wave of the wrong height in the wrong place on all six
surfaces. So the fallback the cap already authorised is what shipped.

### One owner per property, per property

The splits are deliberate and worth stating, because they look inconsistent until you
see the rule: the card's hover **transform** is CSS but its hover **shadow and
border-colour** are native container controls in `build.py`; the header's **blur** is
CSS but its **fill, hairline and sticky behaviour** are Elementor's. The line is not
drawn per component — it is drawn per property, at exactly the point where Elementor
runs out of controls.

**The trap that comes with the watermarks:** `.site-footer { padding-bottom: 300px }`
exists *only* to clear one. If a watermark is dropped, that padding goes with it or
the footer is left with dead space.

### One owner per property

Elementor's per-element rule is **four classes (0,4,0)**; a bare class is (0,2,0).
Elementor always wins. Do not fight it:

- Child theme owns it → **omit it from `build.py`** entirely.
- Elementor owns it → set it in `build.py`, write no CSS for it.

Every capped rule is a property Elementor never sets — zero competition.

---

## 8. Watermarks

Four wave SVGs (`1/2/4/6.svg`, all `viewBox="0 0 2000 500"`) applied through
`::before`/`::after` on six surfaces. Decision 3: **section/card background images
with explicit positioning + overlays**; the client places them by hand if positioning
cannot match.

| Surface | File | Box | Position | Opacity |
|---|---|---|---|---|
| `.about` | `2.svg` | 100% × 400 | `right:-200 bottom:-250` | 1.0 |
| `.about` (second) | `2.svg` | 100% × 400 | `left:-200 top:-250`, **flipped X+Y** | 1.0 |
| `.service-card` | `1.svg` | 100% × 200 | `bottom:-50 left:0` | 0.3 |
| `.why-card`, `.spec-card` | `4.svg` | 100% × 200 | `bottom:-100 left:0` | 0.3 |
| `section#contact` | `6.svg` | 100% × 200 | `top:0 left:0` | 0.3 |
| `.site-footer` | `1.svg` | 100% × 200 | `bottom:0 left:0` | 0.1 |

Three things worth knowing before porting these:

1. **The opacity ones are natively expressible.** Elementor's `background_overlay`
   takes an image *and* an opacity — so a card is `background_color: #fff` plus a
   `background_overlay` image at `0.3`, positioned bottom. No CSS needed.
2. **The `.about` pair is the awkward one** — two full-opacity images on one section,
   one of them mirrored. Elementor cannot transform a background. Ship a pre-flipped
   `2-flip.svg` and use image + overlay.
3. **`.what-happens.about::before/::after` are `display: none`** — `/about-us/` and
   `/service-agreements/` each carry one `.about` section that must **not** get the
   wave pair.

**WordPress blocks SVG uploads by default.** Ship all four watermarks and both logos
as **child-theme assets** (`assets/`), not media-library attachments. They stay in git
that way too.

---

## 9. The `nth-child` alternations — write them down

Elementor has no positional selector, so every one of these is restated widget by
widget. **This list is the source of truth; the pattern breaks the first time someone
adds a card without it.**

| Rule | Restated as |
|---|---|
| `.service-card:nth-child(even) .service-icon` | tiles run **red, blue, red, blue, red, blue** across the 6-card grid (odd = `rgba(193,10,10,.09)`/`#c10a0a`, even = `rgba(37,64,175,.10)`/`#2540af`) |
| `.why-card:nth-child(odd) .why-num` | numerals run **red, blue, red, blue** (base is blue; odd overrides to red) |
| `.step:nth-child(odd) .step-num` | numerals run **red, blue, red, blue** across the 4 steps |
| `.spec-card--blue` | not positional — on `/services/` the **flipped** detail rows get the blue card. Rows run red, blue, red / red, blue, red |
| `.stats li:last-child`, `.area-list li:last-child`, `.rate-table tbody tr:last-child` | the last item drops its bottom hairline |
| `.detail-row:first-of-type` | no top border, `padding-top: 8px` |

---

## 10. Accessibility decisions the design already made — do not "fix" them

- **Focus is designed, not default.** 3px outline, `offset: 3px`, radius 4 — `--focus`
  `#c10a0a` on light bands and `--focus-dark` `#4a9be5` on the hero / comfort /
  contact / footer / faq-media. Form fields get a *filled* ring instead
  (`outline-offset: 0`) so it isn't clipped inside the card.
- **`@media (forced-colors: active)`** is honoured — Windows/macOS high contrast.
- **`prefers-reduced-motion`** disables the reveal animation, and there is a 2.5s
  safety net that un-hides everything if the IntersectionObserver misfires.
- **Every form field has a real `<label>`** — placeholders are supplementary, never
  the label.
- **Inline prose links are underlined** and coloured (`--red-text`, or `--red-on-dark`
  in `.comfort-sub`), scoped to body copy only, because the base rule is
  `color: inherit` — WCAG 1.4.1.
- `.hero-creds` and `.main-nav` carry `aria-label`s; the FAQ marks and eyebrow dots
  are `aria-hidden`.

---

## 11. Voice

Sampled from all seven pages. **Neighbourly and de-escalating, not promotional.** The
reader is a Loganville homeowner whose house is uncomfortable and who does not know
what is wrong.

- **Second person, contractions, short paragraphs.** *"You don't have to know exactly
  what's wrong before you call us."*
- **Lower the stakes before selling.** *"Sometimes the problem isn't your HVAC
  equipment at all."* / *"If a repair makes sense, we'll tell you."* / *"Financing is
  simply another option."*
- **Hedged, never promissory.** *may*, *can help*, *depends on*, *subject to credit
  approval*. Benefit lists are written as *"Encapsulation can help:"*, not "will".
- **Local specificity.** Loganville, Walton and Gwinnett Counties, "Georgia summers",
  "a hot Georgia afternoon", the humidity, named towns.
- **Family-owned is the identity**, restated on every page, alongside the four earned
  proof points: **since 2018**, **75+ years combined**, **24/7 live emergency**,
  **licensed & insured + Parts & Labor Guarantee**.
- **No hype.** No exclamation marks except one *"Yes!"*, no superlatives, no
  competitor jabs, no invented statistics.

Full rules, headline patterns and mechanics: `skills/midlakes-content-style`.

---

## 12. The decisions §11 said to settle — settled

Folded in from `docs/Elementor-Output-Anatomy.md` §11, which no longer carries a Mid
Lakes block. Full reasoning in `PORT-DECISIONS.md`.

| # | Decision | Answer |
|---|---|---|
| 1 | Form system | **Elementor Pro Forms**, built **once** as a saved template. Recipient `websites@exploremedia.com`, honeypot anti-spam, inline success message |
| 2 | Custom CSS allowed? | **Yes** — a capped `mid-lakes` child theme (§7) |
| 3 | Watermarks | Background images + overlays (§8) |
| 4 | Icons | Inline **SVG sprite** for the six service icons, mixed with native/emoji icons |
| 5 | Brand primary | **Blue `#2540af`** |
| 6 | CTA colour | **Red `#c10a0a`** |
| 7 | Blog | **Archive template**, not a page → **six real pages** |
| 8 | Type scale | **Do not collapse.** Record the census (§2) |
| 9 | Header / footer | Theme Builder templates in `pages/_theme/` |
| 10 | FAQ `<details>` | Accordion widget |
| 11 | Map iframe | Google Maps widget |
| 12 | `nth-child` | Restated per widget — the list in §9 |

**Answered 2026-08-27:** Carrier (not Rheem, and **not** "Factory Authorized" — that
is a specific certification and nothing evidences it); the Service Finance CTAs stay
pointing at `#contact` deliberately; Elementor Pro is fine; form recipient
`websites@exploremedia.com`.

**Still open, neither blocking the build:** the production domain, and an SEO plugin
for the seven hand-written locality-targeted `<title>` tags (they are parked in
`tokens.json → pages.seo`).

---

## 13. Measurements, as of this file

| | |
|---|---|
| Pages | 7 `index.php`, zero `<?php` tags |
| CSS | 1832 lines, one file |
| Fonts | Manrope 400–800 + Fraunces italic (`opsz` axis) |
| Container | 1200px |
| Radius | 14px |
| Bands | white · paper `#f4f6f9` · ink `#0f1f35` + two photo bands |
| Font sizes | 27 distinct (25 fixed + 2 `clamp()`) |
| Forms | 6 identical `quote-form`s, JS-only, no backend |
| Images | 5 webp, 2 logo SVG, 4 watermark SVG |
| Button | `#c10a0a` → `#a30808` + `translateY(-2px)`, radius 999px |

> The numbers in §11 of `docs/Elementor-Output-Anatomy.md` (6 pages, 1698 CSS lines,
> 5 forms) predated the About page. That block has been deleted; these are current.
