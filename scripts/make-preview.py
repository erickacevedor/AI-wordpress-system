#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render a built Elementor page JSON to a standalone review HTML.

Why generated rather than hand-written: the PREVIEW.html files in this repo were
authored by hand, one per page, 8-19KB of CSS restating the design a second time. A
hand-written preview is a second source of truth -- it can say the hero is navy while
the JSON says it is white, and nothing catches the disagreement. This renders FROM the
page JSON, so the preview cannot drift from the thing being shipped: if they disagree,
the preview is wrong by construction and you regenerate it.

That matters most when the target site is unreachable. The page is a file handed to
someone else; this is the only look anyone here gets at it before it lands.

What it reproduces, from the JSON alone:
  - the section model: full-width band -> boxed container at the kit's width -> content
  - flex rows/columns and grids, with their gaps, widths and alignment
  - classic + gradient + image backgrounds, radii, padding, borders
  - headings, text, buttons, images, icon lists, accordions, raw html
  - THE BREAKPOINTS: every *_mobile / *_tablet setting becomes a real media query, so
    the mobile layout is inspectable by resizing the window rather than trusted

What it cannot reproduce, and says so instead of pretending:
  - anything painted by the site's stylesheet through a CSS class (pass --css to
    inline that stylesheet and get it back)
  - Pro/third-party widgets (forms, mega-menus, review sliders): drawn as a labelled
    placeholder box naming the widget, which is what the client will need wired up

Usage:
    python3 scripts/make-preview.py <page.json> [-o PREVIEW.html] [--css site.css]
    python3 scripts/make-preview.py <page.json> --check     # report drift, write nothing

