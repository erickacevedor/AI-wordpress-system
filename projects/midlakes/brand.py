# -*- coding: utf-8 -*-
"""
Mid Lakes — site-wide brand layer over scripts/elementor_builder.py.

Site-wide, like tokens.json and skills/: it encodes the component vocabulary of the
HTML prototype at D:/laragon/www/midlakes/public ONCE, so every page assembles from
the same parts instead of re-deriving them. Per-page build.py files import this and
supply only copy + section order.

Everything reads its values from ../tokens.json and ../media.json — no brand constant
is typed twice. Structural + responsive correctness still comes from elementor_builder.

    import brand as B                 # after sys.path.insert(0, SITE)
    B.reset(0x40000000)
    S = [B.hero(...), B.sec(B.WHITE, [...]), ...]
    B.write(B.page("Home", S), "home.json")

═══════════════════════════════════════════════════════════════════════════════
THE THREE SILENT FOOTGUNS — all three are handled here, so pages never hit them
═══════════════════════════════════════════════════════════════════════════════

1. The button background key is `background_color`, NOT `button_background_color`.
   A wrong key does not error; it falls through to var(--e-global-color-accent),
   which on this stock kit is Hello Elementor's default. See _BTN.

2. E.heading(size=…) defaults to unit="px". A heading meant to be 2.4rem renders at
   2.4 PIXELS. Every helper here passes unit="rem" explicitly.
   ⚠️ E.button() is worse: its unit is HARDCODED "px", so the button's 0.95rem has to
   be handed over as 15.2px. See _BTN.

3. typography_font_size_mobile alone emits NO CSS — Elementor only writes a typography
   group when typography_typography:"custom" is present, and E._typo() sets that flag
   only when `font` or `size` is given. The h1/h2 recipe gives neither. See h1()/h2().

═══════════════════════════════════════════════════════════════════════════════
ONE OWNER PER PROPERTY
═══════════════════════════════════════════════════════════════════════════════

The child theme (theme/mid-lakes/assets/mid-lakes.css) owns exactly:
    h1/h2 desktop font-size (clamp)     .ml-h1 / .ml-h2
    Fraunces family+style+weight        .ml-serif / .ml-why-num / .ml-step-num
    the button's hover transform        .ml-btn
    the card's hover transform          .ml-card
    the two 3-stop photo overlays       .ml-hero / .ml-comfort
    the six watermark pseudo-elements   .ml-wm-*
    the rate table                      .ml-rate-table
    :focus-visible rings                (pseudo-class, no Elementor control)

NOTHING in this file may emit any of those properties. Everything else is Elementor's.
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
M = json.load(open(os.path.join(SITE, "media.json"), encoding="utf-8"))

# ---- brand constants, all sourced from tokens.json -------------------------
R = {k: v["hex"] for k, v in T["roles"].items()}

BLUE       = R["blue"]            # #2540af  brand primary
RED        = R["red"]             # #c10a0a  CTA / action
RED_DARK   = R["red-dark"]        # #a30808  button hover only
RED_TEXT   = R["red-text"]        # #c10a0a  red as TEXT on light
RED_DARKBG = R["red-on-dark"]     # #ff8b8b  red as TEXT on navy  (NEVER #c10a0a there)
BLUE_DARKBG = R["blue-on-dark"]   # #6fb3ec  blue as TEXT on navy
SKY        = R["sky"]             # #4a9be5
INK        = R["ink"]             # #0f1f35  dark surface
INK2       = R["ink-2"]           # #17293f  raised card on dark
TEXT       = R["text"]            # #1a2436
MUTED      = R["muted"]           # #5a6472  light-band muted
GRAY_DARKBG = R["gray"]           # #8fb2d8  meta text on navy ONLY
LINE       = R["gray-line"]       # #dde3ec
PAPER_HEX  = R["paper"]           # #f4f6f9
WHITE_HEX  = R["white"]           # #ffffff
RED_TINT   = R["red-tint"]
BLUE_TINT  = R["blue-tint"]

FONT   = T["fonts"]["body"]                       # Manrope
SEC    = T["section"]
CARD   = T["card"]
TS     = T["type_scale"]
LINKS  = T["links"]
PHONE  = T["phone"]
FACTS  = T["facts"]
FORM   = T["form"]
CW     = T["content_width"]                       # 1200
PAD_X  = SEC["container_pad_x"]                   # 24 — .container's own padding
INNER  = CW - 2 * PAD_X                           # 1152 — usable content width

# White at the alphas the prototype uses on its dark/photo bands.
W85, W82, W80, W75, W70, W65, W60, W50, W18, W08, W04 = (
    "rgba(255,255,255,0.85)", "rgba(255,255,255,0.82)", "rgba(255,255,255,0.8)",
    "rgba(255,255,255,0.75)", "rgba(255,255,255,0.7)", "rgba(255,255,255,0.65)",
    "rgba(255,255,255,0.6)", "rgba(255,255,255,0.5)", "rgba(255,255,255,0.18)",
    "rgba(255,255,255,0.08)", "rgba(255,255,255,0.04)")

reset = E.reset_ids


# ---- small value helpers ---------------------------------------------------
def px(v):
    return {"unit": "px", "size": v, "sizes": []}


def pct(v):
    return {"unit": "%", "size": v, "sizes": []}


def rem(v):
    return {"unit": "rem", "size": v, "sizes": []}


def em(v):
    return {"unit": "em", "size": v, "sizes": []}


def gap(v, row=None):
    row = v if row is None else row
    return {"unit": "px", "size": v, "column": str(v), "row": str(row), "isLinked": v == row}


def rad(*v):
    """rad(14) or rad(t,r,b,l)."""
    if len(v) == 1:
        v = v * 4
    return {"unit": "px", "top": str(v[0]), "right": str(v[1]), "bottom": str(v[2]),
            "left": str(v[3]), "isLinked": len(set(v)) == 1}


def pad(t, r, b, l):
    return E._pad(t, r, b, l)


def margin(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def border(color, w=1, sides=None):
    """A 1px solid rule, or an asymmetric one — e.g. sides=(3,0,0,0) for .promise li."""
    t, r, b, l = sides or (w, w, w, w)
    return {"border_border": "solid",
            "border_width": {"unit": "px", "top": str(t), "right": str(r),
                             "bottom": str(b), "left": str(l),
                             "isLinked": len({t, r, b, l}) == 1},
            "border_color": color}


def shadow(h, v, blur, spread, color):
    return {"box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal": h, "vertical": v, "blur": blur,
                                      "spread": spread, "color": color}}


def img(key):
    """A media.json entry, by key. Carries the real attachment id so Elementor can
    resolve sizes and `wp elementor replace_urls` can rewrite it at go-live."""
    return M[key]


def ratio_widths(ratios, gap_px):
    """Turn a CSS `grid-template-columns: 1.4fr 1fr` + gap into flex-row percentages.

    The prototype lays its two- and three-column rows out with fr ratios; Elementor's
    flex row wants percentages. Doing the arithmetic here keeps the ratios exact and
    greppable instead of eyeballed."""
    n = len(ratios)
    avail = INNER - gap_px * (n - 1)
    total = float(sum(ratios))
    return [round(avail * (r / total) / INNER * 100, 2) for r in ratios]


# ============================================================================
# BANDS & SECTIONS
# ============================================================================
def band(hex_color):
    return {"background_background": "classic", "background_color": hex_color}


WHITE = band(WHITE_HEX)
PAPER = band(PAPER_HEX)
DARK  = band(INK)


def photo(key):
    """A photo band: the image only. The navy overlay on .ml-hero / .ml-comfort is a
    3-stop gradient the child theme owns — see mid-lakes.css §5."""
    a = img(key)
    return {"background_background": "classic",
            "background_image": {"url": a["url"], "id": a["id"], "size": "",
                                 "alt": a["alt"], "source": "library"},
            "background_position": "center center",
            "background_size": "cover",
            "background_repeat": "no-repeat",
            "overflow": "hidden"}


def sec(bg, children, pad_=None, pad_mobile=None, classes=None, box=None,
        box_classes=None, gap_=22, anchor=None):
    """Full-width band -> ONE boxed 1200px container -> children.

    `classes` lands on the outer band (backgrounds, watermarks, overlays);
    `box` merges extra settings into the boxed container;
    `anchor` puts an id on the OUTER band, so `#contact` scrolls to the top of the
    band rather than to the inset content container.
    """
    bg = dict(bg)
    if anchor:
        bg["_element_id"] = anchor
    b = {"flex_gap": gap(gap_)}
    if box:
        b.update(box)
    bg["_box"] = b
    return E.section(bg, children, content_width=CW,
                     pad=pad_ or tuple(SEC["pad"]),
                     pad_mobile=pad_mobile or tuple(SEC["pad_mobile"]),
                     classes=classes, box_classes=box_classes)


def sec_about(children, watermark=True, **kw):
    """`.about` — the white band that carries the mirrored 2.svg wave pair.

    ⚠️ Only `.about` gets the waves. `.why` is also white and has NONE — use
    sec_why(). And `.about.what-happens` suppresses them, so pass watermark=False
    there. Suppression is by OMISSION (the class simply isn't added), which is
    cleaner than the prototype's display:none override and renders identically."""
    cls = "ml-wm-waves" if watermark else None
    box = {"z_index": 1} if watermark else None   # .about .container { position: relative }
    kw.setdefault("box", box)
    return sec(WHITE, children, classes=cls, **kw)


def sec_why(children, **kw):
    """`.why` — the OTHER white band. No watermarks: in the prototype the waves are
    on `.about`, and `.why`'s decoration lives on its cards (4.svg) instead."""
    return sec_about(children, watermark=False, **kw)


# Back-compat name for "a white band"; prefer sec_about()/sec_why(), which say which.
sec_white = sec_about


def sec_paper(children, **kw):
    """.services / .faq — the paper band."""
    return sec(PAPER, children, **kw)


# ============================================================================
# TYPOGRAPHY
# ============================================================================
_HEAD = dict(weight=TS["heading_weight"], lh=TS["heading_line_height"],
             ls=TS["heading_letter_spacing"])

# Footgun 3: with size=None AND font=None, E._typo() never sets this flag, and
# Elementor then emits NO CSS for the mobile size — while responsive-audit still
# passes, because it only checks the key exists.
_CUSTOM_TYPO = {"typography_typography": "custom"}


def h1(title, color=None, align=None, classes="ml-h1"):
    """H1. The child theme owns the desktop size: clamp(2.4rem, 5.2vw, 4rem).

    We emit ONLY the mobile size, at the clamp's FLOOR (2.4rem), which is what the
    clamp resolves to below 767px anyway — so the responsive gate passes and fidelity
    is kept. No desktop size, no tablet size: above 767px the clamp is unopposed."""
    return E.heading(title, tag="h1", color=color, align=align,
                     size=None, mobile=TS["h1"]["mobile"], unit="rem",
                     extra=dict(_CUSTOM_TYPO), classes=classes, **_HEAD)


def h2(title, color=None, align=None, classes="ml-h2"):
    """H2. Same recipe; 1.8rem is EXACT below 767px (3.4vw only passes the floor
    above an 847px viewport)."""
    return E.heading(title, tag="h2", color=color, align=align,
                     size=None, mobile=TS["h2"]["mobile"], unit="rem",
                     extra=dict(_CUSTOM_TYPO), classes=classes, **_HEAD)


def h(title, step, tag="h3", color=None, align=None, extra=None, classes=None):
    """Any other heading, sized from a named step in tokens.json's type census.

    The census is NOT collapsed (PORT-DECISIONS decision 8) — `step` is the component
    that owns the size, e.g. h(txt, "card_h3") or h(txt, "detail_h3")."""
    t = TS[step]
    return E.heading(title, tag=tag, color=color, align=align,
                     size=t["size"], unit="rem", weight=t.get("weight"),
                     mobile=t["size"],           # these do not shrink in the prototype
                     lh=t.get("lh"), ls=t.get("ls"), transform=t.get("transform"),
                     extra=extra, classes=classes)


def body(html, step="base", color=None, align=None, mw=None, extra=None, classes=None):
    """A text-editor widget at a named step. `mw` caps the widget's width in px, the
    way the prototype caps .hero-sub (540), .contact-sub (460) and .lead (62ch)."""
    t = TS[step]
    ex = dict(extra or {})
    if mw:
        ex.update(_width(mw))
    return E.text(html, color=color, align=align, size=t["size"], unit="rem",
                  weight=t.get("weight"), lh=t.get("lh"), ls=t.get("ls"),
                  transform=t.get("transform"), extra=ex, classes=classes)


def lead(html, **kw):
    """.lead — 1.1rem muted. The workhorse paragraph."""
    kw.setdefault("color", MUTED)
    return body(html, "lead", **kw)


def _width(px_value):
    """Cap a WIDGET's width. Elementor containers have no max-width control, so a
    fixed px width is used at desktop+tablet and released to 100% on mobile — which
    matches `max-width` everywhere the two can differ by more than a few px."""
    return {"_element_width": "initial",
            "_element_custom_width": px(px_value),
            "_element_custom_width_mobile": pct(100)}


def col_max(children, px_value, gap_px=16, classes=None):
    """A column capped at `px_value` — .hero-copy (700), .comfort-card (560),
    .section-title (720)."""
    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": gap(gap_px),
                        "width": px(px_value),
                        "width_tablet": px(px_value),
                        "width_mobile": pct(100)}, children, classes=classes)


