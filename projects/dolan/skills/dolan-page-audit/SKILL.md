---
name: dolan-page-audit
description: >
  Audit-first review for Dolan Design HVAC Elementor pages/templates. Use when asked
  to review, clean up, fix, or improve a Dolan page, or as the pre-delivery gate
  before shipping one. Checks against the Dolan brand kit, Elementor hygiene, and the
  responsive checklist — without breaking layout or fighting the brand. Pairs with
  dolan-ui-design and dolan-content-style.
---

# Dolan Design HVAC Page Audit

Reviews Dolan Design Elementor pages against the brand kit. Elementor-aware — does not
apply generic "premium web" defaults that conflict with the brand.

## How this works

1. **Scan** — read the page JSON. Note section order/backgrounds, widget types, and
   inline vs. global styling.
2. **Diagnose** — run the audit below; list each issue with its widget/section.
3. **Fix in place** — targeted corrections that keep structure; reuse header/footer.

## Brand-consistency audit

Flag and fix:

- **Broken section structure.** Any section not built as **full-width Section → one
  BOXED (~1140px) Content Container → content**. Padding must live only on the boxed
  container (and self-contained cards); strip it from the outer Section and from
  nested rows/columns/grids.
- **Excess containers.** A lone image or text double-wrapped in its own extra
  container — flatten so the widget sits directly in the boxed container.
- **Off-brand button.** Primary CTA not the brand **square** button: black text +
  1px border (`be5c055 #222222`), `border-radius:0`, arrow icon row-reverse, color-only
  hover. Fix pill/wrong-color buttons. (Keep them square — pills are off-brand here.)
- **Wrong font.** Any widget not using **Ruda**. Fix.
- **Broken section rhythm.** Two identical backgrounds in a row. Alternate
  blue-overlay / white / light-blue `#EDF4FF`.
- **Wrong heading color.** Should be blue `#0C4096` / dark `#222222` on light, white on
  blue-overlay bands.
- **Globals check.** Dolan's globals are REAL — global-referenced colors are fine here
  (unlike kits where globals are Hello defaults). Don't "fix" them to inline for its
  own sake; do ensure the referenced id maps to the intended brand color.

## Do NOT "fix" these (on-brand, not mistakes)

- **Colored hero/CTA bands** (blue-overlay photos) and **alternating** white/light-blue
  rhythm — intended.
- **Square bordered CTAs** — required (do not round into pills).
- **Blue + gold accents** — the "one accent" rule doesn't apply.
- **Numbered spectre-icon process/benefit grids** and **gold check icon-lists** — brand
  patterns.

## SEO checks

- **Exactly one H1** (hero). Others are H2/H3 in a logical hierarchy.
- **Meta title** < ~60 chars; **meta description** < ~155; slug lowercase-hyphenated.
- Target keyword in H1 + intro. Elementor JSON doesn't store WP SEO meta — confirm
  title/description/slug are provided as a publish-time handoff (Rank Math / Yoast).

## Internal linking & media

- Required internal links present with descriptive anchors; no `href="#"`/empty
  (except the intended `#contact` CTA anchor).
- Service cards point to real slugs (`/ac-repair/`, `/air-conditioner-maintenance/`,
  `/air-conditioner-installation/`, `/ac-replacement/`, `/mini-splits/`).
- Every image has descriptive alt text; live widgets are labeled placeholders.

## Responsive checklist (audit the JSON before import)

Run `python3 scripts/responsive-audit.py <page>.json` (exit 0 = clean) and confirm:

- **Grids** set `grid_columns_grid_tablet` (~2) + `_mobile` (1).
- **Flex rows** set `flex_direction_mobile:column`.
- **%-width columns** set `width_mobile:100%` (+ `width_tablet`).
- **H1 + every section H2** carry `typography_font_size_mobile` (globals-only headings
  don't shrink — use self-contained responsive sizes).
- Boxed container has `padding_mobile`; fixed-height images have `height_mobile`.
- Then confirm visually in Elementor's tablet + mobile preview.

## Elementor hygiene

Unique `id` per element; required keys intact; no dead buttons (besides `#contact`);
complete/valid JSON (no truncation). Include the kit's Divi-compat `custom_css` and
`hide_title:"yes"` in `page_settings`. Reuse the kit header/footer.

## Fix priority

1. Fix section structure (full-width → boxed 1140 → content; padding discipline).
2. Correct button to the square bordered brand style; fix off-brand colors/fonts.
3. Restore background rhythm.
4. Responsive passes (`responsive-audit.py`); set mobile sizes/padding.

## Rules

Work within Elementor and the existing kit. Don't break working layout. Keep the JSON
complete and valid (see `full-output-enforcement`).
