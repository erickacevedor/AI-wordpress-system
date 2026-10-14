#!/usr/bin/env python3
"""Lenz: Air Conditioning hub (/air-conditioning/). Copy from source.docx ("Lenz Cooling Services"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/air-conditioning/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x50000000)

PAGE = {
    "slug": "air-conditioning",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Air Conditioning",
    "is_hub": True,
    "cat": "cool",
    "accent": "Cooling Services",
    "cta": "Schedule Cooling Service",
    "form_preselect": "Air Conditioning",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling technician team standing in front of their service vans"),
    "badge": ("24/7 emergency AC service", "Local team, real people, day or night."),
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-snow", "Know the signs")}),
        ("services", {"layout": "rows", "eyebrow": ("i-snow", "Cooling services"),
                      "links": ["ac-repair", "ac-installation", "ac-replacement", "ac-maintenance", "tel"],
                      "icons": ["i-wrench", "i-snow", "i-heat", "i-calendar", "i-clock"]}),
        ("values",),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
