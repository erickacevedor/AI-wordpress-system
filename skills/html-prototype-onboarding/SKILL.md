---
name: html-prototype-onboarding
description: >
  Portable meta-skill. Onboard a site that has NO Elementor kit — an HTML/CSS
  prototype, a static design repo, a tokens.css — and generate that site's
  page-building skill set. Use when pointed at a design-source folder or an HTML
  prototype, or asked to "onboard this HTML site", "there's no kit, only the
  design", "turn this prototype into Elementor pages", or "do what we did for
  Lenz". Produces projects/<site>/tokens.json, KIT-ANALYSIS.md and the five
  site-specific <site>-* skills, then verifies them. Site-agnostic.
---

# HTML Prototype Onboarding (meta-skill)

The kit-less sibling of `elementor-kit-onboarding`. Same job, same outputs, different
source: where that one mines an Elementor export, this one reads a static HTML/CSS
design.

**Use this only when there is no `current-theme/`.** If the site has an exported kit,
use `elementor-kit-onboarding` — it reads what the site actually does in Elementor,
which is always better evidence than a prototype's intent.

> **Why this skill exists.** `projects/lenz/` was onboarded from HTML by hand, the
> skill-generation step got skipped as "not applicable", and it became the only site
> in the repo with no `<site>-*` skills — so there is no recorded voice for its next
> page to build from, and its brand vocabulary ended up inline in an 871-line
> `build.py`. That is the failure this skill prevents.

## Inputs & output

- **Input:** a prototype at `projects/<site>/design-source/` — `.css` (ideally a
  `tokens.css` of custom properties) plus `.html` pages. A design repo living outside
  this repo works too; copy or reference it in, and record where it came from.
- **Output (all SITE-WIDE, at `projects/<site>/`):**
  (a) `tokens.json` — the seam the whole Elementor pipeline consumes;
  (b) `KIT-ANALYSIS.md` — the design-system analysis and the *why*;
  (c) the five skills in `skills/`: `<site>-design-read`, `-ui-design`,
  `-content-style`, `-page-builder`, `-page-audit`;
  then a verification report.

The portable `full-output-enforcement` stays at repo-root `skills/` — referenced,
never copied per site. Pages are built later, each into its own
`projects/<site>/pages/<page-slug>/`.

**Required once per site, before any page is built.**

## Procedure

### 1. Run the counting first

```bash
python3 scripts/analyze-prototype.py projects/<site>/design-source
```

It reports colour ramps, semantic roles (resolving `var()` chains to the hex that
actually lands), the type scale, spacing, radii, fonts, breakpoints, and a contrast
score for every role against white and near-black. Do not re-derive any of that by
hand — it is deterministic, and doing it twice gives two answers.

### 2. Derive the seam

```bash
python3 scripts/analyze-prototype.py projects/<site>/design-source \
        --emit-tokens projects/<site>/tokens.json
```

It refuses to overwrite an existing `tokens.json`; emit elsewhere and merge if the
site already has one.

The script reads two layers — the custom properties AND the rules — so it fills more
than a palette. From the rules it derives the **button spec** (`.btn` / `.btn-primary`
/ `:hover`: fill, hover fill, text, radius, padding, weight, and whether the hover is
an animation), the **background bands** (only classes the markup puts on a
`<section>`, so components with a background are not mistaken for bands), the **font
families** actually assigned to `body` and the headings, and the **section rhythm**.
It then self-checks the file it wrote against `site_tokens.py` and says whether the
seam is fully readable.

Then **fill what remains** — the values a stylesheet genuinely cannot contain:

- **`links`** — root-relative internal targets (`/contact`, `/services/...`). A
  prototype's hrefs are frequently placeholders; confirm against the sitemap the
  client actually intends.
- **`phone`** — display form and `tel:` form.
- **`_roles`** — the script emits this scaffold pre-filled with what `site_tokens.py`
  *would infer from the key names*, which on a hand-written prototype is routinely
  wrong (a key called `blue` gets called the brand primary when the brand's primary
  is the red). **Verify every line of it.** This is the one block where leaving the
  generated value in place produces a confidently wrong answer rather than a hole.
- **`button`** — now derived, not blank. Any field still reading `TODO` is one the
  CSS does not state. **Verify the derived ones** against the prototype in a browser:
  the script reads the base and primary rules, and a prototype with an unusual
  cascade can land elsewhere.
- **`content_width`** — inferred from `--container` / `--max-width`, in that order,
  with the source recorded in `_content_width_from`; falls back to 1140. **Check it.**
  A prototype built at 1800px will not look like an Elementor/Hello site boxed at
  1140px, and this is the cheapest moment to reconcile that.
- **`type_scale` / `spacing`** — when the prototype declares no `--text-*` or
  `--space-*` tokens, these are back-filled from the rules and marked with a `_from`
  key. A back-filled scale is a starting point, not a finding: see below.

### 3. Judge what the counting cannot

The script counts; these are decisions:

- **Which ramp is the brand primary**, and which is secondary/accent. Frequency does
  not decide this — a neutral ramp always has more steps in use than the brand.
- **Which role is the CTA.** Look for the colour on buttons, not the most common one.
- **Is a role's contrast usable?** The report scores every role. A brand colour that
  fails AA on white is not a bug to fix silently — record it in `KIT-ANALYSIS.md`
  with the rule the design uses to work around it (large text only, dark background
  only, etc.).