# ---- the eyebrow -----------------------------------------------------------
_DOT = ('<span style="display:inline-block;width:7px;height:7px;border-radius:50%%;'
        'background:%s;margin-right:8px;vertical-align:middle;"></span>')


def eyebrow(label, light=False):
    """.eyebrow — 0.72rem / 700 / 0.18em / uppercase, preceded by a 7px red dot.

    The dot is an inline-styled span inside the text widget's HTML rather than a
    second widget: it is 7px of decoration and does not deserve its own element."""
    return body(_DOT % RED + label, "eyebrow",
                color=(WHITE_HEX if light else RED_TEXT))


# ============================================================================
# BUTTONS
# ============================================================================
def _btn_spec(variant, block=False, align="left"):
    b = T["button"]
    v = b[variant]
    classes = v["class"] + (" " + b["block"]["class"] if block else "")
    return {
        "font": FONT,
        # ⚠️ E.button() hardcodes unit="px" — 0.95rem must be handed over as 15.2px.
        "size": round(b["size"] * 16, 1),
        "weight": b["weight"],
        "radius": b["radius"],
        "border_width": b["border_width"],
        "padding": b["padding"],
        "align": align,
        # NO hover_animation. The 2px lift is the child theme's (.ml-btn).
        "hover_animation": None,
        "colors": dict(v["colors"]),
        "globals": {},          # the kit is stock — a global ref renders Hello's default
        "classes": classes,
    }


