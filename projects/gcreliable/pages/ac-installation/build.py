#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G.C. Reliable Service — "Professional AC Installation in New Rochelle, NY".

Reproducible build. Structure + responsive correctness come from
scripts/elementor_builder.py; the brand vocabulary (bands, cards, buttons, the
photo+badge, the Pro accordion) comes from projects/gcreliable/brand.py, which reads
projects/gcreliable/tokens.json. Only this page's copy and section order live here.

Source doc:  source.txt (extracted from "GC Reliable_COPY_Page_AC Installation.docx")
Model page:  current-theme/content/page/225063.json ("AC Repair")

Run:  python scripts/../projects/gcreliable/pages/ac-installation/build.py
Then: python scripts/validate-page.py projects/gcreliable/pages/ac-installation/ac-installation.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))          # pages/<slug> -> projects/<site>
sys.path.insert(0, SITE)
import brand as B                                       # noqa: E402

B.reset(0x30000000)
L, IMG = B.LINKS, B.IMAGES
CTA = "Schedule an AC Installation Consultation"

S = []

# ---------------------------------------------------------------- 1. HERO (gradient)
S.append(B.hero(
    "Professional AC Installation", "in New Rochelle, NY",
    "Choose a New Air Conditioner With Confidence",
    CTA))

# ------------------------------------------------- 2. INTRO + photo/badge (white)
S.append(B.sec(B.WHITE, [B.row([
    B.col([
        B.h2("The Right AC Starts With More Than Square Footage"),
        B.body(
            "<p>Buying a new air conditioner is a major investment, and simply replacing your old "
            "system with the same size is not always the best approach.</p>"
            "<p>A cooling system that made sense years ago may no longer fit the home after an attic "
            "was finished, an addition was built, windows were replaced, or insulation was upgraded. "
            "Multi-level homes can also have very different cooling demands from one floor to another.</p>"
            "<p>That is why G.C. Reliable Service looks beyond square footage when recommending new "
            "equipment. The goal is not to install the biggest system available &mdash; it is to choose "
            "one that can cool the home properly without paying for capacity you do not need. We provide "
            '<a href="%s">air conditioning</a> installation and replacement throughout New Rochelle and '
            "Westchester County.</p>" % L["air_conditioning"]),
        B.btn(CTA, align="left"),
    ], width=52, gap=18),
    B.col([B.photo_badge(IMG["technician_2"], "40+",
                         "Years serving New Rochelle &amp; Westchester since 1980")],
          width=44),
], gap=44, align="center", wrap=True, mobile_dir="column-reverse",
   tablet_dir="column-reverse", justify="space-between")]))

# -------------------------------------------- 3. SIGNS IT MAY BE TIME (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("Signs It May Be Time for a New Air Conditioner", align="center"),
    B.body_center(
        "<p>It may be worth comparing repair and replacement when the same problems keep "
        "coming back. Any of these are worth a closer look.</p>"),
    B.row([
        B.col([
            B.h3("Worth Comparing Your Options If&hellip;"),
            B.check_list([
                "Repairs are becoming more frequent or expensive",
                "The system struggles to keep the home comfortable",
                "Certain rooms consistently stay warmer",
                "Cooling costs continue to climb",
                "The AC runs for long periods without keeping up",
                "A major component has failed",
                "The current system no longer fits changes made to the home",
            ]),
        ], width=56),
        B.card([
            B.h3("A New AC Is Not Automatically the Answer", color=B.RED),
            B.body(
                "<p>These signs do not automatically mean you need a new air conditioner. If another "
                "repair still makes financial sense, replacement may not be the first recommendation.</p>"
                '<p>When the problem is isolated and the equipment has otherwise been dependable, '
                '<a href="%s">AC repair</a> may be the better value &mdash; and we will say so.</p>'
                % L["ac_repair"]),
        ], width=40),
    ], gap=44, align="stretch", wrap=True),
    B.body_center(
        "<p>When reliability, comfort, repair costs, or equipment condition point toward "
        "replacement, G.C. Reliable can help you compare the next step.</p>"),
]))

# ------------------------------------- 4. INSTALLATION vs REPLACEMENT (white band)
S.append(B.sec(B.WHITE, [
    B.h2("AC Installation and Replacement Built Around Your Home", align="center"),
    B.body_center(
        "<p>Whether you are adding central air for the first time or replacing aging equipment, "
        "the installation should start with the conditions the new system will actually need to "
        "handle.</p>"),
    B.row([
        B.card([
            B.emoji("📐"),
            B.h3("New AC Installation"),
            B.body(
                "<p>Adding central air where it did not previously exist requires a plan for more "
                "than the equipment itself.</p>"
                "<p>We evaluate the home&rsquo;s layout, ductwork needs, electrical requirements, "
                "airflow, and available installation space before recommending a system. The goal is "
                "to build the cooling setup around the home as it exists today, including renovations, "
                "additions, and finished spaces that affect demand.</p>"),
        ], width=48),
        B.card([
            B.emoji("♻️"),
            B.h3("AC Replacement"),
            B.body(
                "<p>If your existing air conditioner is becoming unreliable, age is only one part of "
                "the decision.</p>"
                "<p>Repair history, current condition, comfort performance, efficiency, and the cost of "
                "another major repair all matter. Replacement may offer better long-term value when "
                "breakdowns are becoming more frequent, comfort has declined, or the system no longer "
                "meets the home&rsquo;s needs. G.C. Reliable helps you understand those tradeoffs "
                "before you decide.</p>"),
        ], width=48),
    ], gap=22, align="stretch", wrap=True),
]))

