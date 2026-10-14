#!/usr/bin/env python3
"""
Lenz: service page template (AC Repair, Heating Maintenance, Humidity Control, ...).

Approved design: design-source/v6-1/ac-repair.html + css/lenz-service.css (Erick,
2026-10-13). The page docs do not share one structure, so the template is a set
of BLOCKS in the same visual system, and each page maps its doc sections to them:

  checklist   copy + white card with a check list    ("... can help you:" + bullets)
  cards       grid of cards, one per item heading    (problems, signs, when-it-makes-sense)
  boldcards   grid of cards from "<b>Label</b> text" paragraphs
  pair        two check-list cards side by side      (furnace vs heat pump tune-up)
  bullets     one wide card, check list in two columns
  values      photo + numbered list                  ("Why timely X matters")
  table       comparison table
  prose       heading + paragraphs
  promo       navy box with copy and one button      (Breathe Easy package)
  plans       the home's RED / WHITE / BLUE plans    (maintenance pages)
  why         three (or four) cards                  ("Why homeowners choose Lenz")
  reviews     the home's reviews block
  faq         the home's FAQ disclosure

Every page also gets: hero, trustbar, the emergency band after the first
cards-like block, related services, and the closing form.

Copy comes from the page's source.docx through tools/docx_outline.py, verbatim,
except the ClickUp overrides in FIXES (applied to every page and listed in its
HANDOFF). A page's build.py gives the block plan, eyebrows and photos.

Category tint: PAGE["cat"] is cool | warm | air | extra (`svc-page--<cat>`).
"""
import json
import os
import re
import sys

import brand as B
from brand import L, svg, eyebrow

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
import docx_outline  # noqa: E402

# ---------------------------------------------------------------- ClickUp ----
# (doc text, replacement, why). Applied to every string taken from a doc.
FIXES = [
    (", no trip or diagnostic fees.", ".",
     "ClickUp 09/10 item 6: only estimates are free; repairs carry a diagnostic fee"),
    ("no trip or diagnostic fees", "upfront pricing before any work begins",
     "ClickUp 09/10 item 6: only estimates are free; repairs carry a diagnostic fee"),
    ("plus priority emergency service, no trip fees, and discounts on any repairs you need during the year.",
     "plus priority emergency service and discounts on repair parts during the year.",
     "ClickUp 09/10 item 7: the plan discount applies to parts only; no trip-fee promise in the plans"),
]
# Section-level replacements: a whole "why" card the client ruled out.
CARD_FIXES = {
    "Free Second Opinions": (
        "Free Estimates",
        "New equipment and full system replacements are quoted free, with no obligation and no pressure. "
        "Repairs carry our standard diagnostic fee, with upfront pricing before any work begins.",
        "ClickUp 09/10 item 6: remove free second opinions, keep free estimates (home's approved wording)"),
}

DEFAULT_TRUST = [("Since 2009", "Serving Central Iowa"), ("24/7/365", "Emergency service"),
                 ("#50871-CL", "Iowa Master Licensed"), ("Veteran &amp; Woman-Owned", "Family operated"),
                 ("Upfront Pricing", "Before any work begins")]

CAT = {
    "cool": {"icon": "i-snow", "label": "Air conditioning", "hub": ("Air Conditioning", "air-conditioning"),
             "card": "cooling", "band": "AC not cooling? We&apos;re ready right now.",
             "band_sub": "24/7 emergency AC service across the Des Moines metro since 2009."},
    "warm": {"icon": "i-flame", "label": "Heating", "hub": ("Heating", "heating"), "card": "heating",
             "band": "No heat? We&apos;re ready right now.",
             "band_sub": "24/7 emergency heating service across the Des Moines metro since 2009."},
    "air": {"icon": "i-air", "label": "Indoor air quality", "hub": ("Indoor Air Quality", "indoor-air-quality"),
            "card": "both", "band": "Questions about your air? We&apos;re here 24/7.",
            "band_sub": "Local team, real people, across the Des Moines metro since 2009."},
    "extra": {"icon": "i-wrench", "label": "Additional services",
              "hub": ("Additional Services", "additional-services"), "card": "both",
              "band": "Need help now? We&apos;re ready right now.",
              "band_sub": "24/7 emergency service across the Des Moines metro since 2009."},
}

