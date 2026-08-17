#!/usr/bin/env python3
"""
Lenz Heating & Cooling — Home page (v4).

Reproducible build on scripts/elementor_builder.py, driven by ../../tokens.json and
../../media.json. Structural + responsive correctness comes from the shared library;
only Lenz's brand values and this page's section assembly live here.

All 15 homepage sections, in source order: hero, trust bar, services, CTA band,
financing, value props, plans, reviews, brands, about, WHO 13, credentials, service
area, FAQs, close + form. Header and footer are separate Theme Builder parts — see
../_theme/build-templates.py.

Run:  python projects/lenz/pages/home/build.py
Then: python scripts/validate-page.py projects/lenz/pages/home/home.json
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
import elementor_builder as E                          # noqa: E402

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))
MEDIA = json.load(open(os.path.join(SITE, "media.json"), encoding="utf-8"))

C  = {k: v["hex"] for k, v in T["roles"].items()}
G  = {k: v["global"] for k, v in T["roles"].items() if v.get("global")}
GR = T["gradients"]
F  = T["fonts"]
TS = T["type_scale"]
NAP = T["nap"]
L  = T["links"]
BTN = T["button"]

NAVY, CREAM, WHITE = C["dark-bg"], C["bg-cream"], C["bg-primary"]
BLUE800 = C["cta-bg-active"]          # blue-800, the trust-bar band
PHONE_TEL, PHONE = NAP["phone"]["tel"], NAP["phone"]["display"]

E.reset_ids(0x10000000)


# --------------------------------------------------------------- helpers ----
def img_url(name):
    """Root-relative, so an exported page is not welded to http://localhost:10010."""
    u = MEDIA[name]["url"]
    if "/wp-content/" not in u:
        return u
    return "/wp-content/" + u.split("/wp-content/", 1)[1]


def img_id(name):
    return MEDIA[name]["id"]


def band(color, glob=None):
    s = {"background_background": "classic", "background_color": color}
    if glob:
        s["__globals__"] = {"background_color": glob}
    return s


def grad(name):
    """Native Elementor gradient from tokens, with stops wired to Global Colors."""
    g = GR[name]
    return E.gradient_bg(
        g["from"], g["to"], angle=g["angle"], gtype=g["type"],
        from_stop=g["from_stop"], to_stop=g["to_stop"],
        frm_global=g.get("from_global"), to_global=g.get("to_global"),
    )


def svg(name, cls="lenz-icon"):
    return '<svg class="%s" aria-hidden="true"><use href="#%s"/></svg>' % (cls, name)


def html(markup, classes=None):
    """Raw-markup widget. Used wherever the design needs the icon sprite or a
    single inline element — the text editor would mangle <use href>."""
    return E.widget("html", {"html": markup}, classes=classes)


def h1(txt):
    return E.heading(txt, "h1", color=WHITE, font=F["heading"],
                     size=TS["h1"]["size"], tablet=TS["h1"]["tablet"], mobile=TS["h1"]["mobile"],
                     weight="800", lh=TS["h1"]["lh"], ls=-0.04)


def h2(txt, color=None, glob=None, align=None):
    return E.heading(txt, "h2", color=color or C["text-primary"], color_global=glob,
                     font=F["heading"], size=TS["h2"]["size"], tablet=TS["h2"]["tablet"],
                     mobile=TS["h2"]["mobile"], weight="800", lh=TS["h2"]["lh"], ls=-0.02,
                     align=align)


def h3(txt, size=None, color=None, classes=None):
    return E.heading(txt, "h3", color=color, font=F["heading"],
                     size=size or TS["h3"]["size"], mobile=TS["h3"]["mobile"],
                     weight="700", lh=1.15, classes=classes)


def body(markup, color=None, size=16, classes=None, glob=None):
    return E.text(markup, color=color or C["text-secondary"], color_global=glob,
                  font=F["body"], size=size, lh=1.7, classes=classes)


def lead(markup, color=None, glob=None):
    return E.text(markup, color=color or C["text-secondary"], color_global=glob,
                  font=F["body"], size=TS["lead"]["size"], lh=TS["lead"]["lh"])


def btn(label, url, variant="primary", icon=None, align="left"):
    """Buttons carry NO colour settings — the stylesheet owns the variants. That is
    deliberate: if Elementor never emits a background for these, there is no
    specificity fight with .lenz-btn--*."""
    spec = {
        "font": F["button"], "weight": "700", "size": 16, "align": align,
        "radius": BTN["_shared"]["radius"], "border_width": BTN["_shared"]["border_width"],
        "padding": BTN["_shared"]["padding"],
        "classes": "lenz-btn lenz-btn--%s" % variant.replace("_", "-"),
    }
    if icon:
        spec["icon"] = icon
    return E.button(label, url, spec)


def ewidth(widget, pct):
    """Give a widget its own width so it can sit DIRECTLY in a row.

    AGENTS.md §7.2: no excess wrapper around a lone widget. Wrapping a single image
    or block in a container purely to carry a column width adds a level to the tree
    the editor then has to navigate — and one more thing a client can delete by
    accident. Always 100% on mobile, which also satisfies the responsive gate.
    """
    widget["settings"].update({
        "_element_width": "initial",
        "_element_custom_width": {"unit": "%", "size": pct, "sizes": []},
        "_element_custom_width_mobile": {"unit": "%", "size": 100, "sizes": []},
    })
    return widget


def eyebrow(icon_name, label, on_warm=False):
    cls = "lenz-eyebrow" + (" lenz-eyebrow--on-warm" if on_warm else "")
    return html('<span class="%s">%s %s</span>' % (cls, svg(icon_name, "lenz-icon-xs"), label))


