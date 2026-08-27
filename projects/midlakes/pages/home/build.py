# -*- coding: utf-8 -*-
"""
Mid Lakes — Home (/).

A 1:1 port of source.php (the prototype's index.php). Copy is VERBATIM, entities
included; the section order and every value come from the prototype, not from taste.

Band order (KIT-ANALYSIS §4):
    hero(photo) · white · paper · comfort(photo) · white · paper · ink

Run:
    python3 projects/midlakes/pages/home/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/home/home.json
    python3 scripts/make-preview.py  projects/midlakes/pages/home/home.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x40000000)          # a seed distinct from every other Mid Lakes page

L, PH = B.LINKS, B.PHONE


# ---------------------------------------------------------------- 1. HERO
hero = B.hero(
    "hero-hvac",
    "Heating, Cooling &amp; Home Comfort in Loganville, GA",
    "Family-owned, locally operated, and backed by over 75 years of combined "
    "experience. We keep your home comfortable year-round with trusted Carrier "
    "installations and 24/7 emergency service.",
    [B.btn_primary("Call Now: %s" % PH["display"], PH["tel"]),
     B.btn_ghost("Get a Free Estimate", L["contact"])],
    creds=[("75+", "Years of Combined Team Experience"),
           ("100%", "Licensed &amp; Insured"),
           ("24/7", "Emergency Availability")],
)


# --------------------------------------------------------------- 2. ABOUT
# .about-grid (1.4fr / 1fr, gap 56, margin-bottom 64) then .promise-wrap
# (1.15fr / 1fr, gap 48, align center). Both live in the one boxed container.
about_grid = B.ratio_row(
    [[B.eyebrow("About Us"),
      B.h2("Your local, family-owned HVAC &amp; home efficiency experts."),
      B.lead("Founded in 2018 right here in Loganville, Mid Lakes HVAC was built on "
             "a simple promise: treat every customer like family and deliver honest, "
             "high-quality work every time. We don&rsquo;t just fix air "
             "conditioners&mdash;we protect your home&rsquo;s total efficiency.")],
     [B.stats([("2018", "Founded in Loganville"),
               ("300+", "Homeowners served"),
               ("24/7", "Emergency support")])]],
    ratios=[1.4, 1], gap_px=56, align="flex-start", col_gap=20)
about_grid["settings"]["margin"] = B.margin(0, 0, 64, 0)

promise_wrap = B.ratio_row(
    [[B.gallery("wall-units", "ductwork")],
     [B.promise([
         ("Carrier&reg; Dealer Quality",
          "We install premium, high-efficiency heating and cooling systems built for "
          "long-term dependability."),
         ("Parts &amp; Labor Guarantee",
          "We stand firmly behind the quality of our workmanship on every single job "
          "we complete."),
         ("Always Here When You Need Us",
          "Live 24/7 after-hours call support, so you never have to deal with an "
          "emergency alone."),
     ])]],
    ratios=[1.15, 1], gap_px=48, align="center")

about = B.sec_about([about_grid, promise_wrap], anchor="about")


# ------------------------------------------------------------ 3. SERVICES
# ⚠️ ALTERNATION: the icon tile runs red, blue, red, blue, red, blue across the
# grid (.service-card:nth-child(even) .service-icon). service_card() takes the
# 0-based index and restates it — do not reorder these without re-reading §9.
SERVICES = [
    ("wrench", "HVAC Repair &amp; Maintenance",
     "Regular tune-ups and fast, diagnostic repair services to keep your central AC "
     "and heating systems at peak performance year-round."),
    ("airflow", "Ductless / Mini-Split Systems",
     "Customized installation, repair, and maintenance for energy-efficient, "
     "multi-zone comfort without the hassle of ductwork."),
    ("shield-check", "Crawl Space Encapsulation",
     "Protect your home&rsquo;s structural foundation, prevent mold growth, and "
     "drastically improve indoor air quality from the ground up."),
    ("attic", "Attic Insulation",
     "Stop heat loss in winter and keep cool air inside during summer with "
     "high-performance home insulation upgrades."),
    ("droplet", "Humidity Control &amp; Air Quality",
     "Balance moisture levels to prevent mold, dust mites, and sticky indoor air "
     "during peak humid months."),
    ("thermostat", "Thermostat Repair &amp; Upgrades",
     "Upgrade to modern, programmable smart thermostats for effortless temperature "
     "control and lower monthly utility bills."),
]

services = B.sec_paper([
    B.section_title([
        B.eyebrow("Services We Offer"),
        B.h2("Complete heating, cooling &amp; indoor environmental services."),
    ]),
    B.grid([B.service_card(i, icon, title, copy)
            for i, (icon, title, copy) in enumerate(SERVICES)],
           cols=3, tablet=2, mobile=1, gap_px=20),
], anchor="services")
services["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ------------------------------------------------------- 4. COMFORT CLUB
comfort = B.comfort(
    "technician", "Comfort Club", "Join the Mid Lakes Comfort Club.",
    ["Protect your investment and save on energy bills every month. Join over 300 "
     "local homeowners who rely on our preventive maintenance program to extend "
     "system lifespan, prevent costly breakdowns, and keep manufacturer warranties "
     "valid."],
    perks=["Priority 24/7 dispatch on emergency calls",
           "Two annual tune-ups (Spring AC &amp; Fall Heating)",
           "Exclusive discounts on repairs &amp; equipment upgrades"],
    buttons=[B.btn_primary("Sign Up for a Service Agreement", L["service_agreements"])],
    anchor="comfort-club")


# ------------------------------------------------------------- 5. WHY US
# ⚠️ ALTERNATION: .why-card:nth-child(odd) .why-num is RED (the base is blue), so
# the numerals run 01 red, 02 blue, 03 red, 04 blue. why_card() takes the 1-based
# numeral as printed and derives the colour from it.
WHY = [
    ("Family-Owned &amp; Locally Operated",
     "Founded right here in Loganville, we&rsquo;re your neighbors. We take personal "
     "pride in every home we serve and treat your family with the care, respect, and "
     "honesty we expect in our own."),
    ("75+ Years of Combined Expertise",
     "Our seasoned technicians bring decades of hands-on experience to every "
     "job&mdash;from complex repairs to ductless mini-splits and crawl space "
     "encapsulation. We get it right the first time."),
    ("24/7 Live Emergency Response",
     "Air conditioners don&rsquo;t wait for business hours to break down, and neither "
     "do we. You&rsquo;ll always speak with a real person and get prompt service when "
     "you need it most."),
    ("Guarantee + Free Estimates",
     "We provide 100% free estimates on new installations and back our repairs with a "
     "comprehensive Parts &amp; Labor Guarantee for total peace of mind."),
]

# .why is white like .about but carries NO wave pair — its decoration is on the
# cards (4.svg). sec_why() is sec_about() minus the watermarks.
why = B.sec_why([
    B.section_title([
        B.eyebrow("Why Mid Lakes"),
        B.h2("Why Mid Lakes HVAC is Loganville&rsquo;s trusted choice."),
    ]),
    B.grid([B.why_card(i, t, c) for i, (t, c) in enumerate(WHY, start=1)],
           cols=2, tablet=2, mobile=1, gap_px=20),
], anchor="why-us")
why["elements"][0]["settings"]["flex_gap"] = B.gap(48)


# ----------------------------------------------------------------- 6. FAQ
# ⚠️ The FIRST item ships open — <details class="faq-item" open> on this page only.
FAQ = [
    ("Do you offer 24/7 emergency service?",
     "Yes. Our live after-hours response team is available 24 hours a day, 7 days a "
     "week. You&rsquo;ll always reach a real person and get prompt service when you "
     "need it most."),
    ("Are estimates on new systems really free?",
     "Absolutely. We provide 100% free estimates on all new installations, with no "
     "obligation and no pressure."),
    ("What brands do you install?",
     "We are a Carrier&reg; dealer and install premium, high-efficiency heating and "
     "cooling systems built for long-term dependability."),
    ("Are your technicians licensed and insured?",
     "Yes&mdash;Mid Lakes HVAC is 100% licensed and insured, and every repair is "
     "backed by our comprehensive Parts &amp; Labor Guarantee."),
    ("Do you service more than air conditioners?",
     "We do. Beyond HVAC repair and installation, we handle crawl space "
     "encapsulation, attic insulation, humidity control, and thermostat upgrades to "
     "protect your home&rsquo;s total efficiency."),
]

faq = B.sec_paper([
    B.ratio_row(
        [[B.eyebrow("Frequently Asked Questions"),
          B.h2("Answers about our HVAC expertise and support."),
          B.faq(FAQ, first_open=True)],
         [B.figure("vents",
                   "Modern HVAC for home upgrades",
                   "Engineered systems designed to elevate everyday living.")]],
        ratios=[1.3, 1], gap_px=56, align="flex-start", col_gap=32),
], anchor="faq")


# ------------------------------------------------------------- 7. CONTACT
contact = B.contact(
    "Ready for total home comfort? Contact us today.",
    ["Don&rsquo;t wait for a complete system breakdown. Whether you need urgent 24/7 "
     "repairs or a free estimate on a new system, our team is standing by to help."],
    [("Direct Phone", B.phone_link(), "24/7 Emergency Line"),
     ("Office Address", B.FACTS["address"], None),
     ("Office Hours", "Monday&ndash;Friday: 8:00 AM &ndash; 5:00 PM",
      "After-hours service available 24/7")],
    B.quote_form(),
)


SECTIONS = [hero, about, services, comfort, why, faq, contact]

if __name__ == "__main__":
    B.write(B.page("Home", SECTIONS), "home.json", HERE)
