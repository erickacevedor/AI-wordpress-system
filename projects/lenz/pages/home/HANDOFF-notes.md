# Lenz: Home (v6-1) handoff

**Status (2026-10-13):** built from the approved prototype v6-1 and imported on the
Mac Local copy `lenz-2026` (page 23, front page). Not on lenz.mysites.io yet.
Verified against the prototype with headless Chromium at 1440, 1024, 768 and 390:
every section has the same height as the prototype at all four widths, and an
element-by-element position diff shows no difference above 3px except the
deliberate fixes listed below.

## SEO (set in the SEO plugin; Elementor JSON cannot carry these)

- **Meta title:** `Des Moines HVAC Repair and Install | Lenz Heating & Cooling`
- **Meta description:** `Des Moines HVAC repair and replacement. Veteran and woman-owned, 24/7 service, upfront pricing, free estimates on new systems.`
  (Changed from the doc and v6-1, which said "no trip or diagnostic fees": that
  contradicts the client's 09/10 ClickUp decision that only estimates are free.
  Approved by Erick 2026-10-13.)
- Slug: `/` (front page, page 23 `home`)
- Canonical: https://www.lenzheatingandcooling.com/
- Schema: the prototype hand-writes HVACBusiness + FAQPage JSON-LD in its <head>.
  Not ported yet: decide whether the SEO plugin or lenz-core owns it, so it is
  not emitted twice. No aggregateRating until verified Google data exists.

## How it is built

`brand.py` mirrors the prototype DOM and class names; `tools/port-css.py` ports
the prototype stylesheet into `lenz-core`; the Elementor adapter at the top of
`lenz-core.css` makes Elementor's wrappers transparent. Rebuild everything with:

```bash
projects/lenz/build-all.sh                      # build + gate + port
LENZ_WP_CLI=<wp wrapper> LENZ_WP=<app/public> projects/lenz/build-all.sh --import   # LOCAL only
```

Band order and backgrounds are CSS-owned (`section`, `section--mist`,
`.dark-section` classes), so the gate's "same background" rhythm warnings are
expected and not findings.

## Dependencies on the target install

- **lenz-core 0.2.0 active** (CSS, icon sprite, fonts, `lenz-site.js`). Without
  it the page is structurally intact and visually broken.
- Elementor + PRO Elements (Pro Form widget for the estimate form).
- Site setting: **Elementor > Settings: Disable Default Colors and Disable Default
  Fonts** (`elementor_disable_color_schemes` / `elementor_disable_typography_schemes`
  = yes). Otherwise the kit paints every heading in the global primary blue.
- Google Fonts are loaded by lenz-core (the prototype's exact weights);
  Elementor's own font loading is switched off by lenz-core.

## Deliberate differences from v6-1

| What | Why |
|---|---|
| Meta description wording | see SEO above |
| Brands section below 904px: column min-width 0 | v6-1 clips the heading, lead and chips off the right edge on phones (marquee sets the column's minimum width) |
| Estimate form is an Elementor Pro form | the prototype form posts nowhere |
| Internal links point to the planned page slugs | the prototype links to `#` |
| "Explore financing" goes to `/financing/` | the prototype pointed at `#contact`; a Financing page now exists in the sitemap |
| "Watch Our Latest News Segments" goes to `/hello-iowa/` | the prototype had `#contact`; the Hello Iowa page doc exists |

## After import: confirm or wire up

- **Form recipient:** the email action sends to Sierra@LenzHeatingandCooling.com
  (the contact email ClickUp settled on). Confirm the recipient, add SMTP and spam
  protection before launch. On Local, mail goes to Mailpit.
- **Page slugs with no doc yet** (links already point at them): heating-replacement,
  duct-cleaning, additional-services and its five children, privacy-policy, terms.
  "Indoor Purification" links to `/air-purification/` (the doc's page name).
- **Reviews** are the hardcoded quotes; "Real reviews" links to a Google Maps
  search until the GBP Place ID is known.
- **Map** shows the Urbandale office only (the doc asks for both offices plus a
  service radius).
- **Media:** attachments 30 to 43 on the Local install (`media.json`). Moving to
  mysites needs the same files and an id remap in `media.json`.

## Editing notes for whoever maintains it

- Style lives in lenz-core: changing a colour or size in the Elementor panel does
  nothing where the prototype CSS sets it. Text, links, images and order are
  editable in Elementor.
- The FAQ, the marquee, the map and the WHO 13 video are html widgets (verbatim
  prototype markup). Edit them in `build.py` and rebuild.
- In the Elementor editor canvas the html widgets keep their wrapper box, so the
  editor view is slightly looser than the front end.
