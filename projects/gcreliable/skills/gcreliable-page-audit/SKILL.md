---
name: gcreliable-page-audit
description: >
  Pre-delivery audit for a G.C. Reliable Service (gcreliable.com) Elementor page.
  Use after building or restyling a GC Reliable page, and whenever reviewing an
  existing one, to check brand fidelity, structure, responsiveness, links, and
  import hygiene before handoff. Triggers: "audit this GC Reliable page", "is this
  on brand", "review before import", "check the page".
---

# G.C. Reliable — Page Audit

Run this as the last step before handoff, and any time you're asked to review a
GC Reliable page. Reference for every "should look like" question:
`current-theme/content/page/225063.json` ("AC Repair").

## 0. The objective gate (run it first)

```
python3 scripts/validate-page.py projects/gcreliable/pages/<slug>/<slug>.json
```

Must exit 0. It covers: JSON parses, single-page wrapper, unique ids, exactly one
H1, no `display_condition_list`, no dead/`localhost` links, and the full responsive
audit. Anything it flags is a blocker — fix it, don't explain it away.

## 1. Brand fidelity

- [ ] Palette is blue `#0033CC` / red `#FF0000` / `#1A1A1A` text — **no** other
      accent color introduced.
- [ ] Band tints are the inline hexes `#EFF2F5` / `#E6ECFA` / `#F8F8FB`, not a
      guessed global id.
- [ ] Hero and the "why trust" band use the linear **135° `#0033CC → #001E78`**
      gradient.
- [ ] Bands alternate; no two identical backgrounds adjacent.
- [ ] `brandon-grotesque` is the only `typography_font_family` on the page.
- [ ] Body `text-editor` widgets carry **no** typography settings (they inherit the
      global *Normal Text*).
- [ ] Every heading has `letter-spacing: 0.5px`; H1 is uppercase 800 at 3.4rem.

## 2. The button

- [ ] Red fill, white text, 2px red border, **square** corners, `size: "xl"`.
- [ ] Hover: background + border `#FF6464`, text white, transition `0s`.
- [ ] **No `hover_animation`** (no `shrink` — that's a different site).
- [ ] `far fa-calendar-check` with `icon_indent: 10`; `icon_align` left at default.
- [ ] Links to `/schedule-appointment` (or the brief's target), root-relative.

## 3. Structure

- [ ] Every section = full-width Section (background only, `flex_align_items:
      center`) → **one** boxed container (`boxed_width` 1280, laptop 92%,
      tablet/mobile 100%) → content.
- [ ] Padding lives on the boxed container (`64/20/64/20`, hero `90`, gradient CTA
      `68`) and on self-contained cards — nowhere else.
- [ ] No lone widget double-wrapped in a redundant container.
- [ ] Layout variety: at least one two-column row, one multi-card row/grid, and the
      accordion. Not a stack of single-column text blocks.
- [ ] Signature components match the reference: photo + floating red-bordered badge,
      `fad fa-check-circle` icon lists, `#F8F8FB` numbered cards with the 4px blue
      left bar, white radius-12 cards with the `0 10 30 -10` shadow, dashed review
      band, stat trio.

## 4. Icons

- [ ] FA Pro icons used the way the kit uses them (`fad fa-check-circle` lists,
      `fas` icon widgets at 40px blue).
- [ ] **Emoji icons appear too** — the page must not depend entirely on the icon
      font. JSON saved UTF-8, emoji intact (not `?` or mojibake).

## 5. Responsive (beyond what the script checks)

- [ ] The intro row stacks **copy-first** on tablet/mobile
      (`flex_direction_tablet/_mobile: column-reverse` when the photo is on the right).
- [ ] The floating badge's negative margin has a mobile value (`-40`) and its width
      goes to ~82% on mobile.
- [ ] Wrapping card rows have `flex_gap_mobile` (~28) so cards don't crowd.
- [ ] Photo containers have `min_height_mobile`.

## 6. Copy & SEO

- [ ] Voice matches `gcreliable-content-style`: advisory, hedged, locally specific,
      no hype, no unearned promises or invented certifications/brands.
- [ ] Only the established proof points appear: since 1980 / 40+ years / 24/7
      emergency / all makes and models / New Rochelle + Westchester County.
- [ ] Exactly one H1; H2s and H3s in a clean hierarchy with no skipped levels.
- [ ] 3–6 internal links, root-relative `/systems/...`, descriptive anchors, **no**
      `/amana/...` or `/services/...` legacy paths, no absolute `gcreliable.com` URLs.
- [ ] Slug, meta title, and meta description are recorded in `HANDOFF-notes.md`.
- [ ] Every image has meaningful `alt` text.

## 7. Import hygiene

- [ ] Wrapper `{version, title, type: "page", content, page_settings}` with
      `page_settings = {"template":"elementor_header_footer","hide_title":"yes"}`.
- [ ] No `display_condition_list`, no `display_settings`/`location` keys copied from
      kit templates.
- [ ] Trustindex shortcode id is the current one
      (`be35b8a27428268b9b962ab1e27`) unless the brief supplies another.
- [ ] Referenced media either uses a real attachment id from the kit or is flagged
      in the handoff as a post-import swap.

## Reporting

State pass/fail per group with the specific offending element id or section index —
not a general impression. If something deliberately departs from the reference
page, say so and say why; otherwise fix it.