def btn(text, url, variant="primary", block=False, align="left"):
    return E.button(text, url, _btn_spec(variant, block, align))


def btn_primary(text, url, **kw):
    return btn(text, url, "primary", **kw)


def btn_ghost(text, url, **kw):
    """.btn-ghost — transparent with a white hairline. Photo bands ONLY: it needs a
    dark backdrop to read."""
    return btn(text, url, "ghost", **kw)


def actions(buttons, gap_px=14):
    """.hero-actions — a wrapping flex row of buttons."""
    return E.container({"content_width": "full", "flex_direction": "row",
                        "flex_wrap": "wrap", "flex_gap": gap(gap_px),
                        "flex_direction_mobile": "column"}, buttons)


def call_btn(variant="primary", label=None):
    return btn(label or ("Call %s" % PHONE["display"]), PHONE["tel"], variant)


# ============================================================================
# HERO
# ============================================================================
def hero(image_key, title, sub, buttons, creds=None, interior=False):
    """.hero / .hero-page — photo band, copy bottom-aligned, capped at 700px.

    The navy overlay is .ml-hero::after in the child theme (3 stops; Elementor's
    gradient control has two). z_index 1 on the boxed container puts the copy above
    it, mirroring the prototype's `.hero-inner { position: relative; z-index: 1 }`."""
    inner = [h1(title, color=WHITE_HEX)]
    if sub:
        inner.append(body(sub, "hero_sub", color=W85, mw=540))
    inner.append(actions(buttons))
    if creds:
        inner.append(hero_creds(creds))

    box = {"min_height": px(SEC["hero_page_min_height"] if interior
                            else SEC["hero_min_height"]),
           "min_height_tablet": px(SEC["hero_min_height_tablet"]),
           "flex_justify_content": "flex-end",
           "z_index": 1,
           "flex_gap": gap(0)}
    return sec(photo(image_key), [col_max(inner, 700, gap_px=22)],
               pad_=tuple(SEC["hero_page_pad"] if interior else SEC["hero_pad"]),
               pad_mobile=(88, 24, 48, 24),
               classes="ml-hero", box=box)


def hero_creds(items):
    """.hero-creds — `<strong>75+</strong> Years of…` under a hairline rule.

    One text widget holding the whole list: it is a single visual unit and splitting
    it into per-item widgets would lose the `gap: 12px 36px` wrap behaviour."""
    lis = "".join(
        '<li style="margin:0;"><strong style="color:%s;font-weight:800;'
        'margin-right:6px;">%s</strong>%s</li>' % (WHITE_HEX, v, label)
        for v, label in items)
    html = ('<ul style="list-style:none;margin:0;padding:0;display:flex;'
            'flex-wrap:wrap;gap:12px 36px;">%s</ul>' % lis)
    return body(html, "base", color=W80,
                extra={"_margin": margin(34, 0, 0, 0),
                       "_padding": pad(26, 0, 0, 0),
                       "_border_border": "solid",
                       "_border_width": {"unit": "px", "top": "1", "right": "0",
                                         "bottom": "0", "left": "0", "isLinked": False},
                       "_border_color": W18})


def hero_compact(title, sub, leads=()):
    """.hero-compact — the photo-less paper header (blog index)."""
    kids = [eyebrow("Blog"), h1(title)]
    if sub:
        kids.append(body(sub, "hero_compact_sub", color=MUTED, mw=740))
    for p in leads:
        kids.append(lead(p, mw=816))
    return sec(PAPER, kids,
               pad_=tuple(SEC["hero_compact_pad"]),
               pad_mobile=tuple(SEC["hero_compact_pad_mobile"]),
               box={"flex_gap": gap(16)},
               classes=None)


# ============================================================================
# COMFORT BAND (photo + copy capped at 560)
# ============================================================================
def comfort(image_key, eyebrow_label, title, subs, perks=None, buttons=None,
            anchor=None):
    kids = [eyebrow(eyebrow_label, light=True), h2(title, color=WHITE_HEX)]
    for s in subs:
        kids.append(body(s, "base", color=W82))
    if perks:
        kids.append(check_list(perks, on_dark=True, size=20, space=14))
    if buttons:
        kids.append(actions(buttons))
    return sec(photo(image_key), [col_max(kids, 560, gap_px=18)],
               pad_=tuple(SEC["comfort_pad"]),
               pad_mobile=tuple(SEC["comfort_pad_mobile"]),
               classes="ml-comfort", box={"z_index": 1}, anchor=anchor)


# ============================================================================
# ROWS, COLUMNS, GRIDS
# ============================================================================
def row(cols, gap_px=34, align="center", reverse=False, classes=None):
    return E.row(cols, reverse=reverse, align=align, gap=gap_px, classes=classes)


def ratio_row(children, ratios, gap_px, align="flex-start", reverse=False,
              classes=None, col_gap=16):
    """A two/three-column row from the prototype's fr ratios."""
    widths = ratio_widths(ratios, gap_px)
    cols = [E.column(c if isinstance(c, list) else [c], width=w, gap=col_gap)
            for c, w in zip(children, widths)]
    return row(cols, gap_px=gap_px, align=align, reverse=reverse, classes=classes)


