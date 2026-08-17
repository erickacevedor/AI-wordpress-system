# -*- coding: utf-8 -*-
"""
G.C. Reliable Service — site-wide brand layer over scripts/elementor_builder.py.

Site-wide, like tokens.json and skills/: it encodes the components mined from the
kit's reference page (`current-theme/content/page/225063.json`, "AC Repair") once, so
every gcreliable page assembles from the same vocabulary instead of re-deriving it.
Per-page build.py files import this and supply only copy + section order.

Everything here reads its values from ../tokens.json — no brand constants are typed
twice. Structural + responsive correctness still comes from elementor_builder.

Import from a page build.py:

    import brand as B          # after sys.path.insert(0, SITE)
    B.reset(0x30000000)
    S = [B.hero(...), B.sec(B.WHITE, [...]), ...]
    doc = B.page("AC Installation", S)
"""
import json, os, sys

SITE = os.path.dirname(os.path.abspath(__file__))


def _find_root(p):
    while p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, "AGENTS.md")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repo root (AGENTS.md) not found above %s" % SITE)


ROOT = _find_root(SITE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E  # noqa: E402

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))

# ---- brand constants, all sourced from tokens.json ----
C = {k: v["hex"] for k, v in T["colors"].items()}
G = {k: v["global"] for k, v in T["colors"].items()}
FONT = T["fonts"]["heading"]
BLUE, RED, DARK = C["primary"], C["secondary"], C["dark"]
TEXT, WHITE_HEX, GREY = C["text"], C["white"], C["grey"]
MIST, TINT, STEP = T["bands"]["mist"], T["bands"]["tint"], T["bands"]["step"]
GRAD = T["bands"]["hero_gradient"]
SEC, CARD, ICONS = T["section"], T["card"], T["icons"]
LINKS, PHONE, IMAGES, FACTS = T["links"], T["phone"], T["images"], T["facts"]
TS = T["type_scale"]

reset = E.reset_ids


# ---- small value helpers ----
def _rem(v):
    return {"unit": "rem", "size": v, "sizes": []}


def _px(v):
    return {"unit": "px", "size": v, "sizes": []}


def _gap(v):
    return {"unit": "px", "size": v, "column": str(v), "row": str(v), "isLinked": True}


def _rad(v):
    return {"unit": "px", "top": str(v), "right": str(v), "bottom": str(v),
            "left": str(v), "isLinked": True}


def _pad(t, r, b, l):
    return E._pad(t, r, b, l)


def _ls(px=0.5):
    """Kit headings track at 0.5px. elementor_builder's `ls=` is em-based, so
    letter-spacing always goes through `extra` instead."""
    return {"typography_letter_spacing": {"unit": "px", "size": px, "sizes": []}}


def _shadow(spec):
    return {"box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": dict(spec)}


# ---- section bands ----
WHITE = {}                                                        # no background
MISTB = {"background_background": "classic", "background_color": MIST}
GRADIENT = {"background_background": "gradient", "background_color": GRAD["from"],
            "background_color_b": GRAD["to"],
            "background_gradient_angle": {"unit": "deg", "size": GRAD["angle"], "sizes": []}}


def sec(bg, children, pad=None, gap=22, align="stretch", hero=False):
    """Full-width band -> ONE boxed 1280px container -> children.

    The kit carries section padding on the OUTER band (the boxed container is
    unpadded), so `pad` lands there and the box gets explicit zero padding — which
    also satisfies the validator's `padding_mobile` requirement on boxed containers.
    """
    pad = pad or SEC["pad"]
    outer = dict(bg)
    outer.update({
        "flex_align_items": "center",
        "padding": _pad(*pad),
        "padding_mobile": _pad(*SEC["pad_mobile"]),
        "margin": _pad(0, 0, 0, 0),
    })
    if hero:
        outer["min_height"] = {"unit": "vh", "size": 44, "sizes": []}
        outer["flex_justify_content"] = "center"
    outer["_box"] = {
        "boxed_width_laptop": {"unit": "%", "size": SEC["boxed_width_laptop_pct"], "sizes": []},
        "boxed_width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "boxed_width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_gap": _gap(gap),
        "flex_align_items": align,
    }
    return E.section(outer, children, content_width=SEC["boxed_width"],
                     pad=(0, 0, 0, 0), pad_mobile=(0, 0, 0, 0))


