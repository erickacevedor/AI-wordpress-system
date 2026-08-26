# design-source/ — the HTML stage

**This is the front half of the pipeline, and it is optional.** Most work in this
repo never touches it.

Use it only when a site arrives with **no Elementor kit to mine** — a brand-new build,
or a design that exists as HTML/CSS somewhere else. If you have an exported kit in
`projects/<site>/current-theme/`, skip this folder entirely; the process is unchanged
and documented in [`../AGENTS.md`](../AGENTS.md).

---

## Which path am I on?

```
Do I have an exported Elementor kit for this site?

  YES ──> projects/<site>/current-theme/       ← the normal path, unchanged
          scripts/analyze-kit.py
          skills/elementor-kit-onboarding
                        │
  NO  ──> design-source/                       ← this stage
          build an HTML/CSS prototype
          projects/<site>/design-source/
          scripts/analyze-prototype.py
          skills/html-prototype-onboarding
                        │
                        ▼
          projects/<site>/tokens.json          ← THE SEAM. Both paths produce it.
                        │
                        ▼
          brand.py → pages/<slug>/build.py → validate-page.py → preview → handoff
                     (identical from here on; nothing downstream knows or cares
                      which origin the tokens came from)
```

Because the seam is `tokens.json`, this stage composes three ways:

- **HTML only** — build the prototype, stop. The deliverable is the static site.
- **WordPress only** — never open this folder.
- **HTML then WordPress** — the Lenz pattern: prototype first, then onboard it and
  build Elementor pages from the same tokens.

---

## What is in here

| | |
|---|---|
| `prompts/local-service-site.md` | A fill-in-the-blanks master prompt that produces a complete static site for a local service business: design system, 16 components, 7 page templates, accessibility and SEO requirements. Three repo adaptations are marked inline with `>>> REPO:`. |

## Using the prompt

1. Copy it, fill every `[[ BRACKETED ]]` field from the client brief. Blanks left in
   place will be built as literal placeholders — the prompt is deliberately strict.
2. Run it in whatever tool builds the prototype (it was written for a from-scratch
   HTML builder and pauses between phases for confirmation).
3. Put the result in `projects/<site>/design-source/`.
4. Onboard it — see below.

**Set `MAX_CONTENT_WIDTH` deliberately.** The prompt defaults to 1800px. Every kit in
`projects/` boxes content at 1140–1280px, and Elementor/Hello themes default to
~1140px. If the prototype is going to be rebuilt in Elementor, decide the width now:
changing it later means re-deciding every section's proportions.

## Onboarding a prototype into the pipeline

```bash
# 1. what does this design system actually contain?
python3 scripts/analyze-prototype.py projects/<site>/design-source

# 2. derive the seam
python3 scripts/analyze-prototype.py projects/<site>/design-source \
        --emit-tokens projects/<site>/tokens.json

# 3. fill the TODO markers (button spec, links, phone) from the brief, then
#    generate the <site>-* skills — see skills/html-prototype-onboarding
```

`analyze-prototype.py` reads both layers a prototype keeps its design system in.

From the **custom properties**: colour ramps, semantic roles (resolving `var()` chains
to the hex that actually lands), type scale, spacing, radii, fonts — scoring every role
for contrast against white and near-black.

From the **rules**: the button spec (`.btn` / `.btn-primary` / `:hover` — fill, hover
fill, text, radius, padding, weight, and whether the hover is an animation), the
section background bands, the font families actually assigned to `body` and the
headings, the section rhythm, and a census of every `font-size` in use with its
frequency. This layer matters because a hand-written prototype declares `--red` and
`--ink` and then hardcodes the rest: read only `:root` on one of those and you get a
palette and nothing else.

A band is identified by the markup, not the selector name — a class only counts if a
page actually puts it on a `<section>`. That is what keeps `.btn-primary` and
`.quote-form` out of the band list.

It does the counting; the judgement (which ramp is the brand primary, which role is
the CTA, whether twenty-seven font-sizes are a scale or drift, what the voice is)
stays with you.

It **will not** overwrite an existing `tokens.json`. Emit elsewhere and merge by hand
if the site already has one — tokens are hand-tuned after generation.

## The one rule that matters

**The prototype is a source design, not a deliverable.** In this repo its job is to
produce `tokens.json` and to answer "what does this brand look like". The shippable
artifact is still the Elementor page JSON, still gated by
`scripts/validate-page.py`, still handed off with a `HANDOFF-notes.md`.

Anyone running the prompt expecting a finished website will produce one — it just
isn't the thing this repo delivers.
