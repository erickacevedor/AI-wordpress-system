# Mid Lakes — environment & access runbook

**As of 2026-08-27.** How to reach the Mid Lakes WordPress install and what is already
on it. Companion to `STATUS.md` (where the port is) and `PORT-DECISIONS.md` (what has
been settled and what is still open).

Everything below was verified against the running install, not inferred. Two details
are traps; both are called out.

---

## The install

| | |
|---|---|
| Host | Local (by WP Engine) |
| Site name | `Mid Lakes` — Local site id **`CwXyblkvS`** |
| Path | `C:\Users\erick\Local Sites\mid-lakes` |
| Web root | `<path>\app\public` |
| URL | <http://localhost:10015> — responding 200 · domain `mid-lakes.local` |
| WordPress | **7.1** |
| Theme | `hello-elementor` **3.5.1**, active. No child theme yet |
| Plugins active | `elementor` **4.2.3**, `elementor-pro` **4.2.2**, `classic-editor` 1.7.0 |
| Source design repo | `D:\laragon\www\midlakes` (remote `em-midlakes`) — `public/` is the prototype |

Local's own service registry is `%APPDATA%\Local\sites.json` — authoritative for this
site's ports if they ever change.

### Ports

| Service | Port |
|---|---|
| nginx (HTTP) | 10015 |
| PHP-CGI | 10013, 10014 |
| **MySQL** | **10019** |
| Mailpit web / SMTP | 10006 / 10011 |

---

## Database access

> **Trap 1 — the port.** `wp-config.php` says `DB_HOST = localhost`. Local runs one
> mysqld **per site**, and this one is on **10019**. Connecting to 3306 reaches a
> different site's server and looks like this install is broken when it is fine.
> (Lenz has the same trap on 10017.)

| | |
|---|---|
| Host / port | `127.0.0.1` : `10019` |
| Database | `local` |
| User / password | `root` / `root` |
| Table prefix | **`wp_9lyk2wofuv_`** |

Local ships its own client — there is no global `mysql` on PATH:

```bash
MYSQL="/c/Users/erick/AppData/Roaming/Local/lightning-services/mysql-8.4.0/bin/win64/bin/mysql.exe"
"$MYSQL" -h 127.0.0.1 -P 10019 -u root -proot -D local -e \
  "SELECT option_name, option_value FROM wp_9lyk2wofuv_options
   WHERE option_name IN ('siteurl','page_on_front','page_for_posts');"
```

The site must be **started in Local** for any of this to answer.

---

## WP-CLI — works, but needs one flag

There is no global `wp`. The phar is vendored in this repo at
`.wp-cli/wp-cli-2.11.0.phar`.

> **Trap 2 — mysqli.** Local's bundled PHP binary loads no `mysqli` from its default
> ini, so `wp` dies with *"Your PHP installation appears to be missing the MySQL
> extension"* and looks like a broken WordPress. It is not. Local generates a
> per-site ini that loads the extensions; pass it with `-c`.

```bash
PHP="/c/Users/erick/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64/php.exe"
INI="/c/Users/erick/AppData/Roaming/Local/run/CwXyblkvS/conf/php/php.ini"
WP="/d/laragon/www/AI-wordpress-system/.wp-cli/wp-cli-2.11.0.phar"
SITE="C:/Users/erick/Local Sites/mid-lakes/app/public"

w(){ "$PHP" -c "$INI" "$WP" --path="$SITE" "$@"; }
w plugin list
```

Notes:

- The ini path contains the **Local site id** (`CwXyblkvS`), not the site name.
- A `php_imagick.dll` startup warning prints on every call. It is **cosmetic** —
  filter it with `| grep -v imagick`.
- Some WP-CLI commands re-invoke php internally without `-c` (e.g. the implicit flush
  inside `wp rewrite structure`) and print the mysqli error even though the command
  succeeded. Run the follow-up explicitly (`w rewrite flush --hard`) and verify.
- `wp elementor flush_css` is available and is the right call after any CSS change.

---

## What is already on the site

Built 2026-08-27. Everything here is **wire-up**, not page content.

| Object | Id | State |
|---|---|---|
| Page **Home** | 10 | Published, empty · set as front page (`show_on_front=page`) |
| Page **About** | 11 | Published, empty · slug `about-us` |
| Page **Services** | 12 | Published, empty · slug `services` |
| Page **Service Agreements** | 13 | Published, empty · slug `service-agreements` |
| Page **Service Areas** | 14 | Published, empty · slug `service-area` |
| Page **Financing** | 15 | Published, empty · slug `financing` |
| Page **Blog** | 16 | Published, empty · set as **posts page** (`page_for_posts`) |
| Menu **Main Menu** | 3 | 7 items → location `menu-1` (Header) |
| Menu **Footer Menu** | 4 | 8 items → location `menu-2` (Footer) |
| Default Kit | 6 | **Untouched** — see below |

The seven page stubs exist so the menus can point at real objects.
`scripts/import-page.php` is **idempotent by slug**, so building a page updates the
stub in place rather than creating a duplicate. Do not renumber them.

Menu labels intentionally differ between header and footer, because the prototype
renders them that way: header says **About**, footer says **About Us**. The footer
also carries a custom `#contact` item — an on-page anchor, since the contact band
repeats on every page.

The header's `tel:` link is deliberately **not** a menu item. It is `.nav-phone`, a
styled button, and belongs in the header template.

**Permalinks** were plain `?page_id=`; set to `/%postname%/`, so all seven URLs now
match the prototype's paths exactly and return 200. (WP-CLI warns about `.htaccess`
— irrelevant, Local runs nginx.)

### The kit is stock, and that matters

Post 6 has **no `_elementor_page_settings`** — the Default Kit is untouched Hello
Elementor. Its Global Colors are still Hello's defaults, and Hello's Roboto /
Roboto Slab are what currently load.

**Consequence: style inline.** Pointing a widget at a global colour slot silently
produces off-brand output. This is the inversion the `html-prototype-onboarding`
skill warns about: keep the variables in the prototype's stylesheet, resolve them to
real values in `tokens.json`, and let the builder write those values into the page.

### Left alone (cleanup candidates, harmless)

`Sample Page` (2), the `Hello world!` post (1), the `Privacy Policy` draft (3), and an
orphan `Elementor #7` draft (7).

---

## The install is not version-controlled

`C:\Users\erick\Local Sites\mid-lakes` is a **deployment target**. Anything
hand-edited there — in the Elementor UI, in the child theme folder, in the DB — is
lost on the next build + import and is invisible to git. Changes belong in this repo,
then get deployed.
