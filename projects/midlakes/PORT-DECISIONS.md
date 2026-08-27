# Mid Lakes — port decisions & verified Elementor behaviour

**As of 2026-08-27.** The decisions §11 of `docs/Elementor-Output-Anatomy.md` says an
HTML→Elementor port must settle, answered for this site — plus the Elementor
behaviour that was tested on the real install rather than assumed.

**Onboarding ran 2026-08-27, and the site was built the same day.** The
design-system half is folded into
`KIT-ANALYSIS.md`; the "Verified behaviour" section is in `midlakes-page-builder`.
This file stays the canonical record of *why* — nothing enters the CSS cap without a
decision written down here.

---

## The mandate

> "We need to build the Elementor version of the site exactly as it is (lo más
> parecido posible) so the colors and stuff should match exactly."

**Fidelity beats editability.** That is the governing trade-off, and it has a price
worth restating whenever someone asks why the Elementor editor "doesn't work":

> Every property shipped in the child theme stops responding to the Elementor editor.
> Change a button colour in the UI and nothing happens, because the CSS class wins.
> The editor stays a **layout** tool; it stops being a **styling** tool for capped
> properties. The client was told this and chose fidelity.

This is §6 strategy **B-lite**: Elementor supplies the skeleton and everything it can
express; a *capped, named* stylesheet in a child theme supplies what it cannot.

---

## Settled

| # | Decision | Answer |
|---|---|---|
| 1 | **Form system** | **Elementor Pro Forms.** Six identical `quote-form`s → build **once** as a saved Elementor template, not six times |
| 2 | **Custom CSS allowed?** | **Yes** — a `hello-elementor` child theme, **capped** to a named rule list (below). Not a companion plugin: the site stays on Hello Elementor, so a child theme is the simpler container |
| 3 | **Watermarks** | Section **background images with explicit positioning + overlays**. Client places them by hand if positioning cannot match |
| 4 | **Icons** | **Export the six service SVGs to an inline sprite**, referenced from small `html` widgets (§6B pattern). Mix with native/emoji icons so the page never depends entirely on one source |
| 5 | **Brand primary** | **Blue `#2540af`** (`--brand-royal`) — client's call |
| 6 | **CTA / action colour** | **Red `#c10a0a`** (`--brand-red`) — it is the button fill. A separate token slot from primary; there is no conflict |
| 7 | **Blog** | **Archive, not a page.** Already wired: page 16 is the WP posts page. Drops the build to **six real pages** |
| 8 | **Type scale** | **Do NOT collapse it.** The 27 sizes are emitted programmatically by `build.py`, so exactness costs nothing. Record the census; skip the 6–8 step collapse §11.7 recommends — that was a maintainability trade, and fidelity outranks it here |
| 9 | Header / footer | Theme Builder templates in `pages/_theme/` |
| 10 | FAQ `<details>` list | Accordion widget (it already does "only one open") |
| 11 | `service-area` map iframe | Google Maps widget |
| 12 | `nth-child` alternation | Restated per widget — **write it down**, or the pattern breaks the first time someone adds a card |

### Colour roles, from the CSS

- **Blue** — `.why-num` / `.step-num` numerals, alternating service icons,
  `.spec-card--blue` bullets, `.rate-amount`.
- **Red** — buttons, eyebrow dots, the active-nav underline, focus rings, list
  markers. Small areas, high salience.
- **`--ink` `#0f1f35`** — the dominant *surface*: the contact and footer bands.

> **Correction — applied 2026-08-27.** §11 of `Elementor-Output-Anatomy.md` used to
> record decision #7 as *"the brand primary is the red `#c10a0a`. Must be corrected by
> hand."* **That was wrong.** The client confirmed blue is the brand primary; red is
> the CTA. `analyze-prototype.py` inferring `primary: blue` was right. That block has
> been deleted; `KIT-ANALYSIS.md` §1 carries the corrected version.
>
> Onboarding did find **two** `_roles` values that genuinely needed hand-correcting,
> just not this one: `muted` was inferred as `gray` `#8fb2d8` (which is the *on-navy*
> meta colour, 2.20:1 on white) instead of `#5a6472`, and `accent` was absent
> entirely. Both are fixed in `tokens.json`.

---

## The CSS cap — the only rules the child theme may carry

Each one is a property Elementor has **no control for**. Nothing else goes in this
file without a decision recorded here.

