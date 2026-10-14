#!/usr/bin/env python3
"""
Lenz: the service page template (child service pages: AC Repair, AC Installation,
Heating Repair, ...).

Approved design: design-source/v6-1/ac-repair.html + css/lenz-service.css
(Erick, 2026-10-13). This module mirrors that DOM, the same way brand.py mirrors
the home. A page's build.py supplies only a PAGE dict (copy, links, photos) and
calls build(PAGE); every service page is a content swap.

Section order: hero, trustbar, intro (copy + checklist), problems grid, emergency
band, why it matters (photo + numbered list), why Lenz, reviews, FAQs, related
services, closing form.

Category tint: PAGE["cat"] is cool | warm | air | extra. Every band carries
`svc-page svc-page--<cat>`, which sets the --cat colours lenz-service.css uses.
"""
import json
import os

import brand as B
from brand import L, svg, eyebrow


def _crumbs(page):
    hub_label, hub_key = page["hub"]
    return B.raw(
        '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
        '<li><a href="%s">%s</a></li><li aria-current="page">%s</li></ol></nav>'
        % (L[hub_key], hub_label, page["title"]))


def build(page):
    """Return the list of sections for one service page."""
    cat = "svc-page svc-page--" + page["cat"]
    S = []

    # ---------------------------------------------------------------- hero ----
    h1 = '%s<span class="accent">%s</span>%s' % page["h1"]
    badge_title, badge_text = page["badge"]
    img_key, img_alt = page["hero_image"]
    S.append(B.section("hero hero--service " + cat, [
        B.box("hero__copy", [
            _crumbs(page),
            B.raw('<span class="hero__eyebrow">%s %s</span>' % (svg(page["cat_icon"], "icon-xs"),
                                                               page["cat_label"])),
            B.heading(h1, "h1", size="var(--text-hero)"),
            B.text(page["lead"], "hero__sub"),
            B.raw('<p class="hero__areas">%s%s</p>' % (svg("i-pin", "icon-sm"), page["areas"])),
            B.box("hero__cta", [
                B.button(page["cta"], L["form"], "btn btn-gold"),
                B.button("Call " + B.PHONE, B.PHONE_TEL, "btn btn-outline-light", icon="phone"),
            ]),
        ]),
        B.box("hero__media", [
            B.image(img_key, img_alt),
            B.raw('<div class="hero__badge"><span class="hero__badge-icon">%s</span><span><b>%s</b>%s</span></div>'
                  % (svg("i-clock", "icon"), badge_title, badge_text)),
        ]),
    ], box_classes="container hero__inner"))

    # ------------------------------------------------------------ trustbar ----
    S.append(B.trustbar(page["trust"], extra=cat))

    # --------------------------------------------------------------- intro ----
    it = page["intro"]
    S.append(B.section("section section--mist svc-intro " + cat, [
        B.box("svc-intro__layout", [
            B.box("svc-intro__copy", [
                eyebrow(*it["eyebrow"]),
                B.heading(it["title"], "h2", "section__title", size="var(--text-2xl)"),
                B.text(it["lead"], "section__lead"),
                B.text("".join("<p>%s</p>" % p for p in it["body"]), "svc-intro__body"),
            ]),
            B.box("checklist-card", [
                B.text(it["checklist_title"], "checklist-card__title"),
                B.raw('<ul class="checklist">%s</ul>' % "".join(
                    "<li>%s%s</li>" % (svg("i-check", "icon-sm"), li) for li in it["checklist"])),
                B.button(page["cta"], L["form"], "btn btn-primary"),
            ], tag="aside"),
        ]),
    ]))

    # ------------------------------------------------------------ problems ----
    pr = page["problems"]
    cards = [B.box("symptom", [
        B.raw('<span class="symptom__icon">%s</span>' % svg(icon, "icon")),
        B.heading(title, "h3"),
        B.text("".join("<p>%s</p>" % p for p in paras)),
    ], tag="article") for icon, title, paras in pr["items"]]
    help_title, help_text = pr["help"]
    cards.append(B.box("service-help symptom-help", [
        B.box("service-help__txt", [B.heading(help_title, "h4"), B.text("<p>%s</p>" % help_text)]),
        B.raw('<a class="phone-link" href="%s">%s %s</a>' % (B.PHONE_TEL, B.PHONE, svg("i-arrow", "icon-sm"))),
    ]))
    S.append(B.section("section symptoms " + cat, [
        B.head(*pr["eyebrow"], pr["title"], pr["lead"]),
        B.box("symptom-grid", cards),
    ], el_id="problems"))

    # ------------------------------------------------------------ CTA band ----
    S.append(B.cta_band(*page["band"], extra=cat))

    # ----------------------------------------------------- why it matters ----
    va = page["values"]
    v_key, v_alt = va["image"]
    S.append(B.section("valueprops section " + cat, [
        B.head(*va["eyebrow"], va["title"], va["lead"]),
        B.box("valueprops__layout", [
            B.box("valueprops__media", [B.image(v_key, v_alt)], tag="figure"),
            B.box("valueprops__grid", [
                B.box("vprop", [
                    B.text("%02d" % n, "vprop__num"),
                    B.box("vprop__text", [B.heading(t, "h3"), B.text("<p>%s</p>" % d)]),
                ]) for n, (t, d) in enumerate(va["items"], 1)
            ]),
        ]),
    ]))

    # ------------------------------------------------------------ why Lenz ----
    wy = page["why"]
    S.append(B.section("creds section " + cat, [
        B.head(*wy["eyebrow"], wy["title"], wy["lead"]),
        B.box("creds__grid", [
            B.box("creds__card", [
                B.raw('<span class="creds__icon">%s</span>' % svg(icon, "icon")),
                B.heading(title, "h3"),
                B.text(body, "creds__text"),
            ], tag="article") for icon, title, body in wy["items"]
        ]),
    ]))

    # ------------------------------------------------------------- reviews ----
    rv = page["reviews"]
    S.append(B.section("reviews section " + cat, [
        B.head("i-star", "Reviews", rv["title"], rv["lead"]),
        B.reviews_grid(),
        B.raw('<p class="reviews__micro"><a href="%s">Ready for service like this? %s %s</a></p>'
              % (L["form"], page["cta"], svg("i-arrow", "icon-sm"))),
    ], el_id="reviews"))

    # ---------------------------------------------------------------- FAQs ----
    S.append(B.section("faqs section " + cat, [
        B.head("i-info", "FAQs", page["faq_title"], extra="section__head--center"),
        B.faq_list(page["faqs"]),
    ], el_id="faqs"))

    # ------------------------------------------------------------- related ----
    rl = page["related"]
    go_label, go_key = rl["go"]
    S.append(B.section("section section--mist related " + cat, [
        B.box("svc-band svc-band--" + page["cat"], [
            B.box("svc-band__head", [
                B.raw('<span class="svc-band__icon">%s</span>' % svg(page["cat_icon"])),
                B.box("svc-band__txt", [B.heading(rl["title"], "h3"), B.text("<p>%s</p>" % rl["text"])]),
                B.arrow_link("svc-band__go", go_label, L[go_key]),
            ]),
            B.box("svc-band__grid", [B.service_card(*c) for c in rl["cards"]]),
        ], tag="section"),
    ]))

    # --------------------------------------------------------- close form ----
    cl = page["close"]
    S.append(B.close_form(cl["title"], "".join("<p>%s</p>" % p for p in cl["paras"]),
                          button_text=page["cta"], preselect=page.get("form_preselect"), extra=cat))
    return S


def write(page, here):
    """Build, write <slug>.json and the class manifest next to the page's build.py."""
    S = build(page)
    doc = B.E.wrap_page(page["title"], S, {"template": "elementor_header_footer", "hide_title": "yes"})
    out = os.path.join(here, page["slug"] + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    B.write_manifest(os.path.join(here, "widget-classes.json"))
    print("wrote %s (%d sections)" % (out, len(S)))
