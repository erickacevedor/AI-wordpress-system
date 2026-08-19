#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diff a rebuilt page against the live page it replaces.

Redesigning an existing page is half this system's job, and it carries a problem a
new page does not: the client already has something, they cannot preview the
replacement, and they need to know exactly what they are losing before they approve
it. Answering that by hand is slow and easy to get wrong -- petitt's handoff note has
a "What changed vs. the live page" section that was written out by eye.

This generates it. Both sides are reduced to a content outline -- headings, body
blocks, CTA labels and targets, image alts, section backgrounds -- and the outlines
are compared. What comes out is the paragraph you paste into the handoff.

It deliberately compares CONTENT, not markup: a rebuilt page shares no element ids
and no container structure with the original, so a structural diff would be noise.

Usage:
    python3 scripts/page-diff.py <new-page.json> <old-kit-page.json>
    python3 scripts/page-diff.py <new-page.json> --kit-page 225062
    python3 scripts/page-diff.py <new-page.json> --find        # list candidate pages

    --markdown   emit a HANDOFF-ready markdown block

Exit code: 0 always (this is a report, not a gate).
"""
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import elementor_meta
except Exception:
    elementor_meta = None


def _text(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = s.replace("&nbsp;", " ").replace("&rsquo;", "'").replace("&mdash;", "-")
    s = re.sub(r"&[a-z]+;", "", s)
    return re.sub(r"\s+", " ", s).strip()


def outline(doc):
    """Reduce a page to what a client would actually notice changing."""
    o = {"headings": [], "body": [], "ctas": [], "images": [], "bands": [],
         "widgets": {}, "sections": 0}
    content = doc.get("content") or []
    o["sections"] = len(content)

    for sec in content:
        if isinstance(sec, dict):
            s = sec.get("settings", {}) or {}
            bg = s.get("background_background")
            if bg == "gradient":
                o["bands"].append("gradient")
            elif bg == "classic":
                if (s.get("background_image") or {}).get("url"):
                    o["bands"].append("image")
                else:
                    o["bands"].append((s.get("background_color") or "?").upper())
            else:
                o["bands"].append("none")

    def walk(e):
        if isinstance(e, dict):
            s = e.get("settings", {}) or {}
            wt = e.get("widgetType")
            if wt:
                o["widgets"][wt] = o["widgets"].get(wt, 0) + 1
            if wt == "heading":
                t = _text(s.get("title"))
                if t:
                    o["headings"].append((s.get("header_size") or "h2", t))
            elif wt == "text-editor":
                t = _text(s.get("editor"))
                if t:
                    o["body"].append(t)
            elif wt == "button":
                o["ctas"].append((_text(s.get("text")), (s.get("link") or {}).get("url") or ""))
            elif wt == "image":
                img = s.get("image") or {}
                o["images"].append((img.get("alt") or "(no alt)",
                                    os.path.basename((img.get("url") or "").split("?")[0])))
            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(content)
    return o


def _norm(t):
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()


def compare(new, old):
    n, o = outline(new), outline(old)
    nh = {_norm(t): (tag, t) for tag, t in n["headings"]}
    oh = {_norm(t): (tag, t) for tag, t in o["headings"]}
    nc = {_norm(l): (l, u) for l, u in n["ctas"]}
    oc = {_norm(l): (l, u) for l, u in o["ctas"]}

    kept = sorted(set(nh) & set(oh))
    return {
        "sections": (o["sections"], n["sections"]),
        "headings_added": [nh[k] for k in sorted(set(nh) - set(oh))],
        "headings_dropped": [oh[k] for k in sorted(set(oh) - set(nh))],
        "headings_kept": [nh[k] for k in kept],
        "heading_retag": [(oh[k][0], nh[k][0], nh[k][1]) for k in kept
                          if oh[k][0] != nh[k][0]],
        "ctas_added": [nc[k] for k in sorted(set(nc) - set(oc))],
        "ctas_dropped": [oc[k] for k in sorted(set(oc) - set(nc))],
        "cta_retargeted": [(k, oc[k][1], nc[k][1]) for k in sorted(set(nc) & set(oc))
                           if oc[k][1] != nc[k][1]],
        "body": (len(o["body"]), len(n["body"])),
        "words": (sum(len(b.split()) for b in o["body"]),
                  sum(len(b.split()) for b in n["body"])),
        "images": (o["images"], n["images"]),
        "bands": (o["bands"], n["bands"]),
        "widgets_added": sorted(set(n["widgets"]) - set(o["widgets"])),
        "widgets_dropped": sorted(set(o["widgets"]) - set(n["widgets"])),
    }


def report(d, markdown=False):
    L = []
    a = L.append
    h2 = (lambda t: a("\n## %s" % t)) if markdown else (lambda t: a("\n%s" % t.upper()))
    bullet = "- " if markdown else "  - "

    a("# What changed vs. the live page" if markdown else "WHAT CHANGED VS. THE LIVE PAGE")
    a("")
    a("%sSections: %d → %d" % (bullet, d["sections"][0], d["sections"][1]))
    a("%sBody blocks: %d → %d  (%d → %d words)"
      % (bullet, d["body"][0], d["body"][1], d["words"][0], d["words"][1]))
    a("%sBand sequence now: %s" % (bullet, " → ".join(str(b) for b in d["bands"][1])))
    if d["bands"][0]:
        a("%sBand sequence was: %s" % (bullet, " → ".join(str(b) for b in d["bands"][0])))

    if d["headings_dropped"]:
        h2("Headings removed (check none of these carried ranking value)")
        for tag, t in d["headings_dropped"]:
            a("%s`%s` %s" % (bullet, tag, t))
    if d["headings_added"]:
        h2("Headings added")
        for tag, t in d["headings_added"]:
            a("%s`%s` %s" % (bullet, tag, t))
    if d["headings_kept"]:
        h2("Headings kept (%d)" % len(d["headings_kept"]))
        for tag, t in d["headings_kept"][:12]:
            a("%s`%s` %s" % (bullet, tag, t))
        if len(d["headings_kept"]) > 12:
            a("%s… and %d more" % (bullet, len(d["headings_kept"]) - 12))
    if d["heading_retag"]:
        h2("Heading level changed")
        for old, new, t in d["heading_retag"]:
            a("%s%s → %s: %s" % (bullet, old, new, t))

    if d["ctas_dropped"] or d["ctas_added"] or d["cta_retargeted"]:
        h2("Calls to action")
        for l, u in d["ctas_dropped"]:
            a("%sremoved: \"%s\" → %s" % (bullet, l, u or "(no target)"))
        for l, u in d["ctas_added"]:
            a("%sadded: \"%s\" → %s" % (bullet, l, u or "(no target)"))
        for k, ou, nu in d["cta_retargeted"]:
            a("%sre-pointed: %s → %s" % (bullet, ou or "(none)", nu or "(none)"))

    old_imgs, new_imgs = d["images"]
    if old_imgs or new_imgs:
        h2("Images")
        a("%s%d → %d" % (bullet, len(old_imgs), len(new_imgs)))
        for alt, fn in new_imgs:
            a("%snow: %s — alt: %s" % (bullet, fn or "(no file)", alt))

    if d["widgets_dropped"] or d["widgets_added"]:
        h2("Widget types")
        if d["widgets_dropped"]:
            a("%sno longer used: %s" % (bullet, ", ".join(d["widgets_dropped"])))
        if d["widgets_added"]:
            a("%snewly used: %s" % (bullet, ", ".join(d["widgets_added"])))

    a("")
    a("> Generated by scripts/page-diff.py — content outline only. Element ids and"
      if markdown else
      "Note: content outline only. Element ids and container structure are")
    a("> container structure are intentionally not compared: a rebuilt page shares"
      if markdown else
      "intentionally not compared -- a rebuild shares neither with the original.")
    if markdown:
        a("> neither with the original.")
    return "\n".join(L)


def find_candidates(site_dir, title_hint):
    facts = elementor_meta.kit_facts(site_dir) if elementor_meta else None
    if not facts:
        return []
    hint = _norm(title_hint)
    rows = []
    for pid, meta in facts["pages"].items():
        score = 0
        t = _norm(meta.get("title"))
        if hint and (hint in t or t in hint):
            score += 2
        if hint and set(hint.split()) & set(t.split()):
            score += 1
        rows.append((score, pid, meta.get("title"), meta.get("url")))
    rows.sort(reverse=True)
    return rows[:10]


def _site_dir(p):
    d = os.path.dirname(os.path.abspath(p))
    for _ in range(5):
        if os.path.isdir(os.path.join(d, "current-theme")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    new_path = args[0]
    with open(new_path, encoding="utf-8") as f:
        new_doc = json.load(f)
    site = _site_dir(new_path)

    if "--find" in sys.argv:
        rows = find_candidates(site, new_doc.get("title", ""))
        if not rows:
            print("No kit manifest to search (site has no current-theme/).")
            sys.exit(0)
        print("Candidate live pages in the kit (best match first):")
        for score, pid, title, url in rows:
            print("  %-8s %-38s %s" % (pid, (title or "")[:38], url))
        print("\nThen: python3 scripts/page-diff.py %s --kit-page <id>" % new_path)
        sys.exit(0)

    if "--kit-page" in sys.argv:
        pid = sys.argv[sys.argv.index("--kit-page") + 1]
        old_path = os.path.join(site or "", "current-theme", "content", "page", "%s.json" % pid)
    elif len(args) > 1:
        old_path = args[1]
    else:
        print("Need the live page: a second path, or --kit-page <id>, or --find")
        sys.exit(2)

    if not os.path.exists(old_path):
        print("✗ live page not found: %s" % old_path)
        sys.exit(2)
    with open(old_path, encoding="utf-8") as f:
        old_doc = json.load(f)

    print(report(compare(new_doc, old_doc), markdown="--markdown" in sys.argv))
    sys.exit(0)


if __name__ == "__main__":
    main()
