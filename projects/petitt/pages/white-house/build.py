#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Petitt Heating & Cooling — "Reliable HVAC & Plumbing Services in White House, TN"
(the /service-areas/white-house/ hub page, refreshed from the client's 7/10 doc).

Reproducible build on top of scripts/elementor_builder.py + ../../tokens.json.
Structural and responsive correctness comes from the shared library; only Petitt's
brand values (tokens) and this page's content/section assembly live here.

Section order mirrors the live page (kit id 4038) and adds the two blocks the client
asked for in the doc's italic notes: a trust bar under the header, and the 4-service
overview as a Card Component Grid with H3 service titles. The card + FAQ patterns are
lifted from the newest page in the kit (id 6619, the White House cooling child page).

Run:  python3 projects/petitt/pages/white-house/build.py
Then: python3 scripts/validate-page.py projects/petitt/pages/white-house/white-house.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def _find_root(p):
    while p != os.path.dirname(p):
        if os.path.exists(os.path.join(p, "AGENTS.md")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repo root (AGENTS.md) not found above %s" % HERE)
ROOT = _find_root(HERE)
SITE = os.path.dirname(os.path.dirname(HERE))          # pages/<slug> -> projects/<site>
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))
C = {k: v["hex"] for k, v in T["colors"].items()}
G = {k: v["global"] for k, v in T["colors"].items()}
F, TG, B, M = T["fonts"], T["typography_globals"], T["bands"], T["media"]
L, PH, CLS = T["links"], T["phone"], T["css_classes"]
NAVY, RED, WHITE, TEXT = C["secondary"], C["accent"], C["white"], C["text"]
SOFT, TINT, BLUE2 = C["soft_gray"], B["tint"], C["blue_2"]
W = T["content_width"]

E.reset_ids(0x30000000)

# ---------------------------------------------------------------- brand wrappers
UP = {"typography_text_transform": "uppercase",
      "typography_letter_spacing": {"unit": "em", "size": -0.02, "sizes": []}}

def h1(txt):
    return E.heading(txt, "h1", color=WHITE, color_global=G["white"], font=F["heading"],
                     size=3.2, unit="em", mobile=2.4, tablet=2.8, lh=1.05, extra=dict(UP))

def h2(txt, color=TEXT, color_global=None, align=None):
    return E.heading(txt, "h2", color=color, color_global=color_global, font=F["heading"],
                     size=2.4, unit="em", mobile=2.0, tablet=2.2, lh=1.1, align=align,
                     extra=dict(UP))

def h3(txt, color=NAVY, color_global=None, align=None):
    return E.heading(txt, "h3", color=color, color_global=color_global, font=F["heading"],
                     size=1.8, unit="em", mobile=1.6, lh=1.15, align=align, extra=dict(UP))

def eyebrow(txt, color=RED, align=None):
    return E.heading(txt, "p", color=color, font=F["body"], size=14, weight="bold",
                     mobile=13, align=align,
                     extra={"typography_text_transform": "uppercase",
                            "typography_letter_spacing": {"unit": "em", "size": 0.2, "sizes": []}})

def body(html, color=TEXT, color_global=None, align=None, size=16, mobile=15, extra=None):
    return E.text(html, color=color, color_global=color_global, font=F["body"], size=size,
                  weight="400", mobile=mobile, lh=1.6, align=align, extra=extra)

def lead(html, color=WHITE, color_global=None, align=None):
    return E.text(html, color=color, color_global=color_global, font=F["body"], size=18,
                  weight="400", mobile=16, lh=1.55, align=align)

def bullets(items, color=TEXT, color_global=None, align=None):
    """Emoji-led bullet list (no icon-font dependency)."""
    return body("".join("<p>%s</p>" % i for i in items), color=color,
                color_global=color_global, align=align)

def btn(txt, url, align="left", spec_key="button"):
    spec = dict(T[spec_key]); spec["align"] = align
    return E.button(txt, url, spec)

