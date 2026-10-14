#!/usr/bin/env python3
"""Lenz: AC Repair (/ac-repair/). Copy from source.docx ("Lenz AC Repair"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/ac-repair/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x40000000)

PAGE = {
    "slug": "ac-repair",
    "source": os.path.join(HERE, "source.docx"),
    "title": "AC Repair",
    "cat": "cool",
    "accent": "AC Repair",
    "cta": "Schedule AC Repair",
    "form_preselect": "AC Repair",
    "hero_image": ("lenz-technician-service-call-webp", "A Lenz technician diagnosing a home comfort system on a service call"),
    "badge": ("24/7 emergency AC repair", "Local team, real people, day or night."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-wrench", "Don&apos;t wait for a breakdown")}),
        ("cards", {"eyebrow": ("i-snow", "What we fix"),
                   "icons": ["i-heat", "i-wind", "i-info", "i-clock", "i-snow", "i-droplet", "i-shield"]}),
        ("values", {"image": ("lenz-comfort-webp", "A family relaxing in a comfortable, cool Des Moines living room")}),
        ("why", {"icons": ["i-card", "i-clock", "i-shield"]}),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": ['Hero photo is the furnace technician until the 2026-10-15 shoot.'],
}

service_page.write(PAGE, HERE)
