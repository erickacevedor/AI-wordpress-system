#!/usr/bin/env bash
# Local verification sandbox: import a built page into a throwaway WordPress and
# check what Elementor actually rendered.
#
# WHY: the deliverable is a JSON file that somebody else imports, usually onto a host
# nobody here can reach. There is no second try. So the render has to be confirmed
# BEFORE handoff -- on a local install kept purely for that purpose, not on the
# client's site.
#
# This is a thin, explicit wrapper: no auto-discovery, no magic. It expects you to say
# where the sandbox is, because guessing wrong would write into a real site.
#
#   SANDBOX_WP    path to the WordPress install (the folder holding wp-config.php)
#   SANDBOX_URL   the URL it serves          (e.g. http://localhost:10010)
#   SANDBOX_PHP   php binary                 (optional; see the notes below)
#
# Usage:
#   scripts/sandbox.sh check
#   scripts/sandbox.sh import projects/<site>/pages/<slug>/<slug>.json [slug]
#   scripts/sandbox.sh template projects/<site>/pages/_theme/header.json
#   scripts/sandbox.sh verify projects/<site>/pages/<slug>/<slug>.json [slug]
#   scripts/sandbox.sh page    projects/<site>/pages/<slug>/<slug>.json [slug]   # import + verify
#
# NOTES ON PHP AND WP-CLI (verified on this machine, see projects/lenz/ENVIRONMENT.md):
#   - Local (by WP Engine) ships neither `wp` nor a php on PATH. Its bundled php lives
#     under %APPDATA%\Local\lightning-services\php-<ver>\bin\win64\php.exe
#   - Laragon's php is under D:\laragon\bin\php\php-<ver>\php.exe
#   - wp-cli is fetched as a pinned phar into .wp-cli/ (gitignored) so a run is
#     reproducible; `latest` would silently change under you.
set -euo pipefail
cd "$(dirname "$0")/.."

WP_CLI_VERSION="2.11.0"
CLI_DIR=".wp-cli"
CLI_PHAR="$CLI_DIR/wp-cli-$WP_CLI_VERSION.phar"

die() { echo "✗ $*" >&2; exit 1; }

find_php() {
  if [ -n "${SANDBOX_PHP:-}" ]; then echo "$SANDBOX_PHP"; return; fi
  if command -v php >/dev/null 2>&1; then command -v php; return; fi
  for p in \
    "$APPDATA/Local/lightning-services"/php-*/bin/win64/php.exe \
    /c/Users/*/AppData/Roaming/Local/lightning-services/php-*/bin/win64/php.exe \
    /d/laragon/bin/php/php-*/php.exe \
    /c/laragon/bin/php/php-*/php.exe ; do
    [ -x "$p" ] && { echo "$p"; return; }
  done
  die "no php found — set SANDBOX_PHP to a php binary"
}

ensure_cli() {
  mkdir -p "$CLI_DIR"
  if [ ! -f "$CLI_PHAR" ]; then
    echo "· fetching wp-cli $WP_CLI_VERSION (pinned)"
    # From the RELEASE asset. The raw.githubusercontent path that
    # projects/lenz/ENVIRONMENT.md documents 404s, and curl cheerfully writes the
    # 14-byte "404: Not Found" body to the target, which then fails later as a
    # baffling wp-cli error. Hence the size/shebang check below.
    curl -sL -o "$CLI_PHAR" \
      "https://github.com/wp-cli/wp-cli/releases/download/v$WP_CLI_VERSION/wp-cli-$WP_CLI_VERSION.phar" \
      || die "could not download wp-cli"
    if [ "$(head -c 2 "$CLI_PHAR")" != "#!" ] || [ "$(wc -c < "$CLI_PHAR")" -lt 1000000 ]; then
      rm -f "$CLI_PHAR"
      die "the wp-cli download was not a phar (a server error page?) — retry, or drop one at $CLI_PHAR"
    fi
  fi
}

wp() {
  "$PHP" "$CLI_PHAR" --path="$SANDBOX_WP" "$@"
}

require_env() {
  [ -n "${SANDBOX_WP:-}" ] || die "set SANDBOX_WP to the WordPress install path"
  [ -f "$SANDBOX_WP/wp-config.php" ] || die "no wp-config.php in $SANDBOX_WP"
  [ -n "${SANDBOX_URL:-}" ] || die "set SANDBOX_URL to the sandbox's URL"
}

slug_of() {  # derive a slug from the json filename
  basename "$1" .json
}

cmd="${1:-}"; shift || true
PHP="$(find_php)"

case "$cmd" in
  check)
    echo "php:      $PHP"
    "$PHP" -v | head -1 | sed 's/^/          /'
    require_env
    ensure_cli
    echo "wp:       $CLI_PHAR"
    echo "install:  $SANDBOX_WP"
    wp core version 2>/dev/null | sed 's/^/          WordPress /' || die "wp-cli cannot read the install (is it running?)"
    echo "plugins:"
    wp plugin list --status=active --field=name 2>/dev/null | sed 's/^/          /' || true
    echo "url:      $SANDBOX_URL"
    curl -s -o /dev/null -w "          HTTP %{http_code}\n" --max-time 8 "$SANDBOX_URL" \
      || echo "          (not responding — start the sandbox)"
    ;;

  import)
    require_env; ensure_cli
    json="${1:?need a page json}"; slug="${2:-$(slug_of "$json")}"
    python scripts/validate-page.py "$json" >/dev/null \
      || die "the gate rejects $json — fix that before importing"
    wp eval-file scripts/import-page.php "$json" "$slug" "" ""
    ;;

  template)
    require_env; ensure_cli
    json="${1:?need a template json}"
    python scripts/validate-page.py "$json" >/dev/null \
      || die "the gate rejects $json — fix that before importing"
    wp eval-file scripts/import-template.php "$json"
    ;;

  verify)
    require_env
    json="${1:?need a page json}"; slug="${2:-$(slug_of "$json")}"
    python scripts/verify-render.py "$json" "$SANDBOX_URL/$slug/"
    ;;

  page)
    "$0" import "$@"
    json="${1:?}"; slug="${2:-$(slug_of "$json")}"
    echo "· re-fetching to verify the render"
    "$0" verify "$json" "$slug"
    ;;

  *)
    sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
    exit 2
    ;;
esac
