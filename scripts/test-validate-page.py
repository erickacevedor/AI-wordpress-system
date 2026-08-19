#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regression tests for the validate-page.py gate.

A gate nobody tests silently stops gating. This mutates a known-good page so that
each check MUST fire, and asserts the deliberate non-firing cases stay quiet (a
padded self-contained card is correct; a padded bare layout row is not).

Usage:  python3 scripts/test-validate-page.py
Exit code: 0 = every check behaved, 1 = a check missed or fired wrongly.
Run it after touching validate-page.py or responsive-audit.py.
"""
import json, io, sys, copy, importlib.util, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "vp", os.path.join(ROOT, "scripts", "validate-page.py"))
vp = importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)

GOOD = os.path.join(ROOT, "projects", "gcreliable", "pages",
                    "ac-installation", "ac-installation.json")
OVERLONG_META = os.path.join(ROOT, "projects", "gcreliable", "pages",
                             "ductless-mini-split", "x.json")
base = json.load(io.open(GOOD, encoding="utf-8"))

def run(doc, label, expect_in, channel):
    errs, warns = vp.validate(doc)
    pool = errs if channel == "error" else warns
    hit = [x for x in pool if expect_in in x]
    print("%-38s %-7s %s  %s" % (label, channel, "FIRED " if hit else "MISSED",
                                 (hit[0][:88] if hit else "")))
    return bool(hit)

results = []

# 1. section not full-width
d = copy.deepcopy(base); d["content"][1]["settings"]["content_width"] = "boxed"
results.append(run(d, "section not full-width", "is not full-width", "error"))

# 2. section with two children / no boxed child
d = copy.deepcopy(base)
d["content"][1]["elements"].append({"id": "deadbeef", "elType": "container",
                                    "settings": {"content_width": "full"}, "elements": []})
results.append(run(d, "section with 2 child containers", "exactly ONE boxed", "error"))

# 3. boxed nested in boxed
d = copy.deepcopy(base)
box = d["content"][1]["elements"][0]
box["elements"].insert(0, {"id": "nestbox1", "elType": "container",
                           "settings": {"content_width": "boxed",
                                        "padding_mobile": {"unit": "px", "top": "1",
                                                           "right": "1", "bottom": "1",
                                                           "left": "1"}},
                           "elements": []})
results.append(run(d, "boxed nested inside boxed", "nested inside another", "error"))

# 4. image without alt
d = copy.deepcopy(base)
box = d["content"][1]["elements"][0]
box["elements"].insert(0, {"id": "noaltimg", "elType": "widget", "widgetType": "image",
                           "settings": {"image": {"url": "x.jpg", "alt": ""}},
                           "elements": []})
results.append(run(d, "image with empty alt", "without alt text", "error"))

# 5. adjacent identical bands
d = copy.deepcopy(base)
d["content"][2]["settings"]["background_background"] = "classic"
d["content"][2]["settings"]["background_color"] = "#FFFFFF"
d["content"][1]["settings"]["background_background"] = "classic"
d["content"][1]["settings"]["background_color"] = "#FFFFFF"
results.append(run(d, "two adjacent identical bands", "share the same background", "warning"))

# 6. padding on a nested bare layout row
d = copy.deepcopy(base)
box = d["content"][1]["elements"][0]
box["elements"].insert(0, {"id": "padrow01", "elType": "container",
                           "settings": {"content_width": "full", "flex_direction": "row",
                                        "flex_direction_mobile": "column",
                                        "padding": {"unit": "px", "top": "40", "right": "0",
                                                    "bottom": "40", "left": "0"}},
                           "elements": []})
results.append(run(d, "padding on bare nested row", "nested layout row/column/grid", "warning"))

# 6b. same, but WITH a background => a card => must NOT fire
d = copy.deepcopy(base)
box = d["content"][1]["elements"][0]
box["elements"].insert(0, {"id": "padcard1", "elType": "container",
                           "settings": {"content_width": "full", "flex_direction": "column",
                                        "background_background": "classic",
                                        "background_color": "#FFF",
                                        "padding": {"unit": "px", "top": "26", "right": "26",
                                                    "bottom": "26", "left": "26"}},
                           "elements": []})
errs, warns = vp.validate(d)
card_ok = not [w for w in warns if "padcard1" in w]
print("%-38s %-7s %s" % ("padded CARD (must not fire)", "warning", "OK    " if card_ok else "FALSE POSITIVE"))
results.append(card_ok)

# 7. emoji icon without mobile size (via responsive-audit delegation)
d = copy.deepcopy(base)
box = d["content"][1]["elements"][0]
box["elements"].insert(0, {"id": "emoji001", "elType": "widget", "widgetType": "heading",
                           "settings": {"title": "🔧", "header_size": "p",
                                        "typography_typography": "custom",
                                        "typography_font_size": {"unit": "px", "size": 42}},
                           "elements": []})
results.append(run(d, "emoji icon w/o mobile size", "typography_font_size_mobile", "error"))

# 8. SEO meta too long (path-based)
d = copy.deepcopy(base)
errs, warns = vp.validate(d, OVERLONG_META)
hit = [w for w in warns if "meta title" in w and "72 chars" in w]
print("%-38s %-7s %s  %s" % ("over-long meta title", "warning", "FIRED " if hit else "MISSED",
                             hit[0][:80] if hit else ""))
results.append(bool(hit))

# 9. control: the unmodified good page stays clean of errors
errs, warns = vp.validate(base, GOOD)
print("%-38s %-7s %s" % ("control: untouched good page", "error", "CLEAN " if not errs else "REGRESSION: %s" % errs))
results.append(not errs)

print("\n%d/%d negative tests behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
