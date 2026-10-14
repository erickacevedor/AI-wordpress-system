#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Deploy the canonical hvia-core plugin from this repo into a WordPress install.
# The REPO is the source of truth; the WP install is a deployment target.
#
#   ./deploy-plugin.sh                       # default: the HVIA Local site
#   HVIA_WP="/c/path/to/app/public" ./deploy-plugin.sh
# (Copied from projects/lenz/deploy-plugin.sh.)
# ---------------------------------------------------------------------------
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/plugin/hvia-core"
WP_ROOT="${HVIA_WP:-/c/Users/erick/Local Sites/hviahealthcom/app/public}"
DEST="$WP_ROOT/wp-content/plugins/hvia-core"

[ -f "$SRC/hvia-core.php" ]          || { echo "x source not found: $SRC"; exit 1; }
[ -d "$WP_ROOT/wp-content/plugins" ] || { echo "x not a WordPress root: $WP_ROOT"; exit 1; }

# Guard: only ever clear a directory that is demonstrably our own plugin.
if [ -e "$DEST" ]; then
  [ -f "$DEST/hvia-core.php" ] || { echo "x refusing to overwrite $DEST: not hvia-core"; exit 1; }
  rm -rf "$DEST"
fi
mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"
rm -rf "$DEST/assets/css/src"        # sources stay in the repo
echo "deployed hvia-core -> $DEST"
