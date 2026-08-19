#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WCAG contrast audit for a built Elementor page.

Why this exists: the page ships as a file to someone else's install, so nobody here
will ever squint at the rendered result. Unreadable text on a brand band is exactly
the defect that survives a JSON review and lands on a live client site -- and it is
pure arithmetic to catch.

Walks the tree carrying the nearest ancestor background down to each text widget,
then scores the pair against WCAG 2.1 AA:

  - normal text          needs >= 4.5:1
  - large text           needs >= 3.0:1   (>= 24px, or >= 18.66px at weight >= 700)

Only pairs where BOTH colours are explicit in the JSON are scored. Two things are
deliberately treated as unknowable and skipped rather than guessed:

  - a colour inherited from a global or a stylesheet
  - anything under a container carrying a CSS class or a background image, because
    the real background is then painted by the site's stylesheet or a photo

That second rule matters: the builder's `classes=` escape hatch exists precisely for
backgrounds Elementor cannot express, so scoring against the last colour seen in the
JSON reports confident nonsense (white-on-cream for text that renders white-on-navy).
A clean report therefore means "nothing provably wrong", not "everything checked" --
the counts below tell you the coverage.

Gradient backgrounds are scored against BOTH stops: text has to survive the whole
sweep, and the worst end is the one that fails on someone's screen.

Usage:  python3 scripts/contrast-audit.py path/to/page.json [--all]
        --all also lists the pairs that pass, and the ones it had to skip.
