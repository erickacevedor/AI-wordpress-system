---
name: petitt-page-builder
description: >
  Orchestrates creation of a new Petitt Heating & Cooling Elementor page from a content
  brief or doc. Use whenever the user says "build/create a Petitt page", "make a page
  from this doc", "new service-area page", or hands over copy to turn into an Elementor
  page. Runs the full pipeline: design-read → map sections → write copy → style →
  complete JSON → validate → audit, reusing the Petitt kit's brand.
---

# Petitt Page Builder

The one entry point for turning a content doc into an import-ready Petitt Elementor
page. Sequences the other Petitt skills so a page comes out on-brand, complete, and
responsive in one pass.

**Input:** a content doc/brief (page kind, city, hero, sections, FAQ, CTA, SEO meta).
Missing pieces come from the closest existing page or **one** focused question.

**Output**, all inside `projects/petitt/pages/<page-slug>/`:
`source.<ext>` · `build.py` · `<page-slug>.json` · `PREVIEW.html` · `HANDOFF-notes.md`.

## Pipeline

### 1. Design read — `petitt-design-read`
State the one-line read: page kind, city, which kit page you're mirroring, band rhythm.

### 2. Map the doc to sections
Walk the source doc top to bottom and assign each block to a section + pattern. Honor
**any formatting note in the doc** (the client's italic "(Note: …)" lines are
instructions, not copy — e.g. "format as a trust bar", "use a Card Component Grid",
"service titles as H3s"). For a service-area hub the default order is:

1. Hero (navy + divider overlay, rating badge, H1, lead, 1–2 CTAs, city image)
2. Trust bar
3. Service card grid (H3 per card + bullets + per-card CTA)
4. Maintenance plan
5. Financing
6. Why neighbors trust us (+ team image)
7. Map / reviews (live widgets, carried over)
8. FAQ (nested accordion, 980px)
9. Closing CTA (photo band + glass card + phone/schedule buttons)
10. Chamber-of-commerce / local badge strip

**Refreshing a live page?** Keep the live section order and only change what the brief
changes; carry over sections the brief doesn't mention (maps, badges) instead of
dropping them.

### 3. Write the copy — `petitt-content-style`
Use the doc's copy as the source of truth. Tighten only where it repeats itself. Keep
headings sentence case, keep every number and guarantee exact.

### 4. Style it — `petitt-ui-design`
Palette, Oswald uppercase scale, red pill buttons (no hover animation), pattern
overlays, glass cards, the card-grid and FAQ patterns, emoji mixed with native icons.

### 5. Emit the JSON — prefer `build.py`
Author `pages/<slug>/build.py` on top of `scripts/elementor_builder.py`, reading
`projects/petitt/tokens.json`. The library bakes in the structure + responsive rules,
so a page built through it passes the gate. Wrapper:
`{"version":"0.4","title":…,"type":"page","content":[…],"page_settings":{"template":"default"}}`.
Follow repo-root `skills/full-output-enforcement` — no placeholders, no truncation,
unique ids, UTF-8.

### 6. Validate — required gate
```
python3 projects/petitt/pages/<slug>/build.py
python3 scripts/validate-page.py projects/petitt/pages/<slug>/<slug>.json   # must exit 0
```

### 7. Audit — `petitt-page-audit`
Brand + hygiene + responsive review. Fix findings in `build.py` and rebuild — never
hand-edit the emitted JSON.

### 8. Preview + handoff
Write `PREVIEW.html` (a static approximation for design review) and
`HANDOFF-notes.md`: import path (Elementor → Templates → Import Templates → Insert),
SEO title/description/slug, live widgets to re-wire, image swaps, link targets to
confirm.

## Link targets (confirmed against the kit manifest)

| Purpose | URL |
|---|---|
| Book online / request appointment | `/contact-us/request-an-appointment/` |
| Schedule service | `/expert-hvac-services-in-sumner-county-schedule-today/` |
| Phone | `tel:+16156540814` |
| Cooling (White House) | `/service-areas/white-house/cooling/` |
| Heating hub | `/heating/` · Gas logs `/heating/gas-log-services/` |
| Plumbing hub | `/plumbing/` · Water heaters `/plumbing/water-heater-services/` |
| Indoor air quality | `/indoor-air-quality/` · Crawl space `/indoor-air-quality/crawlspace-encapsulation/` |
| Maintenance plans | `/maintenance-plans/` |
| Financing | `/financing/` |
| Service areas | `/service-areas/` · About `/about-us/` |

Use absolute `https://petittheatingandcooling.com/…` URLs — that is what the kit does.

## Guardrails

- Emit **complete** JSON. No "…", no "repeat for the other cards".
- One H1. Unique ids. No `display_condition_list`. No `#`/empty/localhost links.
- Don't invent guarantees, prices, licenses, or URLs — every one of them is checkable.
- If the doc contradicts the live page on a fact (URL, title), flag it and keep the live
  value unless told otherwise.
