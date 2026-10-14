#!/usr/bin/env python3
"""Lenz: AC Replacement (/ac-replacement/). Copy from source.docx ("Lenz_COPY_Page_AC Replacement"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/ac-replacement/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x43000000)

PAGE = {
    "slug": "ac-replacement",
    "source": os.path.join(HERE, "source.docx"),
    "title": "AC Replacement",
    "cat": "cool",
    "accent": "AC Replacement",
    "cta": "Schedule AC Replacement",
    "form_preselect": "AC Replacement",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling technician team standing in front of their service vans"),
    "badge": ("Free replacement estimates", "Clear repair versus replacement advice."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-wrench", "Plan ahead")}),
        ("cards", {"eyebrow": ("i-snow", "Signs to watch"),
                   "help": ("Repair or replace?", "Call us and we&apos;ll give you an honest answer.")}),
        ("values",),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
