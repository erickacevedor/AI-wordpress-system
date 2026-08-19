# AGENTS.md — Operating guide for AI agents in this repo

**This file is the canonical, tool-agnostic source of truth.** Claude Code reads
`CLAUDE.md`, OpenAI Codex reads `AGENTS.md`, Gemini CLI reads `GEMINI.md`, Cursor
reads `.cursor/rules` — the per-tool files are thin stubs that all point here. If you
are any coding agent working in this repo, follow this document.

---

## What this repo is

A system for building **on-brand Elementor pages for any WordPress site**. You point
the system at a site's exported Elementor kit; it learns that site's brand and builds
new pages that import cleanly and look like they always belonged.

**Two layers (keep them separate):**
- **Portable** (never changes site to site): the process + `skills/elementor-kit-onboarding`
  + `skills/html-prototype-onboarding` + `skills/full-output-enforcement` + `scripts/`.
- **Per-site** (generated once per website): each `projects/<site>/skills/<site>-*`
  set carries a single site's colors, fonts, voice, and layout.

## Route the task before doing anything

**Most tasks are the third row — a doc for a site that is already onboarded.** Check
which row you are on first; the other two are one-time setup.

| The situation | Start at |
|---|---|
| A doc/brief for an **already-onboarded** site (`projects/<site>/skills/` exists) | **Step 3** of the loop below. The common case. |
| A site with an **exported Elementor kit**, not yet onboarded | Step 1 — `scripts/analyze-kit.py` + `skills/elementor-kit-onboarding` |
| A site with **no kit**: an HTML/CSS prototype, a design repo, or a brand-new build | `design-source/` — `scripts/analyze-prototype.py` + `skills/html-prototype-onboarding` |

**Two origins, one seam.** A site's design system is either *mined from a kit* or
*read from a prototype*. Both produce `projects/<site>/tokens.json`, and everything
downstream — `brand.py`, `build.py`, the gate, the preview, the handoff — is
origin-agnostic. Nothing after the seam knows or cares which path the site took.

```
kit export  ──> current-theme/  ──> analyze-kit.py ──────┐
                                                          ├──> tokens.json ──> the loop below
HTML design ──> design-source/  ──> analyze-prototype.py ─┘
```

A site stays **one folder** either way: `projects/<site>/` holds its origin, its
tokens, its skills and its pages together.

## Folder convention (one per site)

```
projects/<site>/
├── current-theme/     ← the unzipped Elementor kit export (manifest, site-settings, content/, templates/)  [SITE-WIDE]
│                     ...or, for a site with no kit:
├── design-source/     ← the HTML/CSS prototype this site's design system comes from  [SITE-WIDE]
├── tokens.json        ← the site's brand tokens (colors/fonts/button/links) — feeds every page build       [SITE-WIDE]
├── brand.py           ← the site's component vocabulary over elementor_builder.py (extract before page 3)  [SITE-WIDE]
├── KIT-ANALYSIS.md    ← the design-system analysis onboarding produced (why the tokens are what they are)   [SITE-WIDE]
├── skills/            ← GENERATED per-site skills: <site>-{design-read,ui-design,content-style,page-builder,page-audit}/  [SITE-WIDE]
└── pages/             ← one self-contained folder PER PAGE
    └── <page-slug>/
        ├── source.<ext>       ← the page's source doc/brief
        ├── build.py           ← reproducible build (imports scripts/elementor_builder.py, reads ../../tokens.json)
        ├── <page-slug>.json   ← the built, import-ready page
        ├── PREVIEW.html       ← browser design-review
        └── HANDOFF-notes.md   ← import + SEO handoff
```

**Site-wide vs. per-page:** the kit, `tokens.json`, `KIT-ANALYSIS.md`, and `skills/`
are the brand — shared by every page, so they stay at the site root. Everything
specific to one page (source, build, output, preview, handoff) lives together in its
own `pages/<page-slug>/` container, so a site can hold many pages without collisions.
Portable skills live once at repo-root `skills/`; they are **referenced**, never
copied per site.

A `build.py` finds the repo root by walking up to `AGENTS.md`, so it works regardless
of nesting depth.

---

