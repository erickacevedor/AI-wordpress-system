#!/usr/bin/env python3
"""Lenz: Humidity Control (/humidity-control/). Copy from source.docx ("Lenz Humidity Control"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/humidity-control/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x47000000)

PAGE = {
    "slug": "humidity-control",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Humidity Control",
    "cat": "air",
    "accent": "Humidity Control",
    "cta": "Schedule a Humidity Consultation",
    "form_preselect": "Indoor Air Quality",
    "hero_image": ("lenz-comfort-webp", "A family relaxing together in a bright, comfortable Des Moines living room"),
    "badge": ("Whole-home humidity control", "Upfront, To-the-Penny pricing."),
    "kicker_from_section0": True,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("pair", {"eyebrow": ("i-droplet", "30% to 50% is the sweet spot")}),
        ("checklist", {"eyebrow": ("i-droplet", "Dry winter air")}),
        ("checklist", {"eyebrow": ("i-droplet", "Muggy summers"), "bg": "section--cream"}),
        ("table",),
        ("promo",),
        ("why",),
        ("faq",),
        ("close",),
    ],
    "notes": ['Doc comments (Manuel Henao) applied: trustbar, 2-column dry/damp cards, 3-column why cards.'],
}

service_page.write(PAGE, HERE)