def grid(children, cols=3, tablet=2, mobile=1, gap_px=20, classes=None):
    return E.grid(children, cols=cols, tablet=tablet, mobile=mobile, gap=gap_px,
                  classes=classes)


def section_title(children, gap_px=14):
    """.section-title — capped at 720px with 48px of air beneath it."""
    return col_max(children, SEC["section_title_max_width"], gap_px=gap_px,
                   classes=None)


# ============================================================================
# CARDS
# ============================================================================
def card(children, bg=None, radius=None, pad_=None, gap_px=10, border_color=None,
         min_height=None, classes=None, hover=True, extra=None):
    """The base card: white, radius 14, 1px #dde3ec.

    ⚠️ `hover` gates the ENTIRE hover treatment, and it is off for most cards. In the
    prototype only `.service-card` and `.post-card` react to hover; `.why-card`,
    `.spec-card` and `.quote-form` sit still.

    When it is on: the LIFT is the child theme's (.ml-card), while the SHADOW and the
    border-colour are native Elementor container controls set here. That per-property
    split is deliberate — see mid-lakes.css §4."""
    s = {"content_width": "full", "flex_direction": "column",
         "flex_gap": gap(gap_px),
         "background_background": "classic",
         "background_color": bg or CARD["bg"],
         "border_radius": rad(radius if radius is not None else CARD["radius"]),
         "padding": pad(*(pad_ or CARD["pad"]))}
    s.update(border(border_color or CARD["border"], CARD["border_width"]))
    if min_height:
        s["min_height"] = px(min_height)
    if hover:
        h_, v, blur, spread, color = 0, 18, 40, -24, "rgba(15,31,53,0.35)"
        s.update({"box_shadow_hover_box_shadow_type": "yes",
                  "box_shadow_hover_box_shadow": {"horizontal": h_, "vertical": v,
                                                  "blur": blur, "spread": spread,
                                                  "color": color},
                  "border_color_hover": "rgba(0,0,0,0)"})
    if extra:
        s.update(extra)
    cls = " ".join(filter(None, ["ml-card" if hover else None, classes]))
    return E.container(s, children, classes=cls or None)


def service_card(index, icon, title, body_html, min_height=None):
    """.service-card — white card with a 52px tinted icon tile.

    ⚠️ ALTERNATION: .service-card:nth-child(even) .service-icon swaps red for blue.
    Elementor has no positional selector, so it is restated here from the item's
    index. `index` is 0-based: 0 red, 1 blue, 2 red, …"""
    kids = []
    if icon:
        kids.append(icon_tile(icon, index))
    kids.append(h(title, "card_h3"))
    if body_html:
        kids.append(body(body_html, "card_body", color=MUTED))
    return card(kids, min_height=min_height or CARD["min_height"],
                classes="ml-wm-card-1")


def icon_tile(name, index=0):
    """The 52px rounded tile holding a sprite glyph.

    The sprite is inlined at wp_body_open by the child theme (PORT-DECISIONS
    decision 4); this is the `html` widget that references it."""
    odd = index % 2 == 0
    ic = T["icons"]
    fill = ic["tile_odd"]["bg"] if odd else ic["tile_even"]["bg"]
    color = ic["tile_odd"]["color"] if odd else ic["tile_even"]["color"]
    svg = ('<span class="ml-icon-tile" style="display:grid;place-items:center;'
           'width:%dpx;height:%dpx;border-radius:%dpx;background:%s;color:%s;">'
           '<svg aria-hidden="true" style="display:block;width:%dpx;height:%dpx;">'
           '<use href="#ml-icon-%s"></use></svg>'
           '</span>' % (ic["tile"]["size"], ic["tile"]["size"], ic["tile"]["radius"],
                        fill, color,
                        ic["tile"]["icon_size"], ic["tile"]["icon_size"], name))
    return E.widget("html", {"html": svg,
                             "_margin": margin(0, 0, ic["tile"]["margin_bottom"], 0)})


def why_card(n, title, body_html):
    """.why-card — paper fill on the WHITE band (inverted from .service-card), with a
    Fraunces italic numeral.

    ⚠️ ALTERNATION: .why-card:nth-child(odd) .why-num is RED; the base is blue.
    `n` is the 1-based numeral as printed, so 01 red, 02 blue, 03 red, 04 blue."""
    color = RED if n % 2 == 1 else BLUE
    return card([
        h("%02d" % n, "why_num", tag="p", color=color, classes="ml-why-num"),
        h(title, "why_card_h3"),
        body(body_html, "base", color=MUTED),
    ], bg=CARD["why_card"]["bg"], pad_=CARD["why_card"]["pad"],
        min_height=CARD["min_height"], hover=False, classes="ml-wm-card-4")


def spec_card(label, items, blue=False):
    """.spec-card — the uppercase label + a check list. The --blue modifier changes
    ONLY the marker colour."""
    return card([
        body(label, "spec_label", color=MUTED),
        check_list(items, color=BLUE if blue else RED,
                   size=18, space=12, extra={"_margin": margin(16, 0, 0, 0)}),
    ], pad_=CARD["spec_card"]["pad"], gap_px=0, hover=False,
        classes="ml-wm-card-4")


def check_list(items, color=None, on_dark=False, size=18, space=12, extra=None):
    """.spec-list / .perk-list — a red disc with a knockout white check.

    fas fa-check-circle (FA Free Solid, which ships with Elementor) is the native
    stand-in: a filled circle with the check knocked out, which is exactly the
    prototype's data-URI marker."""
    ic = T["icons"]["list_check"]
    s = {
        "icon_list": [{"text": t,
                       "selected_icon": {"value": ic["value"], "library": ic["library"]},
                       "_id": E.nid()[:7]} for t in items],
        "icon_color": color or (RED if not on_dark else RED),
        "icon_size": px(size),
        "space_between": px(space),
        "text_indent": px(12),
        "text_color": WHITE_HEX if on_dark else TEXT,
        "icon_typography_typography": "custom",
        "icon_typography_font_family": FONT,
        "icon_typography_font_size": rem(0.96 if not on_dark else 1.0),
        "icon_typography_font_weight": "600" if on_dark else "400",
        "divider": "",
    }
    if extra:
        s.update(extra)
    return E.widget("icon-list", s)


