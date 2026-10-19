#!/usr/bin/env python3
"""Lenz: Air Purification (/air-purification/). Copy from source.docx ("Lenz Air Purification"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/air-purification/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x49000000)

PAGE = {
    "slug": "air-purification",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Air Purification",
    "cat": "air",
    "accent": "Air Purification",
    "cta": "Schedule Air Purification",
    "form_preselect": "Indoor Air Quality",
    "hero_image": ("lenz-comfort-webp", "A family relaxing together in a bright, comfortable Des Moines living room"),
    "badge": ("Whole-home air purification", "Upfront, To-the-Penny pricing."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("table", {"eyebrow": ("i-air", "1-inch vs 4-inch")}),
        ("bullets", {"eyebrow": ("i-air", "What it removes")}),
        ("cards", {"eyebrow": ("i-air", "Is it right for you?"), "cols": 2, "help": None}),
        ("table", {"eyebrow": ("i-air", "Whole-home vs portable"), "bg": "section--cream"}),
        ("promo",),
        ("why",),
        ("faq",),
        ("close",),
    ],
    "notes": ['Menu and card label "Air Purification" (was "Indoor Purification" until the 2026-10-19 QA), same as the page and doc.'],
}

service_page.write(PAGE, HERE)
