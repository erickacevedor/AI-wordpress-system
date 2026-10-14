#!/usr/bin/env python3
"""Doc-to-page audit: every sentence, heading, list item, table cell and button of each
page's source.docx must appear on the rendered page, or match a known, documented
difference (EXPECT: ClickUp decisions, placeholders, design notes).

Run: LENZ_URL=http://localhost:10003 python3 projects/lenz/tools/audit-docs.py /tmp/audit.json
"""
import sys, os, re, html, json, subprocess, unicodedata
sys.path.insert(0, "/Volumes/DataStorage/Github/AI-wordpress-system/projects/lenz/tools")
import docx_outline as D
ROOT = "/Volumes/DataStorage/Github/AI-wordpress-system/projects/lenz/pages"

def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"[–—]", "-", t).replace("→", " ").replace("•", " ")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

def sentences(t):
    t = norm(t)
    parts = re.split(r"(?<=[.!?])\s+(?=[a-z0-9\"(])", t)
    return [p.strip(" .") for p in parts if len(p.strip(" .")) > 3]

def units(o):
    out = []  # (kind, text)
    out.append(("h1", norm(o["h1"])))
    def walk(nodes, sec):
        for n in nodes:
            if n["t"] in ("p", "li"):
                for s in sentences(n["text"]): out.append((sec + " · " + n["t"], s))
            elif n["t"] == "h":
                out.append((sec + " · h", norm(n["text"])))
            elif n["t"] == "button":
                for l in n["labels"]: out.append((sec + " · button", norm(l)))
            elif n["t"] == "table":
                for r in n["rows"]:
                    for c in r:
                        if c.strip(): out.append((sec + " · cell", norm(c)))
            elif n["t"] == "note":
                out.append((sec + " · note", norm(n["text"])))
    walk(o["hero"], "hero")
    for s in o["sections"]:
        out.append(("section", norm(s["title"])))
        walk(s["nodes"], s["title"][:40])
    return out

def page_text(slug):
    h = subprocess.run(["curl", "-s", os.environ.get("LENZ_URL", "http://localhost:10003") + "/%s/" % slug], capture_output=True, text=True).stdout
    m = re.search(r'<div data-elementor-type="wp-page".*?(?=<footer|<div data-elementor-type="footer")', h, re.S)
    body = m.group(0) if m else h
    body = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", body)
    body = re.sub(r'(?i)<(?:img|iframe)[^>]*(?:alt|title)="([^"]*)"[^>]*>', r" \1 ", body)
    return norm(body)

res = {}
for slug in sorted(os.listdir(ROOT)):
    src = os.path.join(ROOT, slug, "source.docx")
    if not os.path.exists(src): continue
    o = D.read(src)
    txt = page_text(slug)
    miss = []
    us = units(o)
    for kind, u in us:
        uu = u.strip(" .:")
        if not uu or uu in txt: continue
        # tolerate punctuation differences
        if re.sub(r"[^a-z0-9]", "", uu) in re.sub(r"[^a-z0-9]", "", txt): continue
        miss.append((kind, u))
    res[slug] = {"total": len(us), "missing": miss, "meta": o["meta"], "comments": o["comments"]}
EXPECT = [
 (r"\bnote\b|^\(", "design note / instruction (applied, not page copy)"),
 (r"insert |widget|slider|placeholder|\[button\]|^\[", "placeholder replaced by the real component"),
 (r"^(call|call us|call today|call now|call 24/7|questions\? call)[: ].*225-6446", "call button: site-wide label \"Call (515) 225-6446\""),
 (r"headquarter", "ClickUp 08/17: Main office"),
 (r"second opinion|re-evaluate your system for free|re-inspect it for free|scary quote|expensive quote", "ClickUp 09/10 #6: no free second opinions (card replaced by Free Estimates)"),
 (r"1,800", "ClickUp 08/17: 2,000 reviews"),
 (r"free estimates on every request", "ClickUp 09/10 #6: free estimates only on new equipment and replacements"),
 (r"parts and repairs|parts & repair|any repairs you need", "ClickUp 09/10 #7: discount on parts only"),
 (r"maintenance visits|^\d+ ?(1⁄2|½)? ?years?$|^within \d+ hours|consecutively enrolled", "ClickUp 09/10 #8-9: plans shown with the approved home cards (year spelled out, loyalty wording reworked)"),
 (r" - .*manager| - service technicians| - office assistants|^keystone, max|^office team", "roster: shown as one card per person (doc comment)"),
 (r"is located at:$|areas include:$|for immediate help, call", "lead-in replaced by the address / list / button it introduced"),
 (r", ia$", "city chip without \", IA\""),
 (r"\[ browse our full video library \]", "video library shown on the page instead of a link"),
 (r"locationlenz heating & cooling", "office card: city, address and Get Directions"),
 (r"^get a free estimate$|^book online$", "second hero/close button: site-wide Call button + estimate form"),
]
def classify(u):
    for pat, why in EXPECT:
        if re.search(pat, u): return why
    return None
for slug, r in res.items():
    r["real"] = [(k, u) for k, u in r["missing"] if not classify(u)]
    r["expected"] = [(k, u, classify(u)) for k, u in r["missing"] if classify(u)]
json.dump(res, open(sys.argv[1], "w"), indent=1)
for slug, r in res.items():
    print("%-24s units=%4d  expected=%3d  REAL=%2d  %s" % (slug, r["total"], len(r["expected"]), len(r["real"]),
          " | ".join(u[:70] for k, u in r["real"])))