- **What the voice is.** Sample real copy from the prototype's HTML: headings,
  body paragraphs, CTA labels. Characterise tone, locality framing, formatting, and
  the recurring copy patterns (hero intro, problem → reassurance → CTA, closing CTA,
  FAQ intro). Note hype words to avoid.
- **The section rhythm.** The script reports the bands and their vertical padding;
  the judgement is the *order* — which backgrounds alternate, in what sequence, and
  where the full-bleed bands fall. Read the page templates for that.
- **Whether the type scale is a scale at all.** The report prints a census of every
  `font-size` in use with its frequency. A hand-written prototype routinely has
  twenty-plus distinct sizes — that is drift, not a scale, and Elementor cannot
  reproduce drift. Collapse it to a real scale and **record the mapping in
  `KIT-ANALYSIS.md`**, because every later page depends on which size became which
  step.

### 4. Read the components, not just the tokens

A prototype's real value over a bare palette is that it shows the **component
vocabulary**: hero, trust bar, service card, CTA band, value props, review card,
FAQ accordion, closing form. Inventory them — this is what `<site>-ui-design` must
describe and what a later `brand.py` will implement.

For each, record: the structure, which tokens it uses, and **whether Elementor can
express it natively**. That last one matters more than it looks:

- Expressible natively (a flat or two-stop-gradient background, a bordered card, a
  flex row) → the builder emits it, and it stays editable in the Elementor UI.
- Not expressible (three-plus-stop gradients, `background-clip:text`, mask images,
  pseudo-element overlays) → it needs a CSS class plus a stylesheet shipped with the
  site. Say so in `<site>-ui-design`, and note that the class approach makes that
  element's background **invisible to `contrast-audit.py`**, so its contrast has to
  be verified by hand once.

`projects/lenz/plugin/lenz-core/` is the worked example of the stylesheet-plus-sprite
pattern: master CSS, an inline 24-symbol SVG icon sprite, and a custom widget.

### 5. Generate the five skills

Identical in shape to what `elementor-kit-onboarding` produces — see that skill for
the full contents of each. Everything there applies, with these differences:

- **`<site>-design-read`** — the reference is a prototype **page template**, not a
  kit page. Name the specific file (`design-source/index.html`) the way a kit-based
  read names `content/page/<id>.json`.
- **`<site>-ui-design`** — record which components need CSS classes (step 4) and
  where that stylesheet lives.
- **`<site>-page-audit`** — the "do NOT fix" list should carry the design's
  deliberate contrast decisions from step 3, so a later reviewer does not
  "correct" a brand colour the designer chose knowingly.

### 6. Verify (do not skip)

- Palette / fonts / type scale / button spec match the rendered prototype — open it
  in a browser and compare, do not trust the stylesheet alone.
- `content_width` is the value the Elementor build should actually use.
- Voice matches 2–3 real pages of prototype copy.
- `tokens.json` reads cleanly through the pipeline:
  ```bash
  python3 -c "import sys;sys.path.insert(0,'scripts');import site_tokens as ST;\
  t=ST.load('projects/<site>');print(t.missing_core() or 'readable')"
  ```
  Anything it lists as missing means downstream tooling cannot read that role.
- Every generated `SKILL.md` has valid frontmatter and correct `<site>` naming.

Fix the skills, not future output, if anything is off.

## Bake in these Elementor gotchas

The prototype is HTML; the deliverable is Elementor. Every generated skill set must
carry the same hard-won rules as the kit path:

- Single-page import wrapper `{version,title,type:"page",content,page_settings}`.
- Unique element ids; complete, valid, UTF-8 JSON — no elisions.
- Full-width Section → **one boxed content container** at the site's content width →
  content, with no excess wrapper around a lone widget.
- Grids stack (tablet ~2 / mobile 1); flex rows stack on mobile; %-width columns go
  100%; H1 and every H2 carry mobile sizes; boxed containers carry `padding_mobile`;
  fixed-height images carry `height_mobile`.
- Mix **emoji-as-icons** with native icons so a page never depends entirely on an
  icon font — and if the prototype uses an icon library, ship it as an inline SVG
  sprite rather than a CDN link.
- **Accessibility rules the validator does not check**, so they must live in the
  generated skills: heading levels never skip (H1 → H2 → H3 — change the size, not
  the level); every CTA has a visible descriptive label, never icon-only; nothing
  auto-plays; a form field gets a real label rather than a placeholder standing in for
  one; every page records a canonical URL in its handoff note.

> **One rule inverts on the way from prototype to Elementor.** A prototype is told to
> reference CSS variables and never hardcode a hex. In Elementor the opposite holds:
> style **inline**, because a kit's Global Colors are frequently still Hello Elementor
> defaults, so pointing a widget at a global slot silently produces off-brand output.
> Keep the variables in the prototype's stylesheet; resolve them to real values in
> `tokens.json`, and let the builder write those values into the page.
- Root-relative internal links. Never emit `display_condition_list`.

Header and footer become Elementor **library templates** built the same way, under
`pages/_theme/`; they validate as `type:"header"` / `"footer"`, which the gate treats
as pages that must *not* contain an H1.

## Guardrails

- Never hard-code a prior site's values — read them fresh from this prototype.
- A prototype is *intent*; a kit is *evidence*. Where both exist, the kit wins.
- If the prototype is missing pieces (no stylesheet, no page templates, tokens only),
  report that rather than inventing a design system.
- If a brand-critical fact is missing (the CTA target, the phone number, the real
  service URLs), ask one focused question rather than guessing.
