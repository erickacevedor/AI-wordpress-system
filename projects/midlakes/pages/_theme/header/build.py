# -*- coding: utf-8 -*-
"""
Mid Lakes — header Theme Builder template.

PORT-DECISIONS decision 9: the prototype repeats an identical header on every page,
so it belongs here rather than being ported six times.

Validates as type "header", which the gate treats as a page that must NOT contain an
H1 — a header H1 would override the H1 of every page it is applied to.

Run:
    python3 projects/midlakes/pages/_theme/header/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/_theme/header/header.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x4A000000)

if __name__ == "__main__":
    B.write(B.theme_part("Mid Lakes Header", [B.header_bar()], "header"),
            "header.json", HERE)
