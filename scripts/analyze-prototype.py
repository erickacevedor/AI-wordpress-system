#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic reader for an HTML/CSS design prototype — the kit-less sibling of
analyze-kit.py.

Some sites arrive without an Elementor export: a static HTML/CSS prototype, a design
repo, a `tokens.css`. There is no kit to mine, so onboarding has nothing to read —
which is how projects/lenz ended up as the only site with no generated skills.

This closes that gap. Where analyze-kit.py counts inline widget styling, this reads
the prototype's stylesheets. Same division of labour — it does the counting, the
agent does the judging.

It reads two layers, because real prototypes split their design system across both:

  1. **Custom properties** — colour ramps, semantic roles, type scale, spacing,
     radii, fonts. This is where a token-first prototype (the kind the master prompt
     in design-source/prompts/ produces) keeps everything.
  2. **The rules themselves** — the button spec, the section background bands, the
     font sizes actually used, the section rhythm. A hand-written prototype declares
     `--red` and `--ink` and then hardcodes `padding: 96px 0` and `border-radius:
     999px` in the rules. Reading only `:root` on one of those returns a palette and
     nothing else, and reports a button spec of "TODO" for a button the CSS fully
     specifies.

It resolves `var()` indirection in both layers, so a prototype that layers semantic
roles over a palette (`--color-text-primary: var(--neutral-900)`, or `.btn-primary
{ background: var(--red) }`) reports the hex that actually lands, not the reference.

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

# Markup files that count as "a page of the prototype". `.php` earns its place: a
# static site served by Apache routinely names its pages index.php purely to get
# clean directory URLs, with not one `<?php` tag inside. Judging by extension alone
# reported "0 HTML files" for a six-page prototype.
PAGE_EXT = (".html", ".htm", ".xhtml", ".php")

# Directories that never hold prototype source. One list, used by every walk in here
# — they used to disagree, so a dist/ copy could be skipped for CSS and counted for
# pages.
SKIP_DIRS = ("node_modules", ".git", "dist", "build", "vendor", ".next", "__pycache__")

# The steps a real shade ramp uses. `--brand-500` is a ramp; `--ink-2` is a second
# ink, and treating it as "ramp ink, step 2" invents a one-colour ramp AND drops the
# colour from the roles where it belongs.
RAMP_STEPS = frozenset(("0", "50", "100", "200", "300", "400",
                        "500", "600", "700", "800", "900", "950"))

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


def collect_pages(target):
    """Every markup page under a directory, as (relative path, source)."""
    out = []
    if not os.path.isdir(target):
        return out
    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if not n.lower().endswith(PAGE_EXT):
                continue
            p = os.path.join(root, n)
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    out.append((os.path.relpath(p, target), fh.read()))
            except Exception as ex:
                print("  ! skipped %s (%s)" % (p, ex), file=sys.stderr)
    return out


SECTION_TAG = re.compile(
    r"<(section|header|footer|main|aside|nav)\b[^>]*\bclass\s*=\s*[\"']([^\"']+)[\"']",
    re.I)


def section_classes(pages):
    """Classes that appear on a section-level element in the markup.

    This is what separates a background BAND from a component that merely has a
    background. `.about` and `.contact` sit on <section>; `.btn-primary`, `.chip` and
    `.post-thumb` never do. Reading the markup answers that outright, where guessing
    from the selector name cannot — and it is only possible now that .php pages are
    found at all.
    """
    found = set()
    for _path, html in pages:
        for m in SECTION_TAG.finditer(html):
            for cls in m.group(2).split():
                found.add(cls.strip())
    return found


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
    """Which GROUPS bucket a custom property belongs to, by name.

    A prefix also matches the bare name it is a prefix of: a prototype with a single
    corner radius writes `--radius: 14px`, not `--radius-md`, and the trailing-dash
    prefix missed it entirely.
    """
    for label, prefixes in GROUPS:
        for p in prefixes:
            if name.startswith(p) or name == p.rstrip("-"):
                return label
    return None


