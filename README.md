# Elementor AI Page System

A repeatable system for building on-brand Elementor pages for **any** WordPress site.
You point an AI coding agent at a site's exported Elementor kit; it learns that site's
brand once, then builds new pages from a content doc that import cleanly and look like
they always belonged.

> **Works with any file-capable AI coding agent** (Claude Code, OpenAI Codex, Gemini
> CLI, Cursor, …). Each reads its own config file — `CLAUDE.md`, `AGENTS.md`,
> `GEMINI.md`, `.cursor/rules/` — and they all point to the canonical **`AGENTS.md`**,
> the tool-agnostic source of truth. The agent needs file access and a shell (to read
> the kit, write skills, and emit JSON); a plain chat project can hold the
> instructions but can't do those steps.

---

## 1. The core idea — two layers

Keeping these two layers separate is the whole trick:

- **Portable layer (build once, reuse forever):** the process + two site-agnostic
  skills (`elementor-kit-onboarding`, `full-output-enforcement`) + the `scripts/`
  toolchain. Never changes site to site.
- **Per-site layer (generated once per website):** the brand-specific skills +
  `tokens.json` + `KIT-ANALYSIS.md` that carry a single site's colors, fonts, voice,
  and layout.

You never re-teach the process. For each new site you run a one-time **onboarding**
that *generates* that site's skills. After that, each page is just:
**content doc → build → validate → import.**

---

## 2. Repository layout

```
AI-wordpress-system/
├── README.md                         <- this file (how the system works)
├── AGENTS.md                         <- canonical operating guide for AI agents (source of truth)
├── CLAUDE.md · GEMINI.md · .cursor/  <- thin stubs that point every agent at AGENTS.md
├── docs/
│   ├── Elementor-Site-Playbook.md     <- the portable process, in depth
│   ├── Page-Creation-SOP.md           <- human step-by-step SOP
│   ├── content-brief-template.md      <- fill-in brief you hand the agent per page
│   ├── Example-Kit-Analysis-VitalAir.md <- an example of the kit analysis onboarding produces
│   └── Publishing-QA-Checklist.md     <- pre-publish QA gate (SEO, links, media, responsive)
├── skills/                            <- PORTABLE layer (never changes site to site)
│   ├── elementor-kit-onboarding/      <- analyzes a kit, GENERATES the per-site skills
│   ├── full-output-enforcement/       <- keeps Elementor JSON complete/valid
│   └── example-site-vitalair/         <- reference example of what onboarding generates
├── scripts/                           <- dependency-free Python 3 toolchain (any agent / CI)
│   ├── elementor_builder.py           <- reusable builder library (structure + responsive baked in)
│   ├── site_tokens.py                 <- canonical reader for ANY site's tokens.json
│   ├── elementor_meta.py              <- what a page needs from the target install
│   ├── analyze-kit.py                 <- deterministic kit miner (onboarding's counting half)
│   ├── validate-page.py               <- REQUIRED pre-import gate (invariants + responsive + contrast + deps)
│   ├── responsive-audit.py            <- responsive-only subset (also run by validate)
│   ├── contrast-audit.py              <- WCAG AA contrast (also run by validate)
│   ├── make-preview.py                <- PREVIEW.html generated FROM the page JSON
│   ├── page-diff.py                   <- "what changed vs. the live page", for redesigns
│   ├── verify-render.py               <- does the render match what the JSON promised?
│   ├── import-page.php · import-template.php  <- headless import (for the local sandbox)
│   ├── sandbox.sh                     <- drive a throwaway WP install to see the real render
│   ├── test-validate-page.py          <- regression tests for the gate itself
│   └── repackage-skills.sh            <- re-zip the portable skills after editing them
├── projects/                          <- ONE folder per site (the per-site layer)
│   └── <site>/
│       ├── current-theme/             <- the exported Elementor kit          [SITE-WIDE]
│       ├── tokens.json                <- brand tokens that feed every build   [SITE-WIDE]
│       ├── brand.py                   <- the site's component vocabulary      [SITE-WIDE]
│       ├── KIT-ANALYSIS.md            <- the design-system analysis (the "why")[SITE-WIDE]
│       ├── skills/                    <- GENERATED per-site skills            [SITE-WIDE]
│       └── pages/<page-slug>/         <- one self-contained folder PER PAGE:
│           ├── source.<ext>           <-   the page's source doc/brief
│           ├── build.py               <-   reproducible build (imports scripts/elementor_builder.py, reads ../../tokens.json)
│           ├── <page-slug>.json       <-   built, import-ready page
│           ├── PREVIEW.html           <-   browser design-review
│           └── HANDOFF-notes.md       <-   import + SEO handoff
├── skills-zipped/                     <- the two PORTABLE skills, pre-zipped for Claude Desktop upload
└── examples/                          <- real import-ready pages, for reference
```

