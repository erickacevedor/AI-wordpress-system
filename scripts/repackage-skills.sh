#!/usr/bin/env bash
# Re-zip the PORTABLE skills into skills-zipped/ for Claude Desktop / Cowork upload.
# Run this whenever you edit anything under skills/, so the zips don't ship stale
# instructions. Keep the skill list below in step with the folders in skills/ —
# a portable skill that is not listed here silently never reaches Claude Desktop.
#
# Uses `zip` where it exists, and falls back to Python's zipfile otherwise — Git Bash
# on Windows ships no `zip`, and a silent failure here means the zips quietly drift
# out of sync with skills/.
set -euo pipefail
cd "$(dirname "$0")/.."

# Resolve the interpreter once. Git Bash on Windows ships `python`; macOS and most
# Linux ship `python3` and often no `python` at all -- hardcoding either one makes the
# script fail on the other half of the machines this repo is used from.
PY_BIN="$(command -v python3 || command -v python || true)"
[ -n "$PY_BIN" ] || { echo "ERROR: no python3/python on PATH" >&2; exit 1; }

mkdir -p skills-zipped

pack_with_python() {  # $1 = skill dir name
  "$PY_BIN" - "$1" <<'PY'
import os, sys, zipfile
skill = sys.argv[1]
out = os.path.join("skills-zipped", skill + ".zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(os.path.join("skills", skill)):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if f == ".DS_Store":
                continue
            full = os.path.join(root, f)
            # store paths relative to skills/, matching the `zip` invocation below
            z.write(full, os.path.relpath(full, "skills").replace(os.sep, "/"))
PY
}

for skill in elementor-kit-onboarding html-prototype-onboarding full-output-enforcement; do
  if [ -d "skills/$skill" ]; then
    rm -f "skills-zipped/$skill.zip"
    if command -v zip >/dev/null 2>&1; then
      # -D omits directory entries, so this produces a byte-identical archive to
      # the pack_with_python fallback. Without it the two paths differ by the dir
      # entries alone, and every zip churns in git whenever the machine running
      # this script has a different toolchain than the last one.
      ( cd skills && zip -rqD "../skills-zipped/$skill.zip" "$skill" -x '*/.DS_Store' )
    else
      pack_with_python "$skill"
    fi
    echo "repackaged skills-zipped/$skill.zip"
  else
    echo "WARN: skills/$skill not found" >&2
  fi
done

# ---------------------------------------------------------------------------
# Mirror the same portable skills into .claude/skills/ so Claude Code can invoke
# them as /<name>. Without this they are only ever *read* because AGENTS.md points
# at them -- discoverable to a human, invisible to the Skill tool.
#
# `skills/` stays the single source of truth. This is a one-way copy, and it
# deletes each destination first so a skill renamed or a file removed upstream
# does not linger. A copy rather than a symlink on purpose: this repo is used from
# Windows too, where symlinks committed to git need developer mode to survive.
#
# The per-site skills (projects/<site>/skills/<site>-*) are deliberately NOT
# mirrored. They are contextual -- mirroring all of them would put four clients'
# brand instructions in every session.
# ---------------------------------------------------------------------------
sync_claude_skills() {
  "$PY_BIN" - "$@" <<'PY'
import os, shutil, sys

dest_root = os.path.join(".claude", "skills")
os.makedirs(dest_root, exist_ok=True)
for skill in sys.argv[1:]:
    src = os.path.join("skills", skill)
    if not os.path.isdir(src):
        print("WARN: skills/%s not found" % skill, file=sys.stderr)
        continue
    dest = os.path.join(dest_root, skill)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest,
                    ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    print("mirrored .claude/skills/%s" % skill)
PY
}

sync_claude_skills elementor-kit-onboarding html-prototype-onboarding full-output-enforcement

cat > .claude/skills/README.md <<'EOF'
# GENERATED — do not edit anything in here

`scripts/repackage-skills.sh` mirrors the portable skills from `skills/` into this
folder so Claude Code can invoke them as `/<name>`. **`skills/` is the source of
truth.** Edit there and re-run the script; anything changed here is overwritten on
the next run.

Per-site skills (`projects/<site>/skills/<site>-*`) are intentionally not mirrored —
they are contextual, and mirroring them all would load four clients' brand
instructions into every session. Read them from their own folder.
EOF
echo "wrote .claude/skills/README.md"
