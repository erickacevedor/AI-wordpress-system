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
    ("discounts on any repairs you need during the year.", "discounts on repair parts during the year.",
     "ClickUp 09/10 item 7: the service agreement discount applies to parts only"),
    ("Save on parts and repairs all year long", "Save on parts all year long",
     "ClickUp 09/10 item 7: the service agreement discount applies to parts only"),
    ("Parts &amp; Repair Discounts", "Parts Discounts",
     "ClickUp 09/10 item 7: the service agreement discount applies to parts only"),
    ("We provide free estimates on every request because",
     "We provide free estimates on new equipment and full system replacements because",
     "ClickUp 09/10 item 6: only estimates on new equipment and replacements are free"),
    ("Over 1,800+ 5-star reviews", "Over 2,000 5-star reviews",
     "ClickUp 08/17: the client asked for 2,000, not 1,800"),
]
# (regex, replacement, why): case-aware word swaps.
REGEX_FIXES = [
    (r"\bHeadquarters\b", "Main Office", "ClickUp 08/17: \"Main office\", not \"Headquarters\""),
    (r"\bheadquarters\b", "main office", "ClickUp 08/17: \"Main office\", not \"Headquarters\""),
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
            "card": "air", "band": "Questions about your air? We&apos;re here 24/7.",
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
        for pat, new, why in REGEX_FIXES:
            if re.search(pat, s):
                s = re.sub(pat, new, s)
                self.applied.append((pat.strip("\\b"), new, why))
        return s.replace("main main office", "main office").replace("Main Main Office", "Main Office")


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
              "services": ("i-wrench", "Our services"), "promo": ("i-card", ""),
              "people": ("i-award", "Our people"), "roster": ("i-award", "Our team"),
              "steps": ("i-check", "How it works"), "video": ("i-tv", "As seen on TV"),
              "locations": ("i-pin", "Our locations"), "area": ("i-pin", "Service area"),
              "embed": ("i-check", "Apply online"), "coupons": ("i-card", "Current specials")}


def _head(page, eb, title, lead=None, center=False):
    icon, label = eb
    return B.head(icon, label, title, lead, extra="section__head--center" if center else "")


def block_checklist(page, sec, opt, fix):
    paras = [p for p in _paras(sec["nodes"], fix)
             if not any(re.search(d, re.sub(r"<[^>]+>", "", p)) for d in opt.get("drop", []))]
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
                (B.button("Call " + B.PHONE, B.PHONE_TEL, "btn btn-primary", icon="phone") if opt.get("tel")
                 else B.button(btn, L["form"], "btn btn-primary")),
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
        cols = opt.get("cols", 3)
        rem = len(cards) % cols                 # the tile fills what the last row leaves free
        full = " symptom-help--full" if rem == 0 else (" symptom-help--one" if cols - rem == 1 else "")
        if len(cards) % 2 == 0:                 # two-column band (600 to 903px): a row of its own
            full += " symptom-help--wide2"
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
    paras = _paras(sec["nodes"], fix) + _lis(sec["nodes"], fix)
    lead = [p for p in paras if not _bold_split(p)]
    items = [_bold_split(p) for p in paras if _bold_split(p)]
    cards = [_card((opt.get("icons") or [None] * 99)[i] or icon_for(t, i), None, t, [d])
             for i, (t, d) in enumerate(items)]
    cols = opt.get("cols", 4 if len(items) == 4 else 3)
    kids = [_head(page, opt["eyebrow"], fix(sec["title"]), " ".join(lead) if lead else None),
            B.box("symptom-grid symptom-grid--%d" % cols, cards)]
    btns = _doc_buttons(sec["nodes"], opt)
    if btns:
        kids.append(B.box("section-cta", btns))
    return B.section("section symptoms %s %s" % (opt.get("bg", ""), page["_cat"]), kids, el_id=opt.get("id"))


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


ARROW_LINKS = {"Furnace": "heating", "AC Installation": "ac-installation", "AC Replacement": "ac-replacement",
               "Heat Pumps": "heat-pumps", "Water Heater Installation": "water-heater-services",
               "Indoor Air Quality": "indoor-air-quality"}