# ---- headings & text ----
def h1(title, city=None):
    """Hero H1. The city line rides inside the H1 as a styled span, as in the kit."""
    if city:
        title += ('<span style="display:block;font-size:1.9rem;font-weight:400;'
                  'text-transform:none;letter-spacing:0;margin-top:10px;">%s</span>' % city)
    extra = dict(_ls())
    extra["typography_line_height_mobile"] = {"unit": "em", "size": 1.05, "sizes": []}
    return E.heading(title, "h1", color=WHITE_HEX, font=FONT, size=TS["h1"]["size"],
                     unit="rem", weight=TS["h1"]["weight"], mobile=TS["h1"]["mobile"],
                     tablet=2.6, lh=TS["h1"]["lh"], align="center",
                     transform="uppercase", extra=extra)


def hero_sub(txt):
    extra = dict(_ls())
    extra["_margin"] = _pad(0, 0, 4, 0)
    return E.heading(txt, "h2", color=WHITE_HEX, font=FONT, size=TS["hero_sub"]["size"],
                     unit="rem", weight=TS["hero_sub"]["weight"],
                     mobile=TS["hero_sub"]["mobile"], tablet=1.35, align="center",
                     transform="none", extra=extra)


def h2(txt, color=None, align="left"):
    extra = dict(_ls())
    extra["_margin"] = _pad(0, 0, 4, 0)
    return E.heading(txt, "h2", color=color or TEXT, font=FONT, size=TS["h2"]["size"],
                     unit="rem", weight=TS["h2"]["weight"], mobile=TS["h2"]["mobile"],
                     tablet=TS["h2"]["tablet"], align=align, transform="none", extra=extra)


def h3(txt, color=None, size=None, align="left", lh=None):
    extra = dict(_ls())
    extra["_margin"] = _pad(0, 0, 6, 0)
    return E.heading(txt, "h3", color=color or TEXT, font=FONT,
                     size=size or TS["h3"]["size"], unit="rem", weight=TS["h3"]["weight"],
                     align=align, transform="none", lh=lh, extra=extra)


def h4(txt, color=None, align="left"):
    return E.heading(txt, "h4", color=color or TEXT, font=FONT,
                     size=TS["stat_label"]["size"], unit="rem",
                     weight=TS["stat_label"]["weight"], align=align, transform="none",
                     lh=TS["stat_label"]["lh"], extra=_ls())


def stat_number(txt, color=None):
    extra = dict(_ls())
    extra["_margin"] = _pad(0, 0, 2, 0)
    return E.heading(txt, "h3", color=color or RED, font=FONT, size=TS["stat_num"]["size"],
                     unit="rem", weight=TS["stat_num"]["weight"], align="left",
                     transform="none", extra=extra)


def body(html, on_dark=False):
    """Body copy carries NO local typography — it inherits the global 'Normal Text'.
    On the gradient bands the kit sets the colour inline in the HTML instead."""
    if on_dark:
        html = html.replace("<p>", '<p style="color:#FFFFFF;">')
    return E.text(html)


def body_center(html, on_dark=False):
    html = html.replace("<p>", '<p style="text-align:center;">')
    return body(html, on_dark)


def emoji(ch, size=42):
    return E.emoji_icon(ch, font=FONT, size=size)


# ---- button ----
def btn(txt, url=None, align="center"):
    b = T["button"]
    colors = dict(b["colors"])
    colors.update({
        "size": b["elementor_size"],
        "_element_width": "auto",
        "selected_icon": dict(b["icon"]),
        "icon_indent": _px(b["icon_indent"]),
        "typography_font_size": _rem(b["size"]),
        "typography_letter_spacing": _px(b["letter_spacing_px"]),
        "button_hover_transition_duration": {"unit": "s", "size": 0, "sizes": []},
    })
    spec = {"font": b["font"], "weight": b["weight"], "transform": b["transform"],
            "radius": b["radius"], "border_width": b["border_width"], "align": align,
            "hover_color": b["hover_color"], "globals": b["globals"], "colors": colors}
    return E.button(txt, url or LINKS["cta"], spec)


