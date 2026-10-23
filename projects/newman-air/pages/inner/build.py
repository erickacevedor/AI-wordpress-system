#!/usr/bin/env python3
"""
Newman Air: inner pages on the V2.1 design.

Content: content/pages/<key>.json (tools/make-content.py: the old callbestinshow.com
pages, rebranded, see content/REVIEW.md), plus three pages written here from their
Google Docs: Financing (Dani), Maintenance Plan (Alexis) and Contact (old page).

Layout: the homepage bands reused as they are (hero + request form card, trust band,
FAQ, Bear Necessities, final CTA; same classes, so the ported prototype CSS styles
them) and the inner-page pieces in plugin/newman-core/assets/css/src/inner.css
(shorter hero, article column + sticky sidebar, steps, mini cards, pricing).

Run:  python projects/newman-air/pages/inner/build.py
Out:  pages/inner/out/<key>.json, pages/inner/pages.json (import manifest),
      pages/inner/widget-classes.json
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402
from brand import PHONE, PHONE_TEL, svg, STARS  # noqa: E402,F401

CONTENT = os.path.join(SITE, "content", "pages")
OUT = os.path.join(HERE, "out")
ARROW = svg("i-arrow")
H1 = "clamp(2.3rem, 4.6vw, 3.9rem)"        # .page-hero h1 (inner.css)
H2 = "clamp(2rem, 4.2vw, 3.4rem)"          # prototype h2 (FAQ, club)
H2_PROSE = "clamp(1.75rem, 3vw, 2.45rem)"  # .prose h2 (inner.css)
OFFICE_EMAIL = "office@newmanheatandair.com"   # Maintenance Plan sign-ups only (Alexis's doc comment)
ADDRESS = "3583 W Market St, Suite 1, Johnson City, TN 37604"   # old Contact page
HOURS = "Mon to Fri, 8 AM to 5 PM"                               # old Contact page: "Mon–Fri, 8 AM–5 PM"

SERVICE_NAV = [
    ("AC Repair", "/services/ac-repair/"), ("AC Installation", "/services/ac-installation/"),
    ("Cooling", "/services/cooling/"), ("Heating Repair", "/services/heating-repair/"),
    ("Heating Installation", "/services/heating-installation/"), ("Heat Pumps", "/services/heat-pumps/"),
    ("Maintenance", "/services/maintenance/"), ("Ductless Mini Splits", "/services/ductless/"),
    ("Ductwork", "/services/ductwork/"), ("Air Handlers", "/services/air-handlers/"),
    ("Air Cleaners", "/services/air-cleaners/"), ("Germicidal Lights", "/services/germicidal-lights/"),
    ("Indoor Air Quality", "/services/indoor-air-quality/"), ("Thermostats", "/services/thermostats/"),
    ("Commercial HVAC", "/services/commercial/"),
]
AREA_NAV = [("Johnson City", "johnson-city"), ("Kingsport", "kingsport"), ("Bristol", "bristol"),
            ("Elizabethton", "elizabethton"), ("Greeneville", "greeneville"), ("Jonesborough", "jonesborough"),
            ("Gray", "gray")]
# Old "Title<br>text" cards -> the page they describe (first match wins).
CARD_LINKS = [("ac repair", "/services/ac-repair/"), ("ac installation", "/services/ac-installation/"),
              ("heating repair", "/services/heating-repair/"), ("heating installation", "/services/heating-installation/"),
              ("maintenance", "/services/maintenance/"), ("commercial", "/services/commercial/"),
              ("ductwork", "/services/ductwork/"), ("ductless", "/services/ductless/"),
              ("mini split", "/services/ductless/"), ("heat pump", "/services/heat-pumps/"),
              ("air handler", "/services/air-handlers/"), ("air cleaner", "/services/air-cleaners/"),
              ("germicidal", "/services/germicidal-lights/"), ("thermostat", "/services/thermostats/"),
              ("indoor air", "/services/indoor-air-quality/")]

# ------------------------------------------------------------ shared bands ----
RIDGES = (
    '<div class="ridges" aria-hidden="true">'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none" data-parallax=".12"><path class="r1" d="M0 150 L110 92 L210 130 L330 58 L460 120 L580 70 L700 128 L840 44 L980 116 L1100 66 L1240 124 L1360 78 L1480 112 L1600 84 V260 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none" data-parallax=".06"><path class="r2" d="M0 190 L140 128 L260 170 L400 112 L540 176 L680 130 L820 186 L960 120 L1100 178 L1250 132 L1390 182 L1520 140 L1600 160 V260 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 260" preserveAspectRatio="none"><path class="r3" d="M0 236 Q400 206 800 230 T1600 220 V260 H0Z"/><g class="trees"><path d="M120 236 l14-40 14 40Z M150 238 l10-28 10 28Z M1380 226 l14-42 14 42Z M1410 228 l10-30 10 30Z M1440 226 l12-36 12 36Z"/></g></svg>'
    '</div>')
FINAL_RIDGES = (
    '<div class="ridges" aria-hidden="true">'
    '<svg viewBox="0 0 1600 200" preserveAspectRatio="none"><path class="r1" d="M0 120 L160 70 L300 110 L460 50 L620 104 L800 40 L980 100 L1140 56 L1300 108 L1460 64 L1600 96 V200 H0Z"/></svg>'
    '<svg viewBox="0 0 1600 200" preserveAspectRatio="none"><path class="r3" d="M0 170 Q400 140 800 166 T1600 156 V200 H0Z"/></svg>'
    '</div>')
BADGE = ('<div class="badge-ring" aria-hidden="true"><div class="disc"></div>'
         '<svg class="ring" viewBox="0 0 150 150"><defs><path id="circ" d="M75 75 m-60 0 a60 60 0 1 1 120 0 a60 60 0 1 1 -120 0"/></defs>'
         '<text><textPath href="#circ">Trust the bear to fix your air · Since 1994 · </textPath></text></svg>'
         '<img class="mascot" src="%s" alt=""></div>' % B.LOGO_BEAR)
TICK = '<span class="tick">%s</span>' % svg("i-check")
TRUST = [('<span class="num" data-count="30" data-suffix="+">30+</span>', "Years Serving Tri-Cities",
          "Local, family-owned &amp; operated since 1994."),
         ('<span class="num" data-count="1100" data-suffix="+">1,100+</span>', "5-Star Reviews",
          "Rated 4.8/5 stars across Johnson City, Kingsport, and Bristol."),
         ('<span class="num">$<span data-count="75">75</span></span>', "Diagnostic Fee",
          "Upfront evaluations and transparent pricing before repairs begin."),
         ('<span class="num">$$</span>', "Flexible Financing",
          "Fast online application through GoodLeap, Synchrony &amp; Hearth.")]


# Inner pages use native widgets wherever the content is text an editor may change
# (Erick 2026-10-23: raw HTML widgets were hard to edit). Raw html stays only for
# decoration: badge ring, ridges, member card, partner logos, bear image.
def eyebrow(label, extra=""):
    """Eyebrow as a native heading rendered as <p> (never a heading tag, Alexis); paw via CSS."""
    return B.E.widget("heading", {"title": label, "header_size": "p"},
                      classes=("nw-eyebrow " + extra).strip())


def lead(markup, cls="lead"):
    return B.text('<p class="%s">%s</p>' % (cls, markup))


def crumbs(trail):
    items = []
    for i, (label, url) in enumerate(trail):
        if i == len(trail) - 1:
            items.append('<li><span aria-current="page">%s</span></li>' % label)
        else:
            items.append('<li><a href="%s">%s</a></li>' % (url, label))
    return B.text('<ol class="crumbs">%s</ol>' % "".join(items), classes="nw-crumbs")


def form_card(title="Request Service", sub="Tell us what's going on and our team will reach out to confirm your visit.",
              form=None, foot="Upfront $75 diagnostic fee. No hidden surprises."):
    return B.box("form-card fade-up", [
        B.raw(BADGE),
        B.heading(title, "h2", size="1.7rem"),
        B.text('<p class="form-sub">%s</p>' % sub),
        form or B.request_form(),
        B.text('<p class="form-foot nw-lock">%s</p>' % foot),
    ], style="--delay:.4s")


def hero(trail, eb, h1, paras, buttons=None, card=True, extra_cls="", card_el=None):
    left = [crumbs(trail)]
    if eb:
        left.append(eyebrow(eb, "fade-up"))
    left.append(B.heading(h1, "h1", size=H1))
    left += [lead(p, "lead fade-up") for p in paras]
    if buttons is None:
        buttons = [("Schedule Online", "#contact", "btn btn-accent btn-xl", "arrow", True),
                   ("Call Us Today", PHONE_TEL, "btn btn-ghost btn-xl", "phone", False)]
    if buttons:
        left.append(B.box("btn-row fade-up", [B.button(l, u, c, icon=i, icon_after=a) for l, u, c, i, a in buttons],
                          style="--delay:.3s"))
    kids = [B.box("", left)]
    if card:
        kids.append(card_el or form_card())
    cls = "hero page-hero topo grain on-dark" + (" " + extra_cls if extra_cls else "") + ("" if card else " solo")
    return B.section(cls, [B.box("wrap", kids), B.raw(RIDGES)], el_id="contact" if card else None)


def trust():
    return B.section("trust", [B.box("band", [B.box("wrap", [
        B.box("trust-item reveal", [B.text(n), B.text("<strong>%s</strong>" % t), B.text("<span>%s</span>" % d)], d=i)
        for i, (n, t, d) in enumerate(TRUST)])])], label="Why homeowners trust us")


def club():
    """Bear Necessities band, as on the homepage (replaces the old Winner's Circle band)."""
    return B.section("club", [B.box("wrap", [
        B.box("reveal", [B.raw('<div class="member-card"><div class="mc-top"><div class="mc-name">BEAR NECESSITIES<small>'
                               'NEWMAN AIR MEMBER</small></div><span class="chip"></span></div><img class="mascot" src="%s" '
                               'alt=""><div class="mc-foot">Starting at<b>$149/year</b></div></div>' % B.LOGO_BEAR)]),
        B.box("reveal", [
            eyebrow("Bear Necessities Maintenance Plan"),
            B.heading('Protect Your HVAC System Starting at <span class="price">$149/Year</span>', "h2", size=H2),
            lead("East Tennessee weather pushes heating and cooling systems to their limits. Our annual maintenance "
                 "plan keeps your equipment running efficiently, helps prevent sudden breakdowns, and gives you "
                 "priority service when you need it most."),
            B.text('<ul class="checks">%s</ul>' % "".join(
                "<li>%s<span><strong>%s</strong> %s</span></li>" % (TICK, a, b) for a, b in [
                    ("Two Seasonal Tune-Ups:", "Comprehensive spring cooling and fall heating inspections."),
                    ("10% Repair Savings:", "Instant discounts on qualifying parts and labor."),
                    ("Priority Scheduling:", "Jump to the front of the line during extreme weather.")])),
            B.button("Explore Plan Details", B.L["maintenance-plan"], "btn btn-accent", icon="arrow", icon_after=True),
        ], d=1),
    ])], el_id="maintenance-plan")


def faq_band(faq, eb="Got Questions?"):
    side = [eyebrow(eb), B.heading(faq["h2"], "h2", size=H2)]
    if faq.get("intro"):
        side.append(lead(faq["intro"]))
    side.append(B.text('<div class="ask"><img class="mascot" src="%s" alt=""><div><strong>Still wondering about '
                       'something?</strong><a href="%s">Call %s</a></div></div>' % (B.LOGO_BEAR, PHONE_TEL, PHONE)))
    plus = {"value": "fas fa-plus", "library": "fa-solid"}
    acc = B.E.widget("nested-accordion", {
        "items": [{"_id": B.E.nid()[-7:], "item_title": html.escape(it["q"], quote=False)} for it in faq["items"]],
        "title_tag": "h3", "faq_schema": "yes", "default_state": "expanded", "max_items_expended": "one",
        "accordion_item_title_icon": plus, "accordion_item_title_icon_active": plus,
    }, elements=[B.box("faq-ans", [B.text("".join("<p>%s</p>" % a for a in it["a"]))]) for it in faq["items"]],
        classes="faq-acc")
    # Tinted band (Erick 2026-10-23): inner pages are white from the article down, the FAQ needs separation.
    return B.section("faq topo light faq-alt", [B.box("wrap", [B.box("faq-side reveal", side), acc])], el_id="faq")


def final(h2, paras, button=None, eb="Trust the bear to fix your air"):
    label, url = (button or ("Schedule Service", B.L["contact"]))
    return B.section("final topo grain on-dark", [
        B.box("wrap reveal", [
            eyebrow(eb),
            B.heading(h2, "h2", size="clamp(2.4rem, 6vw, 4.8rem)"),
            *[lead(p) for p in paras],
            B.box("btn-row", [B.button(label, url, "btn btn-accent btn-xl", icon="arrow", icon_after=True),
                              B.button("Call Us Now", PHONE_TEL, "btn btn-ghost btn-xl", icon="phone")]),
        ]),
        B.raw('<img class="bear-rise mascot" src="%s" alt="">' % B.LOGO_BEAR),
        B.raw(FINAL_RIDGES),
    ])


# ----------------------------------------------------------------- article ----
def card_link(title):
    t = html.unescape(title).lower()
    return next((u for k, u in CARD_LINKS if k in t), None)


def render_items(items):
    out, run = [], []

    def flush():
        if run:
            out.append(B.text("".join(run)))
            run.clear()

    for it in items:
        t = it["t"]
        if t == "p":
            run.append("<p>%s</p>" % it["html"])
        elif t == "ul":
            run.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in it["items"]))
        elif t == "raw":
            run.append(it["html"])
        else:
            flush()
            if t == "h3":
                out.append(B.heading(it["text"], "h3"))
            elif t == "steps":
                out.append(B.text('<ol class="steps-list">%s</ol>' % "".join(
                    "<li><strong>%s</strong>%s</li>" % (s["title"], ("<p>%s</p>" % s["html"]) if s["html"] else "")
                    for s in it["items"])))
            elif t == "cards":
                cards = []
                for c in it["items"]:
                    url = c.get("link") or card_link(c["title"])
                    inner = "<strong>%s</strong>" % c["title"] + ("<span>%s</span>" % c["html"] if c["html"] else "")
                    if url:
                        cards.append('<a class="mini-card" href="%s">%s<span class="more">Learn more %s</span></a>'
                                     % (url, inner, ARROW))
                    else:
                        cards.append('<div class="mini-card">%s</div>' % inner)
                out.append(B.text('<div class="mini-cards">%s</div>' % "".join(cards)))
            elif t == "btn":
                out.append(B.box("btn-row", [B.button(it["label"], it["url"], "btn btn-accent", icon="arrow",
                                                      icon_after=True)]))
    flush()
    return out


