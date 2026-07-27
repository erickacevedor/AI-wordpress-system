#!/usr/bin/env python3
"""
Dolan Design HVAC — "Cooling Services" page.

Reproducible build on scripts/elementor_builder.py + tokens.json. Structural and
responsive correctness comes from the shared library; only Dolan's brand values
(tokens) and this page's content/section assembly live here.

Run:  python3 projects/dolan/build.py
Then: python3 scripts/validate-page.py projects/dolan/output/cooling-services.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import elementor_builder as E

T = json.load(open(os.path.join(HERE, "tokens.json"), encoding="utf-8"))
C = {k: v["hex"] for k, v in T["colors"].items()}
G = {k: v["global"] for k, v in T["colors"].items()}
F = T["fonts"]
BLUE, WHITE, BLACK = C["blue"], C["white"], C["black"]
LIGHTBLUE = T["bands"]["lightblue"]
BTN, LINKS, PH = T["button"], T["links"], T["phone"]

E.reset_ids(0x10000000)

DIVI_CSS = ("/* Pages using both Elementor AND Divi */\n"
"body.elementor-page.et_pb_button_helper_class #sidebar {\n  display: none;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #left-area {\n  width: 100% !important;\n  float: none !important;\n  padding-right: 0 !important;\n  padding-bottom: 0 !important;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #main-content .container {\n  width: 100%;\n  max-width: 100%;\n  padding-top: 0;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #main-content .container:before {\n  display: none;\n}")

def h1(txt, extra=None):
    return E.heading(txt, "h1", color=WHITE, color_global=G["white"], font=F["heading"],
                     size=3, unit="em", weight="bold", mobile=2.1, lh=1.15, extra=extra)

def subhead(txt, extra=None):
    return E.heading(txt, "p", color=WHITE, font=F["heading"], size=1.2, unit="em", weight="400",
                     lh=1.4, extra=extra)

def h2(txt, color=None, color_global=None, align=None):
    return E.heading(txt, "h2", color=color or "#222222", color_global=color_global,
                     font=F["heading"], size=2.2, unit="em", weight="bold",
                     mobile=1.55, tablet=1.9, lh=1.2, align=align)

def h3(txt, color=BLUE):
    return E.heading(txt, "h3", color=color, font=F["heading"], size=1.35, unit="em",
                     weight="bold", mobile=1.2, lh=1.25)

def body(html, color="#222222", color_global=None, align=None):
    return E.text(html, color=color, color_global=color_global, font=F["body"], lh=1.6, align=align)

def btn(txt, url=LINKS["cta"], align="left"):
    spec = dict(BTN); spec["align"] = align
    return E.button(txt, url, spec)

def emoji(e):
    return E.emoji_icon(e, font=F["heading"], size=42)

def ewidth(pct):
    """Constrain a widget's own width (used on the hero text over the photo band)."""
    return {"_element_width": "initial", "_element_custom_width": {"unit": "%", "size": pct, "sizes": []},
            "_element_custom_width_mobile": {"unit": "%", "size": 100, "sizes": []}}

def band(color):       return {"background_background": "classic", "background_color": color}

