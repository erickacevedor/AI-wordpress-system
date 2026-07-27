# CLAUDE.md

**Read [`AGENTS.md`](./AGENTS.md) — it is the canonical operating guide for this
repo** (the process, the folder convention, the standards, and the tooling). This
file exists so Claude Code auto-loads that guidance; everything below just points
there.

## The one-line loop
Drop the Elementor kit in `projects/<site>/current-theme/` and the content in
`new-content/` → **onboard the kit (generate the `<site>-*` skills) once, before
building any page** → build through those skills to `projects/<site>/output/` →
`python3 scripts/validate-page.py <page>.json` must pass → hand off for import.

See `AGENTS.md` for the full process, `README.md` for the master overview, and
`docs/Elementor-Site-Playbook.md` for the detailed playbook.