| Rule | Why it cannot be native |
|---|---|
| `.ml-btn .elementor-button:hover { transform: translateY(-2px) }` | No transform-on-hover control for buttons. Note the descendant selector — the class lands on the widget *wrapper*, see "Where a CSS class lands" below |
| **Fraunces italic** | Loaded as `ital,opsz,wght@1,9..144,400;1,9..144,500` — the **`opsz` variable axis**. Elementor's font picker has no variable-axis support. The child theme must enqueue the exact Google Fonts URL and apply it by class |
| **`clamp()` h1/h2** | `clamp(2.4rem, 5.2vw, 4rem)` and `clamp(1.8rem, 3.4vw, 2.75rem)`. Continuous fluid scaling; Elementor offers three fixed breakpoints |
| **The rate table** (`/service-agreements/`) | No table widget, and the `<620px` stacking (hide `thead`, each row becomes a card) is pure CSS. Ship the existing markup in one `html` widget |
| **Watermark pseudo-elements** ✅ **ACTIVE** | The condition below was MET — see "The watermark condition fired" |
| **`:focus-visible` rings** ✅ **ACTIVE** | A pseudo-class, with no Elementor control. Not decoration either: the prototype's focus design is the WCAG 2.4.7 / 1.4.11 compliance its own comments document ratio by ratio, and the ring switches colour by band because brand red on navy is 2.62:1 |
| **`.ml-header { backdrop-filter: blur(10px) }`** ✅ **ACTIVE** | Added during the build. Elementor's CSS Filters group emits `filter:`, which blurs an element's OWN CONTENTS — it would smear the logo and the nav instead of the page scrolling under them. There is no `backdrop-filter` control anywhere in Elementor. **Verified empirically: passing `css_filters_*` on the header container generated no CSS at all.** The translucent fill, the hairline and the sticky behaviour are all still Elementor's |

### Cap candidates — SHIPPED on the recommendation, still reversible

Two properties turned up during onboarding that Elementor also cannot express. They
were recorded here rather than added silently, and the build **proceeded on the
recommendation** so the pages could be finished. Both are one rule each, both are
marked `[cap CANDIDATE]` in `mid-lakes.css`, and **either can be removed without
touching a single `build.py`.**

| Candidate | Why | Status |
|---|---|---|
| `.ml-card:hover { transform: translateY(-4px) }` | `.service-card` and `.post-card` lift the same way the button does; Elementor has no transform-on-hover control for containers | **Shipped.** Only the transform is in CSS — the hover box-shadow and border-colour ARE native container controls and stay in `build.py`. That per-property split is the point |
| `.ml-hero::after`, `.ml-comfort::after` | Both photo bands use a **three-stop** overlay gradient; Elementor's control has two. The hero's middle stop lightens through the upper third so the photo reads, then darkens hard behind the copy — exactly what a two-stop approximation flattens | **Shipped.** Every page has a hero, so this could not stay open. The native fallback, if rejected, is a `background_overlay` gradient at 180° `rgba(15,31,53,.45)` → `rgba(15,31,53,.85)` — visibly flatter |

### The watermark condition fired

The cap's conditional row read: *"Watermark pseudo-elements — only if the
background-image route (decision 3) cannot place `1/2/4/6.svg` exactly."*

**It cannot.** Every watermark in the prototype is a `width: 100%; height: <fixed>px`
box, offset OUTSIDE its parent, painted with `background-size: cover`. Elementor's
background controls paint the element's **own box** — they cannot express a 200px-tall
layer hanging 50px below a card, because that layer's height is decoupled from both
the element and the image's 4:1 ratio. Approximating gives a wave of the wrong height
in the wrong place on all six surfaces.

So decision 3's chosen route is unavailable and the fallback the cap already
authorised is what shipped: six pseudo-element rules, verbatim from the prototype.
Elementor never emits pseudo-elements, so there is zero competition.

Two details that came with them:

- **Suppression is by OMISSION.** `.what-happens` sections simply do not get the
  `ml-wm-waves` class, which is cleaner than the prototype's `display: none` override
  and renders identically.
- **`2-flip.svg`** is `2.svg` pre-rotated 180°, generated at build time, because
  Elementor cannot transform a background and the cap should not grow a `transform`
  rule for dressing.
- **The SVGs are child-theme assets, not media-library attachments.** WordPress blocks
  SVG uploads by default, and this keeps them in git.

```css
.hero-overlay    linear-gradient(180deg, rgba(15,31,53,.55) 0%,
                                          rgba(15,31,53,.35) 40%,
                                          rgba(15,31,53,.85) 100%)
.comfort-overlay linear-gradient(100deg, rgba(15,31,53,.94) 0%,
                                          rgba(15,31,53,.80) 45%,
                                          rgba(15,31,53,.35) 100%)
```