def _arrow(li):
    """'<b>Label</b> → Page · Page' (doc link notes) -> label plus real links."""
    if "→" not in li:
        return li
    label, _, targets = li.partition("→")
    links = []
    for t in targets.split("·"):
        t = re.sub(r"<[^>]+>", "", t).strip()
        u = B.href(ARROW_LINKS[t]) if t in ARROW_LINKS else None
        links.append('<a href="%s">%s</a>' % (u, t) if u else t)
    return '%s <span class="checklist__links">%s</span>' % (label.strip(), " · ".join(links))


def block_bullets(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = [_arrow(li) for li in _lis(sec["nodes"], fix)]
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
            ('<th scope="row">%s</th>' % B.nw(fix(c))) if i == 0 else ('<td data-label="%s">%s</td>' % (
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
    btns = _doc_buttons(sec["nodes"], opt)
    if btns:
        kids.append(B.box("section-cta", btns))
    inner = [B.box("prose__inner", kids)]
    if opt.get("partners"):            # name + one line from the doc's own copy, as the doc note asks
        cols = 2 if len(opt["partners"]) in (2, 4) else 3
        inner.append(B.box("symptom-grid symptom-grid--%d partners" % cols, [
            _card(ic, None, n, [d]) for ic, n, d in opt["partners"]]))
    return B.section("section prose " + opt.get("bg", "") + " " + page["_cat"], inner,
                     el_id=opt.get("id"))


def block_promo(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    lis = _lis(sec["nodes"], fix)
    bnode = next((n for n in sec["nodes"] if n["t"] == "button"), None)
    btn = re.sub(r"\s*→\s*$", "", bnode["labels"][0]) if bnode else opt.get("button", page["cta"])
    href = _btn_href(btn, bnode.get("hint", "") if bnode else "", opt.get("links", {}))
    if "link" in opt:
        href = B.PHONE_TEL if opt["link"] == "tel" else (B.href(opt["link"]) or L["form"])
    body, run = "", []                 # doc order: list items grouped into one <ul> where they sit
    for n in sec["nodes"] + [{"t": "end"}]:
        if n["t"] == "li":
            run.append(fix(n["text"]))
            continue
        if run:
            body += '<ul class="checklist checklist--on-dark">%s</ul>' % "".join(
                "<li>%s<span>%s</span></li>" % (svg("i-check", "icon-sm"), li) for li in run)
            run = []
        if n["t"] == "p":
            body += "<p>%s</p>" % fix(n["text"])
    return B.section("section promo-section " + page["_cat"], [
        B.box("service-help promo", [
            B.box("service-help__txt promo__txt", [B.heading(fix(sec["title"]), "h2", "promo__title",
                                                             size="var(--text-xl)"), B.text(body)]),
            B.button(btn, href, "btn btn-gold", icon="phone" if href.startswith("tel:") else None,
                     external=href.startswith("http")),
        ]),
    ], el_id=opt.get("id"))


def block_plans(page, sec, opt, fix):
    paras = _paras(sec["nodes"], fix)
    out = B.plans_section(fix(sec["title"]), " ".join(paras), extra=page["_cat"],
                          eb=opt.get("eyebrow", ("i-award", "Service agreements")))
    links = dict({"View Service Agreement Plans": "maintenance-plans", "Compare Maintenance Plans": "maintenance-plans"},
                 **opt.get("links", {}))
    btns = _doc_buttons(sec["nodes"], dict(opt, links=links))
    if btns:
        out["elements"][0]["elements"].append(B.box("section-cta section-cta--center", btns))
    return out


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
        body = " ".join(ps)
        if _l:
            body += '<ul class="creds__list">%s</ul>' % "".join("<li>%s</li>" % li for li in _l)
        cards.append(B.box("creds__card", [
            B.raw('<span class="creds__icon">%s</span>' % svg(icon, "icon")),
            B.heading(fix(t), "h3"),
            B.text(body, "creds__text"),
        ], tag="article"))
    grid = "creds__grid" + (" creds__grid--4" if len(cards) == 4 else "")
    return B.section("creds section " + page["_cat"], [
        _head(page, opt.get("eyebrow", ("i-award", "Why Lenz")), fix(sec["title"]), " ".join(hp) if hp else None),
        B.box(grid, cards),
    ] + ([B.box("section-cta", _doc_buttons(sec["nodes"], opt))] if _doc_buttons(sec["nodes"], opt) else []))


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
    tail = None
    if opt.get("last_as_cta"):
        tail = items.pop()

    def answer(ps, lis):
        if not lis:
            return " ".join(ps)
        return "<p>%s</p><ul>%s</ul>" % (ps[0], "".join("<li>%s</li>" % li for li in lis)) + \
            "".join("<p>%s</p>" % p for p in ps[1:])
    out = B.section("faqs section " + page["_cat"], [
        B.head("i-info", "FAQs", fix(sec["title"]), extra="section__head--center"),
        B.faq_list([(fix(q), answer(ps, lis)) for q, ps, lis in items]),
    ], el_id="faqs")
    if tail:
        t, ps, _l = tail
        return [out, block_cta(page, {"title": t, "nodes": [{"t": "p", "text": p} for p in ps] +
                                       [n for n in sec["nodes"] if n["t"] == "button"]}, opt, fix)]
    return out


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
        title = it["title"]
        key = opt["links"][i]
        href = B.PHONE_TEL if key == "tel" else B.href(key)
        label = it["btn"] or ("Call " + B.PHONE if key == "tel" else "Explore " + title)
        icon = (opt.get("icons") or [None] * 99)[i] or icon_for(title, i)
        main = [B.raw('<span class="symptom__icon">%s</span>' % svg(icon, "icon")),
                B.heading(title, "h3"),
                B.text("".join("<p>%s</p>" % p for p in it["ps"]), "hub-svc__body")]
        if href:                       # no link for pages outside the signed scope
            main.append(B.arrow_link("svc-band__go hub-svc__go", label, href))
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


# ------------------------------------------------------- company blocks ----
def _btn_href(label, hint, links):
    """Where a doc button goes: page override, the doc's own link hint, or a guess."""
    lab = re.sub(r"<[^>]+>|\s*→\s*$", "", label).strip()
    if lab in links:
        v = links[lab]
        return B.PHONE_TEL if v == "tel" else (v if v.startswith(("http", "#", "/")) else (B.href(v) or L["form"]))
    if hint and hint.startswith("/"):
        return hint
    if re.search(r"\(515\)|\bcall\b", lab, re.I):
        return B.PHONE_TEL
    return L["form"]


# Doc "buttons" that are really notes to the web team ("insert form here", "Review Slider").
NOT_A_BUTTON = r"(?i)^insert |widget|slider|placeholder"


def _doc_buttons(nodes, opt, primary="btn btn-primary", secondary="btn btn-outline"):
    out = []
    for n in nodes:
        if n["t"] != "button":
            continue
        for i, lab in enumerate(n["labels"]):
            if re.search(NOT_A_BUTTON, lab):
                continue
            href = _btn_href(lab, n.get("hint", ""), opt.get("links", {}))
            text = re.sub(r"\s*→\s*$", "", lab)
            cls = primary if i == 0 else secondary
            ext = href.startswith("http")
            out.append(B.button(text, href, cls, icon="phone" if href.startswith("tel:") else None, external=ext))
    return out


def _split(sec, fix):
    """Split a section at short bold-only paragraphs (sub-headings in the doc)."""
    parts, cur = [], {"title": sec["title"], "nodes": []}
    for n in sec["nodes"]:
        raw = re.sub(r"<[^>]+>", "", n.get("text", "")).strip()
        if (n["t"] == "p" and re.fullmatch(r"\s*<b>[^<]+</b>\s*", n["text"]) and len(raw) < 60
                and not raw.endswith((".", "!", "?"))):
            parts.append(cur)
            cur = {"title": raw.rstrip(":"), "nodes": []}
        else:
            cur["nodes"].append(n)
    parts.append(cur)
    return [p for p in parts if p["nodes"]]


def block_multi(page, sec, opt, fix):
    out = []
    for spec, sub in zip(opt["parts"], _split(sec, fix)):
        o = dict(spec[1]) if len(spec) > 1 else {}
        o.setdefault("eyebrow", DEFAULT_EB.get(spec[0], ("i-info", "")))
        out.append(BLOCKS[spec[0]](page, sub, o, fix))
    return out


def _initials(name):
    return "".join(w[0] for w in re.sub(r"[^A-Za-z ]", "", name).split()[:2]).upper()


def _person(name, role, bio=None, dog=False, full=False):
    kids = [B.raw('<span class="person__avatar%s" aria-hidden="true">%s</span>'
                  % (" person__avatar--dog" if dog else "", svg("i-heat" if False else "i-star", "icon") if dog else _initials(name))),
            B.heading(name, "h3", "person__name"),
            B.text(role, "person__role")]
    if bio:
        kids.append(B.text("<p>%s</p>" % bio, "person__bio"))
    return B.box("person" + (" person--compact" if not (bio or full) else "")
                 + (" person--nobio" if full and not bio else ""), kids, tag="article")


def block_people(page, sec, opt, fix):
    """Cards from `Name — Role` headings, each with its bio paragraph(s)."""
    head, items = _items(sec["nodes"], fix)
    cards = []
    for t, ps, _l in items:
        name, _, role = re.sub(r"<[^>]+>", "", t).partition(" — ")
        cards.append(_person(name.strip(), role.strip(), " ".join(ps), dog=opt.get("dogs", False), full=True))
    hp = _paras(head, fix)
    return B.section("section people-section %s %s" % (opt.get("bg", ""), page["_cat"]), [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("people people--%d" % opt.get("cols", 3), cards),
    ], el_id=opt.get("id"))


def block_roster(page, sec, opt, fix):
    """Name lists (`Name — Role · Name — Role`, `A, B, C — Role`) as one card per person."""
    intro, groups, cur = [], [], None
    for n in sec["nodes"]:
        if n["t"] != "p":
            continue
        t = fix(n["text"])
        m = re.match(r"\s*<b>([^<]+)</b>\s*(.*)$", t)
        if m and len(m.group(1)) < 50:
            cur = [m.group(1).strip(), []]
            groups.append(cur)
            t = m.group(2)
            if not t:
                continue
        plain = re.sub(r"<[^>]+>", "", t)
        names_only = (opt.get("role") and "," in plain and not plain.rstrip().endswith((".", "!", "?"))
                      and all(len(x.split()) <= 3 for x in plain.split(",")))
        if " — " in plain or (cur is None and names_only):
            if cur is None:
                cur = [None, []]
                groups.append(cur)
            for chunk in plain.split(" · "):
                names, _, role = chunk.partition(" — ")
                role = role.strip() or opt.get("role", "")
                for nm in names.split(","):
                    if nm.strip():
                        cur[1].append((nm.strip(), role))
        else:
            intro.append(t)
    kids = [_head(page, opt["eyebrow"], fix(sec["title"]), " ".join(intro) if intro else None)]
    for title, people in groups:
        if title:
            kids.append(B.heading(title, "h3", "roster__title"))
        roles = opt.get("roles", {})
        kids.append(B.box("people people--roster", [_person(n, roles.get(n, r), dog=opt.get("dogs", False))
                                                     for n, r in people]))
    btns = _doc_buttons(sec["nodes"], opt)
    if btns:
        kids.append(B.box("section-cta", btns))
    return B.section("section roster %s %s" % (opt.get("bg", ""), page["_cat"]), kids, el_id=opt.get("id"))


def block_steps(page, sec, opt, fix):
    """Numbered steps from `<b>1. Title.</b> text` paragraphs, numbered list items,
    one paragraph with 1. 2. 3. inside, or `1. Title` headings."""
    steps, lead = [], []
    head, items = _items(sec["nodes"], fix)
    if items:
        steps = [(_strip_num(t)[1], " ".join(ps)) for t, ps, _l in items]
        lead = _paras(head, fix)
    else:
        for n in sec["nodes"]:
            if n["t"] not in ("p", "li"):
                continue
            t = fix(n["text"])
            plain = re.sub(r"<[^>]+>", "", t)
            found = re.findall(r"(?:^|\s)(\d)\.\s+(.*?)(?=\s\d\.\s|$)", plain)
            if len(found) > 1 and n["t"] == "p":
                for _, chunk in found:
                    ttl, _, rest = chunk.partition(". ")
                    steps.append((ttl.strip().rstrip("."), rest.strip()))
                continue
            m = re.match(r"\s*(?:<b>)?\s*(\d)\.\s*(.+?)(?:</b>)\s*(.*)$", t)
            if m:
                steps.append((re.sub(r"</?b>", "", m.group(2)).strip().rstrip(".:"), m.group(3).strip()))
            elif n["t"] == "li":
                bs = _bold_split(t)
                steps.append(bs if bs else (plain, ""))
            else:
                lead.append(t)
    cards = [B.box("step", [B.raw('<span class="step__num">%d</span>' % i), B.heading(ttl, "h3", "step__title"),
                            B.text("<p>%s</p>" % body if body else "", "step__body")], tag="article")
             for i, (ttl, body) in enumerate(steps, 1)]
    return B.section("section steps-section %s %s" % (opt.get("bg", ""), page["_cat"]), [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(lead) if lead else None,
              center=opt.get("center", True)),
        B.box("steps steps--%d" % len(cards), cards),
    ])


def block_cta(page, sec, opt, fix):
    """Navy closing band with the doc's buttons and no form."""
    paras = _paras(sec["nodes"], fix)
    btns = _doc_buttons(sec["nodes"], opt, primary="btn btn-gold", secondary="btn btn-outline-light")
    return B.section("cta-band cta-band--final section--tight " + page["_cat"], [
        B.raw('<img class="cta-band__bg" src="%s" alt="" aria-hidden="true" decoding="async" loading="lazy" />'
              % B.MEDIA["lenz-service-van-wrap-webp"]["url"]),
        B.box("cta-band__inner", [
            B.heading(fix(sec["title"]), "h2", size="var(--text-2xl)"),
            B.text("".join("<p>%s</p>" % p for p in paras)),
            B.box("hero__cta", btns),
        ]),
    ])


VIDEOS = ["8jsNz6yxry0", "YYaD8i_nDLY", "eStd5NEOYxw", "kO2JzDZUnWc", "pkeMxmt_gZI"]   # lenzmechanical.com/hello-iowa/


def _yt(vid, title):
    return ('<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s" loading="lazy" '
            'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
            % (vid, title))


def block_video(page, sec, opt, fix):
    """Featured WHO 13 segment; with `library`, the other segments in a grid under a sub-heading."""
    head, items = _items(sec["nodes"], fix)
    hp = _paras(head, fix)
    kids = [_head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
            B.raw(_yt(VIDEOS[0], "Lenz Heating &amp; Cooling on WHO 13 News Hello Iowa!"))]
    if opt.get("library"):
        for t, ps, _l in items:
            ps = [re.sub(r"\s*(?:<b>)?\[[^\]]*\](?:</b>)?", "", p).strip() for p in ps]
            kids.append(B.box("video-lib__head", [B.heading(t, "h3", "video-lib__title"),
                                                  B.text("".join("<p>%s</p>" % p for p in ps))]))
        kids.append(B.raw('<div class="video-grid">%s</div>' % "".join(
            _yt(v, "Lenz Heating &amp; Cooling Hello Iowa! segment %d" % i) for i, v in enumerate(VIDEOS[1:], 2))))
    btns = _doc_buttons(sec["nodes"], opt)
    if btns:
        kids.append(B.box("section-cta", btns))
    return B.section("section video-section %s %s" % (opt.get("bg", "section--mist"), page["_cat"]), kids,
                     el_id=opt.get("id"))


OFFICES = [
    ("Urbandale", "Main office", "7641 Douglas Ave, Urbandale, IA 50322", "7641+Douglas+Avenue,+Urbandale,+IA+50322"),
    ("Waukee", "Waukee location", "810 Interstate Pkwy, Suite 141, Waukee, IA 50263", "810+Interstate+Pkwy+Suite+141,+Waukee,+IA+50263"),
]


def block_locations(page, sec, opt, fix):
    """Two office cards: map, address, directions. Text per office from the doc's
    `h` items when present (Service Areas), else just the address (Contact)."""
    head, items = _items(sec["nodes"], fix)
    hp = [p for p in _paras(head, fix)]
    office_btns, cur = [], -1                       # doc buttons that follow each office heading
    for n in sec["nodes"]:
        if n["t"] == "h":
            cur += 1
            office_btns.append([])
        elif n["t"] == "button" and cur >= 0:
            office_btns[cur].append(n)
    cards = []
    for i, (city, label, addr, q) in enumerate(OFFICES):
        label = opt.get("labels", [label, label])[i]
        body = []
        if i < len(items):
            t, ps, _l = items[i]
            label = fix(re.sub(r"<[^>]+>", "", t))
            body = [p for p in ps if not re.sub(r"<[^>]+>", "", p).strip().endswith(":") and addr.split(",")[0] not in p]
        kids = [B.raw('<div class="office__map"><iframe src="https://www.google.com/maps?q=%s&amp;output=embed" '
                      'title="Map of the Lenz %s office" loading="lazy" referrerpolicy="no-referrer-when-downgrade">'
                      '</iframe></div>' % (q, city)),
                B.box("office__body", [
                    B.heading(label, "h3", "office__title"),
                    B.raw('<p class="office__addr">%s%s</p>' % (svg("i-pin", "icon-sm"), addr)),
                    B.text("".join("<p>%s</p>" % p for p in body), "office__text"),
                    B.box("office__cta", (_doc_buttons(office_btns[i], opt) if i < len(office_btns) else []) + [
                        B.button("Call " + B.PHONE, B.PHONE_TEL,
                                 "btn btn-outline" if i < len(office_btns) and office_btns[i] else "btn btn-primary",
                                 icon="phone"),
                        B.button("Get Directions", "https://www.google.com/maps/dir/?api=1&destination=" + q,
                                 "btn btn-outline", external=True),
                    ]),
                ])]
        cards.append(B.box("office", kids, tag="article"))
    return B.section("section offices-section %s %s" % (opt.get("bg", ""), page["_cat"]), [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(hp) if hp else None),
        B.box("offices", cards),
    ], el_id=opt.get("id"))


def block_area(page, sec, opt, fix):
    """The home's service-area block (city chips, note, offices, map) with the doc's copy."""
    paras = [p for p in _paras(sec["nodes"], fix) if not re.sub(r"<[^>]+>", "", p).strip().endswith(":")]
    cities = [re.sub(r",\s*IA$", "", re.sub(r"<[^>]+>", "", li)) for li in _lis(sec["nodes"], fix)] or \
        ["Urbandale", "Des Moines", "West Des Moines", "Waukee", "Ankeny", "Johnston", "Clive", "Grimes",
         "Altoona", "Norwalk", "Windsor Heights"]
    lead, rest = (paras[0], paras[1:]) if paras else (None, [])
    label = next((re.sub(r"</?b>", "", p) for p in _paras(sec["nodes"], fix)
                  if re.sub(r"<[^>]+>", "", p).strip().endswith(":")), None)
    def chip(c):
        key = c.strip().lower().replace(" ", "-")
        if key in ("urbandale", "waukee"):          # the two city pages
            return '<a class="area-chip area-chip--link" href="%s">%s%s</a>' % (L[key], svg("i-pin", "icon-xs"), c)
        return '<span class="area-chip">%s%s</span>' % (svg("i-pin", "icon-xs"), c)
    copy = ([B.text(label, "area__label")] if label else []) + [B.raw('<div class="area__cities">%s</div>' % "".join(
        chip(c) for c in cities))]
    for p in rest:
        copy.append(B.raw('<p class="area__note">%s%s</p>' % (svg("i-info", "icon-sm"), p)))
    copy.append(B.raw('<p class="area__address">%s<a href="https://www.google.com/maps/dir/?api=1&amp;destination='
                      '7641+Douglas+Avenue,+Urbandale,+IA+50322" target="_blank" rel="noopener noreferrer">Main '
                      'office: 7641 Douglas Ave, Urbandale, IA 50322</a><span class="sep">·</span><a href="https://'
                      'www.google.com/maps/dir/?api=1&amp;destination=810+Interstate+Pkwy+Suite+141,+Waukee,+IA" '
                      'target="_blank" rel="noopener noreferrer">Waukee: 810 Interstate Pkwy, Suite 141</a></p>'
                      % svg("i-pin", "icon-sm")))
    btns = _doc_buttons(sec["nodes"], opt)
    if btns:
        copy.append(B.box("section-cta", btns))
    return B.section("area section " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), lead, center=True),
        B.box("area__layout", [
            B.box("area__copy", copy),
            B.box("area__map", [B.raw(
                '<iframe src="https://www.google.com/maps?q=7641+Douglas+Avenue,+Urbandale,+IA+50322&amp;output=embed" '
                'title="Lenz Heating &amp; Cooling location and service area map" loading="lazy" '
                'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>')]),
        ]),
    ], el_id="area")


