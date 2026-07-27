#!/usr/bin/env bash
# Re-zip the PORTABLE skills into skills-zipped/ for Claude Desktop / Cowork upload.
# Run this whenever you edit skills/elementor-kit-onboarding or skills/full-output-enforcement,
# so the zips don't ship stale instructions.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p skills-zipped
for skill in elementor-kit-onboarding full-output-enforcement; do
  if [ -d "skills/$skill" ]; then
    rm -f "skills-zipped/$skill.zip"
    ( cd skills && zip -rq "../skills-zipped/$skill.zip" "$skill" -x '*/.DS_Store' )
    echo "repackaged skills-zipped/$skill.zip"
  else
    echo "WARN: skills/$skill not found" >&2
  fi
done
