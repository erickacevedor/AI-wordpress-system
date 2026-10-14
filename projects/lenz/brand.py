#!/usr/bin/env python3
"""
Lenz (v6-1): component vocabulary over scripts/elementor_builder.py.

THE APPROACH (decided 2026-10-13, see KIT-ANALYSIS.md "v6-1 port")
-----------------------------------------------------------------
The approved design is the static prototype v6-1 (erickacevedor/lenz @ 12259d2,
snapshot in design-source/v6-1/). Its stylesheet is ported almost verbatim into
lenz-core by tools/port-css.py, so the Elementor tree here MIRRORS THE PROTOTYPE'S
DOM AND CLASS NAMES instead of re-describing the design in Elementor settings:

  - every prototype element that carries layout or skin becomes a container (or a
    widget) carrying the SAME class names;
  - text a person edits is native: heading, text-editor, button, image widgets;
  - markup Elementor cannot express (inline SVG icons, the FAQ disclosure, the
    marquee, iframes) ships verbatim in small html widgets;
  - Elementor's own layout defaults are neutralised by the adapter block at the
    top of lenz-core.css, so the prototype CSS decides layout and look.

A class placed on a native widget lands on the widget WRAPPER, not on the <h2> or
<a> inside it. Every such class is recorded in a manifest (widget-classes.json next
to the page JSON); port-css.py reads it and re-targets those selectors at the inner
element (.elementor-heading-title, .elementor-button, img). That is the only
coupling between this file and the stylesheet.

Elementor containers cannot be <ul>, <li>, <figure> or <blockquote>. Where the
prototype uses those tags on a container, the container gets `lz-<tag>` and the
porter rewrites the element selector to `:is(<tag>, .lz-<tag>)`.
"""
import html as _html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_root(p):
    while p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, "AGENTS.md")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repo root (AGENTS.md) not found above %s" % HERE)


ROOT = _find_root(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E  # noqa: E402

TOKENS = json.load(open(os.path.join(HERE, "tokens.json"), encoding="utf-8"))
MEDIA = json.load(open(os.path.join(HERE, "media.json"), encoding="utf-8"))
for _m in MEDIA.values():   # root-relative, so a build is not welded to one host
    if "/wp-content/" in _m.get("url", ""):
        _m["url"] = "/wp-content/" + _m["url"].split("/wp-content/", 1)[1]

PHONE = "(515) 225-6446"
PHONE_TEL = "tel:+15152256446"
EMAIL = "Sierra@LenzHeatingandCooling.com"   # ClickUp 09/10 item 14

# Site map. Slugs come from the page copy docs (lenz-docs, 2026-10-13); the ones
# marked "planned" have no doc yet and are a proposal until the client confirms.
L = {
    "home": "/",
    "air-conditioning": "/air-conditioning/",
    "ac-installation": "/ac-installation/",
    "ac-repair": "/ac-repair/",
    "ac-maintenance": "/ac-maintenance/",
    "ac-replacement": "/ac-replacement/",
    "heating": "/heating/",
    "heating-installation": "/heating-installation/",
    "heating-repair": "/heating-repair/",
    "heating-maintenance": "/heating-maintenance/",
    "heating-replacement": "/heating-replacement/",          # planned
    "indoor-air-quality": "/indoor-air-quality/",
    "humidity-control": "/humidity-control/",
    "uv-light-purification": "/uv-light-purification/",
    "indoor-purification": "/air-purification/",              # doc: "Air Purification"
    "duct-cleaning": "/duct-cleaning/",                      # planned
    "additional-services": "/additional-services/",          # planned
    "thermostat-services": "/thermostat-services/",          # planned
    "water-heater-services": "/water-heater-services/",      # planned
    "ductwork": "/ductwork/",                                # planned
    "gas-lines": "/gas-lines/",                              # planned
    "heat-pumps": "/heat-pumps/",                            # planned
    "maintenance-plans": "/maintenance-plan/",
    "specials": "/specials/",
    "financing": "/financing/",
    "service-areas": "/service-areas/",
    "about": "/about-us/",
    "contact": "/contact/",
    "privacy": "/privacy-policy/",                           # planned
    "terms": "/terms/",                                      # planned
    "form": "#contact",            # ClickUp 09/10 item 13: CTAs anchor to the form
    "reviews": "https://www.google.com/maps/search/?api=1&query=Lenz+Heating+and+Cooling+Urbandale+IA",
    "who13-video": "https://www.youtube-nocookie.com/embed/8jsNz6yxry0",
}

# Mega menu, mobile menu, footer and the home services block all read this, so
# adding a service is one edit here.
SERVICES = [
    ("Air Conditioning", "air-conditioning", [
        ("AC Installation", "ac-installation"), ("AC Repair", "ac-repair"),
        ("AC Maintenance", "ac-maintenance"), ("AC Replacement", "ac-replacement")]),
    ("Heating", "heating", [
        ("Heating Installation", "heating-installation"), ("Heating Repair", "heating-repair"),
        ("Heating Maintenance", "heating-maintenance"), ("Heating Replacement", "heating-replacement")]),
    ("Indoor Air Quality", "indoor-air-quality", [
        ("Humidity Control", "humidity-control"), ("UV Light Purification", "uv-light-purification"),
        ("Indoor Purification", "indoor-purification"), ("Duct Cleaning", "duct-cleaning")]),
    ("Additional Services", "additional-services", [
        ("Thermostat Services", "thermostat-services"), ("Water Heater Services", "water-heater-services"),
        ("Ductwork", "ductwork"), ("Gas Lines", "gas-lines"), ("Heat Pumps", "heat-pumps")]),
]

NAV = [("Maintenance Plans", "maintenance-plans"), ("Specials", "specials"),
       ("Financing", "financing"), ("Service Areas", "service-areas"),
       ("About Us", "about"), ("Contact Us", "contact")]

# Tags a container can render as (Elementor's html_tag control). Anything else
# falls back to <div> plus an `lz-<tag>` class the porter knows about.
_CONTAINER_TAGS = {"div", "header", "footer", "main", "article", "section", "aside", "nav", "a"}
LZ_TAGS = ("ul", "li", "figure", "figcaption", "blockquote", "span", "p")

# class -> widget kind, collected while building; written next to each page JSON.
_MANIFEST = {}


def _register(classes, kind):
    for c in (classes or "").split():
        prev = _MANIFEST.get(c)
        if prev and prev != kind:
            raise ValueError("class %r used on both %s and %s widgets" % (c, prev, kind))
        _MANIFEST[c] = kind


def reset(seed):
    E.reset_ids(seed)
    _MANIFEST.clear()


def write_manifest(path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(_MANIFEST.items())), f, indent=2)
        f.write("\n")


