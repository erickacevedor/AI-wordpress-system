#!/usr/bin/env python3
"""Lenz: Financing (/financing/). Copy from source.docx ("Lenz Financing"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/financing/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x63000000)

PAGE = {
    "slug": "financing",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Financing",
    "is_hub": True,
    "band": "Heat out? AC down? We&apos;re ready right now.",
    "band_sub": "24/7 emergency service across the Des Moines metro since 2009.",
    "cat": "cool",
    "cat_icon": "i-card",
    "cat_label": "Financing",
    "accent": "HVAC Financing",
    "cta": "Apply Now",
    "hero_image": ("lenz-comfort-webp", "A family relaxing together in a bright, comfortable Des Moines living room"),
    "badge": ("0% deferred interest", "For qualified buyers, through Synchrony Bank."),
    "kicker_from_section0": True,
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("boldcards", {"eyebrow": ("i-card", "Why finance"), "icons": ["i-clock", "i-card", "i-award"]}),
        ("promo", {"button": "See If You Qualify"}),
        ("steps", {"eyebrow": ("i-check", "How it works")}),
        ("bullets", {"eyebrow": ("i-wrench", "What you can finance")}),
        ("prose", {"eyebrow": ("i-shield", "Our financing partner"), "bg": "section--mist"}),
        ("promo", {"link": "specials", "button": "See Current Specials"}),
        ("faq",),
        ("close",),
    ],
    "notes": ['"Apply Now" and "See If You Qualify" go to the estimate form until the Synchrony application URL arrives (pending asset).', 'Doc comment: Synchrony logo in "Financing You Can Trust": logo file not available yet.'],
}

service_page.write(PAGE, HERE)