# ---- layout ----
def row(cols, gap=34, align="center", wrap=False, mobile_dir="column",
        tablet_dir=None, justify=None, gap_mobile=28):
    s = {"content_width": "full", "flex_direction": "row",
         "flex_align_items": align, "flex_gap": _gap(gap),
         "flex_gap_mobile": _gap(gap_mobile), "flex_direction_mobile": mobile_dir}
    if wrap:
        s["flex_wrap"] = "wrap"
    if tablet_dir:
        s["flex_direction_tablet"] = tablet_dir
    if justify:
        s["flex_justify_content"] = justify
    return E.container(s, cols)


def col(children, width=None, gap=16, align=None):
    return E.column(children, width=width, gap=gap, align=align)


def card(children, bg=None, radius=None, pad=None, gap=16, width=None,
         shadow="shadow", align=None):
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": _gap(gap),
         "background_background": "classic", "background_color": bg or CARD["bg"],
         "border_radius": _rad(radius if radius is not None else CARD["radius"]),
         "padding": _pad(*(pad or (CARD["pad"],) * 4))}
    if shadow:
        s.update(_shadow(CARD[shadow] if shadow in CARD else CARD["shadow"]))
    if align:
        s["flex_align_items"] = align
    if width:
        s["width"] = {"unit": "%", "size": width, "sizes": []}
        s["width_tablet"] = {"unit": "%", "size": 100, "sizes": []}
        s["width_mobile"] = {"unit": "%", "size": 100, "sizes": []}
    return E.container(s, children)


def step_card(n, title, html, width=48):
    """#F8F8FB card with the 4px blue left bar and a blue `01.` prefix."""
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": _gap(4),
         "background_background": "classic", "background_color": STEP,
         "border_border": "solid",
         "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "0",
                          "left": "4", "isLinked": False},
         "border_color": BLUE, "__globals__": {"border_color": G["primary"]},
         "border_radius": _rad(10), "padding": _pad(6, 0, 6, 20),
         "width": {"unit": "%", "size": width, "sizes": []},
         "width_tablet": {"unit": "%", "size": 100, "sizes": []},
         "width_mobile": {"unit": "%", "size": 100, "sizes": []}}
    title_html = ('<span style="color:%s;font-weight:700;">%02d.</span>&nbsp; %s'
                  % (BLUE, n, title))
    extra = dict(_ls())
    extra["_margin"] = _pad(0, 0, 6, 0)
    head = E.heading(title_html, "h3", color=TEXT, font=FONT, size=TS["h3_step"]["size"],
                     unit="rem", weight=TS["h3_step"]["weight"], align="left",
                     transform="none", extra=extra)
    return E.container(s, [head, body(html)])


def check_list(items, on_dark=False, space=None):
    """`fad fa-check-circle` icon list — blue/ink on light bands, white on gradient."""
    icon = dict(ICONS["list_check"])
    s = {"icon_list": [{"text": t, "selected_icon": dict(icon), "_id": E.nid()[:7]}
                       for t in items],
         "space_between": _px(space or ICONS["list"]["space_between"]),
         "icon_size": _px(ICONS["list"]["icon_size"]),
         "text_indent": _px(ICONS["list"]["text_indent"]),
         "icon_color": WHITE_HEX if on_dark else BLUE,
         "text_color": WHITE_HEX if on_dark else TEXT,
         "icon_typography_typography": "custom",
         "icon_typography_font_family": FONT}
    return E.widget("icon-list", s)


def fa_icon(value, library="fa-solid", size=40, color=None):
    return E.widget("icon", {"selected_icon": {"value": value, "library": library},
                             "primary_color": color or BLUE, "size": _px(size)})


