"""Turn the old callbestinshow.com page outlines into Newman Air page content.

    in:  content/source/md/<page>.md   (tools/extract-source.py)
    out: content/pages/<key>.json      (read by pages/inner/build.py)
         content/REVIEW.md             (every line the rebrand changed, before/after,
                                        plus any brand or dog term still left)

Scope (DJ's plan doc v2, Phase C, and Erick 2026-10-23): migrate the pages as is and
swap Best in Show for Newman Air. Edits are minimal and listed in REVIEW.md:
  - brand name, dog-show idioms, Winner's Circle -> Bear Necessities;
  - Hearth next to GoodLeap and Synchrony, Ruud next to the brands listed
    (SEO recommendations, ClickUp 86bcajgu4, 10/01);
  - the $75 diagnostic FAQ on the repair pages (86bcajgu6), answer copied from the
    approved homepage FAQ;
  - source typos that are plainly broken markup (a list item split in two).
Dropped from every page: the old global blocks (sidebar menu + form, Winner's Circle
band, reviews shortcode, About teaser); the new templates carry their own.

    python projects/newman-air/tools/make-content.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent / "content"
SRC = ROOT / "source" / "md"
OUT = ROOT / "pages"

# key: (source file stem, new path, page type, WP title)
PAGES = {
    "services": ("services", "services", "hub", "HVAC Services"),
    "ac-installation": ("services__ac-installation", "services/ac-installation", "service", "AC Installation"),
    "ac-repair": ("services__ac-repair", "services/ac-repair", "service", "AC Repair"),
    "air-cleaners": ("services__air-cleaners", "services/air-cleaners", "service", "Air Cleaners"),
    "air-handlers": ("services__air-handlers", "services/air-handlers", "service", "Air Handlers"),
    "commercial": ("services__commercial", "services/commercial", "service", "Commercial HVAC Services"),
    "cooling": ("services__cooling", "services/cooling", "service", "Cooling"),
    "ductless": ("services__ductless", "services/ductless", "service", "Ductless"),
    "ductwork": ("services__ductwork", "services/ductwork", "service", "Ductwork Repair & Installation"),
    "germicidal-lights": ("services__germicidal-lights", "services/germicidal-lights", "service", "Germicidal Lights"),
    "heat-pumps": ("services__heat-pumps", "services/heat-pumps", "service", "Heat Pumps"),
    "heating-installation": ("services__heating-installation", "services/heating-installation", "service", "Heating Installation"),
    "heating-repair": ("services__heating-repair", "services/heating-repair", "service", "Heating Repair"),
    "indoor-air-quality": ("services__indoor-air-quality", "services/indoor-air-quality", "service", "Indoor Air Quality"),
    "maintenance": ("services__maintenance", "services/maintenance", "service", "Maintenance"),
    "thermostats": ("services__thermostats", "services/thermostats", "service", "Thermostats"),
    "service-area": ("service-area", "service-area", "hub", "Service Area"),
    "bristol": ("service-area__bristol", "service-area/bristol", "city", "Bristol"),
    "elizabethton": ("service-area__elizabethton", "service-area/elizabethton", "city", "Elizabethton"),
    "gray": ("service-area__gray", "service-area/gray", "city", "Gray"),
    "greeneville": ("service-area__greeneville", "service-area/greeneville", "city", "Greeneville"),
    "johnson-city": ("service-area__johnson-city", "service-area/johnson-city", "city", "Johnson City"),
    "jonesborough": ("service-area__jonesborough", "service-area/jonesborough", "city", "Jonesborough"),
    "kingsport": ("service-area__kingsport", "service-area/kingsport", "city", "Kingsport"),
    "about-us": ("about-us", "about-us", "about", "About Us"),
    "privacy-policy": ("privacy-policy", "privacy-policy", "legal", "Privacy Policy"),
    "terms-and-conditions": ("terms-and-conditions", "terms-and-conditions", "legal", "Terms and Conditions"),
}

# Pages whose repair FAQs get the $75 diagnostic fee (86bcajgu6: AC, ductwork, heating repair).
FEE_PAGES = {"ac-repair", "ductwork", "heating-repair"}
FEE_FAQ = ("How much do you charge for a diagnostic visit?",
           "Our standard diagnostic fee is <strong>$75</strong>. A technician will inspect your system, find the "
           "issue, and provide a clear, upfront repair estimate before any work starts.")

# Ordered rewrites: (pattern, replacement). Specific phrases first, the bare name last.
REWRITES = [
    # Headlines: neutral, no bear (Erick 2026-10-23; the pages are listed in the ClickUp comment).
    (r"Best-in-Show AC Installation", "Professional AC Installation"),
    (r"Top-Dog AC Repair", "Professional AC Repair"),
    (r"Medal-Worthy AC Services", "Professional AC Services"),
    (r"Finding the Medal-Worthy Cooling Option", "Finding the Right Cooling Option"),
    (r"Ready for Best-in-Show Cooling\?", "Ready for Better Cooling?"),
    (r"Ready for Best-in-Show Ductless Comfort\?", "Ready for Better Ductless Comfort?"),
    (r"About our Best-in-Show Service", "About Our Service"),
    (r"Pure-Bred Comfort Since 1994", "Trusted Comfort Since 1994"),
    (r"Your Comfort Deserves a First-Place Finish", "Your Comfort Deserves a Team You Can Trust"),
    (r"Best [Ii]n Show Heating (&amp;|&|and) Cooling", "Newman Air"),
    (r"That is what best-in-show service means to us", "That is what Newman Air service means to us"),
    (r"\bbest-in-show\b", "bear-strong"),
    (r"\bBest-in-Show\b", "Bear-Strong"),
    (r"\bBest [Ii]n Show\b", "Newman Air"),
    (r"the best service, paws down,", "the best service, hands down,"),
    (r"\bpaws down\b", "hands down"),
    (r"\bTop-Dog\b", "Bear-Strong"),
    (r"\btop-dog\b", "bear-strong"),
    (r"a big-dog headache", "a bigger headache"),
    (r"worthy of a blue ribbon", "worth coming back to"),
    (r"pure-bred", "bear-strong"),
    (r"it’s our pedigree", "it’s in our roots"),
    (r"it's our pedigree", "it's in our roots"),
    (r"Winner[’']s Circle Comfort Club", "Bear Necessities Maintenance Plan"),
    (r"Winner[’']s Circle", "Bear Necessities"),
    (r"worth a standing ovation", "worth recommending to your neighbors"),
    (r"we don’t measure success in trophies or titles", "we don’t measure success in awards or titles"),
    (r"A guarantee that’s more than show", "A guarantee you can count on"),
    (r"Prizewinning Praise", "Reviews &amp; Testimonials"),
    # Public email on Contact and legal pages: dispatch@ (Erick 2026-10-23), as on the homepage.
    (r"office@NewmanHeatAndAir\.com", "dispatch@newmanair.com"),
    (r"https?://(www\.)?callbestinshow\.com/", "https://newmanair.com/"),   # plain-text URLs (Terms)
    # Financing partners: add Hearth (86bcan2a2).
    (r"\bGoodLeap and Synchrony Bank\b", "GoodLeap, Synchrony Bank and Hearth"),
    (r"\bGoodLeap and Synchrony\b", "GoodLeap, Synchrony and Hearth"),
    (r"\bSynchrony and GoodLeap\b", "Synchrony, GoodLeap and Hearth"),
    (r"\bSynchrony &amp; GoodLeap\b", "Synchrony, GoodLeap &amp; Hearth"),
    (r"\bSynchrony & GoodLeap\b", "Synchrony, GoodLeap & Hearth"),
    (r"\bboth Synchrony and GoodLeap\b", "Synchrony, GoodLeap and Hearth"),
    # Brands: add Ruud (86bcajgzg).
    (r"\bDaikin, YORK, Mitsubishi\b", "Ruud, Daikin, YORK, Mitsubishi"),
    (r"\bDaikin®, YORK®, and Mitsubishi\b", "Ruud®, Daikin®, YORK®, and Mitsubishi"),
]
# Left after the rewrites -> listed in REVIEW.md for a person to decide.
LEFTOVER = re.compile(r"best[- ]in[- ]show|winner|pure[- ]?bred|pedigree|ribbon|prize|trophy|trophies|"
                      r"top[- ]dog|\bpaws?\b|\bdogs?\b|walk in the park|first[- ]place|ovation|\bpup|canine|"
                      r"\bkennel|\bleash|\bfetch|\bbark", re.I)

LINK_FIX = [
    (r"https?://(www\.)?callbestinshow\.com", ""),
    (r"/services/mini-splits/", "/services/ductless/"),
]


class Log:
    def __init__(self):
        self.changes = []
        self.left = []

    def rebrand(self, page, s):
        before = s
        for pat, rep in REWRITES:
            s = re.sub(pat, rep, s)
        if s != before:
            self.changes.append((page, before, s))
        for m in LEFTOVER.finditer(s):
            self.left.append((page, s))
            break
        return s


def md_inline(s):
    """[text](url) -> <a>, keep the rest as escaped text (source is already plain)."""
    out, pos = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]*)\)", s):
        out.append(html.escape(s[pos:m.start()], quote=False))
        url = m.group(2)
        for pat, rep in LINK_FIX:
            url = re.sub(pat, rep, url)
        out.append('<a href="%s">%s</a>' % (html.escape(url or "/"), html.escape(m.group(1), quote=False)))
        pos = m.end()
    out.append(html.escape(s[pos:], quote=False))
    return "".join(out).replace(" / ", "<br>")


def fix_link(url):
    for pat, rep in LINK_FIX:
        url = re.sub(pat, rep, url)
    return url or "/"


def parse(stem):
    raw = (SRC / (stem + ".md")).read_text(encoding="utf-8").splitlines()
    head = {}
    for ln in raw:
        m = re.match(r"^- (title|description|canonical): (.*)$", ln)
        if m:
            head[m.group(1)] = m.group(2).strip()
    secs, cur = [], None
    for ln in raw:
        if re.match(r"^## Section \d+$", ln):
            cur = []
            secs.append(cur)
        elif cur is not None and ln.strip():
            cur.append(ln.rstrip())
    return head, secs


def merge_split_items(items):
    """Source bug: one bullet split into two <li> ('Short cycling, where the' / 'system turns on ...')."""
    out = []
    for it in items:
        if out and not re.search(r"[.!?:;)”\"]$", out[-1]) and re.match(r"^[a-z]", it):
            out[-1] = out[-1] + " " + it
        elif out and out[-1].endswith(" Tri") and it.startswith("Cities"):
            out[-1] = out[-1] + "-" + it
        else:
            out.append(it)
    return out


def body_blocks(lines, log, key):
    """Lines of the main content (sidebar and global bands removed) -> blocks."""
    blocks, faq, cur = [], None, None
    in_faq = False
    pending_step = None

    def new_block(h2):
        nonlocal cur
        cur = {"h2": h2, "items": []}
        blocks.append(cur)

    def add(item):
        if cur is None:
            new_block("")
        cur["items"].append(item)

    list_buf = []

    def flush_list():
        if list_buf:
            add({"t": "ul", "items": [md_inline(log.rebrand(key, x)) for x in merge_split_items(list_buf)]})
            list_buf.clear()

    for ln in lines:
        if ln.startswith("- "):
            if in_faq:
                continue
            list_buf.append(ln[2:])
            continue
        flush_list()
        m = re.match(r"^(?:\[h2\] |## )(.*)$", ln)
        if m:
            h = log.rebrand(key, m.group(1).strip())
            if re.match(r"(?i)^frequently asked questions", h):
                in_faq = True
                faq = {"h2": h, "intro": "", "items": []}
                continue
            in_faq = False
            new_block(md_inline(h))
            continue
        if in_faq:
            mq = re.match(r"^\*\*Q: (.*)\*\*$", ln)
            if mq:
                faq["items"].append({"q": log.rebrand(key, mq.group(1)), "a": []})
            elif ln.startswith("A: ") and faq["items"]:
                faq["items"][-1]["a"].append(md_inline(log.rebrand(key, ln[3:])))
            elif not faq["items"]:
                faq["intro"] = md_inline(log.rebrand(key, ln))
            continue
        m = re.match(r"^(?:\[h[3-6]\] |#{3,6} )(.*)$", ln)
        if m:
            add({"t": "h3", "text": md_inline(log.rebrand(key, m.group(1)))})
            continue
        m = re.match(r"^\[p\] (\d+)\. (.*)$", ln)
        if m:
            pending_step = {"title": md_inline(log.rebrand(key, m.group(2))), "html": ""}
            if cur and cur["items"] and cur["items"][-1].get("t") == "steps":
                cur["items"][-1]["items"].append(pending_step)
            else:
                add({"t": "steps", "items": [pending_step]})
            continue
        m = re.match(r"^\[button\] (.*) -> (.*)$", ln)
        if m:
            add({"t": "btn", "label": log.rebrand(key, m.group(1).strip()), "url": fix_link(m.group(2).strip())})
            continue
        m = re.match(r"^\[card\] (.*?) \| (.*)$", ln)
        if m:
            card = {"title": md_inline(log.rebrand(key, m.group(1))), "html": md_inline(log.rebrand(key, m.group(2)))}
            if cur and cur["items"] and cur["items"][-1].get("t") == "cards":
                cur["items"][-1]["items"].append(card)
            else:
                add({"t": "cards", "items": [card]})
            continue
        if ln.startswith("[image]") or ln.startswith("[global template") or ln.startswith("[icon"):
            continue
        if ln.startswith("[p] "):
            add({"t": "h3", "text": md_inline(log.rebrand(key, ln[4:]))})
            continue
        if ln.startswith("["):
            continue
        p = md_inline(log.rebrand(key, ln))
        if cur and cur["items"] and cur["items"][-1].get("t") == "steps" and pending_step and not pending_step["html"]:
            pending_step["html"] = p
            continue
        add({"t": "p", "html": p})
    flush_list()
    return blocks, faq


def split_main(lines):
    """Main content vs the old sidebar template ('explore more' menu + form + Next Step)."""
    main, side = [], []
    target = main
    for ln in lines:
        if ln.startswith("[template] explore more"):
            target = side
            continue
        target.append(ln)
    nxt = None
    for i, ln in enumerate(side):
        if re.match(r"^\[(h6|p)\] Next Step$", ln):
            rest = side[i + 1:]
            h = next((re.sub(r"^\[h\d\] ", "", x) for x in rest if re.match(r"^\[h\d\] ", x)), "")
            t = next((x for x in rest if not x.startswith("[") and not x.startswith("- ")), "")
            nxt = {"h2": h, "text": t}
            break
    return main, nxt


def build(key, log):
    stem, path, ptype, title = PAGES[key]
    head, secs = parse(stem)
    hero = {"eyebrow": "", "h1": "", "paras": []}
    body_lines, nxt = [], None
    for si, sec in enumerate(secs):
        if any(x.startswith("[global template 3802") for x in sec):        # Winner's Circle band
            continue
        if any(re.match(r"^\[p\] (Prizewinning Praise|Reviews)", x) for x in sec):  # reviews shortcode
            continue
        if any(x.startswith("[global template 1406") or x.startswith("[global template 3798") for x in sec):
            if nxt is None:
                _, nxt = split_main(["[template] explore more"] + sec)
            continue
        if not hero["h1"] and any(x.startswith("[h1] ") for x in sec):
            for x in sec:
                if x.startswith("[h1] "):
                    hero["h1"] = log.rebrand(key, x[5:])
                elif re.match(r"^\[(h6|p)\] ", x) and not hero["h1"]:
                    hero["eyebrow"] = log.rebrand(key, re.sub(r"^\[(h6|p)\] ", "", x))
                elif not x.startswith("[") and hero["h1"]:
                    hero["paras"].append(md_inline(log.rebrand(key, x)))
            continue
        main, n = split_main(sec)
        nxt = nxt or n
        body_lines += main
    blocks, faq = body_blocks(body_lines, log, key)
    # The closing CTA: the last block after the FAQ that carries a button.
    cta = None
    if blocks and any(it.get("t") == "btn" for it in blocks[-1]["items"]) and faq:
        last = blocks.pop()
        btn = next(it for it in last["items"] if it.get("t") == "btn")
        cta = {"h2": last["h2"], "paras": [it["html"] for it in last["items"] if it.get("t") == "p"],
               "button": {"label": btn["label"], "url": btn["url"]}}
    if nxt:
        nxt = {"h2": log.rebrand(key, nxt["h2"]), "text": md_inline(log.rebrand(key, nxt["text"]))}
    if faq and key in FEE_PAGES and not any("diagnostic" in i["q"].lower() for i in faq["items"]):
        faq["items"].insert(0, {"q": FEE_FAQ[0], "a": [FEE_FAQ[1]], "added": "86bcajgu6"})
    seo_title = log.rebrand(key, head.get("title", ""))
    seo_title = re.sub(r"\s*[-|]\s*Newman Air$", " | Newman Air", seo_title)
    return {
        "key": key, "path": path, "type": ptype, "title": title,
        "seo": {"title": seo_title, "description": log.rebrand(key, head.get("description", ""))},
        "source": head.get("canonical", ""),
        "hero": hero, "blocks": blocks, "faq": faq, "cta": cta, "next": nxt,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = Log()
    for key in PAGES:
        doc = build(key, log)
        (OUT / (key + ".json")).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print("%-22s blocks=%-2d faq=%-2s cta=%s" % (key, len(doc["blocks"]), len(doc["faq"]["items"]) if doc["faq"] else "-",
                                                      "y" if doc["cta"] else "-"))
    lines = ["# Rebrand review (generated by tools/make-content.py)", "",
             "Every source line the rebrand changed, then anything still matching a brand or dog term.", "",
             "## Still to decide (%d)" % len(log.left), ""]
    seen = set()
    for page, s in log.left:
        if (page, s) in seen:
            continue
        seen.add((page, s))
        lines.append("- **%s**: %s" % (page, s))
    lines += ["", "## Changed (%d)" % len(log.changes), ""]
    for page, a, b in log.changes:
        lines += ["- **%s**" % page, "  - before: %s" % a, "  - after: %s" % b]
    (ROOT / "REVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("review: %d changed, %d left" % (len(log.changes), len(seen)))


if __name__ == "__main__":
    main()
