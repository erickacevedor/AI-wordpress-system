#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic reader for an HTML/CSS design prototype — the kit-less sibling of
analyze-kit.py.

Some sites arrive without an Elementor export: a static HTML/CSS prototype, a design
repo, a `tokens.css`. There is no kit to mine, so onboarding has nothing to read —
which is how projects/lenz ended up as the only site with no generated skills.

This closes that gap. Where analyze-kit.py counts inline widget styling, this reads
CSS custom properties: colour ramps, semantic roles, the type scale, spacing, radii
and fonts. Same division of labour — it does the counting, the agent does the
judging.

It resolves `var()` indirection, so a prototype that layers semantic roles over a
palette (`--color-text-primary: var(--neutral-900)`) reports the hex that actually
lands, not the reference.

`--emit-tokens` writes a projects/<site>/tokens.json skeleton directly, in this
repo's schema. That is the whole point: tokens.json is the seam where the HTML
origin and the kit origin converge, and everything downstream — brand.py, build.py,
the gate, the preview, the handoff — is already origin-agnostic.

Usage:
    python3 scripts/analyze-prototype.py <dir-or-file.css>
    python3 scripts/analyze-prototype.py <dir> --json
    python3 scripts/analyze-prototype.py <dir> --emit-tokens projects/<site>/tokens.json

Reads only (unless --emit-tokens is given, which writes exactly that one file).
Exit code: 0 = analysed, 2 = nothing readable found.
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

VAR_DECL = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)[;}]")
VAR_REF = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,\s*([^)]+))?\)")
HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
RAMP = re.compile(r"^--([a-z][a-z0-9]*(?:-[a-z0-9]+)*?)-(\d{1,3})$")
LEN = re.compile(r"^-?\d*\.?\d+(px|rem|em|%|vh|vw)$")

# Which custom-property prefixes carry which kind of value. Prototypes vary, so these
# are matched loosely and anything unmatched still shows up under "other".
GROUPS = (
    ("type",    ("--text-", "--font-size-", "--fs-")),
    ("space",   ("--space-", "--spacing-", "--gap-")),
    ("radius",  ("--radius-", "--rounded-")),
    ("font",    ("--font-", "--family-")),
    ("motion",  ("--transition-", "--duration-", "--ease-")),
    ("layout",  ("--bp-", "--breakpoint-", "--container", "--navbar", "--offer",
                 "--section-padding", "--card-padding", "--max-width")),
    ("shadow",  ("--shadow", "--elevation")),
    ("border",  ("--border",)),
)


def _load_contrast():
    import importlib.util
    import pathlib
    p = pathlib.Path(__file__).with_name("contrast-audit.py")
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location("contrast_audit", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def collect_css(target):
    """Every .css file under a directory, or the single file given."""
    files = []
    if os.path.isfile(target):
        files = [target]
    else:
        for root, dirs, names in os.walk(target):
            dirs[:] = [d for d in dirs
                       if d not in ("node_modules", ".git", "dist", "build", "vendor")]
            for n in sorted(names):
                if n.endswith(".css"):
                    files.append(os.path.join(root, n))
    out = []
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                out.append((f, fh.read()))
        except Exception as ex:
            print("  ! skipped %s (%s)" % (f, ex), file=sys.stderr)
    return out


def parse_vars(css_blobs):
    """All custom-property declarations, last one wins (CSS cascade, roughly)."""
    decls = {}
    source = {}
    for path, css in css_blobs:
        css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
        for m in VAR_DECL.finditer(css):
            name, value = m.group(1), m.group(2).strip()
            decls[name] = value
            source[name] = os.path.basename(path)
    return decls, source


def resolve(name, decls, seen=None, depth=0):
    """Follow var() chains to the value that actually lands."""
    if depth > 12:
        return decls.get(name, "")
    seen = seen or set()
    val = decls.get(name, "")
    if not val or name in seen:
        return val
    seen = seen | {name}

    def sub(m):
        ref, fallback = m.group(1), (m.group(2) or "").strip()
        r = resolve(ref, decls, seen, depth + 1)
        return r or fallback
    return VAR_REF.sub(sub, val).strip()


def classify(name):
    for label, prefixes in GROUPS:
        if any(name.startswith(p) for p in prefixes):
            return label
    return None


def analyze(target):
    blobs = collect_css(target)
    if not blobs:
        return None
    decls, source = parse_vars(blobs)
    resolved = {k: resolve(k, decls) for k in decls}

    ramps = {}
    roles = {}
    groups = {label: {} for label, _ in GROUPS}
    other = {}

    for name, raw in sorted(decls.items()):
        val = resolved.get(name, raw)
        m = RAMP.match(name)
        if m and HEX.match(val or ""):
            family, step = m.group(1), m.group(2)
            ramps.setdefault(family, {})[step] = val
            continue
        label = classify(name)
        if name.startswith("--color-") or (label is None and HEX.match(val or "")):
            roles[name] = {"value": val, "raw": raw,
                           "indirect": raw.strip() != (val or "").strip()}
            continue
        if label:
            groups[label][name] = {"value": val, "raw": raw}
        else:
            other[name] = {"value": val, "raw": raw}

    ca = _load_contrast()
    contrast = {}
    if ca:
        for name, meta in roles.items():
            v = meta["value"]
            if v and ca._rgb(v):
                on_white = ca.ratio(v, "#FFFFFF")
                on_dark = ca.ratio(v, "#121212")
                contrast[name] = {
                    "hex": v,
                    "on_white": round(on_white, 2) if on_white else None,
                    "on_dark": round(on_dark, 2) if on_dark else None,
                }

    html = []
    if os.path.isdir(target):
        for root, dirs, names in os.walk(target):
            dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "dist")]
            for n in sorted(names):
                if n.endswith((".html", ".htm")):
                    html.append(os.path.relpath(os.path.join(root, n), target))

    return {
        "source": target,
        "css_files": [os.path.relpath(p, target) if os.path.isdir(target) else p
                      for p, _ in blobs],
        "html_files": html,
        "counts": {"custom_properties": len(decls), "ramps": len(ramps),
                   "semantic_roles": len(roles)},
        "ramps": ramps,
        "roles": roles,
        "contrast": contrast,
        "groups": groups,
        "other": other,
        "var_sources": source,
    }


