#!/usr/bin/env python3
"""Lenz: AC Installation (/ac-installation/). Copy from source.docx ("Lenz AC Installation"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/ac-installation/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x41000000)

PAGE = {
    "slug": "ac-installation",
    "source": os.path.join(HERE, "source.docx"),
    "title": "AC Installation",
    "cat": "cool",
    "accent": "AC Installation",
    "cta": "Schedule AC Installation",
    "form_preselect": "AC Installation",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling technician team standing in front of their service vans"),
    "badge": ("Free installation estimates", "Upfront pricing before any work begins."),
    "kicker_from_section0": False,
    "related_text": "The same local team for every part of your home comfort, from the first visit to the last.",
    # One entry per doc section, in doc order (see tools/docx_outline.py).
    "plan": [
        ("checklist", {"eyebrow": ("i-wrench", "Plan it right")}),
        ("cards", {"eyebrow": ("i-snow", "When it makes sense"), "help": ("Not sure what your home needs?", "Call us and talk it through with our local team, no pressure.")}),
        ("values",),
        ("why",),
        ("faq",),
        ("reviews",),
        ("close",),
    ],
    "notes": [],
}

service_page.write(PAGE, HERE)
