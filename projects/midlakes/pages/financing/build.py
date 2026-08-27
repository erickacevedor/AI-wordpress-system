# -*- coding: utf-8 -*-
"""
Mid Lakes — Financing (/financing/).

A 1:1 port of source.php. Copy is VERBATIM, entities included.

Band order (KIT-ANALYSIS §4) — the only page that alternates perfectly all the way
down, and the only one with a closing `.legal` band:
    hero · white · paper · white · paper · white · paper · white · ink · paper(legal)

⚠️ BOTH financing CTAs point at `#contact`, NOT at Service Finance. That is a settled
decision (PORT-DECISIONS "Answered 2026-08-27"), not a placeholder to chase. Do not
"fix" it to a lender URL.

⚠️ The `.step-num` numerals alternate red, blue, red, blue — restated by steps() from
the 1-based index, because `.step:nth-child(odd)` has no Elementor equivalent.

Run:
    python3 projects/midlakes/pages/financing/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/financing/financing.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x45000000)

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "wall-units",
    "Flexible Financing for Your Home Comfort Needs",
    "A new HVAC system or major home-comfort project can be an important "
    "investment&mdash;and sometimes, the need comes sooner than expected.",
    [B.btn_primary("Explore Financing Options", "#financing-options"),
     B.btn_ghost("Call %s" % PH["display"], PH["tel"])],
    creds=[("Family-Owned", "&amp; Operated"),
           ("Free", "Estimates"),
           ("Licensed", "&amp; Insured"),
           ("Parts &amp; Labor", "Guarantee")],
    interior=True)


# ---------------------------------------------------------------- 2. INTRO
intro = B.sec_about([
    B.section_title([
        B.lead("At Mid Lakes Heating and Cooling, we want to make it easier to move "
               "forward with the solution that makes sense for your home and family. "
               "Financing is available for qualifying projects, and our team can help "
               "guide you through the process from your estimate to the online "
               "application."),
    ]),
])


# ---------------------------------------------------------- 3. FLEXIBILITY
flexibility = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("Flexibility"),
          B.h2("More Flexibility When Your Home Needs It"),
          B.lead("Some home improvements are planned months in advance. Others begin "
                 "with an air conditioner that stops working on a hot Georgia "
                 "afternoon or a comfort problem that can no longer be put off."),
          B.lead("Financing gives eligible homeowners another way to manage a larger "
                 "home-comfort expense without having to cover the entire cost "
                 "upfront."),
          B.lead("That means you can focus first on what your home needs, understand "
                 "the recommended solution, and then decide which payment option "
                 "makes the most sense for your household."),
          B.lead("Our goal is simple: give you clear information and help make the "
                 "process easier&mdash;not add more pressure to an already important "
                 "decision.")],
         [B.figure("hero-hvac")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ------------------------------------------------------ 4. LENDING PARTNER
partner = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Our lending partner"),
          B.h2("Financing Through Service Finance"),
          B.lead("Mid Lakes HVAC partners with Service Finance to provide financing "
                 "for qualifying home-comfort projects."),
          B.lead("Available rates, terms, and promotional offers depend on the "
                 "financing program and credit approval."),
          # ⚠️ #contact, deliberately — see the module docstring.
          B.actions([B.btn_primary("Apply for Financing", L["contact"])])],
         [B.spec_card("Here are the key details:", [
             "Services over $3,000 can be financed",
             "0% interest options may be available",
             "Promotional terms may include 12, 18, or 24 months",
             "Applications are completed online",
             "Your Mid Lakes technician can help guide you through the application "
             "process",
          ], blue=True)]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
], anchor="financing-options")


# --------------------------------------------------------------- 5. PROCESS
STEPS = [
    ("Start With an Evaluation",
     ["Tell us what&rsquo;s going on with your home or what you&rsquo;re hoping to "
      "improve.",
      "Our team will evaluate your needs, explain the recommended solution, and "
      "provide pricing for the work."]),
    ("Decide Whether You&rsquo;d Like to Finance",
     ["Once you know what the project involves and what it will cost, you can decide "
      "whether financing makes sense for your household.",
      "If you&rsquo;d like to explore it, just let your technician know."]),
    ("Complete Your Application Online",
     ["The financing application is completed online through Service Finance.",
      "You won&rsquo;t have to navigate the process by yourself. Your Mid Lakes "
      "technician can help walk you through the application and point you toward the "
      "information you need."]),
    ("Review Your Financing Offer",
     ["If approved, review the available financing terms and choose the option that "
      "works for you.",
      "Once your project details and payment arrangements are finalized, our team can "
      "move forward with scheduling your service."]),
]

process = B.sec_paper([
    B.section_title([
        B.eyebrow("Process"),
        B.h2("How the Financing Process Works"),
        B.lead("We keep the process straightforward so you can focus on making the "
               "right decision for your home."),
    ]),
    B.steps(STEPS),
])
process["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# -------------------------------------------------------- 6. CONSIDERATIONS
considerations = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Considerations"),
          B.h2("Why Loganville Homeowners Consider Financing"),
          B.lead("There&rsquo;s no single right way to pay for a home-comfort "
                 "project. For some families, financing simply provides more room to "
                 "work with when a larger expense comes along."),
          B.lead("Financing is simply another option. We&rsquo;ll give you the "
                 "information you need and let you decide what works best for your "
                 "family.")],
         [B.spec_card("It may help you:", [
             "Spread the cost of a larger project over time",
             "Avoid paying the full project cost upfront",
             "Address an important comfort need sooner",
             "Choose a solution based on what your home needs",
             "Keep more flexibility in your household budget",
          ])]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ----------------------------------------------------------------- 7. FAQ
FAQ = [
    ("Who is Mid Lakes HVAC&rsquo;s financing provider?",
     "Mid Lakes HVAC partners with Service Finance to offer financing to qualifying "
     "customers."),
    ("How do I apply for financing?",
     "The application is completed online through Service Finance. If you decide to "
     "apply, your Mid Lakes technician can help guide you through the process."),
    ("Do I need to apply before my appointment?",
     "No. You can start by having our team evaluate your needs and provide pricing "
     "for the recommended work. From there, you can decide whether financing is right "
     "for you."),
    ("Do I have to use financing?",
     "Not at all. Financing is simply one payment option available to qualifying "
     "customers. You can choose the approach that works best for your household."),
    ("Can someone help me with the application?",
     "Yes. Our technicians can help you navigate the online application process so "
     "you&rsquo;re not left figuring it out on your own."),
]

faq = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("FAQs"),
          B.h2("Financing FAQs"),
          B.faq(FAQ, first_open=False)],
         [B.figure("ductwork", "Free estimates first.",
                   "Understand the work and the cost before you consider "
                   "financing.")]],
        ratios=[1.3, 1], gap_px=56, align="flex-start", col_gap=32),
], anchor="faq")


# ------------------------------------------------------- 8. STRAIGHT ANSWERS
straight = B.sec_about([
    B.ratio_row(
        [[B.eyebrow("Straight answers"),
          B.h2("Local Service. Straightforward Help."),
          B.lead("A major HVAC or home-comfort expense can feel like a lot to "
                 "navigate, especially when it wasn&rsquo;t part of the plan."),
          B.lead("As a family-owned and locally operated company, Mid Lakes HVAC "
                 "believes in keeping things straightforward. We&rsquo;ll help you "
                 "understand what your home needs, explain the work clearly, and walk "
                 "you through your options without unnecessary pressure."),
          B.lead("And if you decide financing is the right fit, our team will be "
                 "there to help you take the next step."),
          B.lead("With 75+ years of combined team experience, licensed and insured "
                 "service, free estimates, and a Parts &amp; Labor Guarantee, you can "
                 "feel confident about both the work being recommended and the local "
                 "team standing behind it."),
          B.actions([B.btn_primary("Get to Know the Mid Lakes Team", L["about"])])],
         [B.figure("technician")]],
        ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=14),
])


# ---------------------------------------------------------------- 9. CONTACT
contact = B.contact(
    "Let&rsquo;s Find the Right Way Forward",
    ["You don&rsquo;t need to have the repair, replacement, or payment plan figured "
     "out before you call.",
     "Tell us what&rsquo;s going on with your home. We&rsquo;ll help you understand "
     "the problem, recommend the right next step, and explain your options so you can "
     "make a decision that works for your family.",
     "Call %s or contact us online to get started." % PH["display"]],
    None,
    B.quote_form(),
)
contact["elements"][0]["elements"][0]["elements"][0]["elements"].append(
    B.actions([B.btn_primary("Call %s" % PH["display"], PH["tel"])]))


# ----------------------------------------------------------------- 10. LEGAL
legal = B.legal(
    "Financing is provided by Service Finance and is subject to credit approval. "
    "Available rates, promotional offers, repayment terms, and eligibility "
    "requirements may vary. Review all financing terms and conditions provided by "
    "Service Finance before accepting an offer.")


SECTIONS = [hero, intro, flexibility, partner, process, considerations, faq,
            straight, contact, legal]

if __name__ == "__main__":
    B.write(B.page("Financing", SECTIONS), "financing.json", HERE)
