#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Elementor-kit miner — the mechanical half of onboarding.

Onboarding has to answer "what is this site's real design system?" Most of that
answer is counting, not judgement: which hex codes actually appear, on what, how
often; which font is really used; what the heading sizes cluster at; what a
representative button looks like. Doing that by grepping is slow and gives a
slightly different answer every time.

This script does the counting and hands the agent FACTS. The agent's job is then the
part that needs judgement: which colour is the CTA, is this palette real or a leftover
Hello Elementor default, what is the voice. That split is what makes onboarding
repeatable — and what makes re-onboarding a refreshed kit cheap.

Reads ONLY. Writes nothing. Never guesses: every number it reports is a count of
something that exists in the export.

Usage:
    python3 scripts/analyze-kit.py projects/<site>/current-theme
    python3 scripts/analyze-kit.py projects/<site>/current-theme --json > kit-facts.json

Output: a human-readable report, or --json for the raw findings to feed a build.
Exit code: 0 = analysed, 2 = kit not found / unreadable.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")

# Hello Elementor / Elementor factory defaults. Their presence in site-settings.json
# is the classic false positive: the globals look populated but nobody ever set them.
HELLO_DEFAULTS = {
    "#6EC1E4", "#54595F", "#7A7A7A", "#61CE70", "#4054B2", "#23A455",
    "#000", "#FFF",
}
HELLO_FONTS = {"Noto Sans Coptic", "Roboto", "Roboto Slab"}

# Pro/third-party widget classification lives in elementor_meta so the lists cannot
# drift apart between this reader and the gate.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elementor_meta import PRO_WIDGETS  # noqa: E402


def _iter_json(root, *parts):
    d = os.path.join(root, *parts)
    if not os.path.isdir(d):
        return
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(d, name)
        try:
            with open(path, encoding="utf-8") as f:
                yield path, json.load(f)
        except Exception as ex:
            print("  ! skipped %s (%s)" % (path, ex), file=sys.stderr)


def _walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for v in node.values():
            _walk(v, fn)
    elif isinstance(node, list):
        for x in node:
            _walk(x, fn)


