#!/usr/bin/env python3
"""Lenz: Service Areas (/service-areas/). Copy from source.docx ("Lenz Service Areas"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/service-areas/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x69000000)

PAGE = {
    "slug": "service-areas",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Service Areas",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-pin",
    "cat_label": "Service areas",
    "accent": "HVAC Service Areas",
    "cta": "Schedule Service Online",
    "hero_image": ("lenz-service-van-wrap-webp", "A Lenz Heating &amp; Cooling wrapped service van"),
    "badge": ("Two local offices", "Urbandale and Waukee."),
    
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("locations", {"eyebrow": ("i-pin", "Two local offices")}),
        ("area",),
        ("services", {"eyebrow": ("i-wrench", "Services near you"),
                      "links": ["air-conditioning", "heating", "indoor-air-quality", "additional-services", "tel"],
                      "icons": ["i-snow", "i-flame", "i-air", "i-wrench", "i-clock"]}),
        ("prose", {"eyebrow": ("i-pin", "Built for Central Iowa"), "bg": "section--mist"}),
        ("promo", {"link": "tel"}),
        ("faq",),
        ("close",),
    ],
    "notes": ["Doc map note: a custom Google map with every city pinned needs a My Maps embed from the client's account; the page uses the office map until then."],
}

service_page.write(PAGE, HERE)