def prose(blocks):
    kids = []
    for b in blocks:
        inner = []
        if b["h2"]:
            inner.append(B.heading(b["h2"], "h2", size=H2_PROSE))
        inner += render_items(b["items"])
        kids.append(B.box("prose-block", inner))
    return B.box("prose", kids)


def side_menu(links, current):
    """Native icon list (editable labels and links); the current page carries aria-current."""
    items = []
    for n, u in links:
        link = {"url": u, "is_external": "", "nofollow": "",
                "custom_attributes": "aria-current|page" if u == current else ""}
        items.append({"_id": B.E.nid()[-7:], "text": n, "link": link, "selected_icon": {"value": "", "library": ""}})
    return B.E.widget("icon-list", {"icon_list": items}, classes="side-nav")


def sidebar(current=None, kind="service", nxt=None):
    cards = [B.box("side-card dark", [
        B.heading("Talk to Our Team", "h3"),
        B.text('<p><a class="big-phone" href="%s">%s</a></p>' % (PHONE_TEL, PHONE)),
        B.button("Schedule Online", "#contact", "btn btn-accent", icon="arrow", icon_after=True),
        B.text('<p class="fee nw-lock">$75 diagnostic fee, upfront pricing.</p>'),
    ])]
    if nxt and nxt.get("h2"):
        cards.append(B.box("side-card", [B.heading(nxt["h2"], "h3"), B.text("<p>%s</p>" % nxt["text"]),
                                         B.button("Schedule Now", B.L["contact"], "btn btn-accent")]))
    if kind == "city":
        links = [(n, B.area(s)) for n, s in AREA_NAV]
        title = "Service Areas"
    else:
        links = SERVICE_NAV
        title = "Our Services"
    cards.append(B.box("side-card", [B.heading(title, "h3"), side_menu(links, current)]))
    return B.box("aside", cards, tag="aside")