def cta(txt, url, align="left"):        return btn(txt, url, align, "button")
def ghost(txt, url, align="left"):      return btn(txt, url, align, "button_ghost")
def phone_btn(align="left"):            return btn(PH["display"], PH["tel"], align, "button_phone")

def band(hexcolor, global_ref=None, overlay=None):
    s = {"background_background": "classic", "background_color": hexcolor}
    if global_ref:
        s.setdefault("__globals__", {})["background_color"] = global_ref
    if overlay:
        s.update({
            "background_overlay_background": "classic",
            "background_overlay_image": {"url": overlay["url"], "id": overlay["id"],
                                         "size": "", "alt": "", "source": "library"},
            "background_overlay_position": "center center",
            "background_overlay_repeat": "no-repeat",
            "background_overlay_opacity": {"unit": "px", "size": 1, "sizes": []},
        })
    return s

def photo_band(media, overlay_color="#171925", opacity=0.55):
    return {"background_background": "classic",
            "background_image": {"url": media["url"], "id": media["id"], "size": "",
                                 "alt": "", "source": "library"},
            "background_position": "center center", "background_repeat": "no-repeat",
            "background_size": "cover",
            "background_overlay_background": "classic",
            "background_overlay_color": overlay_color,
            "background_overlay_opacity": {"unit": "px", "size": opacity, "sizes": []}}

def glass(children, pad=34):
    """Translucent white content card used over photo bands (kit pattern)."""
    c = E.card(children, bg="#FFFFFFCF", radius=15, pad=pad, gap=16)
    c["settings"]["css_classes"] = CLS["glass_card"]
    c["settings"]["padding_mobile"] = {"unit": "px", "top": "22", "right": "18",
                                       "bottom": "22", "left": "18", "isLinked": False}
    return c

def logo(media, alt, width=20, width_mobile=42):
    return E.widget("image", {
        "image": {"url": media["url"], "id": media["id"], "size": "", "alt": alt,
                  "source": "library"},
        "align": "center",
        "width": {"unit": "%", "size": width, "sizes": []},
        "width_tablet": {"unit": "%", "size": 32, "sizes": []},
        "width_mobile": {"unit": "%", "size": width_mobile, "sizes": []},
    })

def rating_badge():
    stars = E.widget("rating", {"icon_gap": {"unit": "px", "size": 2, "sizes": []},
                                "icon_color": "#C9D323", "__globals__": {"icon_color": ""}})
    label = E.heading("5.0 (1000+ Reviews)", "p", color=WHITE, color_global=G["white"],
                      font=F["body"], size=15, weight="bold", mobile=14,
                      extra={"text_shadow_text_shadow_type": "yes",
                             "text_shadow_text_shadow": {"horizontal": 0, "vertical": 0,
                                                         "blur": 20, "color": "#000000"}})
    r = E.row([stars, label], align="center", gap=10)
    r["settings"]["_title"] = "Rating Badge"
    return r

def service_card(icon, alt, title, intro, points, cta_text, cta_url):
    """The kit's Card Component Grid item: white icon box -> H3 -> copy -> red CTA."""
    icon_box = E.card([E.widget("image", {
        "image": {"url": icon["url"], "id": icon["id"], "size": "",
                  "alt": alt, "source": "library"},
        "align": "center",
        "width": {"unit": "%", "size": 34, "sizes": []},
        "width_mobile": {"unit": "%", "size": 30, "sizes": []},
    })], bg=WHITE, radius=15, pad=16, gap=0)
    inner = [icon_box, h3(title, align="center"), body(intro), bullets(points),
             cta(cta_text, cta_url, align="center")]
    c = E.card(inner, bg=SOFT, radius=15, pad=20, gap=12)
    c["settings"].update({
        "background_background": "gradient",
        "background_color_b": TINT,
        "__globals__": {"background_color": G["soft_gray"]},
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 4, "blur": 16,
                                  "spread": 0, "color": "rgba(0, 0, 0, 0.15)"},
        "flex_justify_content": "space-between",
    })
    return c

