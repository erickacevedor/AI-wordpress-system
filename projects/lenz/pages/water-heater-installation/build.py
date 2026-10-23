#!/usr/bin/env python3
"""Lenz: Water Heater Installation (/water-heater-installation/). Copy from source.docx
("Lenz Water Heater Installation page", Manuel Henao, ClickUp 86bckn61j); layout from
../../service_page.py.

The doc has no section headings: its meta lines are plain paragraphs and every section
title is a bold-only paragraph, so prepare() reshapes the outline before the build.

Run: python3 projects/lenz/pages/water-heater-installation/build.py
"""
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x6c000000)

SOURCE = os.path.join(HERE, "source.docx")


def _bold_only(n):
    return n["t"] == "p" and re.fullmatch(r"\s*<b>[^<]+</b>\s*", n["text"])


def _plain(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def prepare(doc):
    # Meta: "Meta title" / "Meta description" / "URL" labels, each followed by its value.
    xml = zipfile.ZipFile(SOURCE).read("word/document.xml").decode("utf8")
    lines = [re.sub(r"\s+", " ", "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))).strip()
             for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)]
    lines = [x for x in lines if x]
    keys = {"meta title": "title", "meta description": "description", "url": "slug"}
    doc["meta"] = {keys[x.lower()]: lines[i + 1] for i, x in enumerate(lines[:6]) if x.lower() in keys}

    hero, sections, cur = [], [], None
    for n in doc["hero"]:
        if _bold_only(n) and not (cur and "FAQ" in cur["title"] and _plain(n["text"]).endswith("?")):
            cur = {"title": _plain(n["text"]), "nodes": []}
            sections.append(cur)
        elif _bold_only(n) and cur:                     # an FAQ question
            cur["nodes"].append({"t": "h", "text": _plain(n["text"])})
        else:
            (cur["nodes"] if cur else hero).append(n)
    # "No hot water today? Call ..." becomes the hero badge (the hero already has the call button).
    call = next(n for n in hero if n["t"] == "p" and _plain(n["text"]).startswith("No hot water today?"))
    hero.remove(call)
    q, _, a = _plain(call["text"]).partition("? ")
    PAGE["badge"] = (q + "?", a)
    # Service area: the cities named in the doc's sentence become the area chips.
    area = next(s for s in sections if s["title"].startswith("Water Heater Installation Across"))
    sentence = _plain(next(n["text"] for n in area["nodes"] if n["t"] == "p"))
    cities = re.split(r",\s*(?:and\s+)?", re.search(r"throughout (.+)\.$", sentence).group(1))
    area["nodes"] += [{"t": "li", "text": c} for c in cities]
    doc["hero"], doc["sections"] = hero, sections
    return doc


PAGE = {
    "slug": "water-heater-installation",
    "source": SOURCE,
    "prepare": prepare,
    "title": "Water Heater Installation",
    "cat": "extra",
    "accent": "Water Heater Installation",
    "cta": "Get a Free Water Heater Estimate",
    "form_preselect": "Water Heater Installation",
    "hero_image": ("lenz-technician-service-call-webp",
                   "A Lenz Heating &amp; Cooling technician on a service call in a Des Moines home"),
    "badge": None,                                       # set by prepare() from the doc
    "related": ("More Services From Lenz", [("Heating Installation", "heating-installation"),
                                            ("AC Installation", "ac-installation"),
                                            ("Humidity Control", "humidity-control")]),
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # The doc's link notes (Word comments) point the CTAs to /contact-us/ and the financing
    # links to /service-agreement/ (old site URLs). ClickUp 09/10 item 13: CTAs go to the
    # form on the page; financing goes to the new /financing/ page.
    "doc_patches": [("<b>See financing options.</b>", '<a href="%s">See financing options.</a>' % B.L["financing"])],
    # One entry per doc section, in doc order.
    "plan": [
        ("checklist", {"eyebrow": ("i-info", "Know the signs")}),
        ("boldcards", {"eyebrow": ("i-droplet", "Tank or tankless"), "cols": 3,
                       "icons": ["i-droplet", "i-clock", "i-info"]}),
        ("prose", {"eyebrow": ("i-award", "Brands we install")}),
        ("steps", {"eyebrow": ("i-check", "What to expect"), "buttons": True,
                   "links": {"See Financing Options": "financing"}}),
        ("area", {"eyebrow": ("i-pin", "Service area"), "links": {"See our full service area": "service-areas"}}),
        ("faq",),
        ("close",),
    ],
    "notes": [
        "Hero badge is the doc line \"No hot water today? Call (515) 225-6446.\"",
        "Doc link notes (Word comments): CTAs to /contact-us/ and financing to /service-agreement/ (old site "
        "URLs). Built as the rest of the site: CTAs to the form on the page (#contact, ClickUp 09/10 item 13), "
        "\"See Financing Options\" and the FAQ link to /financing/, \"See our full service area\" to /service-areas/.",
        "Doc note on the service area: 2 column layout with GBP embedded map. Uses the home's area block "
        "(city chips from the doc's sentence + map of the main office); a Google Business Profile embed needs "
        "the Place ID, still pending from the client.",
        "Hero photo: technician on a service call (no water heater photo in the media library yet).",
    ],
}

service_page.write(PAGE, HERE)