**The trap that comes with the watermarks:** `.site-footer { padding-bottom: 300px }`
exists *only* to clear one. If a watermark is dropped, that padding goes with it or
the footer is left with dead space.

**Fraunces is small, distinctive, and the first thing a port loses silently.** It
carries the entire serif voice from three rules — `em`/`.serif` as a general italic
utility, plus `.why-num` and `.step-num`.

---

## Verified Elementor behaviour

Tested on this install (Elementor 4.2.3) by importing a real page, reading the
rendered markup and the generated CSS, then deleting it. Not inferred.

### Where a CSS class lands

`build.py` emits classes programmatically — `_css_classes` for widgets,
`css_classes` for containers (the same field as Advanced → CSS Classes).

```html
<div class="elementor-element ... ml-band e-con e-parent">          <!-- container: on the element itself -->
  <div class="elementor-element ... ml-box e-con-boxed">            <!-- boxed container -->
    <div class="elementor-element ... ml-btn elementor-widget-button">  <!-- widget WRAPPER -->
      <a class="elementor-button elementor-button-link">            <!-- the actual button -->
```

```css
.ml-btn .elementor-button:hover { transform: translateY(-2px); }   /* correct */
.ml-btn:hover { transform: translateY(-2px); }                     /* wrong - moves the wrapper */
```

### `.e-con::before` is ALREADY Elementor's — use `::after`

*(Found 2026-08-27 by looking at a rendered page, after the why-card waves came out
pinned to the top of the card instead of hanging off the bottom.)*

Elementor renders a container's **background overlay** as `.e-con::before`, and that
rule is not passive — it sets position offsets and box size:

```css
.e-con:before { content: var(--background-overlay); position: absolute;
                top:    calc(0px - var(--border-top-width));
                left:   calc(0px - var(--border-left-width));
                width:  max(100% + …, 100%);
                height: max(100% + …, 100%);
                opacity: var(--overlay-opacity); … }
```

A watermark written the way the prototype writes it — `bottom: -100px; height: 200px`,
no `top` — is then **over-constrained**: `top` from Elementor wins, `bottom` is
dropped, and the layer pins itself to the top of the element.

**It still renders.** It looks intentional. It is wrong on every surface anchored to a
bottom or right edge, and nothing warns you.

`.e-con::after` is untouched by Elementor — verified, zero matches in
`frontend.min.css` — so every watermark and both photo overlays live there and compete
with nothing. The single exception is the `.about` band, which needs two layers: its
`::before` is deliberately the **top-left** wave, because that one sets `top` and
`left` explicitly and therefore overrides Elementor's values outright.

> The general lesson, and it is not specific to watermarks: **`::before` on an
> Elementor container is occupied.** Reach for `::after` first.

### Specificity — and the rule that avoids fighting it

Elementor's generated per-element rule is **four classes (0,4,0)**:

```css
.elementor-32 .elementor-element.elementor-element-200026ae .elementor-button { ... }
```

`.ml-btn .elementor-button` is **(0,2,0)**. **Elementor wins.** A class alone will not
override any property Elementor also sets.

> **One owner per property.** Do not fight this with `!important`.
>
> - Child theme owns it → **omit it from `build.py`**. Elementor then generates no
>   rule and the class applies at natural specificity.
> - Elementor owns it → set it in `build.py`, write no CSS for it.
>
> Every rule in the cap above is a property Elementor never sets — `transform`,
> `transition`, pseudo-elements, `clamp()`, the table's stacking. Zero competition.

### Two silent footguns

1. **The button background key is `background_color`, NOT `button_background_color`.**
   A wrong key name does not error — it falls through to
   `var(--e-global-color-accent)`, which on this stock kit is Hello Elementor's
   default. The button renders off-brand with no warning anywhere. With the correct
   key it emits `background-color:#c10a0a` exactly.
2. **`heading(size=2.4)` defaults to `unit="px"`** — a heading meant to be `2.4rem`
   renders at 2.4 *pixels*. Pass `unit="rem"` explicitly.
3. **`typography_font_size_mobile` alone emits no CSS.** *(Found during onboarding,
   2026-08-27.)* Elementor only writes a typography group when
   `typography_typography: "custom"` is present, and `_typo()` sets that flag only
   when `font` **or** `size` is given. The `h1`/`h2` recipe below gives *neither* — it
   passes a mobile size and no desktop size, so the clamp stays unopposed above
   767px. `responsive-audit.py` still passes, because it only checks the key exists.
   Pass `extra={"typography_typography": "custom"}`.

All three belong in `midlakes-page-builder` so no page hits them twice.

### The h1/h2 recipe the cap's `clamp()` rule requires

