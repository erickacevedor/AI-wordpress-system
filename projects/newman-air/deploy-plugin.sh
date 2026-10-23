#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Deploy the canonical newman-core plugin from this repo into a WordPress install.
#
# The REPO is the source of truth; the WP install is a deployment target. Editing
# the plugin inside wp-content/plugins/ and expecting it to persist is the failure
# mode this script exists to prevent — the next deploy overwrites it.
#
#   ./deploy-plugin.sh                        # default Local site
#   NEWMAN_WP="/c/path/to/app/public" ./deploy-plugin.sh
# ---------------------------------------------------------------------------
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/plugin/newman-core"
WP_ROOT="${NEWMAN_WP:-/c/Users/erick/Local Sites/newman-air/app/public}"
DEST="$WP_ROOT/wp-content/plugins/newman-core"

[ -d "$SRC" ]                        || { echo "✗ source not found: $SRC"; exit 1; }
[ -f "$SRC/newman-core.php" ]          || { echo "✗ $SRC is not the plugin (no newman-core.php)"; exit 1; }
[ -d "$WP_ROOT/wp-content/plugins" ] || { echo "✗ not a WordPress root: $WP_ROOT"; exit 1; }

# Guard: only ever clear a directory that is demonstrably our own plugin.
if [ -e "$DEST" ]; then
  [ -f "$DEST/newman-core.php" ] || { echo "✗ refusing to overwrite $DEST — not newman-core"; exit 1; }
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"

echo "✔ deployed newman-core -> $DEST"
find "$DEST" -type f | sed "s|$DEST|  |"
