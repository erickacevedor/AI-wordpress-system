#!/usr/bin/env python3
"""Lenz: Careers (/hvac-jobs/). Copy from source.docx ("Lenz Come Work With Us Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/hvac-jobs/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x68000000)

PAGE = {
    "slug": "hvac-jobs",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Careers",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-wrench",
    "cat_label": "Careers",
    "accent": "Come Work With Us",
    "cta": "Apply Now",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling team standing in front of their service vans"),
    "badge": ("Year-round work", "Veteran-led, family-owned team."),
    "kicker_from_first_bold": True,
    "cta_href": "#apply",
    "no_band": True,
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("embed", {"src": "https://api.leadconnectorhq.com/widget/form/qqIhBpp3Uvkj3zopUtRg", "id": "apply",
                   "frame_id": "qqIhBpp3Uvkj3zopUtRg", "frame_title": "Lenz employment application", "height": 1100}),
        ("boldcards", {"eyebrow": ("i-award", "Why Lenz"), "icons": ["i-card", "i-calendar", "i-shield", "i-wrench", "i-award", "i-pin"]}),
        ("boldcards", {"eyebrow": ("i-wrench", "Open roles"), "bg": "section--mist", "icons": ["i-wrench", "i-flame", "i-phone"]}),
        ("faq", {"last_as_cta": True, "links": {"Submit Your Application Above": "#apply"}}),
    ],
    "notes": ['Application form: the LeadConnector form the current site embeds on its jobs page (doc comment: same as current site). It is the same form id the current site uses for contact requests: confirm it is the right one for applications.'],
}

service_page.write(PAGE, HERE)
