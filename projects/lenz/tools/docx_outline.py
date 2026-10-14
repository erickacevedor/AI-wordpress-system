#!/usr/bin/env python3
"""
Read a Lenz page doc (.docx) into a normalised outline, so a page build takes its
copy straight from the doc instead of a hand transcription.

  outline = read("source.docx")
  outline["meta"]      {"title", "description", "slug"}
  outline["h1"]        the page H1
  outline["hero"]      nodes between the H1 and the first section heading
  outline["sections"]  [{"title", "nodes"}] one per section heading
  node = {"t": "p" | "li" | "h" | "table" | "button" | "note", ...}

Heading levels differ from doc to doc (one uses Heading2 for sections and
Heading3 for items, another Heading3 and Heading4), so they are ranked: the
first heading is the H1, the next level used is the section level, deeper ones
are items (`{"t": "h"}` nodes inside a section). Inline bold survives as <b>.
Word comments are returned in outline["comments"] with the text they anchor.

Run:  python3 projects/lenz/tools/docx_outline.py <doc.docx>   (prints the outline)
"""
import html
import re
import sys
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _runs(p_xml):
    out = []
    for r in re.findall(r"<w:r[ >].*?</w:r>", p_xml, re.S):
        t = "".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", r))
        if "<w:tab/>" in r:
            t += " "
        if not t:
            continue
        bold = bool(re.search(r"<w:b/>|<w:b w:val=\"(?:1|true)\"/>", r))
        out.append((html.unescape(t), bold))
    return out


def _inline(runs, keep_bold=True):
    s, open_b = "", False
    for t, b in runs:
        t = html.escape(t, quote=False)
        if keep_bold and b and not open_b and t.strip():
            s += "<b>"
            open_b = True
        elif open_b and not b:
            s += "</b>"
            open_b = False
        s += t
    if open_b:
        s += "</b>"
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("<b> ", " <b>").replace(" </b>", "</b> ")
    # A bold lead-in sentence sometimes runs straight into the next word in the doc.
    return re.sub(r"([.:!?])</b>(?=[A-Za-z0-9])", r"\1</b> ", s)


def _plain(s):
    return re.sub(r"<[^>]+>", "", s)


