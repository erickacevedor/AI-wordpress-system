# Dolan — accessibility audit fixes

**Two files go to the site:**

1. `dolan-a11y-fixes.php` — paste everything below its header comment into
   `wp-content/themes/Divi-child/functions.php` (or drop the file into
   `wp-content/mu-plugins/`).
2. `page.php` — copy into `wp-content/themes/Divi-child/`. This is Divi's own
   `page.php` with one change: the `#main-content` wrapper is a real `<main>` element.
   The client asked for the semantic element, not just `role="main"`.

`preview-alt.php` is a dev tool, not deployed — see the last section.

## Answering the client point by point

> `<main>` landmark is missing, which is a semantic coding thing as well.

Fixed with a real `<main id="main-content">` element on every page type. Divi-templated
pages get it from the child `page.php`; Elementor Full Width pages get it from a
`the_content` wrapper, because that template bypasses `page.php` entirely.

> "Request Service" buttons don't have sufficient color contrast.

Fixed. The three orange buttons on Home were 3.26:1; they are now 4.90:1.

> The services images mid-page don't have alt text describing what is pictured.

Fixed. Those are the 10 photos in the Home page gallery. Four now use the client's own
Media Library wording, which Divi had been discarding; six were written by looking at
each photo. Every image on the site now has alt text.

> Some of the content isn't keyboard navigable, but it's not interactive content...

**Not a defect — their instinct was right.** Non-interactive content (headings,
paragraphs, images) is not supposed to be in the tab order, and screen readers read it
with a virtual cursor that is independent of tabbing. The gallery *is* keyboard
reachable: each photo is a real `<a>`. See "Worth raising with the client" below for two
genuine adjacent issues found while checking this.

## What it does

| # | Audit item | Fix |
|---|---|---|
| 1 | No `<main>` landmark | Adds `role="main"` to Divi's `<div id="main-content">` |
| 2 | "Request Service" buttons fail AA | Darkens the 3 orange Divi buttons on Home to `#C24A16` |
| 3 | Service images have no alt | Generates alt from the filename for any `<img>` missing it |
| 4 | Focus indicators suppressed | Restores a focus ring, including on Formidable form fields |

## What the backup proved

- **Item 2 is only 3 buttons, all on Home.** `#f16022` with white text = **3.26:1**.
  `#C24A16` is the same hue darkened until white clears AA at **4.90:1**. The other 16
  "Request Service" buttons are `#0c4096` / white = **9.59:1** and already pass.
- **The Elementor buttons are fine.** `post-233352.css` resolves them to
  `var(--e-global-color-accent)` = `#FEBE10`; black on gold is **9.54:1**. No change.
- **Item 4 is not the theme.** Divi's front-end `style.css` contains no `outline` rule
  at all. The suppression is **Formidable Forms** (`.with_frm_style … outline: none`),
  which is why the CSS targets those selectors explicitly.
- **Item 3 needs code.** Divi 4.27.6 only reads `_wp_attachment_image_alt` behind
  `if ( $src_value->is_dynamic() && $src_value->get_content() === 'post_featured_image' )`
  — dynamic featured images only. Every image on these pages is a static URL, so Divi
  renders `alt=""`. Setting alt in the Media Library alone would change nothing.
- **Item 1 needs two different wrappers.** Divi's page template gives
  `<div id="main-content">`, but Elementor Full Width pages don't render that wrapper at
  all — and, contrary to what its source suggested, this Elementor version emits no
  `<main>` either. `/cooling-services/` had *zero* landmarks until the code learned to
  fall back to Elementor's `<div data-elementor-type="wp-page">` root. Pages that
  already have a landmark are left alone.
- **The button rule must exclude Divi Theme Builder.** The header template puts 8
  buttons on every page (Employment Opportunities, Monthly Offer, Duke Energy Rebates,
  Financing Available). A plain `body.page-id-230601 .et_pb_button` turned all of them
  orange on Home only. The `:not([class*="_tb_"])` keeps the rule to the 3 real targets.

## The alt text is generic by design

Derived from the filename — no Media Library lookup, no database queries, no per-image
data entry. On this site the filenames are descriptive enough to read well:

```
Honeywell_logo_a7990cd700.webp   ->  Honeywell logo
trane-logo_94259ac5b2.webp       ->  Trane logo
Rheem_logo.svg_.png              ->  Rheem logo
aprilaire2.png                   ->  Aprilaire
```

The rule strips resize suffixes, `-scaled`, stacked extensions (CompressX writes
`photo.jpg.webp`), and hash or UUID fragments. Filenames that carry no meaning —
`IMG_0476`, `Pic01`, Facebook-style numeric names — fall through to `Dolan Design HVAC`
rather than shipping `alt="IMG"`.

Four filenames are codes rather than words, so they have a one-line override each:

| Filename | Alt |
|---|---|
| `gdmnlogo…` | Goodman Air Conditioning and Heating logo |
| `air-conditioner-2…` | Wall-mounted mini-split air handler |
| `better_air_better_life…` | Better Air Better Life 2025 free HVAC system giveaway |
| `DolanHVAC_RSMQuad…` | $99 fall maintenance special |

Those last two aren't what their filenames suggest — I opened them in the backup.
`air-conditioner-2` is a line-art mini-split icon, not a condenser photo, and
`DolanHVAC_RSMQuad_WLS1025_PROOF` is a $99 Fall Maintenance Special press ad.

**Worth being straight about:** generic alt satisfies the audit and is better than
`alt=""`, but it is not as good as a human describing the image. It says *what the file
is called*, not *what the picture shows*. For the six manufacturer logos that is exactly
right. For photographs it is adequate, not ideal. If the client ever wants real alt text,
type it into the image's Alt field in the Divi module — anything already set is left
untouched, so hand-written alt always wins.

## Checking the generated alt

```
php preview-alt.php          # the 9 images the audit flagged
php preview-alt.php --all    # every image in the Flywheel backup
```

`--all` scans 656 originals and lists only the ones that would produce weak alt.
Currently 46, all of which correctly fall back to the generic. Re-run it after adding an
override to confirm the result reads well.

## Verified on the local copy

Installed into `Divi-child/functions.php` on the Local site
(`dolandesignhvac-080426`, http://localhost:10016) and checked against the running site:

| Page | Template | Landmarks | Images | Missing alt |
|---|---|---|---|---|
| `/` (Home) | default | 1 | 25 | 0 |
| `/cooling-services/` | elementor_header_footer | 1 | 8 | 0 |
| `/plumbing/` | default | 1 | 11 | 0 |
| `/ac-repair/` | default | 1 | 10 | 0 |

Button rule confirmed against the rendered markup: the 8 `_tb_header` buttons are
skipped, and only `et_pb_promo_button`, `et_pb_button_0` and `et_pb_button_1` — the
three "Request Service" buttons — are restyled. No PHP notices or warnings in the
output, and nothing new in `logs/php/error.log`.

Original file backed up as `functions.php.bak-before-a11y` in the same folder.

## Still to check by eye

- The three Home buttons in the new orange (contrast is verified; appearance is not).
- Tab through the contact form for the focus ring — the Formidable fix is the one thing
  a markup check can't confirm.
- On production, install as an mu-plugin if a caching plugin is active, so the rewrite
  runs before the page is cached.

## Worth raising with the client

Found while checking the keyboard question. Neither is in the audit, both affect screen
reader users, and neither is fixed:

- **Gallery links announce a filename.** Each of the 10 gallery photos is wrapped in a
  link carrying `title="dolan_design_hvac-400x284_4c3a36a331"`. Screen readers may read
  that after the alt text. The fix is to clear the Title field on the Divi gallery
  module, or strip `title` from those links in code.
- **10 Font Awesome icons have no `aria-hidden="true"`.** They are decorative
  (`fa-heat`, `fa-snowflakes`, `fa-phone`) and should be hidden from assistive tech.
  Separately, `fa-heat` and `fa-snowflakes` are Font Awesome **Pro** icons and render
  blank on the Free set — worth checking they display at all.

## Loose ends, unrelated to the audit

- Page 233094's slug changed from `/plumbing-services-in-louisburg-nc/` to `/plumbing/`
  in the latest kit export — internal links to the old slug are stale.
- The 8 Font Awesome icons on Home use `fa-heat` and `fa-snowflakes`, which are FA
  **Pro** icons and render blank on the Free set. Two also have a stray quote:
  `style="color: #244ea2;""`.