def article(blocks, side=None, wide=False):
    kids = [prose(blocks)]
    if side is not None and not wide:
        kids.append(side)
    return B.section("article" + (" wide" if wide else ""), [B.box("wrap", kids)])


# ------------------------------------------------------------------- pages ----
def trail_for(doc):
    parts = doc["path"].split("/")
    t = [("Home", "/")]
    if len(parts) == 2:
        parent = {"services": ("Services", "/services/"), "service-area": ("Service Area", "/service-area/")}[parts[0]]
        t.append(parent)
    t.append((doc["title"], "/%s/" % doc["path"]))
    return t


def standard(doc):
    """Services, service areas, the two hubs and About: same skeleton."""
    S = []
    url = "/%s/" % doc["path"]
    h = doc["hero"]
    S.append(hero(trail_for(doc), h["eyebrow"], h["h1"], h["paras"]))
    if doc["type"] != "about":
        S.append(trust())
    kind = "city" if doc["type"] == "city" else "service"
    S.append(article(doc["blocks"], sidebar(url, kind, doc["next"] if doc["cta"] else None)))
    if doc["faq"]:
        S.append(faq_band(doc["faq"]))
    S.append(club())
    end = doc["cta"] or ({"h2": doc["next"]["h2"], "paras": [doc["next"]["text"]], "button": None} if doc["next"] else None)
    if end:
        btn = end.get("button")
        S.append(final(end["h2"], end["paras"], (btn["label"], btn["url"]) if btn else None))
    return S


