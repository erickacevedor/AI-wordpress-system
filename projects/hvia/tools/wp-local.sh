#!/usr/bin/env bash
# wp-cli against the HVIA Local site (Windows, Local by Flywheel, site id XV3Ie38mP).
# The extension_dir override is required: Local's php.ini points at a folder with no
# DLLs, so without it wp-cli fails with "missing the MySQL extension".
# Local must be running the site (it answers at http://localhost:10022).
LP="$LOCALAPPDATA/Programs/Local/resources/extraResources"
PHPDIR="$LP/lightning-services/php-8.2.29+0/bin/win32"
exec "$PHPDIR/php.exe" -c "$APPDATA/Local/run/XV3Ie38mP/conf/php/php.ini" -d extension_dir="$PHPDIR/ext" \
  -d display_errors=stderr "$LP/bin/wp-cli/wp-cli.phar" --path="C:/Users/erick/Local Sites/hviahealthcom/app/public" "$@" 2> >(grep -v -i "xdebug\|imagick" >&2)