The child theme owns `h1`/`h2` font-size. `responsive-audit.py` makes a missing
`typography_font_size_mobile` on any `h1`/`h2` an **error**, unconditionally. Both are
satisfied by emitting the **mobile size only**, set to the clamp's floor:

| | clamp resolves to (≤767px) | emit |
|---|---|---|
| `h1` | 38.4–39.9px | `typography_font_size_mobile: 2.4rem` |
| `h2` | exactly 28.8px | `typography_font_size_mobile: 1.8rem` |

Plus footgun 3's flag. No desktop size, no tablet size. `h2` is exact below 767px
(`3.4vw` only exceeds the floor above an 847px viewport); `h1` is within 1.5px at the
very top of the mobile range. Heading **weight, tracking and line-height** stay
Elementor-owned — the child theme's `h1, h2` rule carries font-size only.

### What the build changed on the kit

The kit was recorded as "untouched" at onboarding. Three settings were added — and
the one that was *not* added matters as much as the three that were.

| Setting | Value | Why |
|---|---|---|
| `system_typography` + `body_typography_*` | Manrope | The built-in default was Roboto, so everything that INHERITS (Pro form fields, accordion body, list items, any later text widget) rendered in the wrong face — and every page paid for two unwanted Google Fonts requests |
| `container_width` | 1200px | `--container`, for the editor's benefit |
| `active_breakpoints` + `viewport_tablet_extra` | 1200px | Where the prototype collapses the nav; the Nav Menu widget's Breakpoint dropdown only offers ACTIVE breakpoints |
| `viewport_laptop` | 1400px | The step before it — `styles.css` tightens the nav (gap 28→18, font 0.95→0.9rem) at 1400 before collapsing it at 1200. Elementor's default is 1366, so it is set explicitly |

> **`system_colors` was deliberately left stock.** Colour stays inline in `build.py`.
> The rule for this site is now: **fonts come from the kit, colours are written into
> the page.** Splitting colour between a kit slot and inline values would create two
> sources of truth for the one thing this port most needs to get exactly right.

`tools/set-kit-defaults.php` applies all three, idempotently.

### Precedent

lenz's `tokens.json` already models the class-driven button:

```json
"primary": { "class": "btn btn-primary", "bg": "#1837BE", "text": "#FFFFFF", "bg_hover": "#122A91" },
"_hover_note": "The -1px lift is CSS-owned (lenz.css:107-110). Do NOT substitute an
                Elementor hover_animation like 'grow' - the brand convention is a subtle lift."
```

Same approach; only the container differs (plugin there, child theme here).

---

## Answered 2026-08-27

| Question | Answer |
|---|---|
| **Carrier vs Rheem** | **Carrier.** Fixed in the prototype at `0417f8d` — eight Rheem mentions on home and `service-area` became Carrier. Two of them also dropped *"Authorized"*: **"Carrier Factory Authorized Dealer" is a specific certification and nothing evidences it**, so the copy now says "a Carrier® dealer" / "Carrier® Dealer Quality", matching the client's own About wording. Swap the word back if the certification does exist |
| **Service Finance application URL** | **Leave as it is.** Both financing CTAs stay pointing at `#contact`. Not a placeholder to chase — a deliberate choice. Do not "fix" it |
| **Elementor Pro licence** | **Not a concern** — client's call. Build against Pro (Forms + Theme Builder) as planned. The Local install currently runs **PRO Elements 4.2.2**, the open-source drop-in, while an official Elementor Pro account is upgraded; the widget names and settings keys are identical, so nothing built here changes. See ENVIRONMENT.md for the swap procedure |
| **Form recipient** | **`websites@exploremedia.com`** |

### Form settings still unstated — defaults chosen

The recipient was given; the other two were not. Proceeding on these unless told
otherwise, because both are reversible in the Elementor UI in seconds:

- **Anti-spam: Elementor's built-in honeypot.** No third-party keys to obtain, nothing
  to configure at go-live. Switch to reCAPTCHA only if spam actually arrives.
- **Success state: inline message.** A thank-you *page* is the better choice if
  conversion tracking is ever wanted, since an inline message fires no pageview —
  but nothing has asked for tracking, and a page is a heavier change to undo.

---

## Open — non-blocking

| # | Needed | Blocks |
|---|---|---|
| 1 | **Production domain** — canonical URLs in handoff notes, and `wp elementor replace_urls` at go-live | Go-live |
| 2 | **SEO plugin** (Yoast or Rank Math). None installed, so the prototype's seven hand-written locality-targeted `<title>` tags have nowhere to live | Go-live |

**Nothing blocks the build any more.** Both remaining items are go-live wire-up.
