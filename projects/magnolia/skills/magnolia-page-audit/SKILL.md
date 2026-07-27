---
name: magnolia-page-audit
description: >
  Audit-first review for Magnolia Air Elementor pages/templates. Use when asked to
  review, clean up, fix, or improve a Magnolia page, or as the pre-delivery gate
  before shipping one. Checks against the Magnolia brand kit, Elementor hygiene, and
  the responsive checklist — without breaking layout or fighting the brand. Pairs
  with magnolia-ui-design and magnolia-content-style.
---

# Magnolia Air Page Audit

Reviews Magnolia Air Elementor pages against the brand kit. Elementor-aware — does
not apply generic "premium web" defaults that conflict with the brand.

## How this works

1. **Scan** — read the page JSON. Note section order/backgrounds, widget types,
   inline vs. global styling, and any `display_condition_list`.
2. **Diagnose** — run the audit below; list each issue with its widget/section.
3. **Fix in place** — targeted corrections that keep structure; reuse header/footer.

## Brand-consistency audit

Flag and fix:

- **Subscriber gate present.** Any `display_condition_list` (esp. `subscriber`) —
  **remove it**; it hides content from normal visitors. (Top-priority check — the kit's
  exported pages all carry it.)
- **Broken section structure.** Any section not built as **full-width Section → one
  BOXED (~1140px) Content Container → content**. Padding must live only on the boxed
  container (and self-contained cards); strip padding from the outer Section and from
  nested rows/columns/grids.
- **Excess containers.** A lone image or text double-wrapped in its own extra
  container — flatten it so the widget sits directly in the boxed container.
- **Off-brand button.** Primary CTA not the gold pill: gold bg (`secondary #D4B351`),
  white text, 2px gold border, `border-radius:50`, teal (`primary #0C4F4D`) hover,
  `hover_animation:"shrink"`, BeVietnamPro-ExtraBold. Fix square/wrong-color buttons.
  (Keep `shrink` — it's this brand's convention, not a mistake.)
- **Wrong font.** Headings not Como-ExtraBold, body not BeVietnamPro-Light. Fix.
- **Broken section rhythm.** Two identical backgrounds in a row. Alternate
  dark `#00333F` / cream `#F3EBD6` / white / teal `#0C4F4D`.
- **Wrong heading color.** Should be teal `#0C4F4D` on light, white on dark/teal.
- **Absolute/localhost links.** Internal links using `localhost:10008` or full URLs —
  convert to root-relative slugs.
- **Broken media.** Hero/section referencing a `moesalley.com` asset that may not
  exist on the target — flag as a swap-me placeholder; ensure alt text.

## Do NOT "fix" these (on-brand, not mistakes)

- **Colored bands** (dark teal, teal, gold, cream) and **alternating** dark/light
  rhythm — intended.
- **`shrink` button hover** — the brand's convention here.
- **Gold pill CTAs** — required.
- **Multiple brand colors** (teal + gold) — the "one accent" rule doesn't apply.

## SEO checks

- **Exactly one H1** (hero). Others are H2/H3 in a logical hierarchy.
- **Meta title** < ~60 chars; **meta description** < ~155; slug lowercase-hyphenated.
- Target keyword ("air conditioning services … Dry Prong") in H1 + intro.
- Elementor JSON doesn't store WP SEO meta — confirm title/description/slug are
  provided as a publish-time handoff (set in the SEO plugin).

## Internal linking & media

- Required internal links present with descriptive anchors; no `href="#"`/empty.
- Service cards point to real slugs (`/ac-repair/`, `/ac-maintenance/`,
  `/ac-installation/`, `/ac-replacement/`, `/request-service/`).
- Every image has descriptive alt text; live widgets (forms) are labeled placeholders.

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

Unique `id` per element; required keys intact; no dead buttons; complete/valid JSON
(no truncation). Reuse the kit header/footer rather than duplicating chrome.

## Fix priority

1. Remove `display_condition_list` gates.
2. Fix section structure (full-width → boxed 1140 → content; padding discipline).
3. Correct button to the gold pill; fix off-brand colors/fonts.
4. Restore background rhythm; convert links to root-relative.
5. Responsive passes (`responsive-audit.py`); set mobile sizes/padding.

## Rules

Work within Elementor and the existing kit. Don't break working layout. Keep the JSON
complete and valid (see `full-output-enforcement`).
