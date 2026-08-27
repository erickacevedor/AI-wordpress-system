#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# WP-CLI against the Mid Lakes Local install, with the two traps from
# ENVIRONMENT.md already handled:
#
#   Trap 1  Local's bundled PHP loads no mysqli from its default ini, so plain
#           `php wp-cli.phar` dies with "missing the MySQL extension" and looks
#           like a broken WordPress. Local generates a per-site ini that loads
#           the extensions; -c points at it. The path carries the Local SITE ID
#           (CwXyblkvS), not the site name.
#
#   Trap 2  A php_imagick.dll startup warning prints on every call. It is
#           cosmetic; it is filtered out below.
#
# Usage:   ./wp.sh plugin list
#          ./wp.sh post list --post_type=page --fields=ID,post_name
#
# The site must be STARTED in Local for any of this to answer.
#
# Note: a few WP-CLI commands re-invoke php internally without -c (e.g. the
# implicit flush inside `wp rewrite structure`) and print the mysqli error even
# though the command succeeded. Run the follow-up explicitly and verify.
# ---------------------------------------------------------------------------
set -uo pipefail

PHP="${MIDLAKES_PHP:-/c/Users/erick/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64/php.exe}"
INI="${MIDLAKES_INI:-/c/Users/erick/AppData/Roaming/Local/run/CwXyblkvS/conf/php/php.ini}"
WP="${MIDLAKES_WPCLI:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/.wp-cli/wp-cli-2.11.0.phar}"
SITE="${MIDLAKES_WP:-C:/Users/erick/Local Sites/mid-lakes/app/public}"

[ -x "$PHP" ] || { echo "✗ Local's PHP not found: $PHP" >&2; exit 1; }
[ -f "$INI" ] || { echo "✗ per-site php.ini not found: $INI (is the site started in Local?)" >&2; exit 1; }
[ -f "$WP"  ] || { echo "✗ wp-cli phar not found: $WP" >&2; exit 1; }

"$PHP" -c "$INI" "$WP" --path="$SITE" "$@" 2>&1 | grep -v -i 'imagick'
exit "${PIPESTATUS[0]}"
