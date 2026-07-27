# GEMINI.md

**Read [`AGENTS.md`](./AGENTS.md) — it is the canonical operating guide for this
repo.** This stub exists so Gemini CLI auto-loads that guidance; it is identical in
intent to `CLAUDE.md`. Follow `AGENTS.md` for the process, folder convention,
standards, and tooling.

Quick loop: kit → `projects/<site>/current-theme/`, content → `new-content/` →
**onboard once (generate `<site>-*` skills) before building** → build to `output/` →
`python3 scripts/validate-page.py <page>.json` must pass → hand off for import.