**Site-wide vs. per-page.** The kit, `tokens.json`, `KIT-ANALYSIS.md`, and `skills/`
are the brand — shared by every page, so they live at the site root. Everything
specific to one page lives together in its own `pages/<page-slug>/` container, so a
site can hold many pages without collisions. Portable skills live once at repo-root
`skills/` and are *referenced*, never copied per site.

---

## 3. The skills

Skills are Markdown files (`SKILL.md`) with YAML frontmatter; an agent auto-invokes
one when a request matches its `description` triggers (or you name it explicitly).

### Portable skills (apply to every site)

**`elementor-kit-onboarding`** — the engine. Use when pointed at a new Elementor
export ("onboard this kit"). It mines the REAL design system from the widget styling
(not `site-settings.json`, whose globals are sometimes still theme defaults),
extracts the content voice, and writes the per-site skills + `tokens.json` +
`KIT-ANALYSIS.md`, then verifies them.

**`full-output-enforcement`** — completeness guard. Use when generating or editing any
Elementor JSON. Elementor exports are long and deeply nested; a truncated file fails
to import. This bans placeholders, enforces unique ids and required keys, and handles
token-limit splits cleanly.

### Per-site skills (generated by onboarding, one set per site)

- **`<site>-design-read`** — the front door. Reads the brief, states a one-line
  "design read" (page kind + closest existing page to mirror), routes to the others.
- **`<site>-ui-design`** — the visual system: palette + roles, type scale, button
  spec, the boxed section structure, emoji-icon guidance, mobile rules, reusable
  template IDs, and a review checklist.
- **`<site>-content-style`** — the copy voice: tone, locality, formatting, reusable
  copy patterns, CTA phrasings, do/don't.
- **`<site>-page-builder`** — the orchestrator. Runs the full pipeline: design read →
  map content to sections → write/polish copy → style → emit complete JSON → validate
  → audit.
- **`<site>-page-audit`** — the checker. Brand + Elementor-hygiene audit, WITH a "do
  NOT fix" list of intentional brand choices (so generic web-redesign instincts don't
  fight the brand).

---

## 4. The loop (do it in this order)

> **Rule: skills first, every new site.** Reading the kit and *generating* the
> `<site>-*` skills is a required step, once per site, **before any page is built.**
> Never build a page from an ad-hoc read of the kit — build only *through* the
> generated skills. That is what keeps every later page fast, consistent, and
> reviewable.

1. **Set up.** Create `projects/<site>/` and unzip the Elementor export
   (**Elementor → Tools → Export Kit**, include content + templates + settings) into
   `projects/<site>/current-theme/`.
2. **Onboard (required, once per site).** Open the repo with your agent and say
   **"Onboard this Elementor kit."** It runs `elementor-kit-onboarding` and writes the
   five `<site>-*` skills to `projects/<site>/skills/`, plus `tokens.json`,
   `KIT-ANALYSIS.md`, and a verification report.
3. **Verify the generated skills** — palette / font / type scale / button spec / voice
   match the live site; section-structure + responsive rules present. Fix the
   *skills*, not the output, if anything's off. Don't proceed until this passes.
4. **Build a page.** Create the page folder `projects/<site>/pages/<page-slug>/`, put
   the source doc in it (`source.<ext>`, or a filled `content-brief-template.md`), and
   say **"Build a page."** The `<site>-page-builder` runs the pipeline and writes the
   page + `PREVIEW.html` + `HANDOFF-notes.md` into that same folder.
5. **Validate & import.** The build must pass `<site>-page-audit` and the gate:
   ```
   python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json   # exit 0
   ```
   Then in WordPress: **Elementor → Templates → Import Templates** (up-arrow icon) →
   select the JSON → **Insert**. Set the SEO slug/title/description (handoff note),
   assign header/footer if not inherited, and publish.

