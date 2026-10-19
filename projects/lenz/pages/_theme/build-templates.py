#!/usr/bin/env python3
"""
Lenz: Theme Builder parts for v6-1. Header (financing offer bar + sticky light nav
with the Services mega menu + mobile menu) and footer.

Same approach as the pages (see ../../brand.py): the prototype's markup and class
names, ported CSS in lenz-core, behaviour in lenz-core/assets/js/lenz-site.js.

The nav, mega menu and mobile menu are one html widget each, verbatim prototype
markup generated from brand.SERVICES / brand.NAV. That replaces the v4 build's
Elementor Mega Menu widget, which rendered ~170px wider than the source and
forced the phone number out of the bar (see git history of HANDOFF-notes.md).
Editing a menu item means editing brand.py and rebuilding, not the WP menu UI.

Three sections in the header, because of how the prototype positions things:
  1. .offer-bar      scrolls away
  2. header.nav      position:sticky; the Theme Builder wrapper is display:contents
                     (overrides.css) so the sticky element's container is the page
  3. .mobile-menu    position:fixed; it must NOT sit inside header.nav, whose
                     backdrop-filter would trap a fixed child

Run:  python3 projects/lenz/pages/_theme/build-templates.py
Then: python3 scripts/validate-page.py projects/lenz/pages/_theme/header.json
      python3 scripts/validate-page.py projects/lenz/pages/_theme/footer.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import L, PHONE, PHONE_TEL, EMAIL, NAV, svg
from brand import MENU as SERVICES     # in-scope pages only  # noqa: E402

LOGO_DARK_INK = B.MEDIA["lenz-logo-new-dark"]["url"]   # for light surfaces
LOGO_REVERSED = B.MEDIA["lenz-logo-new"]["url"]        # for dark surfaces


def write(name, sections, title):
    doc = B.E.wrap_page(title, sections, {"template": "default"})
    doc["type"] = name          # "header" / "footer": the gate skips the H1 rule
    with open(os.path.join(HERE, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


# ================================================================ HEADER ====
B.reset(0x20000000)

offer = B.section("offer-bar", [
    B.text("Own your comfort with flexible financing options.", "offer-bar__msg"),
    B.raw('<a class="offer-bar__cta" href="%s"><span class="offer-bar__cta-label">Explore financing</span>%s</a>'
          % (L["financing"], svg("i-arrow", "icon-xs"))),
], box_classes="offer-bar__inner", tag="div", el_id="offer-bar", label="Financing options")
offer["settings"]["_attributes"] = "aria-label|Financing options\ndata-season|financing"

# Column titles link to the hub pages (QA 2026-10-19: the hubs had no way in from the menu).
mega_cols = "".join(
    '<div class="mega__col"><p class="mega__col-title" id="mega-c%d"><a href="%s">%s</a></p>'
    '<ul class="mega__list" aria-labelledby="mega-c%d">%s</ul></div>'
    % (i, L[hub], title, i, "".join('<li><a href="%s">%s</a></li>' % (L[k], n) for n, k in items))
    for i, (title, hub, items) in enumerate(SERVICES, 1))

nav_links = (
    '<nav class="nav__links" aria-label="Primary"><div class="nav__item nav__item--mega">'
    '<button class="nav__link nav__link--mega" id="mega-trigger" aria-expanded="false" '
    'aria-controls="mega-services">Services %s</button></div>%s</nav>'
    % (svg("i-chevron", "icon-xs nav__caret"),
       "".join('<a class="nav__link" href="%s">%s</a>' % (L[k], n) for n, k in NAV)))

nav = B.section("nav nav--light", [
    B.raw('<a class="nav__logo" href="/"><span class="nav__logo-mark"><img src="%s" width="2080" '
          'height="749" alt="Lenz Heating &amp; Cooling" /></span></a>' % LOGO_DARK_INK),
    B.raw(nav_links),
    B.raw('<span class="nav__spacer"></span>'),
    B.raw('<a class="nav__phone" href="%s">%s%s</a>' % (PHONE_TEL, svg("i-phone", "icon-sm"), PHONE)),
    B.button("Free Estimate", "/#contact", "btn btn-primary nav__cta"),
    B.raw('<button class="nav__toggle" id="nav-toggle" aria-expanded="false" aria-controls="mobile-menu" '
          'aria-label="Open menu">%s%s</button>' % (svg("i-menu", "icon-menu"), svg("i-close", "icon-close"))),
    # In the prototype .mega is a sibling of .nav__inner; it is absolutely placed
    # against header.nav either way, because containers here are position:static.
    B.raw('<div class="mega" id="mega-services" role="group" aria-labelledby="mega-trigger" hidden>'
          '<div class="container mega__inner">%s</div></div>' % mega_cols),
], box_classes="container nav__inner", tag="header", el_id="nav")

m_groups = "".join(
    '<div class="m-acc__head"><button class="m-acc__trigger" aria-expanded="false" aria-controls="m-acc-%d">'
    '%s %s</button></div><div class="m-group__sub" id="m-acc-%d" hidden>%s</div>'
    % (i, title, svg("i-plus", "icon-sm m-acc__icon"), i,
       '<a href="%s">All %s Services</a>' % (L[hub], title) +
       "".join('<a href="%s">%s</a>' % (L[k], n) for n, k in items))
    for i, (title, hub, items) in enumerate(SERVICES, 1))
mobile = B.section("lz-mobile-menu-host", [
    B.raw('<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Menu">'
          '<div class="container"><div class="mobile-menu__head"><span class="nav__logo-mark">'
          '<img src="%s" width="2080" height="749" alt="" /></span>'
          '<button class="mobile-menu__close" id="mobile-menu-close" aria-label="Close menu">%s</button></div>'
          '<nav aria-label="Mobile"><p class="m-group__label">Services</p><div class="m-acc">%s</div>%s</nav>'
          '<div class="mobile-menu__cta"><a class="btn btn-gold" href="/#contact">Get a Free Estimate</a>'
          '<a class="btn btn-outline-light" href="%s">%s%s</a></div></div></div>'
          % (LOGO_REVERSED, svg("i-close"), m_groups,
             "".join('<a href="%s">%s</a>' % (L[k], n) for n, k in NAV),
             PHONE_TEL, svg("i-phone", "icon-sm"), PHONE)),
], box_classes="lz-mobile-menu-box", tag="div")

# The sentinel the sticky-nav observer watches: it scrolls away with the offer bar.
# Absolutely placed so it is not a flex item (no extra gap in the bar).
offer["elements"][0]["elements"].append(B.raw('<span id="nav-sentinel" aria-hidden="true" style="position:absolute"></span>'))

write("header", [offer, nav, mobile], "Lenz Header (v6-1)")
B.write_manifest(os.path.join(HERE, "widget-classes.json"))

# ================================================================ FOOTER ====
_header_manifest = dict(B._MANIFEST)
B.reset(0x30000000)


def links_list(items):
    return "<ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (L[k], n) for n, k in items)


def col(*groups):
    """A footer column with one or more (title, hub, links) groups; the title links to the hub."""
    kids = []
    for title, hub, items in groups:
        kids += [B.heading('<a href="%s">%s</a>' % (L[hub], title) if hub else title, "h3"),
                 B.text(links_list(items))]
    return B.box("footer__col", kids)


# QA 2026-10-19: Indoor Air Quality and the company pages (Meet the Team, Careers, Community
# Outreach, Hello Iowa, the two city pages) had no link in the footer; Privacy Policy and Terms
# are out until their pages exist (Erick).
PLANS_NAV = [("Maintenance Plans", "maintenance-plans"), ("Specials", "specials"), ("Financing", "financing")]
COMPANY_NAV = [("About Us", "about"), ("Meet the Team", "meet-the-team"), ("Careers", "hvac-jobs"),
               ("Community Outreach", "community-outreach"), ("Hello Iowa!", "hello-iowa"),
               ("Service Areas", "service-areas"), ("Urbandale", "urbandale"), ("Waukee", "waukee"),
               ("Contact Us", "contact")]


footer = B.section("footer", [
    B.box("footer__grid", [
        B.box("", [
            B.raw('<span class="footer__logo-mark"><img src="%s" width="2080" height="749" '
                  'alt="Lenz Heating &amp; Cooling" /></span>' % LOGO_REVERSED),
            B.text("Let Our Family Help Yours", "footer__tag"),
            B.raw('<ul class="footer__nap"><li>%s7641 Douglas Avenue, Urbandale, IA</li>'
                  '<li>%s<a href="%s">%s</a></li><li>%s<a href="mailto:%s">%s</a></li><li>%sOpen 24 hours</li></ul>'
                  % (svg("i-pin", "icon-sm"), svg("i-phone", "icon-sm"), PHONE_TEL, PHONE,
                     svg("i-mail", "icon-sm"), EMAIL, EMAIL, svg("i-clock", "icon-sm"))),
        ]),
        col(SERVICES[0], SERVICES[2]),
        col(SERVICES[1], ("Plans &amp; Savings", None, PLANS_NAV)),
        col(("Company", None, COMPANY_NAV)),
    ]),
    B.raw('<div class="footer__bottom"><span>© 2026 Lenz Heating &amp; Cooling</span><span class="sep">·</span>'
          '<span>BBB Accredited Business</span><span class="sep">·</span><span>License #50871-CL</span></div>'),
], tag="footer", label="Site footer")

write("footer", [footer], "Lenz Footer (v6-1)")
footer_manifest = dict(B._MANIFEST)
footer_manifest.update(_header_manifest)
with open(os.path.join(HERE, "widget-classes.json"), "w", encoding="utf-8") as f:
    json.dump(dict(sorted(footer_manifest.items())), f, indent=2)
    f.write("\n")
print("wrote header.json, footer.json")