# -------------------------------------------------------------------- CSS rules
# Everything below reads the rules, not `:root`. A token-first prototype keeps its
# design system in custom properties and none of this fires; a hand-written one
# keeps most of it here.

def _split_top_level(text, sep):
    """Split on `sep`, ignoring separators inside (), [] or quotes.

    Needed because a declaration block can carry `background-image: url("data:image
    /svg+xml,...")`, and a naive split on ";" or "," tears the data URI in half.
    """
    out, buf, depth, quote = [], [], 0, None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == sep and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return out


def parse_decls(body):
    """`prop: value` pairs of one declaration block, last one wins."""
    d = {}
    for part in _split_top_level(body, ";"):
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k and v and not k.startswith("--"):
            d[k] = v
    return d


def parse_rules(css):
    """Every style rule as (selector, {prop: value}, at_rule_context), in source order.

    Deliberately a small hand-rolled scanner rather than a CSS parser dependency:
    this repo's scripts run on a bare python3. It tracks brace depth so `@media`
    blocks are descended into (and recorded), which matters because the mobile
    overrides of the section rhythm live inside them.
    """
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    out, buf, stack = [], [], []
    i, n = 0, len(css)
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = "".join(buf).strip()
            buf = []
            if prelude.startswith("@"):
                # An at-rule that wraps other rules (@media, @supports) — descend.
                # One that does not (@font-face) is skipped by the same code, since
                # its declarations have no selector to attach to.
                stack.append(prelude)
                i += 1
                continue
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            out.append((prelude, parse_decls(css[i + 1:j - 1]), " ".join(stack)))
            i = j
            continue
        if ch == "}":
            if stack:
                stack.pop()
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    return out


def _resolve_value(val, decls):
    """Resolve any var() inside a rule's value to what actually lands."""
    if not val or "var(" not in val:
        return val

    def sub(m):
        ref, fallback = m.group(1), (m.group(2) or "").strip()
        return resolve(ref, decls) or fallback
    for _ in range(6):
        new = VAR_REF.sub(sub, val)
        if new == val:
            break
        val = new
    return val.strip()


def _var_name_of(raw):
    """`var(--red)` -> "red". The name a band should carry: a prototype's own word
    for the colour beats the selector that happens to use it."""
    m = VAR_REF.match((raw or "").strip())
    return m.group(1).lstrip("-") if m else None


def _bg_of(props):
    """The background COLOUR a rule sets, ignoring gradients and images."""
    for prop in ("background-color", "background"):
        v = props.get(prop)
        if not v:
            continue
        v = v.strip()
        if any(k in v for k in ("gradient", "url(", "none")):
            continue
        first = _split_top_level(v, " ")[0].strip()
        return first or None
    return None


# Selector shapes that identify a button. Ordered: the first match wins as the base.
BTN_BASE = re.compile(r"^\.(btn|button|cta|c-btn|b-btn)$")
BTN_PRIMARY = re.compile(r"^\.(btn|button|cta)[-_]{1,2}(primary|main|solid|filled|red|accent)$")
SINGLE_CLASS = re.compile(r"^\.([a-zA-Z][\w-]*)$")


