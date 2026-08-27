# -*- coding: utf-8 -*-
"""
Mid Lakes — Service Agreements (/service-agreements/).

A 1:1 port of source.php. Copy is VERBATIM, entities included.

Band order (KIT-ANALYSIS §4):
    hero · white · paper · white · WHITE · paper · ink
                           ^^^^^^^^^^^^^
⚠️ Sections 4 and 5 are BOTH white, back to back. Deliberate — see the "do NOT fix"
list in midlakes-page-audit. validate-page.py warns; the warning is expected.

⚠️ Section 5 is `.about.what-happens`, which suppresses the wave watermarks.

⚠️ This page carries the ONLY tabular data on the site. The rate table ships as one
`html` widget styled entirely by the child theme's .ml-rate-table — there is no table
widget, and the <620px behaviour (hide the header row, turn each row into a card) is
pure CSS.

Run:
    python3 projects/midlakes/pages/service-agreements/build.py
    python3 scripts/validate-page.py \\
        projects/midlakes/pages/service-agreements/service-agreements.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x43000000)

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "technician",
    "HVAC Service Agreements in Loganville, GA",
    "Join over 300 local homeowners who trust Mid Lakes HVAC for year-round system "
    "tune-ups, priority service, and lower energy bills.",
    [B.btn_primary("Call to Enroll: %s" % PH["display"], PH["tel"])],
    interior=True)


# -------------------------------------------------------- 2. COMFORT CLUB
club = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Comfort Club"),
          B.h2("Protect Your Investment &amp; Avoid Unexpected Breakdowns"),
          B.lead("Your heating and air conditioning system is one of the biggest "
                 "investments in your home. Just like changing the oil in your car, "
                 "regular preventive maintenance extends the life of your equipment, "
                 "preserves your manufacturer warranty, and keeps your monthly "
                 "utility bills as low as possible."),
          B.lead("With a Mid Lakes HVAC Service Agreement, you never have to worry "
                 "about remembering to schedule your seasonal tune-ups. Our NATE and "
                 "EPA-certified technicians handle the care for you, keeping your "
                 "home comfortable in every season across Walton, Gwinnett, DeKalb, "
                 "and surrounding counties.")],
         [B.figure("wall-units")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ------------------------------------------------------------- 3. PRICING
pricing = B.sec_paper([
    B.section_title([
        B.eyebrow("Pricing"),
        B.h2("Simple, Transparent Pricing with Zero Commitment"),
        B.lead("We keep our service agreements simple, transparent, and affordable. "
               "There are no hidden fees, long-term contracts, or cancellation "
               "penalties&mdash;you only pay at the time of your service."),
    ]),
    B.rate_table(
        [("Primary System", "$95 per service visit",
          "Includes complete Spring AC &amp; Fall Heating tune-ups"),
         ("Each Additional System", "+$45 per extra unit",
          "Added to the primary rate for multi-zone homes"),
         ("Cancellation Policy", "$0 penalty",
          "Cancel or modify your service agreement at any time")],
        headers=["Coverage Type", "Semi-Annual Rate", "Details"]),
])
pricing["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------------------ 4. INCLUDED
# ⚠️ No icons on these cards in the prototype, so no red/blue tile alternation.
INCLUDED = [
    ("Two Annual Tune-Ups",
     "Comprehensive seasonal maintenance, one Spring AC tune-up and one Fall Heating "
     "tune-up, to prepare your system for extreme Georgia weather."),
    ("5% Member Discount on Repairs",
     "Agreement holders enjoy 5% off all needed replacement parts, repairs, and "
     "labor."),
    ("Priority 24/7 Dispatch",
     "Agreement members skip the line with priority scheduling on all service calls, "
     "including late-night and weekend emergencies."),
    ("Lower Monthly Energy Bills",
     "Properly cleaned and calibrated systems run at peak efficiency, helping slash "
     "monthly power costs."),
    ("Extended Equipment Lifespan",
     "Regular tune-ups catch minor wear-and-tear before it turns into a major, "
     "expensive system breakdown."),
    ("Warranty Protection",
     "Major HVAC manufacturers require documented proof of annual professional "
     "maintenance to keep valid warranty coverage on parts."),
]

included = B.sec_about([
    B.section_title([
        B.eyebrow("Included"),
        B.h2("What&rsquo;s Included in Your Mid Lakes Service Agreement"),
        B.lead("Our preventive service program is designed to give you total peace "
               "of mind and exclusive financial savings throughout the year:"),
    ]),
    B.grid([B.service_card(i, None, t, c) for i, (t, c) in enumerate(INCLUDED)],
           cols=3, tablet=2, mobile=1, gap_px=20),
])
included["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# --------------------------------------------------------- 5. INSPECTIONS
# ⚠️ `.about.what-happens` — the wave pair is display:none here in the prototype.
inspections = B.sec_about([
    B.section_title([
        B.eyebrow("Inspections"),
        B.h2("What Happens During Your Seasonal Tune-Ups?"),
        B.lead("Our certified technicians bring over 75 years of combined experience "
               "to every inspection."),
    ]),
    B.ratio_row(
        [[B.spec_card("Spring Air Conditioning Tune-Up Checklist", [
            "Inspect and clean evaporator &amp; condenser coils",
            "Check refrigerant charge levels &amp; system operating pressure",
            "Inspect &amp; flush condensate drain lines to prevent water damage",
            "Test capacitors, relays, &amp; electrical connections for safety",
            "Calibrate thermostat &amp; verify proper home airflow",
          ], blue=True)],
         [B.spec_card("Fall Heating System Tune-Up Checklist", [
            "Inspect heat exchanger &amp; burner assembly for safe operation",
            "Test safety controls &amp; ignition systems",
            "Inspect blower motor &amp; check internal electrical components",
            "Inspect gas line connections &amp; vent piping",
            "Replace or inspect standard air filters",
          ])]],
        ratios=[1, 1], gap_px=48, align="stretch"),
], watermark=False)
inspections["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ----------------------------------------------------------------- 6. FAQ
FAQ = [
    ("When does my service agreement kick in after I sign up?",
     "Your coverage begins immediately upon enrollment. We&rsquo;ll work with you to "
     "schedule your first seasonal tune-up right away or queue it up for the upcoming "
     "Spring/Fall maintenance window based on your system&rsquo;s current needs."),
    ("Do I need to be home for the entire tune-up appointment?",
     "Yes, an adult over 18 needs to be present. Because our technicians perform "
     "complete indoor and outdoor checks, including thermostat calibration, indoor "
     "coil inspections, and electrical testing, we need access to both your outdoor "
     "unit and interior equipment."),
    ("Will I receive reminders when it&rsquo;s time for my Spring or Fall tune-up?",
     "Absolutely. You don&rsquo;t have to keep track of the calendar. Our team will "
     "reach out via call, text, or email ahead of each season to schedule your "
     "appointment at a time that works best for your schedule."),
    ("What if a technician finds a problem during my inspection?",
     "If we spot worn components or potential issues during your tune-up, our "
     "technician will explain the findings clearly and present your options before "
     "doing any extra work. As an agreement holder, you&rsquo;ll automatically "
     "receive your 5% discount on any needed replacement parts or repairs."),
]

faq = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("FAQs"),
          B.h2("Service Agreement FAQs"),
          # ⚠️ No item ships open on this page — unlike the home page's first item.
          B.faq(FAQ, first_open=False)],
         [B.figure("vents", "Two visits a year.",
                   "One Spring AC tune-up and one Fall heating tune-up, scheduled "
                   "for you.")]],
        ratios=[1.3, 1], gap_px=56, align="flex-start", col_gap=32),
], anchor="faq")


# ------------------------------------------------------------- 7. CONTACT
contact = B.contact(
    "Ready to Protect Your Home Investment?",
    ["Enrolling in our service agreement takes less than two minutes. Give the Mid "
     "Lakes team a call today or fill out the request form below."],
    [("Direct Phone", B.phone_link(), "24/7 Emergency Line"),
     ("Office Location", B.FACTS["address"], None),
     ("Hours", "Mon&ndash;Fri: 8:00 AM &ndash; 5:00 PM",
      "24/7 After-Hours Emergency Support"),
     ("License", B.FACTS["license"], None)],
    B.quote_form(),
)
contact["elements"][0]["elements"][0]["elements"][0]["elements"].append(
    B.actions([B.btn_primary("Call %s to Enroll" % PH["display"], PH["tel"])]))


SECTIONS = [hero, club, pricing, included, inspections, faq, contact]

if __name__ == "__main__":
    B.write(B.page("Service Agreements", SECTIONS), "service-agreements.json", HERE)
