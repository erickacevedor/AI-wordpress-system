---
name: petitt-design-read
description: >
  Front-door / brief-inference skill for any Petitt Heating & Cooling page request.
  Use FIRST, before building or restyling, to read the brief, state a one-line design
  read, and route to the right Petitt skills. Keeps output on-brand for an established
  Elementor kit — not a hand-coded landing page. Triggers: "new Petitt page", "build a
  Petitt page", "White House / Springfield / Hendersonville service area page",
  "match the Petitt kit".
---

# Petitt Heating & Cooling — Design Read (brief inference)

Use this at the **start** of any Petitt page task. Petitt Heating & Cooling is a
family-owned HVAC + plumbing contractor based on Homer Worsham Road, Springfield, TN,
serving Robertson, Sumner and Davidson Counties (White House, Springfield,
Hendersonville, Gallatin, Goodlettsville, Portland, Cross Plains, Greenbrier, Mt.
Juliet, East Nashville). Founded 2010. Kit is Elementor Containers on **Hello
Elementor**, and its **globals are real** — use them.

## 1. Read the room first

Before touching JSON, infer:

- **Page kind** — service-area hub (`/service-areas/<city>/`), service-area child
  (`/service-areas/<city>/<service>/`), service page (`/cooling/`, `/plumbing/`…),
  utility page (financing, maintenance plans), or blog post.
- **Location focus** — which city + which neighborhoods get named. Petitt copy always
  names them.
- **Trade mix** — HVAC only, or HVAC + plumbing + IAQ? Petitt is all four
  (cooling, heating/gas logs, plumbing/water heaters, IAQ/crawl space).
- **What already exists** — is this a refresh of a live page, or new? A refresh keeps
  the live section order and only swaps what the brief changes.

## 2. State the design read (one line)

Say it out loud before building, e.g.:

> *Design read: service-area hub refresh for White House — mirror `4038` section order,
> pull the card-grid + FAQ patterns from `6619`, navy hero → soft-gray bands, red pill
> CTAs, no hover animation.*

## 3. Closest page to mirror

| Building… | Mirror | Why |
|---|---|---|
| service-area hub | `current-theme/content/page/4038.json` | the White House hub itself |
| service-area child | `current-theme/content/page/6619.json` | newest, cleanest patterns |
| service page | `4564.json` (cooling), `4668.json` (plumbing) | trade hubs |
| city page w/ cards + FAQ | `6619.json` | the "Card Component Grid" + accordion source |

`6619` is the most recent build in the kit — when in doubt, mirror it.

## 4. Route to the other skills

1. `petitt-content-style` — write/refresh the copy in the brand voice.
2. `petitt-ui-design` — palette, type scale, button spec, section rhythm, patterns.
3. `petitt-page-builder` — run the full build pipeline (this is usually what you want).
4. `petitt-page-audit` — the pre-delivery gate.
5. Repo-root `skills/full-output-enforcement` — completeness of the emitted JSON.

## 5. Ground rules that override instinct

- **Don't redesign the kit.** Match it. Petitt's look is navy + red, Oswald uppercase
  headings, pill buttons with a chevron icon.
- **The `primary` global (`#47A3DA`) is not the brand primary** — it is a thin accent
  border. Navy `#2B2E81` is.
- **Buttons never animate on hover** (color change only).
- If a brand-critical fact is missing (a link target, a phone number, a guarantee), ask
  **one** focused question rather than inventing it.
