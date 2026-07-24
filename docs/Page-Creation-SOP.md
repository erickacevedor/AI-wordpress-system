# VitalAir — Fast Page Creation SOP

A repeatable process for turning a content doc into an on-brand, import-ready
Elementor page for the VitalAir site. The goal is a new page in ~10–15 minutes
that looks like it always belonged in the kit.

## What powers this

Six skills in `skills/` do the work. You mostly talk to the first one; it calls
the rest:

| Skill | Role in the process |
|-------|---------------------|
| `vitalair-page-builder` | **Entry point.** Orchestrates the whole pipeline. |
| `vitalair-design-read` | Reads the brief, picks the closest existing page to mirror. |
| `vitalair-content-style` | Writes/edits copy in the VitalAir voice. |
| `vitalair-ui-design` | Applies brand colors, Poppins, pill CTAs, layout. |
| `full-output-enforcement` | Ensures the Elementor JSON comes out complete/valid. |
| `vitalair-page-audit` | Final brand + hygiene check before handoff. |
| `minimalist-ui-OFF-BRAND` | Ignore for VitalAir — off-brand, opt-in only. |

## The process

### Step 1 — Write the content brief
Fill in `content-brief-template.md`: page type, location, hero, sections, FAQ,
CTA. You don't need every field — blanks get inferred from the closest existing
page. Content quality in = page quality out, so focus on real headings, real
local details, and real FAQ answers.

### Step 2 — Hand it over
Tell Claude: **"Build a VitalAir page from this brief"** and attach/paste the
filled template. Claude states a one-line "design read" (e.g. *"a Woodstock
service-area page mirroring Service-Marietta"*) so you can confirm direction
before it builds. If something brand-critical is missing (hero headline,
location, CTA), it asks one quick question instead of guessing.

### Step 3 — Claude builds (automatic)
The page-builder pipeline runs:
1. **Design read** — pick page kind + closest existing page/template to clone.
2. **Map to sections** — navy hero → alternating white/`#EEF2FA` bands →
   icon-box grids → FAQ accordion → closing CTA.
3. **Write copy** — local, plain, reassuring; "symptom → reassurance → CTA".
4. **Style inline** — navy hero, green `#74BC2B` pill CTAs, Poppins, type scale,
   green uppercase eyebrows, ~1200px text width, header `10` + footer `181`.
5. **Emit full JSON** — complete tree, unique ids, all keys, no truncation.
6. **Audit** — brand + Elementor hygiene check; keeps on-brand elements intact.

The fast route is **clone-and-swap**: copy the closest `content/page/<id>.json`,
replace the copy, re-point the location, regenerate all element ids, keep the
styling. Author from scratch only when nothing is close.

### Step 4 — Review the design read + draft
Skim the returned page. Because it clones an approved page, styling is usually
right the first time — your review is mostly about **copy and section choice**,
not pixels.

### Step 5 — Import into WordPress/Elementor
- **Single page:** Elementor → Templates → **Import Template** → select the page JSON.
- **Whole kit:** WordPress → Elementor → Tools → **Import Kit** → the full export.
- Set the page slug/SEO, assign header `10` + footer `181` if not inherited, publish.

### Step 6 — Final on-page check
In the Elementor editor confirm: navy hero, alternating section backgrounds,
green pill CTAs, Poppins rendering, mobile spacing, FAQ toggles work, and all
links point somewhere real.

## Quality bar (what "done" means)

- Reads in the VitalAir voice with local Atlanta framing.
- Alternating navy/white/light section rhythm; no two same-bg sections in a row.
- Green pill CTAs; green uppercase eyebrows above headings; Poppins throughout.
- Colors set inline (not via Elementor global slots).
- JSON imports cleanly (valid, unique ids, nothing truncated).

## Tips for speed

- **Reuse aggressively.** Naming the closest existing page in the brief is the
  single biggest time-saver.
- **Batch service-area pages.** They're near-identical except location + a few
  lines — give Claude several briefs at once.
- **Keep a brief per page.** Store filled briefs alongside pages so future edits
  start from the same source of truth.
- **Don't ask for redesigns mid-build.** If you want a different look, that's a
  separate, off-brand task — the builder's job is kit consistency.
