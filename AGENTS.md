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
  + `skills/full-output-enforcement` + `scripts/`.
- **Per-site** (generated once per website): each `projects/<site>/skills/<site>-*`
  set carries a single site's colors, fonts, voice, and layout.

## Folder convention (one per site)

```
projects/<site>/
├── current-theme/     ← the unzipped Elementor kit export (manifest, site-settings, content/, templates/)  [SITE-WIDE]
├── tokens.json        ← the site's brand tokens (colors/fonts/button/links) — feeds every page build       [SITE-WIDE]
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
   (design-read → map sections → write copy → style → emit JSON) — ideally by
   authoring `pages/<page-slug>/build.py` on top of `scripts/elementor_builder.py`
   (reading `../../tokens.json`) so the page is reproducible. Write the page +
   `PREVIEW.html` + `HANDOFF-notes.md` into that same page folder.
4. **Validate (required gate).** `python3 scripts/validate-page.py <page>.json` must
   exit 0. Then run `<site>-page-audit` for brand/voice.
5. **Hand off.** Tell the user the import path (Elementor → Templates → Import
   Templates) and the post-import wiring (SEO meta/slug, header/footer, image swaps).

Already onboarded (`dolan`, `magnolia`, `petitt`)? Skip to step 3 — reuse `projects/<site>/skills/`.

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
   `display_condition_list` gates; no dead (`#`/empty) or `localhost` links.

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
| `python3 projects/<site>/pages/<slug>/build.py` | Build that page from tokens + section assembly (reproducible) |
| `python3 scripts/validate-page.py <page>.json` | **Required gate.** All import invariants incl. responsive. Exit 0 = ready |
| `python3 scripts/responsive-audit.py <page>.json` | Responsive-only subset (also run by validate) |
| `scripts/repackage-skills.sh` | Re-zip the portable skills into `skills-zipped/` after editing them |

- `scripts/elementor_builder.py` — the reusable builder library. Brand styling is
  passed in (from `tokens.json`); structural + responsive correctness is baked in, so
  a page built entirely through it passes the validator.
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
