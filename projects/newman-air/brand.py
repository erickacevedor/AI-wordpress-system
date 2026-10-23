#!/usr/bin/env python3
"""
Newman Air (V2.1): component vocabulary over scripts/elementor_builder.py.

Same approach as Lenz v6-1 (read projects/lenz/brand.py for the full why): the
approved prototype's stylesheet is ported almost verbatim into newman-core by
tools/port-css.py, so the Elementor tree here MIRRORS THE PROTOTYPE'S DOM AND
CLASS NAMES:

  - every prototype element that carries layout or skin becomes a container
    carrying the same classes;
  - text a person edits is native: heading, text-editor and button widgets;
  - markup Elementor cannot express (inline SVG, the hero badge, the ridges, the
    marquee, the FAQ <details>, the map) ships verbatim in html widgets.

Classes on heading and button widgets land on the widget wrapper; they are
recorded in widget-classes.json and port-css.py retargets those selectors at the
inner element. Text widgets carry their prototype markup (with its classes)
inside, so they need no manifest entry.

Every band is a full-width <section> whose one boxed container has the class
`nw-pass` (display: contents, see adapter.css): the gate gets its band structure
and the browser sees the prototype's `<section><div class="wrap">...` plus any
full-bleed siblings (ridges, slider track, marquee).
"""
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

PHONE = "(423) 753-7788"
PHONE_TEL = "tel:+14237537788"
EMAIL = "dispatch@newmanair.com"

# Plugin-hosted images (root-relative, so the build is not welded to one host).
IMG = "/wp-content/plugins/newman-core/assets/img/"
LOGO_HORIZ = IMG + "NewmanAirLogo_Horiz.svg"
LOGO_BEAR = IMG + "NewmanAirLogo_Bear.svg"
LOGO_STACKED = IMG + "NewmanAirLogo_Stacked.svg"

# Site map. The current site's slugs (callbestinshow.com page sitemap, 2026-10-23)
# as placeholders: the new slugs and redirect list were never shared.
L = {
    "home": "/", "contact": "/contact-us/", "about": "/about-us/", "financing": "/financing/",
    "maintenance-plan": "/maintenance-plan/", "blog": "/blog/", "service-area": "/service-area/",
    "privacy": "/privacy-policy/", "terms": "/terms-and-conditions/",
    "ac-installation": "/services/ac-installation/", "ac-repair": "/services/ac-repair/",
    "ac-maintenance": "/services/maintenance/", "heating-installation": "/services/heating-installation/",
    "heating-repair": "/services/heating-repair/", "heating-maintenance": "/services/maintenance/",
    "air-cleaners": "/services/air-cleaners/", "air-handlers": "/services/air-handlers/",
    "germicidal-lights": "/services/germicidal-lights/", "heat-pumps": "/services/heat-pumps/",
    "ductless": "/services/ductless/", "ductwork": "/services/ductwork/", "thermostats": "/services/thermostats/",
    "commercial": "/services/commercial/", "indoor-air-quality": "/services/indoor-air-quality/",
}

SERVICES = [
    ("Air Conditioning", "i-snow", [("AC Installation", "ac-installation"), ("AC Repair", "ac-repair"),
                                    ("AC Maintenance", "ac-maintenance")]),
    ("Heating", "i-flame", [("Heating Installation", "heating-installation"), ("Heating Repair", "heating-repair"),
                            ("Heating Maintenance", "heating-maintenance")]),
    ("Indoor Air Quality", "i-air", [("Air Cleaners", "air-cleaners"), ("Air Handlers", "air-handlers"),
                                     ("Germicidal Lights", "germicidal-lights")]),
    ("Additional Services", "i-plus", [("Heat Pumps", "heat-pumps"), ("Ductless Mini Splits", "ductless"),
                                       ("Ductwork", "ductwork"), ("Thermostats", "thermostats"),
                                       ("Commercial HVAC", "commercial")]),
]
# Manuel's sitetree: six city pages (Johnson City has a page on the current site
# but not in the sitetree's menu).
AREAS = [("Bristol", "bristol"), ("Elizabethton", "elizabethton"), ("Gray", "gray"),
         ("Greeneville", "greeneville"), ("Jonesborough", "jonesborough"), ("Kingsport", "kingsport")]


def area(slug):
    return "/service-area/%s/" % slug


_CONTAINER_TAGS = {"div", "header", "footer", "main", "article", "section", "aside", "nav", "a"}
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
    return {"url": url, "is_external": "on" if external else "", "nofollow": "", "custom_attributes": ""}


def _zero():
    return {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}


# ------------------------------------------------------------------ nodes ----
def box(classes, children, tag="div", link=None, el_id=None, d=None, style=None, **extra):
    """A container mirroring one prototype element. `d` is the prototype's
    reveal stagger (`style="--d:N"`); `style` any other inline custom property."""
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
    st = "; ".join(x for x in (("--d:%s" % d) if d is not None else "", style or "") if x)
    if st:
        s["_attributes"] = "style|%s" % st
    s.update(extra)
    return E.container(s, children, inner=True, classes=cls or None)