# ------------------------------------------ 5. CHOOSING THE RIGHT SYSTEM (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("What Goes Into Choosing the Right AC System?", align="center"),
    B.body_center(
        "<p>A successful installation starts before the old equipment comes out. The new AC needs "
        "to work with the home around it, not just fit into the same space as the old one.</p>"),
    B.row([
        B.card([
            B.h3("Proper System Sizing"),
            B.body(
                "<p>Bigger does not automatically mean better. An undersized system may run constantly "
                "and still struggle during hot weather, while an oversized system can cycle too quickly "
                "and may not provide the comfort or humidity control you expected.</p>"
                "<p>Replacing a 3-ton system with another 3-ton system simply because that is what was "
                "there before can also repeat an old sizing mistake. Changes to insulation, windows, "
                "additions, or the home&rsquo;s layout can alter cooling needs over time &mdash; which "
                "is why square footage is only one part of the sizing decision.</p>"),
        ], width=48),
        B.card([
            B.h3("Existing Ductwork and Airflow"),
            B.body(
                "<p>A brand-new air conditioner cannot correct every problem elsewhere in the HVAC "
                "system.</p>"
                "<p>If certain rooms have always received weak airflow, that issue should be evaluated "
                "before new equipment goes in. Otherwise, you can invest in a new AC and still end up "
                "with the same uncomfortable bedroom or second floor.</p>"
                "<p>Existing ductwork should be considered for condition, sizing, restrictions, and its "
                "ability to deliver enough air where the home needs it.</p>"),
        ], width=48),
    ], gap=22, align="stretch", wrap=True),
]))

# ----------------------------------------------- 6. WHAT TO EXPECT (white band)
S.append(B.sec(B.WHITE, [
    B.h2("What to Expect From Your AC Installation", align="center"),
    B.body_center(
        "<p>Replacing an air conditioner should not feel like choosing equipment first and asking "
        "questions later.</p>"),
    B.row([
        B.step_card(1, "We Start With What You Want the New System to Fix",
                    "<p>We begin by understanding what is not working today &mdash; uneven "
                    "temperatures, recurring repairs, high operating costs, excess humidity, noise, or "
                    "an AC that simply cannot keep up anymore. Those concerns help define what the "
                    "replacement should improve.</p>"),
        B.step_card(2, "We Evaluate What the New AC Will Be Working With",
                    "<p>We look beyond the model number on the old equipment. The evaluation may "
                    "include the existing system, ductwork, airflow, electrical requirements, drainage, "
                    "available installation space, and conditions that could affect performance &mdash; "
                    "so we can tell whether replacing the equipment alone is enough.</p>"),
        B.step_card(3, "You Compare the Options Before Choosing",
                    "<p>Once we understand the home, we narrow the options based on cooling capacity, "
                    "efficiency, comfort features, budget, and long-term operating considerations. The "
                    "goal is an informed decision, without paying for features or capacity that do not "
                    "add meaningful value for your home.</p>"),
        B.step_card(4, "We Verify the System Before the Job Is Done",
                    "<p>Installation is not complete just because the new AC turns on. We check system "
                    "operation, airflow, temperature performance, drainage, electrical function, and "
                    "controls before the job is finished, then review thermostat operation, filter care, "
                    'and <a href="%s">maintenance</a> expectations with you.</p>' % L["maintenance"]),
    ], gap=20, align="stretch", wrap=True),
    B.card([
        B.h3("Before You Choose, You Should Understand"),
        B.check_list([
            "Why a particular system is being recommended",
            "What changes from one option to another",
            "Which features may be worth paying for",
            "What the installation will involve",
            "Whether additional work is recommended, and why",
            "What the project will cost before you commit",
        ]),
    ]),
]))

