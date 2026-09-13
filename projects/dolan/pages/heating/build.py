#!/usr/bin/env python3
"""
Dolan Design HVAC — "Heating Services" page (the heating counterpart to the
/cooling-services/ hub).

Reproducible build on scripts/elementor_builder.py + tokens.json. Structural and
responsive correctness comes from the shared library; only Dolan's brand values
(tokens) and this page's content/section assembly live here.

Link targets were confirmed against the live site (Novamira) on 2026-09-04:
  /hvac-preventive-maintenance/ (230641) and /heat-pump-repair/ (231490) exist.
  Heating repair + heating replacement have NO page in any post type or status, so
  those two cards route to #contact with action labels. See HANDOFF-notes.md.

Run:  python3 projects/dolan/pages/heating/build.py
Then: python3 scripts/validate-page.py projects/dolan/pages/heating/heating.json
"""
import json, os, sys
# Resolve paths independent of nesting depth: HERE = this page folder,
# ROOT = repo root (has AGENTS.md), SITE = projects/<site>/ (holds tokens.json).
HERE = os.path.dirname(os.path.abspath(__file__))
def _find_root(p):
    while p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, "AGENTS.md")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repo root (AGENTS.md) not found above %s" % HERE)
ROOT = _find_root(HERE)
SITE = os.path.dirname(os.path.dirname(HERE))  # pages/<slug> -> projects/<site>
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))
C = {k: v["hex"] for k, v in T["colors"].items()}
G = {k: v["global"] for k, v in T["colors"].items()}
F = T["fonts"]
BLUE, WHITE, BLACK = C["blue"], C["white"], C["black"]
LIGHTBLUE = T["bands"]["lightblue"]
BTN, LINKS, PH = T["button"], T["links"], T["phone"]

# Media confirmed present in the live library (IDs are the 2026/06 set tokens.json uses).
THERMOSTAT_IMG = "https://dolandesignhvac.com/wp-content/uploads/2025/12/smart-thermostat.png"
THERMOSTAT_ID = 232343

# The Schedule page (post 230606). The two service cards whose spoke pages don't exist
# yet point here rather than at the #contact anchor -- this page carries no element with
# id="contact", so that anchor resolves to nothing.
CONTACT_URL = "https://dolandesignhvac.com/contact/"

E.reset_ids(0x20000000)

DIVI_CSS = ("/* Pages using both Elementor AND Divi */\n"
"body.elementor-page.et_pb_button_helper_class #sidebar {\n  display: none;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #left-area {\n  width: 100% !important;\n  float: none !important;\n  padding-right: 0 !important;\n  padding-bottom: 0 !important;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #main-content .container {\n  width: 100%;\n  max-width: 100%;\n  padding-top: 0;\n}\n\n"
"body.elementor-page.et_pb_button_helper_class #main-content .container:before {\n  display: none;\n}")

def h1(txt, extra=None):
    return E.heading(txt, "h1", color=WHITE, color_global=G["white"], font=F["heading"],
                     size=3, unit="em", weight="bold", mobile=2.1, lh=1.15, extra=extra)

