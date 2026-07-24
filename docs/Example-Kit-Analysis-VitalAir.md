# VitalAir Elementor Kit — Analysis & Build Reference

This is a full WordPress/Elementor site export for **VitalAir** (vitalair.com), an Atlanta-area HVAC company. Use this document as the design-system reference when building a new page so it matches the existing kit.

## What's in the export

- **Theme:** Hello Elementor 3.4.4 (Elementor 4.1.4 + Elementor Pro 4.0.4)
- **34 pages** (`content/page/`) — services, service areas, FAQs, landing pages
- **34 blog posts** (`content/post/`)
- **25 templates** (`templates/`) — 1 header, 1 footer, reusable containers/sections, plus two "Native" atomic-widget page templates
- **Global config:** `site-settings.json` (colors, fonts, experiments), `manifest.json` (index of everything)

Note: `site-settings.json` still holds the *default* Hello Elementor global colors/fonts (the generic `#6EC1E4` palette + "Noto Sans Coptic"). The real brand styling is applied **inline on the widgets**, not through global variables — so the palette below is what's actually used on-screen, extracted from the page content.

## Brand color palette (actual usage)

| Role | Hex | Where it's used |
|------|-----|-----------------|
| Brand navy (dark) | `#16163F` | Header bar, hero backgrounds, dark sections |
| Deep navy variants | `#1C244B`, `#0D1B3E`, `#020101` | Section backgrounds, overlays |
| Brand blue | `#3E67AB` | Footer, accents, gradients |
| Blue variants | `#1B4E8D`, `#324A6D` | Secondary accents |
| Primary green (CTA) | `#74BC2B` | Buttons, highlights |
| Green variants | `#8BE035`, `#8FD13E`, `#6ABF4B`, `#5A9421` | Eyebrow labels, button hover, accents |
| Light blue tint | `#EEF2FA`, `#C8D6E8` | Alternating section backgrounds |
| Neutral dark text | `#212121`, `#222222` | Body/heading text |
| White | `#FFFFFF` | Text on dark, light section bg |
| Muted purple-gray | `#555573` | Secondary text |
| Alert red | `#D72C2C` | Warnings/emphasis |

**Section rhythm:** pages alternate background between white (`#FFFFFF`), light blue tint (`#EEF2FA`), and dark navy (`#16163F`) hero/feature bands.

## Typography

Primary font family in practice: **Poppins** (headings/UI), with **Montserrat, Manrope, Sora, Inter, Archivo** appearing in places. (The global default "Noto Sans Coptic" is not the real brand face.)

Type scale (font sizes actually used, px):

- **Eyebrow / label:** 11–12px, weight 700, uppercase, letter-spacing ~2.6px, green (`#8FD13E`)
- **Body / small:** 15–18px, weight 400
- **Sub-heading (h3):** 22–26px
- **Section heading (h2):** 40–44px
- **Hero heading (h1):** 52–70px (up to 95px on large displays)

Heading tags in use: `h1` (hero), `h3` (sub-sections), plus many `div`/`p` styled headings for eyebrows and labels.

## Buttons (primary CTA pattern)

```
text color:        #FFFFFF
background:         #74BC2B  (brand green)
hover text:        #FFFFFF
hover background:   #5A9421  (darker green)
border-radius:     999px (fully rounded pill)
padding:           16px top/bottom, 30px left/right
font:              15px, weight 700
```

Common CTA copy: "Schedule a Service Inspection", "Schedule a Service".

## Layout system

- **Two generations of layout coexist:**
  - **Newer pages (majority)** use Elementor **Containers** (flexbox model) — e.g. Cooling Services, service-area pages, FAQs, landing pages.
  - **Older pages** use the legacy **Section → Column** model — e.g. `2327` AC Repair, `2315` Cooling Services, `2338` AC Replacement.
  - Two **"Native" atomic-widget** templates exist (`2330`, `2317`) using Elementor's newest V4 atomic elements.
- **Content max-widths (boxed):** commonly ~1200–1240px for text content, up to 1600–1790px for full-bleed hero/footer bands.
- **Widget mix** (most-used across pages): heading (188), text-editor (109), button (62), icon-box (51), image (30), call-to-action (13), plus toggles/accordions for FAQs.

## Reusable building blocks (templates/)

| ID | Name | Type |
|----|------|------|
| 10 | Elementor Header #10 | header (sticky, navy `#16163F`) |
| 181 | Elementor Footer #181 | footer (blue `#3E67AB`, curve shape divider) |
| 186 | Footer | container |
| 2205 | Form Template | section |
| 1979 | bannetemp | container (banner) |
| 1882 | Template-ContactUs | container |
| 1879 | Template-Service | container |
| 1422 / 438 | Services / ServicePages | container |
| 772 / 769 | Service-faq / Service-FAQ | container |
| 766 | Service-IMG | container |
| 624 | VAFAQ | container (FAQ block) |
| 2330 / 2317 | VitalAir AC Repair / Cooling (Native) | atomic page templates |

These are the fastest starting points — a new page can reuse the header (10), footer (181), a service container (1879/438) and FAQ block (624/772).

## Typical page anatomy (from AC Repair, `2327`)

1. **Hero** — navy `#16163F`, eyebrow label (green, uppercase) + h1 + intro text
2. **"Proudly serving" band** — light `#EEF2FA`, heading + text
3. **Service intro** — white, eyebrow + h2 + supporting paragraphs
4. **"Not sure what's wrong?"** — light band + embedded form (shortcode)
5. **"What to expect"** — nested containers of steps
6. **Common problems** — white, heading + icon-box grid
7. **FAQ** — toggle/accordion block
8. **Footer CTA** — green button

## Recommendations for building a new page on this kit

1. **Start from a Container-based template** (the newer model) rather than the legacy Section pages, unless matching a specific old page. Good bases: `1879 Template-Service` or `438 ServicePages`.
2. **Reuse header `10` and footer `181`** so global chrome stays consistent.
3. **Apply colors inline** (this kit doesn't drive styling through global variables): navy `#16163F` heroes, alternating `#FFFFFF`/`#EEF2FA` sections, green `#74BC2B` pill CTAs.
4. **Follow the type scale**: green uppercase eyebrow (11–12px/700/2.6px spacing) → h1/h2 (40–70px) → 15–18px body, Poppins.
5. **Keep the section rhythm**: dark hero → light/white alternating content bands → FAQ accordion → CTA.
