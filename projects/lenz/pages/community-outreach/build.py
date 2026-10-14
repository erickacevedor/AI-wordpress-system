#!/usr/bin/env python3
"""Lenz: Community Outreach (/community-outreach/). Copy from source.docx ("Lenz Community Outreach"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/community-outreach/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x67000000)

PAGE = {
    "slug": "community-outreach",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Community Outreach",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-award",
    "cat_label": "Community",
    "accent": "Giving Back",
    "cta": "Contact Our Team",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling team standing in front of their service vans"),
    "badge": ("Operation Lenz a Helping Hand", "Helping neighbors stay safe and comfortable."),
    "cta_href": "/contact/",
    "no_band": True,
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("prose", {"eyebrow": ("i-award", "Rooted in service")}),
        ("promo", {"link": "tel", "button": "Ask About Operation Lenz a Helping Hand"}),
        ("prose", {"eyebrow": ("i-star", "Students, teams &amp; families"), "bg": "section--mist"}),
        ("prose", {"eyebrow": ("i-shield", "Local partnerships")}),
        ("prose", {"eyebrow": ("i-award", "Local businesses"), "bg": "section--mist", "links": {"Follow Lenz on Facebook": "facebook"}}),
        ("prose", {"eyebrow": ("i-check", "Our values"), "links": {"Explore HVAC Services": "/#services"}}),
        ("close",),
    ],
    "notes": ['Facebook link: https://www.facebook.com/lenzheatingandcooling/ (from the current site).'],
}

service_page.write(PAGE, HERE)
