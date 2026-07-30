# KIT-ANALYSIS — Petitt Heating & Cooling

Design-system analysis mined from `projects/petitt/current-theme/` (Elementor kit
export "petitt", v3.0 — 50 pages, 15 posts, 21 templates). This is the *why* behind
`tokens.json`; every Petitt page build reads from it.

Live site: <https://petittheatingandcooling.com>

---

## 1. Verdict on the globals: **REAL — use them**

Unlike the usual Hello-Elementor trap, this kit's `site-settings.json` holds genuine
brand values, and the site's own pages reference them constantly (`globals/colors?id=…`
appears ~3,900 times across the kit). Evidence:

- `system_colors` are branded (`#2B2E81` navy, `#EC2024` red), not `#6EC1E4`.
- `system_typography` = **Montserrat**; the h1–h6 theme styles = **Oswald**, and the kit
  defines a full custom type scale (`title-h1` … `title-h6`, `leading-text`,
  `uppercase-pre-title`) with **mobile sizes already set**.
- 280 widget-level `font_family` values are Montserrat, 7 are Oswald — i.e. widgets rarely
  override the theme; they inherit it.

**Consequence for builds:** reference the global color slots (`__globals__`) the way the
kit's own pages do, and reproduce the theme type scale inline **in `em`, at exactly the
theme's values**, so the repo's responsive gate passes without changing a single rendered
pixel. Do not invent sizes.

## 2. Palette + roles

| Role | Global slot | Hex | Where it earns the role |
|---|---|---|---|
| White | `a23a917` | `#FFFFFF` | 536 hits + 944 global refs — text on dark bands, card fills |
| Navy (Secondary) | `secondary` | `#2B2E81` | 197 hits — hero background, H3 card titles, phone button |
| Red (Accent) | `accent` | `#EC2024` | 132 hits — CTA background, link hover |
| CTA red (inline) | — | `#D90000` | 162 hits — **the actual button background used on pages** |
| CTA red hover | — | `#AF0000` | 164 hits — button hover background |
| Text | `text` | `#171925` | body + all heading colors |
| Soft Gray | `fd5335f` | `#FAFAFA` | 56 hits — the alternating light band + card fill |
| Blue-2 | `bd6963d` | `#191C64` | 30 hits — deep-navy bands, icon-box titles |
| Tint | — | `#F1F2FF` | 48 hits — gradient partner for card fills |
| Glass | — | `#FFFFFFE6` | 49 hits — translucent content card over photo/pattern bands |
| Primary | `primary` | `#47A3DA` | only 6 hits — **decorative accent line only**, not a section color |
| Star gold | — | `#C9D323` | rating-widget star color |

**Gotcha worth repeating:** the slot named `primary` (`#47A3DA` light blue) is *not* the
brand's primary in practice — it's a 2px bottom-border accent. The working primary is
navy `#2B2E81`. Likewise, buttons on real pages use inline `#D90000`, not the
`accent` `#EC2024` stored in the global button setting.

## 3. Type scale (theme styles — reproduce, don't redesign)

Headings: **Oswald, UPPERCASE, letter-spacing −0.02em**, color `#171925` (white on dark).
Body: **Montserrat 400, 16px**, color `#171925`.

| Tag | Desktop | Mobile | Line height |
|---|---|---|---|
| h1 | 3.2em | 2.4em | 1.05 |
| h2 | 2.4em | 2.0em | 1.1 |
| h3 | 1.8em | 1.6em | 1.15 |
| h4 | 1.5em | 1.35em | 1.2 |
| h5 | 1.25em | 1.15em | 1.3 |
| lead text | 1.35em bold | 1.2em | 1.4 |
| body | 16px | — | 1.6 |

There is also an `uppercase-pre-title` slot (bold, uppercase, 0.2em letter-spacing) used
for eyebrows above H2s.

## 4. Button spec (351 buttons analysed)

The dominant CTA (122 identical + 34 near-identical instances):

```
background        #D90000            (inline — NOT the accent global)
hover background  #AF0000
text / hover text #FFFFFF  (hover via globals/colors?id=a23a917)
typography        Montserrat bold, 1.2em, letter-spacing −0.02em
radius            100px  (full pill — from the global button setting)
border            none
padding           15px 25px
box-shadow        0 4 12 rgba(0,0,0,.12)   (global)
icon              fas fa-chevron-circle-right, icon_align: row-reverse
hover animation   NONE — this brand does not use `shrink` or any size animation
```

Secondary/phone variant: same shape, background = `globals/colors?id=secondary` (navy),
icon `fas fa-phone-alt`. Used for the `tel:` button in closing CTAs.

**Do not add a hover animation.** Color-change only is the convention here.

## 5. Section rhythm

Top-level bands across the kit, in frequency order: transparent/white (170),
Soft Gray `#FAFAFA` (80), White (53), photo/pattern background (46), Navy `#2B2E81`
(31 + 18 via the global), Blue-2 `#191C64` (17).

