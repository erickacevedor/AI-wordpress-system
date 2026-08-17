# G.C. Reliable — Ductless Mini-Split Page: Import & Handoff Notes

One import-ready Elementor page, built on-brand from the kit's real design system
(blue `#0033CC` → `#001E78` gradients, brand red `#FF0000` CTAs, `#EFF2F5` alternating
bands, **brandon-grotesque** throughout, square red buttons with the colour-only
`#FF6464` hover). Modelled section-for-section on the agency's own hand-off templates
(`templates/227368.json` *AC Repair – Full Page* and `templates/227376.json` *Cooling
Services – Full Page*) and their published counterpart
(`current-theme/content/page/225063.json`), from the content doc
*GC Reliable_COPY_Page_Ductless Mini-Split.docx*.

## Files
- `ductless-mini-split.json` — the page (single-page import wrapper) ← **import this**
- `build.py` — reproducible build (`python projects/gcreliable/pages/ductless-mini-split/build.py`)
- `source.txt` — text extracted from the `.docx` brief
- `PREVIEW.html` — approximate browser preview for design review only (final render is Elementor)

## Layout standard (every section)
Full-width Section (100%, background only, section padding `64/20`, mobile `40/16`) →
**one boxed content container at 1280px** (laptop 92%, tablet/mobile 100%) → content.
No double-wrapped single widgets. Bands alternate and never repeat back to back:

`gradient → white → #EFF2F5 → white → #EFF2F5 → white → #EFF2F5 → white → gradient → #EFF2F5`

## Page structure (10 sections, varied layouts)
1. **Hero** — blue gradient (135°), min-height 44vh: H1 with the city as an inline span, sub-line, red CTA
2. **Flexible Comfort Where Traditional HVAC Falls Short** — white, **two columns**: copy + CTA │ technician photo with the overlapping red-bar "40+" badge (stacks copy-first on tablet/mobile)
3. **Ductless May Be a Good Fit If You Have…** — `#EFF2F5`, **two columns**: 6-item duotone check list │ white "The Goal Is Not Simply to Add Equipment" card
4. **Ductless Mini-Split Services Built Around Your Home** — white, **three emoji cards** (❄️ Installation & Replacement │ 🔧 Repair │ 🧰 Maintenance) + a full-width red-titled "Call for Service If You Notice" symptom card
5. **One Zone or Several?** — `#EFF2F5`, **two white cards** (Single-Zone with its own check list │ Multi-Zone)
6. **What to Expect When Adding Ductless Comfort** — white, **four numbered step cards** (`#F8F8FB`, 4px blue left bar)
7. **What Westchester Homeowners Ask About Ductless Mini-Splits** — `#EFF2F5`, **Elementor Pro accordion** (5 Q&A, 62%) │ white "Still Have Questions?" card with CTA (34%)
8. **See How G.C. Reliable Helps Local Properties Stay Comfortable** — white, dashed review band with the Trustindex Google slider + **stat trio** (40+ / 24/7 / All makes)
9. **Why Locals Choose G.C. Reliable for Ductless Comfort** — blue gradient, **two columns**: white copy + 3-item check list + a red "Learn More About G.C. Reliable" CTA │ photo + "24/7" badge
10. **Put Comfort Where You Actually Need It** — `#EFF2F5`, closing CTA

## Copy note
The source doc's review heading read *"See How G.C. Reliable Helps the Local Sound
Properties Stay Comfortable"*. "the Local Sound" appears to be a typo (Long Island
Sound?), so the heading ships as **"See How G.C. Reliable Helps Local Properties Stay
Comfortable."** Tell us if a Sound-shore reference was intended and we'll restore it.

## Icons
A mix of **emoji** (❄️ 🔧 🧰 as the service-card icons) and the kit's native Font Awesome —
`fad fa-check-circle` duotone check lists and 40px `fas` stat icons — so the page never
depends entirely on the icon font. JSON is UTF-8; swap any emoji in the text field.

## After import — wire up
1. **Images.** Both photos use existing media with real attachment ids —
   `227360` (`gc-reliable-technician-2.webp`) in section 2 and `227384`
   (`gc-reliable-3.webp`) in section 9. If you want topical shots, the library already
   has `2025/03/Ductless-Mini-Split-e1742217720601.jpg`; swap it in and keep the alt
   text descriptive.
2. **Trustindex.** Section 8 uses widget id `be35b8a27428268b9b962ab1e27` (the same
   Google-review slider the AC Repair page uses). Re-point if this page should show a
   different widget.
3. **Links** are root-relative: `/service-area/new-rochelle`,
   `/systems/air-conditioning`, `/systems/maintenance`, `/systems/heat-pumps`,
   `/systems/heating`, and all CTAs to `/schedule-appointment`. Confirm they match the
   live site.
4. **Page settings** ship as `{"template":"elementor_header_footer","hide_title":"yes"}`,
   matching the AC Repair page. The site header/footer come from the theme builder —
   confirm they render, then publish.
5. **Replacing the existing page.** The live Ductless Mini Split page (id 225070) is a
   legacy text-only page whose hero is rendered from ACF fields
   (`page_h1_title`, `page_sub-title`, `lead_paragraph`) with `template: "default"`.
   This page builds its own hero, so after import **switch the page template to
   Elementor Full Width / header-footer** and clear or ignore those ACF fields, or the
   hero will appear twice.

## SEO handoff (set in your SEO plugin at the WP page level)
- **Slug:** `/systems/ductless-minisplits` (retain the existing slug)
- **Meta title:** Ductless Mini-Split Services in New Rochelle, NY | G.C. Reliable Service
- **Meta description:** Ductless mini-split installation, repair, and maintenance in New Rochelle and Westchester County — zoning planned around the rooms that actually need help, since 1980.
- **H1:** "Ductless Mini-Split Services in New Rochelle, NY" (exactly one H1 on the page)

## QA — verified before delivery
- `python scripts/validate-page.py projects/gcreliable/pages/ductless-mini-split/ductless-mini-split.json` → **PASS**
  (JSON parses · single-page wrapper · unique ids · exactly one H1 · no
  `display_condition_list` · no dead/localhost links · full responsive audit clean)
- Brand check against the kit: brandon-grotesque only; body text left unstyled so it
  inherits the global *Normal Text*; button is square red, `size: xl`,
  `far fa-calendar-check`, hover `#FF6464`, **no** hover animation; band tints inlined
  (`#EFF2F5` / `#E6ECFA` / `#F8F8FB`) rather than pulled from the kit's duplicated
  colour-global ids.
- One deliberate departure from the reference page: the floating badge is 100% wide on
  mobile (the kit uses 82%), because the repo's responsive gate requires %-width
  columns to go full width once a row has stacked.
