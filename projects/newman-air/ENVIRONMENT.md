# Newman Air: local environment

| | |
|---|---|
| Local site | "Newman Air", `C:\Users\erick\Local Sites\newman-air` (Windows), domain `newman-air.local` |
| URL | <http://localhost:10028> |
| Ports (from `%APPDATA%\Local\sites.json`) | nginx 10028 · php-cgi 10026/10027 · **MySQL 10030** · Mailpit 10017/10025 |
| DB | `local`, prefix `wp_cv8f0uziyk_` |
| Stack (2026-10-20) | WordPress, Hello Elementor 3.5.1, Elementor 4.3.5, Pro Elements 4.3.0, Novamira 1.12.10, Classic Editor |
| Front page | page 15 `newman-air` (the splash), `show_on_front=page` |
| Media | 13 horizontal logo, 14 bear mark (Site Icon) |

## WP-CLI from an ordinary terminal

Local's bundled PHP has no php.ini next to it, so it starts **without mysqli** and
WordPress dies with "missing the MySQL extension". Run it with `-n` and load the
extensions by hand, and point mysqli at this site's MySQL port (`DB_HOST` is plain
`localhost`, which would otherwise hit another site's 3306):

```bash
PHPD="/c/Users/erick/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64"
W() { "$PHPD/php.exe" -n -d extension_dir="$PHPD/ext" -d extension=mysqli -d extension=openssl \
  -d extension=mbstring -d extension=curl -d extension=gd -d extension=zip -d extension=fileinfo \
  -d extension=exif -d mysqli.default_port=10030 -d memory_limit=512M \
  .wp-cli/wp-cli-2.11.0.phar --path="C:/Users/erick/Local Sites/newman-air/app/public" "$@"; }
W option get siteurl
```

The site must be started in Local.

## Importing the splash here

The logo is already in this Media Library, so build a local variant that points at it
(keep the committed `splash.json` portable), then import:

```bash
NEWMAN_LOGO_URL="http://localhost:10028/wp-content/uploads/2026/10/NewmanAirLogo_Horiz@72x.png" \
NEWMAN_LOGO_ID=13 python projects/newman-air/pages/splash/build.py
cp projects/newman-air/pages/splash/splash.json /tmp/splash-local.json
python projects/newman-air/pages/splash/build.py          # restore the portable file
W eval-file scripts/import-page.php /tmp/splash-local.json newman-air "Newman Air"
W elementor flush-css
```
