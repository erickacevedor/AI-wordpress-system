---
name: lenz-content-style
description: >
  The Lenz Heating & Cooling copy voice and the client's settled content rules
  (claims, offers, names, CTA wording). Use whenever writing, editing, condensing
  or reviewing any text for a Lenz page: headings, body, CTAs, FAQs, meta titles
  and descriptions. Triggers: "write Lenz copy", "Lenz CTA", "Lenz FAQ", "Lenz
  meta description", "rewrite this for Lenz".
---

# Lenz: Content Style

## 1. Where copy comes from

- Page copy comes from the client-approved doc (`pages/<slug>/source.docx`),
  **verbatim**. Do not rewrite approved copy for style. Your job is mapping it to
  blocks, not improving it.
- ClickUp decisions override the doc. The settled ones are applied automatically by
  `service_page.py` (`FIXES`, `REGEX_FIXES`, `CARD_FIXES`) and listed in each page's
  `HANDOFF-notes.md`. A new decision becomes a new entry there, not a manual edit
  in one page.
- Write new copy only where no doc exists. Eyebrows, hero badges and help-tile
  lines are builder-owned microcopy: write them in this voice, no note needed. Body
  copy, claims, prices or offers you write go in the page's `notes`.

## 2. Voice

- Local, family, plain-spoken. Des Moines metro and Central Iowa, named often and
  naturally: Urbandale (main office), Waukee, West Des Moines, Ankeny, Johnston,
  Clive, Grimes, Altoona, Norwalk, Windsor Heights.
- Reassuring, no pressure, honest about what a visit costs. Decision support
  ("we'll explain why"), not hard sell.
- Proof through specifics: since 2009, 24/7/365, Iowa Master Licensed `#50871-CL`,
  veteran and woman-owned, family operated, over 2,000 5-star reviews, featured on
  WHO 13 News' Hello Iowa!
- Short sentences, second person, contractions. No hype words ("revolutionary",
  "unparalleled", "best-in-class"), no exclamation stacks.
- Real examples of the tone: "Tell us what you're hearing or feeling and we'll work
  it out." · "Let Our Family Help Yours" · "What you get on every single call" ·
  "No heat? We diagnose it fast."

## 3. Settled content rules (from ClickUp; never reintroduce the old version)

| Rule | Instead of |
|---|---|
| Only estimates on **new equipment and full system replacements** are free; repairs carry a diagnostic fee | "free second opinions", "free diagnostics", "no trip or diagnostic fees" |
| "upfront pricing before any work begins" | "no trip fees" |
| Service agreement discounts apply to **parts only** ("10 to 20% off parts") | "discounts on repairs" |
| "Over 2,000 5-star reviews" | "1,800+" |
| "Main Office" (Urbandale) | "Headquarters" |
| Spell out "year" | "yr" |
| "Give us a call" | "Talk to us" |
| Ecobee thermostat | Nest |
| Optimus is a financing company, not an equipment brand | listing it among brands |
| Contact email `Sierra@LenzHeatingandCooling.com` | any other address |
| Haley's title: "Office Assistant / Marketing Specialist" | older titles |
| "Real reviews from Des Moines homeowners" links to their Google reviews | a dead link |
| DCG Volleyball is among the sponsors | sponsor lists without it |

**Open, do not change on your own:** whether plan members really get "no trip or
diagnostic fees" (it appears on Heating Maintenance and Maintenance Plans as a plan
perk). Leave the doc wording and flag it; Erick confirms with the client.

Financing: 0% deferred interest for qualified buyers **through Synchrony Bank**,
always with "subject to credit approval". Never promise approval or a rate.

## 4. CTAs

- Every on-page CTA anchors to the estimate form (`#contact`, `L["form"]`) unless
  the doc names another target. The phone is always `(515) 225-6446`, `tel:+15152256446`.
- Standard pair in heroes: a gold action ("Schedule AC Repair", "Get a Free
  Estimate" only where the estimate really is free) + "Call (515) 225-6446".
- Labels say what happens: "Schedule Your Service Online", "See If You Qualify",
  "Enroll & Start Earning", "See Current Specials", "Explore Heating Services".
  Never "Click here", "Learn more", "Submit" alone, or an icon-only button.

## 5. Formatting

- Keep the doc's casing. The site mixes Title Case ("Over 2,000 5-Star Reviews
  Across Central Iowa") and sentence case ("Financing that fits your budget") in
  H2s; for a heading you write, match the neighbouring blocks on the same page.
  Eyebrows are short sentence-case labels ("Why finance", "How it works").
- In Python strings use HTML entities: `&apos;` for apostrophes, `&amp;` for `&`.
- Bold (`<b>`) only for labels and key numbers, the way the docs use it.
- No em dashes or en dashes in new copy (doc copy is kept as written).
- One H1 per page; H2 per section; H3 inside cards. Never skip a level.

## 6. SEO text

- Meta title from the doc; if it lacks the brand, the builder appends
  `| Lenz Heating & Cooling`.
- Meta description from the doc, run through the same fixes. The gate warns over
  **60** characters for the title and **155** for the description: flag those in
  `notes`, do not silently trim approved copy.
- Canonical: `https://www.lenzheatingandcooling.com/<slug>/`.
- Schema: none in the page JSON (ownership undecided). Never add `aggregateRating`.
