#!/usr/bin/env python3
"""
Newman Air: Theme Builder single-post template for the migrated blog.

Same bands as the inner pages (pages/inner/build.py): compact hero with the post
title and date, article column (featured image + post content) with the sidebar,
Bear Necessities and the final CTA. Post content is the clean HTML written by
tools/make-blog.py; the `.prose` rules in inner.css style it.

Run:  python projects/newman-air/pages/blog/build.py
Then: W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/blog/single-post.json newman-single-post include/singular/post
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("inner_build", os.path.join(os.path.dirname(HERE), "inner", "build.py"))
I = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(I)
B = I.B


def tag(name):
    return '[elementor-tag id="%s" name="%s" settings="%%7B%%7D"]' % (B.E.nid()[-7:], name)


def build():
    B.reset(0x61000000)
    title = B.E.widget("theme-post-title", {"__dynamic__": {"title": tag("post-title")}, "header_size": "h1"},
                       classes="post-h1")
    meta = B.E.widget("post-info", {"view": "inline", "icon_list": [
        {"_id": "nwdate1", "type": "date", "selected_icon": {"value": "", "library": ""}},
        {"_id": "nwterm1", "type": "terms", "taxonomy": "category", "selected_icon": {"value": "", "library": ""}},
    ]}, classes="post-meta")
    crumbs = B.raw('<nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="/">Home</a></li>'
                   '<li><a href="/blog/">Blog</a></li></ol></nav>')
    hero = B.section("hero page-hero topo grain on-dark compact solo post-hero", [
        B.box("wrap", [B.box("", [crumbs, B.eyebrow("Newman Air Blog"), title, meta])]),
        B.raw(I.RIDGES)])
    body = B.box("prose", [
        B.E.widget("theme-post-featured-image", {"__dynamic__": {"image": tag("post-featured-image")},
                                                 "image_size": "large"}, classes="post-thumb"),
        B.E.widget("theme-post-content", {}, classes="post-body"),
    ])
    article = B.section("article", [B.box("wrap", [body, I.sidebar(None, "service")])])
    final = I.final("Reliable Home Comfort Is Just a Call or Click Away", [
        "From simple repairs to full system replacements, we bring honest answers and upfront pricing to every doorstep "
        "in the Tri-Cities. Give our friendly team a call or book your service visit online in just a few clicks."])
    doc = {"version": "0.4", "title": "Newman Air Single Post (V2.1)", "type": "single-post",
           "content": [hero, article, I.club(), final],
           "page_settings": {}}
    out = os.path.join(HERE, "single-post.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    B.write_manifest(os.path.join(HERE, "widget-classes.json"))
    print("wrote", out)


if __name__ == "__main__":
    build()
