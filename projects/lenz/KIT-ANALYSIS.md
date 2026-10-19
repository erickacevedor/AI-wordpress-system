# Lenz Heating & Cooling — Kit Analysis

Companion to `tokens.json` and the generated `lenz-*` skills.

> **This was not produced by `elementor-kit-onboarding`.** `lenz-2026` is a clean
> WordPress install — there was no kit to mine. Instead the design system was read
> directly from the source project at `d:/laragon/www/lenz`, which ships a fully
> documented token file (`tokens.css`) with contrast ratios baked into the comments,
> plus `css/lenz-v4.css` where nearly every non-obvious value carries its rationale.
> That is a *better* source than widget-mining would recover, so the usual
> archaeology step was replaced with translation. Everything below is traceable to a
> line in those two files.

- **Site:** Lenz Heating & Cooling (`lenzheatingandcooling.com`) — Urbandale, IA.
  Veteran- and woman-owned, family-run, serving the Des Moines metro since 2009.
- **Build target:** **v4** — the colorful "family" body (navy/gradient hero, gradient
  service blocks) with a light cream top nav. v5 is its dark-header sibling; the body
  is identical and only the header surface differs.
- **Stack:** WP 7.0.4 · Hello Elementor 3.4.9 · Elementor 4.2.2 · PRO Elements 4.1.0.
- **Globals:** we are **creating** them, not inheriting them. Task #6 pushes the
  semantic roles into Site Settings and writes the resulting ids back into
  `tokens.json`. Until then, emitters use inline hex.

---

## Palette

Four brand ramps (50→900) plus neutrals. The full ramps live in `tokens.json`; these
are the roles that actually get used.

| Role | Hex | Use |
|---|---|---|
| Deep Navy | `#07113B` | Dominant dark ground — hero, CTA band, reviews, close form |
| Brand blue | `#1A3BCC` | Brand base |
| CTA blue | `#1837BE` | Primary button background (9.02:1 on white) |
| Cream | `#FFFCF0` | The page's warm surface — services, financing, plans, about, FAQs |
| Mist | `#F1F4FD` | The one blue-tinted band (credentials) |
| Flame Gold | `#FFC600` | Gold CTA, accents, the Financing pill |
| Accent rust | `#D6410F` | Eyebrows and icons on light surfaces (4.54:1) |
| Display orange | `#F05A28` | Large display type + gradients **only** |
| Purple | `#7B2D8B` | The cool end of the temperature gradient |

### Contrast rules — the part most likely to get broken

These are deliberate and hard-won. They are the reason the palette looks the way it does.

1. **Gold never carries white text.** `#FFC600` is inherently light; it pairs with
   `#121212` only.
2. **`--orange-500` is display-only.** At 3.39:1 it fails body text. `--orange-600`
   (`#C83D0E`, 5.09:1) is the first body-safe orange, and `--color-accent`
   (`#D6410F`, 4.54:1) is the corrected value actually used for eyebrows.
3. **Eyebrows are an allow-list, not a deny-list** (`lenz.css:63-73`). Rust is the
   default; only genuinely dark panels opt into gold. This was inverted after a new
   light section shipped with an invisible gold eyebrow — do not flip it back.
4. **The financing eyebrow is navy.** Gold and orange both collapse against the warm
   gradient; navy is the only value clearing 4.5:1 across the whole stop range.
5. **Focus rings are two-ring** (gold + navy on light, gold + white on dark) and are
   CSS-owned.

---

## Typography

**Montserrat** (700/800) for headings, **Open Sans** (400/600/700) for body. Major
Third scale, 16px base: 10 · 13 · 16 · 20 · 25 · 31 · 39 · 49 · 61.

| Level | Desktop | Tablet | Mobile |
|---|---|---|---|
| Hero h1 | 61 | 48 | 39 |
| Section h2 | 39 | 33 | 28 |
| Lead-card h3 | 31 | 27 | 24 |
| Card h3 | 25 | 23 | 21 |
| Lead paragraph | 20 | — | — |
| Body | 16 | — | — |
| Eyebrow | 10, `0.14em`, uppercase | — | — |

