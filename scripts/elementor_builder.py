# -*- coding: utf-8 -*-
"""
Reusable, site-agnostic Elementor page-builder library.

Encodes the repo's structural + responsive STANDARDS once so every page built with
it is correct by construction:

  - every section = full-width Section -> ONE boxed content container -> content
  - grids stack (tablet ~2 / mobile 1); flex rows stack on mobile;
    %-width columns go 100% on mobile; boxed containers get padding_mobile;
    images get height_mobile; h1/h2 auto-get mobile/tablet sizes.
  - unique element ids; single-page import wrapper.

BRAND styling (colors, fonts, button spec) is NOT hard-coded here — the per-site
`projects/<site>/build.py` passes it in (usually from `projects/<site>/tokens.json`).
That keeps this library reusable across any site while the brand lives per project.

A page built entirely through these helpers passes `scripts/validate-page.py`.
"""

# ---- unique id generator (deterministic; reset per build for stable output) ----
_counter = [0x10000000]

def reset_ids(seed=0x10000000):
    _counter[0] = seed

def nid():
    _counter[0] += 0x1357
    return format(_counter[0], "x")[-8:]

# ---------------- generic nodes ----------------
def widget(wtype, settings, elements=None, inner=True):
    return {"id": nid(), "settings": settings, "elements": elements or [],
            "isInner": inner, "widgetType": wtype, "elType": "widget"}

def container(settings, elements, inner=True):
    return {"id": nid(), "settings": settings, "elements": elements,
            "isInner": inner, "elType": "container"}

def _px(v):  return {"unit": "px", "size": v, "sizes": []}
def _pct(v): return {"unit": "%", "size": v, "sizes": []}
def _pad(t, r, b, l): return {"unit": "px", "top": str(t), "right": str(r),
                              "bottom": str(b), "left": str(l), "isLinked": False}

# ---------------- structure (standards baked in) ----------------
def section(bg, children, content_width=1140, pad=(70, 20, 70, 20),
            pad_mobile=(45, 18, 45, 18)):
    """Full-width (100%) band -> ONE boxed content container -> children.

    `bg` is a dict of outer-Section settings (background color/image/overlay). It may
    carry a special key `_box` whose dict is merged into the boxed container (e.g. to
    override padding on a hero). content_width caps the boxed container to the site
    width. padding_mobile is always set (responsive gate).
    """
    box_extra = dict(bg.pop("_box", {}))
    box_settings = {
        "content_width": "boxed",
        "boxed_width": _px(content_width),
        "flex_direction": "column",
        "flex_gap": {"unit": "px", "size": 22, "column": "22", "row": "22"},
        "padding": _pad(*pad),
        "padding_mobile": _pad(*pad_mobile),
    }
    box_settings.update(box_extra)
    box = container(box_settings, children)
    outer = {"content_width": "full", "flex_direction": "column"}
    outer.update(bg)
    return container(outer, [box], inner=False)

def row(cols, reverse=False, align="center", gap=34):
    """Multi-column flex row. Always stacks to a column on mobile (responsive gate)."""
    return container({
        "content_width": "full",
        "flex_direction": "row-reverse" if reverse else "row",
        "flex_align_items": align,
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)},
        "flex_direction_mobile": "column",
    }, cols)

