#!/usr/bin/env python3
"""Lenz: Urbandale (/urbandale/). Copy from source.docx ("Lenz Urbandale"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/urbandale/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x6a000000)

PAGE = {
    "slug": "urbandale",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Urbandale",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-pin",
    "cat_label": "Urbandale, IA",
    "accent": "HVAC Services",
    "cta": "Schedule Service Online",
    "hero_image": ("lenz-service-van-wrap-webp", "A Lenz Heating &amp; Cooling wrapped service van"),
    "badge": ("Local Urbandale team", "24/7 emergency service."),
    
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("prose", {"eyebrow": ("i-pin", "Local service")}),
        ("services", {"eyebrow": ("i-wrench", "Services in Urbandale"),
                      "links": ["air-conditioning", "heating", "indoor-air-quality", "additional-services", "tel"],
                      "icons": ["i-snow", "i-flame", "i-air", "i-wrench", "i-clock"]}),
        ("cards", {"eyebrow": ("i-pin", "Neighborhood needs"), "cols": 2, "help": None}),
        ("why", {"icons": ["i-pin", "i-card", "i-clock", "i-shield"]}),
        ("steps", {"eyebrow": ("i-check", "What to expect")}),
        ("faq",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