def overlay(img, img_id, pad_v):
    return {"background_background": "classic",
            "background_image": {"url": img, "id": img_id, "size": "", "alt": "", "source": "library"},
            "background_position": "center center", "background_repeat": "no-repeat", "background_size": "cover",
            "background_overlay_background": "classic",
            "background_overlay_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            "__globals__": {"background_overlay_color": G["blue"]}}

def service_card(em, title, desc, link_text, link_url):
    return E.card([emoji(em), h3(title), body(desc), btn(" " + link_text, url=link_url)],
                  bg=LIGHTBLUE, radius=12, pad=26, gap=12)

def emoji_list(items):
    return body("".join("<p>%s</p>" % it for it in items))

S = []

# 1) HERO (bg image + blue overlay)
hero_body = body(
    "<p>North Carolina summers are brutal, and when the humidity hits Franklin and Wake counties, you "
    "need an AC you can count on. As a local, family-owned team with over 25 years of experience, we&rsquo;ve "
    "fixed just about every cooling disaster imaginable&mdash;so whether your system is blowing warm air on a "
    "hot Saturday, your power bills are spiking, or it&rsquo;s time for a replacement, we&rsquo;re right down "
    "the road and ready to help.</p><p>We proudly serve Louisburg, Raleigh, Wake Forest, Youngsville, Zebulon, "
    "Franklinton, and nearby communities.</p>", color=WHITE, color_global=G["white"])
hero_body["settings"].update(ewidth(60))
S.append(E.section(overlay(T["hero_image"], 233193, 100), [
    h1("Professional Cooling & AC Services in Louisburg, NC", extra=ewidth(72)),
    subhead("Dependable AC repair, maintenance, installation & mini-splits for Franklin & Wake County homes",
            extra=ewidth(62)),
    hero_body,
    btn(" Schedule Your Cooling Service Online"),
], pad=(100, 20, 100, 20), pad_mobile=(60, 18, 60, 18)))

# 2) SERVICES GRID
services = [
    ("🚨", "Emergency AC Repair",
     "When your AC cuts out in the middle of a heatwave, you don&rsquo;t need a corporate sales pitch&mdash;you need cold air, fast. We diagnose the real mechanical issue, explain what went wrong in plain English, and fix it right the first time without sneaky surprise fees.",
     "Explore AC Repair Services", LINKS["ac_repair"]),
    ("🛠️", "Preventative Maintenance & Tune-Ups",
     "The easiest way to avoid a mid-summer breakdown is catching small problems early. Our comprehensive annual tune-ups clear clogged drain lines, clean dirty coils, and make sure your system pulls as little power as possible.",
     "Explore AC Maintenance Services", LINKS["ac_maintenance"]),
    ("♻️", "Air Conditioner Replacement",
     "If your old system is constantly breaking down, leaking refrigerant, or struggling to keep up, throwing more repair money at it doesn&rsquo;t make sense. We give an honest assessment and help you pick a modern, high-efficiency replacement that fits your budget.",
     "Explore AC Replacement Options", LINKS["ac_replacement"]),
    ("🧰", "Professional AC Installation",
     "A new cooling system is only as reliable as the crew setting it up. We take exact measurements, double-check your home&rsquo;s airflow requirements, and install your new central air unit or heat pump to strict local building codes.",
     "Explore AC Installation Services", LINKS["ac_installation"]),
    ("❄️", "Ductless Mini-Split Systems",
     "Got a garage workshop, a sunroom, or a converted attic your central AC just can&rsquo;t reach? Compact ductless mini-splits give you whisper-quiet, pin-point temperature control right where you need it&mdash;no tearing open walls to run ductwork.",
     "Explore Mini-Split Options", LINKS["mini_splits"]),
]
S.append(E.section(band("#FFFFFF"), [
    h2("How We Can Help Keep Your Home Cool", align="center"),
    body("<p>Every house has its own quirks, from drafty older properties downtown to brand-new builds with bonus "
         "rooms that never quite stay cool. We offer straightforward, reliable cooling solutions tailored around "
         "how you actually live.</p>", align="center"),
    E.grid([service_card(*s) for s in services], cols=3),
]))

# 3) WHY CHOOSE (two-column: list + image)
why_left = E.column([
    h2("Why Franklin & Wake County Neighbors Choose Dolan Design"),
    body("<p>We know you have choices when it comes to who you let into your home. Here is why local homeowners "
         "continue to rely on our family for their home comfort.</p>"),
    emoji_list([
        "📍 <strong>25+ years of local experience</strong> in Franklin &amp; Wake counties&mdash;we know the soil, the sticky summers, and the local codes.",
        "🔧 <strong>Dual-trade expertise</strong>&mdash;fully licensed in both HVAC and residential plumbing.",
        "💰 <strong>Honest, upfront pricing</strong> with no high-pressure tactics and zero hidden charges.",
        "💳 <strong>Flexible 0% financing</strong> so you can upgrade without straining household savings.",
    ]),
    btn(" Schedule Your Cooling Service Online"),
], width=50)
why_right = E.column([E.image(T["side_image"], "Dolan Design technician servicing an AC unit", 233248, height=480)], width=50)
S.append(E.section(band(LIGHTBLUE), [E.row([why_left, why_right])]))

# 4) FAQ
faqs = [
    ("What HVAC brands does Dolan Design service and install?",
     "<p><span style=\"font-weight: 400;\">Dolan Design HVAC &amp; Plumbing services and installs all major cooling brands, including Trane, Mitsubishi Electric, Daikin, Carrier, Lennox, Rheem, and Goodman. Our licensed technicians repair, maintain, and install central air conditioners, electric heat pumps, and ductless mini-splits using factory-matched parts.</span></p>"),
    ("What happens when I call Dolan Design for an AC quote or service?",
     "<p><span style=\"font-weight: 400;\">When you call Dolan Design, you speak directly with experienced technicians&mdash;not commissioned salespeople. We perform a straightforward diagnostic, explain your options in plain English, and provide transparent, flat-rate pricing with no hidden fees or high-pressure upselling before any work begins.</span></p>"),
    ("How do I know if I should repair or replace my air conditioner?",
     "<p><span style=\"font-weight: 400;\">You should replace your AC if it is over 10 to 12 years old, requires frequent repairs, or if a single repair costs more than 50% of a new system. Upgrading to a modern, high-efficiency unit also significantly reduces your monthly electricity bills.</span></p>"),
    ("Why is my AC blowing warm air all of a sudden?",
     "<p><span style=\"font-weight: 400;\">An AC blowing warm air is typically caused by a clogged air filter, a tripped circuit breaker, a frozen evaporator coil, or a refrigerant leak. Turn off your thermostat and call a licensed technician to inspect the unit and prevent compressor damage.</span></p>"),
    ("How often should I change my home&rsquo;s air filter in North Carolina?",
     "<p><span style=\"font-weight: 400;\">You should check and replace standard 1-inch air filters every 30 to 60 days. During peak North Carolina summer heat and high pollen seasons, replacing your filter monthly prevents airflow restrictions, lowers energy costs, and keeps your system from freezing up.</span></p>"),
]
S.append(E.section(band(LIGHTBLUE), [
    h2("Frequently Asked Questions", align="center"),
    E.accordion(faqs, title_font=F["heading"]),
]))

# 5) FINAL CTA (bg image + blue overlay)
cta_h = h2("Let&rsquo;s Get Your Cooling Back on Track", color=WHITE, color_global=G["white"])
cta_h["settings"].update(ewidth(60))
cta_t = body("<p><span style=\"font-weight: 400;\">Don&rsquo;t spend another day sweating inside your own living room. "
             "Whether you need an emergency fix or want to talk through replacement options, our local team is just a "
             "quick phone call away.</span></p><p><span style=\"font-weight: 400;\">Call Dolan Design today at "
             "<a href=\"%s\" style=\"color:#FFFFFF;font-weight:600;\">%s</a> or send us a message online to get your "
             "service scheduled!</span></p>" % (PH["tel"], PH["display"]), color=WHITE, color_global=G["white"])
cta_t["settings"].update(ewidth(58))
S.append(E.section(overlay(T["cta_image"], 233139, 70), [
    cta_h, cta_t,
    btn(" Schedule Your Cooling Service Online"),
], pad=(70, 20, 70, 20)))

doc = E.wrap_page("Air Conditioning & Cooling Services in Louisburg, NC", S,
                  {"template": "default", "hide_title": "yes", "custom_css": DIVI_CSS})
out = os.path.join(HERE, "output", "cooling-services.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
print("Wrote", out, "| sections:", len(S))
