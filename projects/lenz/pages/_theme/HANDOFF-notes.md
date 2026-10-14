# Lenz: Theme Builder parts (v6-1) handoff

**Status (2026-10-13):** header (template 25 `lenz-header`) and footer (template 26
`lenz-footer`) rebuilt from the v6-1 prototype and imported on the Mac Local copy,
condition `include/general` (entire site). Matches the prototype at 1440, 1024, 768
and 390 (element diff), including the mega menu, sticky nav and mobile menu.

## What changed from the v4 build

- The v4 header used Elementor's Mega Menu widget, which rendered about 170px wider
  than the source and pushed the phone number out of the bar. v6-1 ships the
  prototype's own nav markup in html widgets, generated from `brand.SERVICES` and
  `brand.NAV`, with the prototype's behaviour in `lenz-core/assets/js/lenz-site.js`.
  The phone number is back in the bar, as in the prototype.
- Offer bar: the financing message (ClickUp 09/10 and 10/08), not the seasonal one.
- Footer: Sierra's email (ClickUp 09/10 item 14).

## Structure (why three header sections)

1. `.offer-bar` scrolls away. It also carries `#nav-sentinel` (absolutely placed)
   for the stuck-state observer.
2. `header.nav` is `position: sticky`. The Theme Builder wrapper is
   `display: contents` (overrides.css) so the sticky element sticks to the page.
3. The mobile menu is `position: fixed` and lives in its own band, because the
   nav's `backdrop-filter` would trap a fixed child.

## Editing

- Menu items: edit `brand.py` (SERVICES, NAV, L) and rebuild; the mega menu, mobile
  menu, footer columns and the home services block all read it. Not the WP menu UI.
- Links point at the planned slugs (see `../home/HANDOFF-notes.md`).
