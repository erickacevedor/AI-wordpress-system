# Elementor Output Anatomy

**What a finished page from this repo actually looks like, and why.**

Every page in `projects/*/pages/` was built by a different `build.py` for a different
brand, and they still share a skeleton. This file records that skeleton — the part
that does **not** change from project to project — plus the two strategies the repo
has used for the parts that do.

Read this before authoring a new `build.py`, and before deciding how to port a design
that Elementor cannot draw natively.

Companion to [`Elementor-Site-Playbook.md`](./Elementor-Site-Playbook.md) (the
process) and [`Page-Creation-SOP.md`](./Page-Creation-SOP.md) (the per-page loop).
Derived from reading every built page in the repo, 2026-08-26.

---

## 1. The wrapper

```json
{ "version": "0.4", "title": "...", "type": "page",
  "content": [ /* sections */ ],
  "page_settings": { "template": "default", "hide_title": "yes" } }
```

`content` is an array of **sections**. `validate-page.py` errors if `type` is not a
recognised value or `content` is not a non-empty list, and warns on a missing
`title` or `page_settings`.

`page_settings.template` differs by site and is a real decision: `"default"` where
the theme supplies the header/footer, `"elementor_header_footer"` where the Theme
Builder does. Match the site's existing pages rather than picking one.

## 2. The two-layer section — the rule that bites

Every section, without exception:

```
container  content_width:"full"   isInner:false     ← the background lives here
└── container  content_width:"boxed"  isInner:true  ← the padding lives here
        boxed_width: 1140…1280
        padding / padding_mobile
    └── the content
```

`validate-page.py` raises **errors**, not warnings, for:

- a section that is not full-width — *"every section must be full-width"*
- a section holding anything other than **exactly one** boxed content container
- a boxed container nested inside another boxed container

`elementor_builder.section()` emits this pair for you. Building the containers by
hand is the usual way a page fails the gate.

A padded nested layout row/column/grid draws a **warning** (padding belongs on the
boxed container or on a self-contained card, not on a bare layout row).

## 3. Colour: `__globals__`, not hex

Pages tie colours to the site's Elementor **Global Colors** rather than hardcoding
them:

```json
"__globals__": { "background_overlay_color": "globals/colors?id=408e485" }
```

This is what the `"global"` field in each `tokens.json` colour role is for:

```json
"blue": { "global": "globals/colors?id=408e485", "hex": "#0C4096" }
```

A hex is the fallback for surfaces Elementor cannot bind (and for the preview). The
global is what lets the client change a brand colour in the kit and have every page
follow. Observed density in the repo:

| Page | `__globals__` refs |
|---|---|
| magnolia / air-conditioning-services | 49 |
| petitt / white-house | 40 |
| gcreliable / ac-installation | 35 |
| lenz / home | 24 (of 203 widgets) |
| lenz / footer | **0** |

Lenz's numbers are low for a structural reason — see §6.

## 4. Responsive failures are errors

`responsive-audit.py` runs inside the gate and its findings are **errors**. A page
does not ship without all of these:

| Element | Required |
|---|---|
| grid | `grid_columns_grid_tablet` **and** `grid_columns_grid_mobile` |
| flex row | a mobile direction — otherwise it never stacks |
| %-width column | `width_mobile: 100` |
| boxed container | `padding_mobile` |
| heading | a mobile font size — otherwise it never shrinks |
| image with a fixed height | `height_mobile` |
| emoji icon | `typography_font_size_mobile` |

The emoji rule exists because an emoji is a `heading` widget: a 42px icon does not
shrink on its own, and it wrecks a phone layout.

Using `elementor_builder`'s `grid()`, `row()`, `column()` and `heading()` satisfies
these by construction.

## 5. The other hard rules

- **Exactly one H1** per page; **no H1 inside an accordion** (it would nest a page
  heading inside collapsed content).
