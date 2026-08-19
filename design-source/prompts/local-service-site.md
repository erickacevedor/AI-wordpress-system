<!--
  STORED IN THIS REPO AS A STAGE INPUT — read design-source/README.md first.

  What this is: a fill-in-the-blanks master prompt that produces a complete static
  HTML/CSS site for a local service business, from a design system down to page
  templates.

  What it is NOT, in this repo: a deliverable. Its output is a SOURCE DESIGN that
  onboarding reads to produce projects/<site>/tokens.json — the seam where this
  stage hands off to the Elementor pipeline. Whoever runs it should know they are
  producing an input, not a shippable site.

  THREE REPO ADAPTATIONS are marked inline below with >>> REPO: <<< so the original
  intent stays visible:
    1. Phase 1.4  — content width is a fillable variable, not a fixed 1800px, so a
                    prototype can be told to match a target from the start.
    2. Phase 1.7  — icons ship as an inline SVG sprite in the site plugin instead of
                    Lucide via CDN. Same icons, no external dependency, survives the
                    Elementor rebuild. projects/lenz/plugin/lenz-core/assets/icons/
                    lenz-sprite.svg is the worked example (24 symbols).
    3. Phase 7    — also emit projects/<site>/tokens.json in this repo's schema.
                    scripts/analyze-prototype.py can derive it from tokens.css, but
                    having the generator write it directly is cheaper and lossless.

  Everything else is unchanged from the original.
-->

You are a senior full-stack web developer and UI/UX designer specializing in conversion-optimized local service websites. You will build a complete, production-ready HVAC company website following every specification in this prompt with zero deviation. Do not add features, pages, or design decisions not explicitly requested. After each major deliverable, output: ✅ [what was completed] and pause for confirmation before proceeding to the next phase.

---

## PHASE 0 — PROJECT CONTEXT

**Company:** [[ COMPANY_NAME ]]
**Tagline / value proposition:** [[ TAGLINE ]]
**Primary service:** HVAC (Heating, Ventilation & Air Conditioning)
**Location / primary city:** [[ PRIMARY_CITY, STATE ]]
**Phone number:** [[ PHONE_NUMBER ]]
**Email:** [[ EMAIL ]]
**Address:** [[ FULL_ADDRESS ]]
**Business hours:** [[ BUSINESS_HOURS ]]
**Emergency hours:** [[ EMERGENCY_HOURS — e.g. 24/7 or Mon–Sun 7am–11pm ]]
**Years in business:** [[ YEARS_IN_BUSINESS ]]
**License number:** [[ LICENSE_NUMBER ]]
**BBB rating:** [[ BBB_RATING — e.g. A+ ]]
**Google rating:** [[ GOOGLE_RATING — e.g. 4.9 ]]
**Number of Google reviews:** [[ REVIEW_COUNT ]]

**Services offered (list all — each becomes a service page):**
- [[ SERVICE_1 — e.g. AC Repair ]]
- [[ SERVICE_2 — e.g. AC Installation ]]
- [[ SERVICE_3 — e.g. Heating Repair ]]
- [[ SERVICE_4 — e.g. Heating Installation ]]
- [[ SERVICE_5 — e.g. HVAC Maintenance / Tune-Up ]]
- [[ OPTIONAL: SERVICE_6 ]]
- [[ OPTIONAL: SERVICE_7 ]]

**City landing pages (each service × each city = one page):**
- [[ CITY_1 ]]
- [[ CITY_2 ]]
- [[ CITY_3 ]]
- [[ OPTIONAL: CITY_4 ]]
- [[ OPTIONAL: CITY_5 ]]

**Equipment brands supported (for trust signals and SEO):**
- [[ BRAND_1 — e.g. Carrier ]]
- [[ BRAND_2 — e.g. Trane ]]
- [[ BRAND_3 — e.g. Lennox ]]
- [[ BRAND_4 — e.g. Daikin ]]
- [[ BRAND_5 — e.g. Goodman ]]
- [[ BRAND_6 — e.g. Rheem ]]
- [[ OPTIONAL: BRAND_7 ]]

**Certifications held:**
- [[ CERT_1 — e.g. NATE Certified ]]
- [[ CERT_2 — e.g. EPA 608 ]]
- [[ OPTIONAL: CERT_3 ]]

**Chamber of Commerce / affiliations:**
- [[ AFFILIATION_1 ]]
- [[ OPTIONAL: AFFILIATION_2 ]]

---

## PHASE 1 — DESIGN SYSTEM

### 1.1 BRAND COLORS

Input the client's brand colors as HEX values. You MUST automatically generate a full color system from these inputs.

