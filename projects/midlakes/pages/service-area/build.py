# -*- coding: utf-8 -*-
"""
Mid Lakes — Service Areas (/service-area/).

A 1:1 port of source.php. Copy is VERBATIM, entities included.

Band order (KIT-ANALYSIS §4):
    hero · white · paper · white · paper · ink

⚠️ The embedded Google Maps iframe becomes the Google Maps WIDGET (PORT-DECISIONS
decision 11), inside a radius-14 bordered frame.

⚠️ Section 4 nests h3 inside h3 (a column heading above a `.promise` list whose items
are also h3). That is the prototype's own markup — levels do not SKIP, so it is
faithful and valid. Do not "fix" it to h4.

Run:
    python3 projects/midlakes/pages/service-area/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/service-area/service-area.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x44000000)

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "hero-hvac",
    "HVAC Service Areas in Loganville, GA &amp; Surrounding Communities",
    "Trusted across Walton &amp; Gwinnett Counties with over 75 years of combined "
    "experience.",
    [B.btn_primary("Call Now: %s" % PH["display"], PH["tel"]),
     B.btn_ghost("Request Service Online", L["contact"])],
    interior=True)


# ------------------------------------------------------ 2. LOCAL SINCE 2018
local = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Local since 2018"),
          B.h2("Serving Our Neighbors with Pride Since 2018"),
          B.lead("At Mid Lakes HVAC, we aren&rsquo;t a big regional "
                 "franchise&mdash;we&rsquo;re your local neighbors. With our "
                 "headquarters located right here in Loganville, Georgia, our "
                 "family-owned business provides fast, reliable, and honest HVAC "
                 "solutions to homeowners across our local community."),
          B.lead("Whether you need 24/7 emergency AC repair, a high-efficiency "
                 "Carrier&reg; installation, or crawl space encapsulation, our "
                 "Loganville technicians deliver 75+ years of combined experience "
                 "right to your door.")],
         [B.figure("technician")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ------------------------------------------------------------ 3. COVERAGE
coverage = B.sec_paper([
    B.section_title([
        B.eyebrow("Coverage"),
        B.h2("Communities We Proudly Serve"),
        B.lead("We provide full-service residential heating, cooling, and home "
               "efficiency solutions to Loganville and the surrounding regional "
               "areas:"),
    ]),
    B.ratio_row(
        [[B.gmap()],
         [B.area_list(B.FACTS["cities_primary"]),
          B.body("Don&rsquo;t see your town listed above? Give our office a call at "
                 '<a href="%s" style="color:%s;text-decoration:underline;'
                 'text-underline-offset:2px;">%s</a>. We&rsquo;ll be happy to check '
                 "our schedule and see if we can accommodate your home!"
                 % (PH["tel"], B.RED_TEXT, PH["display"]),
                 "base", color=B.MUTED,
                 extra={"_margin": B.margin(22, 0, 0, 0)})]],
        ratios=[1.3, 1], gap_px=48, align="flex-start", col_gap=0),
])
coverage["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------------------ 4. WHAT WE OFFER
HEATING_COOLING = [
    ("24/7 Emergency HVAC Repair",
     "Live after-hours dispatch for sudden central AC and heating "
     "breakdowns&mdash;no automated runarounds."),
    ("New Carrier&reg; System Installs",
     "High-efficiency heat pumps, air conditioners, and furnaces backed by free "
     "upfront estimates and our Parts &amp; Labor Guarantee."),
    ("Ductless Mini-Splits",
     "Precision, single or multi-zone heating and cooling for room additions, "
     "garages, or spaces without ductwork."),
]
EFFICIENCY = [
    ("Crawl Space Encapsulation",
     "Heavy-duty vapor barriers, active dehumidification, and mold prevention to "
     "protect your home&rsquo;s foundation and air quality."),
    ("Attic Insulation &amp; Humidity Control",
     "Blown-in insulation and whole-home moisture control to balance sticky air and "
     "slash monthly energy bills."),
    ("Comfort Club Maintenance",
     "Join over 300 local members receiving two annual system tune-ups, priority "
     "emergency dispatch, and exclusive repair discounts."),
]

offer = B.sec_about([
    B.section_title([
        B.eyebrow("Services"),
        B.h2("What We Offer in Your Neighborhood"),
        B.lead("Whether you need urgent midnight repairs or long-term efficiency "
               "upgrades, Mid Lakes HVAC delivers reliable, full-service home "
               "comfort solutions straight to your door."),
    ]),
    B.ratio_row(
        [[B.h("Heating &amp; Cooling Solutions", "card_h3",
              extra={"_margin": B.margin(0, 0, 20, 0)}),
          B.promise(HEATING_COOLING)],
         [B.h("Total Home Efficiency &amp; Air Quality", "card_h3",
              extra={"_margin": B.margin(0, 0, 20, 0)}),
          B.promise(EFFICIENCY)]],
        ratios=[1, 1], gap_px=48, align="flex-start", col_gap=0),
    B.actions([B.btn_primary("See All Services", L["services"])]),
])
offer["elements"][0]["settings"]["flex_gap"] = B.gap(36)


# ----------------------------------------------------------------- 5. FAQ
FAQ = [
    ("How quickly can a technician get to my home if I&rsquo;m outside Loganville?",
     "Response times depend on daily technician routing, but our central Loganville "
     "location allows us to reach surrounding communities across Walton and Gwinnett "
     "Counties promptly."),
    ("How does after-hours and weekend service work?",
     "When you call outside of our standard Monday&ndash;Friday office hours, our "
     "24/7 after-hours call service routes your call directly to an on-call team "
     "member so we can dispatch help when you need it most."),
    ("Do you offer free estimates on replacement systems in all service areas?",
     "Yes! We provide 100% free estimates on new Carrier&reg; system installations "
     "across our entire coverage footprint."),
]

faq = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("FAQs"),
          B.h2("Frequently Asked Questions"),
          B.faq(FAQ, first_open=False)],
         [B.figure("vents", "Central to Walton &amp; Gwinnett.",
                   "Our Loganville base keeps response times short across the "
                   "region.")]],
        ratios=[1.3, 1], gap_px=56, align="flex-start", col_gap=32),
], anchor="faq")


# ------------------------------------------------------------- 6. CONTACT
contact = B.contact(
    "Need Fast HVAC Service in Your Area?",
    ["Don&rsquo;t wait for a complete system breakdown. Contact the Mid Lakes team "
     "today for fast, reliable local service."],
    [("Direct Phone", B.phone_link(), "24/7 Emergency Line"),
     ("Office Location", B.FACTS["address"], None),
     ("Standard Office Hours", "Monday &ndash; Friday: 8:00 AM &ndash; 5:00 PM", None),
     ("After-Hours Support", "Available 24 Hours a Day, 7 Days a Week", None)],
    B.quote_form(),
)
contact["elements"][0]["elements"][0]["elements"][0]["elements"].append(
    B.actions([B.btn_primary("Call %s" % PH["display"], PH["tel"])]))


SECTIONS = [hero, local, coverage, offer, faq, contact]

if __name__ == "__main__":
    B.write(B.page("Service Areas", SECTIONS), "service-area.json", HERE)
