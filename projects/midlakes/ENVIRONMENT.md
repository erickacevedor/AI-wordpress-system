# Mid Lakes — environment & access runbook

**As of 2026-08-27, after the build.** How to reach the Mid Lakes WordPress install
and what is on it. Companion to `STATUS.md` (where the port is) and `PORT-DECISIONS.md` (what has
been settled and what is still open).

Everything below was verified against the running install, not inferred. Three
details are traps; all three are called out.

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
| Theme | **`mid-lakes`** (child of `hello-elementor` **3.5.1**), active — deployed from `projects/midlakes/theme/` by `deploy-theme.sh` |
| Plugins active | `elementor` **4.2.3**, **`pro-elements` 4.2.2**, `classic-editor` 1.7.0 |

> **The Pro widgets currently come from PRO Elements, and that is temporary** —
> confirmed 2026-08-27, an official Elementor Pro account is being upgraded to.
>
> Nothing in this build depends on which one is installed: PRO Elements is the
> open-source drop-in, and every widget name and settings key used here (`form`,
> `nav-menu`, `google_maps`, `nested-accordion`, Theme Builder) is identical, so the
> JSON imports and renders the same on either.
>
> **At the swap:** the two plugins cannot both be active — PRO Elements *replaces*
> Elementor Pro, it does not sit alongside it. Deactivate PRO Elements first, then
> activate Elementor Pro, then `wp elementor flush_css`. The theme templates (49, 50),
> the form and every page keep working, because they are stored as ordinary widget
> types in post meta and neither plugin owns that data.
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

**This is now wrapped: use `projects/midlakes/wp.sh`.** It applies the `-c` flag,
filters the imagick noise, and fails with a useful message if the site is not started.

```bash
projects/midlakes/wp.sh plugin list
projects/midlakes/wp.sh post list --post_type=page --fields=ID,post_name
```

What it does under the hood, if you need it by hand:

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

Built 2026-08-27. The wire-up came first; the **site is now built on top of it**.

| Object | Id | State |
|---|---|---|
| Page **Home** | 10 | **Built** · front page (`show_on_front=page`) |
| Page **About** | 11 | **Built** · slug `about-us` |
| Page **Services** | 12 | **Built** · slug `services` |
| Page **Service Agreements** | 13 | **Built** · slug `service-agreements` |
| Page **Service Areas** | 14 | **Built** · slug `service-area` |
| Page **Financing** | 15 | **Built** · slug `financing` |
| Page **Blog** | 16 | Published, **still empty** · set as **posts page** (`page_for_posts`). Needs an archive template, not a page |
| Menu **Main Menu** | 3 | 7 items → location `menu-1` (Header) |
| Menu **Footer Menu** | 4 | 8 items → location `menu-2` (Footer) |
| Default Kit | 6 | Typography set to Manrope; **Global Colors still stock** — see below |
| Template **Mid Lakes Header** | 49 | `elementor_library`, type `header`, condition *Entire Site* |
| Template **Mid Lakes Footer** | 50 | `elementor_library`, type `footer`, condition *Entire Site* |
| Attachments **34–38** | | `hero-hvac`, `technician`, `ductwork`, `wall-units`, `vents` — alt text set. Mapped in `media.json` |

The seven page stubs exist so the menus can point at real objects.
`scripts/import-page.php` is **idempotent by slug**, so building a page updates the
stub in place rather than creating a duplicate. Do not renumber them.

**Pages 10–15 now hold the six built pages.** Page 16 (Blog) is still the posts
page and still has no archive template — see `STATUS.md`.

Menu labels intentionally differ between header and footer, because the prototype
renders them that way: header says **About**, footer says **About Us**. The footer
also carries a custom `#contact` item — an on-page anchor, since the contact band
repeats on every page.

The header's `tel:` link is deliberately **not** a menu item. It is `.nav-phone`, a
styled button, and belongs in the header template.

**Permalinks** were plain `?page_id=`; set to `/%postname%/`, so all seven URLs now
match the prototype's paths exactly and return 200. (WP-CLI warns about `.htaccess`
— irrelevant, Local runs nginx.)

### The kit: fonts are set, COLOURS ARE STILL STOCK