def legal(doc):
    return [hero(trail_for(doc), "", doc["hero"]["h1"] or doc["title"], doc["hero"]["paras"], buttons=False, card=False,
                 extra_cls="compact"),
            article(doc["blocks"], wide=True)]


def about(doc):
    # DJ's plan doc v2 (Phase B): About says "formerly Best in Show".
    h = dict(doc["hero"])
    h["paras"] = [h["paras"][0].replace("At Newman Air,", "At Newman Air (formerly Best in Show Heating &amp; Cooling),", 1)] + h["paras"][1:]
    return standard(dict(doc, hero=h))


# ---- pages written here from their docs ------------------------------------
def financing():
    """Dani's doc 'Newman Air_Financing' (Drive 17vJiMki6S5G48p3Iwo9ptzvKWLcd9S_2R_Xys_xFsXI, ClickUp 86bcajgzf)."""
    partners = ('<div class="partners"><span><img src="%sfin-goodleap.svg" alt="GoodLeap"></span><span><img '
                'src="%sfin-synchrony.png" alt="Synchrony Bank"></span><span><img class="hearth" src="%sfin-hearth.svg" '
                'alt="Hearth"></span></div>' % (B.IMG, B.IMG, B.IMG))
    P = lambda s: {"t": "p", "html": s}  # noqa: E731
    U = lambda *xs: {"t": "ul", "items": list(xs)}  # noqa: E731
    blocks = [
        {"h2": "Smart Payment Plans That Do Not Strain Your Budget", "items": [
            P("A major HVAC project can feel overwhelming when the cost comes all at once. Financing gives you room to "
              "plan, compare options, and choose the right solution for your home without draining savings in a single payment."),
            P("Newman Air offers financing through:"), {"t": "raw", "html": partners},
            U("<strong>GoodLeap</strong>", "<strong>Synchrony</strong>", "<strong>Hearth</strong>"),
            P("With approved credit, financing may help you:"),
            U("Spread project costs over time", "Move forward with urgent repairs or replacements sooner",
              "Upgrade aging equipment before it fails completely",
              "Choose a higher-efficiency comfort system when it makes sense", "Plan around monthly payments",
              "Protect your budget during unexpected HVAC emergencies"),
            P("Financing terms, approval, payment options, and promotional plans vary by provider. Our team can walk you "
              "through the available options so you know what to expect before making a decision.")]},
        {"h2": "Apply for Financing Through Hearth", "items": [
            P("Want to start with Hearth? You can apply directly through Newman Air&#8217;s Hearth financing application."),
            {"t": "raw", "html": '<p><span class="note">Hearth application link pending: the doc has a placeholder</span></p>'},
            {"t": "btn", "label": "Apply for Financing with Hearth", "url": "#hearth-link-pending"}]},
        {"h2": "What HVAC Services Can Financing Help Cover?", "items": [
            P("Financing may be available for many types of HVAC work. Whether you are planning ahead or dealing with an "
              "unexpected breakdown, Newman Air can help you understand which options may apply to your project."),
            {"t": "h3", "text": "AC Repair and Replacement"},
            P("Do not hibernate in a hot home. Financing may help with major AC repairs, central AC replacement, ductless "
              "mini-split installation, heat pump installation, or other cooling upgrades."),
            {"t": "h3", "text": "Heating Repair and Installation"},
            P("When East Tennessee cold nights settle in, your heating system needs to be ready. Financing may help cover "
              "furnace replacement, heat pump installation, major heating repairs, or system upgrades."),
            {"t": "h3", "text": "Indoor Air Quality Solutions"},
            P("True comfort is about more than temperature. Financing may be available for whole-home air quality "
              "solutions, including air cleaners, air handlers, germicidal lights, and related HVAC improvements."),
            {"t": "h3", "text": "Ductwork and Whole-Home Comfort Projects"},
            P("If your comfort issues are tied to airflow, ductwork, or uneven rooms, financing may help make larger "
              "improvements more manageable.")]},
        {"h2": "Why Financing Can Be a Smart Choice", "items": [
            P("Financing is not about spending more than you need. It is about giving you flexibility when your home "
              "comfort cannot wait."),
            P("It may be a smart option if:"),
            U("Your HVAC system breaks down unexpectedly", "A repair cost is higher than expected",
              "Replacement makes more sense than repeated repairs",
              "You want to upgrade before peak heating or cooling season",
              "Your home needs ductwork or indoor air quality improvements",
              "You want to protect savings while still addressing the problem"),
            P("Our goal is to give you clear information, not pressure. We will explain your service options, discuss "
              "financing availability, and help you decide what fits your home and budget.")]},
        {"h2": "Why Finance with Newman Air?", "items": [
            P("Choosing financing is only part of the decision. You also need an HVAC team that gives honest guidance, "
              "does clean work, and treats your home with respect."),
            P("Newman Air is locally owned and family-operated, with more than 30 years serving homeowners across the "
              "Tri-Cities. Our bear-strong team is known for transparent pricing, friendly service, and dependable workmanship."),
            P("Homeowners choose Newman Air because we offer:"),
            U("Clear recommendations without pressure", "Transparent pricing before work begins",
              "Financing options through GoodLeap, Synchrony, and Hearth",
              "Heating, cooling, ductwork, and indoor air quality solutions",
              "Friendly technicians who respect your home",
              "Local service across Johnson City, Kingsport, Bristol, Jonesborough, and nearby areas"),
            P("When the cost of comfort feels heavy, we help make the next step easier.")]},
    ]
    faq = {"h2": "Frequently Asked Questions About HVAC Financing", "intro": "", "items": [
        {"q": "Who does Newman Air partner with for financing?", "a": [
            "Newman Air offers financing options through <strong>GoodLeap, Synchrony, and Hearth</strong>. Each provider "
            "may offer different payment options, terms, approval requirements, and promotional plans."]},
        {"q": "Can I apply for Hearth financing online?", "a": [
            "Yes. Newman Air can add an <strong>Apply for Financing</strong> button that links directly to the "
            "company&#8217;s Hearth application page. This will take customers to an external Hearth site to complete "
            "the application."]},
        {"q": "What HVAC services can I finance?", "a": [
            "Financing may be available for many HVAC services, including AC replacement, heating replacement, major "
            "repairs, ductwork, indoor air quality upgrades, heat pumps, and full system installations. Availability "
            "depends on the project and financing provider."]},
        {"q": "Is financing only for emergency HVAC repairs?", "a": [
            "No. Financing can help with both urgent repairs and planned upgrades. Some homeowners use financing when a "
            "system fails unexpectedly, while others use it to plan ahead for replacement or efficiency improvements."]},
        {"q": "Will I know my payment options before moving forward?", "a": [
            "In most cases, approved applicants can review available payment options before moving forward. Terms and "
            "approval depend on the financing provider."]},
        {"q": "Does applying for financing guarantee approval?", "a": [
            "No. Financing is subject to credit approval and provider terms. Rates, payment options, promotional plans, "
            "and approval may vary."]},
        {"q": "Can financing help with indoor air quality upgrades?", "a": [
            "Yes, financing may be available for indoor air quality projects such as air cleaners, germicidal lights, "
            "air handler work, and related HVAC improvements. Newman Air can confirm which options may apply to your project."]},
    ]}
    doc = {"key": "financing", "path": "financing", "type": "page", "title": "Financing"}
    S = [hero(trail_for(doc), "Flexible Financing", "Flexible HVAC Financing in Tri-Cities, TN", [
        "HVAC repairs and replacements do not always wait for the right time. A broken AC in the middle of summer, a "
        "failing furnace before the first cold night, or a full system upgrade can put pressure on your home and your "
        "budget fast.",
        "Newman Air offers HVAC financing options for homeowners across Johnson City, Kingsport, Bristol, Jonesborough, "
        "and the greater Tri-Cities area. With trusted financing partners like <strong>GoodLeap, Synchrony, and "
        "Hearth</strong>, you can explore payment options for heating, cooling, ductwork, and indoor air quality "
        "projects without putting off the comfort your home needs.",
        "When your system needs attention, <strong>trust the bear to fix your air</strong> and help you move forward "
        "with clear options."],
        buttons=[("See Financing Options", "#options", "btn btn-accent btn-xl", "arrow", True),
                 ("Call Us Today", PHONE_TEL, "btn btn-ghost btn-xl", "phone", False)]),
         trust()]
    art = article(blocks, sidebar("/financing/", "service"))
    art["settings"]["_element_id"] = "options"
    S += [art, faq_band(faq), club(),
          final("Ready to Talk Through Your HVAC Financing Options?", [
              "You should not have to delay an important HVAC repair, replacement, or comfort upgrade because the timing "
              "is inconvenient. With financing options through GoodLeap, Synchrony, and Hearth, Newman Air can help you "
              "explore payment plans and move forward with confidence.",
              "Schedule service with Newman Air today and ask about HVAC financing options for your heating, cooling, "
              "ductwork, or indoor air quality project. When comfort cannot wait, <strong>trust the bear to fix your air</strong>."])]
    seo = {"title": "HVAC Financing in Johnson City, TN | Newman Air",
           "description": "Flexible HVAC financing in the Tri-Cities through GoodLeap, Synchrony and Hearth. Repairs, "
                          "replacements and upgrades with clear options. Call Newman Air."}
    return doc, S, seo


