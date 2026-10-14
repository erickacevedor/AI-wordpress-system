#!/usr/bin/env python3
"""
HVIA: Theme Builder parts from the prototype option 2. Header = utility bar
(scrolls away) + sticky dark header with the numbered nav; footer = wordmark,
three columns, bottom line, all inside one .wrap.

Same approach as the pages (see ../../brand.py). The nav is one html widget with
the prototype markup; hvia-site.js drives the mobile toggle, the scrolled state and
the active-link spy. The header band is position:sticky; overrides.css makes the
Theme Builder wrapper display:contents so the sticky element's container is the
page (same fix as Lenz).

Run:  python projects/hvia/pages/_theme/build-templates.py
Then: python scripts/validate-page.py projects/hvia/pages/_theme/header.json
      python scripts/validate-page.py projects/hvia/pages/_theme/footer.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import box, section, heading, raw  # noqa: E402
from brand import PHONE, PHONE_TEL, ADDRESS_1, ADDRESS_2  # noqa: E402

MARK_LIGHT = B.MEDIA["hvia-mark-light"]["url"]
BRAND_NAME = '<span>Heart and Vascular</span><span>Institute of Alabama</span>'


def write(name, sections, title):
    doc = B.E.wrap_page(title, sections, {"template": "default"})
    doc["type"] = name          # "header" / "footer": the gate skips the H1 rule
    with open(os.path.join(HERE, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


# ================================================================ HEADER ====
B.reset(0x20000000)

utility = section("utility", [
    box("wrap utility-inner", [
        raw('<a class="skip" href="#main">Skip to content</a><span>%s, Montgomery, AL</span>' % ADDRESS_1),
        raw('<a href="%s">%s</a>' % (PHONE_TEL, PHONE)),
    ]),
], tag="div", label="Address and phone")

nav = ('<nav class="main-nav" aria-label="Main">'
       '<button class="nav-toggle" aria-expanded="false" aria-controls="nav-list"><span></span><span></span>'
       '<span></span><span class="sr">Menu</span></button>'
       '<ul id="nav-list">'
       '<li><a href="#physicians"><i>01</i> Surgeons</a></li>'
       '<li><a href="#locations"><i>02</i> Location</a></li>'
       '<li class="nav-cta"><a class="btn btn-red" href="%s">Call us</a></li>'
       '</ul></nav>' % PHONE_TEL)

header = section("site-header", [
    box("wrap header-inner", [
        raw('<a class="brand" href="#top" aria-label="Heart and Vascular Institute of Alabama, home">'
            '<img class="brand-mark" src="%s" alt="" width="48" height="47">'
            '<span class="brand-name">%s</span></a>' % (MARK_LIGHT, BRAND_NAME)),
        raw(nav),
    ]),
], tag="header", el_id="top")

write("header", [utility, header], "HVIA Header")

# ================================================================ FOOTER ====
B.reset(0x40000000)

footer = section("site-footer", [
    box("wrap", [
        heading("HVIA", "p", "footer-wordmark"),
        box("footer-grid footer-grid--3", [
            raw('<div class="footer-brand"><img src="%s" alt="" width="56" height="55" loading="lazy">'
                '<p class="brand-name">%s</p></div>' % (MARK_LIGHT, BRAND_NAME)),
            box("", [heading("Montgomery", "h3"), raw("<p>%s<br>%s</p>" % (ADDRESS_1, ADDRESS_2))]),
            box("", [heading("Contact", "h3"),
                     raw('<p><a href="%s">%s</a><br><a href="https://hviahealth.com">hviahealth.com</a></p>'
                         % (PHONE_TEL, PHONE))]),
        ]),
        box("footer-bottom", [
            raw('<p>&copy; <span id="year">2026</span> Heart and Vascular Institute of Alabama. '
                'All rights reserved.</p>'),
            raw('<p><a href="https://exploremedia.com/" target="_blank" rel="noopener">Powered by exploreMedia</a></p>'),
        ]),
    ]),
], tag="footer")

write("footer", [footer], "HVIA Footer")
# Widget classes for port-css.py. reset() clears the manifest, but the header is all
# html widgets, so the footer's classes are the whole list.
B.write_manifest(os.path.join(HERE, "widget-classes.json"))
print("wrote header.json, footer.json")
