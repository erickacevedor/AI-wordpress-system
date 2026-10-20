# Newman Air: design system analysis

**Origin:** HTML prototype. `design-source/v2/` is the V2 homepage the team picked on
2026-10-06 (source in the exploremedia repo, `clients/newman-air/design/homepage-v2.html`,
plus the exported `v2.css`). No Elementor kit exists for the new site yet.

**Status (2026-10-20): partial onboarding.** `tokens.json` is written and hand-tuned.
The five `newman-air-*` skills are **not generated yet**: V2 still has 12 pending
review edits and was built before the final logo, so skills written now would encode a
design that is about to change. Generate them at the start of the core-page build
(Build Phase 1, ClickUp 86bcajgzh), after the V2 edits land. The only page built
before then is the splash, which is a single section.

## Palette: from the final logo, not from V2
Jessica's final files (Drive "Web Use", 2026-10-14/15) use exactly these fills:

| Role | Hex | In the logo | Elementor global |
|---|---|---|---|
| teal | `#46BFAF` | fur highlight | Primary |
| deep_teal | `#0F5B6D` | fur shadow | Secondary |
| navy | `#003E51` | outlines, wordmark stroke | Text |
| orange | `#FF8900` | outer stroke (Tennessee orange, client request 2026-10-07) | Accent |
| gold | `#FFA300` | eyes, inner orange | custom |
| cream | `#F7F2E4` | face, wordmark | custom |
| sand | `#DDD4BF` | wordmark gradient end | custom |

V2 used the old kit (`#47BFAF`, `#006F79`, `#003E51`, `#FFA300`): teal and navy carry
over; `#006F79` becomes `#0F5B6D`; the CTA orange moves from `#FFA300` to `#FF8900`.

Contrast: `#FF8900` on `#003E51` is 4.9:1 (AA); on `#0F5B6D` it is 3.2:1 (fails), so
orange text never sits on deep teal. Navy text on `#FF8900` buttons is 4.9:1.

## Fonts
Oxanium (headings, buttons, eyebrows) and Roboto (body), as in the exported V2 and the
current callbestinshow.com kit. The source HTML also loads Bricolage Grotesque and DM
Sans for the Tokens panel; those are not the brand.

## Type scale
V2 has 24 distinct sizes (fluid `clamp()` on h1/h2). Collapsed for the splash:
h1 56/46/34px, eyebrow 15px uppercase +0.14em, lead 19/17px, body 17px, small 14px.
The full mapping is a core-page onboarding task.

## Port strategy
Kit-native (Anatomy section 6A) for the splash. V2's identity effects (topo texture, grain,
parallax ridges, rotating badge) have no Elementor control; whether the core pages
carry them through a small companion stylesheet is undecided (Erick said on 2026-10-08
he would port V2 with custom CSS/JS in separate files). Record that decision here when
it is made.
