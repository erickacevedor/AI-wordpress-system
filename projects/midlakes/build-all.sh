#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Rebuild every Mid Lakes page and theme part, gate each one, and (optionally)
# deploy the whole site to the Local install.
#
#   ./build-all.sh              # build + validate only
#   ./build-all.sh --deploy     # ...then deploy theme, import parts + pages, verify
#
# The gate is not optional: any page whose validate-page.py exits non-zero stops the
# run. Warnings are printed and counted but do not stop it, and on this site EVERY
# current warning is one of exactly two known, deliberate things:
#
#   1. the white-on-white band doubles on /about-us/ and /service-agreements/ — the
#      prototype ships them, and they are on the "do NOT fix" list;
#   2. the prototype's own hand-written SEO title/description running past 60/155
#      characters — existing content decisions, flagged rather than rewritten.
#
# Both are recorded in each page's HANDOFF-notes.md. A warning that is NOT one of
# those two is a real finding.
# ---------------------------------------------------------------------------
set -uo pipefail

SITE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SITE/../.." && pwd)"
# Resolve a python that actually RUNS. `command -v python3` is not enough on
# Windows: it finds the Microsoft Store app-execution stub, which is on PATH, is
# executable, and does nothing but print "Python was not found".
PY=""
for c in python3 python py; do
  p="$(command -v "$c" 2>/dev/null)" || continue
  "$p" -c "import sys" >/dev/null 2>&1 && { PY="$p"; break; }
done
[ -n "$PY" ] || { echo "✗ no working python on PATH (tried python3, python, py)" >&2; exit 1; }

DEPLOY=0
[ "${1:-}" = "--deploy" ] && DEPLOY=1

PARTS="header footer"
PAGES="home about-us services service-agreements service-area financing"

fail=0

echo "── build + gate ─────────────────────────────────────────────"
for p in $PARTS; do
  "$PY" "$SITE/pages/_theme/$p/build.py" >/dev/null || { echo "✗ build failed: $p"; fail=1; continue; }
  if "$PY" "$ROOT/scripts/validate-page.py" "$SITE/pages/_theme/$p/$p.json" >/dev/null 2>&1; then
    echo "  ✔ _theme/$p"
  else
    echo "  ✗ _theme/$p — GATE FAILED"; "$PY" "$ROOT/scripts/validate-page.py" "$SITE/pages/_theme/$p/$p.json"; fail=1
  fi
done

for p in $PAGES; do
  "$PY" "$SITE/pages/$p/build.py" >/dev/null || { echo "✗ build failed: $p"; fail=1; continue; }
  out="$("$PY" "$ROOT/scripts/validate-page.py" "$SITE/pages/$p/$p.json" 2>&1)"
  if [ $? -eq 0 ]; then
    warns="$(printf '%s' "$out" | grep -c '⚠︎' || true)"
    "$PY" "$ROOT/scripts/make-preview.py" "$SITE/pages/$p/$p.json" >/dev/null
    echo "  ✔ $p  ($warns warning(s))  → $p.json + PREVIEW.html"
  else
    echo "  ✗ $p — GATE FAILED"; printf '%s\n' "$out"; fail=1
  fi
done

[ "$fail" -eq 0 ] || { echo; echo "✗ one or more pages failed the gate — nothing deployed."; exit 1; }

if [ "$DEPLOY" -eq 0 ]; then
  echo; echo "✔ all built and gated. Re-run with --deploy to push to the install."
  exit 0
fi

echo
echo "── deploy ───────────────────────────────────────────────────"
"$SITE/deploy-theme.sh" >/dev/null && echo "  ✔ child theme"

W="$SITE/wp.sh"
for p in $PARTS; do
  "$W" eval-file "$ROOT/scripts/import-template.php" "$SITE/pages/_theme/$p/$p.json" \
    | sed 's/^/  /'
done

# Slug + title per page. The stubs already exist (pages 10-16) and import-page.php is
# idempotent by slug, so this updates them in place rather than creating duplicates.
import_page() { "$W" eval-file "$ROOT/scripts/import-page.php" "$SITE/pages/$1/$1.json" "$2" "$3" | sed 's/^/  /'; }
import_page home               home               "Home"
import_page about-us           about-us           "About"
import_page services           services           "Services"
import_page service-agreements service-agreements "Service Agreements"
import_page service-area       service-area       "Service Areas"
import_page financing          financing          "Financing"

"$W" elementor flush_css >/dev/null && echo "  ✔ Elementor CSS flushed"

echo
echo "── verify rendered ──────────────────────────────────────────"
BASE="${MIDLAKES_URL:-http://localhost:10015}"
verify() { "$PY" "$ROOT/scripts/verify-render.py" "$SITE/pages/$1/$1.json" "$BASE$2" 2>&1 | sed 's/^/  /'; }
verify home               /
verify about-us           /about-us/
verify services           /services/
verify service-agreements /service-agreements/
verify service-area       /service-area/
verify financing          /financing/