def analyze(kit_root):
    facts = {
        "kit": kit_root,
        "counts": {},
        "colors": [],
        "color_roles": {},
        "fonts": [],
        "type_scale": {},
        "button": None,
        "section_rhythm": [],
        "widgets": [],
        "pro_widgets": [],
        "templates": [],
        "globals": {},
        "gotchas": {},
    }

    colors = Counter()
    color_ctx = defaultdict(Counter)   # hex -> which setting keys it appeared in
    fonts = Counter()
    sizes = defaultdict(list)          # header_size -> [font_size, ...]
    widgets = Counter()
    buttons = []
    gates = [0]
    localhost = [0]
    rhythms = []

    def visit(el):
        s = el.get("settings")
        if not isinstance(s, dict):
            return
        wt = el.get("widgetType")
        if wt:
            widgets[wt] += 1
        if "display_condition_list" in s:
            gates[0] += 1
        for k, v in s.items():
            if isinstance(v, str):
                if "localhost" in v or "127.0.0.1" in v:
                    localhost[0] += 1
                for hx in HEX.findall(v):
                    colors[hx.upper()] += 1
                    color_ctx[hx.upper()][k] += 1
                if k.endswith("font_family"):
                    fonts[v] += 1
            elif isinstance(v, dict) and "url" in v:
                u = v.get("url") or ""
                if "localhost" in u or "127.0.0.1" in u:
                    localhost[0] += 1
        if wt == "heading":
            tag = s.get("header_size") or "h2"
            fs = (s.get("typography_font_size") or {})
            if fs.get("size"):
                sizes[tag].append((fs.get("size"), fs.get("unit") or "px"))
        if wt == "button":
            buttons.append(s)

    n_pages = n_templates = 0
    for path, doc in _iter_json(kit_root, "content", "page"):
        n_pages += 1
        _walk(doc, visit)
        elements = doc.get("content") if isinstance(doc, dict) else None
        if isinstance(elements, list):
            seq = []
            for sec in elements:
                if not isinstance(sec, dict):
                    continue
                ss = sec.get("settings", {}) or {}
                bg = ss.get("background_background")
                if bg == "gradient":
                    seq.append("gradient")
                elif bg == "classic":
                    seq.append((ss.get("background_color") or "image/none").upper())
                else:
                    seq.append("none")
            if seq:
                rhythms.append({"page": os.path.basename(path), "sequence": seq})

    for path, doc in _iter_json(kit_root, "content", "post"):
        _walk(doc, visit)

    for path, doc in _iter_json(kit_root, "templates"):
        n_templates += 1
        _walk(doc, visit)
        facts["templates"].append({
            "file": os.path.basename(path),
            "title": (doc.get("title") if isinstance(doc, dict) else None) or "?",
            "type": (doc.get("type") if isinstance(doc, dict) else None) or "?",
        })

    # ---- globals: real, or still the factory defaults? --------------------
    ss_path = os.path.join(kit_root, "site-settings.json")
    if os.path.exists(ss_path):
        try:
            with open(ss_path, encoding="utf-8") as f:
                ss = json.load(f)
            sysc = (ss.get("settings", {}) or {}).get("system_colors", []) or []
            custom = (ss.get("settings", {}) or {}).get("custom_colors", []) or []
            sys_hex = [(c.get("color") or "").upper() for c in sysc if isinstance(c, dict)]
            default_hits = [h for h in sys_hex if h in {d.upper() for d in HELLO_DEFAULTS}]
            font_vals = [v for k, v in (ss.get("settings", {}) or {}).items()
                         if k.endswith("font_family") and isinstance(v, str)]
            facts["globals"] = {
                "system_colors": sys_hex,
                "custom_color_count": len(custom),
                "custom_color_ids": [c.get("_id") for c in custom if isinstance(c, dict)],
                "duplicate_custom_ids": [i for i, n in Counter(
                    [c.get("_id") for c in custom if isinstance(c, dict)]).items() if n > 1],
                "looks_like_hello_defaults": len(default_hits) >= 2,
                "default_hits": default_hits,
                "global_fonts": sorted(set(font_vals)),
                "fonts_look_default": bool(set(font_vals) & HELLO_FONTS),
            }
        except Exception as ex:
            facts["globals"] = {"error": str(ex)}

    # ---- assemble ---------------------------------------------------------
    facts["counts"] = {
        "pages": n_pages, "templates": n_templates,
        "distinct_colors": len(colors), "distinct_fonts": len(fonts),
        "widget_instances": sum(widgets.values()),
    }
    facts["colors"] = [
        {"hex": h, "count": n,
         "used_on": [k for k, _ in color_ctx[h].most_common(4)]}
        for h, n in colors.most_common(18)
    ]
    facts["color_roles"] = _infer_roles(color_ctx, colors)
    facts["fonts"] = [{"family": f, "count": n} for f, n in fonts.most_common(8)]
    facts["type_scale"] = {
        tag: _cluster(vals) for tag, vals in sorted(sizes.items())
    }
    facts["button"] = _representative_button(buttons)
    facts["section_rhythm"] = rhythms[:12]
    facts["widgets"] = [{"type": w, "count": n} for w, n in widgets.most_common(24)]
    facts["pro_widgets"] = [{"type": w, "count": widgets[w]}
                            for w in sorted(widgets) if w in PRO_WIDGETS]
    facts["gotchas"] = {
        "display_condition_list": gates[0],
        "localhost_urls": localhost[0],
    }
    return facts


def _infer_roles(color_ctx, colors):
    """Suggest roles from WHERE a colour is used. Suggestions only -- the call between
    'brand blue' and 'a blue that happens to be frequent' stays with the agent."""
    roles = {}

    def top_for(pred, limit=3):
        scored = Counter()
        for hx, ctxs in color_ctx.items():
            for k, n in ctxs.items():
                if pred(k):
                    scored[hx] += n
        return [{"hex": h, "count": n} for h, n in scored.most_common(limit)]

    roles["section_backgrounds"] = top_for(lambda k: k == "background_color")
    roles["button_fill"] = top_for(lambda k: k.startswith("button_background")
                                   or k == "background_color" and False)
    roles["text"] = top_for(lambda k: k in ("title_color", "text_color", "color"))
    roles["borders"] = top_for(lambda k: "border_color" in k)
    roles["most_frequent_overall"] = [{"hex": h, "count": n} for h, n in colors.most_common(3)]
    return roles


def _cluster(vals):
    """Heading sizes cluster around a few real values -- report those, with counts,
    rather than a meaningless average."""
    c = Counter(vals)
    out = [{"size": s, "unit": u, "count": n} for (s, u), n in c.most_common(6)]
    return {"samples": len(vals), "common": out}


def _representative_button(buttons):
    """The most-repeated button settings signature is the site's real CTA spec."""
    if not buttons:
        return None
    keys = ("background_color", "button_text_color", "border_radius", "text_padding",
            "typography_font_weight", "hover_animation", "button_background_hover_color",
            "button_hover_border_color", "size", "selected_icon")
    sig = Counter()
    by_sig = {}
    for b in buttons:
        s = tuple((k, json.dumps(b.get(k), sort_keys=True)) for k in keys if k in b)
        sig[s] += 1
        by_sig.setdefault(s, b)
    best, n = sig.most_common(1)[0]
    rep = by_sig[best]
    return {
        "instances_of_this_spec": n,
        "total_buttons": len(buttons),
        "settings": {k: rep.get(k) for k in keys if k in rep},
        "hover_convention": ("shrink/animation" if rep.get("hover_animation")
                             else "colour-only"),
    }


