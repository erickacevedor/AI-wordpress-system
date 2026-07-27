---
name: magnolia-page-builder
description: >
  Orchestrates fast creation of a new Magnolia Air Elementor page from a content
  brief or doc. Use whenever the user says "build/create a Magnolia page", "make a
  page from this doc", "new AC/service page", or hands over copy to turn into an
  Elementor page. Runs the full pipeline: design-read → content → design → complete
  JSON → responsive audit, reusing the kit's brand.
---

# Magnolia Air Page Builder

The one entry point for turning a content brief into an import-ready Magnolia Air
Elementor page. Sequences the other Magnolia skills so a page comes out on-brand,
complete, and responsive in one pass.

**Input:** a content doc/brief (page type, location, hero, sections, FAQ, CTA).
Missing pieces are inferred from the closest existing page or one focused question.

**Output:** a single-page Elementor JSON saved to `projects/magnolia/output/<slug>.json`,
plus a `PREVIEW.html` and `HANDOFF-notes.md`. Import via Elementor → Templates →
Import Templates.

## Pipeline (run in order)

1. **Design read** — apply `magnolia-design-read`: page kind, closest existing page,
   state the one-line read. Note the ⚠️ `display_condition_list` gotcha and
   root-relative links.
2. **Map content to sections** — turn the doc into the Magnolia anatomy:
   dark-teal hero (h1 + intro + 24/7 call-out + gold CTA) → alternating
   cream/white/teal bands → **service card grid** (emoji cards linking to each
   service page) → **two-column** home/business split → symptom "when to call" +
   CTA → "why trust" list on a teal band → emergency call-out on a dark band → FAQ
   accordion → teal closing CTA. Drop sections the doc doesn't need; don't invent
   filler.
3. **Write/polish copy** — apply `magnolia-content-style`: local Central Louisiana
   framing, right-service honesty, both audiences, plain low-pressure voice.
4. **Style to the system** — apply `magnolia-ui-design`: **every section = full-width
   Section → one boxed (~1140px) Content Container → content**, padding only on the
   container; teal/gold palette via real globals; Como + BeVietnamPro; gold pill CTAs
   with the `shrink` hover; **emoji icons** mixed in; layout variety.
5. **Emit complete JSON** — apply `full-output-enforcement`: full tree, unique `id`s,
   all required keys, every repeated widget written out, valid braces/escaping, UTF-8.
   Single-page wrapper `{version,title,type:"page",content,page_settings}`. **Do not**
   emit any `display_condition_list`.
6. **SEO, links & media** — one H1 + clean hierarchy; carry slug / meta title /
   meta description as a publish-time handoff note; root-relative internal links with
   descriptive anchors (`/ac-repair/`, `/ac-maintenance/`, `/ac-installation/`,
   `/ac-replacement/`, `/request-service/`); images with alt text; note the hero
   image as a swap-me placeholder.
7. **Audit** — apply `magnolia-page-audit`, then run
   `python3 scripts/responsive-audit.py <page>.json` (must exit 0) and confirm the
   JSON parses.

## Fastest path (reuse over rebuild)

Prefer adapting the closest existing page's **content model** (e.g. an "AC Services
In <City>" page) — but rebuild it clean to this system, since kit pages are thin,
text-only, and carry the subscriber-gate. Regenerate all element `id`s. Keep the
brand palette/button/rhythm.

## Deliverable & handoff

Save JSON + PREVIEW.html + HANDOFF-notes.md to `projects/magnolia/output/`. Tell the
user the import path and list post-import wiring (swap hero image + alt, confirm
slugs, header/footer, SEO meta). Note which existing page it was based on.

## Guardrails

- Match the kit; don't redesign it.
- Never copy `display_condition_list` (it hides content).
- Use root-relative links (kit URLs are localhost) and treat `moesalley.com` image
  URLs as swap-me placeholders.
- If the brief lacks a hero headline, location, or CTA target, ask one question
  rather than guessing brand-critical facts.
