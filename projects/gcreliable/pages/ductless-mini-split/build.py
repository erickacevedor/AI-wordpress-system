#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G.C. Reliable Service — "Dependable Ductless Mini-Split Services in New Rochelle, NY".

Reproducible build. Structure + responsive correctness come from
scripts/elementor_builder.py; the brand vocabulary (bands, cards, buttons, the
photo+badge, the Pro accordion) comes from projects/gcreliable/brand.py, which reads
projects/gcreliable/tokens.json. Only this page's copy and section order live here.

Source doc:  source.txt (extracted from "GC Reliable_COPY_Page_Ductless Mini-Split.docx")
Model page:  current-theme/content/page/225063.json ("AC Repair")

Run:  python projects/gcreliable/pages/ductless-mini-split/build.py
Then: python scripts/validate-page.py projects/gcreliable/pages/ductless-mini-split/ductless-mini-split.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))          # pages/<slug> -> projects/<site>
sys.path.insert(0, SITE)
import brand as B                                       # noqa: E402

B.reset(0x40000000)
L, IMG = B.LINKS, B.IMAGES
CTA = "Schedule an Appointment"

S = []

# ---------------------------------------------------------------- 1. HERO (gradient)
S.append(B.hero(
    "Ductless Mini-Split Services", "in New Rochelle, NY",
    "Targeted Heating and Cooling Without the Ductwork",
    CTA))

# ------------------------------------------------- 2. INTRO + photo/badge (white)
S.append(B.sec(B.WHITE, [B.row([
    B.col([
        B.h2("Flexible Comfort Where Traditional HVAC Falls Short"),
        B.body(
            "<p>One room stays hot every afternoon. A finished attic never feels like the rest of the "
            "house. An addition was built without extending the original ductwork. These are the kinds "
            "of comfort problems that can make ductless mini-splits worth considering.</p>"
            "<p>Ductless systems use indoor units connected to outdoor equipment to provide targeted "
            "heating and cooling without traditional ductwork. G.C. Reliable Service designs ductless "
            "solutions for homes and light-commercial properties in "
            '<a href="%s">New Rochelle</a> and throughout Westchester County, based on the property, '
            "existing HVAC equipment, and how each space is used.</p>"
            "<p>For older Westchester homes, additions, and finished spaces where installing new "
            "ductwork may be disruptive, ductless can provide another path to reliable comfort.</p>"
            % L["new_rochelle"]),
        B.btn(CTA, align="left"),
    ], width=52, gap=18),
    B.col([B.photo_badge(IMG["technician_2"], "40+",
                         "Years serving New Rochelle &amp; Westchester since 1980")],
          width=44),
], gap=44, align="center", wrap=True, mobile_dir="column-reverse",
   tablet_dir="column-reverse", justify="space-between")]))

# ------------------------------------------------- 3. IS DUCTLESS A FIT (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("Ductless May Be a Good Fit If You Have&hellip;", align="center"),
    B.body_center(
        "<p>Ductless is rarely about the equipment first. It is about a space that the existing "
        "system was never set up to handle.</p>"),
    B.row([
        B.col([
            B.h3("Spaces Ductless Handles Well"),
            B.check_list([
                "A finished attic, basement, or bonus room",
                "A new addition or converted garage",
                "An older home without central ductwork",
                "One room that stays hotter or colder than the rest",
                "A home office that needs independent temperature control",
                "Multiple areas with different comfort preferences",
            ]),
        ], width=56),
        B.card([
            B.h3("The Goal Is Not Simply to Add Equipment", color=B.RED),
            B.body(
                "<p>It is to solve the comfort problem with the right number of zones and the right "
                "amount of capacity.</p>"
                "<p>Sometimes that means a single indoor unit in one difficult room. Sometimes it "
                "means several zones &mdash; and sometimes extending your existing "
                '<a href="%s">air conditioning</a> or heating system is the better answer. We will '
                "tell you which.</p>" % L["air_conditioning"]),
        ], width=40),
    ], gap=44, align="stretch", wrap=True),
]))

