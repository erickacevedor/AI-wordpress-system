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
