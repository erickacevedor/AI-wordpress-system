---
name: gcreliable-page-builder
description: >
  Orchestrates fast creation of a new G.C. Reliable Service (gcreliable.com)
  Elementor page from a content brief or doc. Use whenever the user says
  "build/create a GC Reliable page", "make a page from this doc", "new AC
  installation / ductless / heating page", or hands over copy to turn into an
  Elementor page. Runs the full pipeline: design-read → content → design →
  complete JSON → validate.
---

# G.C. Reliable Page Builder

The one entry point for turning a content brief into an import-ready G.C. Reliable
Elementor page.

**Input:** a content doc/brief (usually a `.docx` in
`projects/gcreliable/pages/<slug>/`).
**Output:** `projects/gcreliable/pages/<slug>/<slug>.json` + `build.py` +
`PREVIEW.html` + `HANDOFF-notes.md`.

## Pipeline (run in order)

1. **Design read** — apply `gcreliable-design-read`. Name the page kind, confirm the
   reference page (`current-theme/content/page/225063.json`, "AC Repair"), state the
   one-line read, note the kit gotchas.
2. **Extract the source.** For a `.docx`: unzip `word/document.xml`, strip tags,
   un-escape entities, write `source.txt` beside it. Watch for mojibake — the exports
   contain curly quotes that arrive as `?`/`�`; restore them as `&rsquo;`/`&mdash;`.
3. **Map content to the page anatomy** (drop what the doc doesn't have; don't invent
   filler):

   | # | Band | Section |
   |---|------|---------|
   | 1 | gradient | Hero: H1 (service + city) + sub-line + red CTA |
   | 2 | white | Intro row: H2 + 2–3 paragraphs + CTA │ photo with the floating stat badge |
   | 3 | `#EFF2F5` | Qualifier: H2 + lead, two-column — FA check list │ white card (warning / secondary list) + de-escalation paragraph |
   | 4 | white | Service split: two emoji cards (e.g. New Install │ Replacement, or Install │ Repair │ Maintenance) |
   | 5 | `#EFF2F5` | Decision factors: two-column info cards (sizing, ductwork / single-zone, multi-zone) |
   | 6 | white | Process: 4–5 numbered blue-bar cards at 48% width |
   | 7 | `#EFF2F5` | FAQ: Pro `accordion` (62%) │ "Still Have Questions?" white card (34%) |
   | 8 | white | Reviews: H2 + lead + dashed band with the Trustindex shortcode + stat trio |
   | 9 | gradient | Why trust us: H2 + paragraph + FA check list │ photo + badge |
   | 10 | `#EFF2F5` | Closing CTA: H2 + paragraph + red CTA |

   Keep the band alternation intact if you drop a section — never two identical
   bands in a row.
4. **Write/polish copy** — apply `gcreliable-content-style`. Keep the source doc's
   substance and hedging; tighten to the section shapes.
5. **Style to the system** — apply `gcreliable-ui-design`. Build through
   `scripts/elementor_builder.py` from a `pages/<slug>/build.py` that reads
   `../../tokens.json`, so the page is reproducible and the responsive gates are
   baked in. Brand-styled thin wrappers (`h1/h2/h3/body/btn/check_list/step_card/
   photo_badge/faq/review_band`) go at the top of `build.py`.
6. **Emit complete JSON** — apply `full-output-enforcement`. Unique ids, all required
   keys, valid escaping, UTF-8, single-page wrapper with
   `page_settings = {"template":"elementor_header_footer","hide_title":"yes"}`.
   **No `display_condition_list`.**
7. **SEO, links & media** — one H1 + clean hierarchy; 3–6 root-relative internal
   links with descriptive anchors; slug + meta title + meta description recorded in
   `HANDOFF-notes.md`; images with alt text; note any image intended to be swapped
   post-import.
8. **Validate (required gate)** — `python3 scripts/validate-page.py <page>.json` must
   exit 0, then apply `gcreliable-page-audit`.

## Escape hatches the library needs for this site

`elementor_builder.py` is deliberately generic; three of this kit's patterns need a
local helper in `build.py`:

- **Pro `accordion`** — the library's `accordion()` emits `nested-accordion`. Write a
  small `faq()` that emits `widgetType: "accordion"` with a `tabs` array.
- **Button extras** — `size: "xl"`, `_element_width: "auto"`, `selected_icon`,
  `icon_indent`, and the hover colors go through the spec's `colors` dict so
  `icon_align` is *not* forced (the kit leaves it default).
- **Photo + floating badge** — a raw `container()` pair with `background_image`,
  negative `margin`, and `z_index`, since it isn't a generic primitive.

## Fastest path (reuse over rebuild)

Adapt the AC Repair page's **section model and styling values verbatim**; only the
copy and the section mix change. Regenerate all element ids (`E.reset_ids(seed)`
with a distinct seed per page). Never copy the legacy text-blob pages.

## Deliverable & handoff

Tell the user: Elementor → Templates → Import Templates → upload the JSON → open the
imported page → publish at the target slug. List post-import wiring: SEO meta +
slug, header/footer confirmation, image swaps, Trustindex widget id check.

## Guardrails

- Match the kit; don't redesign it. Square red button, colour-only hover.
- Root-relative `/systems/...` links only.
- Emit complete JSON — no elisions.
- If a brand-critical fact is missing (hero headline, city, CTA target), ask one
  focused question rather than guessing.