# ============================================================================
# LIST-LIKE COMPONENTS
# ============================================================================
def stats(items):
    """.stats — a 2.2rem numeral over a 0.9rem label, hairline-separated.

    ⚠️ :last-child drops its rule. Elementor has no positional selector, so the last
    item is built without a border here."""
    out = []
    for i, (num, label) in enumerate(items):
        last = i == len(items) - 1
        s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0),
             "padding": pad(0, 0, 0 if last else 20, 0)}
        if not last:
            s.update(border(LINE, sides=(0, 0, 1, 0)))
        out.append(E.container(s, [
            h(num, "stat_num", tag="p", color=INK),
            body(label, "meta", color=MUTED),
        ]))
    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": gap(24), "margin": margin(6, 0, 0, 0)}, out)


def promise(items):
    """.promise — a 3px red left border per item."""
    out = []
    for title, text in items:
        s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(6),
             "padding": pad(0, 0, 0, 20)}
        s.update(border(RED, sides=(0, 0, 0, 3)))
        out.append(E.container(s, [h(title, "card_h3"),
                                   body(text, "base", color=MUTED)]))
    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": gap(28)}, out)


def steps(items):
    """.steps — 4-up, each under a 2px rule with a Fraunces italic numeral.

    ⚠️ ALTERNATION: .step:nth-child(odd) .step-num is RED, even is blue."""
    out = []
    for i, (title, paras) in enumerate(items, start=1):
        color = RED_TEXT if i % 2 == 1 else BLUE
        s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(8),
             "padding": pad(26, 0, 0, 0)}
        s.update(border(LINE, sides=(2, 0, 0, 0)))
        kids = [h(str(i), "step_num", tag="p", color=color, classes="ml-step-num"),
                h(title, "step_h3")]
        kids += [body(p, "step_body", color=MUTED) for p in paras]
        out.append(E.container(s, kids))
    return grid(out, cols=4, tablet=2, mobile=1, gap_px=26)


def area_list(items):
    """.area-list — hairline-separated rows; the last drops its rule."""
    out = []
    for i, t in enumerate(items):
        last = i == len(items) - 1
        s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0)}
        if last:
            # No rule under the last row, so its spacing is pure layout: margin, not
            # padding on a bare container. Same reasoning as detail_row()'s first row.
            s["margin"] = margin(13, 0, 13, 0)
        else:
            s["padding"] = pad(13, 0, 13, 0)
            s.update(border(LINE, sides=(0, 0, 1, 0)))
        out.append(E.container(s, [body(t, "area_item")]))
    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": gap(0)}, out)


def chips(items, note=None):
    """.chip-row — wrapping pills. One html widget: the wrap behaviour is the point,
    and 20 chips as 20 widgets would be 20 elements of pure noise."""
    lis = "".join(
        '<li style="display:inline-block;padding:9px 17px;border-radius:999px;'
        'background:%s;border:1px solid %s;font-size:0.92rem;font-weight:600;'
        'color:%s;">%s</li>' % (WHITE_HEX, LINE, TEXT, c) for c in items)
    html = ('<ul style="list-style:none;margin:0;padding:0;display:flex;'
            'flex-wrap:wrap;gap:10px;">%s</ul>' % lis)
    out = [E.widget("html", {"html": html})]
    if note:
        out.append(body(note, "base", color=MUTED,
                        extra={"_margin": margin(22, 0, 0, 0)}))
    return out


# ============================================================================
# DETAIL ROWS (the /services/ anatomy)
# ============================================================================
def detail_row(index, anchor, title, paras, cta, spec, flip=False):
    """.detail-row — 1.15fr/1fr with a top hairline.

    ⚠️ .detail-row:first-of-type drops its border and pads 8px instead of 52px.
    ⚠️ On /services/ the FLIPPED rows carry the blue spec card — that pairing is the
       pattern, not a coincidence, so `flip` drives both."""
    first = index == 0
    copy = [h(title, "detail_h3")]
    copy += [body(p, "base", color=MUTED) for p in paras]
    if cta:
        copy.append(actions([btn_primary(cta[0], cta[1])]))

    widths = ratio_widths([1.15, 1], 48)
    cols = [E.column(copy, width=widths[0], gap=12),
            E.column([spec], width=widths[1], gap=16)]
    inner = E.row(cols, reverse=flip, align="flex-start", gap=48)

    s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0),
         "_element_id": anchor}
    if first:
        # No top border on the first row, so its spacing is pure layout: margin, not
        # padding. (Padding on a bare, unbordered layout container is what the gate's
        # padding-discipline check exists to catch — and it is right to.)
        s["margin"] = margin(8, 0, 52, 0)
        s["margin_mobile"] = margin(8, 0, 36, 0)
    else:
        # A bordered row DOES need padding: the rule must sit at the row's top edge
        # with the copy inset below it, which margin cannot express.
        s["padding"] = pad(52, 0, 52, 0)
        s["padding_mobile"] = pad(36, 0, 36, 0)
        s.update(border(LINE, sides=(1, 0, 0, 0)))
    return E.container(s, [inner])


# ============================================================================
# FAQ + FIGURE
# ============================================================================
def faq(items, first_open=False):
    """The <details> list -> the nested-accordion widget (PORT-DECISIONS decision 10).

    nested-accordion ships in Elementor CORE and outputs real details/summary
    semantics, and `max_items_expended: one` reproduces the prototype's JS that keeps
    only one panel open."""
    meta, children = [], []
    for q, a in items:
        meta.append({"item_title": q, "_id": E.nid()[:7]})
        c = E.container({"_title": "item", "content_width": "full"},
                        [body(a, "base", color=MUTED)])
        c["isLocked"] = True
        children.append(c)
    s = {
        "items": meta,
        "default_state": "expanded" if first_open else "all_collapsed",
        "max_items_expended": "one",
        "title_tag": "h3",
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": rem(TS["faq_summary"]["size"]),
        "title_typography_font_weight": "700",
        "normal_title_color": TEXT,
        "hover_title_color": RED_TEXT,
        "active_title_color": TEXT,
        "normal_icon_color": RED,
        "hover_icon_color": RED,
        "active_icon_color": RED,
        "accordion_padding": pad(22, 0, 22, 0),
        "accordion_border_radius": rad(0),
        "content_padding": pad(0, 0, 22, 0),
        "accordion_item_title_space_between": px(20),
        "accordion_item_title_distance_from_content": px(14),
    }
    return E.widget("nested-accordion", s, children)