def trust_item(emoji, label):
    e = E.emoji_icon(emoji, font=F["body"], size=26)
    e["settings"]["align"] = "center"
    t = E.heading(label, "p", color=WHITE, color_global=G["white"], font=F["body"],
                  size=16, weight="bold", mobile=15, align="center")
    return E.column([e, t], gap=4, align="center")

def faq(items):
    a = E.accordion(items)
    a["settings"].update({
        "title_tag": "h3",
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_icon": {"value": "fas fa-chevron-down", "library": "fa-solid"},
        "accordion_item_title_icon_active": {"value": "fas fa-chevron-up", "library": "fa-solid"},
        "n_accordion_animation_duration": {"unit": "ms", "size": 250, "sizes": []},
        "__globals__": {"title_typography_typography": TG["accent"],
                        "active_title_color": G["text"]},
    })
    return a

S = []

# ---------------------------------------------------------------- 1) HERO
hero_bg = band(NAVY, G["secondary"], overlay=M["hero_divider"])
hero_bg["css_classes"] = CLS["hero"]
hero_bg["_title"] = "Hero"
S.append(E.section(hero_bg, [E.row([
    E.column([
        rating_badge(),
        h1("Reliable HVAC &amp; Plumbing Services in White House, TN"),
        lead("Looking for trusted home comfort experts right down the road? "
             "<strong>Petitt Heating &amp; Cooling</strong> delivers fast, dependable heating, "
             "cooling, and plumbing services to keep your system running smoothly and your "
             "family protected all year long."),
        lead("Whether you&rsquo;re in Tyree Springs, Rolling Acres, Walnut Grove, Two Chestnut, "
             "Calista, Pleasant Valley, Mims, Johnsons Crossroads, Cherry Mound, Goodlettsville, "
             "Hendersonville, or surrounding Robertson and Sumner County neighborhoods, our "
             "licensed technicians are just a quick call away."),
        E.row([cta("Call Now", PH["tel"]), ghost("Book Online", L["book"])], gap=16),
    ], width=55, gap=18),
    E.column([E.image(M["white_house_hero"]["url"],
                      "Petitt Heating & Cooling serving White House, TN",
                      M["white_house_hero"]["id"], height=400, height_mobile=250, radius=12)],
             width=45),
], gap=50)], pad=(90, 20, 90, 20), pad_mobile=(55, 18, 55, 18)))

# ---------------------------------------------------------------- 2) TRUST BAR
trust = E.row([
    trust_item("⭐", "5-Star Rated Service"),
    trust_item("🛡️", "Licensed &amp; Insured"),
    trust_item("🏠", "Serving White House Since 2010"),
], align="center", gap=30)
S.append(E.section(band(BLUE2, G["blue_2"]), [trust],
                   pad=(26, 20, 26, 20), pad_mobile=(24, 18, 24, 18)))

