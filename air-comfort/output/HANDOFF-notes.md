# Air Comfort — New IAQ Pages: Import & Handoff Notes

Three import-ready Elementor pages, built on-brand from your kit's real design system
(navy `#1B2C47` / red `#E1333A` / cyan `#0CC0DF`, Asap Condensed + Urbanist), pushed a
bit more modern: full-width sections → one centered content container, floating cards,
emoji/icon accents, varied 1- and 2-column layouts, and labeled image placeholders.

## Files
- `air-purification-services.json`
- `humidity-control-services.json`
- `indoor-air-quality-services.json`
- `PREVIEW.html` — approximate browser preview of all three (design review only; final render is in Elementor)

## How to import (each page)
Elementor → Templates → **Import Templates** (up-arrow icon) → select the JSON → **Insert**.
Then open the page, assign your site **header + footer** if not inherited, and publish.
(The files use the single-page wrapper `{version,title,type:page,content,page_settings}`,
so they import as a page template — not the kit `content/page` format that throws
"Invalid template type.")

## After import — 3 things to wire up
1. **Image placeholders** — each dashed box is labeled with what image goes there. Drop in a
   real image and set descriptive **alt text** (required for SEO/accessibility).
2. **Review slider** — the "REVIEW SLIDER PLACEHOLDER" card marks where your Google/reviews
   widget goes (live widgets can't be stored in template JSON).
3. **Links** — CTAs point to `/request-service`, the Comfort Club button to `/maintenance-plan`,
   and phone to `tel:+14236777856`. Re-point any that differ on your site. Cross-links between
   these three pages use `/air-purification`, `/humidity-control`, `/indoor-air-quality` — make
   the published slugs match (below) or update the anchors.

## SEO handoff (set in Rank Math / Yoast at the WP page level)

**Air Purification**
- Slug: `air-purification`
- Meta title: Air Purification Services in the Tri-Cities
- Meta description: Get cleaner air at home with whole-home air purification for Tri-Cities homes dealing with dust, pets, pollen, odors, and stale indoor air issues today.

**Humidity Control**
- Slug: `humidity-control`
- Meta title: Humidity Control Services in the Tri-Cities
- Meta description: Manage excess indoor humidity with whole-home solutions from Air Comfort Services. Get clearer options for a fresher, more comfortable home. Contact us today!

**Indoor Air Quality**
- Slug: `indoor-air-quality`
- Meta title: Indoor Air Quality Services in the Tri-Cities
- Meta description: Need cleaner indoor air? Get humidity control, UV light purification, and indoor purification services in the Tri-Cities, TN from Air Comfort Services.

## QA — verified before delivery
- Valid JSON, unique element IDs, all required Elementor keys present.
- Exactly one H1 per page; clean H1 → H2 → H3 hierarchy.
- Every section = full-width Section → single padded Content Container → content (no over-nesting).
- Alternating background rhythm (no two identical section backgrounds in a row).
- Brand colors/fonts applied inline (not via Elementor globals); red pill CTAs, color-only hover.
- Mobile: multi-column rows set to stack; heading sizes have mobile overrides.