## The loop — do this in order

> **Rule: skills first, every new site.** Reading the kit and *generating* the
> `<site>-*` skills is a required step, once per site, **before any page is built.**
> Never build a page from an ad-hoc read of the kit — build only *through* the
> generated skills. This is what keeps every later page fast and consistent.

1. **Set up.** Unzip the Elementor export into `projects/<site>/current-theme/`.
2. **Onboard (required, once per site).** Run `skills/elementor-kit-onboarding`: read
   `current-theme/`, mine the REAL design system (see below), and write the five
   `<site>-*` skills to `projects/<site>/skills/`, a `projects/<site>/tokens.json`,
   and `projects/<site>/KIT-ANALYSIS.md`. Verify palette/fonts/button/voice vs. the
   live site before proceeding.
3. **Build a page.** Create `projects/<site>/pages/<page-slug>/`, put the source doc
   there (`source.<ext>`), and run the site's `<site>-page-builder` pipeline
   (design-read → extract source → map sections → write copy → style → emit JSON) by
   authoring `pages/<page-slug>/build.py` on the site's `brand.py` — or directly on
   `scripts/elementor_builder.py` if the site has none yet — reading `../../tokens.json`
   so the page is reproducible. Write the page + `PREVIEW.html` + `HANDOFF-notes.md`
   into that same page folder.
4. **Validate (required gate).** `python3 scripts/validate-page.py <page>.json` must
   exit 0. Then run `<site>-page-audit` for brand/voice.
5. **Preview + verify before handing off.** The target site usually **cannot be
   reached from here** — the deliverable is the JSON plus its handoff note, and
   somebody else imports it, once, with no second try. So confirm it here first:
   `python3 scripts/make-preview.py <page>.json` for a review render straight from the
   JSON (breakpoints included), and — when it matters — import into a local throwaway
   WordPress with `scripts/sandbox.sh page <page>.json` to see what Elementor actually
   does with it. Never verify against the client's live site.
6. **Hand off.** Tell the user the import path (Elementor → Templates → Import
   Templates) and the post-import wiring (SEO meta/slug, header/footer, image swaps).
   List the dependencies the gate reported — addon plugins, shortcodes, custom widgets
   — because a missing plugin renders as an empty gap that the client finds first.
   (Elementor Pro is assumed on every target and is not reported.)

Already onboarded (`dolan`, `magnolia`, `petitt`, `gcreliable`)? Skip to step 3 — reuse `projects/<site>/skills/`.

---

## Standards every page must meet (enforced by the library + validator)

1. **Section structure:** every section = full-width (100%) Section (background only)
   → **one boxed content container at the site's content width (~1140px)** → content
   directly. No excess wrapper around a lone image/text. Padding lives only on the
   boxed container (and self-contained cards).
2. **Layout variety:** mix two-column rows, card grids, and accordions — not stacked
   single-column blocks.
3. **Icons:** mix **emoji as icons** (heading/text widgets) with native icons, so a
   page never depends entirely on an icon font. Save JSON as UTF-8.
4. **Responsive:** grids stack (tablet ~2 / mobile 1); flex rows stack on mobile;
   %-width columns go 100% on mobile; H1 + every H2 have mobile sizes; boxed
   containers have `padding_mobile`; fixed-height images have `height_mobile`.
5. **Import hygiene:** single-page wrapper `{version,title,type:"page",content,page_settings}`;
   unique element ids; exactly one H1; complete/valid JSON (no truncation); no
   `display_condition_list` gates; no dead (`#`/empty) or `localhost` links; alt text
   on every image.

6. **Accessible by construction** (build-time rules — hold to these while authoring;
   the validator does not check them):
   - **Heading levels never skip.** H1 → H2 → H3 in order. Don't jump H2 → H4 to get
     a smaller size — set the size, keep the level.
   - **Every CTA carries a visible, descriptive label.** No icon-only buttons. "Call
     (555) 123-4567", not a bare phone glyph. Where a kit genuinely uses an icon-only
     control (a mobile header phone button), note it in the handoff so an accessible
     name gets added after import.
   - **Nothing auto-plays.** No auto-playing video, audio, or motion.
   - **A form field's label is a label, not a placeholder.** Placeholder text
     disappears on focus and is invisible to most screen readers; every field needs a
     real label.
   - **Every page records a canonical URL** in its `HANDOFF-notes.md`, beside the slug
     and meta. Elementor JSON cannot carry it, so the note is the only place it exists.

