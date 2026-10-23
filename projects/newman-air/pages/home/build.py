#!/usr/bin/env python3
"""
Newman Air: Home page, V2.1.

Source of truth: design-source/v2-1/index.html (the V2 the team picked on
2026-10-06 plus Alexis/Dani/Manuel's and Shelby's edits, the 10/12 Bear
Necessities copy and the final logo), and ClickUp 86bcajgzh. The tree mirrors the
prototype's DOM and class names; see ../../brand.py and tools/port-css.py.

Section order (as the prototype): hero (+ request form), trust band, services,
about, difference slider, Bear Necessities, financing, reviews, brands, service
area, FAQ, final CTA. Header and footer are Theme Builder parts: ../_theme/.

Run:  python3 projects/newman-air/pages/home/build.py
Then: python3 scripts/validate-page.py projects/newman-air/pages/home/home.json
      python3 projects/newman-air/tools/port-css.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import L, PHONE, PHONE_TEL, svg, STARS  # noqa: E402

B.reset(0x41000000)
S = []
ARROW = svg("i-arrow")
# Prototype type scale (h1, h2 and the two h2 overrides); element settings outrank the stylesheet.
H1 = "clamp(2.7rem, 6.2vw, 5.4rem)"
H2 = "clamp(2rem, 4.2vw, 3.4rem)"


# Native widgets for text an editor changes (Erick 2026-10-23), same pieces as the
# inner pages (inner.css): eyebrows, card links, the form foot, the FAQ and the city
# list. Raw html stays for decoration and interactive markup (badge, ridges, glyphs,
# polaroids, slider controls, member card, partner logos, reviews placeholder,
# marquee, map).
def eyebrow(label, extra="", delay=None):
    st = {"title": label, "header_size": "p"}
    if delay:
        st["_attributes"] = "style|--delay:%s" % delay
    return B.E.widget("heading", st, classes=("nw-eyebrow " + extra).strip())


def text_link(label, url):
    return B.text('<p><a class="text-link nw-arrow" href="%s">%s</a></p>' % (url, label), classes="svc-link")


def h2(t):
    return B.heading(t, "h2", size=H2)



def lead(markup, cls="lead", extra=""):
    return B.text('<p class="%s"%s>%s</p>' % (cls, extra, markup))


# =================================================================== HERO ====
H1_WORDS = ["Dependable", "Heating", "&amp;", "Air", "Conditioning", "Service", "in"]
h1 = " ".join('<span class="w" style="--i:%d">%s</span>' % (i, w) for i, w in enumerate(H1_WORDS))
h1 += ' <span class="w hl" style="--i:7">Tri-Cities,&nbsp;TN</span>'

RIDGES = (
    '<div class="ridges" aria-hidden="true">'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none" data-parallax=".12"><path class="r1" d="M0 150 L110 92 L210 130 L330 58 L460 120 L580 70 L700 128 L840 44 L980 116 L1100 66 L1240 124 L1360 78 L1480 112 L1600 84 V260 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none" data-parallax=".06"><path class="r2" d="M0 190 L140 128 L260 170 L400 112 L540 176 L680 130 L820 186 L960 120 L1100 178 L1250 132 L1390 182 L1520 140 L1600 160 V260 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none"><path class="r3" d="M0 236 Q400 206 800 230 T1600 220 V260 H0Z"/><g class="trees"><path d="M120 236 l14-40 14 40Z M150 238 l10-28 10 28Z M1380 226 l14-42 14 42Z M1410 228 l10-30 10 30Z M1440 226 l12-36 12 36Z"/></g></svg>'
    '</div>')

BADGE = ('<div class="badge-ring" aria-hidden="true"><div class="disc"></div>'
         '<svg class="ring" viewBox="0 0 150 150"><defs><path id="circ" d="M75 75 m-60 0 a60 60 0 1 1 120 0 a60 60 0 1 1 -120 0"/></defs>'
         '<text><textPath href="#circ">Trust the bear to fix your air · Since 1994 · </textPath></text></svg>'
         '<img class="mascot" src="%s" alt=""></div>' % B.LOGO_BEAR)

S.append(B.section("hero topo grain on-dark", [
    B.box("wrap", [
        B.box("", [
            eyebrow("Hibernate in total comfort all year long", "fade-up", delay=".05s"),
            B.heading(h1, "h1", size=H1),
            lead("Locally owned and family-operated, Newman Air is proud to serve the Tri-Cities, TN area with "
                 "reliable work and honest service you can count on. We're known for transparent pricing, friendly "
                 "service, and a bear-strong team ready to see you through any heating or cooling issue.",
                 "lead fade-up", ' style="--delay:.75s"'),
            lead("From sudden emergency repairs to routine seasonal maintenance and full system upgrades, we keep "
                 "your home cozy through winter chills and cool through summer heat.",
                 "lead fade-up", ' style="--delay:.85s"'),
            B.box("btn-row fade-up", [
                B.button("Schedule Online", L["contact"], "btn btn-accent btn-xl", icon="arrow", icon_after=True),
                B.button("Call Us Today", PHONE_TEL, "btn btn-ghost btn-xl", icon="phone"),
            ], style="--delay:1s"),
        ]),
        B.box("form-card fade-up", [
            B.raw(BADGE),
            B.heading("Request Service", "h2", size="1.7rem"),
            B.text('<p class="form-sub">Tell us what\'s going on and our team will reach out to confirm your visit.</p>'),
            B.request_form(),
            B.text('<p class="form-foot nw-lock">Upfront $75 diagnostic fee. No hidden surprises.</p>'),
        ], style="--delay:.6s"),
    ]),
    B.raw(RIDGES),
], el_id="contact"))

# ================================================================== TRUST ====
TRUST = [('<span class="num" data-count="30" data-suffix="+">30+</span>', "Years Serving Tri-Cities",
          "Local, family-owned &amp; operated since 1994."),
         ('<span class="num" data-count="1100" data-suffix="+">1,100+</span>', "5-Star Reviews",
          "Rated 4.8/5 stars across Johnson City, Kingsport, and Bristol."),
         ('<span class="num">$<span data-count="75">75</span></span>', "Diagnostic Fee",
          "Upfront evaluations and transparent pricing before repairs begin."),
         ('<span class="num">$$</span>', "Flexible Financing",
          "Fast online application through GoodLeap, Synchrony &amp; Hearth.")]
S.append(B.section("trust", [
    B.box("band", [
        B.box("wrap", [
            B.box("trust-item reveal", [B.text(n), B.text("<strong>%s</strong>" % t), B.text("<span>%s</span>" % d)], d=i)
            for i, (n, t, d) in enumerate(TRUST)
        ]),
    ]),
], label="Why homeowners trust us"))

# =============================================================== SERVICES ====
CARDS = [
    ("aci", "i-snow", "Air Conditioning Installation",
     "Stay cool all summer long. We install high-efficiency central ACs, heat pumps, and ductless mini-splits from "
     "trusted brands like Ruud®, Daikin®, YORK®, and Mitsubishi, tailored to your home and budget.",
     L["ac-installation"], "AC Installation"),
    ("acr", "i-wrench", "Air Conditioning Repair",
     "Don't hibernate in a hot home. Our skilled techs respond quickly to diagnose the issue with a simple $75 "
     "diagnostic fee and an upfront repair estimate before any work starts.", L["ac-repair"], "AC Repair"),
    ("hti", "i-heat", "Heating Installation",
     "Make replacing an outdated heater smooth and hassle-free. We install dependable gas furnaces, heat pumps, and "
     "mini-splits engineered to handle freezing East Tennessee winters.",
     L["heating-installation"], "Heating Installation"),
    ("htr", "i-flame", "Heating &amp; Furnace Repair",
     "When your heat goes out, we get it back on fast. Every service call includes our standard $75 diagnostic fee "
     "with honest, transparent pricing and no hidden surprises.", L["heating-repair"], "Heating Repair"),
    ("mnt", "i-calendar", "Seasonal Maintenance &amp; Tune-Ups",
     "Prevent sudden breakdowns and keep utility bills low. Our seasonal tune-ups catch minor wear early, keep "
     "equipment running efficiently, and extend system lifespan.", L["maintenance-plan"], "Maintenance Plans"),
    ("iaq", "i-air", "Indoor Air Quality Solutions",
     "True comfort is about clean air. We install whole-home purification systems, including REME HALO® in-duct "
     "purifiers and PlasmaPURE ionizers, to remove dust, pollen, and odors.",
     L["indoor-air-quality"], "Air Quality Solutions"),
]
S.append(B.section("services topo light", [
    B.box("wrap", [
        B.box("section-top", [
            B.box("reveal", [eyebrow("Our Services"),
                             h2("Unshakable HVAC Performance &amp; Total Home Comfort")]),
        ]),
        B.box("bento", [
            B.box("svc %s reveal" % c, [
                B.raw('<svg class="glyph" aria-hidden="true"><use href="#%s"/></svg>'
                      '<div class="duo">%s</div>' % (ic, svg(ic))),
                B.heading(h, "h3"),
                B.text("<p>%s</p>" % t),
                text_link(lk, url),
            ], tag="article", d=i % 3)
            for i, (c, ic, h, t, url, lk) in enumerate(CARDS)
        ]),
    ]),
], el_id="services"))

# ================================================================== ABOUT ====
POLAROIDS = ('<div class="polaroid-stack reveal">'
             '<figure class="polaroid p1"><span class="tape"></span><div class="shot"><span class="display" '
             'style="font-size:1.1rem;color:var(--c-base)">Team photo</span><span class="note">Client photos requested</span></div>'
             '<figcaption>Our pack</figcaption></figure>'
             '<figure class="polaroid p2"><span class="tape"></span><div class="shot"><img src="%s" alt="Newman Air">'
             '</div><figcaption>Since 1994</figcaption></figure></div>' % B.LOGO_STACKED)
S.append(B.section("about grain", [
    B.box("wrap", [
        B.raw(POLAROIDS),
        B.box("reveal", [
            eyebrow("About Our Pack"),
            h2("Rock-Solid Reliability &amp; Friendly Local Service"),
            B.text('<div class="big-stat"><div><b data-count="23">23</b><small>local employees</small></div>'
                   '<div><b data-count="150" data-suffix="+">150+</b><small>years of combined experience</small></div></div>'),
            lead("When you call Newman Air, you're welcoming a real neighbor into your home. Our team of 23 local "
                 "employees boasts over 150 years of combined experience, bringing true craftsmanship to every job."),
            lead("We believe in honest communication, clean work, and friendly service that leaves you completely at "
                 "ease. From our office staff to the techs in the field, we treat your home like our own."),
            B.box("btn-row", [
                B.button("Our Story", L["about"], "btn btn-accent", icon="arrow", icon_after=True),
                B.button("Get In Touch", L["contact"], "btn btn-ghost"),
            ], style="margin-top:28px"),
        ], d=1),
    ]),
], el_id="about"))

# ============================================================= DIFFERENCE ====
DIFF = [
    ("Top HVAC Brands", "We work with the most trusted names in the business, including Ruud®, Daikin®, YORK®, and "
     "Mitsubishi. Pairing reliable equipment with our proper installation means your home stays cozy through winter "
     "freezes and cool during summer heatwaves."),
    ("Deep Local Roots", "For us, loyalty goes both ways. We're grateful for the Tri-Cities families who've relied on "
     "us for decades, and we're committed to giving that same support right back. Whether it's supporting local "
     "events or being there when your heat goes out, we believe in being an active, dependable part of our community."),
    ("30+ Years of Experience", "For over 30 years, we've been taking care of heating and air conditioning systems "
     "across East Tennessee. We've built our reputation on good workmanship, reliable performance, and long-lasting "
     "customer relationships. That kind of staying power comes from doing quality work year after year."),
    ("Locally Owned &amp; Family Operated", "As a local, family-operated business, we know what it means to treat "
     "people like neighbors. You can always count on friendly service, familiar faces, and a team that genuinely "
     "cares about your family's comfort, not just making a quick sale."),
    ("Built on Honest Service", "We measure success by how well we keep our promises. Integrity guides everything we "
     "do, from clear estimates to doing what we say we're going to do. When you choose Newman Air, you're choosing "
     "honest advice and a team that stands behind its work."),
    ("Skilled &amp; Respectful Techs", "Our certified technicians bring real skill, training, and care to every home "
     "they visit. Customers count on them for their sharp technical know-how paired with a respectful, friendly "
     "attitude that makes service easy. They're the backbone of our team and take pride in doing the job right."),
]
S.append(B.section("difference topo grain on-dark", [
    B.box("wrap", [
        B.box("slider-head reveal", [
            B.box("", [eyebrow("The Newman Air Difference"),
                       h2("Fierce Standards for Tri&#8209;Cities Homeowners")]),
            B.raw('<div class="slider-nav"><button type="button" data-dir="-1" aria-label="Previous">%s</button>'
                  '<button type="button" data-dir="1" aria-label="Next">%s</button></div>'
                  % (svg("i-left"), svg("i-right"))),
        ]),
    ]),
    B.box("track reveal", [
        B.box("diff-card", [B.text('<span class="num">%02d</span>' % (i + 1)), B.heading(t, "h3"),
                            B.text("<p>%s</p>" % p)], tag="article")
        for i, (t, p) in enumerate(DIFF)
    ], el_id="diffTrack", d=1),
    B.box("wrap", [B.raw('<div class="progress"><span id="diffProgress"></span></div>')]),
], el_id="difference"))

# ======================================================= BEAR NECESSITIES ====
TICK = '<span class="tick">%s</span>' % svg("i-check")
S.append(B.section("club", [
    B.box("wrap", [
        B.box("reveal", [
            B.raw('<div class="member-card"><div class="mc-top"><div class="mc-name">BEAR NECESSITIES<small>NEWMAN AIR '
                  'MEMBER</small></div><span class="chip"></span></div><img class="mascot" src="%s" alt="">'
                  '<div class="mc-foot">Starting at<b>$149/year</b></div></div>' % B.LOGO_BEAR),
        ]),
        B.box("reveal", [
            eyebrow("Bear Necessities Maintenance Plan"),
            h2('Protect Your HVAC System Starting at <span class="price">$149/Year</span>'),
            lead("East Tennessee weather pushes heating and cooling systems to their limits. Our annual maintenance "
                 "plan keeps your equipment running efficiently, helps prevent sudden breakdowns, and gives you "
                 "priority service when you need it most."),
            B.text('<ul class="checks">%s</ul>' % "".join(
                "<li>%s<span><strong>%s</strong> %s</span></li>" % (TICK, a, b) for a, b in [
                    ("Two Seasonal Tune-Ups:", "Comprehensive spring cooling and fall heating inspections."),
                    ("10% Repair Savings:", "Instant discounts on qualifying parts and labor."),
                    ("Priority Scheduling:", "Jump to the front of the line during extreme weather.")])),
            B.button("Explore Plan Details", L["maintenance-plan"], "btn btn-accent", icon="arrow", icon_after=True),
        ], d=1),
    ]),
], el_id="maintenance-plan"))

# ============================================================== FINANCING ====
STEPS = [("i-bolt", "Fast Online Pre-Approval", "Quick applications with no impact on your credit score to check options."),
         ("i-shield", "Trusted Financial Partners", "Flexible plans provided through GoodLeap, Synchrony Bank, and Hearth."),
         ("i-sliders", "Custom Payment Structures", "Tailored solutions for both full system installations and major repairs.")]
S.append(B.section("finance", [
    B.box("wrap", [
        B.box("reveal", [
            eyebrow("Flexible Financing"),
            h2("Smart Payment Plans That Don't Strain Your Budget"),
            lead("HVAC emergencies rarely happen when it's convenient. Newman Air offers low monthly payment options so "
                 "you can upgrade your system or handle repairs without financial stress."),
            B.raw('<div class="partners"><span><img src="%sfin-goodleap.svg" alt="GoodLeap"></span><span><img '
                  'src="%sfin-synchrony.png" alt="Synchrony Bank"></span><span><img class="hearth" src="%sfin-hearth.svg" '
                  'alt="Hearth"></span></div>' % (B.IMG, B.IMG, B.IMG)),
            B.button("See Financing Options", L["financing"], "btn btn-accent", icon="arrow", icon_after=True),
        ]),
        B.box("steps", [
            B.box("step reveal", [B.raw('<span class="n">%s</span>' % svg(ic)),
                                  B.text("<div><strong>%s</strong><span>%s</span></div>" % (t, d))], d=i)
            for i, (ic, t, d) in enumerate(STEPS)
        ]),
    ]),
], el_id="financing"))

# ================================================================ REVIEWS ====
SKEL = ['<div class="skel"></div><div class="skel"></div><div class="skel s"></div>',
        '<div class="skel"></div><div class="skel"></div><div class="skel"></div><div class="skel"></div><div class="skel s"></div>',
        '<div class="skel"></div><div class="skel"></div><div class="skel"></div><div class="skel s"></div>',
        '<div class="skel"></div><div class="skel s"></div>']
RV = "".join('<div class="rv reveal" style="--d:%d"><span class="q">"</span><div class="rv-head"><span class="rv-avatar">'
             '</span><div style="flex:1"><div class="skel s"></div><div class="skel xs"></div></div></div>%s%s</div>'
             % (i, STARS.replace(' role="img" aria-label="5 out of 5 stars"', ""), s) for i, s in enumerate(SKEL))
S.append(B.section("reviews", [
    B.box("wrap", [
        B.box("score reveal", [
            eyebrow("Reviews &amp; Testimonials"),
            h2("Trusted Across the Tri&#8209;Cities Since 1994"),
            B.text('<div class="big"><span data-count="4.8" data-decimals="1">4.8</span><small>/ 5</small></div>' + STARS),
            B.text('<p class="meta">1,100+ 5-star reviews across Johnson City, Kingsport, and Bristol.</p>'),
            lead("We treat every job like we're helping out a neighbor. Read live reviews from local homeowners who "
                 "experienced our service firsthand."),
        ]),
        B.raw('<div><p style="margin-bottom:14px"><span class="note">Live review widget goes here (Alexis). No reviews '
              'are invented in this mockup.</span></p><div class="masonry" aria-hidden="true">%s</div></div>' % RV),
    ]),
], el_id="reviews"))

# ================================================================= BRANDS ====
BRANDS = [("brand-ruud.png", "Ruud"), ("brand-daikin.png", "Daikin"), ("brand-york.png", "YORK"),
          ("brand-mitsubishi.png", "Mitsubishi Electric"), ("brand-goodman.png", "Goodman")]
S.append(B.section("brands", [
    B.box("wrap head reveal", [
        eyebrow("Quality Equipment"),
        h2("Dependable Systems Built for Long-Term Comfort"),
        lead("Whether you're looking for high-efficiency heat pumps, traditional gas furnaces, or versatile "
             "mini-splits, we install proven systems backed by solid manufacturer warranties."),
    ]),
    B.raw('<div class="marquee"><div class="marquee-track" id="brandTrack">%s</div></div>' % "".join(
        '<div class="brand-tile"><img src="%s%s" alt="%s"></div>' % (B.IMG, f, a) for f, a in BRANDS)),
]))

# ================================================================== AREA ====
CITIES = [("jc", "Johnson City", "johnson-city"), ("kp", "Kingsport", "kingsport"), ("br", "Bristol", "bristol"),
          ("el", "Elizabethton", "elizabethton"), ("gv", "Greeneville", "greeneville"),
          ("jb", "Jonesborough", "jonesborough"), ("gr", "Gray", "gray"), ("pf", "Piney Flats", None),
          ("bc", "Bluff City", None), ("ls", "Limestone", None), ("tf", "Telford", None)]
PINS = [("kp", 294, 116, 306, 112, "", "Kingsport"), ("br", 558, 84, 548, 66, "middle", "Bristol"),
        ("jc", 441, 273, 453, 290, "", "Johnson City"), ("el", 542, 249, 554, 245, "", "Elizabethton"),
        ("gv", 104, 373, 116, 369, "", "Greeneville"), ("jb", 356, 286, 344, 306, "end", "Jonesborough"),
        ("gr", 354, 202, 342, 198, "end", "Gray"), ("pf", 474, 202, 486, 206, "", "Piney Flats"),
        ("bc", 506, 166, 518, 170, "", "Bluff City"), ("ls", 247, 334, 235, 338, "end", "Limestone"),
        ("tf", 309, 316, 300, 342, "middle", "Telford")]
MAP = ('<div class="map-card reveal" style="--d:1"><svg viewBox="0 0 640 430" role="img" aria-label="Illustrative map '
       'of the Tri-Cities service area"><g id="pins">%s</g></svg><span class="note">Illustrative only. Replace with GBP '
       'map embed (Alexis)</span></div>' % "".join(
           '<g class="pin" data-city="%s"><circle class="pulse" cx="%d" cy="%d" r="8"/><circle class="dot" cx="%d" '
           'cy="%d" r="7"/><text x="%d" y="%d"%s>%s</text></g>'
           % (k, x, y, x, y, tx, ty, (' text-anchor="%s"' % a) if a else "", n) for k, x, y, tx, ty, a, n in PINS))
S.append(B.section("area grain on-dark", [
    B.box("wrap", [
        B.box("reveal", [
            eyebrow("Our Service Area"),
            h2("Proudly Serving Homes Across the Tri&#8209;Cities Region"),
            lead("We provide prompt diagnostic calls, maintenance, and installations across all major Tri-Cities "
                 "communities:"),
            B.E.widget("icon-list", {"_element_id": "cityList", "icon_list": [
                dict({"_id": "nwcity%s" % k, "text": n + ", TN",
                      "selected_icon": {"value": "fas fa-map-marker-alt", "library": "fa-solid"}},
                     **({"link": {"url": B.area(sl), "is_external": "", "nofollow": ""}} if sl else {}))
                for k, n, sl in CITIES]}, classes="nw-cities"),
            B.text('<p>Not sure if you\'re in our service zone? Give us a quick call at <a class="phone" href="%s">%s</a>.</p>'
                   % (PHONE_TEL, PHONE)),
            B.button("Contact Our Team", L["contact"], "btn btn-accent", icon="arrow", icon_after=True),
        ]),
        B.raw(MAP),
    ]),
], el_id="area"))

# ==================================================================== FAQ ====
FAQ = [
    ("How much do you charge for a diagnostic visit?",
     "Our standard diagnostic fee is <strong>$75</strong>. A technician will inspect your system, find the issue, and "
     "provide a clear, upfront repair estimate before any work starts."),
    ("What areas do you service and do you handle emergencies?",
     "We serve homeowners across Washington, Sullivan, Carter, and Greene counties. When your heat fails in winter or "
     "your AC breaks in summer, our team responds quickly."),
    ("Are your technicians licensed, insured, and certified?",
     "Yes. Newman Air is fully licensed, bonded, and insured in Tennessee. Our 23-person team is background-checked, "
     "certified, and professionally trained."),
    ("Do you offer financing for new system installations?",
     "Yes. We partner with GoodLeap, Synchrony Bank, and Hearth to offer flexible monthly payment plans with quick "
     "online pre-approval."),
    ("Should I repair or replace my heating and cooling system?",
     "If your unit is under 10 years old, repair is usually best. If it's over 10 to 12 years old, requires frequent "
     "fixes, or drives up electric bills, upgrading to a high-efficiency system saves money over time."),
]
PLUS = {"value": "fas fa-plus", "library": "fa-solid"}
S.append(B.section("faq", [
    B.box("wrap", [
        B.box("faq-side reveal", [
            eyebrow("Got Questions?"),
            h2("Frequently Asked Questions"),
            B.text('<div class="ask"><img class="mascot" src="%s" alt=""><div><strong>Still wondering about something?'
                   '</strong><a href="%s">Call %s</a></div></div>' % (B.LOGO_BEAR, PHONE_TEL, PHONE)),
        ]),
        B.E.widget("nested-accordion", {
            "items": [{"_id": "nwfaq%d" % i, "item_title": q} for i, (q, a) in enumerate(FAQ)],
            "title_tag": "h3", "faq_schema": "yes", "default_state": "expanded", "max_items_expended": "one",
            "accordion_item_title_icon": PLUS, "accordion_item_title_icon_active": PLUS,
        }, elements=[B.box("faq-ans", [B.text("<p>%s</p>" % a)]) for q, a in FAQ], classes="faq-acc"),
    ]),
], el_id="faq"))

# ============================================================== FINAL CTA ====
FINAL_RIDGES = (
    '<div class="ridges" aria-hidden="true">'
    '<svg viewBox="0 0 1600 200" preserveAspectRatio="none"><path class="r1" d="M0 120 L160 70 L300 110 L460 50 L620 104 L800 40 L980 100 L1140 56 L1300 108 L1460 64 L1600 96 V200 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 200" preserveAspectRatio="none"><path class="r3" d="M0 170 Q400 140 800 166 T1600 156 V200 H0Z"/></svg>'
    '</div>')
S.append(B.section("final topo grain on-dark", [
    B.box("wrap reveal", [
        eyebrow("Trust the bear to fix your air"),
        B.heading("Reliable Home Comfort Is Just a Call or Click Away", "h2", size="clamp(2.4rem, 6vw, 4.8rem)"),
        lead("From simple repairs to full system replacements, we bring honest answers and upfront pricing to every "
             "doorstep in the Tri-Cities. Give our friendly team a call or book your service visit online in just a few clicks."),
        B.box("btn-row", [
            B.button("Schedule Service", L["contact"], "btn btn-accent btn-xl", icon="arrow", icon_after=True),
            B.button("Call Us Now", PHONE_TEL, "btn btn-ghost btn-xl", icon="phone"),
        ]),
    ]),
    B.raw('<img class="bear-rise mascot" src="%s" alt="">' % B.LOGO_BEAR),
    B.raw(FINAL_RIDGES),
]))

# ================================================================== WRITE ====
doc = B.E.wrap_page("Home", S, {"template": "elementor_header_footer", "hide_title": "yes"})
out = os.path.join(HERE, "home.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
B.write_manifest(os.path.join(HERE, "widget-classes.json"))
print("wrote %s (%d sections)" % (out, len(S)))
