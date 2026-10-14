#!/usr/bin/env python3
"""Lenz: Maintenance Plans (/maintenance-plan/). Copy from source.docx ("Lenz Maintenance Plans"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/maintenance-plan/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x64000000)

PAGE = {
    "slug": "maintenance-plan",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Maintenance Plans",
    "is_hub": True,
    "band": "Heat out? AC down? We&apos;re ready right now.",
    "band_sub": "24/7 emergency service across the Des Moines metro since 2009.",
    "cat": "cool",
    "cat_icon": "i-calendar",
    "cat_label": "Service agreements",
    "accent": "Maintenance Plans",
    "cta": "Enroll Now",
    "hero_image": ("lenz-thermostat-ecobee", "An ecobee smart thermostat installed on a living room wall"),
    "badge": ("Plans from $120 a year", "Priority dispatch and 10 to 20% off parts."),
    "kicker_from_section0": True,
    "form_preselect": "Maintenance",
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("boldcards", {"eyebrow": ("i-calendar", "Why a plan"), "cols": 4, "icons": ["i-shield", "i-card", "i-clock", "i-award"]}),
        ("plans",),
        ("boldcards", {"eyebrow": ("i-check", "Included in every plan"), "bg": "section--mist",
                       "icons": ["i-check", "i-card", "i-calendar", "i-clock", "i-shield", "i-award"]}),
        ("promo", {"button": "Enroll &amp; Start Earning"}),
        ("steps", {"eyebrow": ("i-check", "How it works")}),
        ("faq",),
        ("close",),
    ],
    "notes": ['Plan perks "no diagnostic charges, no trip fees" for members are kept as written: confirm with Sergio (ClickUp 09/10 only ruled out free diagnostics as a general promise).'],
}

service_page.write(PAGE, HERE)
