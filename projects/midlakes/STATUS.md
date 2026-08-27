# Mid Lakes — project status

**As of 2026-08-27.** Where the HTML→Elementor port actually is. Companion to
`ENVIRONMENT.md` (how to reach the install, what is on it) and `PORT-DECISIONS.md`
(what has been settled, what is still open, and the Elementor behaviour verified on
this install).

Update this file when the answer to "where are we?" changes.

---

## One-paragraph summary

**The site is built.** All six pages, the header, the footer, the child theme, the
icon sprite, the form and the media library — built from the prototype, gated at
`validate-page.py` exit 0, imported into the Local install, and verified against the
rendered HTML. All seven URLs return 200 and render with the right header, footer,
watermarks, alternations and fonts.

What remains is **go-live wire-up, not build work**: the blog archive template, the
production domain, and an SEO plugin for the seven hand-written `<title>` tags. Two
child-theme rules are shipped as *cap candidates* and want a yes/no.

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

> These numbers used to disagree with §11 of `docs/Elementor-Output-Anatomy.md`
> (6 pages, 1698 CSS lines, 5 forms — taken before the About page work), and with its
> decision #7, which claimed the brand primary was red. **That block is gone**; the
> current numbers live here and in `KIT-ANALYSIS.md` §13.

---

## What exists

### In this repo

```
projects/midlakes/
├── STATUS.md            this file
├── ENVIRONMENT.md       install access, ports, the three traps, what is on the site
├── PORT-DECISIONS.md    settled decisions, the CSS cap, verified Elementor behaviour
├── KIT-ANALYSIS.md      the design system, the component vocabulary, the port's answers
├── tokens.json          the seam — verified readable by site_tokens.py
├── media.json           the five photos → attachment ids 34–38
├── brand.py             THE VOCABULARY. Every component, once. ~1240 lines
├── build-all.sh         build + gate everything; --deploy to push and verify
├── deploy-theme.sh      repo → wp-content/themes/mid-lakes
├── wp.sh                WP-CLI with both Local traps handled
├── tools/
│   └── set-kit-defaults.php   Manrope base type, 1200 container, tablet_extra@1200
├── theme/mid-lakes/     the CHILD THEME — the capped stylesheet + the SVG assets
├── skills/              the five midlakes-* skills
└── pages/
    ├── _theme/{header,footer}/    Theme Builder parts (templates 49, 50)
    ├── home/  about-us/  services/
    ├── service-agreements/  service-area/  financing/
    └──   each: source.php · build.py · <slug>.json · HANDOFF-notes.md
```

### On the install

Full detail in `ENVIRONMENT.md`.

- Pages **10–15** hold the six built pages; **16 (Blog)** is the posts page and is
  still empty — it needs an archive template, not a page
- Theme **`mid-lakes`** active, deployed from this repo
- Templates **49** (header) and **50** (footer), both *Entire Site*
- Attachments **34–38** — the five photos, alt text set
- Default Kit (6): **typography set to Manrope**, container 1200,
  `tablet_extra` breakpoint at 1200. **Global Colors still stock** — colour stays
  inline, and that has not changed
- All seven URLs return 200

---

## What does not exist yet

- **The blog archive template.** Page 16 is the posts page; the prototype's
  `post-grid` is a loop, so it is a Theme Builder *archive*, not a page. Nothing
  else on the site depends on it
- **A production domain** and an **SEO plugin** — the seven hand-written
  locality-targeted `<title>` tags are parked in `tokens.json → pages.seo` and
  repeated in every `HANDOFF-notes.md`, but have nowhere to live yet
- **A decision on the two cap candidates** (below)
- **Real blog posts.** The archive will be empty until there are some

---

## Next steps, in order

1. ~~**Unblock.**~~ ~~**Onboard.**~~ ~~**`KIT-ANALYSIS.md`.**~~ ~~**The five
   skills.**~~ ~~**Child theme + sprite + form template.**~~ ~~**Header/footer.**~~
   ~~**Build the six pages.**~~ All done 2026-08-27.
2. **Answer the two cap candidates.** Both are shipped and both are one rule each,
   marked `[cap CANDIDATE]` in `mid-lakes.css`, removable without touching a single
   `build.py`:
   - `.ml-card:hover { transform: translateY(-4px) }` — the service/post card lift.
   - `.ml-hero::after` / `.ml-comfort::after` — the two **three-stop** photo
     overlays. Elementor's gradient control has two stops; the hero's middle stop is
     what lets the photo read through the top third. The native fallback is visibly
     flatter.
3. **The blog archive template** (`pages/_theme/archive/`), then some posts.
4. **Go-live wire-up.** Production domain → `wp elementor replace_urls
   http://localhost:10015 https://<domain>`; install an SEO plugin and load the seven
   titles/descriptions from `tokens.json → pages.seo`.
5. **Decide whether the watermarks are worth their cost.** They are **37% of the
   capped stylesheet** (49 of 134 declarations), plus seven SVG assets, plus the
   300px footer-padding trap. They are decoration — dropping them removes no
   information from any page. §11.4 of `docs/Elementor-Output-Anatomy.md` says to
   confirm a late-appended watermark block is wanted at all before paying to port it,
   and the prototype's block is exactly that shape. Ported under decision 3; worth
   re-confirming now the price is measurable.
6. **Raise the SEO string lengths with the client.** The prototype's own titles run to
   61–62 characters and its descriptions to 159–179; Google truncates around 60/155.
   They were kept **verbatim** because rewriting existing content is a client call.

## Standing rules for this site

- **Fidelity beats editability.** The client chose "exactly as it is" knowing capped
  properties stop responding to the Elementor editor.
- **Fonts come from the kit; colours are written into the page.** The kit's base
  typography is Manrope. `system_colors` is deliberately still stock Hello, so a
  global colour slot silently renders off-brand.
- **Build through `brand.py`**, never from an ad-hoc read of the prototype. Every
  component, every alternation and all three footguns are handled there once.
- **One owner per property** — child theme *or* Elementor, never both. No `!important`.
- **`validate-page.py` exit 0 is not optional.** Every current warning is one of
  two known things: the deliberate white-on-white band doubles, and the
  prototype's own over-length SEO strings. Anything else is a real finding.
- The install is a deployment target. Anything hand-edited there is lost on the next
  import and invisible to git.
