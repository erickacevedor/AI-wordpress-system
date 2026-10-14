#!/usr/bin/env python3
"""Lenz: Heating hub (/heating/). Copy from source.docx ("Lenz Heating Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/heating/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x51000000)

PAGE = {
    "slug": "heating",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Heating",
    "is_hub": True,
    "cat": "warm",
    "accent": "Heating and Furnace Services",
    "cta": "Schedule Heating Service",
    "form_preselect": "Furnace & Heating",
    "hero_image": ("lenz-technician-service-call-webp", "A Lenz technician servicing a gas furnace in a Des Moines basement"),
    "badge": ("24/7 emergency heating repair", "Fast heat restoration, day or night."),
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("services", {"eyebrow": ("i-flame", "Heating services"),
                      "links": ["heating-repair", "heating-replacement", "heating-installation", "heating-maintenance"],
                      "icons": ["i-wrench", "i-heat", "i-flame", "i-calendar"]}),
        ("table", {"eyebrow": ("i-flame", "Warning signs")}),
        ("promo", {"link": "financing"}),
        ("faq",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
