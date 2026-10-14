#!/usr/bin/env python3
"""Lenz: Heating Installation (/heating-installation/). Copy from source.docx ("Lenz Heating Installation Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/heating-installation/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x44000000)

PAGE = {
    "slug": "heating-installation",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Heating Installation",
    "cat": "warm",
    "accent": "Heating Installation",
    "cta": "Schedule Heating Installation",
    "form_preselect": "Furnace & Heating",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling technician team standing in front of their service vans"),
    "badge": ("Free installation estimates", "Upfront pricing before any work begins."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-wrench", "Start early")}),
        ("cards", {"eyebrow": ("i-flame", "When it is needed"), "cols": 2, "help": None}),
        ("table", {"eyebrow": ("i-flame", "System options")}),
        ("bullets", {"eyebrow": ("i-check", "Done right")}),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