def subhead(txt, extra=None):
    """Hero sub-headline. Tagged **h2** because the source doc (written by the SEO
    team) marks it Heading2 — keep the tag, keep the subhead's visual weight."""
    return E.heading(txt, "h2", color=WHITE, color_global=G["white"], font=F["heading"],
                     size=1.2, unit="em", weight="400", mobile=1.1, tablet=1.15,
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

def blue_band():
    """Solid brand-blue band (used once, for 'Why Choose') — breaks up the
    white / light-blue alternation without a third photo overlay."""
    return {"background_background": "classic", "background_color": BLUE,
            "__globals__": {"background_color": G["blue"]}}

def overlay(img, img_id):
    return {"background_background": "classic",
            "background_image": {"url": img, "id": img_id, "size": "", "alt": "", "source": "library"},
            "background_position": "center center", "background_repeat": "no-repeat", "background_size": "cover",
            "background_overlay_background": "classic",
            "background_overlay_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            "__globals__": {"background_overlay_color": G["blue"]}}

def service_card(em, title, desc, link_text, link_url):
    return E.card([emoji(em), h3(title), body(desc), btn(" " + link_text, url=link_url)],
                  bg=LIGHTBLUE, radius=12, pad=26, gap=12)

def system_card(em, title, desc):
    return E.card([emoji(em), h3(title), body(desc)],
                  bg=WHITE, radius=12, pad=26, gap=10)

def reason_card(em, title, desc):
    return E.card([emoji(em), h3(title), body(desc)],
                  bg=WHITE, radius=12, pad=24, gap=8)

def city_card(city):
    return E.card([body("<p style=\"font-size:1.1em;font-weight:700;color:%s;\">📍 %s</p>" % (BLUE, city))],
                  bg=LIGHTBLUE, radius=12, pad=18, gap=6)

def emoji_list(items):
    return body("".join("<p>%s</p>" % it for it in items))

S = []

# ---------------------------------------------------------------- 1) HERO
hero_body = body(
    "<p>When chilly weather arrives in Central North Carolina, you depend on your heating system every "
    "day. Whether you wake up to cold drafts that leave you shivering, a heater that refuses to kick on, "
    "or an unexpected rise in your monthly utility bill, heating issues can ruin anyone&rsquo;s day.</p>"
    "<p>At Dolan Design HVAC &amp; Plumbing, we believe keeping your family warm should be straightforward "
    "and stress-free. For over 25 years, our family has looked after homes across Franklin and Wake "
    "counties with honest advice and dependable fixes.</p>"
    "<p>We hold dual state licenses in both HVAC and plumbing (NC License #20026), so you get the complete "
    "peace of mind that every wire, gas pipe, and air duct is handled safely by one local team you can "
    "trust.</p>", color=WHITE, color_global=G["white"])
hero_body["settings"].update(ewidth(60))
S.append(E.section(overlay(T["hero_image"], 233193), [
    h1("Dependable Heating Services in Louisburg, Wake Forest &amp; Raleigh, NC", extra=ewidth(74)),
    subhead("Reliable Warmth When You Need It Most", extra=ewidth(62)),
    hero_body,
    btn(" Schedule Your Heating Service Online"),
], pad=(100, 20, 100, 20), pad_mobile=(60, 18, 60, 18)))

# ---------------------------------------------------- 2) SERVICES (4 cards)
services = [
    ("🛠️", "Fast Heating Repair &amp; Emergency Service",
     "Heaters have a habit of shutting down on the coldest night of the year, and never on a mild "
     "afternoon. When you are bundling up to stay warm, you need your system fixed quickly. Our vans "
     "arrive fully stocked with common parts so we can get to the bottom of the real issue and get your "
     "home cozy again on the spot.",
     "Schedule Heating Repair", CONTACT_URL),
    ("🔄", "Heating System Replacement &amp; Installation",
     "If your current system is over 12 to 15 years old, breaks down often, or struggles to keep your "
     "home warm, upgrading can save you the chills as well as hundreds on your utility bills. Plus, we do "
     "the real math on your home&rsquo;s square footage so you get a system that fits just right.",
     "Get a Replacement Quote", CONTACT_URL),
    ("📋", "Precision Heating Tune-Ups &amp; Safety Checks",
     "Why wait for a winter heating emergency when you could avoid one altogether in September? Think of "
     "our fall tune-up as an annual check-up for your heater. We clear away summer dust, test safety "
     "switches, check for heat exchanger cracks, and make sure your system won&rsquo;t stutter the second "
     "temperatures drop.",
     "Learn About Our Heating Maintenance", LINKS["hvac_maintenance"]),
    ("⚡", "Dedicated Heat Pump Diagnostics &amp; Care",
     "Because heat pumps work year-round by cooling all summer and heating all winter, they require "
     "specialized care. We inspect outdoor coils, test defrost cycles, and balance auxiliary heat strips "
     "so you don&rsquo;t have to worry about your electric bill sending a shiver down your spine.",
     "Explore Dedicated Heat Pump Services", LINKS["heat_pump_repair"]),
]
S.append(E.section(band(WHITE), [
    h2("How We Keep Your Home Warm, Safe, and Efficient", align="center"),
    body("<p>Whether you need a quick repair on a freezing night or want to plan ahead for a new heating "
         "system this year, we have you covered:</p>", align="center"),
    E.grid([service_card(*s) for s in services], cols=2),
]))

# --------------------------------------------- 3) SYSTEMS WE SERVICE (4 cards)
systems = [
    ("🌡️", "Electric Heat Pumps (Standard &amp; Cold-Climate)",
     "As North Carolina&rsquo;s go-to heating choice, heat pumps handle both summer humidity and winter "
     "chills without the need for two separate systems. Whether you have a traditional central unit, a "
     "ductless mini-split, or a high-efficiency variable-speed system, we keep the heat moving efficiently "
     "without wasting electricity."),
    ("🔥", "Gas Furnaces (Natural Gas &amp; Propane)",
     "A gas furnace delivers fast, toasty heat through your vents. Because we are licensed in both HVAC "
     "and plumbing, we safely service gas valves, burner assemblies, ignitors, flame sensors, and exhaust "
     "flues to keep your home warm and safe from carbon monoxide leaks."),
    ("🔀", "Dual-Fuel (Hybrid) Heating Systems",
     "A dual-fuel system pairs an electric heat pump with a gas furnace backup. It uses the heat pump on "
     "mild 70&deg; days and switches over to gas heat during winter freezes. We install and service hybrid "
     "systems to give you the lowest possible monthly heating bill."),
    ("🌬️", "Ductless Mini-Split Systems",
     "Do you have a garage that feels like a walk-in freezer, or a bonus room that makes you immediately "
     "grab a blanket? A mini-split gives you fast, quiet heat in those chilly rooms, without messing with "
     "the rest of the house or starting a thermostat argument."),
]
S.append(E.section(band(LIGHTBLUE), [
    h2("Heating Systems We Service, Repair &amp; Install", align="center"),
    body("<p>Every home in Central North Carolina is built a little differently. Some neighborhoods in "
         "Raleigh and Wake Forest have natural gas lines, while homes in Louisburg and rural Franklin "
         "County often rely on electric heat pumps or delivered propane. No matter what kind of system "
         "warms your home, our certified technicians have the tools and experience to service it "
         "right:</p>", align="center"),
    E.grid([system_card(*s) for s in systems], cols=2),
]))

# ------------------------------------------- 4) 5 WARNING SIGNS (two-column)
signs_left = E.column([
    h2("Is Your Heater Acting Up? 5 Signs It&rsquo;s Time to Give Us a Call"),
    body("<p>Most heating problems give you a few signs before the entire system stops working. If you "
         "notice any of these issues, giving us a call now can prevent an expensive emergency breakdown "
         "later:</p>"),
    emoji_list([
        "🥶 <strong>Cool or lukewarm air</strong> &mdash; rooms never reach the temperature you set.",
        "🔊 <strong>Loud sounds</strong> &mdash; screeching, banging, persistent clicking, or rattling while it runs.",
        "👃 <strong>Odd smells</strong> &mdash; burning plastic, sulfur, or a heavy damp smell that lingers in the air.",
        "⏱️ <strong>Short-cycling</strong> &mdash; the system shuts off after only two or three minutes.",
        "💸 <strong>A power bill that spikes</strong> out of nowhere, without a big change in the weather.",
    ]),
    body("<p>Don&rsquo;t wait for a total breakdown on the coldest night of the year. Let our team take a "
         "look and fix the small stuff before it becomes a big problem.</p>"),
    btn(" Schedule a Diagnostic"),
], width=55)
signs_right = E.column([
    E.image(THERMOSTAT_IMG,
            "North Carolina family adjusting a smart thermostat to stay warm and lower their heating bill",
            THERMOSTAT_ID, height=480)
], width=45)
S.append(E.section(band(WHITE), [E.row([signs_left, signs_right])]))

# ------------------------------------------------- 5) WHY CHOOSE (blue band)
reasons = [
    ("📍", "25+ Years Keeping Franklin &amp; Wake Warm",
     "We know local homes, North Carolina winters, and how to get the job done right."),
    ("🔧", "Dual-Licensed in HVAC and Plumbing (NC #20026)",
     "One experienced team handles your whole system safely, from electrical to gas lines."),
    ("💰", "Upfront Pricing With Zero Sales Commissions",
     "Our techs earn hourly wages, not commissions, so you get honest advice instead of a high-pressure "
     "sales pitch."),
    ("💳", "Flexible 0% Financing Available",
     "Get the new heat pump or furnace you need today without draining your family savings."),
]
S.append(E.section(blue_band(), [
    h2("Why Central NC Homeowners Choose Dolan Design", color=WHITE, color_global=G["white"], align="center"),
    body("<p>Choosing someone to fix your heating shouldn&rsquo;t feel like a stressful decision. Here is "
         "why your neighbors across Franklin and Wake counties trust Dolan Design HVAC &amp; Plumbing to "
         "keep their homes warm:</p>", color=WHITE, color_global=G["white"], align="center"),
    E.grid([reason_card(*r) for r in reasons], cols=2),
]))

# ------------------------------------------------------- 6) SERVICE AREAS
cities = ["Louisburg", "Wake Forest", "Raleigh", "Youngsville", "Franklinton", "Zebulon"]
S.append(E.section(band(WHITE), [
    h2("Proudly Serving Franklin and Wake Counties", align="center"),
    body("<p>We provide fast, reliable heating services to homeowners across Central North Carolina, "
         "including:</p>", align="center"),
    E.grid([city_card(c) for c in cities], cols=3),
    body("<p>&hellip; and more. Not sure if we cover your street? Give us a quick call. If we can get a "
         "truck to you, we&rsquo;ll be glad to help!</p>", align="center"),
    btn(" Call %s" % PH["display"], url=PH["tel"], align="center"),
]))

# ---------------------------------------------------------------- 7) FAQ
faqs = [
    ("How do I know if I have a heat pump or a furnace?",
     "<p>Look at your outdoor unit in the winter. If it runs when you turn on the heat, you have a heat "
     "pump. If it only turns on in the summer for AC and your indoor heater runs on gas, you have a "
     "furnace.</p>"),
    ("How much does heating repair or replacement cost with Dolan Design?",
     "<p>Repairs start with a simple, flat diagnostic fee to find the problem. Replacements depend on your "
     "home&rsquo;s size, but we always give you an exact, upfront price with zero hidden fees before we "
     "touch a thing.</p>"),
    ("How often should my heating system be serviced?",
     "<p>Once a year in the early fall months. A quick pre-winter tune-up catches worn parts before they "
     "break, keeps your power bills low, and protects your warranty.</p>"),
    ("Is a heat pump better than a gas furnace in North Carolina?",
     "<p>It depends on your setup. Heat pumps are usually cheaper to run in our mild NC winters, but gas "
     "furnaces give you faster, warmer heat on super cold nights. Many local homeowners actually use both "
     "in a hybrid system.</p>"),
    ("What does it mean when &ldquo;Aux Heat&rdquo; turns on?",
     "<p>It means your heat pump called in backup power, like electric heating strips, because it&rsquo;s "
     "freezing outside or you raised the thermostat by several degrees. If it stays on during mild weather "
     "above 45&deg;F, give us a call.</p>"),
    ("How long does a typical home heating system last?",
     "<p>Heat pumps usually last 12 to 15 years because they work year-round for both heating and cooling. "
     "Standalone gas furnaces can last 15 to 20 years since they only run a few months out of the "
     "year.</p>"),
]
S.append(E.section(band(LIGHTBLUE), [
    h2("Frequently Asked Questions About Home Heating", align="center"),
    E.accordion(faqs, title_font=F["heading"]),
]))

# ----------------------------------------------------------- 8) FINAL CTA
cta_h = h2("Ready for Reliable Warmth? Schedule Your Heating Service Today!",
           color=WHITE, color_global=G["white"])
cta_h["settings"].update(ewidth(66))
cta_t = body("<p>Do not wait for the first freezing night to find out your heater is struggling. Trust the "
             "local, dual-licensed experts at Dolan Design HVAC &amp; Plumbing for clear answers, honest "
             "pricing, and friendly service.</p>"
             "<p>Call us today at <a href=\"%s\" style=\"color:#FFFFFF;font-weight:600;\">%s</a> or "
             "schedule your heating service online.</p>" % (PH["tel"], PH["display"]),
             color=WHITE, color_global=G["white"])
cta_t["settings"].update(ewidth(58))
S.append(E.section(overlay(T["cta_image"], 233139), [
    cta_h, cta_t,
    btn(" Schedule Your Heating Service Online Now"),
], pad=(70, 20, 70, 20)))

doc = E.wrap_page("Heating Services in Louisburg, Wake Forest & Raleigh, NC", S,
                  {"template": "default", "hide_title": "yes", "custom_css": DIVI_CSS})
out = os.path.join(HERE, "heating.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
print("Wrote", out, "| sections:", len(S))
