---
name: midlakes-page-audit
description: >
  Pre-delivery audit for a Mid Lakes Heating & Cooling (Loganville, GA HVAC)
  Elementor page. Use after building or restyling a Mid Lakes page, and whenever
  reviewing an existing one, to check fidelity to the HTML prototype, structure,
  responsiveness, links, and import hygiene before handoff. Carries an explicit
  "do NOT fix" list of the design's deliberate decisions. Triggers: "audit this Mid
  Lakes page", "is this faithful to the prototype", "review before import",
  "check the Mid Lakes page".
---

# Mid Lakes — Page Audit

Run this as the last step before handoff, and any time you're asked to review a Mid
Lakes page. The reference for every "should look like" question is the prototype file
itself: `D:\laragon\www\midlakes\public\<page>\index.php` + `styles.css`.

## 0. The objective gate (run it first)

```
python3 scripts/validate-page.py projects/midlakes/pages/<slug>/<slug>.json
```

Must exit **0**. It covers: JSON parses, single-page wrapper, unique ids, exactly one
H1, no `display_condition_list`, no dead/`localhost` links, and the full responsive
audit. Errors block. **Warnings are real findings** — read every one and either fix it
or say in the report why it stands.

Then generate and open `PREVIEW.html`, and compare it side by side with the prototype
page at 1440px and at 390px. The target site is not reachable; the preview and a local
throwaway WordPress (`scripts/sandbox.sh`) are the verification.

## 1. ⚠️ Do NOT "fix" these — they are deliberate

Every item here looks like a defect and is not. Check this list before flagging
anything.

- **Two identical bands adjacent.** `/about-us/` runs `about`(white) → `why`(white);
  `/service-agreements/` runs `about`(white) → `about what-happens`(white); `/blog/`
  runs `hero-compact`(paper) → `services`(paper). The prototype ships all three.
- **27 distinct font sizes.** Not collapsed, on purpose — `build.py` emits them
  programmatically, so exactness costs nothing (PORT-DECISIONS decision 8).
- **Both `/financing/` CTAs point at `#contact`**, not at Service Finance. A settled
  decision, not a placeholder to chase.
- **There is no `/contact` page.** The contact band repeats on every page and every
  contact link is the `#contact` anchor. The footer menu points there too.
- **Header says "About"; footer says "About Us".** The prototype renders them
  differently and the install's menus already match.
- **The header phone is not a menu item.** It is a styled red bold link inside the
  nav (`.nav-phone`) and belongs in the header template.
- **`.site-footer` carries 300px of bottom padding.** It exists only to clear the
  footer watermark. Do not trim it *unless* the watermark is also gone.
- **The brand primary is blue, the CTA is red.** Separate slots, no conflict. A red
  "primary" is not a bug.
- **`#8fb2d8` is low-contrast on white (2.20:1)** — it is only ever used on the navy
  band, where it is 8.50:1. Same for `#ff8b8b` and `#6fb3ec`. The design chose these
  knowingly and documented the ratios in source comments.
- **`#c10a0a` on white is 6.33:1** — passes AA for body text and is used as a text
  colour on light bands deliberately.
- **`.what-happens.about` has no watermarks.** Suppressed on purpose.
- **Elementor's editor won't restyle capped properties** — the button's hover lift,
  the Fraunces numerals, the `clamp()` heads, the rate table, the watermarks, the
  header blur. The client chose fidelity over editability with that consequence
  stated.
- **The SEO title/description run past 60/155 characters on most pages.** They are
  the prototype's own hand-written locality-targeted strings, kept verbatim.
  `validate-page.py` warns. **Do not shorten them** — rewriting existing content is a
  client call, not a port decision. Raise it when the SEO plugin is chosen.
- **`/service-area/` nests h3 inside h3** — a column heading above a `.promise` list
  whose items are also h3. That is the prototype's markup, and levels do not *skip*,
  so it is valid. Do not "fix" it to h4.
- **The kit's base typography is Manrope and that is correct.** Only `system_colors`
  is still stock. Fonts from the kit, colours inline.

