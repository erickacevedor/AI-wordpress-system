# Lenz: project status

**As of 2026-10-13 (v6-1 port, branch `lenz-v6-1-home`).** Companion to
`pages/home/HANDOFF-notes.md`, `pages/_theme/HANDOFF-notes.md` and `brand.py`.

## Source of truth

- Design: the approved prototype v6-1, `erickacevedor/lenz` @ 12259d2, snapshot in
  `design-source/v6-1/`.
- Decisions: the ClickUp task 86bbfgdhr (comments and threads). Where a copy doc
  disagrees with ClickUp, ClickUp wins.

## Skills (read these before building anything)

`skills/lenz-design-read`, `lenz-ui-design`, `lenz-content-style`, `lenz-page-builder`,
`lenz-page-audit` (2026-10-18). Tested by having a fresh agent rebuild Heating
Maintenance from its doc using only the skills: same 11 bands and classes as the real page.

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
- Hubs on the same template (`is_hub`, `services` block): Air Conditioning 66, Heating 67, Indoor Air Quality 68.
- Company pages from their docs (people, roster, steps, video, locations, area, coupons, embed blocks):
  About 75, Community Outreach 76, Contact 77, Financing 78, Hello Iowa 79, Careers 80, Maintenance Plans 81,
  Meet the Team 82, Service Areas 83, Specials 84, Urbandale 85, Waukee 86. Blog: posts archive, not built.

## Scope

The signed scope is 26 pages (PandaDoc SOW; ClickUp list "New Website Creation"). Pages outside it
(Heating Replacement, Duct Cleaning, Additional Services and its five children) are listed in
`brand.OUT_OF_SCOPE`: not in menus, never linked; their cards on the home stay as static cards.
AC Replacement is built but not in the SOW: confirm.

## Not built yet

- Service pages with no doc yet (Heating Replacement, Duct Cleaning, Additional Services children); the blog archive (Theme Builder).
- Pages with no doc: heating-replacement, duct-cleaning, additional-services and
  its five children, privacy-policy, terms.

## Open before launch

- Forms: the current site sends every form (contact, plans, jobs) to LeadConnector form qqIhBpp3Uvkj3zopUtRg; the new
  site uses an Elementor Pro email form except Careers (LeadConnector embed). Decide one.

- Form recipient, SMTP, spam protection.
- Schema ownership (prototype JSON-LD not ported).
- GBP Place ID for reviews; second office and radius on the map.
- Production host and domain; move from Local to mysites, with media id remap.