Post 6 started with **no `_elementor_page_settings` at all**. Three settings were
added, by `tools/set-kit-defaults.php` (idempotent, re-runnable):

| Setting | Value | Why |
|---|---|---|
| `system_typography` + `body_typography_*` | **Manrope** | The kit's built-in default was Roboto / Roboto Slab, so everything that INHERITS — Pro form fields, accordion body copy, list items, any text widget added later — rendered in the wrong face, and every page paid for two unwanted Google Fonts requests. Base typography is exactly what the kit is for |
| `container_width` | **1200px** | `--container`. `build.py` sets `boxed_width` explicitly on every section, so this is for the editor and for anything added by hand |
| `active_breakpoints` + `viewport_tablet_extra` | **1200px** | Where the prototype collapses the primary nav to a burger. Elementor ships only mobile (767) and tablet (1024) active, and the Nav Menu widget's Breakpoint dropdown is populated from whatever is ACTIVE, so without this the nav could only collapse at 1024 |
| `viewport_laptop` | **1400px** | The step BEFORE the collapse. `styles.css` does not go straight from a full nav to a burger — at 1400 it first TIGHTENS (gap 28→18, font 0.95→0.9rem), because seven links plus the phone stop fitting comfortably well above the point where they stop fitting at all. Elementor's laptop default is 1366, so it is set explicitly |

The site's breakpoint ladder therefore mirrors the prototype's own:
**mobile 767 · tablet 1024 · tablet_extra 1200 · laptop 1400.** All four are additive —
existing `_tablet` / `_mobile` values are unaffected.

> **`system_colors` was deliberately NOT set, and this still matters.**
>
> Every colour stays **inline** in `build.py`. Pointing a widget at a global colour
> slot would resolve to Hello Elementor's default and silently produce off-brand
> output. Splitting colour between a kit slot and inline values would also create two
> sources of truth for the one thing this port most needs to get exactly right.
>
> So the rule is: **fonts come from the kit, colours are written into the page.**

The child theme also filters `elementor/frontend/print_google_fonts` to `false`,
because it already enqueues both families at the exact axes the prototype uses —
otherwise Elementor adds a second Manrope request at every weight and every italic.

### The child theme is a CAP, not a stylesheet

`wp-content/themes/mid-lakes/` carries only properties Elementor has no control for:
the `clamp()` heads, Fraunces on its variable `opsz` axis, the button and card hover
transforms, the two three-stop photo overlays, the six watermark pseudo-elements, the
rate table, the `:focus-visible` rings, and the header's `backdrop-filter`.

It is deployed **from this repo** by `deploy-theme.sh`. Editing it inside
`wp-content/themes/` is lost on the next deploy.

### Trap 3 — the Theme Builder conditions cache

*(Fixed in `scripts/import-template.php`; recorded because the symptom is baffling.)*

The **first** import of a header or footer used to produce a template that was
created, published, had the right type meta, the right taxonomy term and the right
conditions — **and never rendered**.

`wp_insert_post()` fires `save_post`, something on that hook asks Elementor's
Documents_Manager for a document for the brand-new id, and at that instant
`_elementor_template_type` has not been written yet — so it resolves
`elementor_library` through the post-type map to a **Loop** document and caches that
instance against the id. `Conditions_Cache::regenerate()` then gets the cached Loop
back, asks it for `get_location()`, receives `''`, and skips the template.

The fix is one line — re-resolve the document with `$from_cache = false` before
regenerating. Clearing the post/term object caches does **not** help: the stale thing
is the document object, not the post row.

The tell, if it ever regresses: importing any *second* part fixes the first one by
accident, because by then the bad instance is gone with the request.

### Left alone (cleanup candidates, harmless)

`Sample Page` (2), the `Hello world!` post (1), the `Privacy Policy` draft (3), and an
orphan `Elementor #7` draft (7).

---

## The install is not version-controlled

`C:\Users\erick\Local Sites\mid-lakes` is a **deployment target**. Anything
hand-edited there — in the Elementor UI, in the child theme folder, in the DB — is
lost on the next build + import and is invisible to git. Changes belong in this repo,
then get deployed.