The hero is `clamp(39px, 4.6vw + 12px, 61px)` in source. Elementor's three-breakpoint
model can't express a clamp, so h1 gets explicit desktop/tablet/mobile sizes — and
**every h1 and h2 must carry them**, or the responsive gate fails and the heading
silently won't shrink.

Measure is capped at `62ch`.

---

## Buttons

Pill (`999px`), 2px border, 48px min-height, Montserrat 700 at 16px, 24px inline padding.

| Variant | Background | Text |
|---|---|---|
| `btn-primary` | `#1837BE` → `#122A91` hover | white |
| `btn-gold` | `#FFC600` → `#FFCF29` hover | `#121212` |
| `btn-outline` | transparent, `#BDBDBD` border | `#122A91` |
| `btn-outline-light` | transparent, white 40% border | white |
| `btn-navy` | `#07113B` | white |
| `btn-ghost-navy` | white 86% | `#07113B` |

**Hover convention: a `translateY(-1px)` lift plus a background change.** This is
CSS-owned. Do **not** substitute an Elementor `hover_animation` like `grow` or
`shrink` — that's a different brand's convention.

---

## Gradients — the central translation decision

Thirteen gradient surfaces. They split two ways, and the split is the single most
important thing in this document.

### Native (5 surfaces) — real Elementor gradient backgrounds

| Surface | Gradient |
|---|---|
| `.lead-card--cool` | `cool` — 135°, `#1A3BCC → #07113B` |
| `.lead-card--warm` | `temperature` — 135°, `#F05A28 → #7B2D8B` |
| `.lead-card--air` | `air` — 135°, `#8F34A2 → #122A91` |
| `.lead-card--extra` | `extra` — 135°, `#122A91 → #07113B` |
| `.financing__panel` | `warm` — 135°, `#FFC600 → #F05A28` |

These stay editable in Elementor, and their stops **do** reference Global Colors —
verified on the render, where they emit as
`linear-gradient(135deg, var(--e-global-color-lzorange) 0%, …)`. So changing the brand
purple updates the heating lead card. Keys confirmed against the repo's existing 4.x
kits, and global stops belong in `__globals__` (not in the colour value).

> **Revised during build:** the plan badge and the BLUE plan stripe were originally
> listed here as native. They ended up CSS-owned instead — both are inline decorations
> *inside* a card, and wrapping a 6px bar in its own Elementor container to get a
> background would be structure for structure's sake. Native surfaces: 5, not 7.

**`.lead-card--warm` uses `--gradient-temperature`, NOT `--gradient-warm`.** The class
name and the gradient name disagree in the source; `--gradient-warm` (gold→orange)
belongs to the financing panel. Collapsing the two silently swaps two brand gradients —
this shipped wrong for one build before it was caught.

### CSS-only (6 rules) — Elementor has no control for these

| Rule | Why |
|---|---|
| `.gradient-text`, `.hero h1 .accent`, `.vprop__num`, `.about__stat b` | `background-clip:text` (5 usages) |
| `.hero::before` | two stacked radials with `120% 90% at 88% 8%` sizing |
| `.lead-card::after` | radial white sheen at `120% 100% at 100% 0%` |
| `.cta-band::before` | three rgba stops; Elementor takes two |
| `.marquee` | gradient as `mask-image` |
| `.skel` | animated gradient keyframes |

These live in the `lenz-core` plugin's master stylesheet, with the small subset that
must travel inside a kit export mirrored into Site Settings → Custom CSS.

---

## Section rhythm

`hero (navy) → trustbar (blue-800) → services (cream) → cta-band (navy) → financing
(cream + warm panel) → valueprops (white) → plans (cream) → reviews (navy) → brands
(white) → about (cream) → who13 (white) → creds (mist) → area (white) → faqs (cream)
→ close-form (navy) → footer (neutral-900)`

Never two identical backgrounds back to back. Navy bands are the rhythm breaks; cream
and white alternate between them.

