# Publishing & QA Checklist

Run this before any AI-built page or post goes live. It's the final gate that takes
content from AI draft to published, consistent, and clean. Works for every site.

## 1. Brand & structure
- [ ] Every section is **Section -> Content Container -> content** (padding only on
      the Content Container; children have none).
- [ ] Section backgrounds alternate correctly (no two identical in a row).
- [ ] Correct brand font throughout (no leftover theme default like Noto Sans Coptic).
- [ ] CTAs use the brand button style; hover changes color only (no size/shape animation).
- [ ] Colors set inline, not via Elementor global slots.

## 2. SEO elements
- [ ] Exactly **one H1** (the hero headline); headings follow H1 -> H2 -> H3 with no skipped levels.
- [ ] **Meta title** set, under ~60 characters.
- [ ] **Meta description** set, under ~155 characters.
- [ ] **URL slug** lowercase, hyphenated, concise.
- [ ] Target keyword appears naturally in the H1 and intro paragraph.
- [ ] SEO meta entered in the site's SEO plugin (Rank Math / Yoast) at the WP page level.

## 3. Internal linking
- [ ] Required internal links present, with descriptive anchor text (not "click here").
- [ ] No dead links (`#` or empty); CTAs point to real destinations.
- [ ] External links behave as intended.

## 4. Images & media
- [ ] Every image has descriptive **alt text**.
- [ ] Hero/feature images placed (two-column or background with overlay for legibility).
- [ ] Live/dynamic widgets (review sliders, forms, advanced maps) wired up — the
      import placeholders replaced with the real widgets/shortcodes.
- [ ] Featured image set (especially for posts).

## 5. Responsive & functional
- [ ] Multi-column rows stack correctly on tablet/mobile.
- [ ] Heading/body sizes readable on mobile.
- [ ] Accordions/toggles, maps, and forms work.
- [ ] Page previewed on desktop and mobile.

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