def read_rules(blobs, decls, sec_classes=None):
    """Distil the design decisions that live in rules rather than custom properties."""
    sec_classes = sec_classes or set()
    rules = []
    for _path, css in blobs:
        rules.extend(parse_rules(css))

    # --- button spec -----------------------------------------------------
    # Split base (shape: radius, padding, weight) from the primary variant (colour),
    # because CSS conventionally splits them the same way.
    button = {}
    for sel, props, at in rules:
        for one in (s.strip() for s in _split_top_level(sel, ",")):
            hover = one.endswith(":hover")
            bare = one[:-len(":hover")] if hover else one
            is_base = bool(BTN_BASE.match(bare))
            is_primary = bool(BTN_PRIMARY.match(bare))
            if not (is_base or is_primary):
                continue
            slot = "hover" if hover else ("primary" if is_primary else "base")
            # Inside a @media block these are responsive overrides, not the spec.
            if at:
                continue
            dest = button.setdefault(slot, {})
            for prop in ("background", "background-color", "color", "border-radius",
                         "padding", "font-weight", "font-size", "border",
                         "text-transform", "letter-spacing", "transform"):
                if prop in props:
                    dest[prop] = _resolve_value(props[prop], decls)
                    if prop in ("background", "background-color"):
                        vn = _var_name_of(props[prop])
                        if vn:
                            dest["_bg_var"] = vn

    # --- background bands ------------------------------------------------
    # A single-class selector that sets a flat background colour is a section band.
    # These are what `bands` in tokens.json means, and what the contrast checker
    # reads to know which surface text sits on.
    bands, band_seen, components = {}, {}, {}
    for sel, props, at in rules:
        if at:
            continue
        for one in (s.strip() for s in _split_top_level(sel, ",")):
            m = SINGLE_CLASS.match(one)
            if not m:
                continue
            raw_bg = _bg_of(props)
            if not raw_bg:
                continue
            hexv = _resolve_value(raw_bg, decls)
            if not HEX.match(hexv or ""):
                continue
            name = _var_name_of(raw_bg) or m.group(1)
            # Only a class the markup actually puts on a <section> is a band. Without
            # this the list fills with components that happen to have a background —
            # .btn-primary, .quote-form, .post-thumb — and `bands` in tokens.json
            # ends up claiming the CTA red is a section background.
            if sec_classes and m.group(1) not in sec_classes:
                components.setdefault(hexv, {"hex": hexv, "selectors": []})
                components[hexv]["selectors"].append(one)
                continue
            if hexv in band_seen:
                band_seen[hexv]["selectors"].append(one)
                continue
            entry = {"hex": hexv, "selectors": [one], "name": name}
            band_seen[hexv] = entry
            bands[name] = entry

    # --- font sizes actually used ----------------------------------------
    # Not a scale — a census. A prototype with 27 distinct font-sizes has drift, not
    # a scale, and the agent needs to see the distribution to collapse it honestly.
    sizes, anchors = {}, {}
    for sel, props, at in rules:
        fs = props.get("font-size")
        if not fs:
            continue
        val = _resolve_value(fs, decls)
        px = _px_of(val)
        key = round(px, 1) if px else val.strip()
        entry = sizes.setdefault(key, {"count": 0, "selectors": [], "raw": val.strip()})
        entry["count"] += 1
        if len(entry["selectors"]) < 4:
            where = " [%s]" % at.split("(")[0].strip().lstrip("@") if at else ""
            entry["selectors"].append(sel.strip()[:40] + where)
        for tag in ("h1", "h2", "h3", "h4", "body"):
            if not at and re.match(r"^%s$" % tag, sel.strip()):
                anchors[tag] = val.strip()

    # --- font families, from what the rules assign -----------------------
    # A prototype that names its families by shape (`--font-sans`, `--font-serif`)
    # says nothing about which is the heading face — the heuristic on custom-property
    # names cannot tell, and returned "TODO" for a required field. The rules do say:
    # whatever `body` gets is the body face, whatever h1/h2/h3 get is the heading
    # face, and when the headings set none they inherit the body's.
    families = {}
    for sel, props, at in rules:
        fam = props.get("font-family")
        if not fam or at:
            continue
        val = _resolve_value(fam, decls).split(",")[0].strip().strip("'\"")
        if not val:
            continue
        for one in (s.strip() for s in _split_top_level(sel, ",")):
            if one in ("body", "html"):
                families.setdefault("body", val)
            elif re.match(r"^h[1-3]$", one):
                families.setdefault("heading", val)
            elif one in ("em", ".serif", ".display", ".accent"):
                families.setdefault("accent", val)
    if "heading" not in families and "body" in families:
        families["heading"] = families["body"]
        families["_heading_inherited"] = "no font-family on h1/h2/h3 — inherits body"

    # --- section rhythm --------------------------------------------------
    # Vertical padding on band selectors: the spacing scale of a prototype that has
    # no --space-* tokens.
    rhythm = {}
    for sel, props, at in rules:
        pad = props.get("padding") or props.get("padding-block") or props.get("padding-top")
        if not pad:
            continue
        for one in (s.strip() for s in _split_top_level(sel, ",")):
            m = SINGLE_CLASS.match(one)
            # Match against the section classes from the markup, not the band names
            # — `bands` is keyed by colour ("paper"), so testing membership there
            # matched nothing and the rhythm only ever reported `.section`.
            if not m or (m.group(1) not in sec_classes and one != ".section"):
                continue
            px = _px_of(_split_top_level(_resolve_value(pad, decls), " ")[0].strip())
            if px is None:
                continue
            bucket = "mobile" if at else "desktop"
            rhythm.setdefault(one, {})[bucket] = round(px, 1)

    return {
        "rule_count": len(rules),
        "button": button,
        "bands": bands,
        "font_families": families,
        "component_backgrounds": components,
        "font_sizes": sizes,
        "type_anchors": anchors,
        "section_rhythm": rhythm,
        "section_classes": sorted(sec_classes),
    }


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
        is_hex = bool(HEX.match(val or ""))

        m = RAMP.match(name)
        if m and is_hex and m.group(2) in RAMP_STEPS:
            family, step = m.group(1), m.group(2)
            ramps.setdefault(family, {})[step] = val
            continue

        # A value that IS a colour is a colour, whatever the name suggests. This has
        # to outrank classify(): a hand-written prototype names its body-text colour
        # `--text`, which the type-scale prefix would otherwise swallow — filing the
        # brand's text colour under "type scale" and leaving the palette short one
        # role.
        if is_hex or name.startswith("--color-"):
            roles[name] = {"value": val, "raw": raw,
                           "indirect": raw.strip() != (val or "").strip()}
            continue

        label = classify(name)
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

    pages = collect_pages(target)
    html = [p for p, _ in pages]
    rules = read_rules(blobs, decls, section_classes(pages))

    return {
        "source": target,
        "css_files": [os.path.relpath(p, target) if os.path.isdir(target) else p
                      for p, _ in blobs],
        "html_files": html,
        "counts": {"custom_properties": len(decls), "ramps": len(ramps),
                   "semantic_roles": len(roles), "rules": rules["rule_count"],
                   "bands": len(rules["bands"]), "font_sizes": len(rules["font_sizes"])},
        "ramps": ramps,
        "roles": roles,
        "contrast": contrast,
        "groups": groups,
        "other": other,
        "var_sources": source,
        "rules": rules,
    }


