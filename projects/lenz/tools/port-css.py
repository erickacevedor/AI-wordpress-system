#!/usr/bin/env python3
"""
Port the approved prototype stylesheet into lenz-core.

  in:  design-source/v6-1/tokens.css, design-source/v6-1/css/lenz-v6-1.css
       pages/*/widget-classes.json     (written by each build.py via brand.py)
       plugin/lenz-core/assets/css/src/adapter.css, overrides.css
  out: plugin/lenz-core/assets/css/lenz-core.css

What the port does to every prototype rule, and why:

  1. Prefix with `.elementor `. Scopes the prototype to Elementor content (pages
     and Theme Builder parts) and lifts every rule one class above Elementor's own
     base rules (`.e-con`, `.e-con-full.e-flex`, ...), which load earlier.
  2. Re-target classes that sit on native widgets. Elementor puts a widget's CSS
     class on the wrapper, so `.section__title {...}` would style the <div>, not
     the <h2>. For classes the build placed on heading or button widgets the
     subject is rewritten to the inner element (`.elementor-heading-title`,
     `.elementor-button`), keeping a `:not(.elementor-widget)` copy for the same
     class used inside html widgets. Text and image widgets keep the class on the
     wrapper on purpose: text inherits through it, and the adapter makes an image
     fill its wrapper.
  3. Map tags a container cannot render. `li` becomes `:is(li, .lz-li)`, and the
     same for ul, figure, figcaption, blockquote and span (see brand.py).
  4. A child combinator whose right side is a bare element (`.about__body>p`)
     becomes a descendant combinator, because a widget wrapper now sits between.
  5. Asset URLs move from the prototype tree to the plugin tree.

Global resets that would leak into WordPress (`* { margin: 0 }`) are dropped; the
adapter carries a scoped version.

Run:  python3 projects/lenz/tools/port-css.py
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = os.path.join(SITE, "design-source", "v6-1")
PLUGIN_CSS = os.path.join(SITE, "plugin", "lenz-core", "assets", "css")

INNER = {"heading": ".elementor-heading-title", "button": ".elementor-button"}
LZ_TAGS = ("ul", "li", "figure", "figcaption", "blockquote", "span")
ELEMENTS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "img", "ul", "li", "span", "svg", "b",
            "small", "figure", "blockquote", "figcaption", "iframe"}
KEEP_AS_IS = re.compile(r"^(:root|html|body)\b")


def load_manifest():
    kinds = {}
    for path in sorted(glob.glob(os.path.join(SITE, "pages", "*", "widget-classes.json"))):
        for cls, kind in json.load(open(path, encoding="utf-8")).items():
            if kinds.get(cls, kind) != kind:
                raise SystemExit("class %r is %s in one page and %s in another" % (cls, kinds[cls], kind))
            kinds[cls] = kind
    return kinds


# ------------------------------------------------------------- CSS reading ----
def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def blocks(css):
    """Yield (prelude, body) for each top-level block, body raw."""
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
    """Split on `sep` outside parentheses, brackets and quotes."""
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


# -------------------------------------------------------- selector rewrite ----
_COMB = re.compile(r"\s*([>+~])\s*|\s+")


def compounds(sel):
    """['.a', ' ', '.b', '>', 'p'] -- compounds interleaved with combinators,
    respecting parentheses."""
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
    # collapse leading/duplicate combinators
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
    # classes outside :not(...)/:is(...) arguments only
    base = re.sub(r"\([^)]*\)", "", compound)
    return re.findall(r"\.([A-Za-z0-9_-]+)", base)


def split_pseudo(compound):
    """'.btn-gold:hover::before' -> ('.btn-gold', ':hover::before')."""
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
    if KEEP_AS_IS.match(sel):
        return [sel]
    parts = compounds(sel)
    # The prototype's <html class="on-dark"> is always true. `:root` keeps the
    # rule's specificity, so it still outranks the rules it outranked before.
    if parts and parts[0] == ".on-dark":
        parts[0] = ":root"
    # 4. child combinator onto a bare element -> descendant
    for i, p in enumerate(parts):
        if p == ">" and i + 1 < len(parts):
            tag = re.match(r"^([a-z][a-z0-9]*)", parts[i + 1])
            if tag and tag.group(1) in ELEMENTS:
                parts[i] = " "
    # 3. tags a container cannot render
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
    return [(s.replace(":root ", ":root .elementor ", 1) if s.startswith(":root ")
             else ".elementor " + s) for s in out]


def port_rules(css, kinds, stats):
    res = []
    for prelude, body in blocks(css):
        if prelude.startswith("@media") or prelude.startswith("@supports"):
            inner = port_rules(body, kinds, stats)
            if inner.strip():
                res.append("%s {\n%s}\n" % (prelude, inner))
            continue
        if prelude.startswith("@"):           # @keyframes, @font-face: verbatim
            res.append("%s {%s}\n" % (prelude, body))
            continue
        sels = split_top(prelude)
        if sels == ["*"] and re.fullmatch(r"\s*margin\s*:\s*0;?\s*", body):
            stats["dropped"] += 1
            continue
        new, bumped, wrappers = [], [], []
        for s in sels:
            s = " ".join(s.split())
            r = rewrite(s, kinds)
            if len(r) > 1:
                stats["retargeted"] += 1
                # A retargeted `display: none` hides only the inner element; the
                # empty wrapper would still take a flex gap (the nav CTA on mobile).
                # Mirror display onto the wrapper: none stays none, anything else
                # puts the wrapper back to block.
                base, pseudo = split_pseudo(r[0].replace(":not(.elementor-widget)", ""))
                if not pseudo:
                    wrappers.append(base + ".elementor-widget")
            new.extend(r)
            # Elementor caps every widget at max-width:100% with a (0,4,0) rule, which
            # beats a prototype max-width on a text/image widget class. Restate just
            # that property two classes heavier; every such restatement gets the same
            # bump, so their order among themselves is the prototype's.
            subj = compounds(s)[-1] if compounds(s) else ""
            if any(kinds.get(c) in ("text", "image") for c in classes_of(subj)):
                base, pseudo = split_pseudo(r[-1])
                bumped.append(base + ".elementor-element.elementor-widget" + pseudo)
        body = re.sub(r"url\((['\"]?)\.\./assets/img/", r"url(\1../img/", body)
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
    tokens = strip_comments(open(os.path.join(SRC, "tokens.css"), encoding="utf-8").read())
    proto = strip_comments(open(os.path.join(SRC, "css", "lenz-v6-1.css"), encoding="utf-8").read())
    adapter = open(os.path.join(PLUGIN_CSS, "src", "adapter.css"), encoding="utf-8").read()
    overrides = open(os.path.join(PLUGIN_CSS, "src", "overrides.css"), encoding="utf-8").read()
    ported = port_rules(proto, kinds, stats)
    header = (
        "/* lenz-core.css -- GENERATED by projects/lenz/tools/port-css.py. Do not edit.\n"
        "   Edit design-source/v6-1 (the prototype), assets/css/src/adapter.css or\n"
        "   assets/css/src/overrides.css, then re-run the porter and deploy-plugin.sh.\n"
        "   Source: erickacevedor/lenz v6-1 (see design-source/v6-1/SOURCE.txt). */\n\n")
    out = (header + adapter + "\n/* ---- tokens.css (verbatim) ---- */\n" + tokens.strip() + "\n\n"
           "/* ---- lenz-v6-1.css (ported) ---- */\n" + ported + "\n" + overrides)
    path = os.path.join(PLUGIN_CSS, "lenz-core.css")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote %s: %d rules ported, %d retargeted to inner widget elements, %d dropped; "
          "%d max-width restated; %d widget classes in manifest"
          % (path, stats["rules"], stats["retargeted"], stats["dropped"], stats["bumped"], len(kinds)))


if __name__ == "__main__":
    main()
