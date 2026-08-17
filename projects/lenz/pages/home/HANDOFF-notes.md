# Lenz — Home (v4) · handoff

**Status:** all 15 homepage sections built, imported and verified on `lenz-2026`
(page #23, set as the front page). Header and footer are done as Theme Builder parts —
see `../_theme/HANDOFF-notes.md`.

hero · trust bar · services · CTA band · financing · value props · plans · reviews ·
brands · about · WHO 13 · credentials · service area · FAQs · close + form

## Rebuild / reimport loop

```bash
python projects/lenz/pages/home/build.py
python scripts/validate-page.py projects/lenz/pages/home/home.json     # must exit 0
wp eval-file projects/lenz/tools/import-page.php \
   projects/lenz/pages/home/home.json home "Home"                      # idempotent
```

The plugin is deployed separately — **it is not carried by the page JSON**:

```bash
projects/lenz/deploy-plugin.sh      # repo -> wp-content/plugins/lenz-core
```

Re-run the deploy after *any* stylesheet edit. The repo is the source of truth;
editing the plugin inside `wp-content/plugins/` is overwritten on the next deploy.

## Verified on the live render

| | |
|---|---|
| Page | HTTP 200, 0 PHP errors |
| Headings | 1 × H1, 1 × H2, 5 × H3, 17 × H4 |
| Icon sprite | 24 symbols injected, 33 `<use>` references |
| Container classes | all present with correct counts (5 trust items, 4 lead cards, 17 service cards) |
| Native gradients | 4, all emitted as `linear-gradient(135deg, var(--e-global-color-…))` |
| CSS-owned effects | hero radials, lead-card sheen, clipped text, trust-bar borders, button variants, 5 reduced-motion blocks |

## Three things learned the hard way (already fixed)

1. **Containers use `css_classes`; widgets use `_css_classes`.** Using the widget key
   on a container fails *silently* — the class sits in the JSON, imports without a
   complaint, and never reaches the markup. Cost a full debug cycle. Now handled in
   `_apply_classes()`.
2. **Gradient stops bind to Global Colors via `__globals__`,** not by putting the
   `globals/colors?id=…` string in the colour value. The wrong form renders nothing.
3. **`.lead-card--warm` uses `--gradient-temperature`, not `--gradient-warm`.** The
   class name and the gradient name disagree in the source; collapsing them silently
   swaps two brand gradients. The heating card shipped gold→orange for one build
   before this was caught.

## Known gaps in what is built

- **The form sends nowhere yet.** Pro Forms is wired with an email action to
  `jenny@lenzheatingandcooling.com`, but Local has no SMTP — nothing will actually
  deliver until an SMTP plugin is configured. It also has **no spam protection** and
  **no lead storage**; both are required before this goes near production.
- **The About media bleed is partial.** The row is a grid so the negative margin does
  widen the cell, but it does not reach the full −72px. Decorative only; `overflow:hidden`
  prevents any horizontal scrollbar.
- **Reviews are the hardcoded fallback quotes.** The skeleton/live states and the
  Places REST proxy are not built. No `aggregateRating` is emitted, correctly.
- **Brand logos are text wordmarks.** The marquee widget renders an image the moment a
  repeater row gets one.

## Deliberately deferred

- **Elementor icon-picker library.** The sprite works via `<use>`, but the icons are
  not pickable in widget icon controls. `additional_tabs` is built for icon *fonts*,
  so this needs a generated `mask-image` CSS layer plus a JSON manifest.
- **Services as a CPT.** Hand-assembled per the revised decision. Adding a service is
  currently a three-place edit (grid, mega menu, footer). Card shape is unchanged, so
  migration stays a contents swap.
- **The 13 remaining sections.**

(Header and footer are **done** — see `../_theme/HANDOFF-notes.md`. Read its width-budget
note before adding a nav item.)

## Publish-time wiring (not stored in Elementor JSON)

- SEO title (< 60), meta description (< 155), slug — via Rank Math / Yoast.
- Decide schema ownership: the static build hand-wrote `HVACBusiness` + `FAQPage`
  JSON-LD. An SEO plugin will duplicate it unless one owner is chosen.
- **No `aggregateRating`** until verified Google data exists.
- Image URLs are root-relative (`/wp-content/uploads/…`), so the page is not welded
  to `http://localhost:10010`. Attachment ids are recorded in `../../media.json`.

## Still blocked on assets

Carried from `js/lenz-config.js` — these block launch, not the build: logo SVGs,
approved hero photography (current image is a stand-in with no technician and no Lenz
branding), the nine manufacturer logos, the WHO 13 segment URL, the GBP Place ID +
reviews proxy, the real financing application URL, and the 18 live service page URLs.