def read(path):
    z = zipfile.ZipFile(path)
    doc = z.read("word/document.xml").decode("utf8")
    body = doc[doc.index("<w:body>"):]
    nodes = []
    for m in re.finditer(r"<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>", body, re.S):
        x = m.group(0)
        if x.startswith("<w:tbl>"):
            rows = []
            for tr in re.findall(r"<w:tr[ >].*?</w:tr>", x, re.S):
                rows.append([_inline(_runs(tc), keep_bold=False) for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, re.S)])
            nodes.append({"t": "table", "rows": rows})
            continue
        style = re.search(r'<w:pStyle w:val="([^"]+)"', x)
        style = style.group(1) if style else ""
        runs = _runs(x)
        txt = _inline(runs)
        if not _plain(txt).strip():
            continue
        lvl = re.match(r"Heading(\d)", style) or (re.match(r"(?:Title)()", style) and re.match(r"(1)", "1"))
        if lvl and _plain(txt).strip().lower() in ("seo metadata", "trust bar notes"):
            continue
        if lvl:
            nodes.append({"t": "hx", "lvl": int(lvl.group(1)), "text": _plain(txt)})
        elif "<w:numPr>" in x:
            nodes.append({"t": "li", "text": txt})
        else:
            nodes.append({"t": "p", "text": txt})

    # Meta lines sit in the first few nodes, as paragraphs or headings, one per
    # line or several run together ("URL: /x/ Meta Title: ... Meta Description: ...").
    meta, kept = {}, []
    label = r"(?:SEO Title|Meta Title|Title|Meta Description|Description|URL Slug|URL|Slug)\s*:"
    for i, n in enumerate(nodes):
        raw = _plain(n.get("text", "")) if n["t"] != "table" else ""
        if i < 10 and re.match(r"\s*" + label, raw, re.I):
            for k, v in re.findall(r"(" + label + r")\s*(.*?)(?=\s*" + label + r"|$)", raw, re.I):
                k = k.lower().rstrip(":").strip()
                k = "slug" if ("url" in k or "slug" in k) else ("description" if "description" in k else "title")
                meta[k] = v.strip()
            continue
        kept.append(n)
    nodes = kept

    # Split buttons and notes out of plain paragraphs.
    clean = []
    for n in nodes:
        if n["t"] in ("p", "li"):
            raw = _plain(n["text"])
            if raw.strip().lower() in ("seo metadata", "trust bar notes"):
                continue
            # buttons: [ Label ] possibly several on one line, maybe with a trailing note
            notes = re.findall(r"\((?:Note|note|Nota|nota)[^)]*\)", raw)
            rest = re.sub(r"\((?:Note|note|Nota|nota)[^)]*\)", "", raw).strip()
            if re.fullmatch(r"\(.*\)", rest) or re.match(r"(?i)(map section note|design note)\s*:", rest):
                clean.append({"t": "note", "text": rest})
                continue
            path = re.search(r"\]\s*\((/[^)]*)\)\s*$", rest)
            rest = re.sub(r"(\])\s*\((/[^)]*)\)\s*$", r"\1", rest)
            rest = re.sub(r"(\])\s*[–-]\s*link to .*$", r"\1", rest)
            hint = re.search(r"\((?:link|Link) to ([^)]*)\)", rest)
            rest = re.sub(r"\s*\((?:link|Link) to [^)]*\)", "", rest).strip()
            btns = re.findall(r"\[\s*([^\]]+?)\s*\]", rest)
            if btns and not re.sub(r"\[[^\]]*\]", "", rest).strip():
                clean.append({"t": "button", "labels": btns,
                              "hint": path.group(1) if path else (hint.group(1) if hint else "")})
                for nt in notes:
                    clean.append({"t": "note", "text": nt})
                continue
            if notes and not rest:
                for nt in notes:
                    clean.append({"t": "note", "text": nt})
                continue
            if notes:
                n = dict(n, text=re.sub(r"\s*\((?:Note|note)[^)]*\)", "", n["text"]).strip())
                clean.append(n)
                for nt in notes:
                    clean.append({"t": "note", "text": nt})
                continue
        clean.append(n)

    # Rank heading levels: first heading = H1, next distinct level = section.
    heads = [n for n in clean if n["t"] == "hx"]
    out = {"meta": meta, "h1": "", "hero": [], "sections": [], "comments": comments(z, doc)}
    if not heads:
        out["hero"] = clean
        return out
    h1 = heads[0]
    out["h1"] = h1["text"]
    deeper = sorted({n["lvl"] for n in heads[1:]})
    sec_lvl = deeper[0] if deeper else None
    cur = None
    started = False
    for n in clean:
        if n is h1:
            started = True
            continue
        if not started:
            continue
        if n["t"] == "hx" and n["lvl"] <= (sec_lvl or 0) and n["lvl"] != h1["lvl"]:
            cur = {"title": n["text"], "nodes": []}
            out["sections"].append(cur)
            continue
        if n["t"] == "hx" and n["lvl"] == h1["lvl"]:
            # a second H1-level heading (some docs repeat the level): treat as section
            cur = {"title": n["text"], "nodes": []}
            out["sections"].append(cur)
            continue
        if n["t"] == "hx":
            n = {"t": "h", "text": n["text"]}
        (cur["nodes"] if cur else out["hero"]).append(n)
    return out


def comments(z, doc):
    if "word/comments.xml" not in z.namelist():
        return []
    x = z.read("word/comments.xml").decode("utf8")
    res = []
    for attrs, body in re.findall(r"<w:comment\b([^>]*)>(.*?)</w:comment>", x, re.S):
        cid = re.search(r'w:id="(\d+)"', attrs).group(1)
        m = re.search(r'<w:commentRangeStart w:id="%s"/>(.*?)<w:commentRangeEnd w:id="%s"/>' % (cid, cid), doc, re.S)
        anchor = html.unescape("".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", m.group(1)))) if m else ""
        res.append({"text": html.unescape("".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", body))).strip(),
                    "anchor": anchor.strip()})
    return res


def show(o):
    print("META", o["meta"])
    print("H1  ", o["h1"])
    for n in o["hero"]:
        print("  hero", n["t"], (n.get("text") or n.get("labels") or "")[:110] if n["t"] != "table" else len(n["rows"]))
    for i, s in enumerate(o["sections"]):
        print("S%d  %s" % (i, s["title"]))
        for n in s["nodes"]:
            v = n.get("text") or n.get("labels") or ("%d rows x %d" % (len(n["rows"]), len(n["rows"][0])) if n["t"] == "table" else "")
            print("     %-6s %s" % (n["t"], str(v)[:120]))
    for c in o["comments"]:
        print("COMMENT %s :: %s" % (c["text"], c["anchor"][:80]))


if __name__ == "__main__":
    show(read(sys.argv[1]))
