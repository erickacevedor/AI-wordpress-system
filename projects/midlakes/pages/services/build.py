# -*- coding: utf-8 -*-
"""
Mid Lakes — Services (/services/).

A 1:1 port of source.php. Copy is VERBATIM, entities included.

Band order (KIT-ANALYSIS §4):
    hero · section-nav · white · paper · white · comfort · paper · white · ink

⚠️ ALTERNATIONS restated here (Elementor has no positional selector):
  · `.detail-row:first-of-type` drops its top border and pads 8px — detail_row()
    takes the 0-based index WITHIN ITS SECTION, so both bands restart at 0.
  · On this page the FLIPPED rows are the ones carrying the blue spec card. That
    pairing is the pattern, not a coincidence: rows run red, blue, red / red, blue,
    red, and `flip` drives both the order and the card colour.

Run:
    python3 projects/midlakes/pages/services/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/services/services.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x42000000)

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "ductwork",
    "HVAC &amp; Home Comfort Services in Loganville, GA",
    "When your home isn&rsquo;t comfortable, you want a local team you can trust to "
    "find the problem and make it right.",
    [B.btn_primary("Schedule Service", L["contact"]),
     B.btn_ghost("Call %s" % PH["display"], PH["tel"])],
    creds=[("24/7", "Emergency Service"),
           ("75+", "Years Combined Experience"),
           ("100%", "Licensed &amp; Insured"),
           ("Parts &amp; Labor", "Guarantee")],
    interior=True)


# --------------------------------------------------------- 2. SECTION NAV
nav = B.section_nav([
    ("HVAC Repair &amp; Maintenance", "#hvac-repair"),
    ("Ductless / Mini-Split", "#ductless"),
    ("Thermostats", "#thermostats"),
    ("Crawl Space Encapsulation", "#crawl-space"),
    ("Attic Insulation", "#attic-insulation"),
    ("Humidity Control", "#humidity"),
])


# ---------------------------------------------------------------- 3. INTRO
intro = B.sec_about([
    B.section_title([
        B.lead("Mid Lakes HVAC provides dependable heating, cooling, and whole-home "
               "comfort services for families throughout Madison, Loganville, and "
               "surrounding Georgia communities. From urgent HVAC repairs and "
               "seasonal maintenance to ductless systems, insulation, humidity "
               "control, and crawl space improvements, our team brings decades of "
               "hands-on experience to every home we serve."),
        B.lead("We&rsquo;re family-owned, locally operated, and committed to giving "
               "our neighbors straightforward recommendations, quality workmanship, "
               "and service we&rsquo;re proud to stand behind."),
    ], gap_px=14),
])


# --------------------------------------------------- 4. HEATING & COOLING
heating = B.sec_paper([
    B.section_title([
        B.eyebrow("Heating &amp; Cooling"),
        B.h2("Heating &amp; Cooling Services"),
        B.lead("Your heating and cooling system should keep your family comfortable "
               "without constant headaches."),
        B.lead("Whether you need a repair, seasonal maintenance, or a better "
               "solution for a hard-to-comfort room, our team is here to help you "
               "understand what&rsquo;s going on and find the right way forward."),
    ]),
    B.detail_row(
        0, "hvac-repair", "HVAC Repair &amp; Maintenance",
        ["When your heating or cooling system isn&rsquo;t doing its job, you "
         "shouldn&rsquo;t have to guess what&rsquo;s wrong.",
         "Mid Lakes HVAC provides professional HVAC repair and preventive "
         "maintenance for central heating and cooling systems. Our technicians take "
         "the time to inspect your equipment, diagnose the problem, and explain what "
         "we find so you can make a confident decision about your home.",
         "Routine maintenance is just as important. Seasonal service can help your "
         "equipment run more efficiently, reduce unnecessary wear, and give us a "
         "chance to catch developing problems before they leave your family without "
         "heating or cooling.",
         "For homeowners who want to make ongoing maintenance easier, Mid Lakes HVAC "
         'also offers the <a href="%s" style="color:%s;text-decoration:underline;'
         'text-underline-offset:2px;">Mid Lakes Comfort Club</a>.'
         % (L["service_agreements"], B.RED_TEXT)],
        ("Schedule HVAC Repair or Maintenance", L["contact"]),
        B.spec_card("We can help with issues such as:", [
            "AC or heating systems that won&rsquo;t turn on",
            "Weak or inconsistent airflow",
            "Uneven temperatures throughout the home",
            "Unusual noises or odors",
            "Frequent system cycling",
            "Equipment that runs constantly",
            "Poor heating or cooling performance",
            "Unexpected system breakdowns",
        ])),
    B.detail_row(
        1, "ductless", "Ductless / Mini-Split Systems",
        ["Some rooms are simply harder to keep comfortable than others. A home "
         "addition, bonus room, garage, workshop, or older property without existing "
         "ductwork may need a different approach.",
         "Ductless mini-splits provide flexible, efficient heating and cooling "
         "without requiring a traditional duct system. Mid Lakes HVAC provides "
         "complete ductless installation, repair, and maintenance services to help "
         "you get dependable comfort where you need it.",
         "<strong>Ductless / Mini-Split Installation.</strong> Every home is "
         "different, so we don&rsquo;t believe in a one-size-fits-all approach. Our "
         "team can help determine the right system size, number of indoor units, and "
         "configuration based on your space and comfort goals.",
         "<strong>Ductless / Mini-Split Repair.</strong> If your mini-split "
         "isn&rsquo;t heating or cooling properly, starts leaking, makes unusual "
         "noises, or stops responding, we&rsquo;ll diagnose the issue and explain "
         "your repair options clearly.",
         "<strong>Ductless / Mini-Split Maintenance.</strong> Routine maintenance "
         "helps keep your ductless equipment clean, efficient, and ready for the "
         "seasons ahead. It can also help catch small issues before they turn into "
         "larger repairs.",
         "Whether you&rsquo;re considering your first mini-split or need help with a "
         "system already in your home, our team is ready to help."],
        ("Request Ductless Service", L["contact"]),
        B.spec_card("A ductless system can provide:", [
            "Individual room or zone control",
            "Efficient heating and cooling",
            "Quiet operation",
            "Flexible installation options",
            "Comfort without extensive ductwork",
        ], blue=True),
        flip=True),
    B.detail_row(
        2, "thermostats", "Thermostat Repair &amp; Upgrades",
        ["Your thermostat may be small, but it has a big job. When it isn&rsquo;t "
         "communicating properly with your HVAC system, you may notice inconsistent "
         "temperatures, unusual cycling, or equipment that doesn&rsquo;t respond when "
         "you change the settings.",
         "Mid Lakes HVAC provides thermostat repair, replacement, and installation "
         "services.",
         "We&rsquo;ll check both the thermostat and your HVAC controls to determine "
         "where the problem is really coming from. If a repair makes sense, "
         "we&rsquo;ll tell you. If replacement is the better option, we&rsquo;ll walk "
         "you through your choices without pushing features you don&rsquo;t need.",
         "For homeowners looking for easier control, we can also install compatible "
         "modern thermostats, including options such as:",
         "We&rsquo;ll make sure your new thermostat is properly matched to your "
         "equipment and set up to work the way it should."],
        ("Schedule Thermostat Service", L["contact"]),
        B.spec_card("Including options such as:", [
            "Programmable thermostats",
            "Smart thermostats",
            "Wi-Fi-enabled controls",
            "Temperature scheduling",
            "Remote system management",
        ])),
])
heating["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------- 5. WHOLE-HOME COMFORT
whole_home = B.sec_about([
    B.section_title([
        B.eyebrow("Whole-Home Comfort"),
        B.h2("Whole-Home Comfort &amp; Efficiency"),
        B.lead("Sometimes the problem isn&rsquo;t your HVAC equipment at all."),
        B.lead("Poor insulation, excess humidity, or moisture beneath your home can "
               "make your heating and cooling system work harder and leave certain "
               "rooms feeling uncomfortable. That&rsquo;s why Mid Lakes HVAC looks "
               "beyond the equipment itself when your home isn&rsquo;t feeling the "
               "way it should."),
    ]),
    B.detail_row(
        0, "crawl-space", "Crawl Space Encapsulation",
        ["What happens beneath your home can affect the comfort above it.",
         "When ground moisture and humid outdoor air enter an unprotected crawl "
         "space, they can contribute to high humidity, musty odors, mold-friendly "
         "conditions, and deterioration of materials beneath the home.",
         "Crawl space encapsulation helps separate the area from outside moisture and "
         "creates a cleaner, more controlled environment.",
         "Our team can take a look at your crawl space, explain what we&rsquo;re "
         "seeing, and recommend an approach that makes sense for your property."],
        ("Request a Crawl Space Estimate", L["contact"]),
        B.spec_card("Encapsulation can help:", [
            "Reduce crawl space moisture",
            "Control humidity beneath the home",
            "Reduce conditions that encourage mold growth",
            "Help protect structural materials",
            "Minimize musty odors",
            "Support more comfortable indoor conditions",
            "Improve the overall efficiency of the home",
        ])),
    B.detail_row(
        1, "attic-insulation", "Attic Insulation",
        ["If your home is difficult to keep comfortable, your attic may be part of "
         "the problem.",
         "Inadequate insulation allows heat to move more easily between the attic and "
         "your living space. During Georgia summers, that can mean more heat entering "
         "the home. In colder weather, it can allow the warmth you&rsquo;re paying "
         "for to escape.",
         "Mid Lakes HVAC provides attic insulation upgrades designed to help your "
         "home hold onto conditioned air and make life a little easier on your HVAC "
         "system.",
         "If certain rooms are always too hot or too cold, or your system seems to "
         "run more than it should, we can help determine whether your attic "
         "insulation may be contributing to the problem."],
        ("Get a Free Insulation Estimate", L["contact"]),
        B.spec_card("Proper insulation can help:", [
            "Reduce summer heat gain",
            "Reduce winter heat loss",
            "Maintain more consistent indoor temperatures",
            "Keep conditioned air inside the living space",
            "Reduce unnecessary HVAC workload",
            "Support improved energy efficiency",
        ], blue=True),
        flip=True),
    B.detail_row(
        2, "humidity", "Humidity Control &amp; Air Quality",
        ["Anyone who lives in Georgia knows the humidity doesn&rsquo;t always stay "
         "outside.",
         "When moisture levels inside your home get too high, the air can feel sticky "
         "or clammy even when the thermostat says the temperature should be "
         "comfortable. Excess humidity can also contribute to condensation, musty "
         "odors, dust mites, and conditions that support mold growth.",
         "Mid Lakes HVAC provides humidity-control solutions designed to help your "
         "home feel more balanced and comfortable.",
         "We&rsquo;ll listen to what you&rsquo;ve been noticing in your home, "
         "evaluate the conditions, and recommend a solution that works with your "
         "existing comfort system."],
        ("Ask About Humidity Control", L["contact"]),
        B.spec_card("Better humidity management can help:", [
            "Improve indoor comfort",
            "Reduce sticky or clammy air",
            "Limit excess moisture",
            "Reduce condensation",
            "Create less favorable conditions for mold and dust mites",
            "Help protect furnishings and building materials",
            "Support healthier indoor air conditions",
        ])),
])
whole_home["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------------- 6. 24/7 EMERGENCY
emergency = B.comfort(
    "technician", "Around the clock", "24/7 Emergency HVAC Service",
    ["Heating and cooling problems don&rsquo;t check the clock before they happen.",
     "If your system stops working unexpectedly and your family needs help after "
     "regular business hours, Mid Lakes HVAC offers 24/7 emergency service. Our "
     "after-hours team is available for urgent heating and cooling problems "
     "throughout our service area.",
     "You&rsquo;ll have a local team to call when you need one most. Call %s for "
     "24/7 emergency HVAC service." % PH["display"]],
    buttons=[B.btn_primary("Call Now", PH["tel"])])


# --------------------------------------------------------- 7. COMFORT CLUB
# ⚠️ These service cards carry NO icon in the prototype, so there is no red/blue
# tile alternation to restate on this page.
club = B.sec_paper([
    B.section_title([
        B.eyebrow("Comfort Club"),
        B.h2("Keep Your HVAC System Ready for Every Season"),
        B.lead("A little preventive care can go a long way toward avoiding an "
               "inconvenient breakdown on the hottest or coldest day of the year."),
        B.lead("The Mid Lakes Comfort Club makes it easier to stay on top of routine "
               "HVAC maintenance with:"),
    ]),
    B.grid([
        B.service_card(0, None, "Two Annual Tune-Ups",
                       "one for cooling season and one for heating season"),
        B.service_card(1, None, "Priority 24/7 Dispatch", "on emergency calls"),
        B.service_card(2, None, "Exclusive Discounts",
                       "on qualifying repairs and equipment upgrades"),
    ], cols=3, tablet=2, mobile=1, gap_px=20),
    B.lead("Regular servicing can help maintain system performance, catch developing "
           "issues early, and protect the equipment your family depends on "
           "year-round.", extra={"_margin": B.margin(28, 0, 0, 0)}),
    B.actions([B.btn_primary("Join the Mid Lakes Comfort Club",
                             L["service_agreements"])]),
])
club["elements"][0]["settings"]["flex_gap"] = B.gap(24)


# ------------------------------------------------------------- 8. COVERAGE
coverage = B.sec_about([
    B.section_title([
        B.eyebrow("Coverage"),
        B.h2("Proud to Serve Our Neighbors Across the Area"),
        B.lead("Mid Lakes HVAC provides heating, cooling, and home comfort services "
               "for homeowners throughout Loganville and surrounding Georgia "
               "communities, including:"),
    ]),
] + B.chips(
    B.FACTS["cities_extended"],
    note="Don&rsquo;t see your community listed? "
         '<a href="%s" style="color:%s;text-decoration:underline;'
         'text-underline-offset:2px;">Give us a call</a> and we&rsquo;ll let you know '
         "whether service is available in your area." % (PH["tel"], B.RED_TEXT)))
coverage["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ---------------------------------------------------------------- 9. CONTACT
contact = B.contact(
    "Your Local Team for a More Comfortable Home",
    ["You don&rsquo;t have to know exactly what&rsquo;s wrong before you call us.",
     "Tell us what&rsquo;s going on, and we&rsquo;ll give you an honest "
     "recommendation for the best way forward. Whether you need a repair, a "
     "maintenance visit, a ductless system, or a whole-home comfort improvement, you "
     "can count on Mid Lakes HVAC to treat your home with the same care and respect "
     "we&rsquo;d expect in our own.",
     "As a family-owned and locally operated company, we take pride in serving the "
     "families and communities around us. With 75+ years of combined experience, 24/7 "
     "emergency availability, licensed and insured service, and a Parts &amp; Labor "
     "Guarantee, we&rsquo;re here to help you feel comfortable about both your home "
     "and the work being done in it.",
     "Call %s or schedule your service online today." % PH["display"]],
    None,
    B.quote_form(),
)
# This page closes with a Call button under the copy instead of a details list.
contact["elements"][0]["elements"][0]["elements"][0]["elements"].append(
    B.actions([B.btn_primary("Call %s" % PH["display"], PH["tel"])]))


SECTIONS = [hero, nav, intro, heating, whole_home, emergency, club, coverage, contact]

if __name__ == "__main__":
    B.write(B.page("Services", SECTIONS), "services.json", HERE)