def _link(url, external=False):
    return {"url": url, "is_external": "on" if external else "", "nofollow": "",
            "custom_attributes": ""}


def _zero():
    return {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}


# ------------------------------------------------------------------ nodes ----
def box(classes, children, tag="div", link=None, el_id=None, inner=True, **extra):
    """A container mirroring one prototype element. No gap, no padding, no layout:
    the stylesheet owns all of that (adapter + ported CSS)."""
    cls = classes or ""
    s = {"content_width": "full"}
    if tag in _CONTAINER_TAGS:
        if tag != "div":
            s["html_tag"] = tag
    else:
        cls = (cls + " lz-" + tag).strip()
    if tag == "a" and link:
        s["link"] = _link(link)
    if el_id:
        s["_element_id"] = el_id
    s.update(extra)
    return E.container(s, children, inner=inner, classes=cls or None)


def section(classes, children, box_classes="container", tag="section", el_id=None, label=None):
    """Prototype `<section class=...><div class="container">...` as the gate's
    full-width band -> ONE boxed container pair. The boxed container's inner
    wrapper is display:contents (adapter), so it behaves like the prototype's
    `.container` exactly."""
    inner = E.container({
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": 1140, "sizes": []},
        "padding": _zero(), "padding_mobile": _zero(),
    }, children, classes=box_classes)
    s = {"content_width": "full", "html_tag": tag}
    if el_id:
        s["_element_id"] = el_id
    if label:
        s["_attributes"] = "aria-label|%s" % label
    # Elementor's background lazy-load hides every background-image inside a band
    # with `!important` until its JS marks the band; the prototype paints its
    # waves and the plan badge with background-image. Opt each band out.
    return E.container(s, [inner], inner=False, classes=(classes + " e-no-lazyload").strip())


def heading(text, tag="h2", classes=None, size=None):
    """Native heading. `size` (a CSS length, may be clamp()) is emitted for every
    breakpoint only where the gate needs it (h1/h2) and must equal the
    prototype's value, because element settings outrank the stylesheet."""
    s = {"title": text, "header_size": tag}
    if size:
        for bp in ("", "_tablet", "_mobile"):
            s["typography_font_size" + bp] = {"unit": "custom", "size": size, "sizes": []}
        s["typography_typography"] = "custom"
    _register(classes, "heading")
    return E.widget("heading", s, classes=classes)