The validator **blocks** on all of the above except #6. It **warns** on findings that are real
but are not import failures: two adjacent sections sharing a background; padding on a
nested layout row/column/grid; an over-long meta title (≥60) or description (≥155) in
the page's `HANDOFF-notes.md`; text/background pairs below WCAG AA; widgets that need
an addon plugin or a shortcode on the target install (Elementor Pro is assumed present
and never flagged); and internal links pointing at pages the kit does not have. Clearing a warning is a judgement call
— but each one is a genuine finding, not noise.

The design read, palette-is-real-or-fake call, button-hover convention, and section
rhythm are **per site** — read them from `projects/<site>/skills/<site>-ui-design`
and `KIT-ANALYSIS.md`. Don't invent brand values; onboarding extracts them.

## Onboarding: mine the REAL design system

`site-settings.json` globals are sometimes still Hello-Elementor defaults and
sometimes real — decide per kit by reading the actual widget styling. Extract:
most-used hex colors → palette + roles; most-used `font_family` → brand fonts;
heading `font_size` spread → type scale; a representative button → CTA spec (incl.
hover convention — some sites are color-only, some use `shrink`); section-background
sequence → rhythm; `templates/` → reusable header/footer. Watch for kit gotchas
(e.g. `display_condition_list` visibility gates that must be dropped; `localhost`
export URLs → use root-relative links).

---

## Tooling (dependency-free Python 3 — works under any agent or CI)

| Command | Purpose |
|---|---|
| `python3 scripts/analyze-kit.py projects/<site>/current-theme` | **Onboarding, kit origin.** Mines the kit: palette by real usage, fonts, type scale, button spec, section rhythm, plugin dependencies, gotchas. Does the counting so the agent does the judging |
| `python3 scripts/analyze-prototype.py projects/<site>/design-source` | **Onboarding, HTML origin.** Same job against a prototype's CSS: colour ramps, semantic roles (resolving `var()`), type scale, spacing, contrast. `--emit-tokens <path>` writes the `tokens.json` skeleton |
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

- `scripts/elementor_builder.py` — the reusable builder library. Brand styling is
  passed in (from `tokens.json`); structural + responsive correctness is baked in, so
  a page built entirely through it passes the validator.
- `design-source/` — the HTML stage: the master prompt for building a prototype from
  scratch, and how to onboard one. Optional; untouched by kit-origin sites. See
  `design-source/README.md`.
- `scripts/site_tokens.py` / `scripts/elementor_meta.py` — importable helpers. The
  first reads ANY site's `tokens.json` through a canonical view (sites name their
  colour roles differently; it normalises on read rather than forcing a migration).
  The second answers what a page needs from the target install vs. what the kit's
  manifest says it has.
- `projects/<site>/brand.py` — the middle tier: that site's components (hero, card,
  check list, FAQ, CTA band) built on the library and valued from `tokens.json`, so a
  page's `build.py` supplies only copy + section order. Extract it before the third
  page of a site; `projects/gcreliable/brand.py` is the worked example.
- Reuse the closest existing page's **section model and styling values**, but never by
  text-swapping the kit's `content/page/<id>.json` — those pages predate the responsive
  standards and their ids collide on import. Mirror the decisions, generate the structure.
- Extracting content from a `.docx`: `textutil -convert txt` (macOS) or unzip
  `word/document.xml` and strip tags.

## Guardrails

- Match the kit; don't redesign it. Keep each site's button shape/hover as-is.
- Never emit `display_condition_list`. Use root-relative internal links.
- Emit complete JSON — no `// ...`, no "other sections follow the same pattern."
- If a brand-critical fact is missing (hero headline, location, CTA target), ask one
  focused question rather than guessing.
- The two root PDFs and `docs/*VitalAir*` are legacy references; the live process is
  this file + `README.md` + `docs/Elementor-Site-Playbook.md`.