PRIMARY_COLOR:    [[ #XXXXXX ]] SECONDARY_COLOR:  [[ #XXXXXX ]] ACCENT_COLOR:     [[ OPTIONAL: #XXXXXX — leave empty if not used ]]

From each input color, automatically generate the following tints and shades using HSL manipulation. Name and output every token:

For PRIMARY_COLOR generate:
- primary-50:   5% saturation, 97% lightness
- primary-100:  full saturation, 93% lightness
- primary-200:  full saturation, 85% lightness
- primary-300:  full saturation, 72% lightness
- primary-400:  full saturation, 58% lightness
- primary-500:  [[ PRIMARY_COLOR ]] — base
- primary-600:  full saturation, 42% lightness
- primary-700:  full saturation, 32% lightness
- primary-800:  full saturation, 22% lightness
- primary-900:  full saturation, 13% lightness

Apply the same 10-stop scale to SECONDARY_COLOR and ACCENT_COLOR.

Also generate:
- neutral-0:   #FFFFFF
- neutral-50:  #F8F8F8
- neutral-100: #F0F0F0
- neutral-200: #E0E0E0
- neutral-300: #BDBDBD
- neutral-400: #9E9E9E
- neutral-500: #757575
- neutral-600: #616161
- neutral-700: #424242
- neutral-800: #212121
- neutral-900: #121212

**WCAG COMPLIANCE — MANDATORY**
For every color token that will be used as a background, calculate and output its contrast ratio against both #FFFFFF and #121212. Flag PASS (≥4.5:1 for normal text, ≥3:1 for large text ≥18px bold) or FAIL. NEVER use a failing combination in any component. If a generated shade fails, shift lightness until it passes. Document the final passing value.

Semantic color assignments (map tokens to roles):
--color-bg-primary:        neutral-0 --color-bg-secondary:      neutral-50 --color-bg-tertiary:       neutral-100 --color-surface:           neutral-0 --color-surface-raised:    neutral-0 with 1px neutral-200 border --color-border:            neutral-200 --color-border-strong:     neutral-300

--color-text-primary:      neutral-900 --color-text-secondary:    neutral-600 --color-text-disabled:     neutral-400 --color-text-on-primary:   [[ auto-assign: #FFFFFF or neutral-900 — whichever passes WCAG AA ]] --color-text-on-secondary: [[ auto-assign: #FFFFFF or neutral-900 — whichever passes WCAG AA ]]

--color-cta-primary:          primary-500 --color-cta-primary-hover:    primary-600 --color-cta-primary-active:   primary-700 --color-cta-secondary:        transparent, 1.5px primary-500 border --color-cta-secondary-hover:  primary-50

--color-emergency:         [[ auto-generate: a dark high-contrast bg for the seasonal offer bar — use primary-900 or secondary-900, whichever has higher contrast against light text. Output the exact hex. ]] --color-emergency-text:    [[ #FFFFFF or lightest passing tint of primary — WCAG AA required ]] --color-emergency-cta-bg:  [[ primary-400 or accent-500 — must pass 3:1 contrast against --color-emergency ]]

Seasonal offer bar color sets — generate 4 complete sets: SUMMER:  bg [[ dark warm tone derived from brand — e.g. primary-900 or deep amber ]], text [[ lightest passing contrast ]], cta-bg [[ accent or warm mid-tone ]] WINTER:  bg [[ deep cool tone — secondary-900 or deep blue ]], text [[ lightest passing ]], cta-bg [[ secondary-400 ]] SPRING:  bg [[ deep green or secondary-800 ]], text [[ lightest passing ]], cta-bg [[ green mid-tone ]] FALL:    bg [[ deep earthy tone — burnt orange family ]], text [[ lightest passing ]], cta-bg [[ warm mid-tone ]]

### 1.2 TYPOGRAPHY

Font source: Google Fonts only (zero licensing cost, Elementor-compatible).

FONT_PRIMARY (headings): [[ FONT_NAME — e.g. Plus Jakarta Sans ]] FONT_SECONDARY (body):   [[ FONT_NAME — e.g. Inter ]]

If both fields are left empty, use this HVAC-appropriate pairing: Headings: "Plus Jakarta Sans" — weights 500, 600 Body:     "Inter" — weights 400, 500

**TYPE SCALE — Major Third (ratio 1.250), base 16px paragraph**

The entire scale is mathematically derived from the paragraph base of 16px using the Major Third modular scale (×1.250 per step up, ÷1.250 per step down). Output every token as a CSS custom property. Round to the nearest whole pixel. Do NOT deviate from these values.

Scale derivation: each step = previous × 1.250 Base (paragraph): 16px

--text-2xs:  10px  / line-height 1.5  / letter-spacing 0.08em   ← 16 ÷ 1.250² --text-xs:   13px  / line-height 1.5  / letter-spacing 0.04em   ← 16 ÷ 1.250 --text-sm:   16px  / line-height 1.7  / letter-spacing 0.01em   ← BASE — paragraph / body --text-md:   20px  / line-height 1.6  / letter-spacing 0        ← 16 × 1.250 --text-lg:   25px  / line-height 1.5  / letter-spacing -0.01em  ← 16 × 1.250² --text-xl:   31px  / line-height 1.4  / letter-spacing -0.02em  ← 16 × 1.250³ --text-2xl:  39px  / line-height 1.2  / letter-spacing -0.02em  ← 16 × 1.250⁴ --text-3xl:  49px  / line-height 1.15 / letter-spacing -0.03em  ← 16 × 1.250⁵ --text-4xl:  61px  / line-height 1.05 / letter-spacing -0.04em  ← 16 × 1.250⁶

Responsive overrides — apply at breakpoint ≤599px (mobile):
--text-3xl becomes: --text-2xl (39px) on mobile --text-2xl becomes: --text-xl  (31px) on mobile --text-xl  becomes: --text-lg  (25px) on mobile All other tokens: unchanged on mobile

Font weights:
--font-regular:  400 --font-medium:   500 --font-semibold: 600

Semantic role assignments:
Display / hero H1:    --text-4xl  desktop / --text-3xl  mobile — font-semibold — FONT_PRIMARY H1 (standard pages):  --text-3xl  desktop / --text-2xl  mobile — font-semibold — FONT_PRIMARY H2:                   --text-2xl  desktop / --text-xl   mobile — font-semibold — FONT_PRIMARY H3:                   --text-xl   desktop / --text-lg   mobile — font-medium   — FONT_PRIMARY H4:                   --text-lg             --text-lg           — font-medium   — FONT_PRIMARY Body large:           --text-md                                 — font-regular  — FONT_SECONDARY Body / paragraph:     --text-sm  ← 16px BASE                   — font-regular  — FONT_SECONDARY Label / caption:      --text-xs                                 — font-medium   — FONT_SECONDARY Micro / tag / badge:  --text-2xs                                — font-medium, uppercase, letter-spacing 0.08em

WCAG minimum font-size rule: NEVER use --text-2xs for body content. --text-2xs is permitted only for
badges, tags, legal disclaimers, and form helper text — always with sufficient contrast ratio (≥4.5:1).

### 1.3 SPACING — 8px BASE GRID

All spacing tokens MUST be multiples of 8px. No exceptions.

--space-1:  4px   (half-unit — use only for micro gaps inside components) --space-2:  8px --space-3:  12px  (1.5× — permitted exception for tight UI) --space-4:  16px --space-6:  24px --space-8:  32px --space-10: 40px --space-12: 48px --space-16: 64px --space-20: 80px --space-24: 96px --space-32: 128px --space-40: 160px --space-48: 192px

Fillable component spacing (define per project, must be multiples of 8):
--section-padding-top:        [[ e.g. 96px ]] --section-padding-bottom:     [[ e.g. 96px ]] --section-padding-top-mobile: [[ e.g. 64px ]] --section-padding-bottom-mobile: [[ e.g. 64px ]] --card-padding:               [[ e.g. 32px ]] --card-padding-mobile:        [[ e.g. 24px ]] --card-gap:                   [[ e.g. 24px ]] --navbar-height:              44px (fixed — do not modify) --offer-bar-height:           28px (fixed — do not modify)

### 1.4 LAYOUT GRID — 12 COLUMNS

Desktop (≥1920px default, down to 1440px):
- 12 columns
- Column gutter: 24px
- Outer margin: 60px each side (fixed)
- Max content width: [[ MAX_CONTENT_WIDTH — default 1800px ]]

>>> REPO: make this a real decision, not a default. Elementor/Hello themes box
content at ~1140px and every kit in projects/ sits between 1140 and 1280. If this
prototype will be rebuilt in Elementor, set MAX_CONTENT_WIDTH to the target width
now — retrofitting it later means re-deciding every section's proportions. Emit it
as --container-max so scripts/analyze-prototype.py picks it up. <<<

Large desktop (>1920px):
- Center content at max-width: 1800px
- Outer space: auto

Breakpoints — Material Design + 1920px default:
--bp-xs:  0px     (mobile portrait) --bp-sm:  600px   (mobile landscape / small tablet) --bp-md:  904px   (tablet) --bp-lg:  1240px  (desktop) --bp-xl:  1440px  (large desktop) --bp-2xl: 1920px  (full HD — default design canvas)

Responsive column counts:
- 0–599px:    4 columns, 16px gutter, 16px outer margin
- 600–903px:  8 columns, 16px gutter, 32px outer margin
- 904–1239px: 12 columns, 24px gutter, 48px outer margin
- 1240–1439px: 12 columns, 24px gutter, 60px outer margin
- 1440–1919px: 12 columns, 24px gutter, 60px outer margin
- 1920px+:    12 columns, 24px gutter, auto (content max 1800px centered)

**Rhythm breaks — REQUIRED:**
At least 2 sections per page MUST have one element that intentionally breaks the 60px outer margin. Rules for breaks:
- Full-bleed background sections (dark bg, colored bg): extend 100vw. Content inside remains within the grid.
- Oversized elements (large headline, hero image, CTA banner): can bleed 40px beyond the 60px margin (to 20px from edge) on one side only.
- Never break both sides simultaneously.
- Never break the grid on mobile (≤599px).

### 1.5 BORDER RADIUS

--radius-sm:   4px   (tags, badges, pills) --radius-md:   8px   (inputs, small cards) --radius-lg:   12px  (cards, modals) --radius-xl:   16px  (large cards, feature sections) --radius-full: 9999px (buttons, round elements)

Fillable per project:
--radius-button:  [[ e.g. 8px or 9999px ]] --radius-card:    [[ e.g. 12px ]] --radius-input:   [[ e.g. 8px ]]

### 1.6 ELEVATION / BORDERS

Design approach: FLAT. No drop shadows on primary UI elements.

--border-default:  1px solid var(--color-border) --border-strong:   1px solid var(--color-border-strong) --border-focus:    2px solid var(--color-cta-primary)      (accessibility focus ring) --border-accent:   1.5px solid var(--color-cta-primary)    (featured card highlight only)

NEVER use box-shadow for decoration. The only permitted shadows:
- Focus rings: `0 0 0 3px rgba(primary-500, 0.25)` — accessibility only
- Sticky nav on scroll: `0 1px 0 var(--color-border)` — 1px bottom border, not shadow

### 1.7 ICON SYSTEM

Library: Lucide Icons (https://lucide.dev).

>>> REPO: do NOT load these from a CDN. Build the icons you actually use into a
single inline SVG sprite shipped with the site (an Elementor page that depends on an
external icon font or CDN blanks out when it is unavailable, and this repo's standard
is that a page never depends entirely on an icon font). See
projects/lenz/plugin/lenz-core/assets/icons/lenz-sprite.svg — 24 symbols, referenced
as <svg><use href="#i-name"></use></svg>. Keep the Lucide glyphs; change only the
delivery. <<<
Size tokens:
--icon-sm:  16px --icon-md:  20px --icon-lg:  24px --icon-xl:  32px

- All icons used as UI elements (nav, buttons, feature cards): --icon-md (20px)
- All icons used as decorative/section headers: --icon-xl (32px)
- Icon color always inherits from text color of its context
- NEVER use icons as the sole conveyor of meaning — always pair with visible text label (WCAG 1.4.1)

### 1.8 MOTION

Flat design: minimal, purposeful motion only.
--transition-fast:   150ms ease --transition-base:   200ms ease --transition-slow:   300ms ease-in-out

Permitted transitions: opacity, color, background-color, border-color, transform (scale max 1.02 on hover).
Prohibited: entrance animations, scroll-triggered animations, parallax, auto-playing elements.
Respect prefers-reduced-motion: all transitions MUST be disabled when OS setting is on.

---

## PHASE 2 — COMPONENT LIBRARY

Build these components as reusable, self-contained blocks. Each must work independently and nest inside any page template.

### 2.1 OFFER BAR (seasonal-emergency)

Height: exactly 28px. Fixed. Never grows.
Behavior: static (not sticky). Disappears on scroll. Does NOT stack on top of the sticky navbar.
Mobile: show only primary text + phone number. CTA pill hidden on ≤599px if text exceeds 45 characters.
Seasonal JS switcher: on page load, detect current month and apply correct seasonal set:
  - June–August (month 6–8): SUMMER set
  - December–February (month 12, 1–2): WINTER set
  - March–May (month 3–5): SPRING set
  - September–November (month 9–11): FALL set

Seasonal copy — FILL IN before deploying. Max 55 characters per copy string including CTA label:
SUMMER_COPY: [[ e.g. "Too hot to handle? We're on it — 24/7." ]] SUMMER_CTA:  [[ e.g. "Call now" ]] WINTER_COPY: [[ e.g. "Heat's out? We're 30 min away. Emergency service." ]] WINTER_CTA:  [[ e.g. "Call now" ]] SPRING_COPY: [[ e.g. "AC tune-up — get ready before summer hits." ]] SPRING_CTA:  [[ e.g. "Book now" ]] FALL_COPY:   [[ e.g. "Winter's coming — get your heater checked today." ]] FALL_CTA:    [[ e.g. "Book now" ]]

Structure:
[seasonal bg] [pulsing dot 6px •] [COPY text --text-sm font-medium] [separator 1px] [CTA pill --text-xs]

### 2.2 NAVBAR (sticky)

Height: exactly 44px. Fixed position, top: 28px on page load, top: 0 after offer bar scrolls away (JS transition).
Background: --color-bg-primary. Bottom border: --border-default on scroll.
Structure left→right:
[Logo] ........ [Nav links: Services | Areas | About | Blog] ........ [Phone --text-sm font-medium color-cta-primary] [Book Online — primary button]

Mobile (≤599px): [Logo] ........ [Phone icon — clickable] [Hamburger menu]
Tablet (600–903px): [Logo] ........ [Phone] [Book Online] [Hamburger]

Services dropdown: lists all service pages. On hover/focus, opens below with --border-default border, --radius-lg, --color-bg-primary bg.
Active page: current page link gets --color-cta-primary color + 2px bottom border.
Accessibility: full keyboard navigation, aria-expanded on dropdowns, skip-to-content link as first focusable element.

### 2.3 HERO — HOME

Viewport height: 78vh minimum, max 85vh. The bottom of the hero MUST be visible — show 40–60px of the next section to signal scrollability.
Layout: 2-column grid on desktop. Col 1 (7/12): text content. Col 2 (5/12): image.
Image: real photo of HVAC technician at work or in front of a home. Aspect ratio 4:5. No stock illustration.

Content structure (col 1):
H1: [[ SEASONAL_H1 — e.g. "AC Repair in [City] — Same Day, Guaranteed" ]] Subheading (--text-md): [[ e.g. "Your AC stopped working. We'll have a certified tech at your door today." ]] CTA row: [Primary button: "Book online — same day"] [Secondary button: "Call [PHONE]"] Trust inline row (--text-sm, neutral-500): [green dot] Licensed & insured [·] 4.9 ★ Google [·] NATE certified [·] No fix, no fee

Mobile: single column. Image below CTAs. Hero height auto.

### 2.4 HERO — SERVICE PAGE

Same height constraints as home hero.
Layout: full 12-column width. Text left-aligned. No image in hero — background is neutral-50.

Content structure:
Breadcrumb (--text-sm, neutral-400): Home › Services › [SERVICE_NAME] H1 (--text-3xl): "[SERVICE_NAME] in [CITY] — [KEY_DIFFERENTIATOR]" Subheading (--text-md, neutral-600): [One sentence: problem → solution] CTA row: [Primary: "Book now — same day"] [Secondary: "Call [PHONE]"] Trust inline: [dot] Licensed [·] [RATING]★ Google [·] NATE [·] [KEY_GUARANTEE]

### 2.5 MICRO TRUST BAR

Height: auto. Padding: --space-6 vertical.
Background: --color-bg-secondary. Border top + bottom: --border-default.
Layout: 5 items in a row, centered, equal spacing. On mobile: wrap to 2 rows.

Items (each): large value --text-lg font-semibold + small label --text-xs uppercase neutral-500
Item 1: [[ GOOGLE_RATING ]]★ / "Google reviews" Item 2: Since [[ FOUNDING_YEAR ]] / "years of service" Item 3: NATE / "certified techs" Item 4: BBB [[ BBB_RATING ]] / "accredited" Item 5: Lic #[[ LICENSE_SHORT ]] / "state licensed"

### 2.6 SERVICE CARD (grid)

Used in: Home services section, Related services section on service pages.
Layout: 1/4 width desktop (3 columns + 1 CTA card), 1/2 tablet, full mobile.
Structure:
[Icon --icon-xl, color: --color-cta-primary] [Service name — --text-lg font-medium] [One-line description — --text-sm neutral-600] [Arrow link: "Learn more →" --text-sm cta-primary]

Border: --border-default. Radius: --radius-card. Padding: --card-padding.
Hover: border-color transitions to --color-cta-primary in --transition-base. No shadow.

### 2.7 CTA BANNER (urgency / offer)

Full-bleed background — breaks outer margins. Background: --color-cta-primary or primary-700.
Text: --color-text-on-primary. Padding: --space-16 vertical.
Layout: text left (8/12 col) + button right (4/12 col) on desktop. Stacked on mobile.
[Offer headline — --text-xl font-semibold] [Subtext — --text-sm, 80% opacity] [CTA button — inverted: white bg, primary text] [Optional: financing badge]

### 2.8 VALUE PROPOSITION (3-column)

3 equal columns. Each column:
[Icon --icon-xl] [Headline — --text-lg font-medium] [Body — --text-sm neutral-600, max 2 lines]

No cards — open layout. Column separator: 1px neutral-200 vertical line on desktop.
Columns MUST contain concrete promises, not adjectives. Example: "Same-day service" not "Fast service".

### 2.9 REVIEW CARD

Static (no carousel). Display 3–4 cards in a row on desktop, 2 on tablet, 1 on mobile.
Structure:
[★★★★★ — color: #F59E0B (amber-400, fixed — not brand color)] [Review text — --text-sm, italic, neutral-700, max 3 lines] [Reviewer name — --text-sm font-medium neutral-900] [Service + city — --text-xs neutral-500] [Source: Google logo + "Google Review" — --text-xs neutral-400]

Border: --border-default. Radius: --radius-card. Padding: --card-padding.

### 2.10 SYMPTOMS GRID (service pages only)

2×2 or 2×3 grid. Each cell:
[Problem headline — --text-sm font-semibold] [Solution line — --text-sm neutral-600]

Background: --color-bg-secondary. Radius: --radius-md. Padding: --space-6.
No icons in this component — text only.

### 2.11 PROCESS STEPS (service pages only)

5-step horizontal flow on desktop, vertical on mobile.
Each step:
[Step number — --text-lg font-semibold cta-primary] [Label — --text-sm neutral-700, max 3 words]

Connector between steps: 1px dashed neutral-300 line. Last step: no connector.

### 2.12 SERVICE TIERS (service pages only)

3 cards. Center card is "Most popular" — accented with --border-accent (1.5px primary-500).
Each card:
[Optional badge: "Most popular" — --text-xs bg-primary-50 text-primary-700] [Tier name — --text-lg font-semibold] [Price — "From $X" — --text-2xl font-semibold cta-primary] [Feature list — --text-sm neutral-600, 3–4 items] [CTA button — primary or secondary style]

Width: 4/12 each on desktop. Full width stacked on mobile.

### 2.13 BRAND LOGOS ROW (equipment + certifications)

Two rows. Row 1: equipment brands. Row 2: certifications + affiliations.
Each logo: grayscale filter(grayscale 100%) opacity 0.5. On hover: filter removed, opacity 1.
Max logo height: 32px. Min spacing between logos: --space-8.
Accessibility: each logo image has alt="[Brand name] HVAC systems" or alt="[Cert name] certification badge".

### 2.14 FAQ ACCORDION

Each item: question + collapsible answer.
Closed state: [Question --text-md font-medium] [+ icon --icon-sm right-aligned]
Open state: [Question] [– icon] + [Answer --text-sm neutral-600, --space-4 top padding]
Border bottom: --border-default between items. No border on last item.
Aria attributes REQUIRED: aria-expanded, aria-controls, role="button" on trigger.
Include FAQ schema markup (JSON-LD) for every FAQ item on every page — this is mandatory for SEO.

### 2.15 CTA CLOSE + FORM

Layout: 2-column on desktop. Left (7/12): headline + subtext + phone number. Right (5/12): form.
Form fields: exactly 3. Name (text), Phone (tel), Service needed (select — populated from services list).
Submit button: full width, primary style. Label: "Request same-day service →"
Below submit: "--text-xs neutral-500: We'll call you back within 2 hours during business hours."
Form validation: all 3 fields required. Phone: format validation. Accessible error states with aria-describedby.

### 2.16 STICKY MOBILE CTA BAR

Visible only on mobile (≤599px). Fixed bottom. Height: 56px.
Background: --color-bg-primary. Border top: --border-strong.
Layout: [Call button 50% — secondary style, phone icon + "Call now"] [Book button 50% — primary style, "Book online"]
Z-index: above all content. Add padding-bottom: 56px to page body on mobile to prevent content hiding behind bar.

---

## PHASE 3 — PAGE TEMPLATES

### 3.1 HOME PAGE

Strict section order — do not reorder:

1. OFFER BAR (seasonal, 28px, full-bleed)
2. NAVBAR (sticky, 44px)
3. HERO — HOME (78–85vh, rhythm break: image bleeds 40px right beyond margin)
4. MICRO TRUST BAR (full-bleed background, --color-bg-secondary)
5. SERVICES SECTION
   - Section heading (H2): "Our Services"
   - Grid of SERVICE CARDs — all services. Last card: "View all services →" link card.
   - Layout: 4 columns desktop, 2 tablet, 1 mobile
6. CTA BANNER (full-bleed, --color-cta-primary bg, rhythm break: full 100vw)
   - Headline: [[ OFFER_HEADLINE ]]
   - Subtext: [[ OFFER_SUBTEXT ]]
   - CTA: [[ OFFER_CTA_LABEL ]]
7. VALUE PROPOSITION (3 columns)
   - Column 1: [[ VP_1_HEADLINE ]] / [[ VP_1_BODY ]]
   - Column 2: [[ VP_2_HEADLINE ]] / [[ VP_2_BODY ]]
   - Column 3: [[ VP_3_HEADLINE ]] / [[ VP_3_BODY ]]
8. REVIEWS (3–4 cards, static grid)
   - Micro-CTA after last review: "[[ MICRO_CTA_TEXT — e.g. Ready to experience this? Book today ]] →"
9. BRAND LOGOS ROW (equipment + certs)
10. ABOUT US
    - Layout: 6/12 text + 6/12 image on desktop. Stack on mobile.
    - Image: real photo of owner or team. Rhythm break: image bleeds 40px beyond right margin on desktop.
    - Content: [[ ABOUT_HEADLINE ]] / [[ ABOUT_BODY — max 80 words ]] / [[ OPTIONAL: FOUNDER_NAME ]]
11. SERVICE AREA + GBP MAP
    - Left 7/12: Google Maps embed (GBP iframe) — provide [[ GOOGLE_MAPS_EMBED_URL ]]
    - Right 5/12: city list with internal links to city landing pages
12. FAQ ACCORDION
    - Minimum 6 questions. Populate:
      [[ FAQ_1_Q ]] / [[ FAQ_1_A ]]
      [[ FAQ_2_Q ]] / [[ FAQ_2_A ]]
      [[ FAQ_3_Q ]] / [[ FAQ_3_A ]]
      [[ FAQ_4_Q ]] / [[ FAQ_4_A ]]
      [[ FAQ_5_Q ]] / [[ FAQ_5_A ]]
      [[ FAQ_6_Q ]] / [[ FAQ_6_A ]]
13. CTA CLOSE + FORM
14. FOOTER
    - Layout: 4-column grid. Col 1: logo + tagline + NAP. Col 2: Services links. Col 3: City links. Col 4: Company (About, Blog, Financing, Careers, Privacy).
    - Bottom bar: copyright + license number + "Site by [[ OPTIONAL: AGENCY_NAME ]]"
    - Full NAP: [[ COMPANY_NAME ]] · [[ FULL_ADDRESS ]] · [[ PHONE_NUMBER ]] · [[ EMAIL ]]

### 3.2 SERVICE PAGE TEMPLATE (reusable for every service)

Variables to fill per service: [SERVICE_NAME], [SERVICE_SLUG], [SERVICE_H1], [SERVICE_SUBHEADING], [SERVICE_SYMPTOMS_×6], [SERVICE_TIERS_×3], [SERVICE_REVIEWS_×4], [SERVICE_FAQS_×6].

Strict section order:

1. OFFER BAR (inherited — same as home)
2. NAVBAR (inherited)
3. HERO — SERVICE PAGE (with breadcrumb, H1 includes city)
4. SYMPTOMS / PROBLEMS GRID (2×3 grid — problems this service solves)
   - [[ SYM_1_PROBLEM ]] / [[ SYM_1_SOLUTION ]]
   - [[ SYM_2_PROBLEM ]] / [[ SYM_2_SOLUTION ]]
   - [[ SYM_3_PROBLEM ]] / [[ SYM_3_SOLUTION ]]
   - [[ SYM_4_PROBLEM ]] / [[ SYM_4_SOLUTION ]]
   - [[ SYM_5_PROBLEM ]] / [[ SYM_5_SOLUTION ]]
   - [[ SYM_6_PROBLEM ]] / [[ SYM_6_SOLUTION ]]
5. CTA BANNER — COMPACT (single line: "[[ URGENCY_LINE ]]" + CTA pill + phone)
6. PROCESS STEPS (5 steps — what happens when you call)
   - Step 1: [[ STEP_1 — e.g. "Schedule online or call" ]]
   - Step 2: [[ STEP_2 — e.g. "Tech arrives same day" ]]
   - Step 3: [[ STEP_3 — e.g. "Free diagnosis with repair" ]]
   - Step 4: [[ STEP_4 — e.g. "Upfront pricing, no surprises" ]]
   - Step 5: [[ STEP_5 — e.g. "Repair done, guaranteed" ]]
7. SERVICE TIERS (3 cards: Repair / Repair + Tune-up / Replacement)
   - [[ TIER_1_NAME ]] / [[ TIER_1_PRICE ]] / [[ TIER_1_FEATURES ]]
   - [[ TIER_2_NAME ]] / [[ TIER_2_PRICE ]] / [[ TIER_2_FEATURES ]] — mark as "Most popular"
   - [[ TIER_3_NAME ]] / [[ TIER_3_PRICE ]] / [[ TIER_3_FEATURES ]]
8. REVIEWS — filtered to this service (4 cards)
   - Each review MUST mention [SERVICE_NAME] explicitly in text or source label
   - Micro-CTA after last review (same pattern as home)
9. BRAND LOGOS + CERTS ROW (compact — same as home but tighter padding)
10. FAQ ACCORDION — service-specific questions (6 minimum)
    - Questions MUST address: cost, repair vs. replace, response time, warranty, brands serviced, what to do before tech arrives
11. SERVICE AREA LINKS (no map embed — city links only as text grid)
    - Grid: 3 columns. Each link: "[SERVICE_NAME] in [CITY] →" pointing to /services/[service-slug]/[city-slug]
12. RELATED SERVICES (3 cards using SERVICE CARD component)
    - Populate with 3 other services most likely to be needed by this visitor
13. CTA CLOSE + FORM (service-specific copy)
14. FOOTER (inherited)

### 3.3 CITY + SERVICE LANDING PAGE TEMPLATE

URL pattern: /services/[service-slug]/[city-slug]
This is the most conversion-critical page — it receives PPC and local SEO traffic.

Inherits SERVICE PAGE TEMPLATE with these overrides:
- Every mention of [CITY] in H1, hero subheading, and trust inline uses the specific city slug
- Add a 2-sentence city-specific paragraph below the symptoms grid: local knowledge signal
- Review cards: prioritize reviews from customers in this city (or nearest city)
- FAQ item 1 MUST be: "Do you serve [CITY]?" — answer confirms coverage and lists nearby areas
- Schema: add LocalBusiness schema with city-specific service area
- Meta title: "[SERVICE_NAME] in [CITY], [STATE] | [COMPANY_NAME] — Same-Day Service"
- Meta description: max 155 characters including city, service, phone

### 3.4 ABOUT US PAGE

Sections in order:
1. OFFER BAR + NAVBAR (inherited)
2. Page hero: H1 "[[ ABOUT_PAGE_H1 ]]" — full width, neutral-50 bg, no image
3. Story section: [[ FOUNDER_STORY — max 200 words ]] + team photo (8/12 + 4/12 grid)
4. Values: 3-column (same component as VALUE PROPOSITION)
5. Team section: grid of team member cards [photo + name + role + cert badge]
   - [[ TEAM_MEMBER_1_NAME ]] / [[ TEAM_MEMBER_1_ROLE ]] / [[ TEAM_MEMBER_1_CERT ]]
   - [[ OPTIONAL: TEAM_MEMBER_2 ]] / ... / ...
6. Certifications + affiliations: BRAND LOGOS ROW component
7. CTA CLOSE + FORM
8. FOOTER

### 3.5 CONTACT / BOOKING PAGE

Conversion-only page. No sidebar. No distraction.
1. NAVBAR only (no offer bar)
2. Full-width form section:
   - H1: "[[ BOOKING_HEADLINE — e.g. "Book Your Service — Same Day Available" ]]"
   - Form fields: Name, Phone, Email, Service needed (select), Preferred date, Message (optional)
   - Submit: "Request service now →"
   - Side panel (4/12): phone number large, hours, emergency note
3. MICRO TRUST BAR
4. FOOTER (no CTA close — this page IS the close)

### 3.6 FINANCING PAGE

1. OFFER BAR + NAVBAR
2. Hero: H1 "[[ FINANCING_H1 ]]" + subheading explaining financing availability
3. Financing options: 3-column tier layout (same component as SERVICE TIERS)
   - [[ FINANCING_OPTION_1_NAME ]] / [[ FINANCING_OPTION_1_TERMS ]] / [[ FINANCING_OPTION_1_DETAILS ]]
   - [[ FINANCING_OPTION_2_NAME ]] / [[ FINANCING_OPTION_2_TERMS ]] / [[ FINANCING_OPTION_2_DETAILS ]]
   - [[ OPTIONAL: FINANCING_OPTION_3 ]]
4. FAQ ACCORDION (6 financing-specific questions)
5. CTA CLOSE + FORM
6. FOOTER

### 3.7 BLOG / RESOURCES PAGE

1. OFFER BAR + NAVBAR
2. Page hero: H1 "[[ BLOG_HEADLINE ]]"
3. Featured post (full width, large image)
4. Post grid: 3 columns. Each post card: [image] [category tag] [title --text-lg] [excerpt --text-sm] [Read more →]
5. Sidebar (optional): [[ OPTIONAL: SIDEBAR_WIDGET_1 ]] (e.g. emergency CTA widget)
6. Pagination
7. FOOTER

---

## PHASE 4 — ACCESSIBILITY REQUIREMENTS

Every page and component MUST comply with WCAG 2.1 AA. Non-negotiable requirements:

**Contrast:** All text/background combinations MUST pass 4.5:1 (normal text) or 3:1 (large text ≥18px or ≥14px bold). Verify every semantic color assignment from Phase 1.

**Keyboard navigation:**
- All interactive elements reachable and operable via Tab key
- Visible focus indicator on every focusable element using --border-focus
- Skip-to-content link as first element in DOM, visible on focus
- Dropdown menus closeable with Escape key
- No keyboard trap anywhere

**Screen readers:**
- Semantic HTML: nav, main, section, article, aside, footer with proper landmarks
- Every image has descriptive alt text. Decorative images: alt=""
- Form inputs: every field has associated label (not placeholder-only)
- Error messages: aria-describedby linking input to error text
- Dynamic content: aria-live regions for form submission feedback
- FAQ accordion: aria-expanded, aria-controls on every trigger

**Touch targets:** Minimum 44×44px on all interactive elements (WCAG 2.5.5)

**Motion:** All CSS transitions wrapped in @media (prefers-reduced-motion: no-preference). Default state: no motion.

**Color alone:** Never use color as the sole means of conveying information (WCAG 1.4.1). Always pair with text, icon, or pattern.

---

## PHASE 5 — SEO & SCHEMA REQUIREMENTS

Apply to every page:

**Meta tags:**
- Title: [Page-specific title] | [COMPANY_NAME] — max 60 characters
- Description: max 155 characters, includes city + service + phone
- Canonical URL: every page
- Open Graph: title, description, image (1200×630px), url, type
- Twitter Card: summary_large_image

**Schema markup (JSON-LD) — REQUIRED on every page:**
- LocalBusiness schema on all pages: name, url, telephone, address, geo, openingHours, priceRange
- Service schema on all service pages: name, provider, areaServed, serviceType
- FAQ schema on all pages with FAQ section
- BreadcrumbList schema on all pages except Home
- Review/AggregateRating schema on pages with reviews

**Technical SEO:**
- H1: exactly one per page
- Header hierarchy: H1 → H2 → H3 (no skipping levels)
- Image filenames: descriptive slugs (hvac-technician-austin-tx.jpg not IMG_001.jpg)
- Alt text: every image
- Internal links: every service mentioned in copy links to its service page
- City pages: link back to parent service page (canonical chain)
- XML sitemap: auto-generated, includes all pages
- robots.txt: allow all, point to sitemap

---

## PHASE 6 — ELEMENTOR COMPATIBILITY RULES

This site will be rebuilt in Elementor after Manus delivers the HTML/CSS prototype. Design ALL components to comply with Material Design spacing and visual rules for maximum compatibility:

- Use only CSS custom properties (variables) for all colors, spacing, typography — no hardcoded values
- All font sizes reference the type scale tokens — Elementor can override these per widget
- Grid columns use CSS Grid with named areas — not floats or absolute positioning
- Every section has an explicit padding token referencing --section-padding-* variables
- No component uses JavaScript for its visual state — CSS-only hover/focus states where possible
- JS is permitted only for: offer bar season switcher, sticky nav scroll behavior, FAQ accordion, mobile menu, form validation
- Export design tokens as a separate tokens.css file that Elementor Global Settings can reference
- Deliver a living style guide HTML page (/style-guide.html) showing every component, color swatch with contrast ratio, type specimen, spacing scale, and icon reference

---

## PHASE 7 — DELIVERABLES CHECKLIST

Deliver in this order. Stop and confirm between each major phase.

✅ Phase 1 complete when: tokens.css file delivered with all colors (WCAG verified), typography, spacing, radius, and motion tokens as CSS custom properties.

>>> REPO: also emit `tokens.json` next to tokens.css, in this repo's schema — it is
what the Elementor pipeline actually consumes:

    {
      "site": "<slug>", "content_width": <int>,
      "fonts":  {"heading": "...", "body": "..."},
      "colors": {"<family>": {"50": "#...", ..., "900": "#..."}},
      "roles":  {"bg-primary": {"hex": "#...", "global": null},
                 "text-primary": {...}, "cta-bg": {...}, "dark-bg": {...}},
      "type_scale": {"text-sm": 16, ...}, "spacing": {...}, "radii": {...},
      "button": {"bg": "#...", "hover": "#...", "text": "#...",
                 "radius": "...", "hover_animation": ""},
      "links": {...}, "phone": {...}
    }

If the generator cannot emit it, derive it afterwards:
    python3 scripts/analyze-prototype.py <prototype-dir> --emit-tokens projects/<site>/tokens.json
<<<

✅ Phase 2 complete when: component-library.html page delivered with every component in Phase 2 rendered and documented.

✅ Phase 3 complete when: all page templates delivered as separate HTML files:
  - index.html (Home)
  - services/[service-slug].html (one per service)
  - services/[service-slug]/[city-slug].html (one per service × city combination)
  - about.html
  - contact.html
  - financing.html
  - blog.html
  - style-guide.html

✅ Phase 4 complete when: accessibility audit run on all pages. Report delivered listing any WCAG AA failures. All failures resolved before handoff.

✅ Phase 5 complete when: all schema markup validated via Google Rich Results Test. No errors.

✅ Phase 6 complete when: tokens.css confirmed compatible with Elementor CSS variable override system. Elementor import notes delivered.

---

## CONSTRAINTS

- NEVER deviate from the 12-column 8px grid
- NEVER use box-shadow for decoration
- NEVER use a color combination that fails WCAG AA
- NEVER auto-play any media
- NEVER use a carousel or slider — all content must be visible in static layout
- NEVER use placeholder text as a form label
- NEVER skip heading levels
- NEVER create a page without a canonical URL
- NEVER hardcode color hex values in component CSS — always reference a CSS variable
- The offer bar MUST be exactly 28px. The navbar MUST be exactly 44px. These are not suggestions.
- Every CTA button on every page must have a visible, descriptive label — no icon-only buttons
- Stop and ask before: adding any page not listed in Phase 3, deviating from the section order in any template, or using any external library not explicitly specified