# --------------------------------------------------- 4. SERVICES (white band)
S.append(B.sec(B.WHITE, [
    B.h2("Ductless Mini-Split Services Built Around Your Home", align="center"),
    B.body_center(
        "<p>G.C. Reliable provides ductless installation, replacement, repair, and maintenance with "
        "recommendations tailored to your property and comfort goals.</p>"),
    B.row([
        B.card([
            B.emoji("❄️"),
            B.h3("Installation &amp; Replacement"),
            B.body(
                "<p>Whether you are adding ductless for the first time or replacing an aging system, "
                "proper planning matters. We evaluate room size, layout, insulation, sun exposure, "
                "existing HVAC equipment, electrical requirements, and indoor-unit placement before "
                "recommending single-zone or multi-zone equipment.</p>"
                "<p>We also consider whether ductless should supplement your furnace, boiler, or "
                "central AC, or provide most of the heating and cooling for the space. If you already "
                "have a mini-split, we can help you compare repair and replacement based on its age, "
                "condition, performance, and repair history.</p>"),
        ], width=32),
        B.card([
            B.emoji("🔧"),
            B.h3("Repair"),
            B.body(
                "<p>One leaking indoor unit or uncomfortable zone does not automatically mean the "
                "entire system needs replacement.</p>"
                "<p>G.C. Reliable services all makes and models and offers 24/7 emergency HVAC "
                "availability when a heating or cooling problem cannot wait.</p>"),
        ], width=32),
        B.card([
            B.emoji("🧰"),
            B.h3("Maintenance"),
            B.body(
                "<p>Ductless systems still need regular care. Filters require routine cleaning, while "
                "coils, drains, electrical components, refrigerant performance, and outdoor equipment "
                "should be inspected periodically.</p>"
                '<p>Professional <a href="%s">maintenance</a> can identify drainage, airflow, '
                "electrical, or performance concerns before they interrupt comfort and help keep every "
                "zone operating as intended.</p>" % L["maintenance"]),
        ], width=32),
    ], gap=22, align="stretch", wrap=True),
    B.card([
        B.h3("Call for Service If You Notice", color=B.RED),
        B.check_list([
            "Weak or warm airflow",
            "Water leaking from an indoor unit",
            "Unusual noises",
            "Ice buildup",
            "Frequent starts and stops",
            "Error codes or failure to turn on",
            "One zone working while another does not",
        ]),
    ]),
]))

# ------------------------------------------------ 5. ONE ZONE OR SEVERAL (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("One Zone or Several? Choosing the Right Ductless Setup", align="center"),
    B.body_center(
        "<p>Ductless gives you flexibility, but more zones are not automatically better. The right "
        "setup depends on which spaces need conditioning, how those rooms connect, and whether "
        "ductless will supplement or replace another HVAC system.</p>"),
    B.row([
        B.card([
            B.h3("Single-Zone Ductless Systems"),
            B.body(
                "<p>A single-zone system pairs one indoor unit with compatible outdoor equipment. It "
                "can be a practical choice for one defined problem area:</p>"),
            B.check_list([
                "A finished attic",
                "A home office",
                "An addition",
                "A converted garage",
                "A bedroom with poor airflow",
            ]),
            B.body(
                "<p>If the rest of the home is comfortable, treating one difficult space may make more "
                "sense than changing the entire HVAC system.</p>"),
        ], width=48),
        B.card([
            B.h3("Multi-Zone Ductless Systems"),
            B.body(
                "<p>Multi-zone systems connect several indoor units to compatible outdoor equipment, "
                "allowing different areas to maintain separate temperatures.</p>"
                "<p>They can work well in homes without ductwork, or properties with several areas "
                "that need individual control.</p>"
                "<p>One indoor unit does not necessarily cool several closed rooms effectively. Doors, "
                "hallways, room layout, and airflow all matter, so the number of zones should reflect "
                "how the property actually functions.</p>"),
        ], width=48),
    ], gap=22, align="stretch", wrap=True),
]))

# ----------------------------------------------- 6. WHAT TO EXPECT (white band)
S.append(B.sec(B.WHITE, [
    B.h2("What to Expect When Adding Ductless Comfort", align="center"),
    B.body_center("<p>A ductless project starts with the comfort problem, not the equipment.</p>"),
    B.row([
        B.step_card(1, "We Identify Where Comfort Is Falling Short",
                    "<p>We begin by understanding which rooms are uncomfortable, how they are used, "
                    "and what existing HVAC equipment already serves the property.</p>"),
        B.step_card(2, "We Plan the Zones and Equipment Locations",
                    "<p>Indoor-unit placement affects airflow, visibility, drainage, and service "
                    "access. We also consider line routing, electrical requirements, and how the "
                    'mini-split will work with any furnace, boiler, <a href="%s">heat pump</a>, or '
                    "central AC already in place.</p>" % L["heat_pumps"]),
        B.step_card(3, "We Help You Compare the Options",
                    "<p>Depending on your home, that may mean comparing single-zone versus multi-zone, "
                    "ductless versus extending ductwork, supplemental comfort versus a larger HVAC "
                    "upgrade, repair versus replacement, and different equipment and efficiency "
                    "options. You should understand why a particular setup is being recommended before "
                    "moving forward.</p>"),
        B.step_card(4, "We Install and Test Each Zone",
                    "<p>After installation, we test heating and cooling performance, airflow, "
                    "drainage, and controls. We also review basic system operation and filter care so "
                    "you know what ongoing ownership involves.</p>"),
    ], gap=20, align="stretch", wrap=True),
]))

