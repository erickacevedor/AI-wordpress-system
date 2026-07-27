# Elementor Site → Skills → Page: Reusable Playbook

A repeatable process for onboarding **any** Elementor website and building new
pages on-brand from a content doc. Run it once per site. This is the portable
layer — it never changes site to site; it *generates* the site-specific skills.

Use this file as your **Claude Code `CLAUDE.md`** (drop it at the root of each
site's folder) or paste it as **Claude Project instructions**. Recommended home:
Claude Code / Cowork, because the workflow reads a kit folder, writes skill files,
and emits JSON — a plain claude.ai Project can't do those.

---

## Folder convention (one per site)

Portable skills live once at the repo root (`skills/elementor-kit-onboarding`,
`skills/full-output-enforcement`). Everything site-specific lives under
`projects/<site>/`:

```
projects/<site>/
├── current-theme/           ← the unzipped Elementor kit export
│   ├── manifest.json        ← index of everything
│   ├── site-settings.json   ← global colors/fonts (REAL on some kits, theme defaults on others)
│   ├── content/page/*.json  ← pages   · content/post/*.json ← posts
│   └── templates/*.json     ← header, footer, reusable containers
├── new-content/             ← the source doc/brief for the new page(s)
├── skills/                  ← GENERATED per-site skills (by onboarding — not hand-written)
│   └── <site>-{design-read,ui-design,content-style,page-builder,page-audit}/
└── output/                  ← built page JSON + PREVIEW.html + HANDOFF-notes.md
```

**Skills first, every new site.** Reading `current-theme/` and *generating* the
`<site>-*` skills is a required step, once per site, **before** any page is built.
Never build a page by an ad-hoc read of the kit — build only *through* the generated
skills. (Reuse existing `projects/<site>/skills/`; regenerate only if the kit
changed.) The portable `full-output-enforcement` is referenced from repo-root
`skills/` — it is not copied per site.

---

## The 5-step process

### Step 1 — Export & load the Elementor kit
In WordPress: **Elementor → Tools → Export Kit** (include content + templates +
site settings). Unzip into `projects/<site>/current-theme/`, put the new page's
source doc in `projects/<site>/new-content/`, and point Claude at the repo.

### Step 2 — Analyze the kit & generate the site skills
Run the `elementor-kit-onboarding` skill (or follow it manually). It:

1. **Extracts the real design system** — not from `site-settings.json` (which is
   frequently still the Hello Elementor defaults: `#6EC1E4`, "Noto Sans Coptic"),
   but from the **actual inline widget styling** across pages/templates:
   - Most-used hex colors → brand palette + roles (hero/dark, light bands, CTA).
   - Most-used `font_family` → real brand font.
   - Heading `font_size` distribution → the type scale (eyebrow / body / h3 / h2 / h1).
   - Button settings → CTA spec (bg, hover, radius, padding, weight).
   - Section background sequence → the section rhythm.
   - `templates/` → reusable header/footer/section IDs to reuse.
   - Widget-type frequency → which widgets the site actually uses.
2. **Extracts the content voice** — sample real headings, body paragraphs, and
   CTA labels; characterize tone, locality, formatting, recurring copy patterns.
3. **Generates the site-specific skills** (mirror the VitalAir set):
   - `<site>-ui-design` — palette, type scale, button spec, **section structure
     rule**, layout, reusable templates, review checklist.
   - `<site>-content-style` — voice, formatting, reusable copy patterns, do/don't.
   - `<site>-page-audit` — brand + Elementor-hygiene audit with a "do NOT fix"
     list of intentional brand choices.
   - `<site>-page-builder` — orchestrator that runs the pipeline.
   - `<site>-design-read` — brief-inference front door.
   - (The portable `full-output-enforcement` stays at repo-root `skills/` and is
     referenced during builds — it is **not** copied per site.)

   Write these to `projects/<site>/skills/<site>-<name>/SKILL.md`.

### Step 3 — Double-check (verification gate)
Before building anything, confirm the generated skills are right:

- Palette/font/type-scale/button spec match what you see on the live site.
- The section-structure and mobile rules are present (see "Gotchas" below).
- Spot-check the voice against 2–3 real pages.
- Fix the skills, not the output, if anything's off. Do not proceed until this
  passes. (For high-stakes sites, run this check with a subagent.)

### Step 4 — Request the content doc
Ask the user for the page's content (a doc, brief, or paste). Provide the
`content-brief-template.md` so they can fill: page type, location/topic, hero,
sections, FAQ, CTA. Blanks get inferred from the closest existing page.

### Step 5 — Build the page from content + site context
Run `<site>-page-builder`:
1. **Design read** — page kind + closest existing page/template to mirror.
2. **Map content** to the site's standard section anatomy.
3. **Write/polish copy** with `<site>-content-style`.
4. **Style** with `<site>-ui-design` (inline, on-brand).
5. **Emit complete JSON** with `full-output-enforcement`.
6. **Audit** with `<site>-page-audit`.
7. **Export** an importable single-template file (see format below) + optionally
   register in `manifest.json` for full-kit import.

---

## Publishing & QA (before the page goes live)

After the build, run the pre-publish QA checklist (see
`docs/Publishing-QA-Checklist.md`): brand + structure, SEO elements (one H1, meta
title/description, slug, keyword), required internal links with good anchor text,
images have alt text, live-widget placeholders noted, mobile view checked, and all
links resolve. Then import, set the WP SEO meta (Rank Math / Yoast), assign
header/footer, set the featured image, publish, and test the live URL.

## Posts as well as pages

The same process applies to blog posts. Use the site's single-post template as the
base, set the content brief's page type to "post," and remember post-specific
extras at publish: featured image, category/tags, author, and SEO meta.

## Elementor gotchas (bake these into every site's skills)

These are the lessons that make the difference between "imports and looks right"
and "broken." Encode them in the generated `<site>-ui-design` and `-page-audit`.

1. **Globals are usually fake.** `site-settings.json` often still holds Hello
   Elementor defaults. Read styling from the widgets and apply colors/fonts
   **inline**, never via global slots.
2. **Single-page import needs a template wrapper.** The `content/page/<id>.json`
   kit format throws **"Invalid template type"** in the Import Templates dialog.
   For single-page import, wrap as:
   ```json
   {"version":"0.4","title":"<Page>","type":"page",
    "content":[ ...elements... ],"page_settings":{"template":"default"}}
   ```
   The `content/page/<id>.json` (+ manifest entry) format is only for **Import Kit**.
3. **Section structure (standard):** every section =
   **Section (full-width 100%, background only, no padding) → one BOXED Content
   Container (set to the site's content width — `content_width:"boxed"`,
   `boxed_width` = the kit's content width, e.g. ~1140px on a default Elementor/Hello
   theme; read it from the kit, never exceed ~1300px — carries the padding) →
   content**.
   - **No excess containers:** content widgets sit directly in the boxed container.
     Don't double-wrap a lone image or text — one element = one widget. Add a nested
     container only for a genuine layout need (two-column row, a card with its own
     background, or a grid of repeated items).
   - **Variety:** mix layouts (two-column text+image, card grids, accordions), not
     just stacked single-column blocks.
   - **Padding discipline:** only the boxed container (and self-contained cards)
     carries padding; nested rows/columns/grids get **zero padding**; spacing comes
     from the container padding + gap.
8. **Emoji icons (reduce icon-library dependence):** don't rely only on Elementor /
   FontAwesome / Spectre icons. Where an icon accents content (card headers,
   benefit/feature lists, step markers), use an **emoji as the icon** — in a heading
   widget (large size for a card "icon") or inline at the start of a text line.
   Emoji need no icon font and are edited in the text field; save JSON as UTF-8. Keep
   real icon widgets where they fit (e.g. button arrows) — aim for a **mix** so a
   missing icon font never blanks the page.
4. **Button hover:** match the site. Where specified, color-change only — no
   size/shape animation (`hover_animation` empty).
5. **Mobile (audit the JSON before import):** **grids** set
   `grid_columns_grid_tablet` (~2) + `grid_columns_grid_mobile` (1); **flex rows**
   set `flex_direction_mobile: column`; **%-width columns** set `width_mobile` (100%)
   + `width_tablet`; **H1 + every section H2** carry `typography_font_size_mobile`/
   `_tablet` (a heading using a global typography slot with no mobile size won't
   shrink — give it self-contained responsive sizes); the boxed container gets a
   smaller `padding_mobile`; fixed-height images set `height_mobile`. Full list in
   `docs/Publishing-QA-Checklist.md` §5.
6. **IDs:** every element needs a unique `id`. When cloning a page, regenerate
   **all** ids so it imports as new (no collisions).
7. **Complete JSON only:** no `// ...`, no collapsed repeated widgets, valid
   braces/escaping — truncated Elementor JSON won't import.

---

## Fastest build route: clone-and-swap
Prefer copying the closest existing page and swapping content over authoring from
scratch: copy `content/page/<id>.json` → replace text → re-point location/topic →
regenerate all ids → keep the on-brand styling → audit. Author fresh only when no
existing page is close.

---

## Why per-site skills (not one global skill)
Each site has its own palette, font, voice, and templates. A shared skill would
blur them. The portable playbook + meta-skill stay constant; the *generated*
skills carry each site's identity. This keeps every site on its own brand while
the process itself is write-once.
