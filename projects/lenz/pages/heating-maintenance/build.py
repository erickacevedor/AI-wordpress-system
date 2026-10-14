#!/usr/bin/env python3
"""Lenz: Heating Maintenance (/heating-maintenance/). Copy from source.docx ("Lenz Heating Maintenance"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/heating-maintenance/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x46000000)

PAGE = {
    "slug": "heating-maintenance",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Heating Maintenance",
    "cat": "warm",
    "accent": "Heating Maintenance",
    "cta": "Schedule Heating Maintenance",
    "form_preselect": "Maintenance",
    "hero_image": ("lenz-technician-service-call-webp", "A Lenz technician tuning up a gas furnace before winter"),
    "badge": ("Maintenance plans from $120 a year", "Priority dispatch and discounts on parts."),
    "kicker_from_section0": True,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("boldcards", {"eyebrow": ("i-flame", "Why it matters in Iowa"), "icons": ["i-shield", "i-card", "i-clock", "i-award"]}),
        ("pair", {"eyebrow": ("i-check", "What&apos;s included")}),
        ("bullets", {"eyebrow": ("i-info", "Know the signs")}),
        ("plans",),
        ("why",),
        ("faq",),
        ("close",),
    ],
    "notes": ['Doc comments (Manuel Henao) applied: trustbar from the hero bullets, 4-column cards, 2-column tune-up lists, 3-column why cards.'],
}

service_page.write(PAGE, HERE)