- **Unique element ids.** Call `E.reset_ids(0x10000000)` at the top of `build.py`.
- **No `display_condition_list`** — display gates hide content on import.
- **Every image widget needs alt text.**
- **Band rhythm is a warning:** two consecutive sections sharing a background get
  flagged. Sites therefore declare an explicit sequence — gcreliable's is
  `gradient → white → #EFF2F5 → white → #EFF2F5 → white → #EFF2F5 → white → gradient → #EFF2F5`.
- **SEO meta is read from `HANDOFF-notes.md`**, and warns over 60 characters. The
  handoff file is an input to the gate, not just prose.

### ⚠️ `.e-con::before` is already Elementor's — write pseudo-elements on `::after`

The moment a site ships any custom CSS (§6 strategy B, or a capped child theme), this
bites. Elementor renders a container's **background overlay** as `.e-con::before`, and
that rule is not passive:

```css
.e-con:before { content: var(--background-overlay); position: absolute;
                top:    calc(0px - var(--border-top-width));
                left:   calc(0px - var(--border-left-width));
                width:  max(100% + …, 100%);
                height: max(100% + …, 100%);
                opacity: var(--overlay-opacity); … }
```

So a decorative layer written the natural way —

```css
.my-card::before { content: ""; position: absolute;
                   bottom: -100px; left: 0; width: 100%; height: 200px; }
```

— is **over-constrained**. `top` from Elementor and `height` from you are both set, so
CSS drops `bottom`, and the layer pins itself to the **top-left** of the element
instead of hanging off the bottom.

It still renders. It looks deliberate. Nothing warns you, and the gate cannot see it,
because the JSON is correct — the defect only exists in the browser. On midlakes it
put four of six watermarks in the wrong place and survived a full build, gate, import
and render-verify before anyone looked at the page.

**`.e-con::after` is untouched by Elementor** (zero matches in `frontend.min.css`), so
put decorative layers there and they compete with nothing. If an element genuinely
needs two, give `::before` the one that sets `top` and `left` explicitly — those
override Elementor's values outright — and set `opacity` explicitly too, so a
background overlay added later cannot drag `--overlay-opacity` into your layer.

> The short version: **on an Elementor container, `::before` is taken. Reach for
> `::after` first.**

## 6. Two porting strategies

The repo has done this two ways. Both are legitimate; they trade different things.

### A. Kit-native — dolan, gcreliable, magnolia, petitt

Everything is a native Elementor widget styled through Elementor's own settings.
41–72 widgets per page, 5–10 sections, depth 4–6. Icons are emoji (as `heading`
widgets) or the kit's Font Awesome. Effectively no `html` widgets.

**Buys:** the page is self-contained, the client can edit it in the Elementor editor,
Global Colors propagate, nothing to deploy or maintain alongside it.
**Costs:** anything Elementor cannot draw is approximated or dropped.

### B. Plugin-skinned — lenz (the HTML-origin site)

Elementor supplies the **skeleton**; a companion plugin supplies the **skin**.

The `html` widgets are not the story. They are 72 widgets totalling **15 KB of a
140 KB page**, averaging 210 bytes, with **zero `<style>` or `<script>`** — 57 of the
72 are just an SVG icon pulled from a sprite:

```html
<span class="lenz-lead-card__icon"><svg class="lenz-icon"><use href="#i-snow"/></svg></span>
```

The real dependency is that **137 *native* elements carry `lenz-*` classes** styled
from outside — 65 containers, 41 text-editors, 17 headings, and **all 11 buttons**.
`plugin/lenz-core/` holds 50 KB of CSS with 224 `.lenz-*` rules, a 24-icon SVG
sprite, header JS, and a custom marquee widget.

**Buys:** near-exact fidelity to the source design; the CSS already existed in the
prototype.
**Costs, all real:**

- Changing a button colour in the Elementor editor **does nothing** — `.lenz-btn`
  wins. Whoever maintains the site later must know this.
- Deactivating the plugin leaves the page structurally intact and visually broken.
- Global Colors mostly stop applying, which is why lenz/home has 24 refs and
  lenz/footer has none.
