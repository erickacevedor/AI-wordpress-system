#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Lenz v6-1: build every part, gate it, port the CSS, and (optionally) push it
# into a LOCAL WordPress install.
#
#   ./build-all.sh                   build + validate + port only
#   LENZ_WP_CLI="/path/to/wp-wrapper" LENZ_WP="/path/to/app/public" ./build-all.sh --import
#
# LENZ_WP_CLI is any command that behaves like `wp` against the install (Local's
# php + wp-cli.phar; see the client's site.md). Never point this at a live site:
# the import overwrites page 23 and templates 25/26.
# ---------------------------------------------------------------------------
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"

PAGES=$(cd "$HERE/pages" && ls -d */ | tr -d / | grep -v '^_')     # every page folder
for p in $PAGES; do python3 "$HERE/pages/$p/build.py" >/dev/null; done
python3 "$HERE/pages/_theme/build-templates.py" >/dev/null
for f in $(for p in $PAGES; do echo "pages/$p/$p.json"; done) pages/_theme/header.json pages/_theme/footer.json; do
  printf '%-48s ' "$f"; python3 "$ROOT/scripts/validate-page.py" "$HERE/$f" | tail -1 | cut -c1-40
done
python3 "$HERE/tools/port-css.py"

if [ "${1:-}" = "--import" ]; then
  : "${LENZ_WP_CLI:?set LENZ_WP_CLI to a wp command for the local install}"
  : "${LENZ_WP:?set LENZ_WP to the app/public folder of the local install}"
  LENZ_WP="$LENZ_WP" bash "$HERE/deploy-plugin.sh" >/dev/null && echo "deployed lenz-core"
  for p in $PAGES; do
    title=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "$HERE/pages/$p/$p.json")
    "$LENZ_WP_CLI" eval-file "$HERE/tools/import-page.php" "$HERE/pages/$p/$p.json" "$p" "$title" | head -1
  done
  "$LENZ_WP_CLI" eval-file "$HERE/tools/import-template.php" "$HERE/pages/_theme/header.json" lenz-header | head -1
  "$LENZ_WP_CLI" eval-file "$HERE/tools/import-template.php" "$HERE/pages/_theme/footer.json" lenz-footer | head -1
  "$LENZ_WP_CLI" elementor flush-css >/dev/null && echo "flushed Elementor CSS"
fi
