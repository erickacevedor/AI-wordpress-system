# Newman Air: splash page, import and handoff notes

Temporary page for newmanair.com while the core pages are built (ClickUp 86bcjyqgx,
launch target 2026-10-29). One full-screen section on the Elementor Canvas template:
no header, no footer, no menu, no links, per the brief.

## Files
- `splash.json`: the page (single-page import wrapper) **import this**
- `build.py`: reproducible build (`python projects/newman-air/pages/splash/build.py`)
- `source.md`: the brief as received
- `newman-air-logo-horiz.png`: Jessica's final horizontal logo (1200x506, Drive "Web Use")
- `PREVIEW.html`: generated from the JSON, design review only. The logo shows only once the PNG is at the URL below.

## SEO
- **Meta title:** Newman Air | Heating & Air Conditioning, Tri-Cities TN
- **Meta description:** Best in Show Heating & Cooling is now Newman Air. Our new website is on the way. Call (423) 753-7788 for heating and AC service in the Tri-Cities, TN.
- **Slug:** set as the static front page (Settings > Reading), so it answers at `/`
- **Canonical:** https://newmanair.com/

## Layout
Full-width section (gradient `#003E51` to `#002A38`, 160 deg, 6px `#FF8900` top border,
min-height 100vh, content centred) > one boxed container at 960px (padding 56/20,
mobile 44/16) > logo (460px, tablet 380px, mobile 100%), eyebrow, H1, lead, a 2-column
grid of cream contact cards (1 column on mobile), small print.

## Decisions
- **Kit-native, no custom CSS, no html widgets** ("keep it light"): replacing it at launch is deleting one page.
- **Hex, not Global Colors**: the new install has no Newman Air kit, and a global ref on a default kit paints the page in Elementor's stock colours. `tokens.json` maps the palette to the four system globals for the core pages.
- **Phone and email are plain text** because the brief says no links. iOS and Android usually auto-detect the number as tappable anyway. If DJ wants click-to-call, it is a one-line change (heading link to `tel:+14237537788`).
- **Colours from the final logo SVGs**, not the V2 prototype: Tennessee orange `#FF8900`, navy `#003E51`, cream `#F7F2E4`, deep teal `#0F5B6D`.

## Local site (2026-10-20)
Imported and rendering on Erick's Local install (<http://localhost:10028>, page 15, front page, logo media 13, Site Icon 14). Checked at 1440, 768 and 390px. Recipe in `../../ENVIRONMENT.md`. If that Local site is what gets pushed to Flywheel, the import steps below are already done there.

## Before import (any other install)
1. Upload `newman-air-logo-horiz.png` to `https://explorehvac.com/web/newmanair/assets/newman-air-logo-horiz.png`. Elementor copies it into the Media Library on import. If the URL is not reachable, upload the PNG to Media after import and pick it in the Image widget.

## After import, wire up
- Elementor > Templates > Saved Templates > Import Templates > `splash.json`, then create a page "Newman Air", insert the template, publish.
- Page template must stay **Elementor Canvas** (shipped in `page_settings`).
- Settings > Reading: static front page = this page.
- Site Identity: title "Newman Air", tagline, and the bear mark (`NewmanAirLogo_Bear@72x.png`, 600x601) as the Site Icon.
- Fonts: Oxanium (headings, cards) and Roboto (text) are set per widget and load from Google Fonts through Elementor.
- Dependencies: none beyond Elementor core (no Pro widget, addon or shortcode).

## Open
- Copy drafted for DJ's review; no copy was supplied.
- Email shown: dispatch@newmanair.com (from Alexis's homepage copy). Confirm it is the right public inbox.
- Indexing during the splash period (Settings > Reading "Discourage search engines") is a call for DJ/Esteban.
