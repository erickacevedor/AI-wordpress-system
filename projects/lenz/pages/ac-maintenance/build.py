#!/usr/bin/env python3
"""Lenz: AC Maintenance (/ac-maintenance/). Copy from source.docx ("Lenz AC Maintenance"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/ac-maintenance/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x42000000)

PAGE = {
    "slug": "ac-maintenance",
    "source": os.path.join(HERE, "source.docx"),
    "title": "AC Maintenance",
    "cat": "cool",
    "accent": "AC Maintenance",
    "cta": "Schedule AC Maintenance",
    "form_preselect": "Maintenance",
    "hero_image": ("lenz-thermostat-ecobee", "An ecobee smart thermostat installed on a living room wall"),
    "badge": ("Maintenance plans from $120 a year", "Priority dispatch and discounts on parts."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-calendar", "Ready before summer")}),
        ("cards", {"eyebrow": ("i-snow", "What it prevents"), "help": ("Not sure your AC needs a tune-up?", "Call us and we&apos;ll tell you honestly.")}),
        ("values",),
        ("plans",),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