## 2. Brand fidelity

- [ ] Palette is blue `#2540af` / red `#c10a0a` / navy `#0f1f35` / text `#1a2436` /
      muted `#5a6472` / hairline `#dde3ec` — **no** other accent introduced.
- [ ] Bands are the inline hexes `#ffffff` / `#f4f6f9` / `#0f1f35`.
- [ ] **No `__globals__` colour refs anywhere.** `system_colors` is still stock
      Hello, so a global colour slot silently renders Hello's default. (Font globals
      are fine — the kit's base typography IS Manrope.)
- [ ] On the ink band, red text is `#ff8b8b` and blue text is `#6fb3ec` — **never**
      `#c10a0a` or `#2540af`.
- [ ] Band order matches this page's row in `midlakes-ui-design`, including any
      deliberate double.
- [ ] `Manrope` is the only `typography_font_family` except on `.why-num` /
      `.step-num` / `em`, which are `Fraunces` italic 500.
- [ ] Every heading is weight 800, `line-height 1.1`, `letter-spacing -0.02em`.
- [ ] Every heading size is in **`rem`** — check for a heading rendering at
      single-digit pixels (footgun 2).
- [ ] The section title block is capped at 720px with 48px below it.

## 3. The button

- [ ] Red fill `#c10a0a`, white text, 1.5px border, radius **999px**, padding 14/26,
      Manrope 0.95rem / 700, no text-transform.
- [ ] Hover fill `#a30808`; **no `hover_animation`** (no `grow`, `float`, `shrink`).
      The 2px lift is CSS-owned.
- [ ] The key is **`background_color`** — grep the JSON for
      `button_background_color`, which is the footgun spelling and fails silently.
- [ ] `__globals__` on the button is **empty**.
- [ ] `_css_classes` carries `ml-btn ml-btn-primary` (or `ml-btn-ghost`), so the
      stylesheet's `.ml-btn .elementor-button:hover` can reach the anchor.
- [ ] Ghost buttons appear **only** on the hero and comfort photo bands.
- [ ] Links are root-relative or `#contact`; nothing absolute, nothing `localhost`.

## 4. Structure

- [ ] Every section = full-width Section (background only) → **one** boxed container
      (`boxed_width` **1200px**) → content.
- [ ] Padding lives on the boxed container (`96/24/96/24`, mobile `64/24/64/24`;
      `.comfort` `120`/`80`; heroes per `midlakes-ui-design`) and on self-contained
      cards — nowhere else.
- [ ] No lone widget double-wrapped in a redundant container.
- [ ] Card values match: radius **14**, 1px `#dde3ec`, service/why cards
      `min_height: 350`, why-card fill is **paper** on the white band, form card is
      `#17293f` with a `rgba(255,255,255,.08)` border.
- [ ] Layout variety matches the prototype — the detail rows, the grids, the map
      split, the accordion. Not a stack of single-column text blocks.

## 5. The alternations (the thing that silently drifts)

- [ ] Service icon tiles run **red, blue, red, blue, red, blue** across the 6-up grid.
- [ ] `.why-num` numerals run **red, blue, red, blue** (odd is red).
- [ ] `.step-num` numerals run **red, blue, red, blue** (odd is red).
- [ ] On `/services/`, the **flipped** detail rows carry the blue spec card.
- [ ] The **last** item of `.stats`, `.area-list` and the rate table's `tbody` drops
      its bottom hairline.
- [ ] The **first** `.detail-row` has no top border and 8px of top padding.

## 6. Watermarks

- [ ] The right CLASS is on the right band: `ml-wm-waves` on `.about` **only** (never
      on `.why`), `ml-wm-card-1` on service cards, `ml-wm-card-4` on why/spec cards,
      `ml-wm-contact` on the contact band, `ml-footer` on the footer.
- [ ] `build.py` emits **no watermark background images at all** — these are CSS
      pseudo-elements in the child theme. A `background_image` where a watermark
      belongs means someone re-litigated a settled decision.
- [ ] `.what-happens` sections carry **none** — built with
      `sec_about(watermark=False)`, i.e. suppression by omission.