def plan_form():
    """Maintenance Plan sign-up (Alexis's doc): entries to office@ per her comment. Whether the page keeps a form
    or only 'call the office' is still Megan's call (ClickUp 86bcg1f4b); this is the form version."""
    F = B._field
    return B.E.widget("form", {
        "form_name": "Bear Necessities sign-up",
        "form_fields": [
            F("name", "text", "Your Name", "50"), F("phone", "tel", "Phone Number", "50"),
            F("email", "email", "Email Address", "100"), F("address", "text", "Home Address", "100",
                                                            placeholder="Street Address, City, Zip"),
            F("systems", "select", "How Many Systems Do You Have?", "100",
              field_options="1 System ($149/year)\n2 Systems ($199/year)\n3+ Systems (Pricing Varies)"),
            F("contact_pref", "radio", "How Should We Contact You?", "100", field_options="Call Me\nText Me\nEmail Me",
              inline_list="elementor-subgroup-inline"),
            F("notes", "textarea", "Best Time to Contact / Additional Notes", required=False, rows="2"),
        ],
        "show_labels": "yes", "mark_required": "yes", "button_text": "Submit Request", "button_width": "100",
        "column_gap": {"unit": "px", "size": 12, "sizes": []}, "row_gap": {"unit": "px", "size": 12, "sizes": []},
        "submit_actions": ["email"], "email_to": OFFICE_EMAIL,
        "email_subject": "New Bear Necessities sign-up from newmanair.com", "email_content": "[all-fields]",
        "email_from_name": "Newman Air website", "custom_messages": "yes",
        "success_message": "Thanks! We received your request. Our office will reach out to set up your membership.",
        "required_field_message": "This field is required.", "invalid_message": "Please check the highlighted fields.",
    }, classes="nw-form")