---

## Signature components

- **Lead card** — gradient background, 28px radius, white icon tile at 16% white,
  gold "go" link. Four of them, two across, never four (at four the columns fell to
  ~230px and wrapped body copy every three words).
- **Service card** — white, 1px border, 18px radius, category-tinted icon tile
  (`data-cat` = cooling / heating / both).
- **Trust bar** — five proofs in a 5-column grid whose 1px gaps *are* the borders,
  gold values on `blue-800`.
- **Plan card** — three tiers, BLUE is the recommended flagship with a 2px blue border
  and a gradient "Recommended" badge.
- **Marquee** — nine brand wordmarks, two cloned tracks, edge-faded by a gradient mask,
  pausable on hover and focus, frozen to a wrapped grid under `prefers-reduced-motion`.

---

## Deviation from the portable standard: icons

`AGENTS.md` §3 says to **mix emoji in as icons** so a page never depends entirely on
an icon font. Lenz does **not** follow that rule, deliberately.

The reason the standard exists — a missing icon font blanking the page — does not
apply here: there is no icon font. The 24 Lucide symbols are an inlined `<symbol>`
sprite injected by `lenz-core`, with no external request and no font dependency, so
they cannot fail to load independently of the page. Substituting emoji would also
break the contrast rule the design leans on: every sprite icon inherits
`stroke="currentColor"`, which is what keeps an eyebrow's icon the same colour as its
label. Emoji carry their own fixed colours and would ignore the allow-list entirely.

The standard's *goal* (never depend on a fragile icon font) is met by a different
means. Do not "fix" this by adding emoji.

## Elementor translation decisions (settled 2026-08-14)

| Question | Decision |
|---|---|
| Starting point | Clean build on `lenz-2026`; tokens authored from `tokens.css` |
| Header mega menu | PRO Mega Menu widget **+ a JS shim** restoring roving arrows, Tab containment and Escape-returns-focus from `lenz.js:62-152` |
| The 18 services | **Hand-assembled Elementor containers** (revised 2026-08-14, superseding the earlier CPT + Loop Grid decision). Accepted cost: the grid, the mega menu and the footer stay hand-duplicated, so adding a service is a three-place edit. The card markup shape is unchanged, so migrating to a `service` CPT later is a swap of the grid's contents, not a redesign. |
| Editor permissions | Role Manager, content-only. Styling stays locked to Global Colors + the master CSS |
| Artifacts | **Two**: the `lenz-core` plugin (CPT, custom widgets, master CSS, icon set, a11y shim) and the kit. No child theme — putting the CSS in the plugin means the design survives a theme switch. |

---

## Do NOT "fix" these

Generic web-redesign instincts will want to change all of the following. Every one is
deliberate, and most have a comment in the source explaining why.

1. **Gold on white text** — never. Gold takes `#121212`.
2. **Orange-500 as body text** — never. It's display and gradients only.
3. **The eyebrow allow-list** — rust is the default, dark surfaces opt in. Don't invert it.
4. **Trust proofs appear exactly once**, in the trust bar. The hero's trust chips and
   media badge were deliberately removed; do not reintroduce them.
5. **The hero subhead is 16px, not 20px.** At 20px it ran nine lines and competed with
   the h1 (`lenz.css:353-355`).
6. **Lead cards are two across, never four.**
7. **"Services" in the nav is a label, not a link.** It has no `href` and must never navigate.
8. **No `aggregateRating` in the JSON-LD** until verified Google data loads. The rating
   is never asserted without a source.
9. **The 44px navbar lock is deliberately relaxed in v4** — block padding was added so
   the bar breathes. That's the v4 spec, not a bug.
10. **Button hover is a `-1px` lift**, not `grow`/`shrink`.
11. **The service area has no map-based city picker** — a flat chip list plus one GBP
    embed. Don't turn it into an interactive map.
12. **`prefers-reduced-motion` blocks** — the marquee freezes to a wrapped grid and the
    skeleton stops animating. Keep them.
