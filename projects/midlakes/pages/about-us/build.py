# -*- coding: utf-8 -*-
"""
Mid Lakes — About (/about-us/).

A 1:1 port of source.php. Copy is VERBATIM, entities included.

Band order (KIT-ANALYSIS §4):
    hero · white · paper · white · WHITE · comfort · paper · white · ink
                                   ^^^^^
⚠️ Sections 4 and 5 are BOTH white, back to back. That is the prototype, not a
mistake — see the "do NOT fix" list in midlakes-page-audit. validate-page.py warns
about it; the warning is expected and is recorded in HANDOFF-notes.md.

⚠️ Section 8 is `.about.what-happens`, which suppresses the wave watermarks
(display:none in the prototype). Built with sec_about(watermark=False).

Run:
    python3 projects/midlakes/pages/about-us/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/about-us/about-us.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x41000000)

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "hero-hvac",
    "About Mid Lakes Heating &amp; Cooling",
    "You don&rsquo;t want a faceless call center or a hard sell when your house is "
    "uncomfortable. You want a local team that will take your call, be there when "
    "they say they will, and provide you with an honest recommendation. We set out "
    "to create that kind of business.",
    [B.btn_primary("Request Service", L["contact"]),
     B.btn_ghost("Call %s" % PH["display"], PH["tel"])],
    creds=[("Veteran-Owned", "&amp; Family-Operated"),
           ("Since 2018", "Serving Metro Atlanta &amp; Northeast GA"),
           ("Licensed", "&amp; Insured"),
           ("Parts &amp; Labor", "Guarantee")],
    interior=True)


# ------------------------------------------------------------ 2. WHO WE ARE
who = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Who we are"),
          B.h2("Your Neighbors in Home Comfort, Right Here in Loganville"),
          B.lead("Mid Lakes Heating &amp; Cooling was established in 2018 and is "
                 "based in Loganville. It is a family-run business that operates "
                 "locally and is based on the straightforward principle of treating "
                 "every customer like a neighbor and every home like our own.")],
         [B.stats([("2018", "Founded in Loganville"),
                   ("300+", "Comfort Club members"),
                   ("75+", "Years of combined experience")])]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=20),
])


# -------------------------------------------------------------- 3. OUR STORY
story = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("Our story"),
          B.h2("Built on Doing the Right Thing"),
          B.lead("Giving our neighbors a heating and cooling company they can "
                 "genuinely trust was the simple initial goal of Mid Lakes Heating "
                 "&amp; Cooling. Honest, trustworthy, and truly local&mdash;not the "
                 "biggest or most ostentatious."),
          B.lead("One repair and one cozy house at a time, we have expanded since "
                 "2018 by doing the right thing for our clients. Our technicians "
                 "have over 75 years of combined experience, but what really makes "
                 "us stand out is the way we treat people: honest responses, "
                 "excellent work, and no pressure.")],
         [B.figure("ductwork")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# --------------------------------------------------------------- 4. OWNERSHIP
owner = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Ownership"),
          B.h2("Meet the Owner: John Jessup"),
          B.lead("Born in Georgia, John Jessup was raised in Loganville, where he "
                 "currently resides with his spouse. John joined the US Army after "
                 "graduating from high school and spent three years serving his "
                 "country. In 1993, he graduated from the University of Georgia with "
                 "a degree in accountancy."),
          B.lead("John is in charge of Mid Lakes Heating &amp; Cooling&rsquo;s "
                 "accounting, banking, insurance, and administrative "
                 "departments&mdash;the back-end work that keeps everything honest "
                 "and efficient for each and every client."),
          B.lead("As a member of the Walton County Board of Education, John is also "
                 "quite active in the community where he was raised. He enjoys "
                 "fishing, hunting, watching college football, and yes, supporting "
                 "the Dawgs, when he&rsquo;s not working or giving back to the "
                 "community.")],
         [B.figure("technician")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ------------------------------------------------------------- 5. OUR VALUES
# ⚠️ .why-grid--three — /about-us/ lists THREE values, so the grid is 3-up here; a
# 2-up grid would leave a hole. Numerals still alternate red, blue, red.
VALUES = [
    ("Honest Recommendations",
     "We&rsquo;ll make the necessary repairs and clearly advise you when a "
     "replacement is the better course of action. There is no compulsion to upsell "
     "unnecessary items."),
    ("We Treat Your Home Like Ours",
     "Because we would want the same in our own homes, our professionals respect "
     "your space, arrive prepared, and work carefully."),
    ("We Look at the Whole Home",
     "Sometimes the equipment isn&rsquo;t the issue. In order to address the true "
     "problem, we examine beyond the furnace and air conditioner to insulation, "
     "humidity, and what&rsquo;s going on beneath your house."),
]

values = B.sec_why([
    B.section_title([B.eyebrow("Our values"), B.h2("What We Stand For")]),
    B.grid([B.why_card(i, t, c) for i, (t, c) in enumerate(VALUES, start=1)],
           cols=3, tablet=2, mobile=1, gap_px=20),
])
values["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------------------- 6. BEYOND HVAC
beyond = B.comfort(
    "vents", "Beyond HVAC", "The Work Most Companies Stop Short Of",
    ["The equipment is where most heating and cooling companies end up. We "
     "don&rsquo;t. Mid Lakes assists with crawl space encapsulation, attic "
     "insulation, and humidity control in addition to HVAC repair, maintenance and "
     "installation&mdash;the whole-house upgrades that reduce system effort and "
     "improve the consistency of your rooms. It&rsquo;s what makes us different."],
    buttons=[B.btn_primary("Explore Our Services", L["services"])])


# ------------------------------------------------------------ 7. CREDENTIALS
creds = B.sec_paper([
    B.section_title([B.eyebrow("Credentials"),
                     B.h2("Why Homeowners Choose Mid Lakes")]),
    B.ratio_row(
        [[B.spec_card("Certified &amp; qualified", [
            "<strong>Carrier Dealer:</strong> We install high-end, long-lasting, "
            "high-efficiency systems.",
            "<strong>NATE-Certified Technicians:</strong> Trained and tested to the "
            "industry&rsquo;s leading standard.",
            "<strong>EPA 608 Certified:</strong> Qualified to safely handle "
            "refrigerant systems.",
            "<strong>Licensed &amp; Insured:</strong> You may be sure of "
            "professional, code-compliant work.",
          ], blue=True)],
         [B.spec_card("Backed by our promise", [
            "<strong>Parts &amp; Labor Guaranty:</strong> We firmly support the "
            "quality of our work on every project.",
            "<strong>24/7 Emergency Service:</strong> When your system malfunctions "
            "after hours, a real, local person responds.",
            "<strong>Free Estimates:</strong> No-obligation, 100% free estimates for "
            "new installs.",
          ])]],
        ratios=[1, 1], gap_px=48, align="stretch"),
    B.body("More than 300 local homeowners who rely on us to maintain their systems "
           "throughout the year are members of the Comfort Club &mdash; see our "
           '<a href="%s" style="color:%s;text-decoration:underline;'
           'text-underline-offset:2px;">service agreements</a>.'
           % (L["service_agreements"], B.RED_TEXT),
           "base", color=B.MUTED, extra={"_margin": B.margin(22, 0, 0, 0)}),
])
creds["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# -------------------------------------------------------------- 8. COMMUNITY
# ⚠️ `.about.what-happens` — the wave pair is display:none here in the prototype.
community = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Community"),
          B.h2("Proud to Serve Our Community"),
          B.lead("Being local is more than simply our location; it&rsquo;s who we "
                 "are. We are committed to the community that sustains us, from "
                 "John&rsquo;s work on the Walton County Board of Education to the "
                 "daily tasks of making our neighbors comfortable."),
          B.lead("Mid Lakes serves homeowners across Gwinnett, DeKalb, Rockdale, "
                 "Newton, Walton, Athens-Clarke, Oconee, Morgan, Jasper, Greene, and "
                 "Putnam Counties."),
          B.actions([B.btn_primary("See Our Service Area", L["service_area"])])],
         [B.body("Counties we serve", "spec_label", color=B.MUTED)]
         + B.chips(B.FACTS["counties"])],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
], watermark=False)


# ---------------------------------------------------------------- 9. CONTACT
contact = B.contact(
    "Ready to Get Comfortable?",
    ["Whether you need a repair, a new system, seasonal maintenance, or a whole-home "
     "comfort improvement, we are happy to provide honest answers and service."],
    [("Direct Phone", B.phone_link(), "24/7 Emergency Line"),
     ("Office Location", B.FACTS["address"], None),
     ("Hours", "Mon&ndash;Fri: 8:00 AM &ndash; 5:00 PM",
      "24/7 After-Hours Emergency Support")],
    # ⚠️ This page's form heading differs from every other page's.
    B.quote_form("Schedule Service Online"),
)


SECTIONS = [hero, who, story, owner, values, beyond, creds, community, contact]

if __name__ == "__main__":
    B.write(B.page("About", SECTIONS), "about-us.json", HERE)
