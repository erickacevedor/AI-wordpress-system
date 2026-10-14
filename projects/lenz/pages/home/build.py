#!/usr/bin/env python3
"""
Lenz Heating & Cooling: Home page, v6-1.

Source of truth: the approved prototype v6-1 (design-source/v6-1/v6-1.html,
erickacevedor/lenz @ 12259d2) plus the client decisions recorded in ClickUp task
86bbfgdhr. The tree mirrors the prototype's DOM and class names; see ../../brand.py
for why, and tools/port-css.py for the stylesheet side.

Section order (as the prototype): hero, trustbar, services, cta-band, financing,
valueprops, plans, reviews, brands, about, who13, creds, area, faqs, close-form.
Header (offer bar + nav) and footer are Theme Builder parts: ../_theme/.

Run:  python3 projects/lenz/pages/home/build.py
Then: python3 scripts/validate-page.py projects/lenz/pages/home/home.json
      python3 projects/lenz/tools/port-css.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
from brand import L, PHONE, PHONE_TEL, svg, STARS, eyebrow  # noqa: E402

B.reset(0x10000000)
S = []


head, arrow_link, service_card = B.head, B.arrow_link, B.service_card


# =================================================================== HERO ====
S.append(B.section("hero", [
    B.box("hero__copy", [
        B.heading("Des Moines&apos; Trusted Heating, Cooling &amp; "
                  '<span class="accent">Air Quality</span> Experts', "h1",
                  size="var(--text-hero)"),
        B.text("Since 2009, Lenz Heating &amp; Cooling has been Central Iowa&apos;s go-to team for "
               "honest, hassle-free home comfort. We&apos;re a local, veteran-owned, and family-run "
               "business based right here in Urbandale, dedicated to keeping your home comfortable in "
               "every season. Whether you need 24/7 emergency HVAC repair, a new furnace, or a "
               "high-efficiency AC installation, we proudly serve homeowners across Des Moines, West Des "
               "Moines, Ankeny, Waukee, and surrounding Central Iowa communities.", "hero__sub"),
        # ClickUp 09/10 item 12: links to their Google reviews.
        B.raw('<div class="hero__proof">%s<a class="proof-text" href="%s" target="_blank" '
              'rel="noopener noreferrer">Real reviews from Des Moines homeowners</a></div>'
              % (STARS, L["reviews"].replace("&", "&amp;"))),
        B.box("hero__cta", [
            B.button("Get a Free Estimate", L["form"], "btn btn-gold"),
            B.button("Call " + PHONE, PHONE_TEL, "btn btn-outline-light", icon="phone"),
        ]),
    ]),
    B.box("hero__media", [
        B.image("lenz-comfort-webp",
                "A family relaxing together in a bright, comfortable Des Moines living room"),
    ]),
], box_classes="container hero__inner"))

# =============================================================== TRUSTBAR ====
TRUST = [("Since 2009", "Serving Central Iowa"), ("24/7/365", "Emergency service"),
         ("#50871-CL", "Iowa Master Licensed"), ("Veteran &amp; Woman-Owned", "Family operated"),
         ("WHO 13 News", "As seen on Hello Iowa")]
S.append(B.trustbar(TRUST))

# =============================================================== SERVICES ====
BANDS = [
    ("cool", "i-snow", "Air Conditioning Services", "air-conditioning", "Explore AC Services",
     "Keep your home cool and comfortable during hot Iowa summers. Our certified technicians handle "
     "emergency AC repairs, routine performance tune-ups, and energy-efficient air conditioner "
     "replacements tailored to your home&apos;s layout and budget.",
     [("cooling", "i-snow", "AC Installation", "Right-sized systems, installed properly.", "ac-installation"),
      ("cooling", "i-wrench", "AC Repair", "Fast diagnosis, day or night.", "ac-repair"),
      ("cooling", "i-calendar", "AC Maintenance", "Seasonal tune-ups that prevent breakdowns.", "ac-maintenance"),
      ("cooling", "i-snow", "AC Replacement", "Efficient upgrades sized to your home.", "ac-replacement")]),
    ("warm", "i-flame", "Heating &amp; Furnace Services", "heating", "Explore Heating Services",
     "Dependable heating built to withstand harsh Central Iowa winters. We provide fast diagnostic "
     "repairs, seasonal safety inspections, and high-efficiency furnace replacements for gas and "
     "electric heating systems.",
     [("heating", "i-flame", "Heating Installation", "High-efficiency gas and electric furnaces.", "heating-installation"),
      ("heating", "i-wrench", "Heating Repair", "No heat? We diagnose it fast.", "heating-repair"),
      ("heating", "i-calendar", "Heating Maintenance", "Safety inspections before the first freeze.", "heating-maintenance"),
      ("heating", "i-heat", "Heating Replacement", "Upgrade an aging or failing furnace.", "heating-replacement")]),
    ("air", "i-air", "Indoor Air Quality", "indoor-air-quality", "Improve Air Quality",
     "Breathe cleaner, healthier air year-round. We provide professional air duct cleaning and "
     "advanced whole-home air purifiers to remove dust, allergens, and hot or cold spots.",
     [("both", "i-droplet", "Humidity Control", "Whole-home humidifiers and dehumidifiers.", "humidity-control"),
      ("both", "i-shield", "UV Light Purification", "Treat air as it moves through the system.", "uv-light-purification"),
      ("both", "i-air", "Indoor Purification", "Filtration for dust, dander and allergens.", "indoor-purification"),
      ("both", "i-wind", "Duct Cleaning", "Clear out built-up dust and debris.", "duct-cleaning")]),
    ("extra", "i-wrench", "Additional Services", "additional-services", "View All Additional Services",
     "Specialized home utility solutions that optimize your system&apos;s overall efficiency and "
     "safety. Our team installs and services smart thermostats, heat pumps, water heaters (tank and "
     "tankless), custom ductwork repairs and modifications, airflow balancing, and gas lines.",
     [("both", "i-calendar", "Thermostat Services", "Smart thermostat install and setup.", "thermostat-services"),
      ("both", "i-droplet", "Water Heater Services", "Tank and tankless, professionally installed.", "water-heater-services"),
      ("both", "i-wind", "Ductwork", "Repairs, modifications and airflow balancing.", "ductwork"),
      ("both", "i-flame", "Gas Lines", "Safe runs for appliances and outdoor setups.", "gas-lines"),
      ("both", "i-heat", "Heat Pumps", "Heating and cooling from one efficient system.", "heat-pumps")]),
]


bands = []
for key, icon, title, hub, cta, blurb, cards in BANDS:
    bands.append(B.box("svc-band svc-band--" + key, [
        B.box("svc-band__head", [
            B.raw('<span class="svc-band__icon">%s</span>' % svg(icon)),
            B.box("svc-band__txt", [B.heading(title, "h3"), B.text("<p>%s</p>" % blurb)]),
            arrow_link("svc-band__go", cta, L[hub]),
        ]),
        B.box("svc-band__grid", [service_card(*c) for c in cards]),
    ], tag="section"))

bands.append(B.box("service-help", [
    B.box("service-help__txt", [
        B.heading("Not sure what you need?", "h4"),
        B.text("<p>Tell us what you&apos;re hearing or feeling and we&apos;ll work it out — no "
               "pressure, no charge.</p>"),
    ]),
    B.raw('<a class="phone-link" href="%s">%s %s</a>' % (PHONE_TEL, PHONE, svg("i-arrow", "icon-sm"))),
]))

S.append(B.section("section section--mist w-wave wave-1", [
    head("i-wrench", "Our services", "Complete Heating, Cooling &amp; Essential Home Services",
         "From emergency AC repairs and furnace replacements to gas line runs and indoor air quality, "
         "Lenz Heating &amp; Cooling provides complete HVAC and home comfort solutions across Des Moines "
         "and Central Iowa."),
    B.box("services__layout", bands),
], el_id="services"))

# =============================================================== CTA BAND ====
# The van photo is the band's backdrop. The prototype has it as a sibling of
# `.container.cta-band__inner`; the gate allows one child per band, so here the
# boxed `.container` holds the photo and a `.cta-band__inner` box. Containers are
# position:static (adapter), so the photo still anchors to `.cta-band`.
S.append(B.cta_band("Heat out? AC down? We&apos;re ready right now.",
                      "24/7 emergency service across the Des Moines metro since 2009."))

# ============================================================== FINANCING ====
FIN = [("i-clock", "Fast online pre-approval", "A few minutes online or during your in-home estimate."),
       ("i-card", "Monthly payments that fit",
        "Choose the term that works for your budget, including promotional 0% deferred interest for "
        "qualified buyers."),
       ("i-check", "No impact to browse options", "See what you qualify for before you commit to anything.")]
S.append(B.section("financing section", [
    B.box("financing__panel", [
        B.box("financing__head", [
            eyebrow("i-card", "Financing", "eyebrow--on-warm"),
            B.heading("Financing that fits your budget", "h2", "section__title", size="var(--text-2xl)"),
            B.text("Get pre-approved for a new furnace, an AC replacement, or an emergency repair — with "
                   "plans built around your budget, not ours.", "financing__lead"),
        ]),
        B.box("financing__points", [
            B.box("", [
                B.raw('<span class="financing__point-icon">%s</span>' % svg(ic, "icon")),
                B.heading(t, "h3"),
                B.text("<p>%s</p>" % d),
            ], tag="li") for ic, t, d in FIN
        ], tag="ul"),
        B.box("financing__cta", [
            B.button("Explore financing", L["financing"], "btn btn-gold"),
            # ClickUp 09/10 item 4: "Give us a call", not "Talk to us".
            B.button("Give us a call: " + PHONE, PHONE_TEL, "btn btn-outline-light", icon="phone"),
        ]),
    ]),
], el_id="financing"))

# ============================================================= VALUEPROPS ====
# ClickUp 10/08: do not change this block or the Ecobee photo. 09/10 item 6:
# "Free estimates" only, never free second opinions.
VP = [("01", "Veteran-owned &amp; led",
       "Founded by U.S. Marine Corps Veteran Al Lenz — military-grade precision, transparency, and "
       "respect on every home visit."),
      ("02", "Woman-owned &amp; operated",
       "Led with a focus on family-first customer service, clear communication, and home safety you can "
       "rely on."),
      ("03", "24/7 emergency service",
       "HVAC breakdowns don&apos;t wait for business hours. Our background-checked, certified techs are "
       "ready to roll day or night."),
      ("04", "Free estimates",
       "New equipment and full system replacements are quoted free, with no obligation and no pressure. "
       "Repairs carry our standard diagnostic fee, with upfront pricing before any work begins.")]
S.append(B.section("valueprops section", [
    head("i-shield", "Why Lenz", "What you get on every single call"),
    B.box("valueprops__layout", [
        B.box("valueprops__media", [
            B.image("lenz-thermostat-ecobee", "An ecobee smart thermostat installed on a living room wall"),
        ], tag="figure"),
        B.box("valueprops__grid", [
            B.box("vprop", [
                B.text(n, "vprop__num"),
                B.box("vprop__text", [B.heading(t, "h3"), B.text("<p>%s</p>" % d)]),
            ]) for n, t, d in VP
        ]),
    ]),
]))

# ================================================================== PLANS ====
S.append(B.plans_section())

# ================================================================ REVIEWS ====
S.append(B.section("reviews section", [
    head("i-star", "Reviews", "Over 2,000 5-Star Reviews Across Central Iowa",
         "See what your neighbors in Central Iowa have to say about working with our team."),
    B.reviews_grid(),
    B.raw('<p class="reviews__micro"><a href="%s">Ready for service like this? Get a free estimate %s</a></p>'
          % (L["form"], svg("i-arrow", "icon-sm"))),
], el_id="reviews"))

# ================================================================= BRANDS ====
# ClickUp 09/10 item 11: Optimus is the financing company, not a brand. Removed.
BRANDS = [("Carrier", "carrier", "https://www.carrier.com/"), ("Goodman", "goodman", "https://www.goodmanmfg.com/"),
          ("Lennox", "lennox", "https://www.lennox.com/"), ("Rheem", "rheem", "https://www.rheem.com/"),
          ("Trane", "trane", "https://www.trane.com/"), ("Ruud", "ruud", "https://www.ruud.com/"),
          ("American Pride", "american-pride", "https://www.americanpridehvac.com/"),
          ("Amana", "amana", "https://www.amana-hac.com/"), ("Bryant", "bryant", "https://www.bryant.com/")]
logos = "".join(
    '<a class="brand-logo" data-brand="%s" href="%s" target="_blank" rel="noopener noreferrer">'
    '<img src="%s" width="%d" height="%d" alt="%s HVAC equipment serviced by Lenz" loading="lazy" '
    'decoding="async" /></a>' % (n, u, B.MEDIA["brand-" + k]["url"], B.MEDIA["brand-" + k]["width"],
                                  B.MEDIA["brand-" + k]["height"], n)
    for n, k, u in BRANDS)
CHIPS = [("i-award", "Rheem Pro Partner"), ("i-shield", "BBB Accredited Business"), ("i-check", "Chamber Member")]
S.append(B.section("brands section", [
    B.box("brands__split", [
        B.box("brands__aside", [
            eyebrow("i-wrench", "Equipment we service"),
            B.heading("Certified Technicians Servicing All Major HVAC Brands", "h2", "brands__title",
                      size="var(--text-2xl)"),
            B.text("Whether you need emergency repairs on an existing system or a custom installation for a "
                   "new build, our certified technicians service every major heating and cooling brand on "
                   "the market.", "brands__lead"),
            B.raw('<ul class="brands__creds">%s</ul>' % "".join(
                '<li class="cred-chip">%s<span>%s</span></li>' % (svg(i, "icon-sm"), t) for i, t in CHIPS)),
            B.raw('<div class="marquee" data-marquee><div class="marquee__track">%s</div></div>' % logos),
        ]),
        B.box("brands__media", [
            B.image("lenz-technician-service-call-webp", "A Lenz technician on a service call"),
        ], tag="figure"),
    ]),
]))

# ================================================================== ABOUT ====
S.append(B.section("about section section--mist", [
    B.box("section__head section__head--center about__head", [
        eyebrow("i-tv", "About Lenz"),
        B.heading("Meet Lenz Heating &amp; Cooling: Des Moines&apos; Family-Owned HVAC Team", "h2",
                  "section__title", size="var(--text-2xl)"),
        B.box("about__stats", [
            B.text("<b>%s</b><span>%s</span>" % (v, l), "about__stat")
            for v, l in [("26+ yrs", "Al&apos;s experience"), ("11", "Cities served"), ("A+", "BBB rating")]
        ]),
    ]),
    B.box("about__inner", [
        B.box("about__body", [
            B.text("<p>Since 2009, Lenz Heating &amp; Cooling has delivered dependable home comfort services "
                   "across the Des Moines metro area. Founded by Al Lenz — an Iowa native, U.S. Marine Corps "
                   "Veteran, and Iowa Master License holder with over 26 years of hands-on industry "
                   "experience — our company was built on a simple promise: to do honest work and stand "
                   "behind it.</p>"
                   "<p>Co-owned and operated with his wife Jenny, Lenz Heating &amp; Cooling combines "
                   "technical expertise with dedicated customer care. Every technician on our team undergoes "
                   "rigorous training, background checks, and drug testing so you can feel completely safe "
                   "letting us into your home.</p>"
                   "<p>We don&apos;t just want to earn your business — we want to earn your trust.</p>"),
            B.box("about__cta", [
                B.button("Get a free estimate", L["form"], "btn btn-primary"),
                B.button("Call " + PHONE, PHONE_TEL, "btn btn-outline", icon="phone"),
            ]),
        ]),
        B.box("about__media", [
            B.image("lenz-team-webp", "The Lenz Heating &amp; Cooling technician team standing in front "
                    "of their service vans", "about__img"),
            B.image("lenz-service-van-wrap-webp", "Lenz Heating &amp; Cooling wrapped service van showing "
                    "the blue and orange wave graphic", "about__img about__img--inset"),
            B.text("Let Our Family Help Yours<span>Serving the Des Moines metro since 2009</span>",
                   "about__caption"),
        ]),
    ]),
], el_id="about"))

# ================================================================== WHO 13 ====
S.append(B.section("who13 section--tight section--mist", [
    B.box("who13__inner", [
        B.box("who13__copy", [
            eyebrow("i-tv", "As seen on TV"),
            B.heading("Expert HVAC Tips Featured on WHO 13 News&apos; Hello Iowa!", "h2", "section__title",
                      size="var(--text-2xl)"),
            B.text("We regularly join WHO 13 News to share seasonal advice, energy-saving tips, and home "
                   "maintenance strategies with our Central Iowa neighbors.", "section__lead"),
            B.button("Watch Our Latest News Segments", "/hello-iowa/", "btn btn-primary"),
        ]),
        B.box("who13__media", [
            B.raw('<iframe src="%s" title="Lenz Heating &amp; Cooling on WHO 13 News Hello Iowa!" '
                  'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture" '
                  'allowfullscreen></iframe>' % L["who13-video"]),
        ]),
    ]),
], el_id="who13"))

# ================================================================== CREDS ====
CREDS = [
    ("i-award", "Accredited &amp; master licensed", [
        "<b>BBB Accredited (A+ Rating)</b> — a verified commitment to transparent pricing and honest service.",
        "<b>Iowa Master Licensed</b> — held by founder Al Lenz (#50871-CL) in HVAC, Refrigeration &amp; Hydronics.",
        "<b>Safety first</b> — background-checked technicians and a certified Drug-Free Workplace."]),
    # ClickUp 10/08: DCG Volleyball added next to Football.
    ("i-shield", "Community &amp; chamber partners", [
        "<b>Chambers</b> — Urbandale, Waukee Area, and Creston.",
        "<b>Community partners</b> — ChildServe, American Heart Association, and the Waukee Leadership Institute.",
        "<b>Local outreach</b> — Operation Lenz a Helping Hand and youth sports sponsors (DCG Football, DCG "
        "Volleyball, UGRA Softball)."]),
    ("i-card", "What that means for you", [
        "Straightforward, upfront pricing explained before any work begins.",
        "Trained, vetted technicians you can trust in your home.",
        "A local team invested in the same communities you live in."]),
]
S.append(B.section("creds section", [
    head("i-award", "Trusted, accredited &amp; proudly local", "Trusted, Accredited &amp; Proudly Local"),
    B.box("creds__grid", [
        B.box("creds__card", [
            B.raw('<span class="creds__icon">%s</span>' % svg(ic, "icon")),
            B.heading(t, "h3"),
            B.text('<ul class="creds__list">%s</ul>' % "".join("<li>%s</li>" % li for li in items)),
        ], tag="article") for ic, t, items in CREDS
    ]),
]))

# =================================================================== AREA ====
# ClickUp 08/17: "Main office", not "Headquarters".
CITIES = ["Urbandale", "Des Moines", "West Des Moines", "Waukee", "Ankeny", "Johnston", "Clive", "Grimes",
          "Altoona", "Norwalk", "Windsor Heights"]
S.append(B.section("area section", [
    head("i-pin", "Service area",
         "Proudly Serving the Greater Des Moines Metropolitan Area &amp; Central Iowa",
         "Based right here in Urbandale, Lenz Heating &amp; Cooling proudly serves Des Moines and surrounding "
         "communities with round-the-clock repairs, maintenance, and system replacements you can rely on.",
         extra="section__head--center area__head"),
    B.box("area__layout", [
        B.box("area__copy", [
            B.raw('<div class="area__cities">%s</div>' % "".join(
                '<span class="area-chip">%s%s</span>' % (svg("i-pin", "icon-xs"), c) for c in CITIES)),
            B.raw('<p class="area__note">%sNot sure if you&apos;re in our service radius? Give our local '
                  'office a call at %s to speak with our team.</p>' % (svg("i-info", "icon-sm"), PHONE)),
            B.raw('<p class="area__address">%s<a href="https://www.google.com/maps/dir/?api=1&amp;destination='
                  '7641+Douglas+Avenue,+Urbandale,+IA+50322" target="_blank" rel="noopener noreferrer">Main '
                  'office: 7641 Douglas Ave, Urbandale, IA 50322</a><span class="sep">·</span><a href="https://'
                  'www.google.com/maps/dir/?api=1&amp;destination=810+Interstate+Pkwy+Suite+141,+Waukee,+IA" '
                  'target="_blank" rel="noopener noreferrer">Waukee: 810 Interstate Pkwy, Suite 141</a></p>'
                  % svg("i-pin", "icon-sm")),
        ]),
        B.box("area__map", [
            B.raw('<iframe src="https://www.google.com/maps?q=7641+Douglas+Avenue,+Urbandale,+IA+50322&amp;'
                  'output=embed" title="Lenz Heating &amp; Cooling location and service area map" '
                  'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'),
        ]),
    ]),
], box_classes="container container-bottom", el_id="area"))

# =================================================================== FAQS ====
FAQ = [
    ("What happens if my heating or AC breaks down after hours or on a weekend?",
     "Lenz Heating &amp; Cooling offers 24/7/365 emergency HVAC service across Greater Des Moines. When you "
     "call (515) 225-6446, you speak directly with our local team, not a third-party call center. Our "
     "certified technicians are on call day and night to diagnose and repair your heating or cooling system."),
    ("How do I know if my repair or quote qualifies for a free estimate?",
     "We provide free, no-obligation estimates on all new equipment installations and full system "
     "replacements. For repairs and troubleshooting, we charge a flat diagnostic fee that covers a full "
     "system inspection, followed by upfront pricing before any repair work begins."),
    ("Do I have to sit around all day waiting for my technician to show up?",
     "No, we provide clear arrival windows and real-time text tracking updates. You will receive an "
     "automated text notification when your technician is en route, eliminating long waiting windows and "
     "allowing you to plan your day."),
    ("What can I expect during a home visit from a Lenz technician?",
     "You can expect a professional, clean, and transparent service visit from a direct Lenz employee. Every "
     "home visit includes real-time arrival notifications when your technician is on the way, uniformed "
     "technicians wearing protective shoe covers, and thorough system diagnostics with clear, flat-rate "
     "pricing explained before any work starts."),
    ("How do I apply for financing for a new furnace or AC installation?",
     "You can apply for HVAC financing through Synchrony Bank online or in person during your estimate. We "
     "offer flexible payment plans, including promotional 0% deferred interest financing for qualified "
     "buyers. Pre-approval takes only a few minutes."),
    ("What equipment brands do you service?",
     "Carrier, Goodman, Lennox, Rheem, Ruud, Trane, American Pride, Amana, and Bryant. We&apos;re a Rheem "
     "Pro Partner."),
    ("Are your technicians background-checked?",
     "Yes. Every technician completes extensive training and a background check before entering a home."),
]
S.append(B.section("faqs section", [
    head("i-info", "FAQs", "Frequently Asked HVAC Questions", extra="section__head--center"),
    B.faq_list(FAQ),
], el_id="faqs"))

# ============================================================= CLOSE FORM ====
S.append(B.close_form("Let&apos;s Get Your Home Comfortable Again",
                      "Get fast, friendly HVAC repair, maintenance, or replacement from Central Iowa&apos;s "
                      "trusted family-owned team. We&apos;re ready when you are!"))

# ================================================================== WRITE ====
doc = B.E.wrap_page("Home", S, {"template": "elementor_header_footer", "hide_title": "yes"})
out = os.path.join(HERE, "home.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
B.write_manifest(os.path.join(HERE, "widget-classes.json"))
print("wrote %s (%d sections)" % (out, len(S)))
