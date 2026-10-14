#!/usr/bin/env python3
"""Lenz: UV Light Purification (/uv-light-purification/). Copy from source.docx ("Lenz UV Light Purification"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/uv-light-purification/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x48000000)

PAGE = {
    "slug": "uv-light-purification",
    "source": os.path.join(HERE, "source.docx"),
    "title": "UV Light Purification",
    "cat": "air",
    "accent": "UV Light Purification",
    "cta": "Schedule UV Light Purification",
    "form_preselect": "Indoor Air Quality",
    "hero_image": ("lenz-comfort-webp", "A family relaxing together in a bright, comfortable Des Moines living room"),
    "badge": ("Cleaner coils, fresher air", "Upfront, To-the-Penny pricing."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-air", "How it works")}),
        ("cards", {"eyebrow": ("i-air", "When it makes sense"), "help": ("Not sure UV is right for you?", "Ask for an indoor air quality evaluation and we&apos;ll find the real cause.")}),
        ("prose", {"eyebrow": ("i-wrench", "Add it to your system")}),
        ("prose", {"eyebrow": ("i-air", "UV and filters"), "bg": "section--mist"}),
        ("promo",),
        ("why",),
        ("faq",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
