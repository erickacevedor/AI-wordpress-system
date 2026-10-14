#!/usr/bin/env python3
"""Lenz: Specials (/specials/). Copy from source.docx ("Lenz Specials Page"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/specials/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x65000000)

PAGE = {
    "slug": "specials",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Specials",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-card",
    "cat_label": "Specials",
    "accent": "Save Money",
    "cta": "Book Your Service Online",
    "hero_image": ("lenz-service-van-wrap-webp", "A Lenz Heating &amp; Cooling wrapped service van"),
    "badge": ("Current coupons", "Show your technician to save."),
    "no_band": True,
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("+coupons", {"images": [("coupon-firstservice", "$100 off your first service call. Expires 12/31/2026."),
                                 ("coupon-ductcleaning", "Duct cleaning special. See coupon for details."),
                                 ("coupon-beatheeasy", "Breathe Easy package special. See coupon for details.")]}),
        ("steps", {"eyebrow": ("i-card", "Easy savings")}),
        ("boldcards", {"eyebrow": ("i-award", "Why Lenz"), "cols": 4, "icons": ["i-card", "i-shield", "i-clock", "i-award"]}),
        ("close",),
    ],
    "notes": ['Coupons are the three on lenzmechanical.com/specials (expire 12/31/2026) and still carry the old Lenz logo.'],
}

service_page.write(PAGE, HERE)
