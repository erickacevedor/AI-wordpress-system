# Newman Air: local environment

| | |
|---|---|
| Local site | "Newman Air", `C:\Users\erick\Local Sites\newman-air` (Windows), domain `newman-air.local` |
| URL | <http://localhost:10028> |
| Ports (from `%APPDATA%\Local\sites.json`) | nginx 10028 · php-cgi 10026/10027 · **MySQL 10031** (was 10030 until the 2026-10-22 pull from Flywheel; re-read `sites.json` if WP-CLI cannot connect) · Mailpit 10017/10025 |
| DB | `local`, prefix `wp_cv8f0uziyk_` |
| Stack (2026-10-20) | WordPress, Hello Elementor 3.5.1, Elementor 4.3.5, Pro Elements 4.3.0, Novamira 1.12.10, Classic Editor |
| Front page | page 15 `newman-air` (the splash), `show_on_front=page` |
| Media | 13 horizontal logo, 14 bear mark (Site Icon) |
| V2.1 build (2026-10-23) | page 37 `/home/` (not front page), header template 38, footer template 39 (both conditioned to page 37), plugin newman-core active. See `pages/home/HANDOFF-notes.md` |
| Inner pages (2026-10-23) | 34 pages: hubs 41/42, services, cities, About 43, Contact 70, Financing 68, Maintenance Plan 69, legal and utility pages; header/footer conditioned to every `_newman_core` page. See `pages/inner/HANDOFF-notes.md`. DB backup before the import: `C:\Users\erick\Local Sites\newman-air\backups\2026-10-23-before-inner-pages.sql` |
| Not ours, do not touch | Esteban's Scheduled Promos plugin, promos 27/28, page 29 Promo Landing, page 30 `best-in-show-is-now-newman-air`, Header Footer Code Manager |

## WP-CLI from an ordinary terminal

Local's bundled PHP has no php.ini next to it, so it starts **without mysqli** and
WordPress dies with "missing the MySQL extension". Run it with `-n` and load the
extensions by hand, and point mysqli at this site's MySQL port (`DB_HOST` is plain
`localhost`, which would otherwise hit another site's 3306):

```bash
PHPD="/c/Users/erick/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64"
W() { "$PHPD/php.exe" -n -d extension_dir="$PHPD/ext" -d extension=mysqli -d extension=openssl \
  -d extension=mbstring -d extension=curl -d extension=gd -d extension=zip -d extension=fileinfo \
  -d extension=exif -d mysqli.default_port=10031 -d memory_limit=512M \
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