# Icon by keywords in a card title, first match wins; a page can override.
ICON_RULES = [
    (r"warm air|heat|furnace|flame|winter|cold|no-heat", "i-flame"),
    (r"freez|ice|frozen|cool|summer|ac ", "i-snow"),
    (r"air ?flow|wind|duct|vent", "i-wind"),
    (r"water|leak|humid|damp|mold|moist|musty|drain|coil", "i-droplet"),
    (r"cycl|time|year|old|age|longer|midnight", "i-clock"),
    (r"noise|smell|safe|warranty|protect|family", "i-shield"),
    (r"turn(ing)? on|electric|power|start", "i-info"),
    (r"bill|cost|price|budget|energy|save|penny", "i-card"),
    (r"pet|allerg|asthma|dust|pollen|dander|purif|filter|air quality|breath", "i-air"),
    (r"build|install|new |add|basement|room|space|equipment|ready", "i-wrench"),
    (r"maint|tune|plan|schedul", "i-calendar"),
]
FALLBACK_ICONS = ["i-check", "i-shield", "i-clock", "i-info", "i-wrench", "i-award"]


def icon_for(title, i):
    t = " " + re.sub(r"<[^>]+>", "", title).lower() + " "
    for pat, ic in ICON_RULES:
        if re.search(pat, t):
            return ic
    return FALLBACK_ICONS[i % len(FALLBACK_ICONS)]


# ------------------------------------------------------------------- copy ----
class Copy:
    """Doc text with the ClickUp fixes applied; remembers which fixes fired."""

    def __init__(self):
        self.applied = []

    def __call__(self, s):
        for old, new, why in FIXES:
            if old in s:
                s = s.replace(old, new)
                self.applied.append((old, new, why))
        return s


def _items(nodes, fix):
    """[(title, [paras], [lis])] for each `h` node, plus the nodes before the first."""
    head, items, cur = [], [], None
    for n in nodes:
        if n["t"] == "h":
            cur = [n["text"], [], []]
            items.append(cur)
        elif cur is None:
            head.append(n)
        elif n["t"] == "p":
            cur[1].append(fix(n["text"]))
        elif n["t"] == "li":
            cur[2].append(fix(n["text"]))
    return head, items


def _paras(nodes, fix):
    return [fix(n["text"]) for n in nodes if n["t"] == "p"]


def _lis(nodes, fix):
    return [fix(n["text"]) for n in nodes if n["t"] == "li"]


def _strip_num(t):
    m = re.match(r"\s*(\d+)\.\s*(.+)", t)
    return (m.group(1), m.group(2)) if m else (None, t)


def _bold_split(text):
    """'<b>Label:</b> rest' -> ('Label', 'rest')"""
    m = re.match(r"\s*<b>(.+?)</b>\s*[:\-—–]?\s*(.*)$", text)
    if not m:
        return None
    return m.group(1).strip().rstrip(":"), m.group(2).strip()


def _bold_items(text):
    """Several '<b>Label:</b> text' items run together in one paragraph."""
    parts = re.split(r"(?=<b>)", text)
    out = []
    for p in parts:
        bs = _bold_split(p)
        if bs and bs[1]:
            out.append(bs)
    return out


# ----------------------------------------------------------------- blocks ----
DEFAULT_EB = {"checklist": ("i-wrench", "Why act now"), "cards": ("i-info", "What to look for"),
              "boldcards": ("i-shield", "Why it matters"), "pair": ("i-check", "What&apos;s included"),
              "bullets": ("i-info", "Know the signs"), "values": ("i-shield", "Why it matters"),
              "table": ("i-info", "Compare your options"), "prose": ("i-info", "Good to know"),
              "plans": ("i-award", "Service agreements"), "why": ("i-award", "Why Lenz"),
              "services": ("i-wrench", "Our services"), "promo": ("i-card", "")}


def _head(page, eb, title, lead=None, center=False):
    icon, label = eb
    return B.head(icon, label, title, lead, extra="section__head--center" if center else "")


