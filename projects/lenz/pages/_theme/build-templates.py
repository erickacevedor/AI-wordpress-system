#!/usr/bin/env python3
"""
Lenz — Theme Builder parts: header (v4 light bar) and footer.

v4's defining choice is the header: the colourful body keeps v1's navy/gradient
weight, but the top bar is a clean cream/white surface so the site reads friendly
rather than corporate. Financing is promoted to the single gold accent in the bar.

Run:  python projects/lenz/pages/_theme/build-templates.py
Then: python scripts/validate-page.py projects/lenz/pages/_theme/header.json
      python scripts/validate-page.py projects/lenz/pages/_theme/footer.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_root(p):
    while p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, "AGENTS.md")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repo root not found")


ROOT = _find_root(HERE)
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E  # noqa: E402

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))
MEDIA = json.load(open(os.path.join(SITE, "media.json"), encoding="utf-8"))

C = {k: v["hex"] for k, v in T["roles"].items()}
G = {k: v["global"] for k, v in T["roles"].items() if v.get("global")}
F, NAP, L = T["fonts"], T["nap"], T["links"]
PHONE_TEL, PHONE = NAP["phone"]["tel"], NAP["phone"]["display"]
CREAM, NAVY, WHITE = C["bg-cream"], C["dark-bg"], "#FFFFFF"


def svg(name, cls="lenz-icon"):
    return '<svg class="%s" aria-hidden="true"><use href="#%s"/></svg>' % (cls, name)


def html(markup, classes=None):
    return E.widget("html", {"html": markup}, classes=classes)


def band(color, glob=None):
    s = {"background_background": "classic", "background_color": color}
    if glob:
        s["__globals__"] = {"background_color": glob}
    return s


def url(u):
    return {"url": u, "is_external": "", "nofollow": "", "custom_attributes": ""}


def img_url(name):
    u = MEDIA[name]["url"]
    return "/wp-content/" + u.split("/wp-content/", 1)[-1] if "/wp-content/" in u else u


# ============================================================== HEADER =======
E.reset_ids(0x20000000)

# ---- 1. OFFER BAR — 28px, static, scrolls away (NOT sticky) ----------------
# Seasonal copy is swapped at runtime by lenz-core's offer-bar script; the summer
# set ships in the markup so the bar is never empty with JS disabled.
offer_bar = E.section(
    band("#692007"),  # season-summer-bg (orange-800). JS re-skins via data-season.
    [html(
        '<div class="lenz-offer-bar__inner">'
        '<span class="lenz-offer-bar__msg">AC out? We&rsquo;re on it — 24/7, 365.</span>'
        '<a class="lenz-offer-bar__cta" href="%s">'
        '<span class="lenz-offer-bar__cta-label">Call now</span>%s</a>'
        '</div>' % (PHONE_TEL, svg("i-phone", "lenz-icon-xs")),
        classes="lenz-offer-bar__wrap")],
    pad=(0, 20, 0, 20), pad_mobile=(0, 18, 0, 18),
    classes="lenz-offer-bar", box_classes="lenz-offer-bar__box",
)

# ---- 2. NAV — v4's light cream bar -----------------------------------------
# The four sitemap categories and their eighteen sub-services. This dropdown must
# stay in sync with the services grid and the footer — the accepted cost of the
# hand-assembled decision.
MEGA_COLS = [
    ("Air Conditioning", [
        ("AC Installation", "/services/air-conditioning/ac-installation/"),
        ("AC Repair", "/services/air-conditioning/ac-repair/"),
        ("AC Maintenance", "/services/air-conditioning/ac-maintenance/"),
        ("AC Replacement", "/services/air-conditioning/ac-replacement/"),
    ]),
    ("Heating", [
        ("Heating Installation", "/services/heating/heating-installation/"),
        ("Heating Repair", "/services/heating/heating-repair/"),
        ("Heating Maintenance", "/services/heating/heating-maintenance/"),
        ("Heating Replacement", "/services/heating/heating-replacement/"),
    ]),
    ("Indoor Air Quality", [
        ("Humidity Control", "/services/indoor-air-quality/humidity-control/"),
        ("UV Light Purification", "/services/indoor-air-quality/uv-light-purification/"),
        ("Indoor Purification", "/services/indoor-air-quality/indoor-purification/"),
        ("Duct Cleaning", "/services/indoor-air-quality/duct-cleaning/"),
    ]),
    ("Additional Services", [
        ("Thermostat Services", "/services/additional-services/thermostat-services/"),
        ("Water Heater Services", "/services/additional-services/water-heater-services/"),
        ("Ductwork", "/services/additional-services/ductwork/"),
        ("Gas Lines", "/services/additional-services/gas-lines/"),
        ("Heat Pumps", "/services/additional-services/heat-pumps/"),
    ]),
]

mega_panel_html = '<div class="lenz-mega__inner">'
for title, items in MEGA_COLS:
    mega_panel_html += '<div class="lenz-mega__col"><p class="lenz-mega__col-title">%s</p><ul class="lenz-mega__list">' % title
    for name, href in items:
        mega_panel_html += '<li><a href="%s">%s</a></li>' % (href, name)
    mega_panel_html += "</ul></div>"
mega_panel_html += "</div>"

# "Services" is a LABEL, not a link — it has no href and must never navigate.
NAV_ITEMS = [
    ("Services", None, "yes"),
    ("Maintenance Plans", L["plans"], "no"),
    ("Specials", L["specials"], "no"),
    ("Financing", L["financing"], "no"),   # styled as the gold pill, by href, in CSS
    ("Service Areas", L["area"], "no"),
    ("About Us", L["about"], "no"),
    ("Contact Us", L["contact"], "no"),
]

menu_items, mega_children = [], []
for i, (label, href, has_dd) in enumerate(NAV_ITEMS):
    item = {"_id": "lznav%d" % i, "item_title": label, "item_dropdown_content": has_dd}
    item["item_link"] = url(href) if href else url("")
    menu_items.append(item)
    # children map 1:1 with menu_items BY INDEX — every item needs a container even
    # when it has no dropdown, or the panels attach to the wrong labels.
    kids = [html(mega_panel_html, classes="lenz-mega")] if has_dd == "yes" else []
    child = E.container({"_title": label, "content_width": "full"}, kids)
    child["isLocked"] = True
    mega_children.append(child)

# Spacing is set HERE, not in the stylesheet. Elementor emits an element-scoped rule
# for `menu_item_title_space_between` that outranks a plain class selector, so a CSS
# override silently loses — and the editor's own spacing control would then appear to
# do nothing. Same reasoning as the trust bar: whatever Elementor can express, let it.
# 4px matches the source nav and is what makes seven items fit the 1140px box.
mega_menu = E.widget("mega-menu", {
    "menu_name": "Primary",
    "menu_items": menu_items,
    "item_layout": "horizontal",
    "open_on": "hover",
    "menu_item_title_space_between": {"unit": "px", "size": 4, "sizes": []},
    "menu_item_title_space_between_tablet": {"unit": "px", "size": 4, "sizes": []},
    "menu_item_title_space_between_mobile": {"unit": "px", "size": 0, "sizes": []},
}, mega_children, classes="lenz-nav__menu")

nav_row = E.container(
    # gap 12, not Elementor's default: the boxed container is 1140px at EVERY viewport,
    # so the bar has a fixed budget and no breakpoint can widen it. Logo + seven items
    # + CTA only fits once the row gap, the menu item padding (6px, in CSS) and the CTA
    # padding are all tightened — and the phone moves to the offer bar. Measured on the
    # render, not estimated; see the note above .lenz-nav__phone-wrap.
    {"content_width": "full", "flex_direction": "row",
     "flex_direction_mobile": "row",
     "flex_align_items": "center",
     "flex_gap": {"unit": "px", "size": 12, "column": "12", "row": "12"}},
    [
        html('<a class="lenz-nav__logo" href="/" aria-label="Lenz Heating &amp; Cooling — home">'
             '<img src="%s" width="2080" height="749" alt="Lenz Heating &amp; Cooling" /></a>'
             % img_url("lenz-logo-new-dark"), classes="lenz-nav__logo-wrap"),
        mega_menu,
        # No spacer element — the phone block takes `margin-inline-start:auto` in CSS.
        # An empty flex container here would just be a widget the client can delete
        # by accident and then wonder why the bar collapsed.
        html('<a class="lenz-nav__phone" href="%s">%s%s</a>'
             % (PHONE_TEL, svg("i-phone", "lenz-icon-sm"), PHONE),
             classes="lenz-nav__phone-wrap"),
        E.button("Free Estimate", L["cta"], {
            "font": F["button"], "weight": "700", "size": 13, "align": "right",
            "radius": 999, "border_width": 2, "padding": [0, 14, 0, 14],
            "classes": "lenz-btn lenz-btn--primary lenz-nav__cta",
        }),
    ],
    classes="lenz-nav__inner")

nav = E.section(
    band(CREAM, G.get("bg-cream")),
    [nav_row],
    pad=(8, 20, 8, 20), pad_mobile=(8, 18, 8, 18),
    classes="lenz-nav", box_classes="lenz-nav__box",
)

header = {
    "version": "0.4", "title": "Lenz Header (v4 light)", "type": "header",
    "content": [offer_bar, nav],
    "page_settings": {"template": "default"},
}

# ============================================================== FOOTER =======
E.reset_ids(0x30000000)


_LINK_SEQ = [0]


def link_list(items):
    """Elementor icon-list — a real editable widget rather than raw markup, so the
    client can reorder and relabel footer links without touching HTML.

    Repeater `_id`s must be unique across the whole document, not just within one
    list, hence the running counter."""
    rows = []
    for text, href in items:
        _LINK_SEQ[0] += 1
        rows.append({
            "_id": "lzf%03d" % _LINK_SEQ[0],
            "text": text,
            "link": url(href),
            "selected_icon": {"value": "", "library": ""},
        })
    return E.widget("icon-list", {
        "icon_list": rows,
        "space_between": {"unit": "px", "size": 8, "sizes": []},
    }, classes="lenz-footer__list")


nap_html = (
    '<a class="lenz-footer__logo" href="/"><img src="%s" width="2080" height="749" alt="" /></a>'
    '<p class="lenz-footer__tag">%s</p>'
    '<ul class="lenz-footer__nap">'
    '<li>%s<span>%s, %s, %s</span></li>'
    '<li>%s<a href="%s">%s</a></li>'
    '<li>%s<a href="mailto:%s">%s</a></li>'
    '<li>%s<span>%s</span></li>'
    '</ul>' % (
        img_url("lenz-logo-new"), NAP["slogan"],
        svg("i-pin", "lenz-icon-sm"), NAP["hq"]["street"], NAP["hq"]["city"], NAP["hq"]["region"],
        svg("i-phone", "lenz-icon-sm"), PHONE_TEL, PHONE,
        svg("i-mail", "lenz-icon-sm"), NAP["email"], NAP["email"],
        svg("i-clock", "lenz-icon-sm"), NAP["hours"],
    )
)


def col(title, items):
    return E.column([
        E.heading(title, "h3", font=F["heading"], size=13, weight="700",
                  classes="lenz-footer__col-title"),
        link_list(items),
    ], gap=16, classes="lenz-footer__col")


footer_grid = E.grid([
    E.column([html(nap_html)], gap=16, classes="lenz-footer__brand"),
    col("Air Conditioning", [
        ("AC Installation", "/services/air-conditioning/ac-installation/"),
        ("AC Repair", "/services/air-conditioning/ac-repair/"),
        ("AC Maintenance", "/services/air-conditioning/ac-maintenance/"),
        ("AC Replacement", "/services/air-conditioning/ac-replacement/"),
    ]),
    col("Heating", [
        ("Heating Installation", "/services/heating/heating-installation/"),
        ("Heating Repair", "/services/heating/heating-repair/"),
        ("Heating Maintenance", "/services/heating/heating-maintenance/"),
        ("Heating Replacement", "/services/heating/heating-replacement/"),
    ]),
    col("Company", [
        ("Maintenance Plans", L["plans"]),
        ("Specials", L["specials"]),
        ("Financing", L["financing"]),
        ("Service Areas", L["area"]),
        ("About Us", L["about"]),
        ("Contact Us", L["contact"]),
    ]),
], cols=4, tablet=2, mobile=1, gap=32)

footer_bottom = html(
    '<div class="lenz-footer__bottom">'
    '<span>© 2026 Lenz Heating &amp; Cooling</span><span class="sep">·</span>'
    '<span>BBB Accredited Business</span><span class="sep">·</span>'
    '<span>License %s</span><span class="sep">·</span>'
    '<a href="/privacy-policy/">Privacy Policy</a><span class="sep">·</span>'
    '<a href="/terms/">Terms &amp; Services</a>'
    '</div>' % NAP["license"])

footer = {
    "version": "0.4", "title": "Lenz Footer", "type": "footer",
    "content": [E.section(
        band("#121212"),
        [footer_grid, footer_bottom],
        pad=(64, 20, 32, 20), pad_mobile=(48, 18, 24, 18),
        classes="lenz-footer lenz-on-dark",
    )],
    "page_settings": {"template": "default"},
}

for name, doc in (("header", header), ("footer", footer)):
    out = os.path.join(HERE, name + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False)
    print("wrote %s (%d top-level)" % (out, len(doc["content"])))
print("  nav items / mega children : %d / %d" % (len(menu_items), len(mega_children)))
