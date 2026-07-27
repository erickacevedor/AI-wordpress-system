# Magnolia Air — AC Services Page: Import & Handoff Notes

One import-ready Elementor page, built on-brand from your kit's real design system
(teal `#0C4F4D` / gold `#D4B351` / dark teal `#00333F`, cream `#F3EBD6` bands,
**Como-ExtraBold** headings + **BeVietnamPro** body, gold **pill** buttons that flip to
teal on hover). Built for the new content doc *Air Conditioning Services in Dry Prong, LA*.

## File
- `air-conditioning-services.json` — the page (single-page import wrapper)
- `PREVIEW.html` — approximate browser preview for design review only (final render is in Elementor)

## Layout standard (every section)
Full-width Section (100%, background only) → one boxed content container (the site's
~1140px content width) → content directly. No double-wrapped single widgets; multi-column
rows/grids only where the layout needs them. Backgrounds alternate: dark → cream → white →
cream → white → teal → dark → cream → teal.

## Page structure (9 sections, varied layouts)
1. **Hero** — dark-teal band, **two columns** (headline + intro + 24/7 call-out + button | photo)
2. **Find The Right AC Service** — cream band, centered intro
3. **AC Services That Keep Central Louisiana Comfortable** — white band, **3-col grid** of 6 emoji service cards (Repair, Maintenance, Installation, Replacement, Tune-Up, Emergency), each linking to its service page
4. **Cooling Support For Homes And Businesses** — cream band, **two cards** (Homeowners | Businesses)
5. **When It Is Time To Call Magnolia Air** — white band, two-column symptom lists + CTA
6. **Why Trust Magnolia Air** — teal band (white text), two-column "what to expect" list
7. **Emergency AC Help** — dark-teal band, text + 24/7 call-out
8. **FAQ** — cream band, 5-item nested accordion
9. **Final CTA** — teal band, call-out + Request Service button

## Icons
A mix of **emoji** (service-card icons 🔧🧰📐♻️⚙️🚨, home/business 🏠🏢, benefit + symptom
lists) and native styling, so the page doesn't depend on an icon font. Swap any emoji in
the text field.

## After import — wire up
1. **Hero image** points to `moesalley.com/.../IMG_1190-scaled.webp` (an existing kit image).
   Swap for a Dry Prong / Magnolia photo and set descriptive **alt text**.
2. **Links** use root-relative slugs: services → `/ac-repair/`, `/ac-maintenance/`,
   `/ac-installation/`, `/ac-replacement/`; all CTAs + Emergency → `/request-service/`.
   Note: **AC Tune-Up** points to `/ac-maintenance/` (no dedicated tune-up page) and the
   emergency card to `/request-service/` (you also have `/request-service-em/`) — re-point
   if you prefer. Confirm these slugs match the live site.
3. **Phone** is `tel:318-233-9318` → (318) 233-9318.
4. Assign your site **header + footer** if not inherited, then publish.

## SEO handoff (set in your SEO plugin at the WP page level)
- **Slug:** retain the page's existing slug (per the content doc: *[retain slug]*)
- **Meta title:** Air Conditioning Services in Dry Prong, LA
- **Meta description:** Magnolia Air offers residential and commercial AC services in Dry Prong, LA, with honest guidance for repairs, tune-ups, installs, and replacements.

## QA — verified before delivery
- Valid JSON, 117 elements, all unique IDs, single-page wrapper.
- Exactly one H1; clean H1 → H2 → H3 hierarchy.
- Every section = full-width → single boxed (~1140px) container → content; no excess wrappers.
- Brand colors/fonts via the kit's real globals + inline; gold pill buttons with the site's
  `shrink` hover.
- Did **not** copy the kit's `display_condition_list` subscriber gates (those hide content).
- Responsive: passes `scripts/responsive-audit.py` — grids 3→2→1, rows/columns stack,
  headings have mobile sizes, containers have `padding_mobile`, images have `height_mobile`.