Exit code: 0 = no failures found, 1 = at least one pair below AA.
"""
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HEX3 = re.compile(r"^#([0-9A-Fa-f]{3})$")
HEX6 = re.compile(r"^#([0-9A-Fa-f]{6})$")

AA_NORMAL = 4.5
AA_LARGE = 3.0


def _rgb(hex_str):
    if not isinstance(hex_str, str):
        return None
    s = hex_str.strip()
    m = HEX3.match(s)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = HEX6.match(s)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return None


def _luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_hex, bg_hex):
    fg, bg = _rgb(fg_hex), _rgb(bg_hex)
    if not fg or not bg:
        return None
    l1, l2 = _luminance(fg), _luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _px_size(settings, key="typography_font_size"):
    """Return an approximate px size for the large-text threshold. rem/em are
    resolved against a 16px root -- close enough to classify, and the classification
    only shifts the bar between 4.5 and 3.0."""
    fs = settings.get(key)
    if not isinstance(fs, dict) or not fs.get("size"):
        return None
    try:
        size = float(fs["size"])
    except (TypeError, ValueError):
        return None
    unit = (fs.get("unit") or "px").lower()
    if unit in ("rem", "em"):
        return size * 16.0
    if unit == "%":
        return 16.0 * size / 100.0
    return size


def _is_large(settings):
    # Elementor's button `size` control (xs..xl) scales the label, so an xl button is
    # large text even when the JSON carries no explicit font size.
    if str(settings.get("size") or "") in ("lg", "xl"):
        return True
    size = _px_size(settings)
    if size is None:
        return False
    weight = str(settings.get("typography_font_weight") or "")
    bold = weight in ("bold", "600", "700", "800", "900")
    return size >= 24.0 or (bold and size >= 18.66)


def _backgrounds(settings):
    """The background(s) this container paints, as (label, hex) pairs. A gradient
    contributes both stops; an image contributes nothing knowable."""
    bg = settings.get("background_background")
    if bg == "classic":
        if (settings.get("background_image") or {}).get("url"):
            return []                      # a photo: contrast is not computable
        c = settings.get("background_color")
        return [("bg", c)] if c else []
    if bg == "gradient":
        out = []
        if settings.get("background_color"):
            out.append(("gradient-from", settings["background_color"]))
        if settings.get("background_color_b"):
            out.append(("gradient-to", settings["background_color_b"]))
        return out
    return []


def _text_color(el):
    s = el.get("settings") or {}
    wt = el.get("widgetType")
    if wt == "heading":
        return s.get("title_color")
    if wt == "text-editor":
        return s.get("text_color")
    if wt == "button":
        return s.get("button_text_color")
    if wt == "icon-list":
        return s.get("text_color")
    return s.get("title_color") or s.get("text_color")


def _label(el):
    s = el.get("settings") or {}
    txt = s.get("title") or s.get("text") or ""
    if not txt:
        editor = s.get("editor") or ""
        txt = re.sub(r"<[^>]+>", "", editor)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:46]


def audit(doc, include_passes=False):
    """Returns (failures, passes, skipped_count)."""
    failures, passes = [], []
    skipped = [0]
    styled = [0]      # containers whose background the stylesheet owns
    content = doc.get("content", doc)

    def walk(node, bgs):
        if isinstance(node, dict):
            s = node.get("settings") or {}
            if node.get("elType") == "container":
                own = _backgrounds(s)
                # Two ways a background stops being knowable from the JSON:
                #   - a photo behind the text
                #   - a CSS class, which may paint it from the site's stylesheet
                #     (containers use `css_classes`, widgets `_css_classes`)
                has_image = (s.get("background_background") == "classic"
                             and (s.get("background_image") or {}).get("url"))
                has_class = bool((s.get("css_classes") or s.get("_css_classes") or "").strip())
                if has_image or has_class:
                    if has_class:
                        styled[0] += 1
                    nxt = []
                elif own:
                    nxt = own
                else:
                    nxt = bgs
                for kid in (node.get("elements") or []):
                    walk(kid, nxt)
                return

            wt = node.get("widgetType")
            if wt in ("heading", "text-editor", "button", "icon-list"):
                # A button paints its own fill, so its label sits on THAT, not on the
                # band behind it. Scoring it against the ancestor background reports a
                # white-on-white failure for a perfectly legible white-on-red button.
                if wt == "button":
                    own = (s.get("background_color")
                           or s.get("button_background_color"))
                    bgs = [("button fill", own)] if own else bgs
                fg = _text_color(node)
                if not fg or not _rgb(fg):
                    skipped[0] += 1
                elif not bgs:
                    skipped[0] += 1
                else:
                    large = _is_large(s)
                    need = AA_LARGE if large else AA_NORMAL
                    for label, bg in bgs:
                        r = ratio(fg, bg)
                        if r is None:
                            skipped[0] += 1
                            continue
                        row = {
                            "id": node.get("id", "?"), "widget": wt,
                            "fg": fg, "bg": bg, "on": label,
                            "ratio": round(r, 2), "need": need,
                            "large": large, "text": _label(node),
                        }
                        (passes if r >= need else failures).append(row)

            for kid in (node.get("elements") or []):
                walk(kid, bgs)
            return

        if isinstance(node, list):
            for x in node:
                walk(x, bgs)

    walk(content, [])
    return failures, passes, skipped[0], styled[0]


def format_row(r):
    return ("[%s %s] %.2f:1 (needs %.1f) — %s on %s%s — \"%s\""
            % (r["widget"], r["id"], r["ratio"], r["need"], r["fg"], r["bg"],
               " " + r["on"] if r["on"] != "bg" else "", r["text"]))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all" in sys.argv
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    with open(args[0], encoding="utf-8") as f:
        doc = json.load(f)
    failures, passes, skipped, styled = audit(doc)
    coverage = ("%d pair(s) checked, %d skipped as inherited/unknowable%s"
                % (len(passes) + len(failures), skipped,
                   ", %d block(s) styled by the stylesheet" % styled if styled else ""))

    if show_all:
        for r in passes:
            print("   ok  " + format_row(r))
    if not failures:
        print("✅ Contrast audit: no AA failures (%s)." % coverage)
        sys.exit(0)
    print("⚠️  Contrast audit: %d pair(s) below WCAG AA (%s):" % (len(failures), coverage))
    for r in failures:
        print("   - " + format_row(r))
    sys.exit(1)


if __name__ == "__main__":
    main()