def section(classes, children, tag="section", el_id=None, label=None):
    """`<section class=...>` holding the prototype's children directly (the boxed
    container is `nw-pass`, display: contents)."""
    inner = E.container({
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": 1240, "sizes": []},
        "padding": _zero(), "padding_mobile": _zero(),
    }, children, classes="nw-pass")
    s = {"content_width": "full", "html_tag": tag}
    if el_id:
        s["_element_id"] = el_id
    if label:
        s["_attributes"] = "aria-label|%s" % label
    # Elementor's background lazy-load hides background images until its JS runs;
    # the prototype paints textures with background-image/mask. Opt out.
    return E.container(s, [inner], inner=False, classes=(classes + " e-no-lazyload").strip())


def heading(text, tag="h2", classes=None, size=None):
    """Native heading. `size` must equal the prototype's value (element settings
    outrank the stylesheet); emitted only where the gate needs it."""
    s = {"title": text, "header_size": tag}
    if size:
        for bp in ("", "_tablet", "_mobile"):
            s["typography_font_size" + bp] = {"unit": "custom", "size": size, "sizes": []}
        s["typography_typography"] = "custom"
    _register(classes, "heading")
    return E.widget("heading", s, classes=classes)


def text(markup, classes=None):
    """Native text-editor holding the prototype's inner HTML (with its classes)."""
    _register(classes, "text")
    return E.widget("text-editor", {"editor": markup}, classes=classes)


def button(label, url, classes, icon=None, icon_after=False, external=False):
    """Native button. Icons are CSS masks (`nw-ico-<name>`, overrides.css): button
    text goes through wp_kses_post, which strips inline SVG."""
    cls = classes
    if icon:
        cls += " nw-ico nw-ico-%s%s" % (icon, " nw-ico-after" if icon_after else "")
    _register(classes, "button")
    return E.widget("button", {"text": label, "link": _link(url, external)}, classes=cls)


def raw(markup, classes=None):
    """html widget: markup Elementor cannot express, verbatim from the prototype."""
    return E.widget("html", {"html": markup}, classes=classes)


# ------------------------------------------------------------- fragments ----
def svg(name, cls="icon", style=None):
    st = ' style="%s"' % style if style else ""
    return '<svg class="%s" aria-hidden="true"%s><use href="#%s"/></svg>' % (cls, st, name)


STAR = '<svg><use href="#i-star"/></svg>'
STARS = '<span class="stars" role="img" aria-label="5 out of 5 stars">%s</span>' % (STAR * 5)


def eyebrow(label, extra=""):
    """Eyebrow: always a <p>, never a heading (Alexis, homepage doc comment)."""
    cls = "eyebrow" + (" " + extra if extra else "")
    return raw('<p class="%s"><svg class="paw" aria-hidden="true"><use href="#i-paw"/></svg>%s</p>' % (cls, label))


def text_link(label, url, cls="text-link"):
    return raw('<a class="%s" href="%s">%s %s</a>' % (cls, url, label, svg("i-arrow")))


# ------------------------------------------------------------------ form ----
def _field(fid, ftype, label, width="100", required=True, **kw):
    f = {"_id": fid, "custom_id": fid, "field_type": ftype, "field_label": label,
         "required": "true" if required else "", "width": width, "placeholder": ""}
    f.update(kw)
    return f


def request_form():
    """Elementor Pro form in place of the prototype's static form. Fields are the
    current site's hero form (callbestinshow.com, read 2026-10-23): Name*, Email*,
    Phone*, City*, Message/Request(s). Recipient: dispatch@ (homepage doc) until the
    current form's routing is confirmed."""
    return E.widget("form", {
        "form_name": "Request service",
        "form_fields": [
            _field("name", "text", "Name", "50"), _field("phone", "tel", "Phone", "50"),
            _field("email", "email", "Email", "50"), _field("city", "text", "City", "50"),
            _field("message", "textarea", "Message/Request(s)", required=False, rows="2"),
        ],
        "show_labels": "yes",
        "mark_required": "yes",
        "button_text": "Schedule My Visit",
        "button_width": "100",
        "column_gap": {"unit": "px", "size": 12, "sizes": []},
        "row_gap": {"unit": "px", "size": 12, "sizes": []},
        "submit_actions": ["email"],
        "email_to": EMAIL,
        "email_subject": "New service request from newmanair.com",
        "email_content": "[all-fields]",
        "email_from_name": "Newman Air website",
        "custom_messages": "yes",
        "success_message": "Thanks! Your request was received. Our team will reach out to confirm your visit.",
        "required_field_message": "This field is required.",
        "invalid_message": "Please check the highlighted fields.",
    }, classes="nw-form")
