#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Deploy the canonical lenz-core plugin from this repo into a WordPress install.
#
# The REPO is the source of truth; the WP install is a deployment target. Editing
# the plugin inside wp-content/plugins/ and expecting it to persist is the failure
# mode this script exists to prevent — the next deploy overwrites it.
#
#   ./deploy-plugin.sh                        # default Local site
#   LENZ_WP="/c/path/to/app/public" ./deploy-plugin.sh
# ---------------------------------------------------------------------------
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/plugin/lenz-core"
WP_ROOT="${LENZ_WP:-/c/Users/erick/Local Sites/lenz-2026/app/public}"
DEST="$WP_ROOT/wp-content/plugins/lenz-core"

[ -d "$SRC" ]                        || { echo "✗ source not found: $SRC"; exit 1; }
[ -f "$SRC/lenz-core.php" ]          || { echo "✗ $SRC is not the plugin (no lenz-core.php)"; exit 1; }
[ -d "$WP_ROOT/wp-content/plugins" ] || { echo "✗ not a WordPress root: $WP_ROOT"; exit 1; }

# Guard: only ever clear a directory that is demonstrably our own plugin.
if [ -e "$DEST" ]; then
  [ -f "$DEST/lenz-core.php" ] || { echo "✗ refusing to overwrite $DEST — not lenz-core"; exit 1; }
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"

echo "✔ deployed lenz-core -> $DEST"
find "$DEST" -type f | sed "s|$DEST|  |"
