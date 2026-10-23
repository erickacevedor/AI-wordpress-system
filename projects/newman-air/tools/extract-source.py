"""Extract the page content of the old callbestinshow.com pages into Markdown outlines.

Reads content/source/html/*.html (public HTML of each page) and writes
content/source/md/<page>.md: SEO head (title, description, canonical), then every
Elementor widget inside the page document (header/footer templates skipped) in DOM
order, grouped by top-level section/container.

    python projects/newman-air/tools/extract-source.py
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup, NavigableString

ROOT = pathlib.Path(__file__).resolve().parent.parent / "content" / "source"
SRC = ROOT / "html"
OUT = ROOT / "md"


def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


def rich(el):
    """Text editor content as Markdown-ish lines (paragraphs, lists, inline links kept)."""
    lines = []
    for node in el.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        if node.find_parent("li") and node.name != "li":
            continue
        t = inline(node)
        if not t:
            continue
        first = next((c for c in node.children if not (isinstance(c, NavigableString) and not c.strip())), None)
        if node.name == "p" and getattr(first, "name", None) == "strong" and first.find_next_sibling("br"):
            title = text(first)
            rest = inline(node)[len(title):].lstrip(" /")
            lines.append(f"[card] {title} | {rest}")
            continue
        if node.name == "li":
            lines.append(f"- {t}")
        elif node.name.startswith("h"):
            lines.append(f"{'#' * int(node.name[1])} {t}")
        else:
            lines.append(t)
    if not lines:
        t = text(el)
        if t:
            lines.append(t)
    return lines


def inline(node):
    parts = []
    for c in node.descendants:
        if isinstance(c, NavigableString):
            if c.find_parent("a") and c.find_parent("a") in node.descendants:
                continue
            parts.append(str(c))
        elif c.name == "a":
            parts.append(f"[{text(c)}]({c.get('href', '')})")
        elif c.name == "br":
            parts.append(" / ")
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def widget(w):
    kind = w.get("data-widget_type", "").split(".")[0]
    out = []
    if kind == "heading":
        h = w.find(re.compile(r"^(h[1-6]|p|div|span)$"), class_="elementor-heading-title") or w
        tag = h.name if h.name.startswith("h") else "p"
        out.append(f"[{tag}] {text(h)}")
    elif kind == "text-editor":
        out += rich(w)
    elif kind == "button":
        a = w.find("a")
        out.append(f"[button] {text(w)} -> {a.get('href', '') if a else ''}")
    elif kind == "icon-list":
        for li in w.select(".elementor-icon-list-item"):
            a = li.find("a")
            out.append(f"- {text(li)}" + (f" -> {a.get('href')}" if a else ""))
    elif kind == "icon-box":
        t = w.select_one(".elementor-icon-box-title")
        d = w.select_one(".elementor-icon-box-description")
        out.append(f"[icon-box] **{text(t) if t else ''}**: {text(d) if d else ''}")
    elif kind == "image":
        img = w.find("img")
        if img:
            out.append(f"[image] {img.get('src', '')} alt=\"{img.get('alt', '')}\"")
    elif kind == "nested-accordion":
        for item in w.select("details, .e-n-accordion-item"):
            q = item.select_one("summary, .e-n-accordion-item-title")
            body = item.select_one(".e-con, [role=region]")
            out.append(f"**Q: {text(q) if q else ''}**")
            if body:
                out += ["A: " + l for l in rich(body)]
    elif kind == "form":
        fields = []
        for f in w.select(".elementor-field-group"):
            lab = f.find("label")
            inp = f.find(["input", "textarea", "select"])
            if inp is None or inp.get("type") == "hidden":
                continue
            name = text(lab) if lab else inp.get("placeholder", "")
            req = "*" if inp.has_attr("required") or "elementor-field-required" in f.get("class", []) else ""
            fields.append(f"{name}{req} ({inp.name if inp.name != 'input' else inp.get('type')})")
        btn = w.select_one("button")
        fid = w.find("input", attrs={"name": "form_id"})
        out.append(f"[form] fields: {', '.join(fields)} | submit: {text(btn) if btn else ''} | form_id: {fid.get('value') if fid else ''}")
    elif kind in ("shortcode", "html"):
        t = text(w)
        out.append(f"[{kind}] {t[:300]}" if t else f"[{kind}] (no text)")
    elif kind == "template":
        out.append(f"[template] {text(w)[:200]}")
    elif kind == "icon":
        pass
    else:
        t = text(w)
        if t:
            out.append(f"[{kind}] {t[:300]}")
    return out


def page(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "lxml")
    head = []
    title = soup.find("title")
    head.append(f"- title: {text(title) if title else ''}")
    for name in ("description",):
        m = soup.find("meta", attrs={"name": name})
        head.append(f"- {name}: {m.get('content', '') if m else ''}")
    c = soup.find("link", rel="canonical")
    head.append(f"- canonical: {c.get('href') if c else ''}")
    rob = soup.find("meta", attrs={"name": "robots"})
    head.append(f"- robots: {rob.get('content') if rob else ''}")
    doc = soup.select_one('[data-elementor-post-type="page"]')
    body = []
    if doc is None:
        body.append("(no Elementor page document found)")
    else:
        pid = doc.get("data-elementor-id")
        head.append(f"- elementor id: {pid}")
        tops = [e for e in doc.find_all(attrs={"data-element_type": True}, recursive=True)
                if e.get("data-element_type") in ("section", "container")
                and not e.find_parent(attrs={"data-element_type": ["section", "container"]})]
        for i, sec in enumerate(tops, 1):
            body.append(f"\n## Section {i}")
            for t in sec.select('[data-elementor-post-type="elementor_library"]'):
                t.insert(0, soup.new_string(""))
                body.append(f"[global template {t.get('data-elementor-id')} starts]")
            for w in sec.find_all(attrs={"data-element_type": "widget"}):
                if w.find_parent(attrs={"data-widget_type": re.compile("nested-accordion")}):
                    continue
                body += widget(w)
    schema = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except ValueError:
            continue
        for node in (data.get("@graph", [data]) if isinstance(data, dict) else data):
            if isinstance(node, dict):
                schema.append(str(node.get("@type")))
    head.append(f"- schema types: {', '.join(schema)}")
    return "# " + path.stem.replace("__", "/") + "\n\n" + "\n".join(head) + "\n" + "\n".join(body) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in sorted(SRC.glob("*.html")):
        if p.stat().st_size == 0:
            continue
        (OUT / (p.stem + ".md")).write_text(page(p), encoding="utf-8")
        print(p.stem)


if __name__ == "__main__":
    main()
