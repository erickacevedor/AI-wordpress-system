# -*- coding: utf-8 -*-
"""
What a built page NEEDS from the target install, and what the kit says it HAS.

The deliverable is a JSON file someone else imports, often onto a host nobody here
can reach. There is no second try and no console to read: if a page depends on a
plugin the target does not have, the widget imports as an empty gap, and the first
person to notice is the client.

So a page's dependencies have to be stated up front, in the handoff, before it ships.

Elementor Pro is the exception: every site this system builds for runs it, so Pro
widgets are classified (below) but never reported as a risk. Classifying them still
matters -- it is what keeps `accordion`, `form` and `mega-menu` out of the
"unrecognised widget" bucket, where they would read as a real problem.

This module answers both halves:

  requirements(doc)      -> what this page needs (Pro widgets, third-party widgets,
                            shortcodes from other plugins)
  kit_facts(site_dir)    -> what the kit's manifest says the site actually runs
                            (plugin list, Elementor version, every page's URL)

Shared by validate-page.py (warns per page) and analyze-kit.py (reports per kit), so
the widget lists live in exactly one place.
"""
import json
import os

# Widgets that require Elementor PRO. Pro is assumed present on every target, so this
# set is used for CLASSIFICATION, not for warnings: knowing `accordion` is a Pro widget
# is how we avoid reporting it as an unrecognised one.
PRO_WIDGETS = {
    "accordion", "toggle", "form", "posts", "portfolio", "slides", "nav-menu",
    "animated-headline", "price-list", "price-table", "flip-box", "call-to-action",
    "media-carousel", "testimonial-carousel", "reviews", "table-of-contents",
    "countdown", "share-buttons", "blockquote", "lottie", "hotspot", "paypal-button",
    "search-form", "login", "theme-post-content", "theme-site-logo", "loop-grid",
    "gallery", "post-info", "sitemap", "author-box", "post-comments", "post-navigation",
    "woocommerce-products", "code-highlight", "video-playlist", "progress-tracker",
    "nested-carousel", "mega-menu", "off-canvas", "taxonomy-filter",
}

# Widget-name prefixes contributed by third-party addon packs. Seen in these kits:
# `ha-` (Happy Elementor Addons) on gcreliable.
THIRD_PARTY_PREFIXES = {
    "ha-": "Happy Elementor Addons",
    "uael-": "Ultimate Addons for Elementor",
    "eael-": "Essential Addons for Elementor",
    "wpr-": "Royal Elementor Addons",
    "premium-": "Premium Addons for Elementor",
    "jet-": "JetElements / Crocoblock",
    "elementskit-": "ElementsKit",
    "tp-": "The Plus Addons",
    "sina-": "Sina Extension",
    "pp-": "PowerPack Addons",
}

# Elementor's own free widgets, for classifying anything unrecognised.
CORE_WIDGETS = {
    "heading", "image", "text-editor", "video", "button", "divider", "spacer",
    "google_maps", "icon", "image-box", "icon-box", "star-rating", "image-carousel",
    "image-gallery", "icon-list", "counter", "progress", "testimonial", "tabs",
    "alert", "html", "menu-anchor", "sidebar", "shortcode", "text-path",
    "nested-accordion", "nested-tabs", "container", "social-icons", "rating",
}


def _walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for v in node.values():
            _walk(v, fn)
    elif isinstance(node, list):
        for x in node:
            _walk(x, fn)


def requirements(doc):
    """What this page needs from the target install."""
    pro, third, shortcodes, unknown = {}, {}, [], {}

    def visit(el):
        wt = el.get("widgetType")
        if not wt:
            return
        if wt in PRO_WIDGETS:
            pro[wt] = pro.get(wt, 0) + 1
            return
        for prefix, pack in THIRD_PARTY_PREFIXES.items():
            if wt.startswith(prefix):
                third.setdefault(pack, {})
                third[pack][wt] = third[pack].get(wt, 0) + 1
                return
        if wt == "shortcode":
            code = ((el.get("settings") or {}).get("shortcode") or "").strip()
            if code:
                shortcodes.append(code[:120])
            return
        if wt not in CORE_WIDGETS:
            unknown[wt] = unknown.get(wt, 0) + 1

    _walk(doc.get("content", doc), visit)
    return {
        "pro_widgets": pro,
        "third_party": third,
        "shortcodes": shortcodes,
        "unrecognised": unknown,
    }


def kit_facts(site_dir):
    """Read the kit manifest: which plugins the site runs, and every page's URL.
    Returns None when the site has no kit (e.g. onboarded from HTML)."""
    manifest = os.path.join(site_dir, "current-theme", "manifest.json")
    if not os.path.exists(manifest):
        return None
    try:
        with open(manifest, encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        return None

    plugins = []
    for p in m.get("plugins") or []:
        if isinstance(p, dict) and p.get("name"):
            plugins.append(p["name"])
        elif isinstance(p, str):
            plugins.append(p)

    pages = {}
    content = m.get("content") or {}
    for kind in ("page", "post"):
        for pid, meta in (content.get(kind) or {}).items():
            if isinstance(meta, dict) and meta.get("url"):
                pages[str(pid)] = {"url": meta["url"], "title": meta.get("title", ""),
                                   "kind": kind}
    return {
        "site": m.get("site"),
        "elementor_version": m.get("elementor_version"),
        "theme": m.get("theme"),
        "plugins": plugins,
        "has_pro": any("elementor pro" in p.lower() for p in plugins),
        "pages": pages,
    }


def known_paths(facts):
    """The set of URL paths the kit says exist, normalised to '/slug/' form."""
    out = set()
    if not facts:
        return out
    for meta in facts["pages"].values():
        url = meta.get("url") or ""
        path = url
        for scheme in ("https://", "http://"):
            if path.startswith(scheme):
                path = path[len(scheme):]
                slash = path.find("/")
                path = path[slash:] if slash >= 0 else "/"
                break
        out.add(normalise_path(path))
    return out


def normalise_path(p):
    """'/systems/ac' and '/systems/ac/' are the same page; compare them that way."""
    p = (p or "").split("#")[0].split("?")[0].strip()
    if not p:
        return "/"
    if not p.startswith("/"):
        p = "/" + p
    if len(p) > 1 and p.endswith("/"):
        p = p[:-1]
    return p.lower()
