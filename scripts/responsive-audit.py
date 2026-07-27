#!/usr/bin/env python3
"""
Responsive audit for an Elementor single-page template (the {version,title,type,content,...} JSON).

Walks the tree and flags any element missing its per-breakpoint responsive setting, per the
checklist in docs/Publishing-QA-Checklist.md §5:

  - grid containers missing tablet / mobile column counts
  - multi-column flex rows not set to stack on mobile
  - %-width columns without width_mobile (100%)
  - H1 / H2 headings without a mobile font size (globals-only headings do NOT shrink)
  - boxed content containers without padding_mobile
  - fixed-height images without height_mobile

Usage:  python3 scripts/responsive-audit.py path/to/page.json
Exit code 0 = clean, 1 = issues found (handy in a pre-import gate).
"""
import json, sys


def audit(doc):
    issues = []
    content = doc.get("content", doc)  # accept a raw element list too

    def walk(e):
        if isinstance(e, dict):
            s = e.get("settings", {}) or {}
            et, wt = e.get("elType"), e.get("widgetType")
            eid = e.get("id", "?")

            if s.get("container_type") == "grid":
                if not s.get("grid_columns_grid_tablet", {}).get("size"):
                    issues.append(f"[grid {eid}] missing grid_columns_grid_tablet")
                if not s.get("grid_columns_grid_mobile", {}).get("size"):
                    issues.append(f"[grid {eid}] missing grid_columns_grid_mobile")

            if s.get("flex_direction") in ("row", "row-reverse"):
                if s.get("flex_direction_mobile") not in ("column", "column-reverse"):
                    issues.append(f"[row {eid}] flex row does not stack (set flex_direction_mobile: column)")

            if et == "container" and isinstance(s.get("width"), dict) and s["width"].get("unit") == "%":
                if s.get("width_mobile", {}).get("size") != 100:
                    issues.append(f"[column {eid}] %-width column missing width_mobile: 100")

            if s.get("content_width") == "boxed" and "padding_mobile" not in s:
                issues.append(f"[boxed {eid}] boxed container missing padding_mobile")

            if wt == "heading" and s.get("header_size") in ("h1", "h2"):
                if not s.get("typography_font_size_mobile", {}).get("size"):
                    title = (s.get("title", "") or "")[:34]
                    issues.append(f"[{s.get('header_size')} {eid}] no mobile font size — will not shrink — \"{title}\"")

            if wt == "image" and s.get("height", {}).get("size") and not s.get("height_mobile", {}).get("size"):
                issues.append(f"[image {eid}] fixed height without height_mobile")

            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(content)
    return issues


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        doc = json.load(f)
    issues = audit(doc)
    if not issues:
        print("✅ Responsive audit: no issues — every grid/row/column/heading/container/image has its breakpoint settings.")
        sys.exit(0)
    print(f"⚠️  Responsive audit: {len(issues)} issue(s) found:")
    for i in issues:
        print("   -", i)
    sys.exit(1)


if __name__ == "__main__":
    main()