def block_coupons(page, sec, opt, fix):
    imgs = opt["images"]
    return B.section("section coupons-section section--mist " + page["_cat"], [
        _head(page, opt.get("eyebrow", ("i-card", "Current specials")), opt.get("title", "Current Specials"),
              opt.get("lead"), center=True),
        B.box("coupons", [B.image(k, alt, "coupon") for k, alt in imgs]),
    ], el_id="specials")


def block_embed(page, sec, opt, fix):
    """A third-party form in an iframe (the client's LeadConnector forms)."""
    paras = _paras(sec["nodes"], fix)
    return B.section("section embed-section section--mist " + page["_cat"], [
        _head(page, opt["eyebrow"], fix(sec["title"]), " ".join(paras) if paras else None, center=True),
        B.box("embed-card", [B.raw(
            '<iframe src="%s" id="%s" title="%s" style="width:100%%;height:%dpx;border:none;border-radius:3px" '
            'loading="lazy"></iframe><script src="https://link.msgsndr.com/js/form_embed.js"></script>'
            % (opt["src"], opt.get("frame_id", "lenz-embed-form"), opt.get("frame_title", "Form"), opt.get("height", 900)))]),
    ], el_id=opt.get("id"))


BLOCKS = {"checklist": block_checklist, "cards": block_cards, "boldcards": block_boldcards,
          "pair": block_pair, "bullets": block_bullets, "values": block_values, "table": block_table,
          "prose": block_prose, "promo": block_promo, "plans": block_plans, "why": block_why,
          "reviews": block_reviews, "faq": block_faq, "services": block_services,
          "multi": block_multi, "people": block_people, "roster": block_roster, "steps": block_steps,
          "cta": block_cta, "video": block_video, "locations": block_locations, "area": block_area,
          "coupons": block_coupons, "embed": block_embed}
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
    if page.get("kicker_from_first_bold") and paras and re.fullmatch(r"\s*<b>.*</b>\s*", paras[0]):
        kicker = re.sub(r"</?b>", "", paras.pop(0))
    # "<b>A</b> · <b>B</b> · ..." mini trust bar
    dots = next((p for p in paras if p.count(" · ") >= 2 and "<b>" in p), None)
    if dots:
        paras.remove(dots)
        page.setdefault("trust", [(re.sub(r"</?b>", "", x).strip(), "") for x in dots.split(" · ")])
    if page.get("hero_paras"):
        paras = paras[:page["hero_paras"]]
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
    takes_extra = any(sp[0] == "checklist" for sp in page["plan"])
    if page.get("is_hub") or not takes_extra:
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
    doc_btn = next((re.sub(r"\s*→\s*$", "", l) for n in nodes if n["t"] == "button" for l in n["labels"]
                    if not re.search(r"\(515\)|^call", l, re.I)), None)
    copy.append(B.box("hero__cta", [
        B.button(doc_btn or page["cta"], page.get("cta_href", L["form"]), "btn btn-gold"),
        B.button("Call " + B.PHONE, B.PHONE_TEL, "btn btn-outline-light", icon="phone"),
    ]))
    badge_t, badge_s = page["badge"]
    return B.section("hero hero--service " + page["_cat"], [
        B.box("hero__copy", copy),
        B.box("hero__media", [
            B.image(img_key, img_alt),
            B.raw('<div class="hero__badge"><span class="hero__badge-icon">%s</span><span><b>%s</b>%s</span></div>'
                  % (svg("i-clock", "icon"), B.nw(badge_t), B.nw(badge_s))),
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
    title, hub, kids = next(s for s in B.MENU if s[1] == page["hub"][1])
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
    # Content that arrived after the doc (e.g. ClickUp requests): text patches and
    # extra `h` + `p` items appended to a section, each documented in the page build.
    for old, new in page.get("doc_patches", []):
        for n in doc["hero"] + [x for sec in doc["sections"] for x in sec["nodes"]]:
            if n.get("text") and old in n["text"]:
                n["text"] = n["text"].replace(old, new)
    for match, head, body in page.get("add_items", []):
        sec = next(x for x in doc["sections"] if match in x["title"])
        sec["nodes"].append({"t": "h", "text": head})
        if body:
            sec["nodes"].append({"t": "p", "text": body})
    for n in doc["hero"] + [x for sec in doc["sections"] for x in sec["nodes"]]:
        if n["t"] == "p" and re.match(r"(?i)\s*(<b>)?\s*(web dev )?design note", n.get("text", "")):
            n["t"] = "note"
    fix = Copy()
    c = CAT[page["cat"]]
    if "cat_label" in page:          # a company page, not a service family: the home's band
        page.setdefault("band", "Heat out? AC down? We&apos;re ready right now.")
        page.setdefault("band_sub", "24/7 emergency service across the Des Moines metro since 2009.")
    page.setdefault("cat_icon", c["icon"])
    page.setdefault("cat_label", c["label"])
    page.setdefault("hub", c["hub"])
    page["_cat"] = "svc-page svc-page--" + page["cat"]
    S = [_hero(page, doc, fix)]
    trust = page.get("trust") or page["_trust"]
    long_ = " trustbar--long trustbar--%d" % len(trust) if trust else ""
    S.append(B.trustbar(trust or DEFAULT_TRUST, extra=page["_cat"] + long_))
    banded = page.get("no_band", False)
    secs = iter(doc["sections"])
    consumed = 0
    for spec in page["plan"]:
        kind = spec[0]
        opt = spec[1] if len(spec) > 1 else {}
        if kind.startswith("+"):
            kind, sec = kind[1:], {"title": "", "nodes": []}
        else:
            sec = next(secs)
            consumed += 1
        if kind == "skip":
            continue
        if kind == "close":
            paras = _paras(sec["nodes"], fix)
            if not page.get("is_hub"):
                S.append(_related(page))
            label = next((re.sub(r"\s*→\s*$", "", l) for n in sec["nodes"] if n["t"] == "button" for l in n["labels"]
                          if not re.search(r"\(515\)|^call", l, re.I) and not re.search(NOT_A_BUTTON, l)),
                         page["cta"])
            S.append(B.close_form(fix(sec["title"]), "".join("<p>%s</p>" % p for p in paras),
                                  button_text=label, preselect=page.get("form_preselect"),
                                  extra=page["_cat"]))
            continue
        opt = dict(opt)
        opt.setdefault("eyebrow", DEFAULT_EB.get(kind, ("i-info", "")))
        res = BLOCKS[kind](page, sec, opt, fix)
        S.extend(res if isinstance(res, list) else [res])
        if kind in BAND_AFTER and not banded:
            S.append(B.cta_band(page.get("band", c["band"]), page.get("band_sub", c["band_sub"]),
                                extra=page["_cat"]))
            banded = True
    if consumed != len(doc["sections"]):
        raise SystemExit("plan uses %d sections, doc has %d: %s" % (
            consumed, len(doc["sections"]), [s["title"] for s in doc["sections"]]))
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
