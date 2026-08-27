#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Deploy the canonical mid-lakes child theme from this repo into a WordPress
# install.
#
# The REPO is the source of truth; the WP install is a deployment target.
# Editing the theme inside wp-content/themes/ and expecting it to persist is the
# failure mode this script exists to prevent — the next deploy overwrites it.
#
#   ./deploy-theme.sh                          # default Local site
#   MIDLAKES_WP="/c/path/to/app/public" ./deploy-theme.sh
# ---------------------------------------------------------------------------
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/theme/mid-lakes"
WP_ROOT="${MIDLAKES_WP:-/c/Users/erick/Local Sites/mid-lakes/app/public}"
DEST="$WP_ROOT/wp-content/themes/mid-lakes"

[ -d "$SRC" ]                       || { echo "✗ source not found: $SRC"; exit 1; }
[ -f "$SRC/style.css" ]             || { echo "✗ $SRC is not the theme (no style.css)"; exit 1; }
grep -q '^Template: *hello-elementor' "$SRC/style.css" \
                                    || { echo "✗ $SRC/style.css does not declare Template: hello-elementor"; exit 1; }
[ -d "$WP_ROOT/wp-content/themes" ] || { echo "✗ not a WordPress root: $WP_ROOT"; exit 1; }
[ -d "$WP_ROOT/wp-content/themes/hello-elementor" ] \
                                    || { echo "✗ parent theme hello-elementor is not installed at $WP_ROOT"; exit 1; }

# Guard: only ever clear a directory that is demonstrably our own theme.
if [ -e "$DEST" ]; then
  grep -q '^Theme Name: *Mid Lakes' "$DEST/style.css" 2>/dev/null \
    || { echo "✗ refusing to overwrite $DEST — not the Mid Lakes child theme"; exit 1; }
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"

echo "✔ deployed mid-lakes -> $DEST"
find "$DEST" -type f | sed "s|$DEST|  |"
echo
echo "Next: activate it and flush Elementor's CSS —"
echo "  wp theme activate mid-lakes"
echo "  wp elementor flush_css"
