"""Turn the old callbestinshow.com blog posts into Newman Air posts.

    in:  content/source/html/blog/<slug>.html   (public HTML of each post, gitignored)
         content/source/blog-meta.json          (title, date, category, featured image, Rank Math
                                                 meta; read from the old site with Novamira)
    out: content/blog/<slug>.json               (clean post HTML, read by tools/import-posts.php)
         content/BLOG-REVIEW.md                 (every line the rebrand changed + leftovers)

Same scope as tools/make-content.py (migrate as is, swap the brand, same rewrite rules).
Gutenberg posts: the rendered post content. Elementor posts: their headings, text and FAQ
accordions, in order, as plain HTML (the new single-post template supplies the layout).
Markup is reduced to an allowlist; links to the old domain become relative.

    python projects/newman-air/tools/make-blog.py
"""
import importlib.util
import json
import pathlib
import re

from bs4 import BeautifulSoup, NavigableString, Comment

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent / "content"
SRC = ROOT / "source" / "html" / "blog"
OUT = ROOT / "blog"

_spec = importlib.util.spec_from_file_location("make_content", HERE / "make-content.py")
MC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MC)

KEEP = {"p", "h2", "h3", "h4", "h5", "ul", "ol", "li", "a", "strong", "b", "em", "i", "table", "thead",
        "tbody", "tr", "th", "td", "img", "figure", "figcaption", "blockquote", "br", "sup", "sub"}
ATTRS = {"a": ("href",), "img": ("src", "alt"), "td": ("colspan", "rowspan"), "th": ("colspan", "rowspan")}


def clean(node, log, key):
    """Allowlist tags/attributes, rebrand text, fix links. Returns HTML."""
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in node.find_all(["script", "style", "noscript", "svg", "button", "form", "iframe"]):
        t.decompose()
    for t in list(node.find_all(True)):
        if t.name not in KEEP:
            t.unwrap()
            continue
        keep = ATTRS.get(t.name, ())
        t.attrs = {k: v for k, v in t.attrs.items() if k in keep}
        if t.name == "a" and t.get("href"):
            t["href"] = MC.fix_link(t["href"])
        if t.name == "img" and t.get("src"):
            t["src"] = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", t["src"])  # full size, srcset dropped
            if t.get("alt"):
                t["alt"] = log.rebrand(key, t["alt"])
    for s in list(node.find_all(string=True)):
        if isinstance(s, NavigableString) and s.strip():
            new = log.rebrand(key, str(s))
            if new != str(s):
                s.replace_with(new)
    h = node.decode_contents()
    h = re.sub(r"<(p|li|h\d)>\s*</\1>", "", h)
    return re.sub(r"\n\s*\n+", "\n", h).strip()


def elementor_post(doc, log, key, title):
    parts = []
    for w in doc.select("[data-widget_type]"):
        if w.find_parent(attrs={"data-widget_type": re.compile("nested-accordion")}):
            continue
        kind = w["data-widget_type"].split(".")[0]
        if kind == "heading":
            h = w.select_one(".elementor-heading-title")
            tag = h.name if h.name in ("h2", "h3", "h4", "h5") else ("h2" if h.name == "h1" else "p")
            txt = log.rebrand(key, h.get_text(" ", strip=True))
            if h.name == "h1" or txt == title:
                continue
            parts.append("<%s>%s</%s>" % (tag, txt, tag))
        elif kind == "text-editor":
            parts.append(clean(w.select_one(".elementor-widget-container") or w, log, key))
        elif kind == "nested-accordion":
            for item in w.select("details, .e-n-accordion-item"):
                q = item.select_one("summary, .e-n-accordion-item-title")
                body = item.select_one(".e-con, [role=region]")
                parts.append("<h3>%s</h3>" % log.rebrand(key, q.get_text(" ", strip=True)))
                if body:
                    parts.append(clean(body, log, key))
    return "\n".join(p for p in parts if p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.loads((ROOT / "source" / "blog-meta.json").read_text(encoding="utf-8"))
    log = MC.Log()
    for slug, m in meta.items():
        soup = BeautifulSoup((SRC / (slug + ".html")).read_text(encoding="utf-8"), "lxml")
        title = log.rebrand(slug, m["title"])
        doc = soup.select_one('[data-elementor-type="wp-post"]')
        if doc is not None:
            body, kind = elementor_post(doc, log, slug, title), "elementor"
        else:
            content = soup.select_one(".elementor-widget-theme-post-content .elementor-widget-container") \
                or soup.select_one(".elementor-widget-theme-post-content")
            body, kind = clean(content, log, slug), "gutenberg"
        images = sorted(set(re.findall(r'<img[^>]+src="([^"]+)"', body)))
        post = {
            "slug": slug, "title": title, "date": m["date"], "category": m["cat"][0] if m["cat"] else "",
            "excerpt": log.rebrand(slug, m["excerpt"]), "source_kind": kind,
            "seo_title": log.rebrand(slug, m["seo_title"]).strip(), "seo_description": log.rebrand(slug, m["seo_desc"]).strip(),
            "focus_keyword": m["focus"], "thumb": m["thumb"], "thumb_alt": log.rebrand(slug, m["thumb_alt"]),
            "images": images, "html": body,
        }
        (OUT / (slug + ".json")).write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")
        print("%-58s %-9s %5d words  %d img" % (slug, kind, len(re.sub(r"<[^>]+>", " ", body).split()), len(images)))
    lines = ["# Blog rebrand review (generated by tools/make-blog.py)", "", "## Still to decide", ""]
    seen = set()
    for page, s in log.left:
        if (page, s) not in seen:
            seen.add((page, s))
            lines.append("- **%s**: %s" % (page, s))
    lines += ["", "## Changed (%d)" % len(log.changes), ""]
    for page, a, b in log.changes:
        lines += ["- **%s**" % page, "  - before: %s" % a, "  - after: %s" % b]
    (ROOT / "BLOG-REVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("review: %d changed, %d left" % (len(log.changes), len(seen)))


if __name__ == "__main__":
    main()
