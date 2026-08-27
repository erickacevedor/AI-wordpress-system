---
name: midlakes-page-builder
description: >
  Orchestrates creation of a Mid Lakes Heating & Cooling (Loganville, GA HVAC)
  Elementor page from the HTML prototype or a content brief. Use whenever the user
  says "build the Mid Lakes home page", "port /services/ to Elementor", "make a Mid
  Lakes page from this doc", or hands over copy to turn into an Elementor page. Runs
  the full pipeline: design-read -> read the prototype -> map the anatomy -> build.py
  -> complete JSON -> validate -> preview. Carries the three silent footguns that
  cost this port time.
---

# Mid Lakes Page Builder

The one entry point for turning a prototype page (or a brief) into an import-ready
Mid Lakes Elementor page.

**Input:** the prototype page at `D:\laragon\www\midlakes\public\<page>\index.php`,
or a content doc dropped in `projects/midlakes/pages/<slug>/` as `source.<ext>`.
**Output:** `projects/midlakes/pages/<slug>/<slug>.json` + `build.py` +
`PREVIEW.html` + `HANDOFF-notes.md`, all in that one folder.

```bash
python3 projects/midlakes/pages/<slug>/build.py
python3 scripts/validate-page.py projects/midlakes/pages/<slug>/<slug>.json   # MUST exit 0
python3 scripts/make-preview.py  projects/midlakes/pages/<slug>/<slug>.json
```

Or do the whole site at once — build, gate, deploy the theme, import every part and
page, then verify each against its rendered HTML:

```bash
./projects/midlakes/build-all.sh            # build + gate only
./projects/midlakes/build-all.sh --deploy   # ...and push to the install
```

**Every current warning on this site is one of exactly two known things:** the
deliberate white-on-white band doubles on `/about-us/` and `/service-agreements/`, and
the prototype's own SEO strings running past 60/155 characters. A warning that is not
one of those two is a real finding.

## ⚠️ The four silent footguns

Each one produces **wrong output with no error anywhere**. All three were verified on
this install (Elementor 4.2.3) by importing a real page and reading the generated CSS.

1. **The button background key is `background_color`, NOT
   `button_background_color`.** A wrong key name does not error — it falls through to
   `var(--e-global-color-accent)`, which on this stock kit is Hello Elementor's
   default. The button renders off-brand with no warning. With the correct key it
   emits `background-color:#c10a0a` exactly.
2. **`heading(size=2.4)` defaults to `unit="px"`.** A heading meant to be `2.4rem`
   renders at 2.4 *pixels*. **Pass `unit="rem"` explicitly** on every heading, every
   time.
3. **`typography_font_size_mobile` alone emits no CSS.** Elementor only writes a
   typography group when `typography_typography: "custom"` is present. `_typo()` sets
   it when `font` **or** `size` is given — and the `h1`/`h2` recipe gives *neither*.
   `responsive-audit.py` still passes, because it only checks the key exists. Pass
   `extra={"typography_typography": "custom"}`.
4. **`.e-con::before` is already Elementor's** — it renders the container background
   overlay, and it sets `top`, `left`, `width`, `height` and `opacity`. A CSS layer
   anchored with `bottom`/`right` and no `top`/`left` is over-constrained, Elementor's
   `top` wins, and the layer silently pins itself to the top-left corner. It renders,
   it looks deliberate, and nothing warns you. **Use `::after`** — Elementor does not
   touch it. This is why every watermark and both photo overlays in `mid-lakes.css`
   are `::after`.

## The h1/h2 recipe

The child theme owns `h1`/`h2` **font-size** via `clamp()` (the CSS cap — Elementor
has three fixed breakpoints and cannot do continuous fluid scaling). But
`responsive-audit.py` makes a missing `typography_font_size_mobile` on any `h1`/`h2`
an **error**, unconditionally.

Both are satisfied by emitting the **mobile size only**, set to the clamp's floor:

```python
def h1(title, color=None):
    return E.heading(title, tag="h1", color=color,
                     size=None, mobile=2.4, unit="rem",          # 2.4rem = the clamp floor
                     weight="800", lh=1.1, ls=-0.02,
                     extra={"typography_typography": "custom"})  # footgun 3

def h2(title, color=None):
    return E.heading(title, tag="h2", color=color,
                     size=None, mobile=1.8, unit="rem",
                     weight="800", lh=1.1, ls=-0.02,
                     extra={"typography_typography": "custom"})
```