STARS = '<span class="lenz-stars" role="img" aria-label="5 out of 5 stars">%s</span>' % (
    svg("i-star") * 5
)

SECTIONS = []

# ============================================================ 3. HERO ========
# The navy fill stays a real Elementor background (editable). The two stacked
# radial gradients on top are CSS-owned — .lenz-hero::before.
hero_copy = E.column([
    html('<span class="lenz-hero__eyebrow"><span class="dot"></span> Veteran &amp; woman-owned since 2009</span>'),
    h1("Des Moines&rsquo; Trusted Heating, Cooling &amp; "
       '<span class="lenz-accent">Air Quality</span> Experts'),
    body("Since 2009, Lenz Heating &amp; Cooling has been Central Iowa&rsquo;s go-to team for honest, "
         "hassle-free home comfort. We&rsquo;re a local, veteran-owned, and family-run business based "
         "right here in Urbandale, dedicated to keeping your home comfortable in every season. Whether "
         "you need 24/7 emergency HVAC repair, a new furnace, or a high-efficiency AC installation, we "
         "proudly serve homeowners across Des Moines, West Des Moines, Ankeny, Waukee, and surrounding "
         "Central Iowa communities.",
         color=C["text-on-dark"],
         classes="lenz-hero__sub"),
    html('<span class="lenz-hero__proof">%s<span class="proof-text">Real reviews from Des Moines '
         'homeowners</span></span>' % STARS),
    E.row([
        btn("Get a Free Estimate", L["cta"], "gold"),
        btn("Call " + PHONE, PHONE_TEL, "outline-light"),
    ], gap=12, align="center"),
], width=52, gap=24)

hero_media = ewidth(E.image(
    img_url("lenz-comfort"),
    "A family relaxing together in a bright, comfortable Des Moines living room",
    img_id=img_id("lenz-comfort"), height=560, height_mobile=380, radius=28,
    classes="lenz-hero__media"), 44)

SECTIONS.append(E.section(
    band(NAVY, G.get("dark-bg")),
    [E.row([hero_copy, hero_media], gap=64, align="center")],
    pad=(64, 20, 80, 20), pad_mobile=(48, 18, 56, 18),
    classes="lenz-hero lenz-on-dark", box_classes="lenz-hero__inner",
))

# ==================================================== 4. MICRO TRUST BAR =====
# THE single home for the five trust proofs. Nothing here may be repeated in the
# hero — the hero's trust chips were deliberately removed for exactly this reason.
TRUST = [
    ("Since 2009", "Serving Central Iowa"),
    ("24/7/365", "Emergency service"),
    ("#50871-CL", "Iowa Master Licensed"),
    ("Veteran &amp; Woman-Owned", "Family operated"),
    ("WHO 13 News", "As seen on Hello Iowa"),
]
trust_items = [
    # Text widgets, not raw HTML: these five proofs are exactly the strings a client
    # updates ("Since 2009" ages, the licence number could change). Settings are kept
    # minimal so the stylesheet keeps ownership of type and colour.
    E.container({"content_width": "full", "flex_direction": "column"},
                [E.text(v, classes="lenz-trustbar__value"),
                 E.text(l, classes="lenz-trustbar__label")],
                classes="lenz-trustbar__item")
    for v, l in TRUST
]
SECTIONS.append(E.section(
    band(BLUE800),
    [E.grid(trust_items, cols=5, tablet=3, mobile=2, gap=1,
            classes="lenz-trustbar__grid")],
    pad=(0, 20, 0, 20), pad_mobile=(0, 18, 0, 18),
    classes="lenz-trustbar lenz-on-dark",
))

# ========================================================= 5. SERVICES =======
# (class-suffix, gradient-name, ...) — these differ on purpose. The source names the
# heating card `--warm` but fills it with the TEMPERATURE gradient (orange->purple);
# `--gradient-warm` (gold->orange) belongs to the financing panel. Collapsing the two
# names silently swaps two brand gradients.
LEADS = [
    ("cool", "cool", "i-snow", "Air Conditioning Services", L["cat_air_conditioning"],
     "Keep your home cool and comfortable during hot Iowa summers. Our certified technicians handle "
     "emergency AC repairs, routine performance tune-ups, and energy-efficient air conditioner "
     "replacements tailored to your home&rsquo;s layout and budget.", "Explore AC Services"),
    ("warm", "temperature", "i-flame", "Heating &amp; Furnace Services", L["cat_heating"],
     "Dependable heating built to withstand harsh Central Iowa winters. We provide fast diagnostic "
     "repairs, seasonal safety inspections, and high-efficiency furnace replacements for gas and "
     "electric heating systems.", "Explore Heating Services"),
    ("air", "air", "i-air", "Indoor Air Quality", L["cat_indoor_air_quality"],
     "Breathe cleaner, healthier air year-round. We provide professional air duct cleaning and advanced "
     "whole-home air purifiers to remove dust, allergens, and hot or cold spots.", "Improve Air Quality"),
    ("extra", "extra", "i-wrench", "Additional Services", L["cat_additional"],
     "Specialized home utility solutions that optimize your system&rsquo;s overall efficiency and safety. "
     "Our team installs and services smart thermostats, heat pumps, water heaters (tank and tankless), "
     "custom ductwork repairs and modifications, airflow balancing, and gas lines.",
     "View All Additional Services"),
]