# ------------------------------------------------------------------ report
def report(f):
    out = []
    a = out.append
    c = f["counts"]
    a("Kit: %s" % f["kit"])
    a("  %d pages · %d templates · %d widget instances · %d distinct colours · %d fonts"
      % (c["pages"], c["templates"], c["widget_instances"],
         c["distinct_colors"], c["distinct_fonts"]))

    g = f.get("globals") or {}
    if g and "error" not in g:
        a("")
        a("GLOBALS (site-settings.json)")
        verdict = ("LOOK LIKE HELLO DEFAULTS -- mine the widgets, do not trust these"
                   if g.get("looks_like_hello_defaults") else
                   "look customised -- still verify against the widget styling")
        a("  system colours: %s" % ", ".join(g.get("system_colors") or []) or "  (none)")
        a("  verdict: %s" % verdict)
        if g.get("global_fonts"):
            a("  global fonts: %s%s" % (", ".join(g["global_fonts"]),
                                        "  <- factory default" if g.get("fonts_look_default") else ""))
        if g.get("duplicate_custom_ids"):
            a("  ⚠ duplicate custom_colors ids: %s  (two colour sets sharing ids -- "
              "inline the hexes rather than pointing at a global)"
              % ", ".join(str(x) for x in g["duplicate_custom_ids"]))

    a("")
    a("PALETTE (ranked by real usage)")
    for row in f["colors"][:12]:
        a("  %-9s %5d   on: %s" % (row["hex"], row["count"], ", ".join(row["used_on"])))

    r = f.get("color_roles") or {}
    if r:
        a("")
        a("ROLE SUGGESTIONS (from where each colour is used -- confirm, don't adopt blindly)")
        for role, items in r.items():
            if items:
                a("  %-22s %s" % (role, ", ".join("%s(%d)" % (i["hex"], i["count"]) for i in items)))

    a("")
    a("FONTS")
    for row in f["fonts"]:
        a("  %-28s %d" % (row["family"], row["count"]))

    a("")
    a("TYPE SCALE (heading sizes that actually occur)")
    for tag, d in f["type_scale"].items():
        common = " · ".join("%s%s×%d" % (x["size"], x["unit"], x["count"]) for x in d["common"])
        a("  %-4s %3d sized headings:  %s" % (tag, d["samples"], common))

    b = f.get("button")
    if b:
        a("")
        a("BUTTON (most-repeated spec: %d of %d buttons)"
          % (b["instances_of_this_spec"], b["total_buttons"]))
        a("  hover convention: %s" % b["hover_convention"])
        for k, v in b["settings"].items():
            a("    %-30s %s" % (k, json.dumps(v)[:88]))

    if f["section_rhythm"]:
        a("")
        a("SECTION RHYTHM (top-level backgrounds, first pages)")
        for row in f["section_rhythm"][:6]:
            a("  %-22s %s" % (row["page"], " → ".join(str(x) for x in row["sequence"][:10])))

    a("")
    a("WIDGET MIX")
    a("  " + ", ".join("%s(%d)" % (w["type"], w["count"]) for w in f["widgets"][:14]))

    gz = f["gotchas"]
    a("")
    a("GOTCHAS")
    a("  display_condition_list gates: %d%s" % (gz["display_condition_list"],
      "   <- drop these when building; they hide content on import" if gz["display_condition_list"] else ""))
    a("  localhost/127.0.0.1 URLs: %d%s" % (gz["localhost_urls"],
      "   <- rewrite internal links root-relative" if gz["localhost_urls"] else ""))

    if f["templates"]:
        a("")
        a("TEMPLATES (reusable parts)")
        for t in f["templates"][:20]:
            a("  %-18s %-12s %s" % (t["file"], t["type"], t["title"]))
        if len(f["templates"]) > 20:
            a("  ... and %d more" % (len(f["templates"]) - 20))

    a("")
    a("Next: the counting is done -- the judgement is not. Decide which colour is the")
    a("CTA, whether the palette is real, and what the voice is, then write tokens.json,")
    a("KIT-ANALYSIS.md and the <site>-* skills (see skills/elementor-kit-onboarding).")
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    kit = args[0].rstrip("/\\")
    if not os.path.isdir(kit):
        print("✗ Not a directory: %s" % kit)
        sys.exit(2)
    if not os.path.isdir(os.path.join(kit, "content")) and not os.path.isdir(os.path.join(kit, "templates")):
        print("✗ %s has no content/ or templates/ — is this an unzipped Elementor kit?" % kit)
        sys.exit(2)
    facts = analyze(kit)
    if as_json:
        print(json.dumps(facts, indent=2, ensure_ascii=False))
    else:
        print(report(facts))
    sys.exit(0)


if __name__ == "__main__":
    main()