Exit code: 0 = written (or up to date with --check), 1 = --check found drift.
"""
import html as _html
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TABLET_MAX = 1024
MOBILE_MAX = 767

PLACEHOLDER_WIDGETS = {
    "form": "Elementor Pro Form",
    "mega-menu": "Elementor Pro Mega Menu",
    "nav-menu": "Elementor Pro Nav Menu",
    "shortcode": "Shortcode (renders only on the live site)",
    "loop-grid": "Elementor Pro Loop Grid",
    "posts": "Elementor Pro Posts",
    "theme-site-logo": "Site Logo",
    "search-form": "Search Form",
}


# ------------------------------------------------------------------ helpers
def esc(s):
    return _html.escape(s or "", quote=True)


def _unit(v, default=""):
    """An Elementor size dict -> a CSS length."""
    if not isinstance(v, dict):
        return default
    size = v.get("size")
    if size in ("", None):
        return default
    unit = v.get("unit") or "px"
    if unit == "custom":
        return str(size)
    return "%s%s" % (size, unit)


def _box(v):
    """An Elementor dimensions dict -> a CSS shorthand."""
    if not isinstance(v, dict):
        return None
    unit = v.get("unit") or "px"
    if unit == "custom":
        return v.get("top") or None
    parts = []
    for k in ("top", "right", "bottom", "left"):
        val = v.get(k)
        parts.append("0" if val in ("", None) else "%s%s" % (val, unit))
    return " ".join(parts) if any(p != "0" for p in parts) else "0"


def _bg_css(s):
    out = []
    bg = s.get("background_background")
    img = (s.get("background_image") or {}).get("url")
    if bg == "gradient":
        a = s.get("background_color") or "#fff"
        b = s.get("background_color_b") or "#fff"
        ang = s.get("background_gradient_angle")
        deg = _unit(ang, "180deg") if isinstance(ang, dict) else "180deg"
        gtype = s.get("background_gradient_type") or "linear"
        if gtype == "radial":
            out.append("background:radial-gradient(circle, %s 0%%, %s 100%%)" % (a, b))
        else:
            out.append("background:linear-gradient(%s, %s 0%%, %s 100%%)" % (deg, a, b))
    elif img:
        out.append("background-image:url('%s')" % img)
        out.append("background-size:%s" % (s.get("background_size") or "cover"))
        out.append("background-position:%s" % (s.get("background_position") or "center center"))
        out.append("background-repeat:no-repeat")
        if s.get("background_color"):
            out.append("background-color:%s" % s["background_color"])
    elif bg == "classic" and s.get("background_color"):
        out.append("background-color:%s" % s["background_color"])
    return out


def _typo_css(s, prefix="typography_"):
    out = []
    fam = s.get(prefix + "font_family")
    if fam:
        out.append("font-family:'%s', system-ui, -apple-system, 'Segoe UI', Arial, sans-serif" % fam)
    size = _unit(s.get(prefix + "font_size"))
    if size:
        out.append("font-size:%s" % size)
    w = s.get(prefix + "font_weight")
    if w:
        out.append("font-weight:%s" % w)
    lh = _unit(s.get(prefix + "line_height"))
    if lh:
        out.append("line-height:%s" % lh)
    ls = _unit(s.get(prefix + "letter_spacing"))
    if ls:
        out.append("letter-spacing:%s" % ls)
    tt = s.get(prefix + "text_transform")
    if tt:
        out.append("text-transform:%s" % tt)
    return out


def _border_css(s):
    out = []
    r = _box(s.get("border_radius"))
    if r:
        out.append("border-radius:%s" % r)
    if s.get("border_border"):
        w = _box(s.get("border_width")) or "1px"
        out.append("border:%s %s" % (s["border_border"], s.get("border_color") or "#ddd"))
        out.append("border-width:%s" % w)
    if s.get("box_shadow_box_shadow_type"):
        sh = s.get("box_shadow_box_shadow") or {}
        out.append("box-shadow:%spx %spx %spx %spx %s"
                   % (sh.get("horizontal", 0), sh.get("vertical", 0),
                      sh.get("blur", 0), sh.get("spread", 0),
                      sh.get("color", "rgba(0,0,0,.1)")))
    return out


def _container_css(s):
    """Layout for a container, matching how Elementor's flex/grid containers behave."""
    out = []
    ctype = s.get("container_type")
    if ctype == "grid":
        cols = (s.get("grid_columns_grid") or {}).get("size")
        out.append("display:grid")
        out.append("grid-template-columns:repeat(%s, minmax(0,1fr))" % (cols or 3))
        gaps = s.get("grid_gaps") or {}
        out.append("gap:%spx %spx" % (gaps.get("row", 0) or 0, gaps.get("column", 0) or 0))
        if s.get("grid_align_items"):
            out.append("align-items:%s" % s["grid_align_items"])
    else:
        out.append("display:flex")
        out.append("flex-direction:%s" % (s.get("flex_direction") or "column"))
        gap = s.get("flex_gap")
        if isinstance(gap, dict):
            unit = gap.get("unit") or "px"
            out.append("gap:%s%s %s%s" % (gap.get("row", gap.get("size", 0)), unit,
                                          gap.get("column", gap.get("size", 0)), unit))
        if s.get("flex_align_items"):
            out.append("align-items:%s" % s["flex_align_items"])
        if s.get("flex_justify_content"):
            out.append("justify-content:%s" % s["flex_justify_content"])
        if s.get("flex_wrap"):
            out.append("flex-wrap:%s" % s["flex_wrap"])
    w = _unit(s.get("width"))
    if w:
        out.append("width:%s" % w)
    mh = _unit(s.get("min_height"))
    if mh:
        out.append("min-height:%s" % mh)
    pad = _box(s.get("padding"))
    if pad:
        out.append("padding:%s" % pad)
    mar = _box(s.get("margin"))
    if mar:
        out.append("margin:%s" % mar)
    out += _bg_css(s)
    out += _border_css(s)
    if s.get("content_width") == "boxed":
        bw = _unit(s.get("boxed_width"), "1140px")
        out.append("max-width:%s" % bw)
        out.append("margin-left:auto")
        out.append("margin-right:auto")
        out.append("width:100%")
    return out


def _responsive_css(s, base_fn, suffix):
    """Re-run a css builder against the *_mobile / *_tablet variants, so the preview
    carries the same breakpoints the validator insists on."""
    variant = {}
    for k, v in s.items():
        if k.endswith(suffix):
            variant[k[: -len(suffix)]] = v
    if not variant:
        return []
    merged = dict(s)
    merged.update(variant)
    base = set(base_fn(s))
    return [r for r in base_fn(merged) if r not in base]