def stat_card(icon_value, number, label, width=32):
    """Kit stat card: blue 40px icon, ink 2.2rem/800 number, grey 1rem label — all centred."""
    num = E.heading(number, "h3", color=TEXT, font=FONT, size=2.2, unit="rem",
                    weight="800", align="center", transform="none", extra=_ls())
    lab = E.heading(label, "h4", color="#666666", font=FONT, size=1, unit="rem",
                    weight="500", align="center", transform="none",
                    lh=TS["stat_label"]["lh"], extra=_ls())
    return card([fa_icon(icon_value), num, lab],
                pad=(26, 20, 26, 20), gap=6, width=width, shadow="stat_shadow",
                align="center")


def photo_badge(img, number, label, min_h=380):
    """Background photo + the overlapping white badge with the red left bar."""
    photo = E.container({
        "content_width": "full", "flex_direction": "column",
        "flex_justify_content": "center", "flex_align_items": "center",
        "flex_gap": _gap(4),
        "min_height": _px(min_h), "min_height_mobile": _px(230),
        "background_background": "classic", "background_color": TINT,
        "background_image": {"url": img["url"], "id": img["id"], "size": "",
                             "alt": img["alt"], "source": "library"},
        "background_position": "center center", "background_size": "cover",
        "background_repeat": "no-repeat",
        "border_radius": _rad(12), "padding": _pad(20, 20, 20, 20),
    }, [], classes=None)
    photo["settings"].update(_shadow(CARD["photo_shadow"]))

    badge_s = {
        "content_width": "full", "flex_direction": "column", "flex_gap": _gap(2),
        "width": {"unit": "%", "size": 62, "sizes": []},
        "width_tablet": {"unit": "%", "size": 72, "sizes": []},
        # The kit uses 82% here; the responsive gate requires 100% on mobile, and a
        # full-width badge reads fine once the row has stacked.
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "_flex_align_self": "flex-start",
        "background_background": "classic", "background_color": WHITE_HEX,
        "border_radius": _rad(12),
        "border_border": "solid",
        "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "0",
                         "left": "5", "isLinked": False},
        "border_color": RED, "__globals__": {"border_color": G["secondary"]},
        "padding": _pad(16, 20, 16, 20),
        "margin": _pad(-72, 0, 0, 26),
        "margin_mobile": _pad(-40, 0, 0, 0),
        "z_index": 3,
    }
    badge_s.update(_shadow(CARD["badge_shadow"]))
    badge = E.container(badge_s, [stat_number(number), h4(label)])

    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": _gap(0), "padding": _pad(0, 0, 0, 0)},
                       [photo, badge])


def image_placeholder(caption, min_h=190, min_h_mobile=230):
    """The kit's hand-off convention for a photo slot (templates 227376 / 227368).

    A `#E6ECFA` block that says what photo belongs there, so the site owner drops the
    image on the container's own Background setting after import. Use this instead of a
    real photo when the right asset does not exist in the media library yet."""
    lab = E.heading("▢  Image placeholder", "h4", color="#7C8DB5", font=FONT, size=1.05,
                    unit="rem", weight="500", align="center", transform="none")
    cap = E.text('<p style="text-align:center;color:#7C8DB5;font-size:0.8rem;margin:0;">'
                 '%s<br>(set this container&rsquo;s Background &rarr; Image)</p>' % caption)
    return E.container({
        "content_width": "full", "flex_direction": "column",
        "flex_justify_content": "center", "flex_align_items": "center",
        "flex_gap": _gap(4),
        "min_height": _px(min_h), "min_height_mobile": _px(min_h_mobile),
        "background_background": "classic", "background_color": TINT,
        "border_radius": _rad(12), "padding": _pad(20, 20, 20, 20),
    }, [lab, cap])


def photo_block(img, min_h=190, min_h_mobile=230):
    """Same slot as image_placeholder(), but filled with a real kit attachment."""
    return E.container({
        "content_width": "full", "flex_direction": "column",
        "flex_justify_content": "center", "flex_align_items": "center",
        "flex_gap": _gap(4),
        "min_height": _px(min_h), "min_height_mobile": _px(min_h_mobile),
        "background_background": "classic", "background_color": TINT,
        "background_image": {"url": img["url"], "id": img["id"], "size": "",
                             "alt": img["alt"], "source": "library"},
        "background_position": "center center", "background_size": "cover",
        "background_repeat": "no-repeat",
        "border_radius": _rad(12), "padding": _pad(20, 20, 20, 20),
    }, [])