# ---------------------------------------------------------------- 3) SERVICE CARD GRID
services = [
    (M["icon_ac"], "Air conditioning services icon", "Cooling &amp; Air Conditioning Services",
     "Don&rsquo;t sweat through another humid Tennessee summer. Our local technicians offer "
     "full-service cooling solutions to keep your home crisp and your energy bills manageable.",
     ["❄️ <strong>Emergency AC Repairs:</strong> Rapid diagnostics to get your cooling back online fast.",
      "⚡ <strong>High-Efficiency Installs:</strong> Modern, quiet units that drastically lower summer utility costs.",
      "🔧 <strong>Precision AC Tune-Ups:</strong> Proactive maintenance to boost performance and prevent breakdowns.",
      "☀️ <strong>Attic Solar Fan Setup:</strong> Naturally venting attic heat to reduce the strain on your AC."],
     "Explore White House Cooling Services", L["cooling_white_house"]),
    (M["icon_heat"], "Heating and gas log services icon", "Heating &amp; Gas Log Solutions",
     "When the winter freeze hits Middle Tennessee, you need a heating system you can trust. "
     "We specialize in the unique heating configurations of local homes.",
     ["🔥 <strong>Furnace Repair &amp; Replacement:</strong> Reliable setups for all gas and electric models.",
      "♨️ <strong>Heat Pump Services:</strong> Specialized repair and installation of high-efficiency heat pump systems.",
      "🪵 <strong>Gas Log Installation &amp; Care:</strong> Professional setup and safety checks for a cozy, mess-free fireplace."],
     "Explore White House Heating Services", L["heating"]),
    (M["icon_plumbing"], "Plumbing and water heater services icon", "Licensed Plumbing &amp; Water Heater Care",
     "Plumbing emergencies shouldn&rsquo;t disrupt your life. Our licensed plumbers provide fast, "
     "honest care to protect your home&rsquo;s flow, appliances, and foundation.",
     ["🚿 <strong>Total Water Heater Care:</strong> Repairs, routine flushes, and new tankless or high-recovery tank installations.",
      "🌊 <strong>Drain &amp; Sewer Clearing:</strong> Blasting through tough blockages and main line backups for immediate relief.",
      "💧 <strong>Leak Detection &amp; Repair:</strong> Pinpointing &ldquo;hidden&rdquo; drips behind walls and floors before they cause major water damage.",
      "🚰 <strong>Fixtures &amp; Water Quality:</strong> Expert faucet installs and whole-home filtration for cleaner household water."],
     "Explore White House Plumbing Services", L["plumbing"]),
    (M["icon_air_quality"], "Indoor air quality services icon", "Indoor Air Quality &amp; Crawl Space Encapsulation",
     "Breathe cleaner air and protect your home&rsquo;s structural integrity. We help White House "
     "homeowners eliminate the airborne allergens and structural moisture issues that thrive in "
     "our climate.",
     ["✨ <strong>Whole-Home Purification:</strong> Advanced UV lights and air filtration to kill bacteria and capture dust.",
      "🏠 <strong>Crawl Space Encapsulation:</strong> Sealing your home from the ground up to prevent mold, mildew, and structural rot.",
      "🌦️ <strong>Humidity Solutions:</strong> Whole-home dehumidifiers and humidifiers that balance moisture levels, prevent mold growth, and ease dry skin or sinus problems."],
     "Explore White House IAQ Services", L["indoor_air_quality"]),
]
S.append(E.section(band(SOFT, G["soft_gray"], overlay=M["section_divider_1"]), [
    eyebrow("White House, TN", align="center"),
    h2("Complete home comfort hub for White House, TN", align="center"),
    body("We don&rsquo;t just pass through town&mdash;we live and work here. Petitt Heating &amp; "
         "Cooling is your all-in-one local contractor for fast diagnostics, system replacements, "
         "and emergency repairs.", align="center"),
    E.grid([service_card(*s) for s in services], cols=2, tablet=2, mobile=1, gap=26),
]))

# ---------------------------------------------------------------- 4) MAINTENANCE PLAN
S.append(E.section(band(NAVY, G["secondary"], overlay=M["section_divider_2"]), [
    logo(M["logo_white"], "Petitt Heating & Cooling"),
    h2("Year-round protection: White House HVAC &amp; plumbing maintenance plans",
       color=WHITE, color_global=G["white"], align="center"),
    E.row([
        E.column([body("At Petitt Heating &amp; Cooling, we make it easy to keep your HVAC and "
                       "plumbing systems running smoothly all year long. Our affordable home "
                       "maintenance plan is designed to take the stress out of system upkeep&mdash;so "
                       "you can focus on enjoying a comfortable home, no matter the season.",
                       color=WHITE, color_global=G["white"])], width=50),
        E.column([body("For as low as <strong>$12 per month</strong>, you&rsquo;ll receive two "
                       "thorough maintenance visits each year, along with discounts on parts and "
                       "new systems. Here&rsquo;s what you get with our plan:",
                       color=WHITE, color_global=G["white"])], width=50),
    ], align="flex-start"),
    E.row([
        E.column([bullets(["✅ 10% off needed parts",
                           "✅ 5% off new systems",
                           "✅ Priority emergency service"],
                          color=WHITE, color_global=G["white"])], width=50),
        E.column([bullets(["✅ No overtime charges",
                           "✅ Appointment reminders"],
                          color=WHITE, color_global=G["white"])], width=50),
    ], align="flex-start"),
    E.column([cta("Sign Up for Our Maintenance Plan", L["maintenance"], align="center")],
             align="center"),
]))

