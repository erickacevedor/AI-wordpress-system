# Lenz — project status

**As of 2026-08-17.** Snapshot of what is built, what is live, and what is not.
Companion to `KIT-ANALYSIS.md` (the design system and the *why*) and the per-page
`HANDOFF-notes.md` files (the import/wiring detail). Update this file when the
answer to "where are we?" changes.

---

## Environment

| | |
|---|---|
| WP install | `C:\Users\erick\Local Sites\lenz-2026\app\public` (Local) |
| URL | <http://localhost:10010> — responding 200 |
| Theme | Hello Elementor 3.4.9 |
| Plugins active | `elementor`, `pro-elements`, `lenz-core` |
| Source design repo | `D:\laragon\www\lenz` — v4 is the build target |
| Repo commit | `2e98777` on `main`, pushed to `origin` |

The WP install is **not** version-controlled. The repo is the source of truth and the
install is a deployment target — see the rebuild loop below.

## What exists on the site

| Object | Id | State |
|---|---|---|
| Page **Home** | 23 | Published, set as the front page, 130 KB of `_elementor_data` |
| Template **Lenz Header (v4 light)** | 25 | `include/general` — applied site-wide |
| Template **Lenz Footer** | 26 | `include/general` — applied site-wide |
| Default Kit | 5 | Carries the created Global Colors |
| Attachments | 10–22 | 13 files; ids recorded in `media.json` |

Everything else on the install is WP stock: `Sample Page` (#2) and a draft
`Privacy Policy` (#3). **No other Lenz page has been built.**

The home page renders all 15 sections: hero · trust bar · services · CTA band ·
financing · value props · plans · reviews · brands · about · WHO 13 · credentials ·
service area · FAQs · close form.

## What exists in the repo

```
projects/lenz/
├── KIT-ANALYSIS.md          design system, contrast rules, "do NOT fix these"
├── STATUS.md                this file
├── tokens.json              brand tokens + the real Global Color ids from the live kit
├── media.json               attachment id ↔ filename map
├── deploy-plugin.sh         repo -> wp-content/plugins/lenz-core
├── plugin/lenz-core/        master CSS, 24-symbol icon sprite, marquee widget, a11y shim
├── tools/                   import-page.php · import-template.php · set-globals.php
└── pages/
    ├── _theme/              header.json · footer.json · build-templates.py
    └── home/                home.json · build.py
```

All three page JSONs pass `scripts/validate-page.py` (exit 0). The deployed plugin
matches `plugin/lenz-core/` in content.

## Rebuild loop

```bash
python projects/lenz/pages/home/build.py
python scripts/validate-page.py projects/lenz/pages/home/home.json      # must exit 0
wp eval-file projects/lenz/tools/import-page.php \
   projects/lenz/pages/home/home.json home "Home"                       # idempotent
projects/lenz/deploy-plugin.sh                                          # after ANY CSS edit
```

`wp` is not on the default PATH — run these from Local's site shell, or point
`LENZ_WP` at the install. Editing the plugin inside `wp-content/plugins/` does not
survive the next deploy.

## Not built yet

The nav, mega menu and footer link to **23 URLs that do not exist**:

- 4 service hubs — `/services/air-conditioning/`, `/heating/`, `/indoor-air-quality/`,
  `/additional-services/`
- 18 individual service pages beneath them
- `/specials/`, plus `/privacy-policy/` and `/terms/` from the footer bottom bar

**These have no HTML template to translate from.** The source repo carries homepage
variants only (`index`, `v2`–`v5`); the inner pages were never designed there, so they
have to be built from the v4 system rather than converted.

## Known gaps (carried from the handoff notes)

**Blocking production**
- The close form sends nowhere — Pro Forms has an email action, but Local has no SMTP.
  It also has **no spam protection** and **no lead storage**.
- Logo is still the placeholder PNG; SVG lockups pending.
- Hero photography is a stand-in — no technician, no Lenz branding.
- Brand logos in the marquee are text wordmarks, not the nine manufacturer logos.

**Functional gaps**
- Mobile mega-menu drawer is not styled to match the source's full-screen navy drawer,
  and the phone number needs to appear there.
- The a11y shim has **not** been verified with a real screen reader or keyboard pass.
- Reviews are hardcoded fallback quotes — no Places proxy, no skeleton/live states.
  No `aggregateRating` is emitted, which is correct until verified Google data exists.
- Sticky header behaviour is not yet checked against the offer bar scrolling away.

**Constraints to respect**
- The header's boxed container is **1140px at every viewport**. Seven nav items fit
  only after the phone number was dropped from the bar. **An eighth item overflows** —
  budget for it before adding one.
- Adding a service is a **three-place edit** (services grid, mega menu, footer). This
  was the accepted cost of hand-assembling instead of using a `service` CPT.

## Still blocked on client assets

Carried from `js/lenz-config.js`: logo SVGs, approved hero photography, the nine
manufacturer logos, the WHO 13 segment URL, the GBP Place ID + reviews proxy, the real
financing application URL, and the 18 live service page URLs.

## Recommended next steps

1. **Extract `projects/lenz/brand.py`.** `pages/home/build.py` is 871 lines with the
   brand vocabulary inline. `gcreliable/brand.py` (471 lines) proves the pattern: it
   cut that site's page builds to copy + section order only. Doing this *before*
   building 20+ service pages pays for itself immediately.
2. **Generate the `lenz-*` skills.** Lenz is the only site with no `skills/` — it was
   onboarded from HTML rather than a kit, so step 2 of the loop in `AGENTS.md` was
   never run. There is no `lenz-content-style` to tell the next build what the voice
   is. `KIT-ANALYSIS.md` already holds most of the design-read content.
3. **Design the service-page template once**, then treat the other 17 as content swaps.
4. **Decide schema ownership** before an SEO plugin is installed — the static build
   hand-wrote `HVACBusiness` + `FAQPage` JSON-LD, which a plugin will duplicate.

## Housekeeping note

`core.autocrlf=true` rewrites the working tree to CRLF on checkout, so the deployed
plugin differs from the repo copy in line endings only (content is byte-identical
after stripping `\r`). Harmless for PHP/JS/CSS. A `.gitattributes` with
`* text=auto eol=lf` would stop the churn.