# ------------------------------------------------------------------ render
class Renderer(object):
    def __init__(self, css_path=None):
        self.rules = []          # (selector, [decls])
        self.mobile = []
        self.tablet = []
        self.n = 0
        self.notes = []
        self.extra_css = ""
        if css_path and os.path.exists(css_path):
            with open(css_path, encoding="utf-8") as f:
                self.extra_css = f.read()

    def cls(self, prefix="e"):
        self.n += 1
        return "%s%d" % (prefix, self.n)

    def add(self, cls, decls, mobile=None, tablet=None):
        if decls:
            self.rules.append((cls, decls))
        if tablet:
            self.tablet.append((cls, tablet))
        if mobile:
            self.mobile.append((cls, mobile))

    # -- widgets --------------------------------------------------------
    def widget(self, el):
        s = el.get("settings") or {}
        wt = el.get("widgetType")
        cls = self.cls("w")
        user_cls = (s.get("_css_classes") or "").strip()
        cn = (cls + " " + user_cls).strip()

        if wt == "heading":
            tag = s.get("header_size") or "h2"
            if tag not in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "span"):
                tag = "div"
            decls = _typo_css(s)
            if s.get("title_color"):
                decls.append("color:%s" % s["title_color"])
            if s.get("align"):
                decls.append("text-align:%s" % s["align"])
            decls.append("margin:0")
            self.add(cn.split()[0], decls,
                     mobile=_typo_css_variant(s, "_mobile"),
                     tablet=_typo_css_variant(s, "_tablet"))
            return "<%s class=\"%s\">%s</%s>" % (tag, esc(cn), s.get("title") or "", tag)

        if wt == "text-editor":
            decls = _typo_css(s)
            if s.get("text_color"):
                decls.append("color:%s" % s["text_color"])
            if s.get("align"):
                decls.append("text-align:%s" % s["align"])
            self.add(cn.split()[0], decls,
                     mobile=_typo_css_variant(s, "_mobile"),
                     tablet=_typo_css_variant(s, "_tablet"))
            return "<div class=\"%s\">%s</div>" % (esc(cn), s.get("editor") or "")

        if wt == "button":
            decls = ["display:inline-flex", "align-items:center", "gap:8px",
                     "text-decoration:none", "cursor:pointer"]
            decls += _typo_css(s)
            decls += _border_css(s)
            if s.get("background_color"):
                decls.append("background:%s" % s["background_color"])
            if s.get("button_text_color"):
                decls.append("color:%s" % s["button_text_color"])
            pad = _box(s.get("text_padding"))
            decls.append("padding:%s" % (pad or "14px 28px"))
            label = s.get("text") or "Button"
            url = (s.get("link") or {}).get("url") or "#"
            self.add(cn.split()[0], decls)
            wrap_cls = self.cls("bw")
            self.add(wrap_cls, ["display:flex", "justify-content:%s"
                                % {"left": "flex-start", "right": "flex-end"}.get(s.get("align"), "center")])
            return ("<div class=\"%s\"><a class=\"%s\" href=\"%s\">%s</a></div>"
                    % (wrap_cls, esc(cn), esc(url), esc(label)))

        if wt == "image":
            img = s.get("image") or {}
            decls = ["display:block", "max-width:100%", "width:100%", "object-fit:%s"
                     % (s.get("object-fit") or "cover")]
            h = _unit(s.get("height"))
            if h:
                decls.append("height:%s" % h)
            r = _box(s.get("image_border_radius"))
            if r:
                decls.append("border-radius:%s" % r)
            mob = []
            hm = _unit(s.get("height_mobile"))
            if hm:
                mob.append("height:%s" % hm)
            self.add(cn.split()[0], decls, mobile=mob)
            return ("<img class=\"%s\" src=\"%s\" alt=\"%s\" loading=\"lazy\">"
                    % (esc(cn), esc(img.get("url") or ""), esc(img.get("alt") or "")))

        if wt in ("icon-list",):
            items = s.get("icon_list") or []
            decls = ["list-style:none", "margin:0", "padding:0",
                     "display:flex", "flex-direction:column", "gap:8px"]
            if s.get("text_color"):
                decls.append("color:%s" % s["text_color"])
            self.add(cn.split()[0], decls)
            lis = "".join("<li>✓ %s</li>" % (i.get("text") or "") for i in items)
            return "<ul class=\"%s\">%s</ul>" % (esc(cn), lis)

        if wt in ("accordion", "nested-accordion"):
            return self.accordion(el, cn)

        if wt == "html":
            return s.get("html") or ""

        if wt == "icon":
            return "<div class=\"ph-icon\">◆</div>"

        label = PLACEHOLDER_WIDGETS.get(wt, "Widget: %s" % wt)
        self.notes.append(label)
        return ("<div class=\"ph\"><strong>%s</strong><br><span>not rendered here — "
                "wire up / verify after import</span></div>" % esc(label))

    def accordion(self, el, cn):
        s = el.get("settings") or {}
        out = []
        tabs = s.get("tabs")
        if isinstance(tabs, list) and tabs:                 # Pro accordion
            for t in tabs:
                out.append((t.get("tab_title") or "", t.get("tab_content") or ""))
        else:                                               # nested-accordion
            titles = [i.get("item_title") or "" for i in (s.get("items") or [])]
            bodies = []
            for kid in (el.get("elements") or []):
                inner = []
                _collect_text(kid, inner)
                bodies.append("".join(inner))
            for i, t in enumerate(titles):
                out.append((t, bodies[i] if i < len(bodies) else ""))
        rows = "".join(
            "<details><summary>%s</summary><div class=\"acc-body\">%s</div></details>"
            % (esc(q), a) for q, a in out)
        return "<div class=\"acc %s\">%s</div>" % (esc(cn), rows)

    # -- containers -----------------------------------------------------
    def container(self, el):
        s = el.get("settings") or {}
        cls = self.cls("c")
        user_cls = (s.get("css_classes") or "").strip()
        cn = (cls + " " + user_cls).strip()
        self.add(cls, _container_css(s),
                 mobile=_responsive_css(s, _container_css, "_mobile"),
                 tablet=_responsive_css(s, _container_css, "_tablet"))
        inner = "".join(self.node(k) for k in (el.get("elements") or []))
        return "<div class=\"%s\">%s</div>" % (esc(cn), inner)

    def node(self, el):
        if not isinstance(el, dict):
            return ""
        if el.get("elType") == "container":
            return self.container(el)
        if el.get("elType") == "widget" or el.get("widgetType"):
            return self.widget(el)
        return "".join(self.node(k) for k in (el.get("elements") or []))

    def stylesheet(self):
        parts = []
        for cls, decls in self.rules:
            parts.append(".%s{%s}" % (cls, ";".join(decls)))
        if self.tablet:
            parts.append("@media (max-width:%dpx){%s}" % (
                TABLET_MAX, "".join(".%s{%s}" % (c, ";".join(d)) for c, d in self.tablet)))
        if self.mobile:
            parts.append("@media (max-width:%dpx){%s}" % (
                MOBILE_MAX, "".join(".%s{%s}" % (c, ";".join(d)) for c, d in self.mobile)))
        return "\n".join(parts)