# ---------------------------------------------------------------- 5) FINANCING
finance_card = E.card([
    E.emoji_icon("💳", font=F["body"], size=38),
    h3("Payments that fit your life"),
    bullets(["✅ Cover unexpected HVAC or plumbing costs",
             "✅ Repairs, replacements, and new installs",
             "✅ A payment schedule that works for your budget"]),
], bg=SOFT, radius=15, pad=28, gap=10)
finance_card["settings"]["__globals__"] = {"background_color": G["soft_gray"]}
S.append(E.section(band(WHITE, G["white"]), [
    E.row([
        E.column([
            eyebrow("Financing"),
            h2("Manageable payments for White House families"),
            body("Home emergencies are stressful enough without worrying about the bill. We offer "
                 "White House homeowners simple financing solutions to cover unexpected HVAC or "
                 "plumbing costs. Get back to normal today with a payment schedule that fits your life."),
            cta("Explore Financing Options", L["financing"]),
        ], width=58, gap=16),
        E.column([finance_card], width=42),
    ], gap=40)
]))

# ---------------------------------------------------------------- 6) WHY NEIGHBORS TRUST
S.append(E.section(band(SOFT, G["soft_gray"], overlay=M["section_divider_1"]), [
    E.row([
        E.column([
            h2("Why your neighbors trust Petitt Heating &amp; Cooling"),
            body("Since 2010, the Petitt family has treated every Middle Tennessee home like our "
                 "own. We are a local team that builds trust through honest pricing, certified "
                 "expertise, and strong guarantees."),
            bullets([
                "🎓 <strong>Certified Local Experts:</strong> We hold TN Mechanical and Plumbing licenses with over 50 years of combined experience right here in the White House area.",
                "⏰ <strong>$500 On-Time Guarantee:</strong> We respect your time. If we don&rsquo;t show up on your scheduled installation day, we pay you $500.",
                "🛡️ <strong>10-Year Warranty:</strong> Every new system installation includes a full 10-year parts and labor warranty to protect your investment.",
                "🕐 <strong>12-Hour Priority Repair:</strong> If your main heating or cooling system breaks down, we guarantee a technician will be at your door within 12 hours.",
                "🧹 <strong>Property Protection:</strong> We protect your home by using clean drop cloths and boot covers, leaving your space cleaner than we found it.",
            ]),
            cta("Schedule Service", L["schedule"]),
        ], width=55, gap=16),
        E.column([E.image(M["team"]["url"], "The Petitt Heating & Cooling team in Middle Tennessee",
                          M["team"]["id"], height=460, height_mobile=280, radius=15)], width=45),
    ], gap=40)
]))

# ---------------------------------------------------------------- 7) MAP (live widget)
MAP_IFRAME = (
    '<iframe style="border-radius: 15px;" src="https://www.google.com/maps/embed?pb='
    '!1m14!1m8!1m3!1d14991.140087247724!2d-86.558178!3d36.332168!3m2!1i1024!2i768!4f13.1'
    '!3m3!1m2!1s0x8864471e1260f0bf%3A0x809ce6098346a821!2sPetitt%20Heating%20and%20Cooling'
    '!5e1!3m2!1sen!2sus!4v1770391361674!5m2!1sen!2sus" width="600" height="450" '
    'style="border:0;" allowfullscreen="" loading="lazy" '
    'referrerpolicy="no-referrer-when-downgrade"></iframe>'
)
S.append(E.section(band(WHITE, G["white"]), [
    E.widget("html", {"html": MAP_IFRAME}),
], pad=(40, 20, 40, 20), pad_mobile=(30, 18, 30, 18)))

