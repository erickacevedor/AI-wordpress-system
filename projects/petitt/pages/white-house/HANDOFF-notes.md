# HANDOFF — Reliable HVAC & Plumbing Services in White House, TN

**File to import:** `projects/petitt/pages/white-house/white-house.json`
**Target page:** <https://petittheatingandcooling.com/service-areas/white-house/> (kit id `4038`)
**Source:** `source.docx` — "Petitt White House Main Page (7/10)"
**Gate:** `python3 scripts/validate-page.py projects/petitt/pages/white-house/white-house.json` → **PASS**

---

## 1. Import

1. WordPress → **Elementor → Templates → Import Templates** (up-arrow icon) → select
   `white-house.json` → **Import Now**.
2. Open the existing **White House** page (`/service-areas/white-house/`) in Elementor.
3. In the editor: **⌄ (folder icon) → My Templates → "Reliable HVAC & Plumbing Services in
   White House, TN" → Insert** (choose *Do NOT apply* page settings so the page keeps its
   current template/header/footer).
4. Delete the old sections once the new ones are in place, then **Update**.

Keeping the same page (rather than publishing a new one) preserves the URL, rankings and
internal links — which is what we agreed.

## 2. SEO (Elementor JSON can't carry WP meta — set these by hand)

| Field | Value |
|---|---|
| Slug | `white-house` — **unchanged**, under `/service-areas/` |
| SEO title | `HVAC & Plumbing Services in White House, TN \| Petitt` (52 chars) |
| Meta description | `Trust White House's local experts for 24/7 HVAC, plumbing, and air quality. Backed by a 10-year warranty and the Petitt Promise. Schedule service today!` (151) |
| H1 | Reliable HVAC & Plumbing Services in White House, TN (one only ✓) |

> The doc listed the URL as `petitt-hvac.com/service-area/white-house-tn`. That does not
> match the live site; per your call we kept the live URL. The SEO title in the doc was
> 71 chars — trimmed above to fit under 60. The meta description is the doc's, minus the
> word "your" so it lands under 155.

## 3. What changed vs. the live page

| # | Section | Change |
|---|---|---|
| 1 | Hero | New H1 (**& Plumbing** added), refreshed copy, **two CTAs**: `Call Now` (red, `tel:`) + `Book Online` (outlined, request-an-appointment). Rating badge + city photo kept. |
| 2 | **Trust bar** | **NEW** — ⭐ 5-Star Rated Service · 🛡️ Licensed & Insured · 🏠 Serving White House Since 2010, on a deep-navy strip directly under the hero *(client note #1)*. |
| 3 | Service overview | **Rebuilt as a Card Component Grid** (2×2, 3 breakpoints) with **H3 service titles**, brand service icons, bullet lists and a CTA per card *(client note #2)*. Replaces the old 4-item H4 text grid. |
| 4 | Maintenance plan | Copy refreshed; bullets and $12/month unchanged. |
| 5 | Financing | Retitled "Manageable payments for White House families" + new copy; now a two-column layout with a summary card. |
| 6 | Why neighbors trust | Copy as-is (already matched the doc); team photo kept. |
| 7 | Map | **Carried over unchanged** (Google Maps iframe, `html` widget). |
| 8 | **FAQ** | **NEW** — 4 Q&As in the kit's nested accordion (980px), same styling as the White House cooling page. |
| 9 | Closing CTA | Retitled "Ready to restore your home's comfort?…" + new copy; phone + schedule buttons kept. |
| 10 | Chamber badge | **Carried over unchanged.** |

Only the two italic "(Note: …)" instructions in the doc were treated as formatting
requests — no highlighting survived the `.docx` export (verified in the file's XML).

## 4. Link targets used

| Button | URL |
|---|---|
| Call Now / 615-654-0814 | `tel:+16156540814` |
| Book Online | `/contact-us/request-an-appointment/` |
| Schedule Service (×2) | `/expert-hvac-services-in-sumner-county-schedule-today/` |
| Explore White House **Cooling** Services | `/service-areas/white-house/cooling/` |
| Explore White House **Heating** Services | `/heating/` |
| Explore White House **Plumbing** Services | `/plumbing/` |
| Explore White House **IAQ** Services | `/indoor-air-quality/` |
| Sign Up for Our Maintenance Plan | `/maintenance-plans/` |
| Explore Financing Options | `/financing/` |

⚠️ **Worth a look:** only *cooling* has a White-House-specific child page today. The
heating / plumbing / IAQ buttons keep the client's "White House" wording but point at the
Middle-TN hubs (as agreed). If White House child pages get built later, swap those three
URLs in `build.py` (`T["links"]`) and rebuild.

Also note `/financing/` is the current permalink for the financing page (the live White
House page still links to the older `/flexible-hvac-financing/`).

## 5. Post-import checks

- [ ] Hero video: the current page has a background `.mov` on the hero — **not** carried
      over. Re-add in Elementor if you want to keep it.
- [ ] Images resolve (all reuse existing media IDs — nothing to re-upload).
- [ ] The reviews/rating widget renders (it's the native Elementor `rating` widget).
- [ ] Google Map loads.
- [ ] Mobile: card grid → 1 column, trust bar stacks, hero image 250px, H1 2.4em.
- [ ] Buttons: red `#D90000`, pill, chevron, **no** hover animation; navy phone button.

## 6. Rebuilding

```bash
python3 projects/petitt/pages/white-house/build.py
python3 scripts/validate-page.py projects/petitt/pages/white-house/white-house.json
```

Edit copy/links in `build.py` (brand values come from `projects/petitt/tokens.json`) —
never hand-edit `white-house.json`.
