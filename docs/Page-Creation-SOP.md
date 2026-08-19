# Page Creation SOP (any site)

The short operator runbook: content doc in, import-ready Elementor page out. Where
`docs/Elementor-Site-Playbook.md` explains how a site gets *onboarded* (once), this
explains how a *page* gets built (every time).

Swap `<site>` for the site slug throughout — the process is identical for every site
in `projects/`.

> **Prerequisite:** the site's `<site>-*` skills already exist, generated once by
> `elementor-kit-onboarding`. If `projects/<site>/skills/` is empty, onboard the kit
> first. Never build a page from an ad-hoc read of the kit — that is how a site drifts
> off its own brand.

## What powers this

The site's generated skills (in `projects/<site>/skills/`) plus the portable
`full-output-enforcement`. You mostly talk to the first one; it calls the rest.

| Skill | Role in the process |
|-------|---------------------|
| `<site>-page-builder` | **Entry point.** Orchestrates the whole pipeline. |
| `<site>-design-read` | Reads the brief, picks the closest existing page to mirror. |
| `<site>-content-style` | Writes/edits copy in the site's voice. |
| `<site>-ui-design` | Applies the brand colors, fonts, CTA style, boxed section layout. |
| `full-output-enforcement` | Keeps the emitted Elementor JSON complete and valid. |
| `<site>-page-audit` | Final brand + hygiene + responsive check before handoff. |

## The process

### Step 1 — Put the content in the page folder

```
mkdir -p projects/<site>/pages/<page-slug>
```

Drop the source in it as `source.<ext>` — a client `.docx`, a brief, or a pasted
outline. A filled `content-brief-template.md` is welcome but optional; in practice
most pages start from whatever the client actually sent.

Content quality in, page quality out. Real headings, real local detail and real FAQ
answers are worth more than a complete form.

### Step 2 — Hand it over

Tell the agent: **"Build a `<site>` page from this source."**

It replies with a one-line **design read** — *"a Woodstock service-area page, sibling
of Service-Marietta"* — before building anything. Confirm or redirect. This is the
cheapest correction point in the whole process; a wrong design read caught here costs
one sentence, caught after the build it costs a rebuild.

If something brand-critical is missing (hero headline, location, CTA target), it asks
one focused question rather than guessing.

### Step 3 — The agent builds

1. **Design read** — page kind + the closest existing page to mirror.
2. **Extract the source** — `.docx` → `source.txt` (watch for mojibake in curly quotes).
3. **Map to sections** — the site's own section anatomy and band rhythm.
4. **Write copy** — in the site's voice, from `<site>-content-style`.
5. **Style** — brand values from `tokens.json`, via `<site>-ui-design`.
6. **Emit JSON** — by authoring `pages/<page-slug>/build.py` on
   `scripts/elementor_builder.py` (and the site's `brand.py` where one exists), so the
   page is reproducible and the structural + responsive standards are baked in.
7. **Validate + audit** — the gate below, then `<site>-page-audit`.

Output lands in the page folder: `<page-slug>.json`, `build.py`, `PREVIEW.html`,
`HANDOFF-notes.md`.

### Step 4 — The gate (not optional)

```
python3 projects/<site>/pages/<page-slug>/build.py
python3 scripts/validate-page.py projects/<site>/pages/<page-slug>/<page-slug>.json
```

Exit 0 or it does not ship. Anything it flags is a blocker — fix it, don't explain it
away. Warnings (band rhythm, padding discipline, over-long meta) don't fail the gate,
but each one is a real finding: clear it or make a deliberate call to keep it.

### Step 5 — Review the draft

```
python3 scripts/make-preview.py projects/<site>/pages/<page-slug>/<page-slug>.json
```

`PREVIEW.html` is generated **from** the page JSON — including the breakpoints, so
resizing the window shows the real tablet and mobile layouts. Because it is generated,
it cannot drift from what ships; if it looks wrong, the page is wrong.

Because the page mirrors an approved one, styling is usually right the first time.
Your review is mostly **copy and section choice**, not pixels.

For a genuine render — Elementor's own — import into a local throwaway WordPress:

```
export SANDBOX_WP="/path/to/sandbox/wp"  SANDBOX_URL="http://localhost:10010"
scripts/sandbox.sh page projects/<site>/pages/<page-slug>/<page-slug>.json
```

Never verify against the client's live site. It usually is not reachable, and when it
is, it is not a test environment.

### Step 6 — Import into WordPress

- **Single page:** Elementor → Templates → **Import Templates** → select the JSON → Insert.
- **Whole kit:** WordPress → Elementor → Tools → **Import Kit**.

Then work the `HANDOFF-notes.md`: set the slug and SEO meta in the SEO plugin
(Rank Math / Yoast), confirm the header/footer are inherited, swap any placeholder
images, and wire up live widgets (review sliders, forms, maps).

**State the dependencies in the handoff.** The gate lists what the page needs from the
target install — addon plugins, shortcodes, custom widgets. Whoever imports it needs to
know: a missing plugin does not error, it renders an empty gap, and the client is the
one who finds it. (Elementor Pro is a given on every site we build for, so it is not
reported.)

### Step 7 — Final on-page check

In the Elementor editor and then on the published URL, confirm: the section rhythm
reads as intended, the brand font renders, CTAs are the site's button style, mobile
spacing is comfortable, accordions/forms work, and every link points somewhere real.
Full list: `docs/Publishing-QA-Checklist.md`.

## Quality bar (what "done" means)

- Reads in the site's voice, with its local/topic framing.
- Section backgrounds alternate; no two identical bands adjacent.
- Brand font, brand button, brand type scale — no invented accent colors.
- Colors set inline, not via Elementor global slots (kit globals are often fake).
- `validate-page.py` exits 0 and `<site>-page-audit` passes.
- Handoff note carries slug + meta title (<60) + meta description (<155).

## Tips for speed

- **Reuse aggressively.** Naming the closest existing page is the single biggest
  time-saver — mirror its section model and styling values, then change only copy and
  section mix. Mirror the *design decisions*; don't text-swap the kit's JSON file
  (kit pages predate the responsive standards and their ids collide on import).
- **Extract `brand.py` before page three.** Once a site has a component vocabulary
  reading from `tokens.json`, each new page is copy + section order. See the playbook's
  "three build tiers"; `projects/gcreliable/brand.py` is the worked example.
- **Batch near-identical pages.** Service-area pages differ by location and a few
  lines — hand over several sources at once.
- **Keep the source in the page folder.** Future edits start from the same source of
  truth instead of from the built JSON.
- **Don't ask for a redesign mid-build.** If you want a different look, that's a
  separate, off-brand task — the builder's job is kit consistency.
- **Replacing an existing page?** Generate the change summary rather than writing it:
  `python3 scripts/page-diff.py <new>.json --find`, then `--kit-page <id> --markdown`,
  and paste the result into the handoff. Clients approving a redesign they cannot
  preview need to see exactly what they are losing.