lead_cards = []
for key, gname, icon, title, url, blurb, cta in LEADS:
    lead_cards.append(E.card([
        html('<span class="lenz-lead-card__icon">%s</span>' % svg(icon)),
        h3(title, size=TS["h3_lead"]["size"], color=WHITE),
        body(blurb, color="rgba(255,255,255,0.92)", classes="lenz-lead-card__body"),
        html('<a class="lenz-lead-card__go" href="%s">%s %s</a>'
             % (url, cta, svg("i-arrow", "lenz-icon-sm"))),
    ], gradient=grad(gname), radius=28, pad=32, gap=20,
        classes="lenz-lead-card lenz-lead-card--%s" % key))

# Two across, never four. At four the columns fell to ~230px, which wrapped the body
# copy every three words and stretched the cards into tall text walls.
leads_grid = E.grid(lead_cards, cols=2, tablet=2, mobile=1, gap=24)

# ---- the 17 sub-service cards ----------------------------------------------
# Hand-assembled per the revised decision. Card shape is kept identical to the source
# markup so migrating these to a `service` CPT later is a contents swap.
SERVICES = [
    ("cooling", "i-snow",     "AC Installation",        "Right-sized systems, installed properly.",              "/services/air-conditioning/ac-installation/"),
    ("cooling", "i-wrench",   "AC Repair",              "Fast diagnosis, day or night.",                         "/services/air-conditioning/ac-repair/"),
    ("cooling", "i-calendar", "AC Maintenance",         "Seasonal tune-ups that prevent breakdowns.",            "/services/air-conditioning/ac-maintenance/"),
    ("cooling", "i-snow",     "AC Replacement",         "Efficient upgrades sized to your home.",                "/services/air-conditioning/ac-replacement/"),
    ("heating", "i-flame",    "Heating Installation",   "High-efficiency gas and electric furnaces.",            "/services/heating/heating-installation/"),
    ("heating", "i-wrench",   "Heating Repair",         "No heat? We diagnose it fast.",                         "/services/heating/heating-repair/"),
    ("heating", "i-calendar", "Heating Maintenance",    "Safety inspections before the first freeze.",           "/services/heating/heating-maintenance/"),
    ("heating", "i-heat",     "Heating Replacement",    "Upgrade an aging or failing furnace.",                  "/services/heating/heating-replacement/"),
    ("both",    "i-droplet",  "Humidity Control",       "Whole-home humidifiers and dehumidifiers.",             "/services/indoor-air-quality/humidity-control/"),
    ("both",    "i-shield",   "UV Light Purification",  "Treat air as it moves through the system.",             "/services/indoor-air-quality/uv-light-purification/"),
    ("both",    "i-air",      "Indoor Purification",    "Filtration for dust, dander and allergens.",            "/services/indoor-air-quality/indoor-purification/"),
    ("both",    "i-wind",     "Duct Cleaning",          "Clear out built-up dust and debris.",                   "/services/indoor-air-quality/duct-cleaning/"),
    ("both",    "i-calendar", "Thermostat Services",    "Smart thermostat install and setup.",                   "/services/additional-services/thermostat-services/"),
    ("both",    "i-droplet",  "Water Heater Services",  "Tank and tankless, professionally installed.",          "/services/additional-services/water-heater-services/"),
    ("both",    "i-wind",     "Ductwork",               "Repairs, modifications and airflow balancing.",         "/services/additional-services/ductwork/"),
    ("both",    "i-flame",    "Gas Lines",              "Safe runs for appliances and outdoor setups.",          "/services/additional-services/gas-lines/"),
    ("both",    "i-heat",     "Heat Pumps",             "Heating and cooling from one efficient system.",        "/services/additional-services/heat-pumps/"),
]