def figure(image_key, caption_title=None, caption_body=None, ratio="4/5"):
    """.faq-media — a 4:5 photo with an optional bottom-anchored gradient caption.

    One html widget, because the caption is absolutely positioned over the image and
    Elementor cannot stack a widget on a widget without a positioning hack that would
    be far more fragile than this markup."""
    a = img(image_key)
    cap = ""
    if caption_title or caption_body:
        cap = ('<figcaption style="position:absolute;left:0;right:0;bottom:0;'
               'padding:22px;background:linear-gradient(180deg,transparent,'
               'rgba(15,31,53,0.9));color:%s;font-size:0.9rem;line-height:1.5;">'
               '%s%s</figcaption>'
               % (WHITE_HEX,
                  ('<strong style="display:block;font-size:1.05rem;margin-bottom:4px;">'
                   '%s</strong>' % caption_title) if caption_title else "",
                  caption_body or ""))
    html = ('<figure class="ml-figure" style="position:relative;margin:0;'
            'border-radius:%dpx;overflow:hidden;">'
            '<img src="%s" alt="%s" loading="lazy" style="display:block;width:100%%;'
            'height:100%%;object-fit:cover;aspect-ratio:%s;" />%s</figure>'
            % (CARD["radius"], a["url"], a["alt"], ratio, cap))
    return E.widget("html", {"html": html})


def gallery(main_key, tall_key):
    """.gallery — a 1.4fr/1fr pair of aspect-ratio photos. The tall one goes 3/5 ->
    16/10 on mobile, which is a media query inside the widget's own markup."""
    a, b = img(main_key), img(tall_key)
    widths = ratio_widths([1.4, 1], 16)
    html = (
        '<style>@media(max-width:620px){.ml-gallery{grid-template-columns:1fr!important}'
        '.ml-gallery img:last-child{aspect-ratio:16/10!important}}</style>'
        '<div class="ml-gallery" style="display:grid;grid-template-columns:%s%% %s%%;'
        'gap:16px;">'
        '<img src="%s" alt="%s" loading="lazy" style="border-radius:%dpx;width:100%%;'
        'height:100%%;object-fit:cover;aspect-ratio:4/5;" />'
        '<img src="%s" alt="%s" loading="lazy" style="border-radius:%dpx;width:100%%;'
        'height:100%%;object-fit:cover;aspect-ratio:3/5;" />'
        '</div>' % (widths[0], widths[1], a["url"], a["alt"], CARD["radius"],
                    b["url"], b["alt"], CARD["radius"]))
    return E.widget("html", {"html": html})


# ============================================================================
# THE CONTACT BAND + FORM
# ============================================================================
def contact(title, subs, details, form_widget, anchor="contact"):
    """.contact — the ink band that closes every page.

    ⚠️ On this band red text MUST be #ff8b8b and blue #6fb3ec. #c10a0a on #0f1f35 is
    2.62:1."""
    copy = [h2(title, color=WHITE_HEX)]
    copy += [body(s, "base", color=W75, mw=460) for s in subs]
    if details:
        copy.append(contact_details(details))
    widths = ratio_widths([1, 1.05], 56)
    inner = E.row([E.column(copy, width=widths[0], gap=18),
                   E.column([form_widget], width=widths[1], gap=16)],
                  align="flex-start", gap=56)
    return sec(DARK, [inner], classes="ml-wm-contact ml-band-ink",
               box={"z_index": 1}, anchor=anchor)


def contact_details(items):
    """.contact-details — a <dl>. One html widget: dt/dd is the correct semantics and
    Elementor has no definition-list widget."""
    rows = ""
    for label, value, sub in items:
        rows += (
            '<div style="margin:0;">'
            '<dt style="font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;'
            'color:%s;font-weight:700;margin-bottom:6px;">%s</dt>'
            '<dd style="margin:0;font-size:1.1rem;font-weight:600;color:%s;">%s%s</dd>'
            '</div>' % (
                BLUE_DARKBG, label, WHITE_HEX, value,
                ('<span style="display:block;font-size:0.85rem;font-weight:400;'
                 'color:%s;margin-top:4px;">%s</span>' % (GRAY_DARKBG, sub)) if sub else ""))
    html = ('<dl style="display:grid;gap:26px;margin:0;">%s</dl>' % rows)
    return E.widget("html", {"html": html,
                             "_margin": margin(36, 0, 0, 0)})


def phone_link(label=None):
    return ('<a href="%s" style="color:%s;">%s</a>'
            % (PHONE["tel"], RED_DARKBG, label or PHONE["display"]))


def quote_form(heading=None):
    """The Elementor Pro Form on the #17293f card.

    PORT-DECISIONS decision 1: the SAME form appears on all six pages, so it is built
    once here rather than six times. Recipient, honeypot and the inline success
    message all come from tokens.json.

    Every field keeps a REAL label — the prototype never lets a placeholder stand in
    for one, and neither does this."""
    f = FORM
    fields = []
    for fd in f["fields"]:
        item = {
            "custom_id": fd["name"],
            "field_label": fd["label"],
            "placeholder": fd["placeholder"],
            "field_type": fd["type"],
            "width": str(fd["width"]),
            "required": "true" if fd["required"] else "",
            "_id": E.nid()[:7],
        }
        if fd["type"] == "textarea":
            item["rows"] = fd["rows"]
        fields.append(item)

    s = {
        "form_name": "Mid Lakes Quote Request",
        "form_fields": fields,
        "button_text": f["submit_label"],
        "button_size": "sm",
        "button_width": "100",
        "submit_actions": ["email"],
        "email_to": f["recipient"],
        "email_subject": "New estimate request — Mid Lakes HVAC",
        "email_content": "[all-fields]",
        "email_from_name": "Mid Lakes Website",
        "email_reply_to": "[field id=\"email\"]",
        "success_message": f["success_text"],
        # Anti-spam: Elementor's built-in honeypot. No third-party keys to obtain and
        # nothing to configure at go-live.
        "honeypot": "yes",
        # --- field styling, from .field / .field input in styles.css ---
        "label_spacing": px(7),
        "row_gap": px(16),
        "column_gap": px(16),
        "label_color": W70,
        "field_typography_typography": "custom",
        "field_typography_font_family": FONT,
        "field_typography_font_size": rem(0.95),
        "label_typography_typography": "custom",
        "label_typography_font_family": FONT,
        "label_typography_font_size": rem(TS["field_label"]["size"]),
        "label_typography_font_weight": "600",
        "field_background_color": W04,
        "field_text_color": WHITE_HEX,
        "field_border_color": "rgba(255,255,255,0.4)",
        "field_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1",
                               "left": "1", "isLinked": True},
        "field_border_radius": rad(10),
        "field_padding": pad(13, 15, 13, 15),
        "button_background_color": RED,
        "button_text_color": WHITE_HEX,
        "button_border_color": RED,
        "button_border_border": "solid",
        "button_border_width": {"unit": "px", "top": "1.5", "right": "1.5",
                                "bottom": "1.5", "left": "1.5", "isLinked": True},
        "button_border_radius": rad(999),
        "button_background_hover_color": RED_DARK,
        "button_hover_border_color": RED_DARK,
        "button_text_color_hover": WHITE_HEX,
        "button_typography_typography": "custom",
        "button_typography_font_family": FONT,
        "button_typography_font_size": rem(0.95),
        "button_typography_font_weight": "700",
        "button_padding": pad(14, 26, 14, 26),
    }
    form = E.widget("form", s, classes="ml-form ml-btn")

    return card([
        h(heading or f["heading"], "form_h3", color=WHITE_HEX),
        body(f["intro"], "small", color=W65),
        form,
    ], bg=CARD["form_card"]["bg"], border_color=CARD["form_card"]["border"],
        pad_=CARD["form_card"]["pad"], gap_px=6, hover=False,
        extra={"padding_mobile": pad(*CARD["form_card"]["pad_mobile"])})


