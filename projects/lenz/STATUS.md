# Lenz: project status

**As of 2026-10-13 (v6-1 port, branch `lenz-v6-1-home`).** Companion to
`pages/home/HANDOFF-notes.md`, `pages/_theme/HANDOFF-notes.md` and `brand.py`.

## Source of truth

- Design: the approved prototype v6-1, `erickacevedor/lenz` @ 12259d2, snapshot in
  `design-source/v6-1/`.
- Decisions: the ClickUp task 86bbfgdhr (comments and threads). Where a copy doc
  disagrees with ClickUp, ClickUp wins.

## Pipeline

```
design-source/v6-1 ── tools/port-css.py ──> plugin/lenz-core/assets/css/lenz-core.css
                         (+ src/adapter.css, src/overrides.css, pages/*/widget-classes.json)
brand.py ── pages/<page>/build.py ──> <page>.json ── scripts/validate-page.py
build-all.sh [--import]   one command for all of it (import = LOCAL installs only)
```

## Where it is

| | |
|---|---|
| Local (Mac) | `~/Local Sites/lenz-2026`, http://localhost:10003 (site id lagFmabAD). Home 23, header 25, footer 26 on v6-1. Backup of the v4 state in `~/Local Sites/lenz-2026/backups/2026-10-13-before-home-v6-1/` |
| lenz.mysites.io | still the v4 build from August |
| Media | v6-1 photos and brand logos are attachments 30 to 43 on the Mac Local (`media.json`) |

## Built

- Home (all 15 sections), header, footer.
- Service page template (`service_page.py`, block-based, copy read from each page's source.docx by
  `tools/docx_outline.py`, ClickUp overrides in `FIXES`) and 10 service pages on Local: AC Repair 46,
  AC Installation 48, AC Maintenance 49, AC Replacement 50, Air Purification 51, Heating Installation 52,
  Heating Maintenance 53, Heating Repair 54, Humidity Control 55, UV Light Purification 56.

## Not built yet

- Service pages with no doc yet (Heating Replacement, Duct Cleaning, Additional Services children), the three hubs
  (Cooling, Heating, IAQ: different structure, need their own template), and the
  company pages (About, Contact, Financing, Specials, Service Areas, ...).
- Pages with no doc: heating-replacement, duct-cleaning, additional-services and
  its five children, privacy-policy, terms.

## Open before launch

- Form recipient, SMTP, spam protection.
- Schema ownership (prototype JSON-LD not ported).
- GBP Place ID for reviews; second office and radius on the map.
- Production host and domain; move from Local to mysites, with media id remap.
