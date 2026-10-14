#!/usr/bin/env python3
"""Lenz: Contact Us (/contact/). Copy from source.docx ("Lenz Contact Us"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/contact/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x62000000)

PAGE = {
    "slug": "contact",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Contact Us",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-phone",
    "cat_label": "Contact",
    "accent": "Contact Lenz Heating &amp; Cooling",
    "cta": "Book Online",
    "hero_image": ("lenz-service-van-wrap-webp", "A Lenz Heating &amp; Cooling wrapped service van"),
    "badge": ("Open 24 hours", "Call (515) 225-6446 for urgent help."),
    "no_band": True,
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("checklist", {"eyebrow": ("i-clock", "Urgent? Call us"), "tel": True, "drop": [r"^For immediate help", r"\[button\]"]}),
        ("close",),
        ("cards", {"eyebrow": ("i-check", "What to expect"), "cols": 2, "numbered": True, "help": None}),
        ("locations", {"eyebrow": ("i-pin", "Our offices"), "labels": ["Urbandale Location", "Waukee Location"]}),
        ("reviews",),
        ("faq",),
        ("cta", {"links": {"Book Online": "#contact"}}),
    ],
    "notes": ["The form section uses the site's estimate form (Elementor Pro). The client's current site sends every form to LeadConnector (form qqIhBpp3Uvkj3zopUtRg): decide which one the new site uses."],
}

service_page.write(PAGE, HERE)
