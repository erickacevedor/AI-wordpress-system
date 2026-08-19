# GEMINI.md

**Read [`AGENTS.md`](./AGENTS.md) — it is the canonical operating guide for this
repo.** This stub exists so Gemini CLI auto-loads that guidance; it is identical in
intent to `CLAUDE.md`. Follow `AGENTS.md` for the process, folder convention,
standards, and tooling.

## Route the task first

**Most tasks are the third row.**

| The situation | Where to start |
|---|---|
| A doc/brief for a site that is **already onboarded** (`projects/<site>/skills/` exists) | Skip to "build a page" — the common case |
| A site with an **exported Elementor kit**, not yet onboarded | `scripts/analyze-kit.py` + `skills/elementor-kit-onboarding` |
| A site with **no kit** — an HTML/CSS prototype, or brand new | `design-source/` + `scripts/analyze-prototype.py` + `skills/html-prototype-onboarding` |

Both onboarding paths converge on `projects/<site>/tokens.json`; everything after it
is identical and origin-agnostic.

## Build a page

```
projects/<site>/pages/<page-slug>/          # source doc goes here as source.<ext>
python3 projects/<site>/pages/<page-slug>/build.py
python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json   # MUST exit 0
python3 scripts/make-preview.py projects/<site>/pages/<page-slug>/<page-slug>.json
```

Build through the site's generated `<site>-*` skills, never from an ad-hoc read of
the kit. Match the kit; don't redesign it. Emit complete JSON. The client's site
usually is not reachable — verify locally before handoff, never against their live
site.