def maintenance_plan():
    """Alexis's doc 'Newman Air Maintenance Plan Page' (Drive 1kgeJXvozdlbvV3j8UYtKSdqVPW4nucvU2q6oJEh_zo4)."""
    doc = {"key": "maintenance-plan", "path": "maintenance-plan", "type": "page", "title": "Bear Necessities Maintenance Plan"}
    card = form_card("Lock In Your Coverage", "Fill out the form to lock in your coverage!", plan_form(),
                     "Online checkout comes later. Our office confirms every sign-up.")
    S = [hero([("Home", "/"), ("Maintenance Plan", "/maintenance-plan/")], "Year-Round Comfort &amp; Peace of Mind",
              "Protect Your Home with the Bear Necessities Maintenance Plan", [
                  "Your heating and cooling system works hard through East Tennessee&#8217;s humid summers and freezing "
                  "winter cold snaps. Skipping routine care allows dust and wear to build up, leading to sudden "
                  "breakdowns, higher energy bills, and a shorter equipment lifespan.",
                  "With the <strong>Bear Necessities Maintenance Plan</strong>, our local technicians handle the heavy "
                  "lifting by inspecting, cleaning, and tuning your system twice a year so you can enjoy worry-free comfort."],
              buttons=[("Call %s" % PHONE, PHONE_TEL, "btn btn-accent btn-xl", "phone", False)], card_el=card)]
    pricing = ('<div class="price-cards">'
               '<div class="price-card featured"><span class="tier">First HVAC System</span><span class="amt">$149<small> / year</small></span>'
               '<p>Covers 1 full year &amp; 2 complete maintenance visits</p></div>'
               '<div class="price-card"><span class="tier">Each Additional System</span><span class="amt">$50<small> / year</small></span>'
               '<p>Full annual coverage for multi-zone homes or extra units</p></div></div>'
               '<p class="fine">All memberships run for one full year from the date of sign-up and include two complete '
               'seasonal visits (one heating tune-up and one cooling tune-up).</p>')
    S.append(B.section("article wide", [B.box("wrap", [B.box("prose", [
        B.box("prose-block", [eyebrow("Transparent Pricing"), B.heading("Simple, Upfront Membership Pricing", "h2", size=H2_PROSE),
                              B.text("<p>No surprise fees or hidden catches, just honest, reliable protection for your home.</p>"),
                              B.text(pricing)]),
        B.box("prose-block", [eyebrow("Membership Advantages"), B.heading("What&#8217;s Included in Your Membership?", "h2", size=H2_PROSE),
                              B.text("<p>Joining our maintenance plan gives you more than routine tune-ups. You get priority care and complete peace of mind:</p>"
                                     "<ul>%s</ul>" % "".join("<li><strong>%s</strong> %s</li>" % x for x in [
                                         ("Two Seasonal Tune-Ups Per Year:", "One comprehensive heating inspection in the fall and one full cooling check in the spring."),
                                         ("10% Discount on Repairs &amp; Priority Service:", "Save on qualifying parts and labor, plus jump to the front of the line when emergency service is needed."),
                                         ("Deep System Cleaning:", "Includes condenser coil, condensate drain, and evaporator coil cleaning to prevent water leaks and keep your system running efficiently."),
                                         ("Full Inspection &amp; Filter Service:", "We inspect electrical components, test safety controls, verify performance, and install fresh air filters (using customer-provided filters)."),
                                         ("Automated Seasonal Reminders:", "We track your schedule and remind you when it&#8217;s time for your bi-annual maintenance visits.")]))]),
        B.box("prose-block", [eyebrow("Simple Three-Step Process"), B.heading("How the Plan Works", "h2", size=H2_PROSE),
                              B.text('<ol class="steps-list">%s</ol>' % "".join("<li><strong>%s</strong><p>%s</p></li>" % x for x in [
                                  ("Sign Up &amp; Lock In Savings", "Call our office or submit a quick request online to start your one-year membership."),
                                  ("We Schedule Your Tune-Ups", "Our local office team reaches out every spring and fall to book your maintenance visits at a time that fits your busy schedule."),
                                  ("Enjoy Worry-Free Comfort", "Sit back and relax knowing your system is running at peak performance, backed by 10% repair savings and priority service.")])),
                              B.box("btn-row", [B.button("Get Started Today", "#contact", "btn btn-accent", icon="arrow", icon_after=True),
                                                B.button("Speak With Our Team", PHONE_TEL, "btn btn-ghost", icon="phone")])]),
    ])])]))
    S.append(faq_band({"h2": "Frequently Asked Questions About Maintenance", "intro": "", "items": [
        {"q": "Does the $149 fee cover my entire home if I have two HVAC units?", "a": [
            "<strong>No, the $149 fee covers your primary HVAC system for one full year.</strong> You can add each additional "
            "heating and cooling unit in your home to your plan for just <strong>$50 per year</strong>, which includes two "
            "complete maintenance visits for those secondary systems as well."]},
        {"q": "When are the two seasonal maintenance visits performed?", "a": [
            "<strong>Maintenance visits are scheduled twice a year, once in the spring and once in the fall.</strong> Your "
            "spring visit preps your air conditioner or heat pump for summer heat, while your fall visit ensures your furnace "
            "or backup heating coils run safely before winter freezes arrive."]},
        {"q": "What if I need repairs during my maintenance visit?", "a": [
            "<strong>If our technician finds worn parts or electrical issues, we will provide a clear, upfront estimate "
            "before doing any work.</strong> As a maintenance plan member, you automatically receive a <strong>10% discount "
            "on all qualifying repairs</strong>."]},
        {"q": "Do you supply the replacement air filters?", "a": [
            "<strong>No, our technicians install customer-provided air filters during tune-up visits.</strong> If you have "
            "your preferred filter brand or media size ready when we arrive, our technician will inspect the air box, remove "
            "the old filter, and properly install the fresh replacement at no extra charge."]},
    ]}))
    S.append(final("Ready to Protect Your Home Year-Round?", [
        "Join the Bear Necessities Maintenance Plan today starting at just <strong>$149/year</strong>. Enjoy total peace of "
        "mind, lower energy bills, and priority service whenever you need us."], ("Join Today", "#contact"),
        eb="Start Your Membership"))
    seo = {"title": "Bear Necessities HVAC Maintenance Plan | Newman Air",
           "description": "Protect your home's comfort with the Bear Necessities Maintenance Plan from Newman Air. Two "
                          "tune-ups a year, priority scheduling & 10% repair discounts."}
    return doc, S, seo


