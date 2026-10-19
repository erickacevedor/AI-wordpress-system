---
name: lenz-page-audit
description: >
  Brand, content and Elementor-hygiene audit for Lenz Heating & Cooling pages, with
  the list of deliberate design choices that must NOT be "fixed". Use before
  delivering any Lenz page or component, when reviewing feedback on one, or when
  asked to "audit/review/QA a Lenz page". Triggers: "audit the Lenz page", "QA
  Lenz", "check this Lenz page", "review Lenz feedback".
---

# Lenz: Page Audit

Run on the built JSON **and** the rendered page. Report findings; fix them in
`build.py`, a block in `service_page.py` / `brand.py`, or the design-source CSS,
never in the output files.

## 1. Gate

- `python3 scripts/validate-page.py projects/lenz/pages/<slug>/<slug>.json` exits 0.
- The build did not raise ("plan uses N sections, doc has M" means doc content was
  dropped or duplicated).

## 2. Brand and structure

- [ ] Built from existing blocks; no inline colours, fonts, padding or hover
      animations in widget settings (only what `brand.py` sets: heading sizes, the
      form colours, and the zero padding of the boxed container).
- [ ] Every class on the page exists in `lenz-core.css` (a class with no rule is a
      typo or a component that was never ported). Known hook classes with no rule
      of their own are fine: `e-no-lazyload`, `svc-page`, `pair`, `trustbar--<n>`,
      `promo-section`.
- [ ] `cat` matches the service family; all blocks carry the same `svc-page--<cat>`.
- [ ] No two identical light backgrounds back to back **where a `bg` option could
      avoid it** (see `lenz-ui-design` section 3; `faq` then related services is
      expected).
- [ ] Buttons: gold on dark, primary on light; labels describe the action; every CTA
      goes to `#contact` or its documented target; phone CTAs use `tel:+15152256446`.
- [ ] Promo boxes: copy first, button below. Help tiles: phone with the text.
- [ ] Icons from the sprite only; images from `media.json` with specific alt text.

## 3. Content

- [ ] Copy matches the doc verbatim except the ClickUp fixes listed in
      `HANDOFF-notes.md`, and every self-written string is in `notes`.
- [ ] None of the retired claims (see `lenz-content-style` section 3): no free
      second opinions, no free diagnostics, no "no trip or diagnostic fees",
      discounts on parts only, 2,000 reviews, "Main Office".
- [ ] Paragraph order makes sense when read top to bottom (a list intro like
      "includes:" must be followed by its list, not by another paragraph).
- [ ] No links to pages in `brand.OUT_OF_SCOPE`.

## 4. Accessibility

- [ ] One H1; H2 per section; H3 in cards; no skipped levels.
- [ ] No icon-only CTA; form fields have real labels (the estimate form does).
- [ ] Iframes have a `title`; nothing autoplays.
- [ ] Focus is visible on every interactive element (CSS-owned two-ring outline).

## 5. Rendered check

- [ ] 1440, 1024, 768 and 390: no horizontal scroll, nothing clipped.
- [ ] Compared against the reference page: same hero, trustbar, band and card
      treatment.
- [ ] If CSS changed: every page that uses the touched class was re-checked, not
      just the page that prompted the change.
- [ ] On staging, the Flywheel cache was flushed before judging (otherwise the old
      CSS version is served).

## 6. Do NOT "fix" these (deliberate)

1. **Style in CSS, not in Elementor.** The panel's style controls are unused on
   purpose. Do not "make it editable" by moving styles into widget settings.
2. **No emoji icons.** The repo-wide rule to mix emoji does not apply: Lenz ships
   its own inline SVG sprite (no icon font to fail), and sprite icons inherit
   `currentColor`, which the eyebrow contrast rule depends on.
3. **Gold never carries white text**; orange-500 is display only; eyebrows are rust
   on light surfaces.
4. **Trust proofs live in the trustbar.** The hero carries only what the reference
   has (home: the star line to Google reviews; other pages: the photo badge). Do
   not add trust chips. A proof repeated in the doc's own copy (for example "To
   the Penny" in the trustbar and a why card) stays: the doc wins.
5. **Button hover is a `-1px` lift**, not Elementor's grow/shrink.
6. **"Services" in the nav is a label, not a link.**
7. **Reviews are hardcoded** until the GBP Place ID exists; no `aggregateRating`
   anywhere until verified Google data loads.
8. **`prefers-reduced-motion` blocks** (marquee frozen to a wrapped grid) stay.
9. **The FAQ, marquee, maps and videos are html widgets** with prototype markup.
    That is intended; edit them in the build.
10. **Gate warnings about identical backgrounds** are expected: bands are classes the
    gate cannot see.
11. **The meta description avoids "no trip or diagnostic fees"** even where the doc
    has it (ClickUp 09/10).

## Output

List findings as: page, block, what is wrong, where it must be fixed (build, block,
CSS source), and whether it is a brand rule, a ClickUp rule or an accessibility
rule. Separate confirmed findings from things you could not verify.
