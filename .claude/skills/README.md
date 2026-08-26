# GENERATED — do not edit anything in here

`scripts/repackage-skills.sh` mirrors the portable skills from `skills/` into this
folder so Claude Code can invoke them as `/<name>`. **`skills/` is the source of
truth.** Edit there and re-run the script; anything changed here is overwritten on
the next run.

Per-site skills (`projects/<site>/skills/<site>-*`) are intentionally not mirrored —
they are contextual, and mirroring them all would load four clients' brand
instructions into every session. Read them from their own folder.
