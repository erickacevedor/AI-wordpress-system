#!/usr/bin/env python3
"""
HVIA (option 2): component vocabulary over scripts/elementor_builder.py.

Same approach as projects/lenz/brand.py (approved for Lenz v6-1, 2026-10-13):
the prototype stylesheet is ported almost verbatim into hvia-core by
tools/port-css.py, so the Elementor tree MIRRORS THE PROTOTYPE'S DOM AND CLASS
NAMES instead of re-describing the design in Elementor settings:

  - every prototype element that carries layout or skin becomes a container (or a
    widget) carrying the SAME class names;
  - text a person edits is native: heading and button widgets, plus image widgets;
  - markup Elementor cannot express (inline SVG, <address>/<dl>, the nav) ships
    verbatim in small html widgets;
  - Elementor's own layout defaults are neutralised by the adapter block at the top
    of hvia-core.css (copied from lenz-core).

A class placed on a native widget lands on the widget WRAPPER. Every such class is
recorded in widget-classes.json next to the page JSON; port-css.py re-targets those
selectors at the inner element. Short styled lines (eyebrows, names, roles) are
heading widgets with a p/span/div tag rather than text-editor widgets, so the class
reaches the element that the prototype styled.

Section shape (the gate wants one full-width band holding exactly one boxed
container): band = the prototype <section> (its classes, id, tag) > a neutral boxed
container at 100% (its inner wrapper is display:contents, adapter) > the
prototype's `.wrap ...` element as a plain container. That keeps every prototype
child combinator (`.hero-grid > *`) pointing at the right element.

Containers cannot be <ul>, <li>, <figure> or <span>: those get `lz-<tag>` and the
porter rewrites the element selector to `:is(<tag>, .lz-<tag>)`.

Scroll-reveal delays are inline `style="--d:..."` in the prototype; here they are
classes (`d-100`), defined in overrides.css, because the delay must reach widgets too.
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

MEDIA = json.load(open(os.path.join(HERE, "media.json"), encoding="utf-8"))
for _m in MEDIA.values():   # root-relative, so a build is not welded to one host
    if "/wp-content/" in _m.get("url", ""):
        _m["url"] = "/wp-content/" + _m["url"].split("/wp-content/", 1)[1]

# Contact details: ClickUp 86bcc5579. Phone is the AVS number "for the moment"
# (Nicolas, 2026-10-12); address from the client (2026-10-08).
PHONE = "(334) 801-9952"
PHONE_TEL = "tel:+13348019952"
ADDRESS_1 = "4791 Woodmere Blvd"
ADDRESS_2 = "Montgomery, AL 36106"
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=4791+Woodmere+Blvd+Montgomery+AL+36106"

MAP_EMBED = "https://www.google.com/maps?q=4791+Woodmere+Blvd,+Montgomery,+AL+36106&amp;output=embed"

_CONTAINER_TAGS = {"div", "header", "footer", "main", "article", "section", "aside", "nav", "a"}

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
def box(classes, children, tag="div", link=None, el_id=None, **extra):
    """A container mirroring one prototype element. No gap, padding or layout of its
    own: the stylesheet owns all of that (adapter + ported CSS)."""
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
    return E.container(s, children, inner=True, classes=cls or None)


def section(classes, children, tag="section", el_id=None, label=None):
    """Prototype `<section class=...>` band -> one neutral boxed container -> children
    (normally one `box("wrap ...")`)."""
    inner = E.container({
        "content_width": "boxed",
        "boxed_width": {"unit": "%", "size": 100, "sizes": []},
        "padding": _zero(), "padding_mobile": _zero(),
    }, children)
    # Zero padding vars: Elementor gives top-level containers a 10px side padding on
    # mobile. Ported rules that set padding (`.hero`, `.section`) still win, because
    # they set the property and Elementor only sets the variables.
    s = {"content_width": "full", "html_tag": tag,
         "padding": _zero(), "padding_tablet": _zero(), "padding_mobile": _zero()}
    if el_id:
        s["_element_id"] = el_id
    if label:
        s["_attributes"] = "aria-label|%s" % label
    # Elementor's background lazy-load hides background-images inside a band with
    # !important until its JS marks the band; the prototype paints patterns with
    # background-image. Opt each band out.
    return E.container(s, [inner], inner=False, classes=(classes + " e-no-lazyload").strip())


def heading(text, tag="h2", classes=None, size=None):
    """Native heading. `size` (a CSS length, may be clamp()) is emitted for every
    breakpoint where the gate needs it (h1/h2) and must equal the prototype's
    value, because element settings outrank the stylesheet."""
    s = {"title": text, "header_size": tag}
    if size:
        for bp in ("", "_tablet", "_mobile"):
            s["typography_font_size" + bp] = {"unit": "custom", "size": size, "sizes": []}
        s["typography_typography"] = "custom"
    _register(classes, "heading")
    return E.widget("heading", s, classes=classes)


def button(label, url, classes, external=False):
    """Native button. Text only: the button text runs through wp_kses_post, which
    strips inline SVG (Lenz uses CSS-mask icons if one is ever needed)."""
    _register(classes, "button")
    return E.widget("button", {"text": label, "link": _link(url, external)}, classes=classes)


def image(key, alt, classes=None):
    m = MEDIA[key]
    _register(classes, "image")
    s = {"image": {"url": m["url"], "id": m["id"], "size": "", "alt": alt, "source": "library"},
         "image_size": "full"}
    return E.widget("image", s, classes=classes)


def raw(markup, classes=None):
    """html widget: markup Elementor cannot express, verbatim from the prototype."""
    return E.widget("html", {"html": markup}, classes=classes)


def esc(s):
    return _html.escape(s, quote=False)


# ============================================================ components ====
SEC_H2 = "clamp(2.6rem, 5.6vw, 4.8rem)"     # .sec-head h2 (v2.css)


def sec_head(num, kicker, title_html):
    """`header.sec-head`: issue number, kicker, h2 with an italic accent."""
    return box("sec-head reveal", [
        heading(num, "div", "sec-num"),
        box("", [heading(kicker, "p", "kicker"), heading(title_html, "h2", size=SEC_H2)]),
    ], tag="header")
