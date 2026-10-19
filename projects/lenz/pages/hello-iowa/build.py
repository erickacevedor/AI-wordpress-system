#!/usr/bin/env python3
"""Lenz: Hello Iowa! (/hello-iowa/). Copy from source.docx ("Lenz Hello Iowa Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/hello-iowa/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x66000000)

PAGE = {
    "slug": "hello-iowa",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Hello Iowa!",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-tv",
    "cat_label": "As seen on TV",
    "accent": "Hello Iowa!",
    "cta": "Schedule Service Online",
    "hero_image": ("lenz-technician-service-call-webp", "A Lenz technician on a service call"),
    "badge": ("As seen on WHO 13", "Seasonal HVAC tips for Central Iowa."),
    "kicker_from_first_bold": True,
    "no_band": True,
    "doc_patches": [("Catch our most recent broadcast on Hello Iowa! Below:",
                     "Catch our most recent Hello Iowa! broadcast below.")],   # QA 2026-10-19: doc typo
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("video", {"library": True}),
        ("boldcards", {"eyebrow": ("i-award", "Why Lenz"), "icons": ["i-award", "i-card", "i-pin"]}),
        ("close",),
    ],
    "notes": ['Videos: the five segments on lenzmechanical.com/hello-iowa/. Doc comment: full video library as on that page.'],
}

service_page.write(PAGE, HERE)
