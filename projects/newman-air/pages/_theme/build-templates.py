#!/usr/bin/env python3
"""
Newman Air: Theme Builder header and footer for V2.1. Same approach as the pages
(see ../../brand.py): the prototype's markup and class names, ported CSS and
behaviour in newman-core.

Header: the prototype's fixed `.site-head` (utility bar + `header.bar` with the
Services mega menu, the Service Areas dropdown and the mobile drawer). The nav and
the drawer are html widgets, verbatim prototype markup generated from
brand.SERVICES / brand.AREAS; editing a menu item means editing brand.py and
rebuilding. The CTA is a native button.

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
from brand import L, PHONE, PHONE_TEL, EMAIL, SERVICES, AREAS, svg  # noqa: E402


def write(name, sections, title):
    doc = B.E.wrap_page(title, sections, {"template": "default"})
    doc["type"] = name
    with open(os.path.join(HERE, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


# ================================================================ HEADER ====
B.reset(0x42000000)

utility = ('<div class="utility"><div class="wrap"><span class="hide-sm">%sLocally owned &amp; family operated in the '
           'Tri-Cities since 1994</span><span style="gap:18px"><a href="mailto:%s">%s%s</a><a href="%s">%s%s</a></span>'
           '</div></div>' % (svg("i-pin"), EMAIL, svg("i-mail"), EMAIL, PHONE_TEL, svg("i-phone"), PHONE))

mega_cols = "".join('<div class="mega-col"><p class="mega-title">%s%s</p>%s</div>'
                    % (svg(ic), t, "".join('<a href="%s">%s</a>' % (L[k], n) for n, k in items))
                    for t, ic, items in SERVICES)
mega_cta = ('<a class="mega-cta" href="%s"><img class="mascot" src="%s" alt=""><span><strong>Not sure what you need?'
            '</strong>Upfront $75 diagnostic. Call %s</span></a>' % (L["contact"], B.LOGO_BEAR, PHONE))
areas = "".join('<a href="%s">%s</a>' % (B.area(s), n) for n, s in AREAS)
NAV_SIMPLE = [("Maintenance Plan", "maintenance-plan"), ("Financing", "financing"), ("Blog", "blog"),
              ("About Us", "about"), ("Contact Us", "contact")]
nav = ('<nav class="main" aria-label="Main">'
       '<div class="nav-item has-mega"><a href="/#services" class="nav-link" aria-haspopup="true">Services %s</a>'
       '<div class="mega">%s%s</div></div>'
       '<div class="nav-item has-drop"><a href="/#area" class="nav-link" aria-haspopup="true">Service Areas %s</a>'
       '<div class="drop">%s</div></div>%s</nav>'
       % (svg("i-down", "icon chev"), mega_cols, mega_cta, svg("i-down", "icon chev"), areas,
          "".join('<div class="nav-item"><a class="nav-link" href="%s">%s</a></div>' % (L[k], n) for n, k in NAV_SIMPLE)))

drawer = ('<div class="drawer" id="drawer"><details><summary>Services</summary>%s</details>'
          '<details><summary>Service Areas</summary><div class="drawer-group">%s</div></details>%s'
          '<div class="btn-row" style="margin-top:16px"><a class="btn btn-accent" href="%s">Schedule Online</a>'
          '<a class="btn btn-ghost" href="%s">%s%s</a></div></div>'
          % ("".join('<div class="drawer-group"><p>%s</p>%s</div>' % (t, "".join('<a href="%s">%s</a>' % (L[k], n)
                                                                               for n, k in items))
                     for t, ic, items in SERVICES),
             areas, "".join('<a class="drawer-link" href="%s">%s</a>' % (L[k], n) for n, k in NAV_SIMPLE),
             L["contact"], PHONE_TEL, svg("i-phone"), PHONE))

header = B.section("site-head", [
    B.raw(utility),
    B.box("bar", [
        B.box("wrap", [
            B.raw('<a class="logo" href="/" aria-label="Newman Air home"><img src="%s" alt="Newman Air" width="143" '
                  'height="60"></a>' % B.LOGO_HORIZ),
            B.raw(nav),
            B.box("head-cta", [B.button("Schedule Online", L["contact"], "btn btn-accent")]),
            B.raw('<button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false">%s</button>'
                  % svg("i-menu", "icon", "width:30px;height:30px")),
        ]),
        B.raw(drawer),
    ], tag="header"),
], tag="div", el_id="siteHead")

write("header", [header], "Newman Air Header (V2.1)")
header_manifest = dict(B._MANIFEST)

# ================================================================ FOOTER ====
B.reset(0x43000000)


def links(items):
    return "<ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in items)


FOOT_SERVICES = [("AC Installation", L["ac-installation"]), ("AC Repair", L["ac-repair"]),
                 ("Heating Installation", L["heating-installation"]), ("Heating Repair", L["heating-repair"]),
                 ("Heat Pumps", L["heat-pumps"]), ("Ductless Mini Splits", L["ductless"]),
                 ("Indoor Air Quality", L["indoor-air-quality"]), ("Commercial HVAC", L["commercial"])]
FOOT_COMPANY = [("About Us", L["about"]), ("Maintenance Plan", L["maintenance-plan"]), ("Financing", L["financing"]),
                ("Blog", L["blog"]), ("Contact Us", L["contact"])]

footer = B.section("site", [
    B.box("wrap", [
        B.box("cols", [
            B.box("", [
                B.raw('<img class="foot-logo" src="%s" alt="Newman Air">' % B.LOGO_HORIZ),
                B.text("<p>Locally owned and family-operated heating &amp; air conditioning in the Tri-Cities, TN since "
                       "1994. Licensed, bonded &amp; insured.</p>"),
                B.raw('<div class="foot-contact"><a href="%s">%s%s</a><a href="mailto:%s">%s%s</a></div>'
                      % (PHONE_TEL, svg("i-phone"), PHONE, EMAIL, svg("i-mail"), EMAIL)),
            ]),
            B.box("", [B.heading("Services", "h4"), B.text(links(FOOT_SERVICES))]),
            B.box("", [B.heading("Company", "h4"), B.text(links(FOOT_COMPANY))]),
            B.box("", [B.heading("Service Areas", "h4"), B.text(links([(n, B.area(s)) for n, s in AREAS]))]),
        ]),
        B.raw('<div class="legal"><span>© 2026 Newman Air. All rights reserved.</span><nav aria-label="Legal">'
              '<a href="%s">Privacy Policy</a><a href="%s">Terms of Service</a></nav></div>' % (L["privacy"], L["terms"])),
    ]),
], tag="footer", label="Site footer")

write("footer", [footer], "Newman Air Footer (V2.1)")
manifest = dict(B._MANIFEST)
manifest.update(header_manifest)
with open(os.path.join(HERE, "widget-classes.json"), "w", encoding="utf-8") as f:
    json.dump(dict(sorted(manifest.items())), f, indent=2)
    f.write("\n")
print("wrote header.json, footer.json")