service_cards = []
for cat, icon, name, blurb, url in SERVICES:
    card = E.container(
        {"content_width": "full", "flex_direction": "row",
         "flex_direction_mobile": "row",   # icon stays beside the label at every size
         "flex_gap": {"unit": "px", "size": 16, "column": "16", "row": "16"},
         "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}},
        [
            html('<span class="lenz-service-card__icon" data-cat="%s">%s</span>'
                 % (cat, svg(icon, "lenz-icon-sm"))),
            E.column([
                E.heading(name, "h4", font=F["heading"], size=16, weight="700",
                          classes="lenz-service-card__title"),
                body(blurb, size=13, classes="lenz-service-card__blurb"),
            ], gap=2),
        ],
        classes="lenz-service-card")
    service_cards.append(card)

services_grid = E.grid(service_cards, cols=3, tablet=2, mobile=1, gap=16)

service_help = E.container(
    {"content_width": "full", "flex_direction": "row",
     "flex_direction_mobile": "column",
     "flex_gap": {"unit": "px", "size": 16, "column": "16", "row": "16"}},
    [
        E.column([
            E.heading("Not sure what you need?", "h3", font=F["heading"], size=20,
                      weight="700", color=WHITE),
            body("Tell us what you&rsquo;re hearing or feeling and we&rsquo;ll work it out — "
                 "no pressure, no charge.", color=C["text-on-dark"]),
        ], gap=2, classes="lenz-service-help__txt"),
        html('<a class="lenz-phone-link" href="%s">%s %s</a>'
             % (PHONE_TEL, PHONE, svg("i-arrow", "lenz-icon-sm"))),
    ],
    classes="lenz-service-help")

SECTIONS.append(E.section(
    band(CREAM, G.get("bg-cream")),
    [
        E.column([
            eyebrow("i-wrench", "Our services"),
            h2("Complete Heating, Cooling &amp; Essential Home Services"),
            lead("From emergency AC repairs and furnace replacements to gas line runs and indoor air "
                 "quality, Lenz Heating &amp; Cooling provides complete HVAC and home comfort solutions "
                 "across Des Moines and Central Iowa."),
        ], gap=12, classes="lenz-section-head"),
        leads_grid,
        services_grid,
        service_help,
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-services",
))

# ======================================================== 6. CTA BAND ========
# Full-bleed rhythm break. The navy fill is a real Elementor background; the
# three-stop diagonal wash on top is CSS-owned (Elementor's gradient takes two).
SECTIONS.append(E.section(
    band(NAVY, G.get("dark-bg")),
    [E.column([
        E.heading("Heat out? AC down? We&rsquo;re ready right now.", "h2",
                  color=WHITE, font=F["heading"], size=TS["h2"]["size"],
                  tablet=TS["h2"]["tablet"], mobile=TS["h2"]["mobile"],
                  weight="800", lh=1.15, ls=-0.02, align="center"),
        E.text("24/7 emergency service across the Des Moines metro since 2009.",
               color=C["text-on-dark"], font=F["body"], size=TS["lead"]["size"], lh=1.6, align="center"),
        btn("Call " + PHONE, PHONE_TEL, "gold", align="center"),
    ], gap=20, align="center", classes="lenz-cta-band__inner")],
    pad=(48, 20, 48, 20), pad_mobile=(40, 18, 40, 18),
    classes="lenz-cta-band lenz-on-dark",
))

# ======================================================= 7. FINANCING ========
# Sits right after the services grid, where a homeowner is already price-anxious,
# and immediately before the service agreements.
FIN_POINTS = [
    ("i-clock", "Fast online pre-approval", "A few minutes online or during your in-home estimate."),
    ("i-card", "Flexible monthly terms", "Including promotional 0% deferred interest for qualified buyers."),
    ("i-check", "No impact to browse options", "See what you qualify for before you commit to anything."),
]
fin_cards = [
    E.card([
        html('<span class="lenz-financing__point-icon">%s</span>' % svg(ic)),
        E.heading(t, "h3", font=F["heading"], size=TS["lead"]["size"], weight="700",
                  color=NAVY),
        body(d, color=C["text-body-strong"]),
    ], bg="rgba(255,255,255,0.72)", radius=18, pad=24, gap=8,
        border="rgba(7,17,59,0.10)")
    for ic, t, d in FIN_POINTS
]

# Everything on this panel sits on the warm gradient, so text is navy (not white)
# and the primary CTA is a solid navy fill — never a ghost outline.
financing_panel = E.card([
    E.column([
        eyebrow("i-card", "Financing", on_warm=True),
        h2("Financing that fits your budget", color=NAVY),
        E.text("Get pre-approved for a new furnace, an AC replacement, or an emergency repair — "
               "with plans built around your budget, not ours.",
               color=C["text-muted-warm"], font=F["body"], size=TS["lead"]["size"], lh=1.6),
    ], gap=12, classes="lenz-financing__head"),
    E.grid(fin_cards, cols=3, tablet=3, mobile=1, gap=24),
    E.row([
        btn("Explore financing", T["links"]["financing"], "navy"),
        btn("Talk to us: " + PHONE, PHONE_TEL, "ghost-navy"),
    ], gap=16, align="center"),
], gradient=grad("warm"), radius=28, pad=48, gap=40, classes="lenz-financing__panel")

SECTIONS.append(E.section(
    band(CREAM, G.get("bg-cream")),
    [financing_panel],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-financing",
))

# ===================================================== 8. VALUE PROPS ========
VPROPS = [
    ("01", "Veteran-owned &amp; led",
     "Founded by U.S. Marine Corps Veteran Al Lenz — military-grade precision, transparency, "
     "and respect on every home visit."),
    ("02", "Woman-owned &amp; operated",
     "Led with a focus on family-first customer service, clear communication, and home safety "
     "you can rely on."),
    ("03", "24/7 emergency service",
     "HVAC breakdowns don&rsquo;t wait for business hours. Our background-checked, certified "
     "technicians are ready to roll day or night."),
    ("04", "Free second opinions",
     "Got an expensive quote from another contractor? We&rsquo;ll re-evaluate your system for "
     "free — zero pressure, zero obligation."),
]
vprop_cells = [
    E.column([
        # Clipped-text numeral — CSS-owned; Elementor has no background-clip control.
        html('<span class="lenz-stat-num" style="font-size:49px">%s</span>' % num),
        h3(t),
        body(d),
    ], gap=12, classes="lenz-vprop")
    for num, t, d in VPROPS
]
SECTIONS.append(E.section(
    band(WHITE, G.get("bg-primary")),
    [
        E.column([
            eyebrow("i-shield", "Why Lenz"),
            h2("Why homeowners choose Lenz"),
        ], gap=12, classes="lenz-section-head"),
        E.grid(vprop_cells, cols=4, tablet=2, mobile=1, gap=32),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-valueprops",
))

# ================================================= 9. SERVICE AGREEMENTS =====
PLANS = [
    ("red", "RED", "$120", "+ tax / year", "1 year term", False, "Choose RED", "outline", [
        ("2", "maintenance checks"), ("72-hour", "emergency response"),
        ("10%", "off parts &amp; service"), ("$50/yr", "loyalty bonus, consecutive years")]),
    ("white", "WHITE", "$160", "+ tax / year", "1&frac12; year term", False, "Choose WHITE", "outline", [
        ("3", "maintenance checks"), ("48-hour", "emergency response"),
        ("15%", "off parts &amp; service"), ("$100/yr", "loyalty bonus, consecutive years")]),
    ("blue", "BLUE", "$220", "+ tax / year", "2 year term", True, "Choose BLUE", "primary", [
        ("4", "maintenance checks"), ("24-hour", "emergency response"),
        ("20%", "off parts &amp; service"), ("$150/yr", "loyalty bonus, consecutive years")]),
]
plan_cards = []
for key, name, price, unit, meta, featured, cta, variant, rows in PLANS:
    items = "".join(
        '<li>%s<span><b>%s</b> %s</span></li>' % (svg("i-check", "lenz-icon-sm"), b, rest)
        for b, rest in rows)
    kids = []
    if featured:
        # Badge and stripe both take the temperature gradient — but as MARKUP here,
        # not a container background: they are inline decorations inside the card,
        # and a nested Elementor container for a 6px bar would be silly.
        kids.append(html('<span class="lenz-plan__badge">Recommended</span>'))
    kids += [
        html('<span class="lenz-plan__stripe" data-plan="%s" aria-hidden="true"></span>' % key),
        # Prices change. Keeping them in raw HTML would mean a developer edit every
        # time, which defeats the point of building this in Elementor at all.
        E.text(name, classes="lenz-plan__name"),
        E.text("%s <small>%s</small>" % (price, unit), classes="lenz-plan__price"),
        E.text(meta, classes="lenz-plan__meta"),
        html('<ul class="lenz-plan__list">%s</ul>' % items),
        btn(cta, L["cta"], variant),
    ]
    plan_cards.append(E.card(kids, bg=WHITE, radius=28, pad=32, gap=8,
                             border=C["border"] if not featured else C["cta-bg"],
                             classes="lenz-plan lenz-plan--%s" % key))

SECTIONS.append(E.section(
    band(CREAM, G.get("bg-cream")),
    [
        E.column([
            eyebrow("i-award", "Service agreements"),
            h2("Save Money &amp; Prevent Sudden HVAC Breakdowns", align="center"),
            E.text("Keep your heating and cooling systems running smoothly year-round with a Lenz "
                   "Service Agreement. Enjoy priority emergency dispatch, routine maintenance checks, "
                   "exclusive discounts on repairs, and banked loyalty rewards all managed "
                   "automatically by our team.",
                   color=C["text-secondary"], font=F["body"], size=TS["lead"]["size"],
                   lh=1.6, align="center"),
        ], gap=12, align="center", classes="lenz-section-head lenz-section-head--center"),
        E.grid(plan_cards, cols=3, tablet=2, mobile=1, gap=24),
        E.text("We call you to schedule the appointments — no reminder notes on your fridge. "
               "Loyalty bonus transfers to a new homeowner who continues the agreement.",
               color=C["text-secondary"], font=F["body"], size=16, lh=1.6, align="center"),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-plans",
))

# =========================================================== 10. REVIEWS =====
# One weighted pull-quote plus supporting cards, static grid. These are the
# hardcoded fallback quotes — the same ones the source ships and falls back to when
# the Places proxy is unavailable. The skeleton/live states and the REST proxy are a
# later pass, and NO aggregateRating is emitted until verified data exists.
REVIEWS = [
    ("LENZ did a phenomenal job on my evaporator coil replacement. I&rsquo;ve never seen techs work "
     "so hard on a relatively small job — and they came back the next day to make sure it was done "
     "right. Great follow-through and price, and a commitment to honest work. LENZ has my business "
     "for life now.", "Curtis Taylor", True),
    ("Puia was great. Great attitude and service. As always, I appreciate the work you all do and "
     "happy to be a customer.", "Dave Olsen", False),
    ("Your service man did a great job, very courteous young man. Lenz is the best and we appreciate "
     "all you do for us.", "Ron &amp; Janet Hester", False),
]


def review_card(quote, name, featured):
    """<figure>/<blockquote>/<figcaption> as raw markup, deliberately. Rebuilding a
    quotation out of heading + text widgets would lose the semantics the source was
    careful about, and a screen reader would announce a paragraph, not a quote."""
    return html(
        '<figure class="lenz-review %s">%s'
        '<blockquote>&ldquo;%s&rdquo;</blockquote>'
        '<figcaption class="lenz-review__name">— %s</figcaption></figure>'
        % ("lenz-review--feature" if featured else "lenz-review--card", STARS, quote, name))


SECTIONS.append(E.section(
    band(NAVY, G.get("dark-bg")),
    [
        E.column([
            eyebrow("i-star", "Reviews"),
            h2("Over 1,800+ 5-Star Reviews Across Central Iowa", color=WHITE),
            E.text("See what your neighbours in Central Iowa have to say about working with our team.",
                   color=C["text-on-dark"], font=F["body"], size=TS["lead"]["size"], lh=1.6),
        ], gap=12, classes="lenz-section-head"),
        E.row([
            ewidth(review_card(*REVIEWS[0]), 58),
            E.column([review_card(*REVIEWS[1]), review_card(*REVIEWS[2])], width=38, gap=24),
        ], gap=24, align="stretch"),
        html('<p class="lenz-reviews__micro"><a href="%s">Ready for service like this? '
             'Get a free estimate %s</a></p>' % (L["cta"], svg("i-arrow", "lenz-icon-sm"))),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-reviews lenz-on-dark",
))

# ============================================ 11. BRANDS & CREDENTIALS =======
# The nine brands ship as linked text wordmarks and upgrade to logo images as soon as
# each repeater row gets a file — so the strip works today and improves later.
BRANDS = [
    ("Carrier", "https://www.carrier.com/"),
    ("Goodman", "https://www.goodmanmfg.com/"),
    ("Lennox", "https://www.lennox.com/"),
    ("Rheem", "https://www.rheem.com/"),
    ("Trane", "https://www.trane.com/"),
    ("American Pride", "https://www.americanpridehvac.com/"),
    ("Amana", "https://www.amana-hac.com/"),
    ("Optimus", "https://www.optimushvac.com/"),
    ("Bryant", "https://www.bryant.com/"),
]
marquee = E.widget("lenz-marquee", {
    "brands": [
        {"_id": "lzb%02d" % i, "brand_name": n,
         "brand_logo": {"url": "", "id": ""},
         "brand_url": {"url": u, "is_external": "true", "nofollow": "", "custom_attributes": ""}}
        for i, (n, u) in enumerate(BRANDS)
    ],
    "speed": {"unit": "s", "size": 42, "sizes": []},
})

CRED_CHIPS = [
    ("i-award", "BBB Accredited (A+ Rating)"),
    ("i-shield", "Iowa Master Licensed #50871-CL"),
    ("i-check", "Certified Drug-Free Workplace"),
]
SECTIONS.append(E.section(
    band(WHITE, G.get("bg-primary")),
    [
        E.column([
            eyebrow("i-wrench", "Equipment we service"),
            h2("Certified Technicians Servicing All Major HVAC Brands"),
            lead("Whether you need emergency repairs on an existing system or a custom installation "
                 "for a new build, our certified technicians service every major heating and cooling "
                 "brand on the market. We install, repair, and maintain industry-leading systems to "
                 "keep your home running efficiently year-round."),
        ], gap=12, classes="lenz-section-head"),
        marquee,
        html('<div class="lenz-brands__creds">%s</div>' % "".join(
            '<span class="lenz-cred-chip">%s<span>%s</span></span>' % (svg(ic, "lenz-icon-sm"), label)
            for ic, label in CRED_CHIPS)),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-brands",
))

# ============================================================ 12. ABOUT ======
about_body = E.column([
    eyebrow("i-tv", "About Lenz"),
    h2("Meet Lenz Heating &amp; Cooling: Des Moines&rsquo; Family-Owned HVAC Team"),
    # Zero overlap with the trust bar by design — "since 2009" is NOT repeated here.
    html('<div class="lenz-about__stats">'
         '<div><b class="lenz-stat-num">26+ yrs</b><span>Al&rsquo;s experience</span></div>'
         '<div><b class="lenz-stat-num">11</b><span>Cities served</span></div>'
         '<div><b class="lenz-stat-num">A+</b><span>BBB rating</span></div>'
         '</div>'),
    body("Since 2009, Lenz Heating &amp; Cooling has delivered dependable home comfort services "
         "across the Des Moines metro area. Founded by Al Lenz — an Iowa native, U.S. Marine Corps "
         "Veteran, and Iowa Master License holder with over 26 years of hands-on industry experience "
         "— our company was built on a simple promise: to do honest work and stand behind it."),
    body("Co-owned and operated with his wife Jenny, Lenz Heating &amp; Cooling combines technical "
         "expertise with dedicated customer care. Every technician on our team undergoes rigorous "
         "training, background checks, and drug testing so you can feel completely safe letting us "
         "into your home."),
    body("We don&rsquo;t just want to earn your business — we want to earn your trust."),
    E.row([
        btn("Get a free estimate", L["cta"], "primary"),
        btn("Call " + PHONE, PHONE_TEL, "outline"),
    ], gap=12, align="center"),
], gap=16)

about_media = E.column([
    E.image(img_url("lenz-service-van-wrap"),
            "Lenz Heating & Cooling wrapped service van showing the blue and orange wave graphic",
            img_id=img_id("lenz-service-van-wrap"), height=440, height_mobile=280, radius=28),
    html('<p class="lenz-about__caption">Let Our Family Help Yours'
         '<span>Serving the Des Moines metro since 2009</span></p>'),
], classes="lenz-about__media")

# GRID, not a flex row with %-widths. The media bleeds past the content column on one
# side (right, desktop only), and a negative margin on a %-width FLEX item only shrinks
# the slot it occupies — the element still renders at its declared width, so nothing
# visibly extends. On a GRID item the same negative margin genuinely widens the cell,
# which is how the source does it. Neither column carries an explicit width now.
SECTIONS.append(E.section(
    band(CREAM, G.get("bg-cream")),
    [E.grid([about_body, about_media], cols=2, tablet=1, mobile=1, gap=64)],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-about",
))

# ====================================================== WHO 13 NEWS ==========
# Ships with a labelled placeholder; swap for the player once the segment URL is
# supplied. A live embed cannot be built blind — see AGENTS.md rule 8.
SECTIONS.append(E.section(
    band(WHITE, G.get("bg-primary")),
    [E.row([
        E.column([
            eyebrow("i-tv", "As seen on TV"),
            h2("Expert HVAC Tips Featured on WHO 13 News&rsquo; Hello Iowa!"),
            lead("We regularly join WHO 13 News to share seasonal advice, energy-saving tips, and "
                 "home maintenance strategies with our Central Iowa neighbours."),
            btn("Watch Our Latest News Segments", L["cta"], "primary"),
        ], width=50, gap=16),
        ewidth(html('<div class="lenz-who13__media"><div class="lenz-who13__placeholder">%s'
                    '<span>Hello Iowa! segment</span></div></div>' % svg("i-tv")), 46),
    ], gap=64, align="center")],
    pad=(48, 20, 48, 20), pad_mobile=(40, 18, 40, 18),
    classes="lenz-who13",
))

# ============================ TRUSTED, ACCREDITED & PROUDLY LOCAL ============
CREDS = [
    ("i-award", "Accredited &amp; master licensed", [
        "<b>BBB Accredited (A+ Rating)</b> — a verified commitment to transparent pricing and honest service.",
        "<b>Iowa Master Licensed</b> — held by founder Al Lenz (#50871-CL) in HVAC, Refrigeration &amp; Hydronics.",
        "<b>Safety first</b> — background-checked technicians and a certified Drug-Free Workplace."]),
    ("i-shield", "Community &amp; chamber partners", [
        "<b>Chambers</b> — Urbandale, Waukee Area, and Creston.",
        "<b>Community partners</b> — ChildServe, American Heart Association, and the Waukee Leadership Institute.",
        "<b>Local outreach</b> — Operation Lenz a Helping Hand and youth sports sponsors (DCG Football, UGRA Softball)."]),
    ("i-check", "What that means for you", [
        "Straightforward, upfront pricing explained before any work begins.",
        "Trained, vetted technicians you can trust in your home.",
        "A local team invested in the same communities you live in."]),
]
cred_cards = [
    E.card([
        html('<span class="lenz-creds__icon">%s</span>' % svg(ic)),
        h3(title),
        html('<ul class="lenz-creds__list">%s</ul>' % "".join("<li>%s</li>" % i for i in items)),
    ], bg=WHITE, radius=18, pad=24, gap=16, border=C["border"])
    for ic, title, items in CREDS
]
SECTIONS.append(E.section(
    band(C["bg-mist"], G.get("bg-mist")),
    [
        E.column([
            eyebrow("i-award", "Trusted, accredited &amp; proudly local"),
            h2("Trusted, Accredited &amp; Proudly Local"),
        ], gap=12, classes="lenz-section-head"),
        E.grid(cred_cards, cols=3, tablet=2, mobile=1, gap=20),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-creds",
))

# ==================================================== 13. SERVICE AREA =======
# City list plus ONE Google Business Profile embed. Deliberately not an interactive
# map picker — see the do-NOT-fix list in KIT-ANALYSIS.md.
chips = "".join(
    '<span class="lenz-area-chip">%s%s</span>' % (svg("i-pin", "lenz-icon-xs"), city)
    for city in NAP["areas_served"])

SECTIONS.append(E.section(
    band(WHITE, G.get("bg-primary")),
    [
        E.column([
            eyebrow("i-pin", "Service area"),
            h2("Proudly Serving the Greater Des Moines Metropolitan Area &amp; Central Iowa"),
            lead("Based right here in Urbandale, Lenz Heating &amp; Cooling proudly serves Des Moines "
                 "and surrounding communities with round-the-clock repairs, maintenance, and system "
                 "replacements you can rely on."),
        ], gap=12, classes="lenz-section-head"),
        # Copy first, map second — that is also the mobile source order.
        E.row([
            E.column([
                html('<div class="lenz-area__cities">%s</div>' % chips),
                html('<p class="lenz-area__note">%s Not sure if you&rsquo;re in our service radius? '
                     'Give our local office a call at %s to speak with our team.</p>'
                     % (svg("i-info", "lenz-icon-sm"), PHONE)),
                html('<p class="lenz-area__address">%s<a href="%s" target="_blank" '
                     'rel="noopener noreferrer">Headquarters: %s, %s, %s</a></p>'
                     % (svg("i-pin", "lenz-icon-sm"), L["directions"],
                        NAP["hq"]["street"], NAP["hq"]["city"], NAP["hq"]["region"])),
            ], width=48, gap=24),
            # aspect-ratio reserves the space so the lazy iframe cannot shift layout
            ewidth(html('<div class="lenz-area__map"><iframe src="%s" '
                        'title="Lenz Heating &amp; Cooling location and service area map" '
                        'loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
                        'allowfullscreen></iframe></div>' % L["gbp_embed"]), 48),
        ], gap=48, align="center"),
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-area",
))

# ============================================================= 14. FAQS ======
# nested-accordion is an Elementor CORE widget and emits real details/summary
# semantics, which is why it beats rebuilding an accordion out of containers + JS.
FAQS = [
    ("What happens if my heating or AC breaks down after hours or on a weekend?",
     "<p>Lenz Heating &amp; Cooling offers 24/7/365 emergency HVAC service across Greater Des Moines. "
     "When you call (515) 225-6446, you speak directly with our local team, not a third-party call "
     "centre. Our certified technicians are on call day and night to diagnose and repair your heating "
     "or cooling system.</p>"),
    ("How do I know if my repair or quote qualifies for a free estimate?",
     "<p>We provide free, no-obligation estimates for all new equipment installations, full system "
     "replacements, and second opinions. For routine repairs and troubleshooting, we charge a flat "
     "diagnostic fee that covers a full system inspection, followed by upfront pricing before any "
     "repair work begins.</p>"),
    ("Do I have to sit around all day waiting for my technician to show up?",
     "<p>No, we provide clear arrival windows and real-time text tracking updates. You will receive an "
     "automated text notification when your technician is en route, eliminating long waiting windows "
     "and allowing you to plan your day.</p>"),
    ("What can I expect during a home visit from a Lenz technician?",
     "<p>You can expect a professional, clean, and transparent service visit from a direct Lenz "
     "employee. Every home visit includes real-time arrival notifications when your technician is on "
     "the way, uniformed technicians wearing protective shoe covers, and thorough system diagnostics "
     "with clear, flat-rate pricing explained before any work starts.</p>"),
    ("How do I apply for financing for a new furnace or AC installation?",
     "<p>You can apply for HVAC financing through Synchrony Bank online or in person during your "
     "estimate. We offer flexible payment plans, including promotional 0% deferred interest financing "
     "for qualified buyers. Pre-approval takes only a few minutes.</p>"),
    ("What equipment brands do you service?",
     "<p>Carrier, Goodman, Lennox, Rheem, Trane, American Pride, Amana, Optimus, and Bryant. "
     "We&rsquo;re a Rheem Pro Partner.</p>"),
    ("Are your technicians background-checked?",
     "<p>Yes. Every technician completes extensive training and a background check before entering "
     "a home.</p>"),
]
_faq_acc = E.accordion(FAQS, title_font=F["heading"], classes="lenz-faqs__list")
_faq_acc["settings"]["default_state"] = "all_collapsed"

SECTIONS.append(E.section(
    band(CREAM, G.get("bg-cream")),
    [
        E.column([
            eyebrow("i-info", "FAQs"),
            h2("Frequently Asked HVAC Questions", align="center"),
        ], gap=12, align="center", classes="lenz-section-head lenz-section-head--center"),
        # all_collapsed: the source ships every panel closed (aria-expanded="false").
        # Elementor's default expands the first item, which changes what a visitor
        # sees first and pushes the rest of the list down.
        _faq_acc,
    ],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-faqs",
))

# ==================================================== 15. CLOSE + FORM =======
# This is the one section that was a NON-FUNCTIONAL STUB in the source: the static
# form validated client-side and then posted nowhere (lenz.js just hid it and showed
# a success state). Rebuilt on Elementor Pro Forms so it actually submits.
#
# Three fields only, matching the source — every extra field costs completions.
# "Choose a service…|" uses Pro Forms' label|value syntax with an EMPTY value, which
# is what makes it a real prompt rather than a selectable answer: the field is
# required, so submitting without choosing fails validation. The `placeholder` control
# does not produce this for a select — it is silently ignored.
SERVICE_OPTIONS = "\n".join([
    "Choose a service…|",
    "Air Conditioning", "AC Installation", "AC Repair", "AC Replacement",
    "Furnace & Heating", "Heat Pumps", "Ductwork", "Duct Cleaning",
    "Indoor Air Quality", "Water Heater Installation", "Maintenance",
])

estimate_form = E.widget("form", {
    "form_name": "Estimate Request",
    "form_fields": [
        {"_id": "lzfld1", "custom_id": "name", "field_type": "text",
         "field_label": "Name", "placeholder": "", "required": "true", "width": "100"},
        {"_id": "lzfld2", "custom_id": "phone", "field_type": "tel",
         "field_label": "Phone", "placeholder": "", "required": "true", "width": "100"},
        {"_id": "lzfld3", "custom_id": "service", "field_type": "select",
         "field_label": "Service", "required": "true", "width": "100",
         "field_options": SERVICE_OPTIONS},
    ],
    "button_text": "Schedule Your Service Online",
    "button_size": "md",
    "button_width": "100",
    "step_next_label": "Next",
    "success_message": ("Thanks — your request was received. We&rsquo;ll call you back within "
                        "2 hours during business hours. Need help now? Call " + PHONE + "."),
    "error_message": "Please fix the highlighted fields and try again.",
    "required_field_message": "This field is required.",
    "submit_actions": ["email"],
    "email_to": NAP["email"],
    "email_subject": "New estimate request — lenzheatingandcooling.com",
    "email_from_name": "Lenz Website",
    "email_content": "[all-fields]",
    "mark_required": "yes",
}, classes="lenz-form")

SECTIONS.append(E.section(
    band(NAVY, G.get("dark-bg")),
    [E.row([
        E.column([
            E.heading("Let&rsquo;s Get Your Home Comfortable Again", "h2",
                      color=WHITE, font=F["heading"], size=TS["h2"]["size"],
                      tablet=TS["h2"]["tablet"], mobile=TS["h2"]["mobile"],
                      weight="800", lh=1.15, ls=-0.02),
            E.text("Get fast, friendly HVAC repair, maintenance, or replacement from Central "
                   "Iowa&rsquo;s trusted family-owned team. We&rsquo;re ready when you are!",
                   color=C["text-on-dark"], font=F["body"], size=TS["lead"]["size"], lh=1.6),
            html('<div class="lenz-close-form__alt">'
                 '<a class="lenz-phone-link" href="%s">%s%s</a>'
                 '<small>Open 24 hours · Serving the Des Moines metro</small></div>'
                 % (PHONE_TEL, svg("i-phone", "lenz-icon-sm"), PHONE)),
        ], width=46, gap=16),
        E.column([
            E.card([estimate_form], bg=WHITE, radius=28, pad=32, gap=0,
                   classes="lenz-form-card"),
        ], width=48),
    ], gap=64, align="center")],
    pad=(80, 20, 80, 20), pad_mobile=(64, 18, 64, 18),
    classes="lenz-close-form lenz-on-dark",
))

# ------------------------------------------------------------------ emit ----
page = E.wrap_page("Lenz Heating & Cooling — Home (v4)", SECTIONS)
out = os.path.join(HERE, "home.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False)

print("wrote %s" % out)
print("  sections : %d" % len(SECTIONS))
print("  lead cards / service cards : %d / %d" % (len(lead_cards), len(service_cards)))
