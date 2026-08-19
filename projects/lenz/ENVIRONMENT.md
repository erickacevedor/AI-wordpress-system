# Lenz — environment & access runbook

**As of 2026-08-18.** How to reach the Lenz WordPress install and how a built page
actually gets into it. Companion to:

- `STATUS.md` — what is built and what is not
- `KIT-ANALYSIS.md` — the design system and the *why*
- `pages/*/HANDOFF-notes.md` — per-page import detail
- `../../AGENTS.md` — the site-agnostic build loop

This file exists because the connection details are not guessable and one of them
is an outright trap. Everything below was verified against the running install,
not inferred.

---

## The install

| | |
|---|---|
| Host | Local (by WP Engine) |
| Site name | `lenz 2026` — Local site id `kLxSbGXKb` |
| Path | `C:\Users\erick\Local Sites\lenz-2026` |
| Web root | `<path>\app\public` |
| URL | <http://localhost:10010> · domain `lenz-2026.local` |
| Theme | `hello-elementor` |
| Plugins active | `elementor`, `pro-elements`, `lenz-core` |
| Front page | Page **23** (`show_on_front=page`, `page_on_front=23`) |

Local's own service registry is `%APPDATA%\Local\sites.json` — that is the
authoritative source for this site's ports if they ever change.

### Ports

| Service | Port |
|---|---|
| nginx (HTTP) | 10010 |
| PHP-CGI | 10008, 10009 |
| **MySQL** | **10017** |
| Mailpit web / SMTP | 10005 / 10007 |

---

## Database access

> **The trap.** `wp-config.php` says `DB_HOST = localhost`, and there *is* a
> mysqld listening on 3306 — but **that is a different Local site's**. Connecting
> to 3306 returns `ERROR 1049: Unknown database 'local'` and looks like the site is
> broken when it is fine. Local runs one mysqld per site; this one is on **10017**.

