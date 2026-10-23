#!/usr/bin/env python3
"""
Port the approved V2.1 prototype into newman-core. Same approach as Lenz
(projects/lenz/tools/port-css.py); read that docstring for the why of each rule.

  in:  design-source/v2-1/index.html        (<style>, icon sprite <svg>)
       pages/*/widget-classes.json           (written by each build.py via brand.py)
       plugin/newman-core/assets/css/src/adapter.css, overrides.css
  out: plugin/newman-core/assets/css/newman-core.css
       plugin/newman-core/assets/icons/newman-sprite.svg

Differences from the Lenz porter:
  - Scope is `.nw-site .elementor ` (body class set by newman-core only on pages
    built from this design), because the same install serves the live splash and
    the promo landing pages, which must not change.
  - `:root` and `body` become `body.nw-site`, `html` becomes `html:has(body.nw-site)`.
  - The prototype keeps CSS, sprite and script inline in one HTML file; this reads
    them from there. The script is ported by hand (assets/js/newman-site.js).

Run:  python3 projects/newman-air/tools/port-css.py
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = os.path.join(SITE, "design-source", "v2-1", "index.html")
PLUGIN = os.path.join(SITE, "plugin", "newman-core", "assets")
SCOPE = ".nw-site .elementor "

INNER = {"heading": ".elementor-heading-title", "button": ".elementor-button"}
LZ_TAGS = ("ul", "li", "figure", "figcaption", "blockquote", "span")
ELEMENTS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "img", "ul", "li", "span", "svg", "b",
            "small", "figure", "blockquote", "figcaption", "iframe", "strong", "label", "input",
            "select", "textarea", "summary"}


def load_manifest():
    kinds = {}
    for path in sorted(glob.glob(os.path.join(SITE, "pages", "*", "widget-classes.json"))):
        for cls, kind in json.load(open(path, encoding="utf-8")).items():
            if kinds.get(cls, kind) != kind:
                raise SystemExit("class %r is %s in one page and %s in another" % (cls, kinds[cls], kind))
            kinds[cls] = kind
    return kinds


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def blocks(css):
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            return
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            c = css[k]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            elif c in "\"'":
                k = css.index(c, k + 1)
            k += 1
        yield prelude, css[j + 1:k - 1]
        i = k


def split_top(s, sep=","):
    out, depth, cur, q = [], 0, [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return [p.strip() for p in out if p.strip()]


_COMB = re.compile(r"\s*([>+~])\s*|\s+")


def compounds(sel):
    parts, cur, depth, i = [], "", 0, 0
    while i < len(sel):
        ch = sel[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if depth == 0 and (ch.isspace() or ch in ">+~"):
            m = _COMB.match(sel, i)
            comb = (m.group(1) or " ")
            if cur:
                parts.append(cur)
            cur = ""
            parts.append(comb)
            i = m.end()
            continue
        cur += ch
        i += 1
    if cur:
        parts.append(cur)
    clean = []
    for p in parts:
        if p in (" ", ">", "+", "~"):
            if clean and clean[-1] in (" ", ">", "+", "~"):
                clean[-1] = p if p != " " else clean[-1]
                continue
            if not clean:
                continue
        clean.append(p)
    return clean


def classes_of(compound):
    base = re.sub(r"\([^)]*\)", "", compound)
    return re.findall(r"\.([A-Za-z0-9_-]+)", base)


def split_pseudo(compound):
    depth = 0
    for i, ch in enumerate(compound):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == ":" and depth == 0:
            return compound[:i], compound[i:]
    return compound, ""


def map_tags(compound):
    m = re.match(r"^([a-z][a-z0-9]*)(.*)$", compound)
    if m and m.group(1) in LZ_TAGS:
        return ":is(%s, .lz-%s)%s" % (m.group(1), m.group(1), m.group(2))
    return compound


def rewrite(sel, kinds):
    if sel == ":root" or sel == "body":
        return ["body.nw-site"]
    if sel == "html":
        return ["html:has(body.nw-site)"]
    parts = compounds(sel)
    for i, p in enumerate(parts):
        if p == ">" and i + 1 < len(parts):
            tag = re.match(r"^([a-z][a-z0-9]*)", parts[i + 1])
            if tag and tag.group(1) in ELEMENTS:
                parts[i] = " "
    parts = [map_tags(p) if p not in (" ", ">", "+", "~") else p for p in parts]
    subject = parts[-1]
    prefix = "".join(p if p in (" ",) else (" %s " % p if p in (">", "+", "~") else p)
                     for p in parts[:-1])
    out = []
    widget_kind = next((kinds[c] for c in classes_of(subject) if kinds.get(c) in INNER), None)
    if widget_kind:
        base, pseudo = split_pseudo(subject)
        out.append(prefix + base + ":not(.elementor-widget)" + pseudo)
        out.append(prefix + base + " " + INNER[widget_kind] + pseudo)
    else:
        out.append(prefix + subject)
    return [SCOPE + s for s in out]


def port_rules(css, kinds, stats):
    res = []
    for prelude, body in blocks(css):
        if prelude.startswith("@media") or prelude.startswith("@supports"):
            inner = port_rules(body, kinds, stats)
            if inner.strip():
                res.append("%s {\n%s}\n" % (prelude, inner))
            continue
        if prelude.startswith("@"):
            res.append("%s {%s}\n" % (prelude, body))
            continue
        sels = split_top(prelude)
        if sels == ["*", "*::before", "*::after"]:      # Hello Elementor already sets border-box
            stats["dropped"] += 1
            continue
        new, bumped, wrappers = [], [], []
        for s in sels:
            s = " ".join(s.split())
            r = rewrite(s, kinds)
            if len(r) > 1:
                stats["retargeted"] += 1
                base, pseudo = split_pseudo(r[0].replace(":not(.elementor-widget)", ""))
                if not pseudo:
                    wrappers.append(base + ".elementor-widget")
            new.extend(r)
            subj = compounds(s)[-1] if compounds(s) else ""
            if any(kinds.get(c) in ("text", "image") for c in classes_of(subj)):
                base, pseudo = split_pseudo(r[-1])
                bumped.append(base + ".elementor-element.elementor-widget" + pseudo)
        decl = " ".join(body.split())
        res.append("%s {\n  %s\n}\n" % (",\n".join(new), decl))
        disp = re.findall(r"(?:^|;)\s*display\s*:\s*([^;]+)", body)
        if wrappers and disp:
            res.append("%s {\n  display: %s;\n}\n" % (",\n".join(wrappers),
                                                      "none" if disp[-1].strip() == "none" else "block"))
        mw = re.findall(r"(?:^|;)\s*(max-width\s*:[^;]+)", body)
        if bumped and mw:
            res.append("%s {\n  %s;\n}\n" % (",\n".join(bumped), mw[-1].strip()))
            stats["bumped"] += 1
        stats["rules"] += 1
    return "".join(res)


def main():
    kinds = load_manifest()
    stats = {"rules": 0, "retargeted": 0, "dropped": 0, "bumped": 0}
    src = open(SRC, encoding="utf-8").read()
    proto = strip_comments(re.search(r"<style>(.*?)</style>", src, re.S).group(1))
    sprite = re.search(r'(<svg width="0" height="0".*?</svg>)', src, re.S).group(1)
    adapter = open(os.path.join(PLUGIN, "css", "src", "adapter.css"), encoding="utf-8").read()
    overrides = open(os.path.join(PLUGIN, "css", "src", "overrides.css"), encoding="utf-8").read()
    ported = port_rules(proto, kinds, stats)
    header = (
        "/* newman-core.css -- GENERATED by projects/newman-air/tools/port-css.py. Do not edit.\n"
        "   Edit design-source/v2-1/index.html (the prototype), assets/css/src/adapter.css or\n"
        "   assets/css/src/overrides.css, then re-run the porter and deploy-plugin.sh. */\n\n")
    out = header + adapter + "\n/* ---- V2.1 prototype stylesheet (ported) ---- */\n" + ported + "\n" + overrides
    with open(os.path.join(PLUGIN, "css", "newman-core.css"), "w", encoding="utf-8") as f:
        f.write(out)
    with open(os.path.join(PLUGIN, "icons", "newman-sprite.svg"), "w", encoding="utf-8") as f:
        f.write(sprite + "\n")
    print("wrote newman-core.css: %d rules ported, %d retargeted to inner widget elements, %d dropped; "
          "%d max-width restated; %d widget classes in manifest; sprite %d symbols"
          % (stats["rules"], stats["retargeted"], stats["dropped"], stats["bumped"], len(kinds),
             sprite.count("<symbol")))


if __name__ == "__main__":
    main()
