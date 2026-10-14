#!/usr/bin/env python3
"""Lenz: Indoor Air Quality hub (/indoor-air-quality/). Copy from source.docx ("Lenz IAQ Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/indoor-air-quality/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x52000000)

PAGE = {
    "slug": "indoor-air-quality",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Indoor Air Quality",
    "is_hub": True,
    "cat": "air",
    "accent": "Indoor Air Quality",
    "cta": "Schedule Your Air Quality Evaluation",
    "form_preselect": "Indoor Air Quality",
    "hero_image": ("lenz-comfort-webp", "A family relaxing together in a bright, comfortable Des Moines living room"),
    "badge": ("Indoor air quality evaluations", "Upfront, flat-rate pricing."),
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("services", {"eyebrow": ("i-air", "Air quality solutions"),
                      "links": ["indoor-purification", "uv-light-purification", "humidity-control", "duct-cleaning", "ductwork"],
                      "icons": ["i-air", "i-shield", "i-droplet", "i-wind", "i-wrench"]}),
        ("table", {"eyebrow": ("i-air", "Warning signs")}),
        ("promo", {"link": "financing"}),
        ("faq",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