def block_checklist(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = _lis(sec["nodes"], fix)
    title_i = next((i for i, p in enumerate(paras) if re.sub(r"<[^>]+>", "", p).rstrip().endswith(":")), None)
    ck_title = re.sub(r"</?b>", "", paras[title_i]) if title_i is not None else opt.get("checklist_title", "")
    rest = [p for i, p in enumerate(paras) if i != title_i]
    lead, body = (rest[0], rest[1:]) if rest else ("", [])
    body = page["_hero_extra"] + body
    page["_hero_extra"] = []          # the hero's extra paragraphs go to the first checklist only
    btn = next((n["labels"][0] for n in sec["nodes"] if n["t"] == "button"), page["cta"])
    copy = [eyebrow(*opt["eyebrow"]),
            B.heading(fix(sec["title"]), "h2", "section__title", size="var(--text-2xl)")]
    if lead:
        copy.append(B.text(lead, "section__lead"))
    if body:
        copy.append(B.text("".join("<p>%s</p>" % p for p in body), "svc-intro__body"))
    return B.section("section %s svc-intro %s" % (opt.get("bg", "section--mist"), page["_cat"]), [
        B.box("svc-intro__layout", [
            B.box("svc-intro__copy", copy),
            B.box("checklist-card", [
                B.text(ck_title, "checklist-card__title"),
                B.raw('<ul class="checklist">%s</ul>' % "".join(
                    "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis)),
                B.button(btn, L["form"], "btn btn-primary"),
            ], tag="aside"),
        ]),
    ])


def _card(icon, num, title, paras, lis=None):
    chip = ('<span class="symptom__icon symptom__icon--num">%s</span>' % num if num
            else '<span class="symptom__icon">%s</span>' % svg(icon, "icon"))
    body = "".join("<p>%s</p>" % p for p in paras)
    if lis:
        body += '<ul class="checklist checklist--tight">%s</ul>' % "".join(
            "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis)
    return B.box("symptom", [B.raw(chip), B.heading(title, "h3"), B.text(body)], tag="article")


def block_cards(page, sec, opt, fix):
    head, items = _items(sec["nodes"], fix)
    hp = _paras(head, fix)
    cards = []
    for i, (t, ps, lis) in enumerate(items):
        num, t = _strip_num(fix(t))
        icon = (opt.get("icons") or [None] * 99)[i] or icon_for(t, i)
        cards.append(_card(icon, num if opt.get("numbered", num is not None) else None, t, ps, lis))
    help_ = opt.get("help", ("Not sure what&apos;s wrong?",
                             "Tell us what you&apos;re hearing or feeling and we&apos;ll work it out."))
    if help_:
        full = " symptom-help--full" if len(cards) % opt.get("cols", 3) == 0 else ""
        cards.append(B.box("service-help symptom-help" + full, [
            B.box("service-help__txt", [B.heading(help_[0], "h4"), B.text("<p>%s</p>" % help_[1])]),
            B.raw('<a class="phone-link" href="%s">%s %s</a>' % (B.PHONE_TEL, B.PHONE, svg("i-arrow", "icon-sm"))),
        ]))
    cols = opt.get("cols", 3)
    return B.section("section symptoms " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("symptom-grid symptom-grid--%d" % cols, cards),
    ], el_id=opt.get("id"))


def block_boldcards(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lead = [p for p in paras if not _bold_split(p)]
    items = [_bold_split(p) for p in paras if _bold_split(p)]
    cards = [_card((opt.get("icons") or [None] * 99)[i] or icon_for(t, i), None, t, [d])
             for i, (t, d) in enumerate(items)]
    cols = opt.get("cols", 4 if len(items) == 4 else 3)
    return B.section("section symptoms " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(lead) if lead else None),
        B.box("symptom-grid symptom-grid--%d" % cols, cards),
    ])


def _checklist_card(title, lis, sub=None):
    kids = [B.heading(title, "h3", "checklist-card__heading")]
    if sub:
        kids.append(B.text("<p>%s</p>" % sub, "checklist-card__sub"))
    kids.append(B.raw('<ul class="checklist">%s</ul>' % "".join(
        "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis)))
    return B.box("checklist-card", kids)


def block_pair(page, sec, opt, fix):
    head, items = _items(sec["nodes"], fix)
    hp = _paras(head, fix)
    cards = [_checklist_card(fix(t), lis, " ".join(ps) if ps else None) for t, ps, lis in items]
    return B.section("section section--mist pair " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("checklist-pair", cards),
    ])


def block_bullets(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = _lis(sec["nodes"], fix)
    return B.section("section bullets " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(paras) if paras else None),
        B.box("bullets-card", [B.raw('<ul class="checklist checklist--2col">%s</ul>' % "".join(
            "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis))]),
    ])


def block_values(page, sec, opt, fix):
    head, items = _items(sec["nodes"], fix)
    hp = _paras(head, fix)
    v_key, v_alt = opt.get("image", ("lenz-comfort-webp", "A family relaxing in a comfortable Des Moines home"))
    return B.section("valueprops section " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("valueprops__layout", [
            B.box("valueprops__media", [B.image(v_key, v_alt)], tag="figure"),
            B.box("valueprops__grid", [
                B.box("vprop", [
                    B.text("%02d" % n, "vprop__num"),
                    B.box("vprop__text", [B.heading(fix(t), "h3"), B.text("".join("<p>%s</p>" % p for p in ps))]),
                ]) for n, (t, ps, _l) in enumerate(items, 1)
            ]),
        ]),
    ])


def block_table(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    tbl = next(n for n in sec["nodes"] if n["t"] == "table")
    head, rows = tbl["rows"][0], tbl["rows"][1:]
    html = '<div class="compare"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        "".join("<th scope=\"col\">%s</th>" % fix(c) for c in head),
        "".join("<tr>%s</tr>" % "".join(
            ('<th scope="row">%s</th>' % fix(c)) if i == 0 else ('<td data-label="%s">%s</td>' % (
                re.sub(r"<[^>]+>|\"", "", head[i]), fix(c))) for i, c in enumerate(r)) for r in rows))
    return B.section("section compare-section " + opt.get("bg", "section--mist") + " " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(paras) if paras else None),
        B.text(html, "compare-wrap"),
    ])


def block_prose(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = _lis(sec["nodes"], fix)
    kids = [eyebrow(*opt["eyebrow"]),
            B.heading(fix(sec["title"]), "h2", "section__title", size="var(--text-2xl)"),
            B.text("".join("<p>%s</p>" % p for p in paras), "prose__body")]
    if lis:
        kids.append(B.raw('<ul class="checklist checklist--2col">%s</ul>' % "".join(
            "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis)))
    return B.section("section prose " + opt.get("bg", "") + " " + page["_cat"], [B.box("prose__inner", kids)])


def block_promo(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = _lis(sec["nodes"], fix)
    btn = next((n["labels"][0] for n in sec["nodes"] if n["t"] == "button"), page["cta"])
    btn = re.sub(r"\s*→\s*$", "", btn)
    body = "".join("<p>%s</p>" % p for p in paras)
    if lis:
        body += '<ul class="checklist checklist--on-dark">%s</ul>' % "".join(
            "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in lis)
    return B.section("section promo-section " + page["_cat"], [
        B.box("service-help promo", [
            B.box("service-help__txt promo__txt", [B.heading(fix(sec["title"]), "h2", "promo__title",
                                                             size="var(--text-xl)"), B.text(body)]),
            B.button(btn, L[opt.get("link", "form")], "btn btn-gold"),
        ]),
    ])


def block_plans(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    return B.plans_section(fix(sec["title"]), " ".join(paras), extra=page["_cat"],
                           eb=opt.get("eyebrow", ("i-award", "Service agreements")))


def block_why(page, sec, opt, fix):
    head, items = _items(sec["nodes"], fix)
    hp = _paras(head, fix)
    cards = []
    for i, (t, ps, _l) in enumerate(items):
        t = re.sub(r"<[^>]+>", "", t).strip()
        if t in CARD_FIXES:
            nt, body, why = CARD_FIXES[t]
            fix.applied.append((t, nt, why))
            t, ps = nt, [body]
        icon = (opt.get("icons") or [None] * 99)[i] or ["i-card", "i-shield", "i-clock", "i-award"][i % 4]
        cards.append(B.box("creds__card", [
            B.raw('<span class="creds__icon">%s</span>' % svg(icon, "icon")),
            B.heading(fix(t), "h3"),
            B.text(" ".join(ps), "creds__text"),
        ], tag="article"))
    grid = "creds__grid" + (" creds__grid--4" if len(cards) == 4 else "")
    return B.section("creds section " + page["_cat"], [
        _head(page, opt.get("eyebrow", ("i-award", "Why Lenz")), fix(sec["title"]), " ".join(hp) if hp else None),
        B.box(grid, cards),
    ])


def block_reviews(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    return B.section("reviews section " + page["_cat"], [
        B.head("i-star", "Reviews", fix(sec["title"]), paras[0] if paras else None),
        B.reviews_grid(),
        B.raw('<p class="reviews__micro"><a href="%s">Ready for service like this? %s %s</a></p>'
              % (L["form"], page["cta"], svg("i-arrow", "icon-sm"))),
    ], el_id="reviews")


def block_faq(page, sec, opt, fix):
    _h, items = _items(sec["nodes"], fix)

    def answer(ps, lis):
        if not lis:
            return " ".join(ps)
        return "<p>%s</p><ul>%s</ul>" % (ps[0], "".join("<li>%s</li>" % li for li in lis)) + \
            "".join("<p>%s</p>" % p for p in ps[1:])
    return B.section("faqs section " + page["_cat"], [
        B.head("i-info", "FAQs", fix(sec["title"]), extra="section__head--center"),
        B.faq_list([(fix(q), answer(ps, lis)) for q, ps, lis in items]),
    ], el_id="faqs")


def block_services(page, sec, opt, fix):
    """Hub list: one card per child service, its summary, an optional check list
    and an "Explore ... ->" link to the child page."""
    head, items, cur = [], [], None
    for n in sec["nodes"]:
        if n["t"] == "h":
            cur = {"title": fix(n["text"]), "ps": [], "lis": [], "list_title": None, "btn": None}
            items.append(cur)
        elif cur is None:
            head.append(n)
        elif n["t"] == "button":
            cur["btn"] = re.sub(r"\s*→\s*$", "", n["labels"][0])
        elif n["t"] == "li":
            cur["lis"].append(fix(n["text"]))
        elif n["t"] == "p":
            if not cur["lis"] and re.sub(r"<[^>]+>", "", n["text"]).rstrip().endswith(":"):
                cur["list_title"] = fix(n["text"])
            else:
                cur["ps"].append(fix(n["text"]))
    rows = opt.get("layout") == "rows"
    cards = []
    for i, it in enumerate(items):
        num, title = _strip_num(it["title"])
        key = opt["links"][i]
        href = B.PHONE_TEL if key == "tel" else L[key]
        label = it["btn"] or ("Call " + B.PHONE if key == "tel" else "Explore " + title)
        icon = (opt.get("icons") or [None] * 99)[i] or icon_for(title, i)
        main = [B.raw('<span class="symptom__icon">%s</span>' % svg(icon, "icon")),
                B.heading(title, "h3"),
                B.text("".join("<p>%s</p>" % p for p in it["ps"]), "hub-svc__body"),
                B.arrow_link("svc-band__go hub-svc__go", label, href)]
        lst = ('<ul class="checklist">%s</ul>' % "".join(
            "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in it["lis"])) if it["lis"] else ""
        if rows and lst:
            aside = [B.text(it["list_title"] or "", "hub-svc__list-title"), B.raw(lst)]
            cards.append(B.box("hub-svc hub-svc--row", [B.box("hub-svc__main", main),
                                                        B.box("hub-svc__aside", aside)], tag="article"))
        else:
            if lst:
                main.insert(3, B.raw(lst))
            cards.append(B.box("hub-svc", main, tag="article"))
    hp = _paras(head, fix)
    return B.section("section section--mist hub-services " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("hub-list " + ("hub-list--rows" if rows else "hub-list--grid"), cards),
    ], el_id="services")


BLOCKS = {"checklist": block_checklist, "cards": block_cards, "boldcards": block_boldcards,
          "pair": block_pair, "bullets": block_bullets, "values": block_values, "table": block_table,
          "prose": block_prose, "promo": block_promo, "plans": block_plans, "why": block_why,
          "reviews": block_reviews, "faq": block_faq, "services": block_services}
BAND_AFTER = ("cards", "boldcards", "services")


# ------------------------------------------------------------- page build ----
def _crumbs(page):
    if page.get("is_hub"):
        return B.raw('<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
                     '<li aria-current="page">%s</li></ol></nav>' % page["title"])
    hub_label, hub_key = page["hub"]
    return B.raw('<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
                 '<li><a href="%s">%s</a></li><li aria-current="page">%s</li></ol></nav>'
                 % (L[hub_key], hub_label, page["title"]))


def _hero(page, doc, fix):
    nodes = list(doc["hero"])
    kicker = None
    if page.get("kicker_from_section0"):
        s0 = doc["sections"].pop(0)
        kicker = fix(s0["title"])
        nodes += s0["nodes"]
    paras = [fix(n["text"]) for n in nodes if n["t"] == "p"]
    areas = next((p for p in paras if re.sub(r"<[^>]+>", "", p).startswith("Serving ")), None)
    paras = [p for p in paras if p is not areas]
    # trust items written as "<b>Label:</b> text" (list items or one run-on paragraph)
    trust = [_bold_split(n["text"]) for n in nodes if n["t"] == "li" and _bold_split(n["text"])]
    if not trust:
        for p in list(paras):
            items = _bold_items(p)
            if len(items) >= 3:
                trust = items
                paras.remove(p)
    if page.get("is_hub"):
        paras = ["".join("<p>%s</p>" % p for p in paras)] if paras else []
    lead, extra = (paras[0], paras[1:]) if paras else ("", [])
    page["_hero_extra"] = extra
    page["_trust"] = [(fix(a), fix(b)) for a, b in trust] if trust else None
    h1 = fix(doc["h1"])
    acc = page.get("accent")
    if acc and acc in h1:
        h1 = h1.replace(acc, '<span class="accent">%s</span>' % acc, 1)
    img_key, img_alt = page["hero_image"]
    copy = [_crumbs(page),
            B.raw('<span class="hero__eyebrow">%s %s</span>' % (svg(page["cat_icon"], "icon-xs"), page["cat_label"])),
            B.heading(h1, "h1", size="var(--text-hero)")]
    if kicker:
        copy.append(B.text(kicker, "hero__kicker"))
    copy.append(B.text(lead, "hero__sub"))
    if areas:
        copy.append(B.raw('<p class="hero__areas">%s%s</p>' % (svg("i-pin", "icon-sm"),
                                                               re.sub(r"</?b>", "", areas))))
    copy.append(B.box("hero__cta", [
        B.button(page["cta"], L["form"], "btn btn-gold"),
        B.button("Call " + B.PHONE, B.PHONE_TEL, "btn btn-outline-light", icon="phone"),
    ]))
    badge_t, badge_s = page["badge"]
    return B.section("hero hero--service " + page["_cat"], [
        B.box("hero__copy", copy),
        B.box("hero__media", [
            B.image(img_key, img_alt),
            B.raw('<div class="hero__badge"><span class="hero__badge-icon">%s</span><span><b>%s</b>%s</span></div>'
                  % (svg("i-clock", "icon"), badge_t, badge_s)),
        ]),
    ], box_classes="container hero__inner")


# Card blurbs, the same lines the home's service bands use.
BLURBS = {
    "ac-installation": "Right-sized systems, installed properly.", "ac-repair": "Fast diagnosis, day or night.",
    "ac-maintenance": "Seasonal tune-ups that prevent breakdowns.",
    "ac-replacement": "Efficient upgrades sized to your home.",
    "heating-installation": "High-efficiency gas and electric furnaces.",
    "heating-repair": "No heat? We diagnose it fast.",
    "heating-maintenance": "Safety inspections before the first freeze.",
    "heating-replacement": "Upgrade an aging or failing furnace.",
    "humidity-control": "Whole-home humidifiers and dehumidifiers.",
    "uv-light-purification": "Treat air as it moves through the system.",
    "indoor-purification": "Filtration for dust, dander and allergens.",
    "duct-cleaning": "Clear out built-up dust and debris.",
    "thermostat-services": "Smart thermostat install and setup.",
    "water-heater-services": "Tank and tankless, professionally installed.",
    "ductwork": "Repairs, modifications and airflow balancing.",
    "gas-lines": "Safe runs for appliances and outdoor setups.",
    "heat-pumps": "Heating and cooling from one efficient system.",
}


def _related(page):
    title, hub, kids = next(s for s in B.SERVICES if s[1] == page["hub"][1])
    cards = [(CAT[page["cat"]]["card"], icon_for(n, i), n, BLURBS.get(k, ""), k)
             for i, (n, k) in enumerate(kids) if L[k] != "/%s/" % page["slug"]]
    cards = cards[:3] + [("both", "i-award", "Maintenance Plans", "Priority dispatch and 10 to 20% off parts.",
                          "maintenance-plans")]
    return B.section("section section--mist related " + page["_cat"], [
        B.box("svc-band svc-band--" + page["cat"], [
            B.box("svc-band__head", [
                B.raw('<span class="svc-band__icon">%s</span>' % svg(page["cat_icon"])),
                B.box("svc-band__txt", [B.heading("More %s Services" % title, "h3"),
                                        B.text("<p>%s</p>" % page["related_text"])]),
                B.arrow_link("svc-band__go", "All %s Services" % title, L[hub]),
            ]),
            B.box("svc-band__grid", [B.service_card(*c) for c in cards]),
        ], tag="section"),
    ])


def build(page):
    """Return (sections, meta, fixes_applied) for one service page."""
    doc = docx_outline.read(page["source"])
    fix = Copy()
    c = CAT[page["cat"]]
    page.setdefault("cat_icon", c["icon"])
    page.setdefault("cat_label", c["label"])
    page.setdefault("hub", c["hub"])
    page["_cat"] = "svc-page svc-page--" + page["cat"]
    S = [_hero(page, doc, fix)]
    trust = page.get("trust") or page["_trust"]
    long_ = " trustbar--long trustbar--%d" % len(trust) if trust else ""
    S.append(B.trustbar(trust or DEFAULT_TRUST, extra=page["_cat"] + long_))
    banded = False
    for spec, sec in zip(page["plan"], doc["sections"]):
        kind = spec[0]
        opt = spec[1] if len(spec) > 1 else {}
        if kind == "skip":
            continue
        if kind == "close":
            paras = _paras(sec["nodes"], fix)
            if not page.get("is_hub"):
                S.append(_related(page))
            S.append(B.close_form(fix(sec["title"]), "".join("<p>%s</p>" % p for p in paras),
                                  button_text=page["cta"], preselect=page.get("form_preselect"),
                                  extra=page["_cat"]))
            continue
        opt = dict(opt)
        opt.setdefault("eyebrow", DEFAULT_EB.get(kind, ("i-info", "")))
        S.append(BLOCKS[kind](page, sec, opt, fix))
        if kind in BAND_AFTER and not banded:
            S.append(B.cta_band(page.get("band", c["band"]), page.get("band_sub", c["band_sub"]),
                                extra=page["_cat"]))
            banded = True
    if len(page["plan"]) != len(doc["sections"]):
        raise SystemExit("plan has %d entries, doc has %d sections: %s" % (
            len(page["plan"]), len(doc["sections"]), [s["title"] for s in doc["sections"]]))
    meta = {k: fix(v) for k, v in doc["meta"].items()}
    return S, meta, fix.applied


def write(page, here):
    """Build, write <slug>.json, the class manifest and the SEO/fixes block of HANDOFF-notes.md."""
    S, meta, applied = build(page)
    doc = B.E.wrap_page(page["title"], S, {"template": "elementor_header_footer", "hide_title": "yes"})
    out = os.path.join(here, page["slug"] + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    B.write_manifest(os.path.join(here, "widget-classes.json"))
    slug = "/" + page["slug"] + "/"
    title = re.sub(r"&amp;", "&", meta.get("title", ""))
    if title and "Lenz" not in title:
        title += " | Lenz Heating & Cooling"
    desc = re.sub(r"&amp;", "&", meta.get("description", ""))
    fixes = sorted({(o, n, w) for o, n, w in applied})
    lines = ["# Lenz: %s handoff" % page["title"], "",
             "Generated by `build.py` from `source.docx` on the service template "
             "(`../../service_page.py`). Rebuild instead of editing this file.", "",
             "## SEO", "",
             "- **Meta title:** `%s`" % title,
             "- **Meta description:** `%s`" % desc,
             "- Slug: `%s` · Canonical: https://www.lenzheatingandcooling.com%s" % (slug, slug), "",
             "## Copy changes against the doc (ClickUp decisions)", ""]
    lines += ["- \"%s\" → \"%s\" (%s)" % (re.sub(r"&amp;", "&", o), re.sub(r"&amp;", "&", n), w)
              for o, n, w in fixes] or ["- none"]
    lines += ["", "## Notes", ""] + ["- " + n for n in page.get("notes", [])] + [""]
    with open(os.path.join(here, "HANDOFF-notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote %s (%d sections, %d copy fixes)" % (out, len(S), len(fixes)))