# --------------------------------------------------------- 7. FAQ (mist band)
S.append(B.sec(B.MISTB, [
    B.h2("What Homeowners Want to Know Before Replacing an AC", align="center"),
    B.row([
        B.col([B.faq([
            ("How do I know what size AC my home needs?",
             "<p>The right size depends on more than square footage. Layout, insulation, windows, sun "
             "exposure, ceiling height, air leakage, ductwork, and other characteristics can affect the "
             "cooling load. A professional evaluation helps determine how much capacity the home "
             "actually needs instead of automatically matching the size of the old system.</p>"),
            ("Should I repair my old AC or replace it?",
             "<p>Repair may make sense when the problem is relatively minor and the system has "
             "otherwise been reliable. Replacement is worth considering when repairs are becoming "
             "frequent, the equipment is aging, comfort has declined, or an expensive component has "
             'failed. The better choice depends on the condition of the individual system, not age '
             'alone &mdash; see <a href="%s">AC repair</a> if a fix may still be the right call.</p>'
             % L["ac_repair"]),
            ("How long does AC installation take?",
             "<p>It depends on the scope of the project. A straightforward replacement may be less "
             "involved than adding central air where none existed, or than correcting ductwork, "
             "electrical, drainage, or other conditions at the same time. Your installer should explain "
             "the expected scope before work begins.</p>"),
            ("Will a new air conditioner lower my energy bills?",
             "<p>A newer, properly sized system may operate more efficiently than aging equipment, but "
             "lower bills are not guaranteed. Actual energy use also depends on weather, thermostat "
             "settings, insulation, duct performance, and how often the system runs. The goal is to find "
             "the right balance of purchase price, efficiency, comfort, and long-term operating cost.</p>"),
            ("Do I need to replace my ductwork when I replace my AC?",
             "<p>Not necessarily. Existing ductwork may continue to work well with the new system if it "
             "is appropriately sized, in good condition, and able to deliver the required airflow. If "
             "there are leaks, restrictions, damaged sections, or long-standing comfort problems, those "
             "issues may need to be addressed as part of the installation plan.</p>"),
        ])], width=62),
        B.card([
            B.h3("Still Have Questions?"),
            B.body(
                "<p>Tell us what your current system is doing and what you want the new one to fix. "
                "We will help you book the right visit &mdash; an installation consultation, a repair "
                'evaluation, or <a href="%s">seasonal maintenance</a>.</p>' % L["maintenance"]),
            B.btn("Schedule Your Appointment", align="left"),
        ], width=34),
    ], gap=34, align="stretch", wrap=True),
]))

# ----------------------------------------------------- 8. REVIEWS (white band)
S.append(B.sec(B.WHITE, [
    B.h2("See What Local Customers Say About G.C. Reliable", align="center"),
    B.body_center(
        "<p>A new cooling system is a significant investment, so the company installing it matters "
        "just as much as the equipment. Browse recent Google reviews to see what local homeowners and "
        "businesses say about G.C. Reliable&rsquo;s communication, professionalism, responsiveness, "
        "and workmanship.</p>"),
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
        B.h2("Why Homeowners Trust G.C. Reliable With a New AC", color=B.WHITE_HEX),
        B.body(
            "<p>G.C. Reliable has served the area since 1980, helping homeowners make HVAC decisions "
            "based on the property, the condition of the equipment, and the value of the investment "
            "rather than a one-size-fits-all recommendation.</p>", on_dark=True),
        B.check_list([
            "<strong>Decades of experience evaluating more than the equipment:</strong> homes change "
            "over time, and additions, renovations, aging ductwork, insulation improvements, and "
            "changing comfort needs all affect what a replacement system needs to do.",
            "<strong>Sizing based on today&rsquo;s home:</strong> we consider the home&rsquo;s current "
            "conditions rather than automatically duplicating the capacity of the equipment being removed.",
            "<strong>Clear choices before you commit:</strong> we explain the differences between your "
            "options so you can decide which features, efficiency levels, and improvements are worth "
            "the investment for your home.",
        ], on_dark=True, space=16),
        B.btn("Learn More About G.C. Reliable", L["about"], align="left"),
    ], width=55, gap=18),
    B.col([B.photo_badge(IMG["cooling_services"], "24/7",
                         "Emergency help when cooling can&rsquo;t wait")],
          width=40),
], gap=44, align="center", wrap=True, mobile_dir="column-reverse",
   tablet_dir="column-reverse", justify="space-between")], pad=[68, 20, 68, 20]))

# ------------------------------------------------- 10. CLOSING CTA (mist band)
S.append(B.cta_section(
    "Start With the Right System, Not Just a New One",
    "<p>Replacing your air conditioner should do more than put newer equipment in the same spot. "
    "It is an opportunity to address the comfort, reliability, and performance issues that led you "
    "to consider replacement in the first place. Schedule an AC installation consultation with "
    "G.C. Reliable Service and get clear guidance on a cooling system that fits your home, "
    "priorities, and budget.</p>",
    CTA))

doc = B.page("AC Installation", S)
out = os.path.join(HERE, "ac-installation.json")
B.write(doc, out)
print("wrote %s (%d sections)" % (out, len(S)))
