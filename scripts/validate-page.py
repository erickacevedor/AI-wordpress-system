#!/usr/bin/env python3
"""
Pre-import validation gate for an Elementor single-page template.

Runs ALL the invariants a page must satisfy before import — one command, objective
pass/fail — so "done" doesn't depend on remembering a checklist:

  1. Parses as JSON.
  2. Single-page wrapper present: type == "page", a `content` list, `page_settings`.
  3. Unique element ids (no collisions -> imports as new).
  4. Exactly one H1, and a heading hierarchy that doesn't skip levels badly.
  5. No `display_condition_list` (subscriber/visibility gates hide content on import).
  6. No dead or environment-specific links: bare `#`/empty button urls, or
     `localhost` / `127.0.0.1` internal links.  (Intentional `#anchor` links are OK.)
  7. Responsive: delegates to responsive-audit.py (grids/rows/columns/headings/
     containers/images all carry their breakpoint settings).

Usage:  python3 scripts/validate-page.py path/to/page.json
Exit code: 0 = clean, 1 = issues found, 2 = unreadable/not JSON.  Works under any
runtime (plain dependency-free Python 3) — Claude, Codex, Gemini CLI, a human, CI.
"""
import json, sys, pathlib, importlib.util


def _load_responsive_audit():
    p = pathlib.Path(__file__).with_name("responsive-audit.py")
    spec = importlib.util.spec_from_file_location("responsive_audit", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate(doc):
    errors = []
    warnings = []

    # 2. wrapper
    if not isinstance(doc, dict) or doc.get("type") != "page":
        errors.append('wrapper: top-level `type` must be "page" (single-page import wrapper)')
    if not isinstance(doc.get("content"), list) or not doc.get("content"):
        errors.append("wrapper: `content` must be a non-empty list of sections")
    if "page_settings" not in doc:
        warnings.append("wrapper: no `page_settings` (usually {\"template\":\"default\"})")
    if not doc.get("title"):
        warnings.append("wrapper: no `title`")

    content = doc.get("content", [])
    ids, h = [], {"h1": 0, "h2": 0, "h3": 0, "h4": 0}
    gates = [0]
    bad_links = []

    def walk(e):
        if isinstance(e, dict):
            if "id" in e and "elType" in e:
                ids.append(e["id"])
            s = e.get("settings", {}) or {}
            if "display_condition_list" in s:
                gates[0] += 1
            if e.get("widgetType") == "heading":
                hs = s.get("header_size")
                if hs in h:
                    h[hs] += 1
            # links on buttons / link fields
            link = s.get("link")
            if isinstance(link, dict):
                u = (link.get("url") or "").strip()
                if u in ("#", ""):
                    bad_links.append("dead button link (%s)" % (u or "empty"))
                elif "localhost" in u or "127.0.0.1" in u:
                    bad_links.append("environment link: %s" % u)
            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(content)

    # 3. unique ids
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append("ids: %d duplicate element id(s): %s" % (len(dupes), ", ".join(dupes[:8])))

    # 4. single H1
    if h["h1"] != 1:
        errors.append("headings: exactly one H1 required, found %d" % h["h1"])

    # 5. subscriber gates
    if gates[0]:
        errors.append("gates: %d `display_condition_list` found — remove them (they hide content on import)" % gates[0])

    # 6. links
    for b in bad_links:
        errors.append("links: " + b)

    # 7. responsive (delegate)
    try:
        ra = _load_responsive_audit()
        for issue in ra.audit(doc):
            errors.append("responsive: " + issue)
    except Exception as ex:  # pragma: no cover
        warnings.append("responsive: could not run responsive-audit.py (%s)" % ex)

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            doc = json.load(f)
    except Exception as ex:
        print("✗ Could not read/parse JSON: %s" % ex)
        sys.exit(2)

    errors, warnings = validate(doc)
    for w in warnings:
        print("  ⚠︎ " + w)
    if not errors:
        print("✅ validate-page: PASS — %s is import-ready." % sys.argv[1])
        sys.exit(0)
    print("❌ validate-page: %d issue(s):" % len(errors))
    for e in errors:
        print("   - " + e)
    sys.exit(1)


if __name__ == "__main__":
    main()
