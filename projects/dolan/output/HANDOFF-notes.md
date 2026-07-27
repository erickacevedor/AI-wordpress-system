# Dolan Design — Cooling Services Page: Import & Handoff Notes

One import-ready Elementor page, built on-brand from your kit's real design system
(Blue `#0C4096` / White / Black `#222222`, light-blue section bands `#EDF4FF`, gold check
accents `#FAB914`, **Ruda** throughout). Cloned from the structure of your existing AC Repair
service page so it looks like it always belonged.

## File
- `cooling-services.json` — the page (single-page import wrapper)
- `PREVIEW.html` — approximate browser preview for design review only (final render is in Elementor)

## Layout standard (applies to every section)
Every section is built as **full-width Section (100%, background only) → one boxed
content container (the site's content width, **1140px** on this kit) → content**.
Content widgets sit directly in that boxed container — a lone image or text is
**not** double-wrapped in its own extra container. Multi-column rows/grids are used
only where the layout genuinely needs them, for variety.

**Icons:** a mix of **emoji** (service-card icons 🚨🛠️♻️🧰❄️ and the benefit list
📍🔧💰💳) and Elementor icons (button arrows), so the page isn't fully dependent on
the Elementor/FontAwesome icon library. Emoji render cross-platform and need no icon
font — swap any for a different emoji right in the text field.

## Page structure (5 sections, varied layouts)
1. **Hero** — full-bleed blue-overlay photo band; boxed H1 + intro + service-area line + "Schedule Your Cooling Service Online" button
2. **How We Can Help Keep Your Home Cool** — centered intro + **3-column grid** of 5 service cards (each led by an emoji icon), each with an "Explore…" button linking to that service page
3. **Why Franklin & Wake County Neighbors Choose Dolan Design** — light-blue band, **two-column** (emoji benefits list + CTA | photo)
4. **Frequently Asked Questions** — light-blue band, 5-item nested accordion (single column)
5. **Final CTA** — full-bleed blue-overlay photo band; boxed heading + phone + button

## How to import
Elementor → Templates → **Import Templates** (up-arrow icon) → select `cooling-services.json` → **Insert**.
Then open the page, assign your site **header + footer** if not inherited, and publish.
(Uses the single-page wrapper `{version,title,type:page,content,page_settings}`, so it imports as a
page template — not the kit `content/page` format that throws "Invalid template type.")

## After import — wire up
1. **Hero & CTA background images** already point to media already in your library
   (`hero-neighborhood_25.webp` and `large-cta-Group-Photo1-1-scaled-1.webp`). Swap if you prefer
   cooling-specific photos, and set **alt text**.
2. **CTA buttons** point to `#contact` — re-point to your booking form/anchor if different.
   Service-card "Explore…" links point to your live pages:
   `/ac-repair/`, `/air-conditioner-maintenance/`, `/ac-replacement/`,
   `/air-conditioner-installation/`, `/mini-splits/` — confirm these slugs match (update if not).
3. **Phone** is `tel:+19198968630` → (919) 896-8630.

## SEO handoff (set in Rank Math / Yoast at the WP page level — not stored in Elementor JSON)
- **Slug:** `cooling-services`
- **Meta title:** Air Conditioning & Cooling Services
- **Meta description:** Dependable AC repair, maintenance, installation & mini-splits in Louisburg & Wake County. Call Dolan Design at (919) 896-8630

## QA — verified before delivery
- Valid JSON, 65 elements, all unique IDs, required Elementor keys present.
- Exactly one H1; clean H1 → H2 → H3 hierarchy.
- Every section = full-width Section → single boxed (≤1300px) content container → content; no double-wrapped single widgets.
- Alternating background rhythm (hero dark → white → light-blue → light-blue FAQ → dark CTA).
- Brand colors/fonts applied via the kit's real globals + inline fallbacks; square bordered buttons.
- Responsive (verified): 3-col service grid steps 3→2→1 (desktop→tablet→mobile); the
  two-column "Why Choose" row stacks and its columns go 50%→100%; every boxed
  container has a smaller `padding_mobile`; H1 + all four section H2s + the emoji card
  icons carry tablet/mobile font-size overrides; images have `height_mobile`.
