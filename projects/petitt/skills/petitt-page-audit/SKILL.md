---
name: petitt-page-audit
description: >
  Audit-first review for Petitt Heating & Cooling Elementor pages/templates. Use when
  asked to review, clean up, fix, or improve a Petitt page, or as the pre-delivery gate
  before shipping one. Checks against the Petitt brand kit, Elementor hygiene, SEO,
  links, media, and the responsive checklist — without breaking layout or fighting the
  brand. Pairs with petitt-ui-design and petitt-content-style.
---

# Petitt Page Audit

Reviews Petitt Elementor pages against the brand kit. Elementor-aware — it does not
apply generic "premium web redesign" defaults that conflict with this brand.

## How this works

1. **Scan** — read the page JSON. Note section order + backgrounds, widget types,
   inline vs. global styling, and any `display_condition_list`.
2. **Diagnose** — run the checks below; list each issue with its section/widget.
3. **Fix at the source** — change `build.py` and rebuild. Never hand-patch the JSON.
4. **Gate** — `python3 scripts/validate-page.py <page>.json` must exit 0.

## A. Brand

- [ ] Headings **Oswald**, uppercase transform, at the kit scale
      (h1 3.2/2.4em · h2 2.4/2.0em · h3 1.8/1.6em · h4 1.5/1.35em); body **Montserrat**
      16px, `#171925`.
- [ ] Headings written in **sentence case** in the JSON (the theme uppercases them).
- [ ] CTA buttons: `#D90000` bg, `#AF0000` hover, white text, 100px pill, 15/25 padding,
      `fas fa-chevron-circle-right` icon, `icon_align: row-reverse`,
      **no `hover_animation`**.
- [ ] Phone button = navy (`globals/colors?id=secondary`) + `fas fa-phone-alt`.
- [ ] Band rhythm alternates (navy / soft-gray `#FAFAFA` / white / photo); at least the
      hero carries a `Petitt_WebSectionDividers-*` overlay.
- [ ] Content over a photo band sits in a glass card (`#FFFFFFE6` / `#FFFFFFCF`).
- [ ] `#47A3DA` used only as an accent border — never as a section background.
- [ ] Card grid matches the kit card: `#FAFAFA` fill, radius 15, shadow, white icon box,
      **H3 navy centered**, red button.

## B. Content & SEO

- [ ] Exactly one **H1**, containing the service + city; heading levels don't skip.
- [ ] Target keyword in the H1 and the first paragraph.
- [ ] Meta title < 60 chars, meta description < 155 chars, slug lowercase-hyphenated —
      recorded in `HANDOFF-notes.md` (Elementor JSON can't carry WP SEO meta).
- [ ] Neighborhoods named; "Petitt Promise" numbers exact ($500 / 10-year / 12-hour /
      $12 a month / since 2010 / 50+ years).
- [ ] Voice per `petitt-content-style` — no hype, no unquantified "affordable".
- [ ] Brand written "Petitt Heating & Cooling" (never Pettit/Petit/PHC).

## C. Links & media

- [ ] No dead (`#`, empty), `localhost`, or invented URLs. Every internal link resolves
      to a real page in the kit manifest.
- [ ] CTA destinations correct: book → `/contact-us/request-an-appointment/`,
      schedule → `/expert-hvac-services-in-sumner-county-schedule-today/`,
      phone → `tel:+16156540814`.
- [ ] Descriptive anchor text ("Explore White House Cooling Services", not "click here").
- [ ] Every image has **alt text**; reused images keep their real attachment `id`.
- [ ] Live widgets (Google Maps iframe, review sliders) preserved as `html` widgets and
      flagged in the handoff.

## D. Elementor hygiene

- [ ] Single-page wrapper `{version,title,type:"page",content,page_settings}`.
- [ ] Unique element ids throughout (regenerated if cloned).
- [ ] No `display_condition_list` anywhere.
- [ ] Every section = full-width Section → **one** boxed 1140px container → content;
      no wrapper around a lone image/text; nested containers have zero padding.
- [ ] Complete, valid, **UTF-8** JSON — no truncation, no placeholder comments.

## E. Responsive

- [ ] Grids: `grid_columns_grid_tablet` (2) + `grid_columns_grid_mobile` (1).
- [ ] Flex rows: `flex_direction_mobile: column`.
- [ ] %-width columns: `width_tablet` + `width_mobile` = 100%.
- [ ] H1 and **every** H2 carry `typography_font_size_mobile`.
- [ ] Boxed containers carry `padding_mobile`; fixed-height images carry `height_mobile`.

## Do NOT "fix" these — they are intentional

- **UPPERCASE headings.** Brand, not a mistake.
- **No button hover animation.** Color change only; don't add `shrink`.
- **Inline `#D90000` buttons** even though the global button color is `#EC2024`.
- **The `primary` global being light blue** while navy carries the brand.
- **Pill (100px) buttons** — don't square them off.
- **Long neighborhood lists** in the hero — that's the local SEO play.
- **The rating badge + "5.0 (1000+ Reviews)"** in the hero.
- **Absolute `https://petittheatingandcooling.com/…` links** — the kit uses absolute
  URLs, and they are not localhost artifacts.
