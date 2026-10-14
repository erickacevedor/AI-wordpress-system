#!/usr/bin/env python3
"""Lenz: Heating Repair (/heating-repair/). Copy from source.docx ("Lenz Heating Repair"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/heating-repair/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x45000000)

PAGE = {
    "slug": "heating-repair",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Heating Repair",
    "cat": "warm",
    "accent": "Heating Repair",
    "cta": "Schedule Heating Repair",
    "form_preselect": "Furnace & Heating",
    "hero_image": ("lenz-technician-service-call-webp", "A Lenz technician repairing a gas furnace in a Des Moines basement"),
    "badge": ("24/7 emergency heating repair", "Local team, real people, day or night."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-flame", "Don&apos;t wait for a no-heat night")}),
        ("cards", {"eyebrow": ("i-flame", "What we fix")}),
        ("values",),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
