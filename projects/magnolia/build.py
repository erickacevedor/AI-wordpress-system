#!/usr/bin/env python3
"""
Magnolia Air — "Air Conditioning Services in Dry Prong, LA" page.

Reproducible build on top of scripts/elementor_builder.py + tokens.json. Structural
and responsive correctness comes from the shared library; only Magnolia's brand
values (tokens) and this page's content/section assembly live here.

Run:  python3 projects/magnolia/build.py
Then: python3 scripts/validate-page.py projects/magnolia/output/air-conditioning-services.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import elementor_builder as E

T = json.load(open(os.path.join(HERE, "tokens.json"), encoding="utf-8"))
C = {k: v["hex"] for k, v in T["colors"].items()}
G = {k: v["global"] for k, v in T["colors"].items()}
F = T["fonts"]
TEAL, GOLD, DARK, WHITE = C["primary"], C["secondary"], C["dark"], C["white"]
CREAM = T["bands"]["cream"]
BTN, LINKS, PH = T["button"], T["links"], T["phone"]

E.reset_ids(0x20000000)

# ---- brand-styled thin wrappers over the generic library ----
def h1(txt, color=WHITE):
    return E.heading(txt, "h1", color=color, font=F["heading"], size=46, weight="800",
                     mobile=29, tablet=36, lh=1.15)

def h2(txt, color=TEAL, align=None, extra=None):
    return E.heading(txt, "h2", color=color, font=F["heading"], size=33, weight="800",
                     mobile=24, tablet=28, lh=1.2, align=align, extra=extra)

def h3(txt, color=TEAL):
    return E.heading(txt, "h3", color=color, font=F["heading"], size=22, weight="800",
                     mobile=20, lh=1.25)

def body(html, color="#000000", align=None, extra=None):
    return E.text(html, color=color, font=F["body"], size=17, weight="300", mobile=15,
                  lh=1.7, align=align, extra=extra)

def btn(txt, url=LINKS["cta"], align="left"):
    spec = dict(BTN); spec["align"] = align
    return E.button(txt, url, spec)

def emoji(e):
    return E.emoji_icon(e, font=F["heading"], size=42)

def band(color):            return {"background_background": "classic", "background_color": color}
def band_global(cg):        return {"background_background": "classic", "__globals__": {"background_color": cg}}

def overlay(img, img_id, pad_v):
    return {"background_background": "classic",
            "background_image": {"url": img, "id": img_id, "size": "", "alt": "", "source": "library"},
            "background_position": "center center", "background_repeat": "no-repeat",
            "background_size": "cover"}

def call_out():
    lab = E.heading("📞 24/7 Emergency Service", "p", color=WHITE, font=F["body"], size=20,
                    weight="300", mobile=16, lh=1.4)
    phone = E.heading('<a href="%s">%s</a>' % (PH["tel"], PH["display"]), "p", color=GOLD,
                      font=F["heading"], size=34, weight="800", mobile=26, lh=1.2)
    return E.column([lab, phone], gap=2)

def service_card(em, title, desc, link_text, link_url):
    return E.card([emoji(em), h3(title), body(desc), btn(" " + link_text, url=link_url)],
                  bg=WHITE, border="#E4D9B8")

def emoji_list(items, on_dark=False):
    color = WHITE if on_dark else "#000000"
    return body("".join("<p>%s</p>" % it for it in items), color=color)

S = []

# 1) HERO
S.append(E.section(band_global(G["dark"]), [E.row([
    E.column([
        h1("Air Conditioning Services In Dry Prong, LA"),
        body("When your AC struggles in a Dry Prong summer, comfort can disappear fast. Warm air, weak airflow, "
             "rising energy bills, high indoor humidity, and unexpected breakdowns can make your home or business "
             "harder to manage. <strong>Magnolia Air</strong> provides dependable residential and commercial cooling "
             "support across Dry Prong and Central Louisiana &mdash; and our NATE-certified technicians help identify "
             "the issue, explain your options, and recommend the right next step.", color=WHITE),
        call_out(),
        btn(" Schedule Service"),
    ], width=58),
    E.column([E.image(T["hero_image"], "Magnolia Air air conditioning services in Dry Prong, LA", 13134, height=440)],
             width=42),
])], pad=(100, 20, 100, 20), pad_mobile=(60, 18, 60, 18)))

# 2) FIND THE RIGHT SERVICE
S.append(E.section(band(CREAM), [
    h2("Find The Right AC Service For Your Cooling Problem", align="center"),
    body("Not every cooling issue needs the same solution. A system blowing warm air may need repair, while an "
         "older unit with repeated breakdowns may be better suited for replacement. A new addition may need "
         "installation, while a working system may simply need maintenance or a seasonal tune-up.", align="center"),
    body("Magnolia Air helps homeowners and businesses choose the right service based on the problem, the "
         "system&rsquo;s condition, and the comfort needs of the property. In Central Louisiana &mdash; where AC "
         "systems run through long stretches of heat and humidity &mdash; getting the right diagnosis helps you "
         "avoid unnecessary repairs, prevent small issues from becoming bigger problems, and make better "
         "decisions about your cooling system.", align="center"),
]))

# 3) SERVICES GRID
services = [
    ("🔧", "AC Repair Service",
     "If your AC blows warm air, leaks water, short cycles, makes unusual noises, or struggles to keep up, we diagnose the issue and explain your repair options clearly.",
     "Explore AC Repair", LINKS["ac_repair"]),
    ("🧰", "AC Maintenance",
     "Routine maintenance keeps your system clean, efficient, and ready for daily use &mdash; improving airflow, reducing strain, and catching small issues before they become larger repairs.",
     "Explore AC Maintenance", LINKS["ac_maintenance"]),
    ("📐", "AC Installation",
     "Ideal for new homes, additions, renovations, or light commercial spaces adding central cooling. We help with proper system sizing, airflow planning, and installation guidance.",
     "Explore AC Installation", LINKS["ac_installation"]),
    ("♻️", "AC Replacement",
     "If your current AC is aging, unreliable, inefficient, or expensive to repair, we help you compare repair costs, system age, comfort concerns, and replacement options.",
     "Explore AC Replacement", LINKS["ac_replacement"]),
    ("⚙️", "AC Tune-Up",
     "A seasonal tune-up prepares your system for heavy cooling demand &mdash; a smart step if it runs but does not feel as strong, efficient, or consistent as it should.",
     "Explore AC Maintenance", LINKS["ac_maintenance"]),
    ("🚨", "Emergency AC Repair",
     "When your AC stops cooling during extreme heat, leaks water, trips the breaker, or creates safety concerns, we offer 24/7 emergency service to restore comfort quickly.",
     "Request Emergency Service", LINKS["emergency"]),
]
S.append(E.section(band(WHITE), [
    h2("AC Services That Keep Central Louisiana Comfortable", align="center"),
    body("Magnolia Air offers a full range of air conditioning services in Dry Prong, LA, and surrounding areas. "
         "Each service is designed for a specific comfort need, so you get the right help without being pushed "
         "toward the wrong solution.", align="center"),
    E.grid([service_card(*s) for s in services], cols=3),
]))

# 4) HOMES & BUSINESSES
res = E.card([emoji("🏠"), h3("For Homeowners"), emoji_list([
    "✅ Warm rooms, uneven cooling &amp; weak airflow",
    "✅ High indoor humidity &amp; cleaner indoor air",
    "✅ Rising energy bills &amp; loud AC noises",
    "✅ Strange odors &amp; frequent breakdowns",
    "✅ Seasonal maintenance, installation &amp; replacement decisions",
])], bg=WHITE, pad=28, gap=12)
com = E.card([emoji("🏢"), h3("For Businesses &amp; Light Commercial"), emoji_list([
    "✅ Cooling system downtime &amp; preventative maintenance",
    "✅ Larger equipment demands",
    "✅ Employee &amp; customer comfort",
    "✅ Emergency AC problems",
    "✅ Replacement / installation planning with clear communication",
])], bg=WHITE, pad=28, gap=12)
S.append(E.section(band(CREAM), [
    h2("Cooling Support For Homes And Businesses", align="center"),
    body("Magnolia Air provides both residential and commercial air conditioning services &mdash; but each "
         "property has different priorities. We focus on practical recommendations, clear communication, and "
         "service that fits the property.", align="center"),
    E.row([res, com]),
]))

# 5) WHEN TO CALL
S.append(E.section(band(WHITE), [
    h2("When It Is Time To Call Magnolia Air", align="center"),
    body("Some AC problems start small, but they can become more expensive when ignored. You can safely check "
         "thermostat settings, replace a dirty filter, and make sure vents are open. Beyond that, professional "
         "service is often the safer and smarter choice. Call Magnolia Air if your AC is:", align="center"),
    E.row([
        E.column([emoji_list([
            "⚠️ Blowing warm air or producing weak airflow",
            "⚠️ Leaving rooms humid or leaking water",
            "⚠️ Making unusual sounds or burning odors",
        ])], width=50),
        E.column([emoji_list([
            "⚠️ Short cycling or running constantly without cooling",
            "⚠️ Tripping the breaker",
            "⚠️ Driving energy bills up without a clear reason",
        ])], width=50),
    ]),
    body("These symptoms can point to airflow restrictions, refrigerant problems, electrical concerns, dirty "
         "coils, clogged drain lines, duct issues, or worn components. A professional inspection finds the root "
         "cause instead of relying on trial and error.", align="center"),
    E.column([btn(" Schedule An Inspection Today", align="center")], align="center"),
]))

# 6) WHY TRUST
S.append(E.section(band_global(G["primary"]), [
    h2("Why Trust Magnolia Air For Your Cooling Needs", color=WHITE, align="center"),
    body("Choosing the right HVAC team matters when your comfort depends on clear answers and reliable work. Our "
         "team understands how Louisiana heat and humidity affect AC performance &mdash; long summer run times "
         "strain equipment, expose airflow problems, and make indoor moisture harder to control. When you choose "
         "Magnolia Air, you can expect:", color=WHITE, align="center"),
    E.row([
        E.column([emoji_list([
            "🎓 <strong>NATE-certified technicians</strong> for residential &amp; light commercial cooling",
            "🤝 <strong>Honest recommendations</strong> for repair, maintenance, installation, replacement &amp; tune-ups",
            "📍 <strong>Local comfort expertise</strong> shaped by Central Louisiana heat &amp; humidity",
        ], on_dark=True)], width=50),
        E.column([emoji_list([
            "💳 <strong>Flexible payment options</strong>, including financing through GoodLeap",
            "🕐 <strong>24/7 emergency service</strong> when cooling problems cannot wait",
            "❄️ <strong>Long-season reliability</strong> tuned to how Louisiana homes &amp; businesses run",
        ], on_dark=True)], width=50),
    ]),
]))

# 7) EMERGENCY HELP
S.append(E.section(band_global(G["dark"]), [
    h2("Emergency AC Help When You Need It Most", color=WHITE, align="center"),
    body("AC emergencies can happen during a hot afternoon, overnight, over the weekend, or when your business "
         "needs to stay open. Emergency service may be needed if your AC stops cooling completely, water is "
         "leaking near the system, electrical concerns appear, or indoor conditions become unsafe during extreme "
         "heat. Fast response matters in Central Louisiana, because indoor temperatures and humidity can rise "
         "quickly when cooling fails.", color=WHITE, align="center"),
    E.column([call_out()], align="center"),
]))

# 8) FAQ
faqs = [
    ("How do I know which AC service I need?",
     "<p>If your system is not cooling, making noise, leaking, or shutting off, start with an AC repair call. If it is working but has not been serviced recently, maintenance or a tune-up may be the better first step. If it is old, unreliable, or costly to repair, we can help you compare repair and replacement options.</p>"),
    ("Do I need AC repair if my system still runs?",
     "<p>Possibly. An AC can run and still have problems &mdash; weak airflow, poor humidity control, short cycling, dirty coils, low refrigerant, or failing parts. If your system runs constantly but your home still feels warm or sticky, it should be inspected.</p>"),
    ("Is AC maintenance really worth it in Louisiana?",
     "<p>Yes. In Central Louisiana, air conditioners often run for long periods through heat and humidity. Regular maintenance helps reduce strain, improve airflow, support efficiency, and catch developing problems before they lead to breakdowns.</p>"),
    ("Can Magnolia Air handle both home and business AC needs?",
     "<p>Yes. We provide residential and commercial air conditioning services in Dry Prong, LA, and surrounding areas &mdash; helping homeowners, business owners, and property managers with repairs, maintenance, installation, replacement, tune-ups, and emergency cooling needs.</p>"),
    ("Should I repair or replace my AC system?",
     "<p>It depends on the system&rsquo;s age, repair history, efficiency, comfort performance, and repair cost. A newer system with a minor issue may be worth repairing. An older system with frequent breakdowns, rising energy bills, or poor humidity control may be better suited for replacement.</p>"),
]
S.append(E.section(band(CREAM), [
    h2("Frequently Asked Questions About Air Conditioning Services", align="center"),
    E.accordion(faqs, title_font=F["heading"]),
]))

# 9) FINAL CTA
S.append(E.section(band_global(G["primary"]), [
    h2("Get Cooling Service That Makes Sense For Your Space", color=WHITE, align="center"),
    body("Do not wait until a small cooling issue turns into a costly breakdown. Magnolia Air provides air "
         "conditioning services in Dry Prong, LA, and surrounding Central Louisiana areas for homeowners and "
         "businesses that need clear answers, skilled service, and dependable comfort. Contact us today to "
         "schedule your air conditioning service.", color=WHITE, align="center"),
    E.column([call_out(), btn(" Request Service", align="center")], align="center", gap=14),
]))

doc = E.wrap_page("Air Conditioning Services in Dry Prong, LA", S, {"template": "default"})
out = os.path.join(HERE, "output", "air-conditioning-services.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
print("Wrote", out, "| sections:", len(S))
