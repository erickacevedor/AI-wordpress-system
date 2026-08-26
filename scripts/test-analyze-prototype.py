#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regression tests for scripts/analyze-prototype.py.

This script shipped without ever having been run against a real prototype: every
site in projects/ arrived with an Elementor kit, and projects/lenz was onboarded by
hand before the script existed. The first real prototype it met (a hand-written
static site, pages named index.php, no --text-*/--space-* tokens) exposed a class of
bug the token-first fixtures never could.

So the fixtures here come in two shapes, and both must keep working:

  TOKEN_FIRST  a design system expressed as custom properties -- what the master
               prompt in design-source/prompts/ produces.
  HANDWRITTEN  semantic variable names, the rest of the system in the rules -- what
               a real client prototype looks like.

Usage:  python3 scripts/test-analyze-prototype.py
Exit code: 0 = every check behaved, 1 = a regression.
"""
import importlib.util
import os
import shutil
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "ap", os.path.join(ROOT, "scripts", "analyze-prototype.py"))
ap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ap)

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import site_tokens as ST  # noqa: E402


TOKEN_FIRST_CSS = """
:root{
  --brand-50:#eef6ff; --brand-500:#1d6fe0; --brand-900:#0b2c5c;
  --neutral-0:#ffffff; --neutral-900:#141822;
  --color-text-primary: var(--neutral-900);
  --color-primary: var(--brand-500);
  --font-heading:'Poppins',sans-serif; --font-body:'Inter',sans-serif;
  --text-base:1rem; --text-4xl:3.5rem;
  --space-4:16px; --space-16:64px;
  --radius-md:8px;
  --container:1200px;
}
"""

# The shapes that broke the script. Every line here is a real pattern from the
# em-midlakes prototype, reduced.
HANDWRITTEN_CSS = """
:root{
  --brand-red:#c10a0a;
  --red: var(--brand-red);
  --red-dark:#a30808;
  --blue:#2540af;
  --ink:#0f1f35;
  --ink-2:#17293f;
  --paper:#f4f6f9;
  --white:#ffffff;
  --text:#1a2436;
  --radius:14px;
  --container:1200px;
  --max-width:1800px;
  --font-sans:'Manrope', system-ui, sans-serif;
  --font-serif:'Fraunces', Georgia, serif;
}
body { font-family: var(--font-sans); color: var(--text); }
h1 { font-size: clamp(2.4rem, 5.2vw, 4rem); }
.section { padding: 96px 0; }
.about { background: var(--white); }
.services { background: var(--paper); }
.contact { background: var(--ink); }
.quote-form { background: var(--ink-2); }
.chip { background: var(--white); }
.btn { border-radius: 999px; padding: 14px 26px; font-weight: 700; }
.btn-primary { background: var(--red); color: var(--white); }
.btn-primary:hover { background: var(--red-dark); transform: translateY(-2px); }
.hero-media img { background-image: url("data:image/svg+xml,%3Csvg;x%3E"); }
@media (max-width: 620px) { .section { padding: 64px 0; } }
"""

HANDWRITTEN_PAGE = """<!DOCTYPE html><html><body>
<header class="site-header"></header>
<main>
  <section class="section about"><a class="btn btn-primary">Go</a></section>
  <section class="section services"><span class="chip">Athens</span></section>
  <section class="section contact"><form class="quote-form"></form></section>
