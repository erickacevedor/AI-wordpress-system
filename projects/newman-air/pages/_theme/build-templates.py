#!/usr/bin/env python3
"""
Newman Air: Theme Builder header and footer for V2.1. Same approach as the pages
(see ../../brand.py): the prototype's markup and class names, ported CSS and
behaviour in newman-core.

Header: the prototype's fixed `.site-head` (utility bar + `header.bar`), all native
widgets since 2026-10-23: icon lists, logo image, a Nav Menu widget showing the
WordPress menu "Newman Main" (tools/make-menus.php; the Services mega menu and the
mobile dropdown are styled in inner.css) and the CTA button. Footer: logo image,
text, icon lists for contact and link columns, legal line.

Display condition: set by tools/import-template.php. While the splash is the
front page these parts show only on pages built from this design; switch them to
"Entire Site" at launch.

Run:  python3 projects/newman-air/pages/_theme/build-templates.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import L, PHONE, PHONE_TEL, EMAIL, AREAS  # noqa: E402


def write(name, sections, title):
    doc = B.E.wrap_page(title, sections, {"template": "default"})
    doc["type"] = name
    with open(os.path.join(HERE, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


FA = lambda v, lib="fa-solid": {"value": v, "library": lib}  # noqa: E731


def link(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def icon_list(items, classes, inline=False):
    """Native icon list: items are (text, url or None, icon or None)."""
    s = {"icon_list": [{"_id": B.E.nid()[-7:], "text": t, "selected_icon": icon or {"value": "", "library": ""},
                        **({"link": link(u)} if u else {})} for t, u, icon in items]}
    if inline:
        s["view"] = "inline"
    return B.E.widget("icon-list", s, classes=classes)


def logo(cls):
    return B.E.widget("image", {"image": {"url": B.LOGO_HORIZ, "id": "", "alt": "Newman Air", "source": "library"},
                                "image_size": "full", "link_to": "custom", "link": link("/")}, classes=cls)


# ================================================================ HEADER ====
# Native widgets (Erick 2026-10-23): the menu is the WordPress menu "Newman Main"
# (tools/make-menus.php, edited in Appearance > Menus) in a Nav Menu widget; inner.css
# lays the Services submenu out as the V2.1 mega menu and styles the mobile dropdown.
B.reset(0x42000000)

utility = B.box("utility", [B.box("wrap", [
    icon_list([("Locally owned & family operated in the Tri-Cities since 1994", None, FA("fas fa-map-marker-alt"))],
              "utility-left hide-sm", inline=True),
    icon_list([(EMAIL, "mailto:" + EMAIL, FA("far fa-envelope", "fa-regular")),
               (PHONE, PHONE_TEL, FA("fas fa-phone-alt"))], "utility-right", inline=True),
])])

nav = B.E.widget("nav-menu", {
    "menu": "newman-main", "menu_name": "Main", "layout": "horizontal", "pointer": "none",
    "submenu_icon": FA("fas fa-chevron-down"), "dropdown": "tablet", "full_width": "stretch",
    "toggle": "burger",
}, classes="nw-nav")

header = B.section("site-head", [
    utility,
    B.box("bar", [
        B.box("wrap", [
            logo("logo"),
            nav,
            B.box("head-cta", [B.button("Schedule Online", L["contact"], "btn btn-accent")]),
        ]),
    ], tag="header"),
], tag="div", el_id="siteHead")

write("header", [header], "Newman Air Header (V2.1)")
header_manifest = dict(B._MANIFEST)

# ================================================================ FOOTER ====
B.reset(0x43000000)

FOOT_SERVICES = [("AC Installation", L["ac-installation"]), ("AC Repair", L["ac-repair"]),
                 ("Heating Installation", L["heating-installation"]), ("Heating Repair", L["heating-repair"]),
                 ("Heat Pumps", L["heat-pumps"]), ("Ductless Mini Splits", L["ductless"]),
                 ("Indoor Air Quality", L["indoor-air-quality"]), ("Commercial HVAC", L["commercial"])]
FOOT_COMPANY = [("About Us", L["about"]), ("Maintenance Plan", L["maintenance-plan"]), ("Financing", L["financing"]),
                ("Blog", L["blog"]), ("Contact Us", L["contact"])]


def foot_links(items):
    return icon_list([(n, u, None) for n, u in items], "foot-links")


footer = B.section("site", [
    B.box("wrap", [
        B.box("cols", [
            B.box("", [
                logo("foot-logo"),
                B.text("<p>Locally owned and family-operated heating &amp; air conditioning in the Tri-Cities, TN since "
                       "1994. Licensed, bonded &amp; insured.</p>"),
                icon_list([(PHONE, PHONE_TEL, FA("fas fa-phone-alt")),
                           (EMAIL, "mailto:" + EMAIL, FA("far fa-envelope", "fa-regular"))], "foot-contact"),
            ]),
            B.box("", [B.heading("Services", "h4"), foot_links(FOOT_SERVICES)]),
            B.box("", [B.heading("Company", "h4"), foot_links(FOOT_COMPANY)]),
            B.box("", [B.heading("Service Areas", "h4"), foot_links([(n, B.area(s)) for n, s in AREAS])]),
        ]),
        B.box("legal", [
            B.text("<p>&copy; 2026 Newman Air. All rights reserved.</p>"),
            icon_list([("Privacy Policy", L["privacy"], None), ("Terms of Service", L["terms"], None)],
                      "legal-links", inline=True),
        ]),
    ]),
], tag="footer", label="Site footer")

write("footer", [footer], "Newman Air Footer (V2.1)")
manifest = dict(B._MANIFEST)
manifest.update(header_manifest)
with open(os.path.join(HERE, "widget-classes.json"), "w", encoding="utf-8") as f:
    json.dump(dict(sorted(manifest.items())), f, indent=2)
    f.write(chr(10))
print("wrote header.json, footer.json")
