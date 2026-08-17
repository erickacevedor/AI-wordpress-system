# Lenz — Theme Builder parts · handoff

**Status:** header and footer built, imported, applied site-wide, verified on the
live render.

| | |
|---|---|
| Header | template #25 `lenz-header` — offer bar + v4 light cream nav |
| Footer | template #26 `lenz-footer` — 4-column, NAP + link lists + bottom bar |
| Condition | `include/general` (Entire Site) on both |

## Rebuild loop

```bash
python projects/lenz/pages/_theme/build-templates.py
python scripts/validate-page.py projects/lenz/pages/_theme/header.json   # exit 0
python scripts/validate-page.py projects/lenz/pages/_theme/footer.json
projects/lenz/deploy-plugin.sh
wp eval-file projects/lenz/tools/import-template.php \
   projects/lenz/pages/_theme/header.json lenz-header
```

Setting the display condition is the step that gets forgotten: without
`_elementor_conditions`, the template exists in the library, imports cleanly, and
never appears on the site. `import-template.php` sets it and regenerates the
conditions cache.

## The header's width budget — read this before adding a nav item

**The boxed container is 1140px at every viewport width.** A wider window gives the
bar no extra room, so nav crowding is *never* fixable with a media query. That cost
several wrong iterations before it was obvious.

Measured budget:

```
1140  content box
 −100  logo
 −110  Free Estimate CTA
 − 48  row gaps
 ≈692  available for seven menu items
```

Elementor's Mega Menu renders those seven items at **~860px** — it adds a wrapper
and a dropdown-icon button per item that the source's plain anchors don't have, so
the source design's "phone appears above 1240px" threshold does not transfer.

What made it fit:

| Lever | Where | Value |
|---|---|---|
| Item spacing | widget `menu_item_title_space_between` | 4px |
| Item padding | CSS `.e-n-menu-title-container` | 8px / 6px |
| Row gap | container `flex_gap` | 12px |
| CTA padding | button spec | 14px |
| **Phone number** | **removed from the bar** | — |

The phone was the one element genuinely duplicated elsewhere — it sits in the offer
bar directly above, and will be in the mobile menu. Dropping a nav *link* would have
changed the sitemap; this didn't. The markup is retained and hidden, so it can be
re-enabled if the item count ever drops.

**Adding an eighth nav item will overflow the bar.** Budget for it.

## Markup facts that cost a debug cycle each

1. **`.e-n-menu-title` is a DIV, not the link.** The interactive element is
   `.e-n-menu-title-container` inside it — an `<a class="… e-link">` for linked items,
   a plain `<div>` for a label-only item like Services. Styling the title as though
   it were the anchor puts padding and hover on the wrong box, and the Financing pill
   selector matches nothing.
2. **`aria-expanded` lives on the nested `.e-n-menu-dropdown-icon` button,** not on
   the title. Its `aria-controls` points at the `e-n-menu-content-*` panel. The a11y
   shim reads it from there, and returns focus to that button on Escape — which is
   correct anyway, since that button is what opened the panel.
3. **Widget-owned properties beat class selectors.** `menu_item_title_space_between`
   emits an element-scoped custom property; declaring `gap` in the stylesheet loses
   silently *and* makes the editor's spacing control appear broken. Whatever Elementor
   can express, let it — the stylesheet only takes what Elementor cannot.

## Financing gold pill

Targeted by `href`, not position:

```css
.lenz-nav__menu .e-n-menu-title-container[href*="#financing"] { … }
```

The widget exposes no per-item class, and `:nth-child` would silently move the pill
onto the wrong label the first time someone reorders the menu.

## Accessibility shim

`assets/js/lenz-header.js` layers back what the source implemented by hand and Pro's
widget does not provide: arrow keys walking the open panel, Home/End, Tab containment
inside the panel, and Escape returning focus to the trigger. It never opens or closes
anything itself — it only moves focus and lets the widget's own handling do the rest,
so if Elementor changes its markup the queries miss and the menu keeps working
unshimmed.

**Not yet verified with a real screen reader or keyboard pass** — that needs a human.

## Still open

- **Mobile menu.** Pro's Mega Menu has its own responsive collapse; it has not been
  styled to match the source's full-screen navy drawer, and the phone number needs to
  appear there.
- **Sticky behaviour** is CSS `position:sticky` plus an `is-stuck` shadow class. Not
  yet checked against the offer bar scrolling away above it.
- **Logo** is still the placeholder PNG; SVG lockups pending.
- `/privacy-policy/` and `/terms/` in the footer bottom bar are not real pages yet.
