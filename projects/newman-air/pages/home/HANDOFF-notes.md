# Newman Air: Home (V2.1) handoff

**Status (2026-10-23):** built from the V2.1 prototype (`design-source/v2-1/`) and imported on the
Windows Local copy `newman-air` as page 37 `/home/`, with Theme Builder header 38 and footer 39.
The splash (page 15) is still the front page; nothing is on Flywheel yet.

Verified against the prototype with headless Chrome at 1440, 1024, 768 and 390: every section has
the same top and height as the prototype (1px or less), and the form card, polaroids, member card,
marquee, map, final bear and mobile drawer match in position and size. Form submission tested:
the email reaches Mailpit addressed to dispatch@newmanair.com.

## SEO (set in the SEO plugin; Elementor JSON cannot carry these)

Not defined yet: no meta title or description in the homepage doc. Slug `/home/` is temporary;
at launch this page becomes the front page.

## How it is built

Same method as Lenz v6-1. `brand.py` mirrors the prototype DOM and class names;
`tools/port-css.py` ports the prototype stylesheet (read from `design-source/v2-1/index.html`)
into `plugin/newman-core/assets/css/newman-core.css`, after `src/adapter.css` and before
`src/overrides.css`. Rebuild:

```bash
python projects/newman-air/pages/home/build.py
python projects/newman-air/pages/_theme/build-templates.py
python scripts/validate-page.py projects/newman-air/pages/home/home.json
python projects/newman-air/tools/port-css.py
bash projects/newman-air/deploy-plugin.sh          # Local only
W eval-file projects/newman-air/tools/import-page.php projects/newman-air/pages/home/home.json home "Home"
W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/_theme/header.json newman-header include/singular/page/37
W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/_theme/footer.json newman-footer include/singular/page/37
W elementor flush-css
```

(`W` is the WP-CLI wrapper in `../../ENVIRONMENT.md`.) Band backgrounds are CSS-owned, so the
gate's "same background" rhythm warnings are expected.

## Scope on a shared install

The install also serves the live splash and Esteban's promo pages (Scheduled Promos). newman-core
loads only on pages with post meta `_newman_core = 1` (set by `tools/import-page.php`), which get
the body class `nw-site`; every ported rule is scoped to it. Checked: `/`, `/promo-landing/` and
`/best-in-show-is-now-newman-air/` load none of it. Header and footer are conditioned to page 37
only; switch them to Entire Site (`include/general`) at launch. No Elementor site option was changed.

## Dependencies on the target install

- newman-core 0.1.0 active (CSS, fonts Bricolage Grotesque + DM Sans, icon sprite, newman-site.js,
  logo and brand images in `assets/img/`).
- Elementor + Pro Elements (Pro form, Theme Builder).

## Deliberate differences from the prototype

| What | Why |
|---|---|
| Hero form is an Elementor Pro form | the prototype form posts nowhere |
| H1 underline is a CSS mask, not an inline SVG | the heading title is kses-filtered (SVG stripped); same path and draw timing |
| Button icons are CSS masks | button text is kses-filtered |
| Footer legal: no "Accessibility" link | it pointed to `#`; no page exists |

## Open items

- **Form routing:** sends to dispatch@newmanair.com. The current site's form recipient was not
  checked (callbestinshow.com admin); Alexis's Bear Necessities doc routes plan sign-ups to
  office@newmanheatandair.com. Confirm, plus SMTP and spam protection before launch.
- **Links** use the current site's slugs as placeholders; the new slugs and redirects were never shared.
- **Pending content** (yellow notes kept on purpose): team photo, live review widget, GBP map.
- **Tracking:** GTM-TCW4SVVM (from Juanse, ClickUp 86bcjyqph, 2026-10-22) is installed site-wide by Esteban
  through Header Footer Code Manager (snippets 1 and 2) and loads once on this page. Do not add it to
  newman-core. Juanse verifies form submissions and phone clicks after launch.
- **Fonts:** V2.1 uses Bricolage Grotesque + DM Sans (approved V2); tokens.json and the splash use Oxanium + Roboto.

## Editing notes

Style lives in newman-core: colours and sizes set in the Elementor panel do nothing where the
prototype CSS sets them. Text, links and order are editable in Elementor. The header nav, mobile
drawer, eyebrows, ridges, badge, polaroids, reviews skeleton, marquee, map, city list and FAQ are
html widgets (verbatim prototype markup): edit them in `build.py` / `brand.py` and rebuild.
