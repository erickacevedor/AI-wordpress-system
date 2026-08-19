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
├── current-theme/           ← the unzipped Elementor kit export             [SITE-WIDE]
│   ├── manifest.json        ← index of everything
│   ├── site-settings.json   ← global colors/fonts (REAL on some kits, theme defaults on others)
│   ├── content/page/*.json  ← pages   · content/post/*.json ← posts
│   └── templates/*.json     ← header, footer, reusable containers
├── tokens.json              ← brand tokens that feed every page build       [SITE-WIDE]
├── KIT-ANALYSIS.md          ← design-system analysis (the "why")            [SITE-WIDE]
├── skills/                  ← GENERATED per-site skills (by onboarding)     [SITE-WIDE]
│   └── <site>-{design-read,ui-design,content-style,page-builder,page-audit}/
└── pages/                   ← one self-contained folder PER PAGE
    └── <page-slug>/
        ├── source.<ext>        ← the page's source doc/brief
        ├── build.py            ← reproducible build (imports scripts/elementor_builder.py, reads ../../tokens.json)
        ├── <page-slug>.json    ← built import-ready page
        ├── PREVIEW.html
        └── HANDOFF-notes.md
```

The kit, `tokens.json`, `KIT-ANALYSIS.md`, and `skills/` are **site-wide** (shared by
every page). Everything specific to one page lives together in its own
`pages/<page-slug>/` container, so a site can hold many pages without collisions.

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
site settings). Unzip into `projects/<site>/current-theme/` and point Claude at the
repo. (Each page's source doc goes in its own `projects/<site>/pages/<page-slug>/`
folder at build time — Step 5.)

### Step 2 — Analyze the kit & generate the site skills

Start with the counting, which is mechanical and should not vary between runs:

```
python3 scripts/analyze-kit.py projects/<site>/current-theme
```

That reports the palette ranked by real usage (and what each colour is used *on*),
the fonts, the heading sizes that actually occur, the most-repeated button spec and
its hover convention, the section rhythm, the widget mix, whether `site-settings.json`
is still Hello-Elementor defaults, which Elementor Pro / addon plugins the kit relies
on, and the gotchas (visibility gates, `localhost` URLs, duplicate global colour ids).

Then run the `elementor-kit-onboarding` skill over those facts to do the part that
needs judgement — which colour is the CTA, is the palette real, what is the voice. It:

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
2. **Extract the source.** For a `.docx`: unzip `word/document.xml`, strip tags,
   un-escape entities, and write `source.txt` beside it. Watch for mojibake — client
   exports carry curly quotes that arrive as `?`/`�`; restore them as
   `&rsquo;`/`&mdash;` rather than flattening them to ASCII.
3. **Map content** to the site's standard section anatomy.
4. **Write/polish copy** with `<site>-content-style`.
5. **Style** with `<site>-ui-design` (inline, on-brand).
6. **Emit complete JSON** with `full-output-enforcement`, by authoring
   `projects/<site>/pages/<page-slug>/build.py` on top of `scripts/elementor_builder.py`
   (which bakes in the boxed section structure + responsive settings, so the page is
   reproducible and passes the gate) driven by the site-wide `projects/<site>/tokens.json`.
   See "The three build tiers" below — on a site with more than two or three pages,
   `build.py` should sit on a site-wide `brand.py`, not directly on the library.
7. **Validate** — `python3 scripts/validate-page.py <page>.json` must exit 0 (all
   import invariants incl. responsive), then **audit** with `<site>-page-audit`.
8. **Export** an importable single-template file (see format below) + optionally
   register in `manifest.json` for full-kit import.

Each page folder ends up holding: `source.<ext>`, `build.py`, `<page-slug>.json`,
`PREVIEW.html`, `HANDOFF-notes.md`. The handoff note is where the WP-level metadata
lives (slug, meta title, meta description) — Elementor JSON cannot carry it, and the
validator length-checks what it finds there.

---

## Publishing & QA (before the page goes live)

After the build, run the pre-publish QA checklist (see
`docs/Publishing-QA-Checklist.md`): brand + structure, SEO elements (one H1, meta
title/description, slug, keyword), required internal links with good anchor text,
images have alt text, live-widget placeholders noted, mobile view checked, and all
links resolve. `validate-page.py` already enforces the mechanical half of that list
(structure, alt text, responsive, links, ids) and *warns* on band rhythm, padding
discipline and over-long meta — so the checklist items left for a human are the
judgement ones: does the copy read right, do the links point at the right pages, is
the live widget wired up. Then import, set the WP SEO meta (Rank Math / Yoast), assign
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
4. **Emoji icons (reduce icon-library dependence):** don't rely only on Elementor /
   FontAwesome / Spectre icons. Where an icon accents content (card headers,
   benefit/feature lists, step markers), use an **emoji as the icon** — in a heading
   widget (large size for a card "icon") or inline at the start of a text line.
   Emoji need no icon font and are edited in the text field; save JSON as UTF-8. Keep
   real icon widgets where they fit (e.g. button arrows) — aim for a **mix** so a
   missing icon font never blanks the page.
5. **Button hover:** match the site. Where specified, color-change only — no
   size/shape animation (`hover_animation` empty).
6. **Mobile (audit the JSON before import):** **grids** set
   `grid_columns_grid_tablet` (~2) + `grid_columns_grid_mobile` (1); **flex rows**
   set `flex_direction_mobile: column`; **%-width columns** set `width_mobile` (100%)
   + `width_tablet`; **H1 + every section H2** carry `typography_font_size_mobile`/
   `_tablet` (a heading using a global typography slot with no mobile size won't
   shrink — give it self-contained responsive sizes); the boxed container gets a
   smaller `padding_mobile`; fixed-height images set `height_mobile`. Full list in
   `docs/Publishing-QA-Checklist.md` §5.
7. **IDs:** every element needs a unique `id`. When cloning a page, regenerate
   **all** ids so it imports as new (no collisions).
8. **Complete JSON only:** no `// ...`, no collapsed repeated widgets, valid
   braces/escaping — truncated Elementor JSON won't import.

---

## The three build tiers

Brand knowledge is split by *kind*, so every fact lives in exactly one place:

| Tier | File | Holds | Changes |
|---|---|---|---|
| Values | `projects/<site>/tokens.json` | colors, fonts, type scale, button spec, links | per site |
| Vocabulary | `projects/<site>/brand.py` | that site's components — hero, card, check list, FAQ, CTA band | per site |
| Invariants | `scripts/elementor_builder.py` | section structure + responsive correctness | never |

`brand.py` is the tier that makes a site's *second* page cheap. It reads
`tokens.json` (no brand constant is typed twice) and exposes the components mined
from the kit's reference page, so each `pages/<slug>/build.py` supplies only **copy
and section order**. `projects/gcreliable/brand.py` is the worked example.

Skip it for a one-page site. Extract it **before** the third page, and certainly
before a run of near-identical service pages — after that, the vocabulary is already
duplicated across build scripts and the extraction costs more than it saves.

## Fastest content route: mirror the closest page

Reuse the closest existing page's **section model and styling values** — that is the
single biggest time-saver, and it is what keeps a new page looking like it always
belonged. Name it in the design read ("a sibling of AC Repair"), then rebuild it
cleanly through `build.py`, changing only copy and section mix.

> **Not by copying the JSON file.** Text-swapping a `content/page/<id>.json` from the
> kit looks faster but fails the gate: kit pages predate the responsive standards, so
> they carry no `*_mobile` keys, and their element ids collide on import. Mirror the
> *design decisions*, generate the *structure*.

---

## When a site arrives without an Elementor kit

Step 1 assumes an export. A site sometimes arrives as a static design instead (an
HTML/CSS repo, a Figma handoff, a live URL with no export access), or has to be
designed from scratch. That path is a first-class stage of this repo — see
[`design-source/README.md`](../design-source/README.md):

```bash
# building the design from scratch? start from the master prompt
design-source/prompts/local-service-site.md      # fill every [[ FIELD ]], then run it

# then, prototype in hand:
python3 scripts/analyze-prototype.py projects/<site>/design-source
python3 scripts/analyze-prototype.py projects/<site>/design-source \
        --emit-tokens projects/<site>/tokens.json
# then run skills/html-prototype-onboarding to write KIT-ANALYSIS.md + the five skills
```

The loop still holds — only the *source* of the design read changes:

- Step 1 has no `current-theme/`. Point the onboarding at whatever the design system
  actually lives in (the stylesheet's custom properties, the source repo's config).
- Steps 2–3 are unchanged and still **required**: mine the palette/type/voice, write
  `tokens.json` + `KIT-ANALYSIS.md`, and still generate the `<site>-*` skills. Without
  them there is no recorded voice for the next build, and page two starts from zero.
- Note the source and variant in `tokens.json` (e.g. `_source`, `_variant`) so a later
  build knows which design it is matching.
- Theme parts (header/footer) become Elementor **library templates** built the same
  way, under `pages/_theme/`; they validate as `type: "header"` / `"footer"`, which
  the gate treats as pages-without-an-H1.

`projects/lenz/` is this case. It is also the cautionary example: it was onboarded
from HTML, the skill-generation step got skipped as "not applicable," and it is the
one site with no `<site>-*` skills to build its next page from — which is exactly
what `skills/html-prototype-onboarding` now exists to prevent.

**Set the content width deliberately on this path.** A from-scratch prototype has no
kit telling it what the content width is, and the master prompt defaults to 1800px
while every kit in `projects/` boxes at 1140–1280px. Decide it before the prototype
is built; reconciling it afterwards means re-deciding every section's proportions.

## Why per-site skills (not one global skill)
Each site has its own palette, font, voice, and templates. A shared skill would
blur them. The portable playbook + meta-skill stay constant; the *generated*
skills carry each site's identity. This keeps every site on its own brand while
the process itself is write-once.