# ------------------------------------------------------------------ tokens.json
def _ramp_base(steps):
    for k in ("500", "600", "400"):
        if k in steps:
            return steps[k]
    return steps[sorted(steps)[len(steps) // 2]] if steps else None


def _px_of(val):
    if not val:
        return None
    m = re.match(r"^(-?\d*\.?\d+)(px|rem|em)$", val.strip())
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) in ("rem", "em") else n


def emit_tokens(facts, site_slug):
    """A tokens.json skeleton in this repo's schema. Deliberately incomplete: the
    values it cannot know (site url, phone, links, the button spec) are left as
    explicit TODO markers rather than invented, so the agent fills them from the
    brief instead of shipping a plausible guess."""
    ramps = facts["ramps"]
    roles = {k: v["value"] for k, v in facts["roles"].items() if v.get("value")}

    colors = {}
    for family, steps in sorted(ramps.items()):
        colors[family] = dict(sorted(steps.items(), key=lambda kv: int(kv[0])))

    role_block = {}
    for name, hexv in sorted(roles.items()):
        key = name[len("--color-"):] if name.startswith("--color-") else name.lstrip("-")
        role_block[key] = {"hex": hexv, "global": None}

    # A prototype often declares the page surface only as `--neutral-0`, never as a
    # `--color-bg-*` role. Downstream tooling asks for "surface", so fill it from the
    # lightest neutral and mark it inferred rather than leaving a hole.
    if not any(k in role_block for k in ("bg-primary", "surface", "white", "background")):
        neutrals = ramps.get("neutral") or {}
        for step in ("0", "50"):
            if step in neutrals:
                role_block["bg-primary"] = {"hex": neutrals[step], "global": None,
                                            "_inferred": "lightest neutral (--neutral-%s)" % step}
                break

    fonts = {}
    for name, meta in facts["groups"]["font"].items():
        v = (meta["value"] or "").strip().strip("'\"")
        if not v or LEN.match(v):
            continue
        first = v.split(",")[0].strip().strip("'\"")
        if "head" in name:
            fonts["heading"] = first
        elif "body" in name or "second" in name:
            fonts["body"] = first
        elif "button" in name:
            fonts["button"] = first
        elif "primary" in name and "heading" not in fonts:
            fonts["heading"] = first

    type_scale = {}
    for name, meta in facts["groups"]["type"].items():
        px = _px_of(meta["value"])
        if px:
            type_scale[name.lstrip("-")] = round(px, 1)

    spacing = {}
    for name, meta in facts["groups"]["space"].items():
        px = _px_of(meta["value"])
        if px:
            spacing[name.lstrip("-")] = round(px, 1)

    radii = {}
    for name, meta in facts["groups"]["radius"].items():
        v = (meta["value"] or "").strip()
        radii[name.lstrip("-")] = v

    content_width = 1140
    for name, meta in facts["groups"]["layout"].items():
        if "container" in name or "max-width" in name:
            px = _px_of(meta["value"])
            if px and 900 <= px <= 1920:
                content_width = int(px)

    doc = {
        "site": site_slug,
        "_source": "html-prototype: %s" % facts["source"],
        "_note": ("Generated by scripts/analyze-prototype.py. Values marked TODO are "
                  "NOT derivable from a stylesheet — fill them from the brief before "
                  "building any page."),
        "content_width": content_width,
        "fonts": fonts or {"heading": "TODO", "body": "TODO"},
        "colors": colors,
        "roles": role_block,
        "type_scale": type_scale,
        "spacing": spacing,
        "radii": radii,
        "button": {
            "_todo": "the CTA spec: fill/hover/text colours, radius, padding, hover "
                     "convention (colour-only vs animation)",
            "bg": role_block.get("cta-bg", {}).get("hex") or "TODO",
            "hover": role_block.get("cta-bg-hover", {}).get("hex") or "TODO",
            "text": "TODO",
            "radius": radii.get("radius-button") or "TODO",
            "hover_animation": "",
        },
        "links": {"_todo": "root-relative internal link targets, e.g. /contact"},
        "phone": {"_todo": "display + tel: form"},
    }
    return doc


# ---------------------------------------------------------------------- report
def report(f):
    L = []
    a = L.append
    c = f["counts"]
    a("Prototype: %s" % f["source"])
    a("  %d CSS file(s) · %d HTML file(s) · %d custom properties · %d ramps · %d semantic roles"
      % (len(f["css_files"]), len(f["html_files"]), c["custom_properties"],
         c["ramps"], c["semantic_roles"]))

    if f["ramps"]:
        a("")
        a("COLOUR RAMPS (a prototype's palette is usually a ramp per brand colour)")
        for family, steps in sorted(f["ramps"].items()):
            ordered = sorted(steps.items(), key=lambda kv: int(kv[0]))
            base = _ramp_base(steps)
            a("  %-10s %2d steps   base %s   %s"
              % (family, len(ordered), base or "?",
                 " ".join("%s:%s" % (k, v) for k, v in ordered[:5])
                 + (" …" if len(ordered) > 5 else "")))

    if f["roles"]:
        a("")
        a("SEMANTIC ROLES (what the design says each colour is FOR — trust these over the ramp)")
        for name, meta in sorted(f["roles"].items()):
            via = "  ← %s" % meta["raw"] if meta["indirect"] else ""
            cr = f["contrast"].get(name)
            note = ""
            if cr and cr["on_white"] is not None:
                note = "   %5.2f:1 on white · %5.2f:1 on #121212" % (cr["on_white"], cr["on_dark"])
            a("  %-28s %-9s%s%s" % (name, meta["value"], note, via))

    for label, title in (("font", "FONTS"), ("type", "TYPE SCALE"),
                         ("space", "SPACING"), ("radius", "RADII"),
                         ("layout", "LAYOUT / BREAKPOINTS"), ("motion", "MOTION")):
        block = f["groups"].get(label) or {}
        if block:
            a("")
            a(title)
            for name, meta in sorted(block.items()):
                a("  %-28s %s" % (name, (meta["value"] or "")[:60]))

    if f["html_files"]:
        a("")
        a("HTML PAGES IN THE PROTOTYPE")
        for h in f["html_files"][:14]:
            a("  %s" % h)
        if len(f["html_files"]) > 14:
            a("  … and %d more" % (len(f["html_files"]) - 14))

    a("")
    a("Next: the counting is done — the judgement is not. Decide which ramp is the")
    a("brand primary, which role is the CTA, and what the voice is; then write")
    a("tokens.json (--emit-tokens gives you the skeleton), KIT-ANALYSIS.md and the")
    a("five <site>-* skills. See skills/html-prototype-onboarding.")
    return "\n".join(L)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    target = args[0].rstrip("/\\")
    if not os.path.exists(target):
        print("✗ not found: %s" % target)
        sys.exit(2)

    facts = analyze(target)
    if not facts:
        print("✗ no .css found under %s — point this at a prototype's stylesheet(s)" % target)
        sys.exit(2)

    if "--emit-tokens" in sys.argv:
        out = sys.argv[sys.argv.index("--emit-tokens") + 1]
        slug = os.path.basename(os.path.dirname(os.path.abspath(out))) or "site"
        doc = emit_tokens(facts, slug)
        if os.path.exists(out):
            print("✗ %s already exists — refusing to overwrite a site's tokens." % out)
            print("  Write elsewhere and merge by hand; tokens.json is hand-tuned after generation.")
            sys.exit(2)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print("✅ wrote %s" % out)
        print("   %d colour ramp(s), %d role(s), %d type step(s), %d spacing step(s)"
              % (len(doc["colors"]), len(doc["roles"]), len(doc["type_scale"]),
                 len(doc["spacing"])))
        print("   TODO markers remain for the button spec, links and phone — fill them")
        print("   from the brief. Then verify with: python3 scripts/validate-tokens.py "
              "(or read it back with site_tokens.py).")
        sys.exit(0)

    if "--json" in sys.argv:
        print(json.dumps(facts, indent=2, ensure_ascii=False))
    else:
        print(report(facts))
    sys.exit(0)


if __name__ == "__main__":
    main()