# --------------------------------------------------------- 7. FAQ (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("What Westchester Homeowners Ask About Ductless Mini-Splits", align="center"),
    B.body_center(
        "<p>Ductless systems can solve specific comfort problems, but they are not the best fit for "
        "every property. These common questions can help you compare your options.</p>"),
    B.row([
        B.col([B.faq([
            ("Can a ductless mini-split both heat and cool?",
             "<p>Yes. Many ductless mini-splits operate as heat pumps and provide both heating and "
             "cooling. Whether ductless should serve as the primary heating source or supplement "
             "existing equipment depends on the system, property, number of zones, insulation, and "
             'heating needs &mdash; see <a href="%s">heating</a> for whole-home options.</p>'
             % L["heating"]),
            ("Can one mini-split cool multiple rooms?",
             "<p>Sometimes, but not reliably in every layout. One indoor unit works best in the room "
             "or open area where it is installed. Closed doors and separate rooms can limit airflow, "
             "so multiple zones may be more appropriate when several distinct spaces need "
             "conditioning.</p>"),
            ("Are ductless mini-splits expensive to run?",
             "<p>Operating costs depend on equipment efficiency, temperature settings, insulation, "
             "outdoor conditions, and how the zones are used. Zoning can allow you to focus comfort on "
             "occupied spaces, but actual energy savings vary from one property to another.</p>"),
            ("Do ductless mini-splits work well in older Westchester homes?",
             "<p>They can be a strong option when installing traditional ductwork would require "
             "opening finished walls or working around layouts that were not designed for central air. "
             "Electrical capacity, insulation, existing heating equipment, and room layout should "
             "still be evaluated before deciding.</p>"),
            ("Should I choose ductless or central air conditioning?",
             "<p>Neither is automatically better. Central AC may make more sense when a home already "
             "has effective ductwork and needs consistent whole-home cooling. Ductless can be useful "
             "for homes without ducts, additions, individual problem rooms, or properties where zoning "
             'is a priority &mdash; compare it with <a href="%s">central air conditioning</a> before '
             "you decide.</p>" % L["air_conditioning"]),
        ])], width=62),
        B.card([
            B.h3("Still Have Questions?"),
            B.body(
                "<p>Tell us which room is not working and how you use it. We will help you book the "
                "right visit &mdash; a ductless consultation, a repair evaluation, or "
                '<a href="%s">seasonal maintenance</a>.</p>' % L["maintenance"]),
            B.btn(CTA, align="left"),
        ], width=34),
    ], gap=34, align="stretch", wrap=True),
]))

# ----------------------------------------------------- 8. REVIEWS (white band)
S.append(B.sec(B.WHITE, [
    B.h2("See How G.C. Reliable Helps Local Properties Stay Comfortable", align="center"),
    B.body_center(
        "<p>Browse recent Google reviews to see how local customers describe G.C. "
        "Reliable&rsquo;s communication, responsiveness, workmanship, and approach to solving comfort "
        "problems throughout New Rochelle, Larchmont, Mamaroneck, Scarsdale, and beyond.</p>"),
    B.review_band(),
    B.stat_trio([
        ("fas fa-calendar-check", "40+", "Years serving Westchester"),
        ("fas fa-clock", "24/7", "Emergency HVAC availability"),
        ("fas fa-wrench", "All", "Makes &amp; models serviced"),
    ]),
]))

# ------------------------------------------------- 9. WHY TRUST US (gradient band)
S.append(B.sec(B.GRADIENT, [B.row([
    B.col([
        B.h2("Why Locals Choose G.C. Reliable for Ductless Comfort", color=B.WHITE_HEX),
        B.body(
            "<p>G.C. Reliable has served Westchester County since 1980 with professional workmanship, "
            "straightforward communication, and HVAC solutions designed around the property rather "
            "than a one-size-fits-all recommendation.</p>", on_dark=True),
        B.check_list([
            "<strong>Decades of Westchester experience:</strong> more than 40 years of local HVAC work "
            "inform our approach to older homes, additions, finished spaces, and room-to-room comfort "
            "problems.",
            "<strong>Systems planned around how you use the property:</strong> we consider which rooms "
            "actually need help, how they are used, and how ductless will work alongside existing HVAC "
            "equipment.",
            "<strong>One local team beyond installation:</strong> system planning, professional "
            "installation, maintenance, repairs for all makes and models, and 24/7 emergency "
            "availability.",
        ], on_dark=True, space=16),
        B.btn("Learn More About G.C. Reliable", L["about"], align="left"),
    ], width=55, gap=18),
    B.col([B.photo_badge(IMG["gc_reliable_3"], "24/7",
                         "Emergency help when comfort can&rsquo;t wait")],
          width=40),
], gap=44, align="center", wrap=True, mobile_dir="column-reverse",
   tablet_dir="column-reverse", justify="space-between")], pad=[68, 20, 68, 20]))

# ------------------------------------------------- 10. CLOSING CTA (mist band)
S.append(B.cta_section(
    "Put Comfort Where You Actually Need It",
    "<p>If one room never feels right, you are adding usable living space, or extending ductwork "
    "does not make sense for your property, ductless may be a practical solution. Contact "
    "G.C. Reliable Service to discuss ductless mini-split options for your New Rochelle, Pelham, "
    "Scarsdale, or Eastchester property and find a system built around the way you use your space.</p>",
    CTA))

doc = B.page("Ductless Mini Split", S)
out = os.path.join(HERE, "ductless-mini-split.json")
B.write(doc, out)
print("wrote %s (%d sections)" % (out, len(S)))
