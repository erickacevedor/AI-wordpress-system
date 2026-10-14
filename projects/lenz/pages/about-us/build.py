#!/usr/bin/env python3
"""Lenz: About Us (/about-us/). Copy from source.docx ("Lenz About Us"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/about-us/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x60000000)

PAGE = {
    "slug": "about-us",
    "source": os.path.join(HERE, "source.docx"),
    "title": "About Us",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-award",
    "cat_label": "About Lenz",
    "accent": "About Lenz Heating &amp; Cooling",
    "cta": "Get a Free Estimate",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling team standing in front of their service vans"),
    "badge": ("Family-owned since 2009", "Veteran-owned and woman-owned."),
    "hero_paras": 1,
    "trust": [("Veteran-Owned &amp; Led", "Founded by U.S. Marine Corps veteran Al Lenz"),
              ("Woman-Owned &amp; Operated", "Co-owned with Jenny Lenz"),
              ("Serving Central Iowa Since 2009", "Across the greater Des Moines metro"),
              ("Licensed, Bonded &amp; Insured", "Iowa Master License #50871-CL")],
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("multi", {"parts": [("prose", {"eyebrow": ("i-award", "Our story")}),
                             ("boldcards", {"eyebrow": ("i-shield", "Our values"), "cols": 4,
                                            "icons": ["i-shield", "i-card", "i-award", "i-check"]}),
                             ("people", {"eyebrow": ("i-award", "The owners"), "cols": 2})]}),
        ("roster", {"eyebrow": ("i-award", "Our team"), "bg": "section--mist"}),
        ("roster", {"eyebrow": ("i-star", "Office dogs"), "role": "Office Dog", "dogs": True,
                    "links": {"Meet Our Team": "meet-the-team", "Join Our Team": "hvac-jobs"}}),
        ("why", {"icons": ["i-card", "i-clock", "i-shield"]}),
        ("promo", {"link": "community-outreach"}),
        ("why", {"eyebrow": ("i-award", "Trusted &amp; local"), "icons": ["i-award", "i-shield", "i-pin"]}),
        ("video", {"links": {"Watch Our Segment": "hello-iowa"}}),
        ("reviews",),
        ("area", {"links": {"View Our Service Area": "service-areas"}}),
        ("faq",),
        ("close",),
    ],
    "notes": ['Doc comments applied: trustbar, 4-column values, a card per person and dog (no bios), 3-column why and trusted cards. Team photos and headshots not available: cards use initials.'],
}

service_page.write(PAGE, HERE)
