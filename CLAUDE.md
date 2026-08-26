# CLAUDE.md

**Read [`AGENTS.md`](./AGENTS.md) — it is the canonical operating guide for this
repo** (the process, the folder convention, the standards, and the tooling). This
file exists so Claude Code auto-loads that guidance; everything below is the
30-second version.

## First, route the task

**Most tasks are the third row.** Check which one you are on before doing anything.

| The situation | Where to start |
|---|---|
| A doc/brief for a site that is **already onboarded** (`projects/<site>/skills/` exists) | Skip straight to "build a page" below. This is the common case. |
| A site with an **exported Elementor kit** but no skills yet | Onboard first: `scripts/analyze-kit.py` + `skills/elementor-kit-onboarding` |
| A site with **no kit** — only an HTML/CSS prototype or a brand-new build | `design-source/` + `scripts/analyze-prototype.py` + `skills/html-prototype-onboarding` |

Both onboarding paths converge on `projects/<site>/tokens.json`. Everything after
that point is identical and origin-agnostic.

## Build a page

```
projects/<site>/pages/<page-slug>/          # source doc goes here as source.<ext>
python3 projects/<site>/pages/<page-slug>/build.py
python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json   # MUST exit 0
python3 scripts/make-preview.py projects/<site>/pages/<page-slug>/<page-slug>.json
```

Out: `<page-slug>.json` + `PREVIEW.html` + `HANDOFF-notes.md` in that same folder.
Build **through the site's generated `<site>-*` skills**, never from an ad-hoc read
of the kit.

## The rules that bite

- **Match the kit; don't redesign it.** Brand values come from `tokens.json`, which
  onboarding extracts. Don't invent them.
- **`validate-page.py` exit 0 is not optional.** Warnings are real findings, but
  only errors block.
- **The target site usually is not reachable.** Verify with the preview (and
  `scripts/sandbox.sh` against a *local throwaway* WordPress) before handoff — never
  against the client's live site.
- Emit complete JSON. No elisions, no "the rest follows the same pattern."

## Before authoring a build.py

Read [`docs/Elementor-Output-Anatomy.md`](./docs/Elementor-Output-Anatomy.md) — what a
finished page from this repo actually looks like: the full-width→boxed section pair the
gate enforces as an **error**, `__globals__` colour binding instead of hex, the
responsive settings that are errors and not warnings, and the two porting strategies
(kit-native vs. a companion CSS plugin) with what each costs.

See `AGENTS.md` for the full process, `README.md` for the master overview,
`docs/Elementor-Site-Playbook.md` for the detailed playbook,
`docs/Elementor-Output-Anatomy.md` for the anatomy of the output, and
`design-source/README.md` for the HTML stage.