No desktop size, no tablet size. Above 767px the child theme's `clamp()` is unopposed
and scales fluidly; below it Elementor writes the floor. `h2`'s floor is **exact**
below 767px (`3.4vw` only exceeds `1.8rem` above an 847px viewport); `h1`'s is within
1.5px at the very top of the mobile range.

**Every other heading** takes a real desktop `size` in `unit="rem"` and lets
`heading()` auto-derive its mobile step.

## One owner per property

Elementor's per-element rule is **four classes (0,4,0)**:

```css
.elementor-32 .elementor-element.elementor-element-200026ae .elementor-button { … }
```

A bare class like `.ml-btn .elementor-button` is **(0,2,0)**. **Elementor always
wins.** Do not fight it with `!important`:

- **Child theme owns it** → **omit it from `build.py`.** Elementor then generates no
  rule and the class applies at natural specificity.
- **Elementor owns it** → set it in `build.py`, write no CSS for it.

Every rule in the CSS cap is a property Elementor never sets — `transform`,
`transition`, pseudo-elements, `clamp()`, the rate table's stacking. Zero competition.

### Where a CSS class lands

`build.py` emits `_css_classes` for widgets and `css_classes` for containers (the same
field as Advanced → CSS Classes).

```html
<div class="elementor-element … ml-band e-con e-parent">            <!-- container: on the element -->
  <div class="elementor-element … ml-box e-con-boxed">              <!-- boxed container -->
    <div class="elementor-element … ml-btn elementor-widget-button"><!-- widget WRAPPER -->
      <a class="elementor-button elementor-button-link">            <!-- the actual button -->
```

```css
.ml-btn .elementor-button:hover { transform: translateY(-2px); }   /* correct */
.ml-btn:hover { transform: translateY(-2px); }                     /* wrong — moves the wrapper */
```

## Pipeline (run in order)

1. **Design read** — apply `midlakes-design-read`. Name the page kind, open the
   prototype file, state the one-line read, note the page's band order **including its
   deliberate double** if it has one.
2. **Read the source.** For an existing page: the prototype `index.php` section by
   section, plus each class's rules in `styles.css`. For a new page from a doc:
   extract to `source.txt` beside `build.py`, watching for mojibake (curly quotes
   arriving as `?`/`�` — restore them as `&rsquo;`/`&mdash;`).
3. **Map to the page anatomy.** Reproduce the prototype's section order exactly. For
   a *new* page, borrow the closest existing page's anatomy rather than inventing one.

   | Page | Band order |
   |---|---|
   | `/` | hero · white · paper · comfort · white · paper · ink |
   | `/about-us/` | hero · white · paper · white · **white** · comfort · paper · white · ink |
   | `/services/` | hero · section-nav · white · paper · white · comfort · paper · white · ink |
   | `/service-agreements/` | hero · white · paper · white · **white** · paper · ink |
   | `/service-area/` | hero · white · paper · white · paper · ink |
   | `/financing/` | hero · white · paper · white · paper · white · paper · white · ink · paper(legal) |

   The bolded doubles are deliberate. **Do not alternate them "properly".**
4. **Copy.** For the six existing pages, use the prototype's copy **verbatim**,
   entities and all. Anything new goes through `midlakes-content-style`.
5. **Style to the system** — apply `midlakes-ui-design`. Build through
   `scripts/elementor_builder.py` from a `pages/<slug>/build.py` that reads
   `../../tokens.json`, so the page is reproducible and the responsive gates are baked
   in. Brand-styled thin wrappers go at the top of `build.py` (see below).
6. **Emit complete JSON** — apply `full-output-enforcement`. Unique ids
   (`E.reset_ids(seed)` with a distinct seed per page), all required keys, valid
   escaping, UTF-8, single-page wrapper with
   `page_settings = {"template":"elementor_header_footer","hide_title":"yes"}`.
   **No `display_condition_list`.**
7. **SEO, links & media** — one H1 + clean hierarchy; root-relative internal links
   with descriptive anchors; the slug, meta title and meta description **from
   `tokens.json → pages.seo`** recorded in `HANDOFF-notes.md`; every image carries the
   prototype's alt text verbatim; flag every image as a post-import swap until
   `media.json` exists.
8. **Validate (required gate)** — `python3 scripts/validate-page.py <page>.json` must
   exit **0**, then apply `midlakes-page-audit`, then generate `PREVIEW.html`.

## The `build.py` wrapper set — already written

**`projects/midlakes/brand.py` is the vocabulary.** It reads `tokens.json` and
`media.json`, implements every component in `midlakes-ui-design`, restates all three
alternations, and handles all three footguns. A page `build.py` supplies **copy and
section order, and nothing else**:

```python
import brand as B
B.reset(0x4N000000)          # a seed distinct from every other Mid Lakes page
SECTIONS = [B.hero(...), B.sec_about([...]), B.sec_paper([...]), B.contact(...)]
B.write(B.page("Title", SECTIONS), "<slug>.json", HERE)
```

⚠️ **`sec_about()` vs `sec_why()`.** Both are white bands. `sec_about()` carries the
mirrored wave pair; `sec_why()` does not, because in the prototype `.why`'s decoration
lives on its cards. Reaching for a generic "white band" helper is how a page picks up
watermarks it should not have.

What is in there:

| Helper | What it gives you |
|---|---|
| `h1` / `h2` | the clamp recipe above, footgun 3 handled |
| `h(text, step)` | any other heading, sized from the type census by the component that owns the size |
| `body(html, step)` / `lead(html)` | text at a named step, `unit="rem"` always |
| `eyebrow(label, light=False)` | the 7px red dot span + 0.72rem/700/`0.18em`/uppercase |
| `btn_primary` / `btn_ghost` / `actions([...])` | the pill spec, `background_color`, `ml-btn`, no `hover_animation` |
| `sec_about` / `sec_why` / `sec_paper` / `sec(DARK, …)` | the four bands, watermarks attached correctly |
| `hero` / `hero_compact` / `comfort` | the photo bands, `z_index: 1` on the copy |
| `service_card(i, icon, …)` | **restates the red/blue tile alternation from `i`** |
| `why_card(n, …)` / `steps([...])` | **restate the odd/even numeral colour** |
| `spec_card(label, items, blue=False)` | the label + the `fas fa-check-circle` list |
| `detail_row(i, anchor, …, flip=False)` | 1.15fr/1fr, the top hairline, **and the first-row exception** |
| `stats` / `promise` / `chips` / `area_list` | the list components, last-child rules included |
| `faq(items, first_open=False)` | the nested-accordion, `max_items_expended: one` |
| `figure` / `gallery` | the aspect-ratio photos and the gradient caption |
| `contact` / `quote_form` / `contact_details` | the ink band and the shared Pro Form |
| `rate_table` / `gmap` / `section_nav` / `legal` | the one-off components |
| `header_bar` / `footer_bar` / `logo` / `nav_menu` | the two theme parts |

**Containers take `margin` / `padding`; widgets take `_margin` / `_padding`.** Mixing
them up fails silently. And padding on a bare, unbordered layout container trips the
gate's padding-discipline check — use `margin` there (see `detail_row`'s first row and
`area_list`'s last row for the pattern).

### Escape hatches `elementor_builder.py` does not cover

- **The rate table** — one `html` widget carrying the prototype's `<table>` verbatim,
  styled by the cap's `.ml-rate-table`. `elementor_builder` has no table primitive and
  the `<620px` stacking is pure CSS.
- **The service icons** — small `html` widgets referencing the child theme's inline
  SVG sprite (`assets/icons.svg`), not `icon` widgets.
- **The eyebrow dot** — an inline-styled `<span>` inside the text widget's HTML, not a
  separate widget.
- **The 3-stop photo overlays** — see `midlakes-ui-design`; pending the cap decision.
- **The quote form** — an Elementor **Pro Form**, built **once** as a saved template
  and referenced, not rebuilt per page.

## Deliverable & handoff

Tell the user: Elementor → Templates → Import Templates → upload the JSON → open the
imported page → publish at the target slug. `scripts/import-page.php` is **idempotent
by slug**, so a build updates the existing stub (pages 10–16) in place rather than
creating a duplicate — do not renumber them.

List post-import wiring in `HANDOFF-notes.md`: the child theme active, the SEO meta +
slug (no SEO plugin is installed yet), header/footer template assignment, image
uploads + `media.json`, the form template's recipient, and any watermark the client
needs to nudge by hand.

## Guardrails

- **Match the prototype; do not redesign it.** Fidelity beats editability — that was
  the client's explicit choice.
- **Style inline. Never a global colour slot** — the kit is stock Hello.
- **One owner per property** — child theme *or* Elementor, never both. No
  `!important`.
- Root-relative internal links; the contact target is `#contact`, and there is no
  `/contact` page.
- Emit complete JSON — no elisions, no "the rest follows the same pattern."
- `validate-page.py` exit 0 is **not optional**. Warnings are real findings; only
  errors block.
- **The install is a deployment target.** Anything hand-edited there is lost on the
  next import and invisible to git. Changes belong in this repo, then get deployed.
- Verify against the preview and a **local throwaway** WordPress (`scripts/sandbox.sh`)
  — never against a client's live site.