def service_card(icon_value, title, url, body_html, media=None,
                 link_text="Learn more &rarr;", width=48, emoji_ch=None):
    """The kit's real service card (template 227376 §2).

    media block -> icon (38px red) -> H3 whose title is a BLUE LINK -> body ->
    a red bold "Learn more →" text link. `emoji_ch` swaps the Font Awesome icon for an
    emoji, which is how this repo keeps a page off a single icon-font dependency."""
    head = E.heading('<a href="%s" style="color:%s;">%s</a>' % (url, BLUE, title), "h3",
                     color=BLUE, font=FONT, size=1.4, unit="rem", weight="500",
                     align="left", transform="none", extra=_ls())
    icon = emoji(emoji_ch, size=38) if emoji_ch else fa_icon(icon_value, size=38, color=RED)
    kids = ([media] if media is not None else []) + [
        icon, head, body(body_html),
        E.text('<p><a href="%s" style="color:%s;font-weight:700;">%s</a></p>'
               % (url, RED, link_text)),
    ]
    return card(kids, gap=10, width=width)


def faq(items):
    """Elementor PRO `accordion` (a `tabs` array) — the kit's FAQ widget.
    elementor_builder.accordion() emits `nested-accordion`, which this kit does not use."""
    s = {"tabs": [{"tab_title": q, "tab_content": a, "_id": E.nid()[:7]}
                  for q, a in items],
         "title_color": TEXT, "tab_active_color": BLUE,
         "icon_color": RED, "icon_active_color": BLUE,
         "title_typography_typography": "custom",
         "title_typography_font_family": FONT,
         "title_typography_font_size": _rem(1.25),
         "title_typography_font_weight": "500",
         "content_typography_typography": "custom",
         "content_typography_font_family": FONT,
         "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1",
                          "left": "1", "isLinked": True},
         "border_color": GREY,
         "__globals__": {"tab_active_color": G["primary"], "icon_color": G["secondary"]}}
    return E.widget("accordion", s)


def review_band():
    """Dashed off-white band wrapping the Trustindex Google-review widget."""
    shortcode = E.widget("shortcode", {
        "shortcode": T["reviews"]["trustindex_shortcode"],
        "_background_background": "classic",
        "__globals__": {"_background_color": G["white"]},
        "_padding": _pad(15, 25, 25, 25),
        "_border_radius": _rad(15),
    })
    return E.container({
        "content_width": "full", "flex_direction": "column", "flex_gap": _gap(6),
        "flex_align_items": "center",
        "background_background": "classic",
        "__globals__": {"background_color": G["offwhite"]},
        "background_color": T["bands"]["mist"],
        "border_border": "dashed",
        "border_width": {"unit": "px", "top": "2", "right": "2", "bottom": "2",
                         "left": "2", "isLinked": True},
        "border_color": GREY,
        "border_radius": _rad(20), "padding": _pad(30, 24, 30, 24),
    }, [shortcode])


def stat_trio(items):
    """Three centred white stat cards: (fa icon value, number, label)."""
    return row([stat_card(v, n, l) for v, n, l in items],
               gap=20, align="stretch", wrap=True, justify="center")


# ---- composed sections ----
def hero(title, city, subline, cta_text, cta_url=None):
    return sec(GRADIENT, [h1(title, city), hero_sub(subline),
                          btn(cta_text, cta_url, align="center")],
               pad=SEC["hero_pad"], gap=16, align="center", hero=True)


def cta_section(heading, paragraph, cta_text, cta_url=None, bg=None):
    return sec(MISTB if bg is None else bg,
               [h2(heading, align="center"), body_center(paragraph),
                btn(cta_text, cta_url, align="center")],
               align="center")


def page(title, sections):
    return E.wrap_page(title, sections, dict(T["page_settings"]))


def write(doc, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return path