</main>
</body></html>"""


def make(tmp, css, pages=None):
    d = os.path.join(tmp, "proto")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "styles.css"), "w", encoding="utf-8") as fh:
        fh.write(css)
    for name, body in (pages or {}).items():
        p = os.path.join(d, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
    return d


results = []


def check(label, got, want, how="=="):
    ok = (got == want) if how == "==" else (want in got)
    results.append(ok)
    print("%-46s %s  got=%r" % (label, "PASS" if ok else "FAIL", got))
    return ok


tmp = tempfile.mkdtemp(prefix="ap-test-")
try:
    # ---------------------------------------------------------- handwritten
    d = make(tmp, HANDWRITTEN_CSS,
             {"index.php": HANDWRITTEN_PAGE,
              "services/index.php": HANDWRITTEN_PAGE})
    f = ap.analyze(d)
    r = f["rules"]

    # 1. .php pages are pages. Judging by extension reported "0 HTML files" for a
    #    six-page prototype whose files hold not one <?php tag.
    check("php pages counted", len(f["html_files"]), 2)

    # 2. `--radius: 14px` -- a bare name the trailing-dash prefix never matched.
    check("bare --radius classified as a radius",
          "--radius" in f["groups"]["radius"], True)

    # 3. `--ink-2` is a second ink, not "ramp ink, step 2".
    check("--ink-2 is not a false ramp", "ink" in f["ramps"], False)
    check("--ink-2 kept as a role", "--ink-2" in f["roles"], True)

    # 4. A hex value is a colour whatever the name suggests: `--text` must not be
    #    swallowed by the --text- type-scale prefix.
    check("--text stays a colour role", f["roles"].get("--text", {}).get("value"),
          "#1a2436")

    # 5. The button spec IS derivable from a stylesheet.
    check("button radius read from rules",
          r["button"]["base"].get("border-radius"), "999px")
    check("button fill resolved through var()",
          r["button"]["primary"].get("background"), "#c10a0a")
    check("button hover fill read", r["button"]["hover"].get("background"), "#a30808")
    check("hover animation recorded",
          r["button"]["hover"].get("transform"), "translateY(-2px)")

    # 6. A band is a class the markup puts on a <section>. Components that merely
    #    have a background must not become bands.
    check("bands are the three section bands", sorted(r["bands"]),
          ["ink", "paper", "white"])
    check(".quote-form is not a band",
          any(".quote-form" in e["selectors"] for e in r["bands"].values()), False)
    check(".chip is not a band",
          any(".chip" in e["selectors"] for e in r["bands"].values()), False)

    # 7. Font families come from what the rules assign, not from token names.
    #    --font-sans/--font-serif tell you nothing about which is the heading face.
    check("body family read from the body rule", r["font_families"].get("body"),
          "Manrope")
    check("heading inherits body when unset", r["font_families"].get("heading"),
          "Manrope")

    # 8. Section rhythm, including the mobile override inside @media.
    check("section rhythm desktop", r["section_rhythm"][".section"]["desktop"], 96.0)
    check("section rhythm mobile", r["section_rhythm"][".section"]["mobile"], 64.0)

    # 9. A data: URI holding ';' must not tear the declaration block apart.
    check("data URI did not corrupt parsing", r["rule_count"] >= 12, True)

    doc = ap.emit_tokens(f, "fixture")
    # 10. content_width is deterministic: --container wins over --max-width rather
    #     than whichever dict order put last.
    check("content_width prefers --container", doc["content_width"], 1200)
    check("content_width provenance recorded", doc["_content_width_from"], "--container")
    check("button emitted, not TODO", doc["button"]["bg"], "#c10a0a")
    check("bands emitted", sorted(doc["bands"]), ["ink", "paper", "white"])
    check("fluid h1 keeps both ends", doc["type_scale"].get("h1_mobile"), 38.4)
    check("_roles scaffold emitted", "_roles" in doc, True)

    out = os.path.join(tmp, "hand.json")
    import json
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh)
    check("pipeline can read the emitted seam", ST.load(out).missing_core(), [])
    check("seam self-check agrees", ap._seam_check(out), [])

    # A prototype that never names anything primary-ish cannot have a primary
    # inferred. The seam check must SAY so rather than let the gap ship quietly.
    thin = make(tmp, HANDWRITTEN_CSS.replace("--blue:#2540af;", ""),
                {"index.php": HANDWRITTEN_PAGE})
    doc_thin = ap.emit_tokens(ap.analyze(thin), "thin")
    out_thin = os.path.join(tmp, "thin.json")
    with open(out_thin, "w", encoding="utf-8") as fh:
        json.dump(doc_thin, fh)
    check("seam check reports an un-inferable primary",
          ap._seam_check(out_thin)[0], "colors.primary", how="in")

    # ---------------------------------------------------------- token-first
    shutil.rmtree(os.path.join(tmp, "proto"))
    d = make(tmp, TOKEN_FIRST_CSS, {"index.html": "<html></html>"})
    f2 = ap.analyze(d)
    check("control: ramps still read", sorted(f2["ramps"]), ["brand", "neutral"])
    check("control: roles still read", len(f2["roles"]) >= 2, True)
    check("control: type tokens still read", "--text-4xl" in f2["groups"]["type"], True)
    check("control: spacing tokens still read", "--space-4" in f2["groups"]["space"], True)
    check("control: .html pages still found", f2["html_files"], ["index.html"])

    doc2 = ap.emit_tokens(f2, "fixture2")
    check("control: type_scale from tokens, not rules",
          doc2["type_scale"].get("text-4xl"), 56.0)
    check("control: heading font from --font-heading",
          doc2["fonts"]["heading"], "Poppins")
    out2 = os.path.join(tmp, "tok.json")
    with open(out2, "w", encoding="utf-8") as fh:
        json.dump(doc2, fh)
    check("control: token-first seam readable", ST.load(out2).missing_core(), [])

    # 11. Numeric, not lexicographic, ramp middle. Sorted as strings, "100" lands
    #     before "30" and the middle step is whichever sorted there.
    # Steps chosen to miss the 500/600/400 fast path, so the sort is what is tested:
    # lexicographically "200" < "30" < "700" and the middle would be "30".
    check("ramp base sorts numerically",
          ap._ramp_base({"30": "#aaa", "200": "#bbb", "700": "#ccc"}), "#bbb")
    check("clamp range parsed", ap._clamp_range("clamp(1rem, 2vw, 2rem)"), (16.0, 32.0))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n%d/%d checks passed" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