- The plugin must be deployed from the repo (`deploy-plugin.sh`); editing it inside
  `wp-content/plugins/` and expecting it to persist is the failure that script exists
  to prevent.

### Choosing

Default to **A**. Reach for **B**'s technique — a small `html` widget — only for what
Elementor genuinely cannot draw, which in practice means custom SVG icons. Reach for
a whole companion plugin only when the design's identity depends on effects Elementor
has no control for, and record that decision in `KIT-ANALYSIS.md` with what it costs.

Lenz's own `KIT-ANALYSIS.md` models this well: it has a *"Gradients — the central
translation decision"* section splitting them into *"Native (5 surfaces)"* vs
*"CSS-only (6 rules) — Elementor has no control for these"*, plus a *"Do NOT 'fix'
these"* section.

## 7. Header and footer are not page content

Where a site's header/footer are built in this repo they live as Theme Builder
templates — `projects/<site>/pages/_theme/header.json` and `footer.json` — not inside
a page. Lenz is the worked example.

Any prototype whose pages repeat an identical header and footer (most of them) should
have those lifted out before the page count is estimated.

## 8. What ships per page

```
projects/<site>/pages/<slug>/
├── source.<ext>        ← the brief, as received
├── build.py            ← the reproducible build
├── <slug>.json         ← the deliverable; import this
├── PREVIEW.html        ← flat HTML approximation, for design review only
└── HANDOFF-notes.md    ← see below
```

`HANDOFF-notes.md` is a deliverable, not a README. The ones in the repo declare: the
layout standard applied, the band sequence, every section one by one, the icon
strategy, and an **"After import — wire up"** section naming real media attachment
ids, links to confirm, and the `page_settings` shipped.

## 9. How a `build.py` is shaped

```python
T = json.load(open(os.path.join(SITE, "tokens.json")))
C = {k: v["hex"]    for k, v in T["colors"].items()}   # hex
G = {k: v["global"] for k, v in T["colors"].items()}   # Global Color refs
F, BTN, LINKS, PH = T["fonts"], T["button"], T["links"], T["phone"]

E.reset_ids(0x10000000)

def h2(txt, ...): return E.heading(txt, "h2", font=F["heading"], size=2.2, mobile=1.55, ...)
def band(color):  return {"background_background": "classic", "background_color": color}

S = []
S.append(E.section(band(LIGHTBLUE), [ h2("..."), body("..."), btn("...") ]))
...
doc = E.wrap_page(TITLE, S, {"template": "default", "hide_title": "yes"})
```

Brand values come from `tokens.json`; structural and responsive correctness come from
`elementor_builder`; only the content and the section assembly are page-specific.
Local one-line helpers (`h1`, `h2`, `body`, `btn`, `emoji`, `band`, `overlay`,
`service_card`) keep the assembly readable — every existing `build.py` defines them.

`scripts/elementor_builder.py` exposes: `section`, `row`, `column`, `grid`, `card`,
`heading`, `text`, `button`, `image`, `emoji_icon`, `accordion`, `gradient_bg`,
`wrap_page`, `reset_ids`.

## 10. Rough scale

| Page | Sections | Widgets | Max depth |
|---|---|---|---|
| dolan / cooling-services | 5 | 41 | 4 |
| magnolia / air-conditioning-services | 9 | 69 | 5 |
| petitt / white-house | 10 | 69 | 5 |
| gcreliable / ac-installation | 10 | 67 | 6 |
| lenz / home | 15 | 203 | 5 |

A service page lands around 5–10 sections and 40–70 widgets. A page that needs 200
widgets is either a homepage or a sign that a per-item component should be a grid.

---

## 11. Decisions every HTML→Elementor port must settle

A static prototype contains things WordPress does differently and things Elementor
cannot draw. None of these are discovered by `analyze-prototype.py` — it reads the
design system, not the intent — and each one changes the shape or the cost of the
job. **Settle them before the first `build.py`**, and record the answers in the
site's `KIT-ANALYSIS.md`.

Left implicit, they get decided by accident halfway through page four.