def text(markup, classes=None):
    """Native text-editor. Pass the inner HTML exactly as the prototype has it,
    including the <p> when the prototype's selector targets `p`."""
    _register(classes, "text")
    return E.widget("text-editor", {"editor": markup}, classes=classes)


def button(label, url, classes, icon=None, external=False):
    """Native button. `classes` are the prototype's (`btn btn-gold`). An icon is a
    CSS mask (`lz-ico-<name>`), because the button text runs through wp_kses_post,
    which strips inline SVG."""
    cls = classes + (" lz-ico lz-ico-%s" % icon if icon else "")
    _register(classes, "button")
    return E.widget("button", {"text": label, "link": _link(url, external)},
                    classes=cls)


def image(key, alt, classes=None, lazy=True):
    m = MEDIA[key]
    _register(classes, "image")
    s = {"image": {"url": m["url"], "id": m["id"], "size": "", "alt": alt, "source": "library"},
         "image_size": "full"}
    return E.widget("image", s, classes=classes)


def raw(markup, classes=None):
    """html widget: markup Elementor cannot express, verbatim from the prototype."""
    return E.widget("html", {"html": markup}, classes=classes)


# ------------------------------------------------------------- fragments ----
def svg(name, cls=None, style=None):
    c = ' class="%s"' % cls if cls else ""
    st = ' style="%s"' % style if style else ""
    return '<svg%s aria-hidden="true"%s><use href="#%s"/></svg>' % (c, st, name)


STAR = ('<svg viewBox="0 0 24 24" aria-hidden="true" style="fill:var(--color-star);'
        'stroke:var(--color-star-edge);stroke-width:1"><use href="#i-star"/></svg>')
STARS = '<span class="stars" role="img" aria-label="5 out of 5 stars">%s</span>' % (STAR * 5)


def eyebrow(icon, label, extra=""):
    cls = "eyebrow" + (" " + extra if extra else "")
    return raw('<span class="%s">%s %s</span>' % (cls, svg(icon, "icon-xs"), label))


def esc(s):
    return _html.escape(s, quote=False)


# ============================================================ components ====
# Shared by the home and every service page. Each one builds its widgets in a
# fixed order, so a page that uses them rebuilds to identical JSON.

def head(icon, label, title, lead=None, extra="", lead_cls="section__lead"):
    """`.section__head`: eyebrow, h2.section__title, optional p.section__lead."""
    kids = [eyebrow(icon, label), heading(title, "h2", "section__title", size="var(--text-2xl)")]
    if lead:
        kids.append(text(lead, lead_cls))
    return box(("section__head " + extra).strip(), kids)


def arrow_link(cls, label, href, icon="i-arrow", icon_cls="icon-sm", attrs=""):
    return raw('<a class="%s" href="%s"%s>%s %s</a>' % (cls, href, attrs, label, svg(icon, icon_cls)))


def service_card(cat, icon, name, blurb, key):
    return box("service-card", [
        raw('<span class="service-card__icon" data-cat="%s">%s</span>' % (cat, svg(icon, "icon-sm"))),
        box("", [heading(name, "h4"), text("<p>%s</p>" % blurb)], tag="span"),
    ], tag="a", link=L[key])


# Hardcoded fallback quotes, as the prototype ships them until a Places proxy
# exists. No aggregateRating anywhere until verified Google data exists.
REVIEWS = [
    ("LENZ did a phenomenal job on my evaporator coil replacement. I&apos;ve never seen techs work so "
     "hard on a relatively small job — and they came back the next day to make sure it was done right. "
     "Great follow-through and price, and a commitment to honest work. LENZ has my business for life now.",
     "Curtis Taylor"),
    ("Puia was great. Great attitude and service. As always, I appreciate the work you all do and happy "
     "to be a customer.", "Dave Olsen"),
    ("Your service man did a great job, very courteous young man. Lenz is the best and we appreciate "
     "all you do for us.", "Ron &amp; Janet Hester"),
]


def review(cls, quote, name):
    return box(cls, [raw(STARS), text("<blockquote>%s</blockquote>" % quote),
                     text("— " + name, "review-name")], tag="figure")


def reviews_grid():
    return box("reviews__grid", [
        review("review-feature", *REVIEWS[0]),
        box("review-side", [review("review-card", *REVIEWS[1]), review("review-card", *REVIEWS[2])]),
    ])


