#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# HVIA: build every part, gate it, port the CSS, and (optionally) push it into a
# LOCAL WordPress install. Copied from projects/lenz/build-all.sh.
#
#   ./build-all.sh             build + validate + port only
#   ./build-all.sh --import    also deploy hvia-core, Rank Math, media, page, templates and
#                              site settings (tools/site-setup.php) into the Local site
#
# HVIA_WP_CLI defaults to tools/wp-local.sh (the Windows Local site, see the
# client's site.md). Never point this at a live site: the import overwrites the
# `home` page and the hvia-header / hvia-footer templates.
# ---------------------------------------------------------------------------
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PY="${PYTHON:-python}"
WP="${HVIA_WP_CLI:-$HERE/tools/wp-local.sh}"
win() { cygpath -m "$1" 2>/dev/null || echo "$1"; }   # PHP on Windows needs C:/... paths

PAGES=$(cd "$HERE/pages" && ls -d */ | tr -d / | grep -v '^_')
for p in $PAGES; do "$PY" "$HERE/pages/$p/build.py" >/dev/null; done
"$PY" "$HERE/pages/_theme/build-templates.py" >/dev/null
for f in $(for p in $PAGES; do echo "pages/$p/$p.json"; done) pages/_theme/header.json pages/_theme/footer.json; do
  printf '%-32s ' "$f"; "$PY" "$ROOT/scripts/validate-page.py" "$HERE/$f" | tail -1 | cut -c1-60
done
"$PY" "$HERE/tools/port-css.py"

if [ "${1:-}" = "--import" ]; then
  bash "$HERE/deploy-plugin.sh"
  "$WP" plugin activate hvia-core >/dev/null && echo "hvia-core active"
  "$WP" plugin is-installed seo-by-rank-math || "$WP" plugin install seo-by-rank-math >/dev/null
  "$WP" plugin activate seo-by-rank-math >/dev/null 2>&1; echo "rank math active"
  "$WP" eval-file "$(win "$HERE/tools/upload-media.php")" "$(win "$HERE/media")" "$(win "$HERE/media.json")" | tail -1
  for p in $PAGES; do
    title=$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "$HERE/pages/$p/$p.json")
    "$WP" eval-file "$(win "$HERE/tools/import-page.php")" "$(win "$HERE/pages/$p/$p.json")" "$p" "$title" | head -1
  done
  "$WP" eval-file "$(win "$HERE/tools/import-template.php")" "$(win "$HERE/pages/_theme/header.json")" hvia-header | head -1
  "$WP" eval-file "$(win "$HERE/tools/import-template.php")" "$(win "$HERE/pages/_theme/footer.json")" hvia-footer | head -1
  "$WP" eval-file "$(win "$HERE/tools/site-setup.php")" | tail -1
  "$WP" elementor flush-css >/dev/null && echo "flushed Elementor CSS"
fi