def contact():
    """Old Contact page, rebranded. The old 'Plumbing Repair' heading was a template leftover: HVAC services listed."""
    doc = {"key": "contact-us", "path": "contact-us", "type": "page", "title": "Contact Us"}
    card = form_card("Contact Newman Air Today!", "Send us a message and our team will get back to you.")
    S = [hero([("Home", "/"), ("Contact Us", "/contact-us/")], "Contact Us", "Reach Out to Us Today", [
        "If you have a residential or commercial HVAC issue that needs professional attention, you can count on us at "
        "Newman Air to provide a long-lasting solution. It doesn&#8217;t matter if it&#8217;s a quick repair or a complex "
        "replacement, your comfort matters to us, and we&#8217;re always ready to get to work!"],
        buttons=[("Call Us Today", PHONE_TEL, "btn btn-accent btn-xl", "phone", False)], card_el=card)]
    info = B.box("aside", [B.box("side-card dark", [
        B.heading("Newman Air", "h3"),
        B.E.widget("icon-list", {"icon_list": [
            {"_id": "nwct01", "text": ADDRESS, "selected_icon": {"value": "fas fa-map-marker-alt", "library": "fa-solid"}},
            {"_id": "nwct02", "text": PHONE, "link": {"url": PHONE_TEL, "is_external": "", "nofollow": ""},
             "selected_icon": {"value": "fas fa-phone-alt", "library": "fa-solid"}},
            {"_id": "nwct03", "text": B.EMAIL, "link": {"url": "mailto:" + B.EMAIL, "is_external": "", "nofollow": ""},
             "selected_icon": {"value": "fas fa-envelope", "library": "fa-solid"}},
            {"_id": "nwct04", "text": HOURS, "selected_icon": {"value": "far fa-clock", "library": "fa-regular"}},
        ]}, classes="contact-list"),
    ])], tag="aside")
    areas = [{"title": "%s, TN" % n, "html": "", "link": B.area(s)} for n, s in AREA_NAV]
    S.append(B.section("article", [B.box("wrap", [B.box("prose", [
        B.box("prose-block", [B.heading("Proudly Serving the Following Communities", "h2", size=H2_PROSE)] +
              render_items([{"t": "cards", "items": areas}])),
        B.box("prose-block", [B.heading("We Offer a Full Range of HVAC Services", "h2", size=H2_PROSE),
                              B.text("<ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in SERVICE_NAV))]),
    ]), info])]))
    S.append(club())
    seo = {"title": "Contact Us | Newman Air",
           "description": "Contact Newman Air for heating and cooling service in Johnson City and the Tri-Cities. Call "
                          "(423) 753-7788 or send us a message."}
    return doc, S, seo


def simple(key, title, h1, eb, body, seo, trail=None):
    doc = {"key": key, "path": key, "type": "page", "title": title}
    S = [hero(trail or [("Home", "/"), (title, "/%s/" % key)], eb, h1, [], buttons=False, card=False, extra_cls="compact")]
    if body:
        S.append(B.section("article wide", [B.box("wrap", [B.box("prose", body)])]))
    return doc, S, seo


def thanks(key):
    body = [B.box("prose-block", [eyebrow("About Us"), B.heading("Trusted Comfort Since 1994", "h2", size=H2_PROSE),
                                  B.text("<p>At Newman Air, we&#8217;ve spent over 30 years delivering honest, reliable service "
                                         "with the care and craftsmanship every neighbor deserves.</p>"),
                                  B.box("btn-row", [B.button("Learn More", B.L["about"], "btn btn-accent", icon="arrow", icon_after=True),
                                                    B.button("Back to Home", "/", "btn btn-ghost")])])]
    title = {"thank-you": "Thank You", "confirmed": "Confirmed"}[key]
    return simple(key, title, "Thank You for your message. We will get back to you ASAP!", "Confirmed", body,
                  {"title": "%s | Newman Air" % title, "description": "", "robots": "noindex"})


def a2p():
    embed = ('<div class="embed-wrap"><iframe src="https://api.leadconnectorhq.com/widget/form/XVWf4Kh8yQaMh79JUrby" '
             'style="width:100%;height:100%;border:none;border-radius:4px" id="inline-XVWf4Kh8yQaMh79JUrby" '
             'data-layout="{\'id\':\'INLINE\'}" data-trigger-type="alwaysShow" data-trigger-value="" '
             'data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" '
             'data-deactivation-value="" data-form-name="A2P Optin Form" data-height="906" '
             'data-layout-iframe-id="inline-XVWf4Kh8yQaMh79JUrby" data-form-id="XVWf4Kh8yQaMh79JUrby" '
             'title="A2P Optin Form"></iframe><script src="https://link.msgsndr.com/js/form_embed.js"></script></div>')
    return simple("a2p-submission", "A2P Submission", "Text Message Opt-In", "", [B.box("prose-block", [B.raw(embed)])],
                  {"title": "A2P Submission | Newman Air", "description": "", "robots": "noindex"})


def blog_page():
    """Blog index: an Elementor Pro Posts grid (the old site had no /blog/ page; its posts lived under /blog/)."""
    grid = B.E.widget("posts", {
        "_skin": "classic", "classic_columns": "3", "classic_columns_tablet": "2", "classic_columns_mobile": "1",
        "classic_posts_per_page": 12, "classic_thumbnail": "top", "classic_thumbnail_size_size": "medium_large",
        "classic_item_ratio": {"unit": "px", "size": 0.62, "sizes": []}, "classic_show_title": "yes",
        "classic_title_tag": "h3", "classic_show_excerpt": "yes", "classic_excerpt_length": 22,
        "classic_meta_data": ["date"], "classic_show_read_more": "yes", "classic_read_more_text": "Read More",
        "posts_post_type": "post", "posts_exclude": ["manual_selection"], "posts_exclude_ids": ["1"],  # WordPress's "Hello world!"
        "pagination_type": "numbers",
    }, classes="blog-grid")
    doc, S, seo = simple("blog", "Blog", "Blog", "Newman Air Blog", [B.box("prose-block", [grid])],
                         {"title": "Blog | Newman Air", "description": "HVAC tips and answers for Tri-Cities homeowners "
                                                                       "from the Newman Air team."})
    S[1]["settings"]["css_classes"] = S[1]["settings"].get("css_classes", "") + " blog-index"
    return doc, S + [club(), final("Reliable Home Comfort Is Just a Call or Click Away", [
        "From simple repairs to full system replacements, we bring honest answers and upfront pricing to every doorstep "
        "in the Tri-Cities. Give our friendly team a call or book your service visit online in just a few clicks."])], seo


def sitemap(all_pages):
    groups = [("Company", [("Home", "/"), ("About Us", "/about-us/"), ("Contact Us", "/contact-us/"),
                           ("Financing", "/financing/"), ("Maintenance Plan", "/maintenance-plan/")]),
              ("HVAC Services", [("All Services", "/services/")] + SERVICE_NAV),
              ("Service Area", [("All Areas", "/service-area/")] + [(n, B.area(s)) for n, s in AREA_NAV] +
               [("Privacy Policy", "/privacy-policy/"), ("Terms and Conditions", "/terms-and-conditions/")])]
    cols = "".join('<div><h3>%s</h3><ul>%s</ul></div>' % (g, "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in items))
                   for g, items in groups)
    return simple("sitemap", "Sitemap", "Sitemap", "", [B.box("prose-block", [B.text('<div class="sitemap-cols">%s</div>' % cols)])],
                  {"title": "Sitemap | Newman Air", "description": ""})


# -------------------------------------------------------------------- main ----
def write(doc, S, seo, seed, manifest, parent=None):
    page = B.E.wrap_page(doc["title"], S, {"template": "elementor_header_footer", "hide_title": "yes"})
    path = os.path.join(OUT, doc["key"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(page, f, ensure_ascii=False, indent=1)
    parts = doc["path"].split("/")
    manifest.append({"key": doc["key"], "json": os.path.relpath(path, SITE).replace("\\", "/"),
                     "slug": parts[-1], "parent": parts[0] if len(parts) == 2 else "",
                     "title": doc["title"], "seo_title": seo.get("title", ""), "seo_description": seo.get("description", ""),
                     "robots": seo.get("robots", "")})


def main():
    os.makedirs(OUT, exist_ok=True)
    B.reset(0x52000000)
    manifest, seed = [], 0x52000000
    keys = [f[:-5] for f in sorted(os.listdir(CONTENT)) if f.endswith(".json")]
    # Hubs first so their children find a parent on import.
    keys.sort(key=lambda k: (k not in ("services", "service-area"), k))
    for k in keys:
        doc = json.load(open(os.path.join(CONTENT, k + ".json"), encoding="utf-8"))
        seed += 0x10000
        B.E.reset_ids(seed)
        if doc["type"] == "legal":
            S = legal(doc)
        elif doc["type"] == "about":
            S = about(doc)
        else:
            S = standard(doc)
        write(doc, S, doc["seo"], seed, manifest)
    for fn in (financing, maintenance_plan, contact, a2p, sitemap, blog_page, lambda: thanks("thank-you"), lambda: thanks("confirmed")):
        seed += 0x10000
        B.E.reset_ids(seed)
        doc, S, seo = fn(manifest) if fn is sitemap else fn()
        write(doc, S, seo, seed, manifest)
    with open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    B.write_manifest(os.path.join(HERE, "widget-classes.json"))
    print("wrote %d pages to %s" % (len(manifest), OUT))


if __name__ == "__main__":
    main()