def column(children, width=None, gap=16, align=None):
    s = {"content_width": "full", "flex_direction": "column",
         "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}}
    if align:
        s["flex_align_items"] = align
    if width:  # %-width columns always go 100% on mobile (+ tablet) — responsive gate
        s["width"] = _pct(width)
        s["width_tablet"] = _pct(100)
        s["width_mobile"] = _pct(100)
    return container(s, children)

def grid(children, cols=3, tablet=2, mobile=1, gap=22, bg=None, radius=14, pad=26):
    """Grid container. Always sets tablet + mobile column counts (responsive gate)."""
    s = {"content_width": "full", "container_type": "grid",
         "grid_columns_grid": {"unit": "fr", "size": cols, "sizes": []},
         "grid_columns_grid_tablet": {"unit": "fr", "size": tablet, "sizes": []},
         "grid_columns_grid_mobile": {"unit": "fr", "size": mobile, "sizes": []},
         "grid_rows_grid": {"unit": "fr", "size": 0, "sizes": []},
         "grid_gaps": {"column": str(gap), "row": str(gap), "isLinked": True, "unit": "px"},
         "grid_align_items": "stretch",
         "presetTitle": "Grid", "presetIcon": "eicon-container-grid"}
    if bg:
        s.update({"background_background": "classic", "background_color": bg,
                  "border_radius": {"unit": "px", "top": str(radius), "right": str(radius),
                                    "bottom": str(radius), "left": str(radius), "isLinked": True},
                  "padding": _pad(pad, pad, pad, pad), "grid_align_items": "start"})
    return container(s, children)

def card(children, bg="#FFFFFF", radius=14, pad=26, gap=10, border=None):
    s = {"content_width": "full", "flex_direction": "column",
         "background_background": "classic", "background_color": bg,
         "border_radius": {"unit": "px", "top": str(radius), "right": str(radius),
                           "bottom": str(radius), "left": str(radius), "isLinked": True},
         "padding": _pad(pad, pad, pad, pad),
         "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}}
    if border:
        s.update({"border_border": "solid",
                  "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1",
                                   "left": "1", "isLinked": True},
                  "border_color": border})
    return container(s, children)

# ---------------- widgets ----------------
def _typo(font=None, size=None, weight=None, unit="px", mobile=None, tablet=None,
          lh=None, transform=None):
    t = {}
    if font or size:
        t["typography_typography"] = "custom"
    if font:   t["typography_font_family"] = font
    if size is not None:   t["typography_font_size"] = {"unit": unit, "size": size, "sizes": []}
    if tablet is not None: t["typography_font_size_tablet"] = {"unit": unit, "size": tablet, "sizes": []}
    if mobile is not None: t["typography_font_size_mobile"] = {"unit": unit, "size": mobile, "sizes": []}
    if weight: t["typography_font_weight"] = weight
    if lh:     t["typography_line_height"] = {"unit": "em", "size": lh, "sizes": []}
    if transform: t["typography_text_transform"] = transform
    return t

def heading(title, tag="h2", color=None, color_global=None, font=None, size=None,
            unit="px", weight=None, mobile=None, tablet=None, lh=None, align=None, extra=None):
    """Heading. For h1/h2, if no mobile size is given, one is auto-derived so the
    responsive gate always passes (globals-only headings don't shrink)."""
    s = {"title": title, "header_size": tag}
    if tag in ("h1", "h2") and size is not None and mobile is None:
        mobile = round(size * (0.62 if tag == "h1" else 0.72), 2)
        if tablet is None:
            tablet = round(size * (0.78 if tag == "h1" else 0.85), 2)
    s.update(_typo(font, size, weight, unit, mobile, tablet, lh))
    if color_global:
        s.setdefault("__globals__", {})["title_color"] = color_global
    if color:
        s["title_color"] = color
    if align:
        s["align"] = align
    if extra:
        s.update(extra)
    return widget("heading", s)

def text(html, color=None, color_global=None, font=None, size=None, unit="px",
         weight=None, mobile=None, lh=None, align=None, extra=None):
    s = {"editor": html}
    s.update(_typo(font, size, weight, unit, mobile, None, lh))
    if color_global:
        s.setdefault("__globals__", {})["text_color"] = color_global
    if color:
        s["text_color"] = color
    if align:
        s["align"] = align
    if extra:
        s.update(extra)
    return widget("text-editor", s)

def button(txt, url, spec):
    """Build a button from a brand `spec` dict. Recognized spec keys:
      font, size, size_mobile, weight, transform, radius, border_width,
      align, hover_animation, hover_color, globals(dict), colors(dict inline),
      padding(t,r,b,l).
    """
    s = {"text": txt, "align": spec.get("align", "left"),
         "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}}
    s.update(_typo(spec.get("font"), spec.get("size"), spec.get("weight"),
                   "px", spec.get("size_mobile"), None, None, spec.get("transform")))
    r = spec.get("radius", 0)
    s["border_radius"] = {"unit": "px", "top": str(r), "right": str(r), "bottom": str(r),
                          "left": str(r), "isLinked": True}
    bw = spec.get("border_width", 1)
    s["border_border"] = "solid"
    s["border_width"] = {"unit": "px", "top": str(bw), "right": str(bw), "bottom": str(bw),
                         "left": str(bw), "isLinked": True}
    if "padding" in spec:
        s["text_padding"] = _pad(*spec["padding"])
    if spec.get("hover_animation"):
        s["hover_animation"] = spec["hover_animation"]
    if spec.get("hover_color"):
        s["hover_color"] = spec["hover_color"]
    if spec.get("icon"):  # {"value": "far fa-...", "library": "fa-regular"}
        s["selected_icon"] = spec["icon"]
        s["icon_align"] = spec.get("icon_align", "row-reverse")
    if spec.get("globals"):
        s["__globals__"] = dict(spec["globals"])
    for k, v in (spec.get("colors") or {}).items():
        s[k] = v
    return widget("button", s)

def image(url, alt, img_id="", height=440, height_mobile=280, radius=14):
    """Image. Always sets height_mobile (responsive gate)."""
    return widget("image", {
        "image": {"url": url, "id": img_id, "size": "", "alt": alt, "source": "library"},
        "height": _px(height), "height_mobile": _px(height_mobile),
        "object-fit": "cover",
        "image_border_radius": {"unit": "px", "top": str(radius), "right": str(radius),
                                "bottom": str(radius), "left": str(radius), "isLinked": True},
    })

def emoji_icon(emoji, font=None, size=42):
    """An emoji used as a decorative icon (no icon-font dependency)."""
    s = {"title": emoji, "header_size": "p"}
    s.update(_typo(font, size, None, "px", round(size * 0.85), None, 1))
    return widget("heading", s)

def accordion(items, title_font=None):
    """items = list of (question, answer_html). Builds a nested-accordion."""
    meta, children = [], []
    for q, a in items:
        meta.append({"item_title": q, "_id": nid()[:7]})
        c = container({"_title": "item", "content_width": "full"}, [text(a)])
        c["isLocked"] = True
        children.append(c)
    s = {"items": meta}
    if title_font:
        s["title_typography_typography"] = "custom"
        s["title_typography_font_family"] = title_font
    return widget("nested-accordion", s, children)

# ---------------- page wrapper ----------------
def wrap_page(title, sections, page_settings=None):
    """Single-page Elementor import wrapper."""
    return {
        "version": "0.4",
        "title": title,
        "type": "page",
        "content": sections,
        "page_settings": page_settings or {"template": "default"},
    }
