---
name: vitalair-page-audit
description: >
  Audit-first review for existing VitalAir Elementor pages/templates. Use when
  asked to review, clean up, fix, or improve an existing VitalAir page, or before
  restyling one, to check it against the VitalAir brand kit and Elementor best
  practices — without breaking the layout or fighting the brand. Pairs with
  vitalair-ui-design (the design rules) and vitalair-content-style (the copy).
---

# VitalAir Page Audit

Reviews existing VitalAir Elementor pages against the brand kit. This is the Elementor-aware replacement for generic web-redesign checklists — it does **not** assume a CSS/React codebase, and it does **not** apply "premium web" defaults that conflict with the VitalAir brand.

## How this works

1. **Scan** — read the page/template JSON. Note: Container vs. legacy Section model, section order and backgrounds, widget types, and where styling is set (inline vs. global slot).
2. **Diagnose** — run the audit below and list every issue found, with the widget/section it applies to.
3. **Fix in place** — apply targeted corrections that keep the existing structure and reuse existing templates. Do not rebuild from scratch.

## Brand-consistency audit (VitalAir-specific)

Flag and fix:

- **Broken section structure.** Any section not built as **Section → Content Container → content**. Every section must be a full-width outer Section wrapping a single Content Container that holds the content.
- **Padding on the wrong element.** Padding must live ONLY on the Content Container (which always has the default padding). Flag any padding on the outer Section, on child widgets, or on nested containers/columns inside the Content Container — strip it and let the Content Container's padding + gap handle spacing.
- **Button hover animation.** Any button with a size/shape hover animation (`grow`, `shrink`, `scale`, etc.). Buttons change background + text color only — set `hover_animation` to empty/`none`.
- **Wrong font.** Any widget using "Noto Sans Coptic" (the leftover Hello default) or browser default. Replace with **Poppins**.
- **Styling via global slots.** Colors/typography pulled from Elementor global slots instead of set inline — the kit's globals are still Hello defaults, so global-referenced styling renders off-brand. Set values inline.
- **Off-brand CTAs.** Buttons that aren't the brand pill: green `#74BC2B` bg, white text, `border-radius: 999px`, darker-green `#5A9421` hover, 16/30px padding, 15px/700. Fix any square, outline, or wrong-color primary buttons.
- **Missing eyebrow pattern.** Section headings without the green (`#8FD13E`) uppercase 11–12px, ~2.6px-tracked eyebrow above them.
- **Broken section rhythm.** Two identical backgrounds stacked in a row. The kit alternates navy `#16163F` / white `#FFFFFF` / light `#EEF2FA`. Reassign so adjacent sections differ.
- **Type scale drift.** Heroes not in the 52–70px h1 range, section headings off the 40–44px h2 range, body outside 15–18px.
- **Unbounded text width.** Text content not constrained to a ~1200–1240px boxed inner width.
- **Legacy Section model on a page meant to match newer ones.** Note it; migrate to Containers only if the task calls for it (don't break a working page just to modernize).
- **Missing mobile padding.** Sections without responsive padding (kit uses heavier vertical padding on mobile).
- **Missing CTA.** A major section with no path to contact/schedule.

## Do NOT "fix" these (they are on-brand, not mistakes)

Generic redesign advice flags these — but for VitalAir they are correct:

- **Colored hero/feature bands** (navy, occasionally blue). Keep them.
- **Alternating dark and light sections down the page.** This is the intended rhythm, not a copy-paste accident.
- **Multiple brand accents** (navy + blue + green). The "use only one accent" rule does not apply here.
- **Pill-shaped primary buttons.** Required, not to be squared off.
- **All-caps eyebrow labels.** These are the brand's section labels.

## SEO checks

- **Exactly one H1** on the page (the hero headline). Additional headings are H2/H3
  in a logical hierarchy (no skipped levels).
- **Meta title** set and under ~60 characters.
- **Meta description** set and under ~155 characters.
- **URL slug** lowercase and hyphenated, no stop-word clutter.
- **Target keyword** appears in the H1 and the intro paragraph, naturally.
- Note: Elementor template JSON does not carry WordPress SEO meta — the title,
  description, and slug are a handoff note to set on the WP page (Rank Math / Yoast)
  at publish time. The audit confirms they are provided and valid.

## Internal linking checks

- The page includes the **required internal links** from the brief, with
  descriptive anchor text (not "click here").
- No dead links (`href="#"` or empty). External links set appropriately.
- Key CTAs point to real destinations (contact, service pages, etc.).

## Media checks

- Every image has descriptive **alt text**.
- Placeholders for live widgets (review sliders, forms) are clearly labeled so
  they get wired up after import.

## Content audit

Defer to `vitalair-content-style` for voice. Quick flags: missing local/Atlanta framing; hype words ("Elevate," "Seamless," "world-class"); dense multi-sentence blocks; passive or salesy tone; missing "symptom → reassurance → CTA" structure on service sections.

## Elementor hygiene

- Every element has a unique `id`; required keys (`elType`, `widgetType`, `elements`, `settings`) intact.
- Images have meaningful `alt` text.
- No dead buttons (links to `#`); forms use the kit's shortcode/form pattern.
- Reuse header `10` and footer `181` rather than duplicating chrome.

## Fix priority (highest impact, lowest risk first)

1. Font swap to Poppins.
2. Move styling from global slots to inline; correct off-brand colors.
3. Fix CTAs to the brand green pill.
4. Restore section-background rhythm and eyebrow pattern.
5. Constrain text width; set mobile padding.
6. Tune the type scale.

## Rules

- Work within Elementor and the existing kit. Do not migrate away from Elementor or invent a new aesthetic.
- Do not break working layout or functionality. Keep changes targeted and reviewable.
- When restyling, keep the JSON complete and valid (see full-output-enforcement).
