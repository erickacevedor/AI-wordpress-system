#!/usr/bin/env python3
"""Lenz: Meet the Team (/meet-the-team/). Copy from source.docx ("Lenz Meet the team"); layout from ../../service_page.py.

Run: python3 projects/lenz/pages/meet-the-team/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import brand as B  # noqa: E402
import service_page  # noqa: E402

B.reset(0x61000000)

PAGE = {
    "slug": "meet-the-team",
    "source": os.path.join(HERE, "source.docx"),
    "title": "Meet the Team",
    "is_hub": True,
    "cat": "cool",
    "cat_icon": "i-award",
    "cat_label": "Our people",
    "accent": "Meet the Team",
    "cta": "Schedule Service Online",
    "hero_image": ("lenz-team-webp", "The Lenz Heating &amp; Cooling team standing in front of their service vans"),
    "badge": ("Background-checked &amp; drug-tested", "The same people who show up at your door."),
    
    # Added after the doc: ClickUp 86bbja6rr "Add Will and Songwa to the Lenz team page" (Sierra, 8/21/2026).
    # Songwa has no bio yet (Sierra did not send one): the card shows name and title only.
    "add_items": [("Service &amp; Installation Team", "Will — Installation Expert", "Will is originally from Adel, he grew up in the community and continues to call Adel home today. He attended ADM High School. He joined the Lenz team in July of 2026. Will comes from a family of four, his mom, dad, and a sister. When Will isn't working, you can usually find him staying active at the gym, spending time outdoors fishing, or enjoying one of his favorite hobbies, riding his motorcycle. He chose to work for Lenz because of the great things he had heard about the company, the team, and the reputation Lenz has built in the community."),
                  ("Service &amp; Installation Team", "Songwa — Service Technician", "")],
    # One entry per doc section, in doc order ("+x" adds a block without a doc section).
    "plan": [
        ("people", {"eyebrow": ("i-award", "Ownership"), "cols": 2}),
        ("people", {"eyebrow": ("i-award", "Leadership"), "bg": "section--mist"}),
        ("people", {"eyebrow": ("i-wrench", "In the field")}),
        ("people", {"eyebrow": ("i-calendar", "In the office"), "cols": 2, "bg": "section--mist"}),
        ("people", {"eyebrow": ("i-star", "Office dogs"), "dogs": True}),
        ("promo", {"link": "hvac-jobs"}),
        ("close",),
    ],
    "notes": ["Doc comment applied: mini trust bar. Headshots not available: cards use initials (Lucy's headshots in ClickUp could replace them)."],
}

service_page.write(PAGE, HERE)
