---
name: vitalair-page-builder
description: >
  Orchestrates fast creation of a new VitalAir Elementor page from a content
  brief. Use whenever the user says "build/create a VitalAir page", "make a page
  from this doc/brief", "new service/service-area/FAQ/landing page", or hands over
  page copy to turn into an Elementor page. Runs the full pipeline: design-read →
  content → design → complete JSON → audit, reusing the existing kit and templates.
---

# VitalAir Page Builder

The one entry point for turning a content brief into an import-ready VitalAir
Elementor page. It sequences the other VitalAir skills so a page comes out
on-brand and complete in one pass.

**Input:** a content brief (see `content-brief-template.md`), or any doc/paste of
page copy. If the brief is missing pieces, infer from the closest existing page or
ask one focused question.

**Output:** an Elementor-importable page JSON saved to the kit (e.g.
`content/page/<id>.json`), styled inline to the brand, ready to import via
Elementor → Templates → Import, or Site Settings → Import Kit.

## Pipeline (run in order)

1. **Design read** — apply `vitalair-design-read`. Identify page kind, find the
   closest existing page/template to mirror (AC Repair `2327`, Cooling Services,
   Service-Marietta `1913`, FAQ `2353`, Promo Landing `2289`, etc.), decide
   Container vs. Section (default: Container). State the one-line read.
2. **Map content to sections** — turn the brief into the standard anatomy:
   navy hero (eyebrow + h1 + intro + CTA) → alternating white/`#EEF2FA` content
   bands → icon-box/feature grids → FAQ accordion → closing CTA band. Drop any
   section the brief doesn't need; don't invent filler.
3. **Write/polish copy** — apply `vitalair-content-style`: local Atlanta framing,
   plain reassuring voice, "symptom → reassurance → CTA" service paragraphs,
   brand CTA phrasings. Never web-startup hype.
4. **Style to the system** — apply `vitalair-ui-design`: build **every section as
   Section → Content Container → content**, with padding ONLY on the Content
   Container (default padding; children and nested containers get zero padding).
   Inline colors (navy `#16163F` hero, alternating `#FFFFFF`/`#EEF2FA`, green
   `#74BC2B` pill CTAs with **no hover size/shape animation** — color-change
   only), Poppins, the type scale, green uppercase eyebrows, boxed ~1200px text
   width. Reuse header `10` and footer `181`.
5. **Emit complete JSON** — apply `full-output-enforcement`: full tree, unique
   `id`s, all required keys (`elType`/`widgetType`/`elements`/`settings`), every
   repeated widget written out, valid braces/escaping. No truncation.
6. **SEO, links & media** — set the page's H1 (one only) and heading hierarchy;
   carry the slug / meta title / meta description from the brief as a publish-time
   handoff note (Elementor JSON doesn't store WP SEO meta); insert the required
   internal links with descriptive anchor text; place images (two-column or
   background) with alt text, and labeled placeholders for live widgets.
7. **Audit** — apply `vitalair-page-audit`: run the brand-consistency and
   Elementor-hygiene checks, confirm the "do NOT fix" on-brand items are intact,
   fix anything off, and validate the JSON parses.

## Fastest path (reuse over rebuild)

Prefer **cloning the closest existing page** and swapping content over authoring
from scratch:

1. Copy the closest `content/page/<id>.json` as the starting structure.
2. Replace text (headings, eyebrows, body, FAQ items, CTA labels) with the brief's copy.
3. Re-point location references (city/county) and any service specifics.
4. Regenerate all element `id`s so it imports as a new page (no collisions).
5. Keep the section backgrounds/rhythm and button styles as-is (already on-brand).
6. Run the audit.

This is usually the 10-minute route. Author from scratch only when no existing
page is close.

## Deliverable & handoff

- Save the JSON into the kit's `content/page/` folder with a new numeric id, and
  register it in `manifest.json` under `content.page` if delivering a full kit
  re-import. For a single-page import, the standalone page JSON is enough.
- Present the file to the user and tell them the import path (Elementor →
  Templates → Import Template, or Tools → Import Kit for the whole export).
- Offer a quick before/after note of which existing page it was based on.

## Guardrails

- Match the kit; don't redesign it. If tempted to "improve" the aesthetic, stop —
  see the "do NOT fix" list in `vitalair-page-audit`.
- Don't use `minimalist-ui-OFF-BRAND` for VitalAir pages.
- If the brief lacks a hero headline, location, or CTA, ask one question rather
  than guessing brand-critical facts.