def _typo_css_variant(s, suffix):
    variant = {}
    for k, v in s.items():
        if k.endswith(suffix) and k.startswith("typography_"):
            variant[k[: -len(suffix)]] = v
    if not variant:
        return []
    merged = dict(s)
    merged.update(variant)
    base = set(_typo_css(s))
    return [r for r in _typo_css(merged) if r not in base]


def _collect_text(el, out):
    if isinstance(el, dict):
        s = el.get("settings") or {}
        if el.get("widgetType") == "text-editor":
            out.append(s.get("editor") or "")
        elif el.get("widgetType") == "heading":
            out.append("<p>%s</p>" % (s.get("title") or ""))
        for kid in (el.get("elements") or []):
            _collect_text(kid, out)
    elif isinstance(el, list):
        for x in el:
            _collect_text(x, out)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s (Preview)</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:system-ui,-apple-system,'Segoe UI',Arial,sans-serif;line-height:1.55;color:#1a1a1a}
img{max-width:100%%}
a{color:inherit}
.acc details{border-bottom:1px solid rgba(0,0,0,.12)}
.acc summary{cursor:pointer;padding:14px 0;font-weight:600;list-style:revert}
.acc .acc-body{padding:0 0 14px}
.ph{border:2px dashed #b9c2cf;border-radius:10px;padding:22px;text-align:center;
    background:repeating-linear-gradient(45deg,#f7f9fc,#f7f9fc 10px,#eef2f7 10px,#eef2f7 20px);
    color:#5a6676;font-size:14px}
.ph strong{color:#31405a;font-size:15px}
.ph-icon{font-size:28px;line-height:1;opacity:.55}
.pv-bar{position:sticky;top:0;z-index:99;background:#101828;color:#fff;padding:9px 14px;
        font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;display:flex;
        gap:16px;flex-wrap:wrap;align-items:center}
.pv-bar b{color:#7dd3fc;font-weight:600}
.pv-bar .warn{color:#fbbf24}
%(extra)s
%(css)s
</style>
</head>
<body>
<div class="pv-bar">
  <span><b>PREVIEW</b> %(title)s</span>
  <span>%(sections)d sections · %(widgets)d widgets</span>
  <span>generated from %(source)s — resize the window to check tablet/mobile</span>
  %(notes)s
</div>
%(body)s
</body>
</html>
"""


def render(doc, source_name, css_path=None):
    r = Renderer(css_path)
    content = doc.get("content") or []
    body = "".join(r.node(sec) for sec in content)
    widgets = len(re.findall(r'class="w\d+', body)) + len(r.notes)
    notes = ""
    if r.notes:
        uniq = sorted(set(r.notes))
        notes = ("<span class=\"warn\">placeholders: %s</span>"
                 % esc(", ".join(uniq)))
    if css_path and not os.path.exists(css_path or ""):
        notes += "<span class=\"warn\">css not found: %s</span>" % esc(css_path)
    return SHELL % {
        "title": esc(doc.get("title") or source_name),
        "css": r.stylesheet(),
        "extra": r.extra_css,
        "body": body,
        "sections": len(content),
        "widgets": widgets,
        "source": esc(source_name),
        "notes": notes,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__)
        sys.exit(2)
    src = args[0]
    out = None
    css = None
    if "-o" in sys.argv:
        out = sys.argv[sys.argv.index("-o") + 1]
    if "--css" in sys.argv:
        css = sys.argv[sys.argv.index("--css") + 1]
    check = "--check" in sys.argv

    try:
        with open(src, encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        print("✗ page JSON not found: %s" % src)
        sys.exit(2)
    except ValueError as ex:
        print("✗ not valid JSON: %s (%s)" % (src, ex))
        sys.exit(2)
    if not isinstance(doc, dict) or not doc.get("content"):
        print("✗ %s is not a single-page wrapper (no `content` array) — this renders "
              "built pages, not kit content/page files." % src)
        sys.exit(2)
    html_out = render(doc, os.path.basename(src), css)

    target = out or os.path.join(os.path.dirname(os.path.abspath(src)), "PREVIEW.html")
    if check:
        if not os.path.exists(target):
            print("⚠️  no PREVIEW.html beside %s" % src)
            sys.exit(1)
        existing = open(target, encoding="utf-8").read()
        if existing.strip() == html_out.strip():
            print("✅ PREVIEW.html is current for %s" % os.path.basename(src))
            sys.exit(0)
        print("⚠️  PREVIEW.html differs from what %s renders — regenerate it"
              % os.path.basename(src))
        sys.exit(1)

    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)
    print("✅ wrote %s  (%d sections, from %s)"
          % (target, len(doc.get("content") or []), os.path.basename(src)))
    sys.exit(0)


if __name__ == "__main__":
    main()