# ---------------------------------------------------------------- 8) FAQ
FAQS = [
    ("Where is Petitt Heating &amp; Cooling located?",
     "<p>Petitt Heating &amp; Cooling is physically based at Homer Worsham Road in Springfield, TN, "
     "allowing our team to provide rapid, same-day HVAC and plumbing services to nearby White House, "
     "Tyree Springs, and Rolling Acres homeowners. Because we are locally owned and centrally located "
     "in the Robertson and Sumner County area, our trucks can reach your neighborhood quickly without "
     "dispatch delays.</p>"),
    ("Are your HVAC technicians and plumbers licensed and background-checked?",
     "<p>Yes, every technician who wears a Petitt Heating &amp; Cooling uniform is fully licensed, "
     "certified, and has passed a rigorous background check and drug testing panel. We hold "
     "specialized Tennessee Mechanical and Plumbing licenses, ensuring all installations and repairs "
     "near White House meet strict local safety and state building codes.</p>"),
    ("What is the Petitt Promise?",
     "<p>The Petitt Promise is a comprehensive home services guarantee that protects homeowners with "
     "three core policies:</p>"
     "<p><strong>A $500 Schedule Guarantee:</strong> We pay you $500 if our team does not show up on "
     "your installation day.</p>"
     "<p><strong>A 10-Year Warranty:</strong> Every new installation includes a full 10-year parts and "
     "labor warranty.</p>"
     "<p><strong>A 12-Hour Priority Response:</strong> We guarantee a technician will be at your door "
     "within 12 hours if your primary climate system fails.</p>"),
    ("How does Petitt Heating &amp; Cooling handle service pricing?",
     "<p>Petitt Heating &amp; Cooling uses an upfront, flat-rate pricing system. Our technicians "
     "provide an exact quote explaining all required parts and labor before any heating, cooling, or "
     "plumbing work begins. The price you approve upfront is the exact price you pay, with no hidden "
     "hourly charges, surprise mileage fees, or high-pressure sales tactics.</p>"),
]
S.append(E.section(band(SOFT, G["soft_gray"]), [
    h2("Frequently asked questions", align="center"),
    faq(FAQS),
], content_width=T["narrow_width"]))

# ---------------------------------------------------------------- 9) CLOSING CTA
S.append(E.section(photo_band(M["closing_photo"]), [glass([
    h2("Ready to restore your home&rsquo;s comfort? Schedule service in White House now",
       align="center"),
    body("We&rsquo;re known for being honest, respectful, and thorough, offering the best HVAC and "
         "Plumbing services throughout Sumner, Davidson, and Robertson Counties.", align="center"),
    body("Whether you need a precision AC tune-up or an emergency pipe repair, you can trust our "
         "family to take care of yours.", align="center"),
    E.row([phone_btn(align="center"), cta("Schedule Service", L["schedule"], align="center")],
          align="center", gap=16),
])], pad=(90, 20, 90, 20), pad_mobile=(55, 18, 55, 18)))

# ---------------------------------------------------------------- 10) LOCAL BADGE
S.append(E.section(band(WHITE, G["white"]), [
    logo(M["white_house_coc"], "White House Area Chamber of Commerce member", width=34, width_mobile=70),
], pad=(40, 20, 40, 20), pad_mobile=(30, 18, 30, 18)))

doc = E.wrap_page("Reliable HVAC & Plumbing Services in White House, TN", S,
                  {"template": "default"})
out = os.path.join(HERE, "white-house.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
print("Wrote", out, "| sections:", len(S))