def faq_list(items):
    """The prototype's FAQ disclosure (lenz-site.js drives it), verbatim markup."""
    return raw('<div class="faq-list">' + "".join(
        '<div class="faq"><h3 style="margin:0"><button class="faq__trigger" aria-expanded="false" '
        'aria-controls="faq-%d" id="faq-%d-t">%s %s</button></h3><div class="faq__panel" id="faq-%d" '
        'role="region" aria-labelledby="faq-%d-t"><p>%s</p></div></div>'
        % (i, i, q, svg("i-plus", "faq__icon icon-sm"), i, i, a)
        for i, (q, a) in enumerate(items, 1)) + "</div>")


FORM_SERVICES = ["Air Conditioning", "AC Installation", "AC Repair", "AC Replacement", "Furnace & Heating",
                 "Heat Pumps", "Ductwork", "Duct Cleaning", "Indoor Air Quality", "Water Heater Installation",
                 "Maintenance"]


def _field(fid, ftype, label, **kw):
    f = {"_id": fid, "custom_id": fid, "field_type": ftype, "field_label": label, "required": "true",
         "width": "100", "placeholder": ""}
    f.update(kw)
    return f


def estimate_form(button_text="Schedule Your Service Online", preselect=None):
    """Elementor Pro form in place of the prototype's static form, so a request
    goes somewhere. Recipient = the contact email ClickUp settled on (09/10 item
    14); confirm before launch. Local routes mail to Mailpit."""
    service = _field("service", "select", "Service",
                     field_options="Choose a service…|\n" + "\n".join(FORM_SERVICES))
    if preselect:
        service["field_value"] = preselect
    return E.widget("form", {
        "form_name": "Estimate request",
        "form_fields": [_field("name", "text", "Name"), _field("phone", "tel", "Phone"), service],
        "show_labels": "yes",
        "mark_required": "yes",
        "button_text": button_text,
        "button_width": "100",
        # Element CSS for the submit colour outranks any stylesheet, so the
        # prototype's .btn-gold values are set here (the stylesheet has the rest).
        "button_text_color": "#121212",
        "button_hover_color": "#121212",
        "button_background_color": "#FFC600",
        "button_background_hover_color": "#FFCF29",
        "field_background_color": "#FFFFFF",
        "column_gap": {"unit": "px", "size": 0, "sizes": []},
        "row_gap": {"unit": "px", "size": 20, "sizes": []},
        "submit_actions": ["email"],
        "email_to": EMAIL,
        "email_subject": "New estimate request from the website",
        "email_content": "[all-fields]",
        "email_from_name": "Lenz website",
        "success_message": "Thanks — your request was received. We'll call you back within 2 hours during "
                           "business hours. Need help now? Call (515) 225-6446.",
        "required_field_message": "This field is required.",
        "invalid_message": "Please check the highlighted fields.",
    }, classes="lz-form")


def close_form(title, lead_html, button_text="Schedule Your Service Online", preselect=None, extra=""):
    """The navy closing band with the estimate form (`#contact`)."""
    form = estimate_form(button_text, preselect)
    return section(("close-form section " + extra).strip(), [
        box("close-form__inner", [
            box("", [
                heading(title, "h2", size="var(--text-2xl)"),
                text(lead_html, "close-form__lead"),
                raw('<div class="close-form__alt"><a class="phone-link" href="%s">%s%s</a><small>Open 24 hours · '
                    'Serving the Des Moines metro</small></div>' % (PHONE_TEL, svg("i-phone", "icon-sm"), PHONE)),
            ]),
            box("form-card", [
                form,
                raw('<p class="form-note">We&apos;ll call you back within 2 hours during business hours.</p>'
                    '<div class="form-status" role="status" aria-live="polite"></div>'),
            ]),
        ]),
    ], el_id="contact")


def cta_band(title, sub, extra=""):
    """The navy emergency band with the van photo behind it."""
    return section(("cta-band section--tight " + extra).strip(), [
        raw('<img class="cta-band__bg" src="%s" alt="" aria-hidden="true" decoding="async" loading="lazy" />'
            % MEDIA["lenz-service-van-wrap-webp"]["url"]),
        box("cta-band__inner", [
            heading(title, "h2", size="var(--text-2xl)"),
            text("<p>%s</p>" % sub),
            button("Call " + PHONE, PHONE_TEL, "btn btn-gold", icon="phone"),
        ]),
    ])


def trustbar(items, extra=""):
    return section(("trustbar " + extra).strip(), [
        box("trustbar__grid", [
            box("trustbar__item", [text(v, "trustbar__value"), text(l, "trustbar__label")]) for v, l in items
        ]),
    ], label="At a glance")