Already onboarded a site? Skip to step 4 and reuse `projects/<site>/skills/`.

---

## 5. Building a page (reproducible)

Prefer authoring `pages/<page-slug>/build.py` on top of `scripts/elementor_builder.py`,
driven by the site-wide `tokens.json`, so a page is reproducible and correct by
construction. The library bakes in the section structure and responsive settings; the
page's `build.py` supplies the brand values (from tokens) and assembles the sections:

```
python3 projects/<site>/pages/<page-slug>/build.py           # writes <page-slug>.json
python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json
```

`validate-page.py` runs every import invariant in one command: valid JSON, single-page
wrapper, unique ids, exactly one H1, no visibility gates, no dead/`localhost` links,
the section-structure standard (full-width band → one boxed container, never nested),
alt text on every image, plus the full responsive check. Exit 0 = import-ready.

It also emits **warnings**, which report real problems without failing the gate:
adjacent sections sharing a background, padding on a nested layout row, and an
over-long meta title/description in the page's `HANDOFF-notes.md`. They encode design
and SEO convention rather than import invariants, so clearing them is a judgement
call — but each one is a genuine finding, not noise.

### The three build tiers

| Tier | File | Holds | Changes |
|---|---|---|---|
| Values | `projects/<site>/tokens.json` | colors, fonts, type scale, button spec, links | per site |
| Vocabulary | `projects/<site>/brand.py` | the site's components — hero, card, check list, FAQ, CTA band | per site |
| Invariants | `scripts/elementor_builder.py` | section structure + responsive correctness | never |

`brand.py` is what makes a site's *second* page cheap: it reads `tokens.json` (so no
brand constant is typed twice) and exposes the components mined from the kit's
reference page, leaving each `build.py` to supply only copy and section order.
`projects/gcreliable/brand.py` is the worked example. Skip it on a one-page site;
extract it before the third page, and certainly before a run of near-identical
service pages.

**Fastest content route: mirror the closest page.** Reuse the closest existing page's
*section model and styling values* — name it in the design read, then rebuild it
cleanly through `build.py`, changing only copy and section mix. Do **not** text-swap
the kit's own `content/page/<id>.json`: those pages predate the responsive standards
(no `*_mobile` keys) and their element ids collide on import, so the gate rejects
them. Mirror the design decisions; generate the structure.

---

## 6. Elementor rules baked into this system (hard-won)

These separate "imports and looks right" from "broken." Every per-site `ui-design`
and `page-audit` skill enforces them.

1. **Globals may be fake — decide per kit.** `site-settings.json` sometimes still
   holds Hello Elementor defaults (`#6EC1E4`, "Noto Sans Coptic") and sometimes holds
   real brand values. Read styling from the actual widgets; onboarding records whether
   this kit's globals are real (use them) or fake (apply colors/fonts inline).
2. **Single-page import needs a template wrapper.** The kit `content/page/<id>.json`
   format throws **"Invalid template type."** For single-page import, wrap as:
   `{"version":"0.4","title":"<Page>","type":"page","content":[ …elements… ],"page_settings":{"template":"default"}}`
   (The `content/page/<id>.json` + manifest form is only for **Import Kit**.)
