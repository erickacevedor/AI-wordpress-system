#!/usr/bin/env bash
# Re-zip the PORTABLE skills into skills-zipped/ for Claude Desktop / Cowork upload.
# Run this whenever you edit skills/elementor-kit-onboarding or skills/full-output-enforcement,
# so the zips don't ship stale instructions.
#
# Uses `zip` where it exists, and falls back to Python's zipfile otherwise — Git Bash
# on Windows ships no `zip`, and a silent failure here means the zips quietly drift
# out of sync with skills/.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p skills-zipped

pack_with_python() {  # $1 = skill dir name
  python - "$1" <<'PY'
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

for skill in elementor-kit-onboarding full-output-enforcement; do
  if [ -d "skills/$skill" ]; then
    rm -f "skills-zipped/$skill.zip"
    if command -v zip >/dev/null 2>&1; then
      ( cd skills && zip -rq "../skills-zipped/$skill.zip" "$skill" -x '*/.DS_Store' )
    else
      pack_with_python "$skill"
    fi
    echo "repackaged skills-zipped/$skill.zip"
  else
    echo "WARN: skills/$skill not found" >&2
  fi
done
