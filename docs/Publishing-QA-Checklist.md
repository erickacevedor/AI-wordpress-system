# Publishing & QA Checklist

Run this before any AI-built page or post goes live. It's the final gate that takes
content from AI draft to published, consistent, and clean. Works for every site.

> **Run the machine half first:** `python3 scripts/validate-page.py <page>.json`.
> It already enforces the structural, responsive, link, alt-text and id items below,
> and warns on band rhythm, padding discipline and over-long meta. Items it cannot
> reach — does the copy read right, is the live widget wired up, do the links point at
> the pages you meant — are the ones that need your eyes. Items marked 🤖 are checked
> for you; the rest are yours.

## 1. Brand & structure
- [ ] 🤖 Every section is **Section -> Content Container -> content** (padding only on
      the Content Container; children have none).
- [ ] 🤖 Section backgrounds alternate correctly (no two identical in a row) *(warning)*.
- [ ] Correct brand font throughout (no leftover theme default like Noto Sans Coptic).
- [ ] 🤖 Text is readable on its background (WCAG AA) *(warning — a brand's own palette
      can fail, which is a decision to make, not a build bug)*.
- [ ] CTAs use the brand button style; hover changes color only (no size/shape animation).
- [ ] Colors set inline, not via Elementor global slots.

## 2. SEO elements
- [ ] 🤖 Exactly **one H1** (the hero headline); headings follow H1 -> H2 -> H3 with no skipped levels.
- [ ] 🤖 **Meta title** set, under ~60 characters *(length-checked in `HANDOFF-notes.md`)*.
- [ ] 🤖 **Meta description** set, under ~155 characters *(length-checked in `HANDOFF-notes.md`)*.
- [ ] **URL slug** lowercase, hyphenated, concise.
- [ ] Target keyword appears naturally in the H1 and intro paragraph.
- [ ] SEO meta entered in the site's SEO plugin (Rank Math / Yoast) at the WP page level.

## 3. Internal linking
- [ ] Required internal links present, with descriptive anchor text (not "click here").
- [ ] 🤖 No dead links (`#` or empty); CTAs point to real destinations.
- [ ] External links behave as intended.

## 4. Images & media
- [ ] 🤖 Every image has **alt text** — that it is *descriptive* is still your call.
- [ ] Hero/feature images placed (two-column or background with overlay for legibility).
- [ ] 🤖 Live/dynamic widgets (review sliders, forms, advanced maps) wired up — the
      import placeholders replaced with the real widgets/shortcodes. *(The gate lists
      what the target install must provide; put that list in the handoff.)*
- [ ] Featured image set (especially for posts).

## 5. Responsive & functional
Audit these in the JSON *before* import (each has an explicit per-breakpoint setting),
then confirm visually in Elementor's tablet + mobile preview:
- [ ] **Grids stack:** every grid container has `grid_columns_grid_tablet` (~2) and
      `grid_columns_grid_mobile` (1) — not just the desktop `grid_columns_grid`.
- [ ] **Rows stack:** every multi-column flex row (`flex_direction: row`/`row-reverse`)
      sets `flex_direction_mobile: column`.
- [ ] **Columns go full width:** any container with a `%` `width` also sets
      `width_mobile` (usually 100%) — and `width_tablet` where the layout needs it.
- [ ] **Headings shrink:** H1 and every section H2 carry
      `typography_font_size_mobile` (and ideally `_tablet`). A heading pointing at a
      global typography slot with no mobile size does **not** shrink — give it
      self-contained responsive sizes instead.
- [ ] **Container padding:** the boxed content container has a smaller
      `padding_mobile` (heavy desktop vertical padding is uncomfortable on phones).
- [ ] **Images:** fixed-height images set `height_mobile` so they don't crop oddly.
- [ ] **Emoji icons:** if used as icons, they carry a mobile font size too.
- [ ] Accordions/toggles, maps, and forms work; page previewed on desktop + mobile.

> Tip: run `python3 scripts/responsive-audit.py <page>.json` — it walks the JSON and
> flags any grid/row/%-column/heading/container/image missing its `*_mobile` /
> `*_tablet` key. Exit code 1 = issues, so it works as a pre-import gate.

## 6. Publish steps
1. Import the template (Elementor -> Templates -> Import Templates) or insert onto the page.
2. Assign the site header and footer if not inherited.
3. Set the URL slug and SEO meta (title/description) in the SEO plugin.
4. Set the featured image; for posts, set category/tags and author.
5. Publish.
6. Load the live URL and re-check items 1-5 on the published page.

---
*Tick every box before publishing. This is what "consistent, repeatable, low-cleanup"
looks like in practice.*