- [ ] `.why` sections carry none either — `sec_why()`, not `sec_about()`.
- [ ] The SVGs are referenced as **child-theme assets**, not media-library
      attachments (WordPress blocks SVG uploads by default).
- [ ] If the footer watermark was dropped, the 300px bottom padding went with it.

## 7. Icons

- [ ] The six service icons come from the child theme's inline SVG sprite via `html`
      widgets — no CDN link, no icon-font substitute for these six.
- [ ] Check lists use `fas fa-check-circle` at 18px, `#c10a0a` (or `#2540af` on a blue
      spec card).
- [ ] **Emoji icons appear somewhere too** — no page depends entirely on one icon
      source. JSON saved UTF-8, emoji intact (not `?` or mojibake).

## 8. Responsive (beyond what the script checks)

- [ ] **H1 and every H2** carry `typography_font_size_mobile` (2.4rem / 1.8rem) **and**
      `typography_typography: "custom"` — without the latter, Elementor emits no CSS
      at all and the gate still passes (footgun 3).
- [ ] Grids set tablet **and** mobile column counts; the 6-up service grid goes 3 → 2
      (≤1024) → 1 (≤767).
- [ ] Every flex row sets `flex_direction_mobile: column`; every %-width column sets
      `width_tablet` and `width_mobile: 100%`.
- [ ] Every boxed container has `padding_mobile`; every fixed-height image has
      `height_mobile`.
- [ ] Prototype-specific mobile values are carried: `.gallery-tall` 3/5 → **16/10**,
      hero buttons full-width, the field row 1-up, the form card padding 26/22, the
      footer 3 → 2 → 1 column, hero creds 0.88rem.
- [ ] The rate table's `<620px` card stacking is present in the cap's CSS, not lost.

## 9. Copy & SEO

- [ ] For an existing page: the copy is the prototype's, **verbatim**, entities
      intact (`&rsquo;`, `&mdash;`, `&ndash;`, `&reg;`).
- [ ] Voice matches `midlakes-content-style`: neighbourly, de-escalating, hedged,
      locally specific, no hype.
- [ ] Only the earned proof points appear — 2018 / 75+ combined / 24/7 live /
      licensed & insured / Parts & Labor / free estimates / 300+ members / NATE /
      EPA 608 / `#CR108663`.
- [ ] **"a Carrier® dealer" — never "Carrier Factory Authorized Dealer".** No Rheem.
- [ ] Exactly one H1; H2/H3 in a clean hierarchy with no skipped levels.
- [ ] Internal links are root-relative with descriptive anchors; contact is
      `#contact`.
- [ ] Slug, meta title and meta description from `tokens.json → pages.seo` are
      recorded in `HANDOFF-notes.md`, along with the canonical URL.
- [ ] Every image carries the prototype's `alt` text verbatim.
- [ ] Every CTA has a visible descriptive label — none icon-only. Nothing auto-plays.
      Every form field has a real `<label>`.

## 10. Import hygiene

- [ ] Wrapper `{version, title, type: "page", content, page_settings}` with
      `page_settings = {"template":"elementor_header_footer","hide_title":"yes"}`.
      Theme templates instead validate as `type: "header"` / `"footer"` and carry
      **no** H1.
- [ ] **No `display_condition_list`**, no `display_settings`/`location` keys.
- [ ] Element ids are unique across the page (`E.reset_ids(seed)` with a seed
      distinct from every other Mid Lakes page).
- [ ] Images either use a real attachment id from `media.json` or are flagged in the
      handoff as a post-import swap — the media library is currently **empty**.
- [ ] The quote form references the shared Pro Form template rather than rebuilding
      the fields inline.
- [ ] The page's slug matches its existing stub (pages 10–16). Do not renumber them.

## Reporting

State pass/fail per group with the specific offending element id or section index —
not a general impression. Where the page departs from the prototype, say so and say
why; if the reason isn't in §1's do-NOT-fix list or `PORT-DECISIONS.md`, it is a bug,
not a decision. Fix it rather than explaining it away.
