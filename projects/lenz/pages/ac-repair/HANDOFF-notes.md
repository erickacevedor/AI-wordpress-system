# Lenz: AC Repair (service page template) handoff

**Status (2026-10-13):** built on the approved service template
(design-source/v6-1/ac-repair.html + css/lenz-service.css) and imported on the Mac
Local copy as page 46 `ac-repair`, http://localhost:10003/ac-repair/. Checked at
390, 768, 1024 and 1440: no sideways scroll, one H1, FAQ and form working, form
preselects "AC Repair".

## SEO

- **Meta title:** `AC Repair in Des Moines, IA | Lenz Heating & Cooling`
- **Meta description:** `Fast AC repair in Des Moines, IA. 24/7 service, veteran and woman-owned, upfront pricing before any work begins. Schedule AC repair today.`
  (The doc says "no trip or diagnostic fees", which contradicts the 09/10 ClickUp
  decision; same change as the home. Needs Erick's ok.)
- Slug: `/ac-repair/` · Canonical: https://www.lenzheatingandcooling.com/ac-repair/
- Schema in the prototype: Service, BreadcrumbList, FAQPage. Not ported yet (same
  schema-ownership decision as the home).

## Copy

Verbatim from source.docx except:
- meta description (above);
- the hero shows the doc's first paragraph; the second moves to the intro section,
  as in the approved template;
- template pieces with no doc copy: breadcrumb, eyebrows, hero badge ("24/7
  emergency AC repair / Local team, real people, day or night."), trustbar
  ("Upfront Pricing" as the fifth proof), help tile, "More Cooling Services";
- "take a second look" kept as written: it never says free (ClickUp 09/10 item 6).

## How a new service page is made

Copy `pages/ac-repair/build.py`, change the PAGE dict (copy, `cat` = cool | warm |
air | extra, icons, photos, related cards), add the page to `build-all.sh`. The
layout lives in `service_page.py`; nothing else changes.

## Open

- Hero photo is the furnace technician (stand-in until the 2026-10-15 shoot).
- Links to `/air-conditioning/`, `/ac-installation/`, `/ac-maintenance/`,
  `/ac-replacement/`, `/maintenance-plan/` resolve once those pages exist.
