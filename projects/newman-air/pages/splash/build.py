#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Newman Air: temporary splash page for newmanair.com (ClickUp 86bcjyqgx).

One full-screen section, Elementor Canvas template (no theme header, footer or
menu), no links, per the brief. Kit-native: native widgets only, no custom CSS,
no html widgets, so the core pages can replace it at launch with nothing to undo.

Colours are hex, not __globals__: the new Flywheel install has no Newman Air kit
yet, and a global reference on a default kit would paint the page in Elementor's
stock colours. The tokens map to the four system globals for the core-page build.

Source brief: source.md
Run:  python projects/newman-air/pages/splash/build.py
Then: python scripts/validate-page.py projects/newman-air/pages/splash/splash.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))           # pages/<slug> -> projects/<site>
ROOT = HERE
while not os.path.exists(os.path.join(ROOT, "AGENTS.md")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import elementor_builder as E                            # noqa: E402

T = json.load(open(os.path.join(SITE, "tokens.json"), encoding="utf-8"))
C = {k: v["hex"] for k, v in T["colors"].items()}
F, TS, PH = T["fonts"], T["type_scale"], T["phone"]

# Where the logo is fetched from on import (Elementor sideloads it into the Media
# Library). Upload pages/splash/newman-air-logo-horiz.png there before importing.
# On a site where the logo is already in the Media Library, point at it instead:
#   NEWMAN_LOGO_URL=<attachment url> NEWMAN_LOGO_ID=<attachment id> python build.py
LOGO_URL = os.environ.get("NEWMAN_LOGO_URL",
                          "https://explorehvac.com/web/newmanair/assets/newman-air-logo-horiz.png")
LOGO_ID = os.environ.get("NEWMAN_LOGO_ID", "")

E.reset_ids(0x4E000000)


def eyebrow(txt, color):
    s = TS["eyebrow"]
    return E.heading(txt, "p", color=color, font=F["heading"], size=s["size"],
                     weight=s["weight"], mobile=13, transform=s["transform"],
                     ls=s["ls"], lh=1.4, align="center")


def body(html, color, size, mobile=None, lh=1.6, align="center"):
    return E.text(html, color=color, font=F["body"], size=size, mobile=mobile,
                  lh=lh, align=align)


def logo():
    return E.widget("image", {
        "image": {"url": LOGO_URL, "id": LOGO_ID, "size": "", "alt": "Newman Air",
                  "source": "library"},
        "image_size": "full",
        "align": "center",
        "width": {"unit": "px", "size": 460, "sizes": []},
        "width_tablet": {"unit": "px", "size": 380, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
    })


def contact_card(label, value, size, mobile):
    """Cream card on the dark band. Plain text by brief (no tel:/mailto: links)."""
    return E.card([
        eyebrow(label, C["deep_teal"]),
        E.heading(value, "p", color=C["navy"], font=F["heading"], size=size,
                  weight="800", mobile=mobile, lh=1.15, align="center"),
    ], bg=C["cream"], radius=T["radii"]["radius"], pad=26, gap=6)


h1 = TS["h1"]
hero = E.section({
    **E.gradient_bg(T["bands"]["hero_gradient"]["from"], T["bands"]["hero_gradient"]["to"],
                    angle=T["bands"]["hero_gradient"]["angle"]),
    "min_height": {"unit": "vh", "size": 100, "sizes": []},
    "flex_justify_content": "center",
    "border_border": "solid",
    "border_width": {"unit": "px", "top": "6", "right": "0", "bottom": "0", "left": "0",
                     "isLinked": False},
    "border_color": C["orange"],
    "_box": {"flex_align_items": "center",
             "flex_gap": {"unit": "px", "size": 20, "column": "20", "row": "20"}},
}, [
    logo(),
    eyebrow("Formerly Best in Show Heating &amp; Cooling", C["orange"]),
    E.heading("Our New Website Is on the Way", "h1", color=C["cream"], font=F["heading"],
              size=h1["size"], tablet=h1["tablet"], mobile=h1["mobile"],
              weight=h1["weight"], lh=h1["lh"], align="center"),
    body("<p>Best in Show Heating &amp; Cooling is now Newman Air. Same locally owned, "
         "family-operated team, same heating and air conditioning service across the "
         "Tri-Cities, TN since 1994. While we finish our new website, give us a call and "
         "we&rsquo;ll take care of you.</p>",
         C["cream"], TS["lead"]["size"], mobile=TS["lead"]["mobile"]),
    E.grid([
        contact_card("Call us", PH["display"], 32, 26),
        contact_card("Email us", T["email"], 21, 18),
    ], cols=2, tablet=2, mobile=1, gap=20),
    body("<p>Licensed, bonded &amp; insured &middot; &copy; 2026 Newman Air</p>",
         C["mist"], TS["small"]["size"], mobile=13),
], content_width=960, pad=(56, 20, 56, 20), pad_mobile=(44, 16, 44, 16))

doc = E.wrap_page("Newman Air", [hero],
                  {"template": "elementor_canvas", "hide_title": "yes"})
out = os.path.join(HERE, "splash.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(doc, fh, ensure_ascii=False, indent=1)
print("wrote %s" % out)
