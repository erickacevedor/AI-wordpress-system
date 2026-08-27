# Mid Lakes — project status

**As of 2026-08-27.** Where the HTML→Elementor port actually is. Companion to
`ENVIRONMENT.md` (how to reach the install, what is on it) and `PORT-DECISIONS.md`
(what has been settled, what is still open, and the Elementor behaviour verified on
this install).

Update this file when the answer to "where are we?" changes.

---

## One-paragraph summary

The prototype is finished and clean. The WordPress install exists, is reachable, and
has its **wire-up done** — seven page stubs, two menus, permalinks, front page and
posts page. **Nothing has been onboarded and no page has been built.** The next step
is onboarding: `tokens.json`, `KIT-ANALYSIS.md`, and the five `midlakes-*` skills.
**Nothing blocks the build** — the content and form questions were answered
2026-08-27 (see `PORT-DECISIONS.md`); only the production domain and the SEO plugin
are still open, and both are go-live wire-up.

---

## The two repos

| | |
|---|---|
| **Prototype** | `D:\laragon\www\midlakes` — remote `em-midlakes`. `public/` holds the design |
| **This repo** | `D:\laragon\www\AI-wordpress-system` — the pipeline and the deliverable |
| **Install** | `C:\Users\erick\Local Sites\mid-lakes` — a deployment target, not a source of truth |

The prototype repo is **level with `origin/main` at `f45edfc`** (pushed 2026-08-27),
working tree clean. Its last five commits are the ones this port is built on: the
About page build, the Maintenance→Service Agreements rename, the ductwork image crop,
the wave-decoration fix, and the cache stamps.

---

## The prototype, as measured

Run `python scripts/analyze-prototype.py D:/laragon/www/midlakes/public` to refresh.
Read-only without `--emit-tokens`.

| | |
|---|---|
| Pages | **7** `index.php` files with **zero** `<?php` tags |
| CSS | **1832 lines**, one file |
| Fonts | Manrope (400/500/600/700/800) + Fraunces (italic, `opsz` axis) |
| Container | `--container: 1200px` |
| Radius | `14px` |
| Bands | `white` · `paper` `#f4f6f9` · `ink` `#0f1f35` |
| Font sizes | **27 distinct** — plus two `clamp()` heads |
| Forms | **6** identical `quote-form`s, JS-only, no backend |
| Images | 5 webp, 2 logo SVG, 4 watermark SVG (`1/2/4/6.svg`) |
| Button | `#c10a0a` → hover `#a30808` + `translateY(-2px)`, radius `999px` |

> **These numbers drifted from the ones recorded in §11 of
> `docs/Elementor-Output-Anatomy.md`**, which were taken before the About page work:
> that block says 6 pages, 1698 CSS lines, 5 forms. It is stale, not wrong-in-kind.
> Its decision #7 (brand primary is red) **is** wrong — see `PORT-DECISIONS.md`.

---

## What exists

### In this repo

```
projects/midlakes/
├── STATUS.md            this file
├── ENVIRONMENT.md       install access, ports, the two traps, what is wired up
└── PORT-DECISIONS.md    settled decisions, the CSS cap, verified Elementor behaviour
```

Nothing else. **No `tokens.json`, no `KIT-ANALYSIS.md`, no `skills/`, no `pages/`.**

### On the install

Wire-up only — no page content anywhere. Full detail in `ENVIRONMENT.md`.

- Pages **10–16** (Home, About, Services, Service Agreements, Service Areas,
  Financing, Blog) — published, **empty**, slugs matching the prototype
- Home (10) is the front page; Blog (16) is the posts page
- **Main Menu** (3) → Header, **Footer Menu** (4) → Footer
- Permalinks `/%postname%/`; all seven URLs return 200
- Default Kit (6) **untouched** — Global Colors are still Hello Elementor defaults

---

## What does not exist yet

- Onboarding output: `tokens.json`, `KIT-ANALYSIS.md`, the five `midlakes-*` skills
- The `mid-lakes` **child theme** (decision 2) and its capped stylesheet
- The **SVG icon sprite** (decision 4)
- The **Elementor Pro Form template** (decision 1)
- Header / footer **Theme Builder templates** (`pages/_theme/`)
- **Any page.** Six real pages to build — blog is an archive, not a page
- **Media library is empty** (0 attachments). Images need uploading and a `media.json`
  attachment-id map, the way lenz does it

---

## Next steps, in order

1. ~~**Unblock.**~~ Done 2026-08-27 — see "Answered" in `PORT-DECISIONS.md`. Only the
   production domain and the SEO plugin remain, and neither blocks building.
2. **Onboard.** `python scripts/analyze-prototype.py D:/laragon/www/midlakes/public
   --emit-tokens projects/midlakes/tokens.json`, then hand-verify `_roles`
   (**primary is blue, CTA is red** — the script's inference is right, the old doc
   note is not), `links`, `phone`, `button`, `content_width` (1200).
3. **Write `KIT-ANALYSIS.md`**, folding in the §11 Mid Lakes block and deleting it
   from `docs/Elementor-Output-Anatomy.md` — with the primary-colour correction.
4. **Generate the five `midlakes-*` skills** per
   `skills/html-prototype-onboarding`. Put the two footguns from `PORT-DECISIONS.md`
   into `midlakes-page-builder`.
5. **Child theme + sprite + form template**, then header/footer.
6. **Build pages**, one folder each, validator exit 0 before every import.

---

## Standing rules for this site

- **Fidelity beats editability.** The client chose "exactly as it is" knowing capped
  properties stop responding to the Elementor editor.
- **Style inline, never at a global colour slot** — the kit is stock Hello.
- **One owner per property** — child theme *or* Elementor, never both. No `!important`.
- **`validate-page.py` exit 0 is not optional.**
- The install is a deployment target. Anything hand-edited there is lost on the next
  import and invisible to git.