The signature move is a **band + brand pattern overlay**: sections layer
`Petitt_WebSectionDividers-01/02/03.png` as a `background_overlay_image` over a flat
color. Hero uses divider **-03** over navy; light content bands use **-01** over Soft
Gray. Over photo/pattern bands, content sits in a **glass card** (`#FFFFFFE6`, radius 15,
class `is-blurred-background`).

Rhythm used for a service-area page: `navy hero → soft-gray → navy/photo → soft-gray →
white → soft-gray → photo+glass CTA`.

## 6. Structure & layout patterns

The kit uses the Elementor **Container (flexbox/grid)** model throughout — no legacy
sections. Top-level containers are boxed (default 1140px content width; no
`container_width` override in site settings), and a few narrow sections use **980px**
(the FAQ block on the White House cooling page).

Reusable patterns worth cloning, with the page that owns each:

- **Hero** (`4038`, `6619`, `12`): navy band, `css_classes: hero-pages`, rating badge
  (`rating` widget, stars `#C9D323`) + "5.0 (1000+ Reviews)", white H1, white lead text
  (typography global `accent`), CTA button; optional right-hand image at 400px height,
  radius 12.
- **Service card grid** (`6619`): grid container → per-card container
  (`#FAFAFA→#F1F2FF` gradient, radius 15, shadow `0 4 16 rgba(0,0,0,.15)`, padding 15,
  `min_height` 350, class `translate-y-10`) → white rounded image box → H3 (navy,
  centered) → body → red button, centered. **This is the "Card Component Grid".**
- **Icon-box row** (`6619`, `12`): `icon-box`, `position: inline-start`, icon 30px in
  accent red, title h5, description at `.9em` — used for trust/benefit strips.
- **FAQ** (`6619`): `nested-accordion`, `title_tag: h3`, chevron-down/up icons,
  250ms animation, in a 980px container.
- **Closing CTA** (`4038`, `6619`): photo band → glass card `#FFFFFFCF` → H2 + icon-list
  + text → row of two buttons (`tel:` navy + red schedule).
- **Live widgets:** a Google Maps `iframe` in an `html` widget (Petitt's Springfield
  location) and a reviews block. Keep them as-is; don't try to rebuild them.

Widget mix (kit-wide): `text-editor` 1086, `heading` 817, `button` 351, `icon-list` 256,
`image` 196, `icon-box` 181, `nested-accordion` 53, `rating` 51, `html` 9.

## 7. Content voice

Local, plain-spoken, family-business confident — never hypey. Recurring devices:

- **Locality first:** neighborhoods and counties by name ("Tyree Springs, Rolling Acres…
  Robertson and Sumner County"), and "we live and work here" framing against national
  chains ("We aren't a big national chain dispatching trucks from an hour away").
- **Symptom → reassurance → CTA:** name what the homeowner is experiencing, explain the
  fix in one sentence, then a specific CTA ("Explore White House Cooling Services", not
  "Learn more").
- **Proof in numbers:** since 2010, 50+ years combined experience, 1,000+ five-star
  reviews, TN Mechanical license TN-64284, $12/month plan, $500 on-time guarantee,
  10-year warranty, 12-hour priority response ("the Petitt Promise").
- **Second person, contractions, short paragraphs.** Headings are sentence-cased in the
  source and rendered UPPERCASE by the theme — write them in sentence case.
- Avoid: "best in the business", "unbeatable", exclamation stacks, generic filler.

## 8. Kit gotchas

1. Kit `content/page/<id>.json` will **not** import as a single page ("Invalid template
   type"). Wrap as `{version,title,type:"page",content,page_settings}`.
2. `primary` global ≠ the brand primary (see §2).
3. Buttons: inline `#D90000`, no hover animation.
4. Headings inherit theme sizes; a heading with only a global reference **will not shrink
   on mobile** — always emit explicit `typography_font_size_mobile` (the repo gate checks
   this).
5. The kit's own pages nest 4–6 container levels deep for simple content. **Don't copy
   that** — the repo standard is full-width Section → one boxed container → content.
6. Media URLs are absolute `https://petittheatingandcooling.com/wp-content/uploads/…`
   with real attachment IDs — reuse the IDs in `tokens.json` `media` so images resolve
   after import instead of re-uploading.
7. `background_video_link` on the home/White House hero points at a `.mov` — leave it out
   of new builds unless asked.

## 9. Closest page to mirror

| Building… | Mirror |
|---|---|
| a **service-area** page | `content/page/4038.json` (White House) + `6619.json` (its cooling child) |
| a **service** page | `content/page/4564.json` (cooling) / `4668.json` (plumbing) |
| a **city child** page | `6619.json` — newest, cleanest patterns (cards + FAQ) |

`6619` is the most recent build and the best structural reference in the kit.