# ============================================================================
# ONE-OFF COMPONENTS
# ============================================================================
def rate_table(rows, headers):
    """The rate card, shipped as ONE html widget.

    Elementor has no table widget, and the <620px behaviour — hide the header row,
    turn each row into a card — is pure CSS. The child theme's .ml-rate-table owns
    every style here, so this widget emits markup and nothing else."""
    thead = "".join('<th scope="col">%s</th>' % h_ for h_ in headers)
    tbody = ""
    for label, amount, detail in rows:
        tbody += ('<tr><th scope="row">%s</th>'
                  '<td class="rate-amount">%s</td><td>%s</td></tr>'
                  % (label, amount, detail))
    html = ('<div class="ml-rate-table-wrap"><table class="ml-rate-table">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (thead, tbody))
    return E.widget("html", {"html": html})


def gmap(anchor_title=None):
    """The /service-area/ iframe -> the Google Maps widget (decision 11)."""
    inner = E.widget("google_maps", {
        "address": FACTS["address"],
        "zoom": {"unit": "px", "size": 14, "sizes": []},
        "height": px(420),
        "height_mobile": px(320),
    })
    return E.container({"content_width": "full", "flex_direction": "column",
                        "flex_gap": gap(0),
                        "background_background": "classic",
                        "background_color": WHITE_HEX,
                        "border_radius": rad(CARD["radius"]),
                        "overflow": "hidden",
                        **border(LINE)}, [inner])


def section_nav(items):
    """.section-nav — the sticky in-page anchor bar on /services/.

    Sticky at top:76px (the header's height). One html widget: it is a horizontally
    scrolling link row, and 6 link widgets would not scroll as one."""
    links = "".join(
        '<li><a href="%s" style="display:block;padding:15px 16px;white-space:nowrap;'
        'font-size:0.9rem;font-weight:600;color:%s;border-bottom:2px solid transparent;'
        'text-decoration:none;">%s</a></li>' % (href, MUTED, label)
        for label, href in items)
    html = ('<nav aria-label="Services on this page">'
            '<ul style="display:flex;gap:2px;list-style:none;margin:0;padding:0;'
            'overflow-x:auto;">%s</ul></nav>' % links)
    return sec({"background_background": "classic",
                "background_color": "rgba(244,246,249,0.94)",
                **border(LINE, sides=(0, 0, 1, 0))},
               [E.widget("html", {"html": html})],
               pad_=(0, 24, 0, 24), pad_mobile=(0, 24, 0, 24),
               box={"flex_gap": gap(0)})


def legal(text):
    """.legal — the financing fine print."""
    return sec({**PAPER, **border(LINE, sides=(1, 0, 0, 0))},
               [body(text, "fine", color=MUTED, mw=900)],
               pad_=tuple(SEC["legal_pad"]), pad_mobile=(24, 24, 28, 24),
               box={"flex_gap": gap(0)})


# ============================================================================
# HEADER / FOOTER PARTS  (pages/_theme/)
# ============================================================================
# The two logos and the four watermarks are child-theme assets, not media-library
# attachments: WordPress blocks SVG uploads by default and this keeps them in git.
# Root-relative, so the path survives the go-live domain change untouched.
THEME_ASSETS = "/wp-content/themes/mid-lakes/assets/"


def logo(white=False, height=48, href="/"):
    """The stacked wordmark lockup. An `html` widget rather than an `image` widget
    because the asset is an SVG living in the theme — see THEME_ASSETS."""
    a = T["images"]["logo_white" if white else "logo"]
    return E.widget("html", {"html":
        '<a href="%s" aria-label="Mid Lakes Heating and Cooling home" '
        'style="display:inline-block;line-height:0;">'
        '<img src="%s%s" alt="%s" width="%d" height="%d" '
        'style="height:%dpx;width:auto;display:block;" /></a>'
        % (href, THEME_ASSETS, a["file"], a["alt"], a["w"], a["h"], height)})


def nav_menu(menu_slug, vertical=False, dropdown="tablet_extra"):
    """The Pro Nav Menu widget.

    ⚠️ `dropdown` names an ACTIVE breakpoint. The prototype collapses its primary nav
    at exactly 1200px — seven links plus the phone run out of room well before the
    page grid does — so tools/set-kit-defaults.php turns on Elementor's tablet_extra
    breakpoint at 1200 for this one purpose."""
    s = {
        "menu": menu_slug,
        "layout": "vertical" if vertical else "horizontal",
        "pointer": "none",
        "menu_typography_typography": "custom",
        "menu_typography_font_family": FONT,
        "menu_typography_font_size": rem(0.95),
        "menu_typography_font_weight": "600",
        "color_menu_item": W80 if vertical else INK,
        "color_menu_item_hover": RED_DARKBG if vertical else RED_TEXT,
        "color_menu_item_active": RED_TEXT,
        "padding_horizontal_menu_item": px(0),
        "padding_vertical_menu_item": px(0),
        # ⚠️ Without this a widget in a flex ROW defaults to width:100% and fights its
        # siblings for space — the nav then wraps onto three lines while the phone and
        # the button get a third of the bar each. `auto` sizes it to its content.
        "_element_width": "auto",
    }
    if vertical:
        s["menu_space_between"] = px(12)
        s["align_items"] = "left"
    else:
        s.update({
            # styles.css @media (max-width:1400px) tightens the nav BEFORE collapsing
            # it, because seven links plus the phone stop fitting well above the
            # collapse point. `laptop` is that breakpoint, set to 1400 in
            # tools/set-kit-defaults.php.
            "menu_space_between": px(28),
            "menu_space_between_laptop": px(18),
            "menu_typography_font_size_laptop": rem(0.9),
            "dropdown": dropdown,
            # The collapsed panel, from @media (max-width: 1200px) in styles.css.
            "color_dropdown_item": INK,
            "background_color_dropdown_item": PAPER_HEX,
            "color_dropdown_item_hover": RED_TEXT,
            "padding_horizontal_dropdown_item": px(0),
            "padding_vertical_dropdown_item": px(14),
            "dropdown_divider_width": px(1),
            "dropdown_divider_color": LINE,
            "toggle_size": px(24),
            "toggle_color": INK,
        })
    return E.widget("nav-menu", s, classes=None if vertical else "ml-nav")


def nav_phone():
    """`.nav-phone` — a red 700 tel: link INSIDE the nav row.

    ⚠️ Deliberately NOT a menu item (see ENVIRONMENT.md): it is a styled link, and a
    menu item would land in the footer menu too."""
    return body('<a href="%s" style="color:%s;font-weight:700;text-decoration:none;'
                'white-space:nowrap;">%s</a>' % (PHONE["tel"], RED_TEXT, PHONE["display"]),
                "base", extra={"_element_width": "auto"})


def header_bar():
    """The sticky header. `.site-header` — translucent paper, blurred, hairline base.

    Sticky (Pro Motion Effects) and the backdrop blur (the CSS Filters control) are
    both native, so nothing here reaches into the capped stylesheet."""
    # `.header-cta { display: none }` below 1200px. The hide controls live on the
    # BUTTON — a wrapper container would default to width:100% and squeeze the row.
    cta = btn_primary("Get a Free Estimate", LINKS["contact"])
    cta["settings"].update({
        "_element_width": "auto",
        "hide_tablet_extra": "hidden-tablet_extra",
        "hide_tablet": "hidden-tablet",
        "hide_mobile": "hidden-mobile",
    })

    right = E.container({
        "content_width": "full", "flex_direction": "row",
        "flex_align_items": "center", "flex_gap": gap(20),
        "flex_direction_mobile": "row",     # deliberate: nav + hamburger stay a row
        "flex_justify_content": "flex-end",
        "flex_wrap": "nowrap",
        # No `width`: it sizes to its content and `bar`'s space-between pushes it
        # right, which is what `.main-nav { margin-left: auto }` does in the prototype.
    }, [nav_menu("main-menu"), nav_phone(), cta])

    bar = E.container({
        "content_width": "full", "flex_direction": "row",
        "flex_align_items": "center", "flex_justify_content": "space-between",
        "flex_gap": gap(24), "flex_direction_mobile": "row",
    }, [
        E.container({"content_width": "full", "flex_direction": "column",
                     "flex_gap": gap(0), "width": px(134), "width_mobile": px(120),
                     "flex_shrink": "0"},
                    [logo()]),
        right,
    ])

    bg = {
        "background_background": "classic",
        "background_color": "rgba(244,246,249,0.92)",
        "z_index": 50,
        "sticky": "top",
        "sticky_on": ["desktop", "tablet", "mobile"],
        "sticky_offset": 0,
    }
    bg.update(border(LINE, sides=(0, 0, 1, 0)))
    # ⚠️ The translucent fill above is HALF the effect. `backdrop-filter: blur(10px)`
    # is the other half, and Elementor has no control for it — its CSS Filters group
    # emits `filter:`, which would blur the header's own CONTENTS instead of what is
    # behind them. So the blur is the child theme's, on .ml-header. Verified: passing
    # css_filters_* here emitted no CSS at all.
    return sec(bg, [bar], pad_=(0, 24, 0, 24), pad_mobile=(0, 24, 0, 24),
               box={"min_height": px(SEC["header_height"]),
                    "flex_justify_content": "center", "flex_gap": gap(0)},
               classes="ml-header", anchor="top")


FOOTER_BLURB = ("Family-owned heating, cooling, and home efficiency experts serving "
                "Loganville, GA and surrounding areas.")


def footer_bar():
    """`.site-footer` — the ink band that closes every page.

    ⚠️ The 300px bottom padding exists ONLY to clear .ml-footer::after (1.svg at 10%
    opacity). Drop the watermark and this goes with it, or the footer is left with
    dead space."""
    widths = ratio_widths([1.6, 1, 1], 40)

    brand_col = [logo(white=True, height=64),
                 body(FOOTER_BLURB, "base", color=W70, mw=340)]

    contact_col = [
        body('<a href="%s" style="color:%s;font-weight:800;text-decoration:none;">%s</a>'
             % (PHONE["tel"], WHITE_HEX, PHONE["display"]), "footer_phone"),
        body(FACTS["address"], "small", color=W70),
    ]

    inner = E.row([
        E.column(brand_col, width=widths[0], gap=18),
        E.column([nav_menu("footer-menu", vertical=True)], width=widths[1], gap=12),
        E.column(contact_col, width=widths[2], gap=10),
    ], align="flex-start", gap=40)
    inner["settings"]["margin"] = margin(0, 0, 48, 0)

    bottom_s = {
        "content_width": "full", "flex_direction": "row",
        "flex_wrap": "wrap", "flex_justify_content": "space-between",
        "flex_gap": gap(16), "flex_direction_mobile": "column",
        "padding": pad(22, 0, 22, 0),
    }
    bottom_s.update(border(W08, sides=(1, 0, 0, 0)))
    bottom = E.container(bottom_s, [
        # [ml_year] is a child-theme shortcode standing in for the prototype's
        # <span id="year"> + JS. Elementor's text-editor runs do_shortcode().
        body("&copy; [ml_year] Mid Lakes Heating &amp; Cooling, LLC. All rights "
             "reserved.", "fine", color=GRAY_DARKBG),
        body('Powered by <a href="%s" target="_blank" rel="noopener" '
             'style="color:rgba(255,255,255,0.85);font-weight:700;'
             'text-decoration:none;">ExploreHVAC</a>'
             % LINKS["external"]["powered_by"], "fine", color=GRAY_DARKBG),
    ])

    bg = dict(DARK)
    bg.update(border(W08, sides=(1, 0, 0, 0)))
    return sec(bg, [inner, bottom],
               pad_=tuple(SEC["footer_pad"]),
               pad_mobile=(48, 24, 240, 24),
               classes="ml-footer ml-band-ink",
               box={"flex_gap": gap(0)})


def theme_part(title, sections, part_type):
    """A Theme Builder part. Validates as type header/footer, which the gate treats as
    a page that must NOT contain an H1."""
    doc = E.wrap_page(title, sections, {"template": "elementor_header_footer"})
    doc["type"] = part_type
    return doc


# ============================================================================
# PAGE WRAPPER
# ============================================================================
PAGE_SETTINGS = dict(T["page_settings"])


def page(title, sections, settings=None):
    return E.wrap_page(title, sections, settings or dict(PAGE_SETTINGS))


def write(doc, filename, folder=None):
    """Write the page JSON beside its build.py. UTF-8, no elisions, newline at EOF."""
    path = os.path.join(folder or os.getcwd(), filename)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote %s (%d bytes)" % (path, os.path.getsize(path)))
    return path
