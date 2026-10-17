#!/usr/bin/env python3
"""
HVIA home (one-page landing), built from the prototype option 2
(design-source/v2/v2.html), the client's pick. Header and footer are Theme Builder
parts (pages/_theme/build-templates.py).

Run:  python projects/hvia/pages/home/build.py
Then: python scripts/validate-page.py projects/hvia/pages/home/home.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import box, section, heading, button, image, raw, sec_head  # noqa: E402
from brand import PHONE, PHONE_TEL, ADDRESS_1, ADDRESS_2, MAPS, MAP_EMBED  # noqa: E402

B.reset(0x30000000)

# ------------------------------------------------------------------ hero ----
# Building picture in place of the group photo (client, 2026-10-12).
hero = section("hero", [
    box("wrap hero-grid", [
        box("hero-copy", [
            heading('<span class="dot" aria-hidden="true"></span>Introducing HVIA', "p", "kicker reveal-load d-0"),
            heading('<span class="line">Heart and</span> <span class="line">Vascular <em>Institute</em></span> '
                    '<span class="line red"><em>of</em> Alabama</span>',
                    "h1", "reveal-load d-100", size="clamp(3.4rem, 8.4vw, 7.6rem)"),
            box("hero-sub reveal-load d-380", [
                heading("Board-certified vascular and endovascular surgeons in Montgomery, Alabama.", "p", "lede"),
            ]),
            box("hero-ctas reveal-load d-480", [
                button("Call " + PHONE, PHONE_TEL, "btn btn-red btn-lg"),
                button("Find Us", "#locations", "btn btn-line btn-lg"),
            ]),
        ]),
        box("hero-media reveal-load d-200", [
            box("hero-photo hero-photo--building", [
                image("hvia-new-building", "Rendering of the new HVIA building at 4791 Woodmere Blvd, Montgomery"),
            ]),
            box("", [heading("Our new facility at %s, Montgomery." % ADDRESS_1, "span", "cap")], tag="figcaption"),
        ], tag="figure"),
    ]),
    box("wrap", [
        raw('<ul class="ledger ledger--contact reveal-load" style="--d:650ms" aria-label="Contact">'
            '<li><strong>Visit</strong><span>%s, %s</span></li>'
            '<li><strong>Call</strong><span><a href="%s">%s</a></span></li></ul>'
            % (ADDRESS_1, ADDRESS_2, PHONE_TEL, PHONE)),
    ]),
], el_id="main", label="Introducing HVIA")

# ------------------------------------------------------------- surgeons ----
# Names and photos only, no bios (client, 2026-10-08). All three "Vascular Surgeon" and a
# non-breaking space before MD so it never wraps alone (client, 2026-10-16).
DOCTORS = [
    ("dr-ralph-redd", "No. 1", "Vascular Surgeon", "Dr. Ralph Redd", "d-0"),
    ("dr-richard-tan", "No. 2", "Vascular Surgeon", "Dr. Richard Tan", "d-100"),
    ("dr-irwin-white-gittens", "No. 3", "Vascular Surgeon", "Dr. Irwin White-Gittens", "d-200"),
]


def surgeon(key, no, role, name, delay):
    return box("surgeon reveal " + delay, [
        box("doc-photo", [image(key, name + ", MD")]),
        heading("<span>%s</span>%s" % (no, role), "p", "doc-role"),
        heading("%s,&nbsp;<span>MD</span>" % name, "h3"),
    ], tag="li")


surgeons = section("physicians paper section", [
    box("wrap", [
        sec_head("01", "Our Surgeons", "Expert care, <em>experienced hands</em>"),
        box("surgeons", [surgeon(*d) for d in DOCTORS], tag="ul"),
    ]),
], el_id="physicians", label="Our Surgeons")

# ------------------------------------------------------------- location ----
# Map instead of the building photo, which is now in the hero (Erick, 2026-10-14).
# The figure is a container, not part of the html widget, because the prototype's
# `.building-photo + .loc` rule needs it to be the card's real sibling.
locations = section("locations section", [
    box("wrap", [
        sec_head("02", "Location", "Visit our <em>new facility</em>"),
        box("loc-grid", [
            box("building-photo loc-map reveal d-0", [
                raw('<iframe src="%s" title="Map: %s, %s" loading="lazy" '
                    'referrerpolicy="no-referrer-when-downgrade"></iframe>' % (MAP_EMBED, ADDRESS_1, ADDRESS_2)),
            ], tag="figure"),
            box("loc reveal d-120", [
                heading("Montgomery", "h3"),
                raw('<address>%s<br>%s</address><dl><div><dt>Phone</dt><dd><a href="%s">%s</a></dd></div></dl>'
                    '<a class="link" href="%s" target="_blank" rel="noopener">Get directions</a>'
                    % (ADDRESS_1, ADDRESS_2, PHONE_TEL, PHONE, MAPS)),
            ], tag="article"),
        ]),
    ]),
], el_id="locations", label="Location")

# ------------------------------------------------------------ final CTA ----
final = section("final-cta", [
    box("wrap final-inner reveal", [
        heading("Questions?", "p", "kicker kicker--light"),
        heading("Give our team <em>a call</em>", "h2", size="clamp(2.4rem, 5vw, 4.4rem)"),
        raw('<a class="big-phone" href="%s"><span>(334)</span> 801-9952</a>' % PHONE_TEL),
    ]),
], label="Call HVIA")

doc = B.E.wrap_page("Home", [hero, surgeons, locations, final], {"template": "elementor_header_footer"})
with open(os.path.join(HERE, "home.json"), "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
B.write_manifest(os.path.join(HERE, "widget-classes.json"))
print("wrote home.json (%d sections)" % len(doc["content"]))