| | |
|---|---|
| Host / port | `127.0.0.1` : `10017` |
| Database | `local` |
| User / password | `root` / `root` (Local's dev defaults) |
| Table prefix | `wp_t62elvso08_` |

Local ships its own client — there is no global `mysql` on PATH:

```
C:\Users\erick\AppData\Roaming\Local\lightning-services\mysql-8.4.0\bin\win64\bin\mysql.exe
```

```bash
MYSQL="/c/Users/erick/AppData/Roaming/Local/lightning-services/mysql-8.4.0/bin/win64/bin/mysql.exe"
"$MYSQL" -h 127.0.0.1 -P 10017 -u root -proot -D local -e \
  "SELECT option_name, option_value FROM wp_t62elvso08_options
   WHERE option_name IN ('siteurl','page_on_front');"
```

The site must be **started in Local** for any of this to answer.

---

## WP-CLI

**Not installed** — there is no global `wp`, and Local does not bundle one. The
`wp eval-file` commands in `STATUS.md` and the handoff notes assume you are in
Local's own site shell (right-click the site → *Open site shell*), which puts a
`wp` on PATH for that session only.

To drive the loop from an ordinary terminal instead, pair the WP-CLI phar with
Local's bundled PHP:

```bash
PHP="/c/Users/erick/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64/php.exe"
curl -sL -o /tmp/wp-cli.phar \
  https://github.com/wp-cli/wp-cli/releases/download/v2.11.0/wp-cli-2.11.0.phar
"$PHP" /tmp/wp-cli.phar --path="/c/Users/erick/Local Sites/lenz-2026/app/public" option get siteurl
```

> **Corrected 2026-08-18.** This previously pointed at
> `raw.githubusercontent.com/wp-cli/wp-cli/v2.11.0/phar/wp-cli.phar`, which **404s**.
> The phar is a release asset, not a file in the repo. Worse, `curl -sL -o` happily
> writes the 14-byte "404: Not Found" body to the target, so the failure surfaces
> later as an incomprehensible wp-cli error. `scripts/sandbox.sh` now fetches the
> release asset and size-checks the download.

Pin the version rather than fetching `wp-cli.phar` from `latest` so a build is
reproducible. `--path` is required; without it WP-CLI cannot find the install.

`scripts/sandbox.sh` automates all of this (it finds Local's bundled php by itself);
this section remains as the manual recipe. Lenz keeps its own `tools/*.php` copies —
the promoted `scripts/import-page.php` differs deliberately in reading the page
template from the document instead of forcing `elementor_header_footer`, so migrate
Lenz to it only alongside a re-import and a check.

---

## How a page actually lands

Nothing is built in the Elementor UI. The page is generated as JSON and written
straight into post meta:

```
projects/lenz/pages/home/build.py          author the page in Python
    |                                      (helpers from scripts/elementor_builder.py,
    |                                       brand values from projects/lenz/tokens.json)
    v
projects/lenz/pages/home/home.json         single-page wrapper: { "content": [ ... ] }
    |
    v
scripts/validate-page.py home.json         MUST exit 0 before importing
    |
    v
wp eval-file projects/lenz/tools/import-page.php home.json home "Home"
    |
    v
page 23  ->  _elementor_data  (127 KB, 320 containers on the rendered page)
```

`tools/import-page.php` is the headless equivalent of *Templates → Import
Templates → Insert*. It is **idempotent** — matched by slug, so re-running updates
page 23 rather than creating duplicates. It writes four meta keys
(`_elementor_data`, `_elementor_edit_mode`, `_elementor_template_type`,
`_wp_page_template`) and clears Elementor's file cache.

> **The other trap**, already handled inside that script: `_elementor_data` must go
> through `wp_slash()`. `update_post_meta()` runs the value through `wp_unslash()`
> on the way in, so an unslashed JSON payload comes back mangled and Elementor
> renders a silently empty page.

Header and footer are separate Elementor **library templates** (ids 25 and 26),
imported by `tools/import-template.php`, applied site-wide. Global Colors live on
the Default Kit (id 5) and are set by `tools/set-globals.php`.

After **any** CSS change: `projects/lenz/deploy-plugin.sh`. Editing the plugin
inside `wp-content/plugins/` directly does not survive the next deploy — the repo
copy is the source of truth.

---

## Verifying a build

```bash
# renders, and Elementor actually emitted containers
curl -s -o /tmp/h.html -w '%{http_code}\n' http://localhost:10010/
grep -c 'e-con' /tmp/h.html          # expect ~320 for the current home page

# stored payload sizes
"$MYSQL" -h 127.0.0.1 -P 10017 -u root -proot -D local -e \
 "SELECT p.ID, p.post_title, ROUND(CHAR_LENGTH(m.meta_value)/1024,1) AS kb
  FROM wp_t62elvso08_posts p
  JOIN wp_t62elvso08_postmeta m ON m.post_id=p.ID AND m.meta_key='_elementor_data'
  WHERE p.post_status='publish';"

# deployed plugin matches the repo (line endings differ by design — see STATUS.md)
diff <(tr -d '\r' < projects/lenz/plugin/lenz-core/lenz-core.php) \
     <(tr -d '\r' < "/c/Users/erick/Local Sites/lenz-2026/app/public/wp-content/plugins/lenz-core/lenz-core.php")
```

Last verified 2026-08-18: HTTP 200, 181 KB, 320 containers, all 15 sections
present, `lenz-core.css` loading, all five plugin files byte-identical to the repo
after stripping `\r`.

---

## The install is not version-controlled

`C:\Users\erick\Local Sites\lenz-2026` is a **deployment target**, not a source of
truth. Anything hand-edited there — in the Elementor UI, in the plugin folder, in
the DB — is lost on the next `build.py` + import, and is invisible to git. Changes
belong in this repo, then get deployed.

A copy of this file is kept at the install's web root
(`app/public/LENZ-ENVIRONMENT.md`) purely as a signpost for anyone who opens the
site folder first; **the copy here is the one that is maintained.**