3. **Section structure:** every section = **Section (full-width 100%, background, no
   padding) → one BOXED Content Container (the site's content width) → content.**
   Content widgets go directly in the boxed container — no excess wrappers around a
   lone image or text. Nested containers get **zero padding**. (Full standard in §7.)
4. **Button hover matches the site.** Some brands are color-change only (no size/shape
   animation); some use `shrink`. Keep the kit's convention — don't impose one.
5. **Mobile (every page must pass):** grids set `grid_columns_grid_tablet` (~2) +
   `grid_columns_grid_mobile` (1); flex rows set `flex_direction_mobile: column`;
   %-width columns set `width_mobile` (100%) + `width_tablet`; **H1 + every section
   H2** carry `typography_font_size_mobile`/`_tablet` (a heading pointing at a global
   typography slot with no mobile size will **not** shrink); the boxed container gets
   a smaller `padding_mobile`; fixed-height images set `height_mobile`.
6. **Unique ids.** Every element needs a unique `id`; regenerate all ids when cloning
   a page so it imports as new.
7. **Complete JSON only.** No `// …`, no collapsed repeated widgets, valid
   braces/escaping — truncated Elementor JSON won't import. Save as UTF-8.
8. **Live widgets can't be embedded** (e.g. Google review sliders). Insert a labeled
   shortcode/placeholder and swap the real widget in after import.

Rules 3, 5, 6, 7 (and more) are checked automatically by `scripts/validate-page.py`.

---

## 7. Layout standards

Every page the system builds follows these; every per-site `ui-design`,
`page-builder`, and `page-audit` skill enforces them, and `scripts/elementor_builder.py`
bakes them in.

**1. Two-tier section structure — full-width band + boxed content.**

```
Section                 (full-width 100% — background only, NO padding)
  └─ Content Container   (BOXED to the site's content width — carries the padding)
       └─ content        (headings, text, buttons, and multi-column rows/grids)
```

The outer Section always spans the full viewport (so backgrounds/overlays go edge to
edge). Inside sits **exactly one** boxed Content Container set to the **site's own
content width** (`content_width: "boxed"`, `boxed_width` = the kit's content width —
e.g. ~1140px on a default Elementor/Hello theme; read it from the kit, never exceed
~1300px).

**2. No excess containers.** Content widgets sit **directly** in the boxed container —
one image = one image widget; one paragraph = one text widget. Add a nested container
**only** for a genuine layout need: a two-column row, a card that carries its own
background, or a grid of repeated items. Aim for a variety of layouts (two-column
text+image, card grids, accordions), not stacked single-column blocks.

**3. Padding discipline.** Only the boxed Content Container (and self-contained cards)
carries padding. Nested rows/columns/grids get zero padding; spacing comes from the
container's padding + gap.

**4. Button behavior.** Keep the site's own button shape and hover convention.

**5. Emoji icons (reduce icon-library dependence).** Where an icon accents content
(card headers, benefit/feature lists, step markers), use an **emoji as the icon** — in
a heading/text widget (large size for a card "icon", inline for a list line). Emoji
render cross-platform and need no icon font. Keep genuine icon widgets where they fit
(e.g. a button arrow); the goal is a **mix**, so a missing icon font never blanks the
page.

---

## 8. Content-to-live coverage (SEO, links, media, QA, posts)

The system takes content from draft to a publish-ready page — not just layout. Every
per-site skill enforces these; onboarding builds them into each new site's skills.

- **SEO elements:** exactly one H1 with a clean heading hierarchy; meta title
  (< 60 chars), meta description (< 155 chars), and a lowercase-hyphenated slug; target
  keyword in the H1 and intro. (Elementor JSON doesn't store WP SEO meta, so
  title/description/slug are a publish-time handoff for Rank Math / Yoast.)
- **Internal linking:** required internal links with descriptive anchor text; no dead
  links; CTAs point to real destinations.
- **Image / media placement:** hero and feature images via the two-column or
  background pattern with a dark overlay for legibility; alt text on every image;
  labeled placeholders for live widgets to wire up after import.
- **Publishing & QA:** the pre-publish gate in `docs/Publishing-QA-Checklist.md`
  (brand, structure, SEO, links, media, responsive), then the publish steps.
- **Posts as well as pages:** the same workflow builds blog posts — use the site's
  single-post template, set the brief's page type to "post," and handle post extras
  (featured image, category/tags, author, SEO) at publish.

---

## 9. Toolchain (`scripts/`)

Dependency-free Python 3, so any agent or CI can run it.

| Command | Purpose |
|---|---|
| `python3 scripts/analyze-kit.py projects/<site>/current-theme` | **Onboarding.** Mines the kit: palette by real usage, fonts, type scale, button spec, section rhythm, Pro/plugin dependencies, gotchas. Does the counting so the agent does the judging |
| `python3 projects/<site>/pages/<slug>/build.py` | Build that page from tokens + section assembly (reproducible) |
| `python3 scripts/validate-page.py <page>.json` | **Required gate.** All import invariants incl. responsive, contrast, dependencies. Exit 0 = ready |
| `python3 scripts/responsive-audit.py <page>.json` | Responsive-only subset (also run by validate) |
| `python3 scripts/contrast-audit.py <page>.json` | WCAG AA contrast only (also run by validate) |
| `python3 scripts/make-preview.py <page>.json [--css site.css]` | Generate `PREVIEW.html` **from** the page JSON, breakpoints included, so it cannot drift |
| `python3 scripts/page-diff.py <new>.json --kit-page <id>` | **Redesigns.** "What changed vs. the live page", ready for the handoff (`--find` to locate the live page) |
| `python3 scripts/verify-render.py <page>.json <url>` | Compare a rendered page against what the JSON promised |
| `scripts/sandbox.sh check\|import\|verify\|page` | Drive a local throwaway WordPress to see the real Elementor render before handoff |
| `python3 scripts/test-validate-page.py` | Regression tests for the gate — run after touching the validator |
| `scripts/repackage-skills.sh` | Re-zip the portable skills into `skills-zipped/` after editing them |

`scripts/elementor_builder.py` is the reusable builder library — brand styling is
passed in (from `tokens.json`); structural + responsive correctness is baked in, so a
page built entirely through it passes the validator. A site's `brand.py` sits between
the two: site components built from the library, valued from the tokens.

The gate has its own tests because a gate nobody tests silently stops gating —
`test-validate-page.py` mutates a known-good page so each check *must* fire, and
asserts the deliberate non-firing cases stay quiet.

---

## 10. Seeing the page before you ship it

The target site usually **cannot be reached from here.** The deliverable is a JSON
file plus its handoff note; somebody else imports it, on a host we may never touch,
once. That single constraint shapes the whole back half of this system: everything
has to be verified *before* handoff, because there is no feedback afterwards.

Three levels, cheapest first:

**1. The gate.** `validate-page.py` proves the file is structurally sound and reports
what it cannot fix for you — contrast below AA, addon plugins and shortcodes the target
must have, links to pages that do not exist. (Elementor Pro is assumed everywhere, so
Pro widgets are never flagged.)

**2. The preview.** `make-preview.py` renders the page JSON to a standalone HTML file,
including real media queries, so the mobile and tablet layouts are inspectable by
resizing the window. It is generated *from* the page, so it cannot disagree with what
ships. Pass `--css` to inline a site stylesheet when the design leans on CSS classes.

```
python3 scripts/make-preview.py projects/<site>/pages/<slug>/<slug>.json
```

**3. The sandbox.** The only ground truth is Elementor itself. Keep one throwaway
WordPress + Elementor install locally, import into *that*, and compare the render
against the JSON:

```
export SANDBOX_WP="/path/to/wp"  SANDBOX_URL="http://localhost:10010"
scripts/sandbox.sh check
scripts/sandbox.sh page projects/<site>/pages/<slug>/<slug>.json
```

`sandbox.sh page` validates, imports (idempotently, matched by slug), refetches the
URL and checks that every heading, CTA and image the JSON promised is actually in the
rendered HTML — plus the container count, which is how you catch a payload that
imported "successfully" and rendered nothing.

**Never point this at the client's site to "try it".** The sandbox exists so the
client's install only ever sees a file that has already been proven.

---

## 11. Redesigning an existing page

Same loop, one extra step: the client already has a page, cannot preview the
replacement, and needs to know what they are losing before they approve it.

```
python3 scripts/page-diff.py <new>.json --find          # find the live page in the kit
python3 scripts/page-diff.py <new>.json --kit-page 225062 --markdown
```

That emits a "What changed vs. the live page" block — headings added, dropped and
kept, CTA changes and re-targets, image and word counts, band sequence before/after —
to paste into `HANDOFF-notes.md`. It compares *content*, not markup, because a rebuilt
page shares no element ids or container structure with the original.

---

## 12. Set up your agent

- **Claude Code / Codex / Gemini CLI / Cursor:** clone the repo and open it. The agent
  auto-loads its config file (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` /
  `.cursor/rules/`), all of which point to `AGENTS.md`. Say **"Onboard this Elementor
  kit."**
- **Claude Desktop (Cowork):** upload the zips from `skills-zipped/`
  (`elementor-kit-onboarding.zip`, `full-output-enforcement.zip`) via
  **Customize → Skills → Create skill**, connect the folder holding the kit, keep
  `docs/Elementor-Site-Playbook.md` handy, and say **"Onboard this Elementor kit."**

The `skills/example-site-vitalair/` set and the `examples/*.json` pages are reference
material showing what a good onboarding + build produces — they are not installed on
other sites; onboarding generates fresh `<site>-*` skills for each website.
