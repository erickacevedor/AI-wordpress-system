# -*- coding: utf-8 -*-
"""
Mid Lakes — footer Theme Builder template.

PORT-DECISIONS decision 9. Validates as type "footer" (no H1).

⚠️ The 300px bottom padding is NOT dead space: it clears .ml-footer::after, the
1.svg wave at 10% opacity. If that watermark is ever dropped, drop the padding with
it — see PORT-DECISIONS "The trap that comes with the watermarks".

Run:
    python3 projects/midlakes/pages/_theme/footer/build.py
    python3 scripts/validate-page.py projects/midlakes/pages/_theme/footer/footer.json
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, SITE)
import brand as B  # noqa: E402

B.reset(0x4B000000)

if __name__ == "__main__":
    B.write(B.theme_part("Mid Lakes Footer", [B.footer_bar()], "footer"),
            "footer.json", HERE)
