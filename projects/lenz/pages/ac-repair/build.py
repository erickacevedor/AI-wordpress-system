#!/usr/bin/env python3
"""
Lenz: AC Repair (/ac-repair/). Service page template, see ../../service_page.py.

Copy: the page doc (source.docx, "Lenz AC Repair", 2026-10-13), verbatim except
where a ClickUp decision overrides it (noted inline). Template-only pieces the
doc does not have (breadcrumb, eyebrows, hero badge, trustbar, related services,
help tile) come from the approved template, design-source/v6-1/ac-repair.html.

Run:  python3 projects/lenz/pages/ac-repair/build.py
Then: python3 scripts/validate-page.py projects/lenz/pages/ac-repair/ac-repair.json
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x40000000)

PAGE = {
    "slug": "ac-repair",
    "title": "AC Repair",
    "cat": "cool",
    "cat_icon": "i-snow",
    "cat_label": "Air conditioning",
    "hub": ("Air Conditioning", "air-conditioning"),
    "h1": ("Reliable ", "AC Repair", " in Des Moines &amp; Central Iowa"),
    "lead": "When your air conditioner stops cooling, makes strange noises, or struggles to keep up with "
            "summer heat, you need more than a quick guess. You need clear answers, honest recommendations, and "
            "reliable AC repair from a team that knows how to get your home comfortable again.",
    "areas": "Serving Des Moines, Urbandale, West Des Moines, Ankeny, Altoona, Clive, Waukee, and surrounding "
             "Central Iowa communities.",
    "cta": "Schedule AC Repair",
    "form_preselect": "AC Repair",
    # Stand-in until the 2026-10-15 photo shoot delivers an AC service shot.
    "hero_image": ("lenz-technician-service-call-webp",
                   "A Lenz technician diagnosing a home comfort system on a service call"),
    "badge": ("24/7 emergency AC repair", "Local team, real people, day or night."),
    "trust": [("Since 2009", "Serving Central Iowa"), ("24/7/365", "Emergency service"),
              ("#50871-CL", "Iowa Master Licensed"), ("Veteran &amp; Woman-Owned", "Family operated"),
              ("Upfront Pricing", "Before any work begins")],

    "intro": {
        "eyebrow": ("i-wrench", "Don&apos;t wait for a breakdown"),
        "title": "Fast AC Repair Before Small Problems Get Worse",
        "lead": "AC problems rarely fix themselves. A system that runs longer than usual, cools unevenly, or "
                "struggles during hot and humid Central Iowa weather is often working under extra strain.",
        "body": [
            "At Lenz Heating &amp; Cooling, we provide professional air conditioning repair for homeowners across "
            "the Des Moines metro. Whether your AC is blowing warm air, short cycling, leaking water, freezing up, "
            "or not turning on at all, our technicians can diagnose the issue and recommend the right repair for "
            "your system.",
            "Lenz Heating &amp; Cooling helps Des Moines homeowners get clear answers quickly. Our technicians "
            "inspect your system, explain what is causing the issue, and recommend the repair that makes the most "
            "sense for your home.",
        ],
        "checklist_title": "Scheduling AC repair early can help you:",
        "checklist": [
            "Restore comfort before the next hot day",
            "Prevent minor issues from turning into major repairs",
            "Reduce unnecessary wear on your cooling system",
            "Improve efficiency and help control energy costs",
            "Avoid a complete breakdown during peak summer demand",
        ],
    },

    "problems": {
        "eyebrow": ("i-snow", "What we fix"),
        "title": "Types of AC Problems We Repair",
        "lead": "Our technicians inspect the full cooling system, find the cause, and explain the repair clearly "
                "before any work begins.",
        "items": [
            ("i-heat", "AC Blowing Warm Air", [
                "If your air conditioner is running but the air feels warm, the problem may be related to low "
                "refrigerant, a dirty coil, airflow restrictions, thermostat issues, or compressor trouble.",
                "Our technicians inspect the full cooling system to determine whether the issue is simple, such as "
                "a clogged filter, or more serious, such as a refrigerant leak or failing component. Repairing the "
                "cause early can help restore cooling and reduce strain on your system."]),
            ("i-wind", "Weak Airflow or Uneven Cooling", [
                "Weak airflow can make certain rooms uncomfortable even when your AC is running. This may be caused "
                "by a dirty air filter, blower motor problems, blocked vents, ductwork issues, frozen coils, or "
                "airflow restrictions inside the system.",
                "Professional AC repair can help improve air movement, reduce hot spots, and help your cooling "
                "system keep your home more comfortable during Central Iowa summers."]),
            ("i-info", "AC Not Turning On", [
                "If your AC will not start, the issue may involve the thermostat, electrical connections, "
                "capacitor, contactor, circuit breaker, or outdoor condenser unit.",
                "Our technicians check the electrical and mechanical components carefully so you are not left "
                "guessing. Once we identify the source, we explain the repair clearly and help you understand your "
                "options."]),
            ("i-clock", "Frequent Short Cycling", [
                "Short cycling happens when your AC turns on and off too often without completing a full cooling "
                "cycle. This can increase energy use, reduce comfort, and place extra wear on the system.",
                "Common causes include thermostat issues, restricted airflow, low refrigerant, overheating "
                "components, or an improperly sized system. Addressing short cycling quickly can help prevent "
                "larger cooling system repairs."]),
            ("i-snow", "Frozen AC Coils or Refrigerant Lines", [
                "Ice on your AC system is not normal during cooling season. Frozen coils may point to restricted "
                "airflow, low refrigerant levels, dirty coils, or blower motor issues.",
                "If your system freezes, it should be inspected before being run heavily again. Continuing to "
                "operate a frozen AC can increase the risk of compressor damage and more expensive repairs."]),
            ("i-droplet", "Water Leaks Around the AC", [
                "Air conditioners remove moisture from the air as they cool your home. That moisture should drain "
                "safely away from the system. If you see water around your indoor unit, the issue may be a clogged "
                "condensate drain, frozen coil, damaged drain pan, or installation issue.",
                "AC water leaks should be addressed quickly to prevent water damage and restore proper moisture "
                "removal."]),
            ("i-shield", "Loud Noises or Strange Smells", [
                "Your AC should not bang, clank, buzz loudly, or give off burning or musty odors. These symptoms can "
                "point to loose components, electrical issues, motor problems, mold or moisture buildup, or failing "
                "parts.",
                "Our technicians can inspect the system, identify the source, and recommend the safest repair "
                "before the issue gets worse."]),
        ],
        "help": ("Not sure what&apos;s wrong?", "Tell us what you&apos;re hearing or feeling and we&apos;ll work it out."),
    },

    "band": ("AC not cooling? We&apos;re ready right now.",
             "24/7 emergency AC repair across the Des Moines metro since 2009."),

    "values": {
        "eyebrow": ("i-shield", "Why it matters"),
        "title": "Why Timely AC Repair Matters",
        "lead": "Small AC problems rarely stay small for long. If your system is struggling, running longer, or "
                "showing warning signs, waiting can lead to higher repair costs and more stress during peak summer "
                "heat. Investing in timely air conditioning repair can help improve:",
        "image": ("lenz-comfort-webp", "A family relaxing in a comfortable, cool Des Moines living room"),
        "items": [
            ("Comfort", "A properly repaired AC cools more consistently and helps reduce hot spots throughout the "
                        "home."),
            ("Efficiency", "Fixing airflow, refrigerant, or electrical issues helps your system run more efficiently "
                           "and use less energy."),
            ("System lifespan", "When problems are repaired early, your AC does not have to work as hard, which can "
                                "reduce wear on major components."),
            ("Indoor air quality", "A clean, properly operating system helps manage humidity, airflow, and "
                                   "filtration more effectively."),
            ("Peace of mind", "Knowing what is wrong with your AC and how it can be fixed helps you make confident "
                              "decisions without unnecessary pressure."),
        ],
    },

    "why": {
        "eyebrow": ("i-award", "Why Lenz"),
        "title": "Why Central Iowa Homeowners Choose Lenz Heating &amp; Cooling",
        "lead": "At Lenz Heating &amp; Cooling, we believe AC repair should be honest, clear, and stress-free. Our "
                "team helps homeowners across Urbandale, Des Moines, West Des Moines, Ankeny, Clive, Altoona, "
                "Waukee, and nearby communities restore comfort with practical cooling solutions.",
        "items": [
            ("i-card", "Quality, affordable AC repair in Des Moines",
             "We help homeowners get their cooling systems back on track with honest diagnostics and dependable "
             "repair options. With our &ldquo;To the Penny&rdquo; Pricing Guarantee, you will know the cost upfront "
             "with no hidden fees or surprises."),
            ("i-clock", "24/7 emergency AC repair",
             "AC problems do not always happen during business hours. If your air conditioner stops working during "
             "extreme heat or your home becomes uncomfortable fast, Lenz Heating &amp; Cooling provides emergency "
             "HVAC service to help restore comfort when you need it most."),
            # The doc's wording, which offers a second look but never a free one
            # (ClickUp 09/10 item 6 removed "free second opinions").
            ("i-shield", "Superior customer service",
             "We believe AC repair should be clear, honest, and pressure-free. If another company has recommended a "
             "major repair or system replacement, our experienced technicians can take a second look and help you "
             "understand whether repair or replacement makes the most sense for your home."),
        ],
    },

    "reviews": {
        "title": "Cool Customers Across Central Iowa",
        "lead": "Homeowners throughout Central Iowa trust Lenz Heating &amp; Cooling for clear communication, "
                "honest recommendations, and dependable service.",
    },

    "faq_title": "AC Repair FAQs",
    "faqs": [
        ("How quickly should I schedule AC repair if my system is still running?",
         "If your AC is still running but not performing normally, it is best to schedule service sooner rather "
         "than later. Small issues often become more expensive when the system keeps running under strain, "
         "especially during hot Central Iowa weather."),
        ("What should I do before calling for AC repair?",
         "Before calling, check your thermostat settings, replace the air filter if it is dirty, make sure vents "
         "are open, and confirm the outdoor unit has power. If those simple steps do not solve the problem, a "
         "technician can inspect the system safely."),
        ("Will I know the repair cost before the work begins?",
         "A reputable HVAC company should explain the problem, review your repair options, and provide clear "
         "pricing before completing the work. At Lenz Heating &amp; Cooling, the &ldquo;To the Penny&rdquo; "
         "Pricing Guarantee helps homeowners understand the cost upfront."),
        ("How long does an AC repair usually take?",
         "Many common AC repairs can be completed during the same visit, depending on the issue and whether parts "
         "are available. More complex repairs, such as major component replacement or refrigerant leak repair, may "
         "take longer."),
        ("Can regular maintenance help me avoid future AC repairs?",
         "Yes. Routine maintenance helps catch worn parts, airflow issues, dirty components, and performance "
         "problems before they lead to breakdowns. It is one of the best ways to reduce surprise AC repair calls "
         "during peak summer weather."),
    ],

    "related": {
        "title": "More Cooling Services",
        "text": "Installation, maintenance, and replacement from the same local team, so your AC is covered from "
                "the first day to the last.",
        "go": ("All AC Services", "air-conditioning"),
        "cards": [
            ("cooling", "i-snow", "AC Installation", "Right-sized systems, installed properly.", "ac-installation"),
            ("cooling", "i-calendar", "AC Maintenance", "Seasonal tune-ups that prevent breakdowns.", "ac-maintenance"),
            ("cooling", "i-snow", "AC Replacement", "Efficient upgrades sized to your home.", "ac-replacement"),
            ("both", "i-award", "Maintenance Plans", "Priority dispatch and 10 to 20% off parts.", "maintenance-plans"),
        ],
    },

    "close": {
        "title": "Ready to Get Your Cool Air Back?",
        "paras": [
            "If your AC is blowing warm air, leaking, freezing up, making noise, or struggling to keep your home "
            "comfortable, it is time to have it checked.",
            "Lenz Heating &amp; Cooling provides AC repair in Des Moines, Urbandale, West Des Moines, Ankeny, Clive, "
            "Altoona, Waukee, and surrounding Central Iowa communities. Whether you need routine air conditioning "
            "repair or emergency AC service, our team is ready to help you get your cooling system back on track.",
            "Call (515) 225-6446 or schedule AC repair online today.",
        ],
    },
}

service_page.write(PAGE, HERE)
