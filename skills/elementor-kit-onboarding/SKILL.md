---
name: elementor-kit-onboarding
description: >
  Portable meta-skill. Onboard ANY Elementor site export and generate that site's
  page-building skill set. Use when pointed at a new/unfamiliar Elementor kit
  folder, or asked to "analyze this site", "set up skills for this website",
  "onboard this Elementor export", or "do the same we did for VitalAir on another
  site". Produces site-specific <site>-ui-design, -content-style, -page-builder,
  -page-audit, -design-read skills, then verifies them. Site-agnostic.
---

# Elementor Kit Onboarding (meta-skill)

Turns a raw Elementor export into a working, site-specific page-building skill set.
This skill is **portable and site-agnostic** — it reads whatever kit it's pointed
at and generates the per-site skills. It does not hard-code any brand.

Pairs with `Elementor-Site-Playbook.md` (the human process). This skill automates
its Steps 2–3.

## Inputs & output

- **Input:** an unzipped Elementor kit export folder (`manifest.json`,
  `site-settings.json`, `content/page/*.json`, `content/post/*.json`,
  `templates/*.json`).
- **Output:** a `skills/` folder with `<site>-ui-design`, `<site>-content-style`,
  `<site>-page-audit`, `<site>-page-builder`, `<site>-design-read`, plus the
  portable `output-enforcement` copied in — then a verification report.

Use a short site slug (from `manifest.json` `site`/`title`) as `<site>`.

## Procedure

### 1. Extract the real design system (from widgets, not globals)
`site-settings.json` is frequently still Hello Elementor defaults — do not trust
it. Mine the actual inline styling:

- **Palette:** rank hex colors across `content/page` + `templates`
  (`grep -rhoE '#[0-9A-Fa-f]{6}'` → sort | uniq -c). Assign roles from where they
  appear: header/hero background = dark/brand; footer = secondary; button bg =
  CTA; frequent light tints = alternating section backgrounds.
- **Fonts:** rank `font_family` values → the real brand font(s).
- **Type scale:** distribution of heading `typography_font_size` → map to
  eyebrow / body / h3 / h2 / h1 bands; note eyebrow treatment (uppercase,
  letter-spacing, color).
- **Buttons:** pull a representative button's settings → CTA spec (text/bg color,
  hover color, `border_radius`, `text_padding`, weight, `hover_animation`).
- **Section rhythm:** list top-level section `background_color` sequences across
  pages → the alternating pattern.
- **Structure:** detect whether sections use the Container model and whether they
  follow an outer-Section → inner-Content-Container pattern; note padding placement
  and the content-container width. **Read the kit's content width** (the theme's
  boxed content width, ~1140px on a default Elementor/Hello theme) and use it.
  **Standard to enforce when building:** every section = full-width (100%) Section
  (background only) → **one BOXED content container** set to that site content width
  (`content_width:"boxed"`, `boxed_width` = the kit width, never exceed ~1300px) →
  content widgets directly, with no excess wrapper around a lone image/text and a
  variety of layouts (two-column, card grid, accordion).
- **Icons:** note the icon libraries in use, but the build standard is to **mix in
  emoji as icons** (card headers, benefit lists, step markers) so pages aren't fully
  dependent on the Elementor/FontAwesome/Spectre icon fonts. Emoji go in heading/text
  widgets; save JSON as UTF-8.
- **Reusable templates:** read `templates/*` → header/footer/section IDs + names.
- **Widget mix:** rank `widgetType` → which widgets the site actually uses.

### 2. Extract the content voice
Sample real copy: headings (`"title":`), body (`"editor":`), and button `"text":`
values across pages. Characterize tone, locality/topic framing, formatting
(eyebrow casing, heading case), second/first person, and recurring copy patterns
(hero intro, symptom→reassurance→CTA, closing CTA, FAQ intro). Note any hype words
to avoid.

### 3. Generate the site skills
Write each as `skills/<site>-<name>/SKILL.md` with proper frontmatter
(`name`, `description` with trigger phrases). Model them on the VitalAir set:

- **`<site>-ui-design`** — palette + roles, type scale, button spec (incl. hover
  rule), **section-structure rule**, **mobile/responsive rule**, layout, reusable
  template IDs, review checklist. Flag "style inline, not via global slots."
- **`<site>-content-style`** — voice, formatting conventions, reusable copy
  patterns pulled from real pages, CTA phrasings, do/don't, name usage.
- **SEO + linking + media coverage (all generated skills):** the generated
  `ui-design` gets image/media-placement guidance; `page-audit` gets SEO element
  checks (one H1 + heading hierarchy, meta title < 60, meta description < 155,
  clean slug, keyword in H1/intro), internal-linking requirements (descriptive
  anchors, no dead links), and media/alt-text checks; `page-builder` folds all of
  these into its pipeline plus a publish-time SEO handoff note.
- **Posts as well as pages:** the same system covers blog posts — the generated
  skills should reference the site's single-post template and note post extras
  (featured image, categories/tags, author) at publish time.
- **`<site>-page-audit`** — brand + Elementor-hygiene checks AND a "do NOT fix"
  list of intentional brand choices (so generic web-redesign rules don't fight
  the brand). Include the **responsive checklist**: grids set tablet(~2)/mobile(1)
  columns; flex rows set `flex_direction_mobile:column`; %-width columns set
  `width_mobile:100%`; H1 + every section H2 have `typography_font_size_mobile`
  (globals-only headings don't shrink); boxed container has `padding_mobile`;
  fixed-height images have `height_mobile`. Audit these in the JSON before import
  (see `docs/Publishing-QA-Checklist.md` §5).
- **`<site>-page-builder`** — orchestrator: design-read → map sections → write
  copy → style inline → emit complete JSON → audit → export.
- **`<site>-design-read`** — brief-inference front door that routes to the above.
- **`output-enforcement`** — copy the portable skill in unchanged.

### 4. Verify (do not skip)
Produce a short report and confirm before any page is built:

- Palette / font / type scale / button spec match the live site (spot-check).
- Section-structure + mobile rules captured correctly.
- Voice matches 2–3 real pages.
- Every generated SKILL.md has valid frontmatter and correct `<site>` naming.

Fix the skills, not future output, if anything is off. For high-stakes sites, run
this verification with a subagent.

## Bake in these Elementor gotchas
Every generated skill set must encode: globals are often fake (style inline);
single-page import needs the `{version,title,type:"page",content,page_settings}`
wrapper (kit `content/page` format throws "Invalid template type"); unique ids
(regenerate on clone); complete/valid JSON only; the **full-width Section → one
boxed content container (at the site's content width, ~1140px) → content, no excess
wrappers** layout standard; **emoji-as-icons** mixed in so pages don't fully depend
on icon fonts; plus whatever the site's own section-rhythm, button-hover, and mobile
conventions are.

## Guardrails
- Never hard-code VitalAir (or any prior site's) values — read them fresh each time.
- Match the kit; don't redesign it during onboarding.
- If the export is missing pieces (no templates, empty pages), report it rather
  than inventing a design system.
