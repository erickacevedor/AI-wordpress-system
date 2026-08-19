#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify that an imported page actually rendered what the JSON promised.

The gate proves a page is structurally valid. It cannot prove Elementor agreed to
render it: a widget the install does not have, a payload mangled on the way into post
meta, a theme that swallows the content -- all of those import "successfully" and
produce a page that is quietly wrong. The only way to know is to fetch the rendered
HTML and count.

Point it at a sandbox install after importing (see scripts/import-page.php), or at the
live URL on the rare occasion the target is reachable.

Compares, JSON vs rendered HTML:
  - container count      (Elementor emits one .e-con per container)
  - headings             every H1/H2/H3 title in the JSON must appear in the HTML
  - CTA labels + targets
  - image sources
  - placeholder/empty widgets that rendered as nothing

Dependency-free: uses urllib, so it runs anywhere Python does.

Usage:
    python3 scripts/verify-render.py <page.json> <url>
    python3 scripts/verify-render.py <page.json> --html rendered.html

Exit code: 0 = everything the JSON promised is present, 1 = something is missing.
"""
import html as _html
import json
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "verify-render/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        charset = r.headers.get_content_charset() or "utf-8"
        return r.getcode(), raw.decode(charset, errors="replace")


def strip_tags(s):
    s = re.sub(r"<script\b.*?</script>", " ", s or "", flags=re.S | re.I)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", _html.unescape(s or "").lower()).strip()


def expectations(doc):
    exp = {"containers": 0, "headings": [], "ctas": [], "images": [], "widgets": {}}

    def walk(e):
        if isinstance(e, dict):
            s = e.get("settings", {}) or {}
            if e.get("elType") == "container":
                exp["containers"] += 1
            wt = e.get("widgetType")
            if wt:
                exp["widgets"][wt] = exp["widgets"].get(wt, 0) + 1
            if wt == "heading":
                t = strip_tags(s.get("title") or "")
                if t and s.get("header_size") in ("h1", "h2", "h3"):
                    exp["headings"].append(t)
            elif wt == "button":
                exp["ctas"].append((strip_tags(s.get("text") or ""),
                                    (s.get("link") or {}).get("url") or ""))
            elif wt == "image":
                url = ((s.get("image") or {}).get("url") or "").split("/")[-1].split("?")[0]
                if url:
                    exp["images"].append(url)
            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(doc.get("content") or [])
    return exp


def verify(doc, html):
    exp = expectations(doc)
    text = norm(strip_tags(html))
    problems, notes = [], []

    rendered_cons = len(re.findall(r'class="[^"]*\be-con\b', html))
    notes.append("containers: %d in JSON, %d rendered" % (exp["containers"], rendered_cons))
    if rendered_cons == 0:
        problems.append("no .e-con containers in the rendered HTML — Elementor rendered "
                        "nothing. Classic causes: _elementor_data stored without "
                        "wp_slash(), or the page template is not an Elementor one.")
    elif rendered_cons < exp["containers"] * 0.8:
        problems.append("only %d of %d containers rendered (%.0f%%) — part of the page "
                        "was dropped" % (rendered_cons, exp["containers"],
                                         100.0 * rendered_cons / max(exp["containers"], 1)))

    missing_h = [h for h in exp["headings"] if norm(h) and norm(h) not in text]
    if missing_h:
        problems.append("%d heading(s) missing from the render: %s"
                        % (len(missing_h), "; ".join(h[:40] for h in missing_h[:5])))

    missing_cta = [c for c, u in exp["ctas"] if norm(c) and norm(c) not in text]
    if missing_cta:
        problems.append("%d CTA label(s) missing: %s"
                        % (len(missing_cta), "; ".join(missing_cta[:5])))

    missing_href = [u for _c, u in exp["ctas"]
                    if u and u.startswith("/") and ('href="%s"' % u) not in html
                    and ('href="%s"' % u.rstrip("/")) not in html]
    if missing_href:
        notes.append("CTA targets not found verbatim (may be rewritten to absolute "
                     "URLs by WordPress): %s" % ", ".join(sorted(set(missing_href))[:5]))

    missing_img = [i for i in exp["images"] if i not in html]
    if missing_img:
        problems.append("%d image(s) not referenced in the render: %s"
                        % (len(missing_img), ", ".join(missing_img[:4])))

    empties = len(re.findall(r'class="[^"]*elementor-widget-empty', html))
    if empties:
        problems.append("%d widget(s) rendered EMPTY — usually a widget whose plugin is "
                        "missing on this install (check the gate's deps warnings)" % empties)

    notes.append("headings checked: %d · CTAs: %d · images: %d"
                 % (len(exp["headings"]), len(exp["ctas"]), len(exp["images"])))
    return problems, notes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    try:
        with open(args[0], encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        print("✗ page JSON not found: %s" % args[0])
        sys.exit(2)
    except ValueError as ex:
        print("✗ not valid JSON: %s (%s)" % (args[0], ex))
        sys.exit(2)

    if "--html" in sys.argv:
        path = sys.argv[sys.argv.index("--html") + 1]
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                html = f.read()
        except FileNotFoundError:
            print("✗ rendered HTML not found: %s" % path)
            print("  save the page first, e.g.  curl -s <url> -o rendered.html")
            sys.exit(2)
        source = path
    else:
        if len(args) < 2:
            print("Need a URL (or --html <file>).")
            sys.exit(2)
        url = args[1]
        try:
            code, html = fetch(url)
        except Exception as ex:
            print("✗ could not fetch %s (%s)" % (url, ex))
            print("  is the sandbox running? Local/Laragon must be started.")
            sys.exit(2)
        if code != 200:
            print("✗ %s returned HTTP %d" % (url, code))
            sys.exit(1)
        source = url

    problems, notes = verify(doc, html)
    for n in notes:
        print("   · " + n)
    if not problems:
        print("✅ verify-render: %s matches the built JSON." % source)
        sys.exit(0)
    print("❌ verify-render: %d problem(s):" % len(problems))
    for p in problems:
        print("   - " + p)
    sys.exit(1)


if __name__ == "__main__":
    main()
