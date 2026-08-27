# Mid Lakes — port decisions & verified Elementor behaviour

**As of 2026-08-27.** The decisions §11 of `docs/Elementor-Output-Anatomy.md` says an
HTML→Elementor port must settle, answered for this site — plus the Elementor
behaviour that was tested on the real install rather than assumed.

Fold the design-system half into `KIT-ANALYSIS.md` when onboarding runs. The
"Verified behaviour" section belongs in the generated `midlakes-page-builder` skill.

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

> **Correction.** §11 of `Elementor-Output-Anatomy.md` records decision #7 as *"the
> brand primary is the red `#c10a0a`. Must be corrected by hand."* **That is wrong.**
> The client confirmed blue is the brand primary; red is the CTA. `analyze-prototype.py`
> inferring `primary: blue` was right. Fix that block when it folds into
> `KIT-ANALYSIS.md`.

---

## The CSS cap — the only rules the child theme may carry

Each one is a property Elementor has **no control for**. Nothing else goes in this
file without a decision recorded here.

| Rule | Why it cannot be native |
|---|---|
| `.btn:hover { transform: translateY(-2px) }` | No transform-on-hover control for buttons |
| **Fraunces italic** | Loaded as `ital,opsz,wght@1,9..144,400;1,9..144,500` — the **`opsz` variable axis**. Elementor's font picker has no variable-axis support. The child theme must enqueue the exact Google Fonts URL and apply it by class |
| **`clamp()` h1/h2** | `clamp(2.4rem, 5.2vw, 4rem)` and `clamp(1.8rem, 3.4vw, 2.75rem)`. Continuous fluid scaling; Elementor offers three fixed breakpoints |
| **The rate table** (`/service-agreements/`) | No table widget, and the `<620px` stacking (hide `thead`, each row becomes a card) is pure CSS. Ship the existing markup in one `html` widget |
| **Watermark pseudo-elements** | Only if the background-image route (decision 3) cannot place `1/2/4/6.svg` exactly |

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

Both belong in `midlakes-page-builder` so no page hits them twice.

### Precedent

lenz's `tokens.json` already models the class-driven button:

```json
"primary": { "class": "btn btn-primary", "bg": "#1837BE", "text": "#FFFFFF", "bg_hover": "#122A91" },
"_hover_note": "The -1px lift is CSS-owned (lenz.css:107-110). Do NOT substitute an
                Elementor hover_animation like 'grow' - the brand convention is a subtle lift."
```

Same approach; only the container differs (plugin there, child theme here).

---

## Open — blocking

| # | Needed | Blocks |
|---|---|---|
| 1 | **Form recipient email**, **anti-spam** (Elementor honeypot vs. reCAPTCHA + keys), **success state** (inline message vs. thank-you page — the latter is what conversion tracking needs) | The form template, so every page |
| 2 | **Elementor Pro licence status.** A key is present, but the options show `_elementor_pro_free_trial_data` and **no licence-data record** — it looks like a **trial**. Theme Builder and Forms are both Pro-only; if it lapses the header, footer and all six forms stop working | Everything |
| 3 | **Carrier vs Rheem.** About says *Carrier Dealer*; home and services say *Rheem® Authorized*. Unresolved since the content work — one is wrong and it gets baked in | About, home, services content |
| 4 | **Service Finance application URL.** Both financing CTAs still point at `#contact` as a placeholder | Financing content |
| 5 | **Production domain** — canonical URLs in handoff notes, and `wp elementor replace_urls` at go-live | Go-live |
| 6 | **SEO plugin** (Yoast or Rank Math). None installed, so the prototype's seven hand-written locality-targeted `<title>` tags have nowhere to live | Go-live |

Items 3 and 4 block page *content*. The rest block go-live rather than the build.
