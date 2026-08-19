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
  - emoji-as-icon headings sized in px without a mobile size (checklist §5)

Usage:  python3 scripts/responsive-audit.py path/to/page.json
Exit code 0 = clean, 1 = issues found (handy in a pre-import gate).
"""
import json, re, sys

# Same cp1252 guard as validate-page.py — the report markers are non-ASCII.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# Emoji used as an icon (card headers, benefit lists, step markers). Matches the
# pictographic + dingbat ranges the builder's emoji_icon() emits; deliberately not a
# full grapheme parser -- a false negative here just means one fewer flagged heading.
_EMOJI = re.compile("[🌀-🫿☀-➿⬀-⯿]")


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
                # The bug this catches is OMITTING a mobile direction, so a layout row
                # stays side-by-side and squashes at 375px. Explicitly setting
                # `row`/`row-reverse` for mobile is a different thing: a deliberate
                # choice, and a common, legitimate one — an icon beside its label, a
                # rating beside its count, a price beside its unit. Stacking those
                # would be the bug. So: omission fails, an explicit value passes, and
                # the deliberate cases stay greppable in the build source.
                mobile_dir = s.get("flex_direction_mobile")
                if mobile_dir is None:
                    issues.append(f"[row {eid}] flex row has no mobile direction — it will not stack "
                                  f"(set flex_direction_mobile: column, or 'row' if that is intended)")

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

            # An emoji icon is a heading widget carrying an explicit size. h1/h2 are
            # covered above; this catches the p/h3/h4 ones used as card icons, which
            # otherwise stay at their 42px desktop size on a 375px screen.
            if (wt == "heading" and s.get("header_size") not in ("h1", "h2")
                    and _EMOJI.search(s.get("title", "") or "")
                    and s.get("typography_font_size", {}).get("size")
                    and not s.get("typography_font_size_mobile", {}).get("size")):
                issues.append(f"[emoji {eid}] emoji icon \"{(s.get('title') or '')[:2]}\" has a "
                              f"desktop font size but no typography_font_size_mobile")

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