### 11.1 Forms — the one thing that is never a 1:1 port

A prototype's form is markup plus client-side validation and no backend. In
WordPress it becomes a widget or a plugin, and that brings decisions that are
infrastructure, not layout: **which form system** (Elementor Pro Forms, or a plugin
such as WPForms/Fluent Forms), **where submissions go** (email recipient, CRM, both),
**anti-spam**, and **what the success state is** (inline message vs. thank-you page,
which affects conversion tracking).

If the same form repeats on every page, decide once whether it is a saved Elementor
template rather than rebuilt per page.

### 11.2 The blog index is a template, not a page

A prototype's blog page is a static placeholder grid. In WordPress it is an **archive
template** in the Theme Builder driven by real posts — different object, different
build path. Take it out of the page count before estimating.

The same applies to any page whose content is a loop over posts, products, or
testimonials.

### 11.3 Header and footer come out of the page

See §7. Most prototypes repeat an identical header and footer on every page; they
belong in `pages/_theme/`. Deciding this late means porting the same 50 lines six
times and then unpicking it.

### 11.4 Decorative backgrounds and watermarks

Prototypes routinely carry decorative SVG or image layers applied through
`::before`/`::after` on sections and cards. Elementor has no pseudo-element control:
each one becomes a section background image with explicit positioning, or it is
dropped.

Ask three things: **is it part of the brand or is it dressing?**, **does dropping it
change the design's identity?**, and **what compensating spacing exists purely to
make room for it?** — a large `padding-bottom` on a footer usually exists only to
clear a watermark, and porting the padding without the watermark leaves dead space.

Watch for these arriving as a block appended to the end of a stylesheet in a
different hand from the rest (no comments, duplicated declarations). That is a late
addition, and it is worth confirming it is wanted at all before paying to port it.

### 11.5 Effects Elementor has no control for

Every prototype has a handful: a hover `transform`, a `clamp()` fluid type ramp, a
`nth-child` colour alternation, a sticky in-page anchor bar, scroll-reveal
animation.

The choice is per-effect, not per-project:

| | |
|---|---|
| **Native equivalent** | Elementor entrance animations for scroll-reveal; the Accordion widget for a `<details>` list (it already does "only one open"); a Google Maps widget for an embedded iframe |
| **Approximate** | fluid `clamp()` → explicit desktop/tablet/mobile sizes |
| **Restate per widget** | `nth-child` alternation — Elementor has no positional selector, so the colour is set widget by widget. **This must be written down**, or the pattern breaks the first time someone adds a card |
| **A little CSS** | a hover `transform`, a sticky offset — a few lines that Elementor cannot express |
| **Drop** | anything whose absence nobody would notice |

The last two are where the project's shape is decided. **Settle up front whether the
deliverable may carry any custom CSS at all**, because "a few lines" is how §6's
companion plugin starts. If the answer is yes, cap it: name the rules and keep them
in one place.

### 11.6 Icons

A prototype's inline SVGs have no Elementor equivalent. Either map them to the
kit's icon font / emoji (kit-native, §6A), or carry a sprite and reference it from
small `html` widgets (§6B). Mixing is fine and usually right — gcreliable
deliberately mixes emoji and Font Awesome "so the page never depends entirely on the
icon font."

### 11.7 The type scale, when there isn't one

A hand-written prototype often has twenty-plus distinct `font-size` values. That is
drift, not a scale, and Elementor cannot reproduce drift — every heading also needs a
mobile size (§4), so the count doubles. Collapse it to 6–8 steps and **record which
original size became which step**, because every later page depends on that mapping.

> **A worked answer to all seven.** `projects/midlakes/KIT-ANALYSIS.md` settles §11.1
> through §11.7 for a real HTML→Elementor port, with the reasoning in
> `projects/midlakes/PORT-DECISIONS.md`. It also declines §11.7's collapse on purpose:
> when `build.py` emits the sizes programmatically, exactness costs nothing, and the
> collapse is a maintainability trade that a fidelity-first mandate outranks.