# ------------------------------------------------------------------ tokens.json
def _ramp_base(steps):
    for k in ("500", "600", "400"):
        if k in steps:
            return steps[k]
    if not steps:
        return None
    # Sort the steps numerically. Sorting them as strings puts "100" before "30",
    # so the "middle" step of a ramp was whichever one sorted there alphabetically.
    ordered = sorted(steps, key=lambda s: int(s))
    return steps[ordered[len(ordered) // 2]]


def _px_of(val):
    if not val:
        return None
    m = re.match(r"^(-?\d*\.?\d+)(px|rem|em)$", val.strip())
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) in ("rem", "em") else n


CLAMP = re.compile(r"^clamp\(\s*([^,]+),([^,]+),\s*([^)]+)\)\s*$", re.I)


def _clamp_range(val):
    """`clamp(2.4rem, 5.2vw, 4rem)` -> (38.4, 64.0) in px, or None.

    A fluid heading is a real design decision — its floor and ceiling are what an
    Elementor rebuild needs (desktop size + mobile size). Printing the raw clamp()
    truncated to fit a column threw both numbers away.
    """
    m = CLAMP.match((val or "").strip())
    if not m:
        return None
    lo, hi = _px_of(m.group(1).strip()), _px_of(m.group(3).strip())
    return (lo, hi) if lo and hi else None


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

    rules = facts.get("rules") or {}

    # Whatever the property names could not settle, the rules can. Never overwrite an
    # explicit `--font-heading`; only fill the holes.
    for which, val in sorted((rules.get("font_families") or {}).items()):
        if not which.startswith("_"):
            fonts.setdefault(which, val)

    type_scale = {}
    for name, meta in facts["groups"]["type"].items():
        px = _px_of(meta["value"])
        if px:
            type_scale[name.lstrip("-")] = round(px, 1)
    # No --text-*/--font-size-* tokens: fall back to what the rules actually set on
    # the heading tags. Deliberately only the anchors, never the full census — a
    # prototype with 27 distinct font-sizes has drift, and copying all 27 into
    # tokens.json would launder that drift into "the scale".
    if not type_scale:
        for tag, val in sorted((rules.get("type_anchors") or {}).items()):
            px = _px_of(val)
            if px:
                type_scale[tag] = round(px, 1)
                continue
            # A fluid heading carries two numbers an Elementor rebuild needs: the
            # mobile floor and the desktop ceiling. Keep both, not the clamp() string.
            rng = _clamp_range(val)
            if rng:
                type_scale[tag] = round(rng[1], 1)
                type_scale["%s_mobile" % tag] = round(rng[0], 1)
            else:
                type_scale[tag] = val
        if type_scale:
            type_scale["_from"] = "css rules (no type tokens declared); anchors only"

    spacing = {}
    for name, meta in facts["groups"]["space"].items():
        px = _px_of(meta["value"])
        if px:
            spacing[name.lstrip("-")] = round(px, 1)
    # Same fallback for spacing: the section rhythm IS the spacing scale on a
    # prototype that hardcodes `padding: 96px 0`.
    if not spacing:
        for sel, buckets in sorted((rules.get("section_rhythm") or {}).items()):
            for bucket, px in sorted(buckets.items()):
                spacing["%s-%s" % (sel.lstrip("."), bucket)] = px
        if spacing:
            spacing["_from"] = "css rules (no spacing tokens declared); section padding"

    radii = {}
    for name, meta in facts["groups"]["radius"].items():
        v = (meta["value"] or "").strip()
        radii[name.lstrip("-")] = v

    # Deterministic and explained. The old loop walked every layout var and kept the
    # LAST in-range hit, so a prototype declaring both --container and --max-width
    # got whichever dict order happened to put second.
    content_width, width_from = 1140, "default (no container width declared)"
    layout = facts["groups"]["layout"]
    for want in ("--container", "--max-width", "--content-width", "--wrapper"):
        for name in sorted(layout):
            if not (name == want or name.startswith(want + "-")):
                continue
            px = _px_of(layout[name]["value"])
            if px and 900 <= px <= 1920:
                content_width, width_from = int(px), name
                break
        if width_from != "default (no container width declared)":
            break

    doc = {
        "site": site_slug,
        "_source": "html-prototype: %s" % facts["source"],
        "_note": ("Generated by scripts/analyze-prototype.py. Values marked TODO are "
                  "NOT derivable from a stylesheet — fill them from the brief before "
                  "building any page."),
        "content_width": content_width,
        "_content_width_from": width_from,
        "fonts": fonts or {"heading": "TODO", "body": "TODO"},
        "colors": colors,
        "roles": role_block,
        "type_scale": type_scale,
        "spacing": spacing,
        "radii": radii,
        "button": _button_block(rules.get("button") or {}, role_block, radii),
        "links": {"_todo": "root-relative internal link targets, e.g. /contact"},
        "phone": {"_todo": "display + tel: form"},
    }

    # Section background bands. dolan/tokens.json already carries this key and
    # site_tokens.band_hexes() already reads it — the HTML path just never filled it.
    band_block = {}
    for name, entry in (rules.get("bands") or {}).items():
        band_block[name] = entry["hex"]
    if band_block:
        doc["bands"] = band_block

    # site_tokens.py maps a site's own colour names onto canonical roles, and without
    # an explicit `_roles` block it INFERS them from the usual names. On a prototype
    # like this one that inference is silently wrong: it sees a key called "blue" and
    # calls it the brand primary, when the brand's primary is the red. Emitting the
    # scaffold — with what would be inferred — turns a silent wrong answer into a
    # visible decision the agent has to make.
    inferred = {}
    for role, aliases in (("primary", ("primary", "blue", "brand", "main", "cta-bg")),
                          ("secondary", ("secondary", "orange", "gold", "red", "purple")),
                          ("accent", ("accent", "cta", "highlight")),
                          ("dark", ("dark", "navy", "black", "ink")),
                          ("text", ("text", "body", "ink", "black")),
                          ("surface", ("white", "surface", "bg", "background")),
                          ("muted", ("grey", "gray", "soft_gray", "neutral", "muted"))):
        for alias in aliases:
            if alias in role_block or alias in colors:
                inferred[role] = alias
                break
    if inferred:
        doc["_roles"] = dict(inferred)
        doc["_roles"]["_todo"] = ("VERIFY these. They are what site_tokens.py would "
                                  "infer from the key names, not what the brand means. "
                                  "Correct them against the design before building.")

    return doc


def _button_block(btn, role_block, radii):
    """The CTA spec, read off the prototype's own .btn rules where they exist.

    The previous version emitted TODO for every field and told the agent the spec was
    "NOT derivable from a stylesheet". For a hand-written prototype that is simply
    untrue — `.btn` and `.btn-primary` state the radius, padding, weight, fill and
    hover fill outright. Anything the rules genuinely do not say still comes back as
    TODO, so a guess never ships as a fact.
    """
    base = btn.get("base") or {}
    primary = btn.get("primary") or base
    hover = btn.get("hover") or {}

    def pick(src, *props):
        for p in props:
            if src.get(p):
                return src[p]
        return None

    bg = pick(primary, "background-color", "background") or \
        role_block.get("cta-bg", {}).get("hex")
    hover_bg = pick(hover, "background-color", "background") or \
        role_block.get("cta-bg-hover", {}).get("hex")
    text = pick(primary, "color") or pick(base, "color")
    radius = pick(base, "border-radius") or pick(primary, "border-radius") or \
        radii.get("radius-button") or radii.get("radius")
    padding = pick(base, "padding") or pick(primary, "padding")
    weight = pick(base, "font-weight") or pick(primary, "font-weight")

    # A transform on :hover is the prototype saying the hover is an animation, not
    # just a colour swap. That distinction is exactly what the button spec is for.
    transform = pick(hover, "transform")

    out = {
        "bg": bg or "TODO",
        "hover": hover_bg or "TODO",
        "text": text or "TODO",
        "radius": radius or "TODO",
        "padding": padding or "TODO",
        "font_weight": weight or "TODO",
        "hover_animation": transform or "",
    }
    if btn:
        out["_from"] = "css rules (.btn / .btn-primary)"
    if any(v == "TODO" for v in out.values()):
        out["_todo"] = ("fields still marked TODO are not stated by the CSS — fill "
                        "them from the brief")
    return out


# ---------------------------------------------------------------------- report
def report(f):
    L = []
    a = L.append
    c = f["counts"]
    a("Prototype: %s" % f["source"])
    a("  %d CSS file(s) · %d page(s) · %d custom properties · %d ramps · %d semantic roles"
      % (len(f["css_files"]), len(f["html_files"]), c["custom_properties"],
         c["ramps"], c["semantic_roles"]))
    a("  %d CSS rules read · %d background band(s) · %d distinct font-size(s)"
      % (c.get("rules", 0), c.get("bands", 0), c.get("font_sizes", 0)))

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

    r = f.get("rules") or {}

    if r.get("bands"):
        a("")
        a("BACKGROUND BANDS (a section's background is a design decision, not a colour)")
        for name, e in sorted(r["bands"].items(), key=lambda kv: -len(kv[1]["selectors"])):
            sels = ", ".join(e["selectors"][:5])
            if len(e["selectors"]) > 5:
                sels += " … +%d" % (len(e["selectors"]) - 5)
            a("  %-14s %-9s %s" % (name, e["hex"], sels))

    if r.get("font_families"):
        a("")
        a("FONT FAMILIES (what the rules actually assign, not what the tokens are named)")
        for which, val in sorted(r["font_families"].items()):
            if which.startswith("_"):
                continue
            note = ""
            if which == "heading" and r["font_families"].get("_heading_inherited"):
                note = "   ← %s" % r["font_families"]["_heading_inherited"]
            a("  %-10s %s%s" % (which, val, note))

    if r.get("button"):
        a("")
        a("BUTTON SPEC (read off the prototype's own rules)")
        for slot in ("base", "primary", "hover"):
            block = r["button"].get(slot)
            if not block:
                continue
            shown = ["%s: %s" % (k, v) for k, v in sorted(block.items())
                     if not k.startswith("_")]
            a("  %-9s %s" % (slot, "  ·  ".join(shown)[:150]))

    if r.get("font_sizes"):
        a("")
        a("FONT SIZES IN USE (a census, not a scale — collapse it yourself)")
        px_keys = sorted([k for k in r["font_sizes"] if isinstance(k, float)], reverse=True)
        other_keys = [k for k in r["font_sizes"] if not isinstance(k, float)]
        for k in px_keys[:18] + other_keys:
            e = r["font_sizes"][k]
            if isinstance(k, float):
                label = "%gpx" % k
            else:
                rng = _clamp_range(str(k))
                label = ("%g→%gpx fluid" % rng) if rng else str(k)[:22]
            a("  %-16s %2d× %s" % (label, e["count"], ", ".join(e["selectors"][:3])[:60]))
        if len(px_keys) > 18:
            a("  … and %d more distinct size(s)" % (len(px_keys) - 18))
        if len(px_keys) + len(other_keys) > 12:
            a("  ⚠ %d distinct sizes is drift, not a scale. Decide the real steps and"
              % (len(px_keys) + len(other_keys)))
            a("    record the mapping in KIT-ANALYSIS.md — Elementor cannot reproduce drift.")

    if r.get("section_rhythm"):
        a("")
        a("SECTION RHYTHM (vertical padding per band)")
        for sel, buckets in sorted(r["section_rhythm"].items()):
            a("  %-18s %s" % (sel, "  ·  ".join("%s %gpx" % (b, p)
                                                for b, p in sorted(buckets.items()))))

    if f["html_files"]:
        a("")
        a("PAGES IN THE PROTOTYPE")
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


def _seam_check(path):
    """What the canonical reader still cannot answer about the file just written.

    Returns [] when the seam is fully readable, a list of gaps when it is not, and
    None when the check itself could not run.
    """
    try:
        import site_tokens
        return site_tokens.load(path).missing_core()
    except Exception:
        return None


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
        print("   %d colour ramp(s), %d role(s), %d band(s), %d type step(s), %d spacing step(s)"
              % (len(doc["colors"]), len(doc["roles"]), len(doc.get("bands") or {}),
                 len(doc["type_scale"]), len(doc["spacing"])))
        print("   content_width %s — from %s" % (doc["content_width"], doc["_content_width_from"]))
        todo = sorted(k for k, v in doc["button"].items() if v == "TODO")
        if todo:
            print("   button: still TODO -> %s" % ", ".join(todo))
        else:
            print("   button: fully read from the prototype's .btn rules — verify it")
        print("   links and phone are always TODO — fill them from the brief.")

        # Check the seam ourselves. Printing a command for the operator to run is not
        # the same as knowing the file works: producing a tokens.json the rest of the
        # pipeline can read IS this script's job, so it verifies that before claiming
        # success.
        print("")
        missing = _seam_check(out)
        if missing is None:
            print("   ? could not self-check the seam (site_tokens.py not importable)")
        elif missing:
            print("   ⚠ the pipeline CANNOT fully read this seam yet:")
            for m in missing:
                print("       - %s" % m)
            print("     A prototype that never names a brand primary cannot have one")
            print("     inferred. Decide it, then set it in the `_roles` block.")
        else:
            print("   ✅ seam verified: site_tokens.py reads every canonical role.")
        sys.exit(0)

    if "--json" in sys.argv:
        print(json.dumps(facts, indent=2, ensure_ascii=False))
    else:
        print(report(facts))
    sys.exit(0)


if __name__ == "__main__":
    main()
