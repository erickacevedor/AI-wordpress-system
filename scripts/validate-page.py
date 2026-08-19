#!/usr/bin/env python3
"""
Pre-import validation gate for an Elementor single-page template.

Runs ALL the invariants a page must satisfy before import — one command, objective
pass/fail — so "done" doesn't depend on remembering a checklist:

  1. Parses as JSON.
  2. Single-page wrapper present: type == "page", a `content` list, `page_settings`.
  3. Unique element ids (no collisions -> imports as new).
  4. Exactly one H1, and a heading hierarchy that doesn't skip levels badly.
  5. No `display_condition_list` (subscriber/visibility gates hide content on import).
  6. No dead or environment-specific links: bare `#`/empty button urls, or
     `localhost` / `127.0.0.1` internal links.  (Intentional `#anchor` links are OK.)
  7. Responsive: delegates to responsive-audit.py (grids/rows/columns/headings/
     containers/images all carry their breakpoint settings).
  8. Section structure: every top-level section is a full-width band holding exactly
     ONE boxed content container, and no boxed container nests inside another.
  9. Alt text: every image widget carries alt text.
 10. Band rhythm (warning): no two adjacent sections share an identical background.
 11. Padding discipline (warning): padding lives on boxed containers and self-contained
     cards -- not on nested layout rows/columns/grids.
 12. SEO handoff (warning): if a HANDOFF-notes.md sits beside the JSON, the meta title
     (<60) and meta description (<155) recorded there are length-checked. Elementor
     JSON cannot carry WP meta, so that note is the only place these exist.

 13. Contrast (warning): delegates to contrast-audit.py -- text/background pairs below
     WCAG AA. Nobody here sees the rendered page, so unreadable text has to be caught
     arithmetically or not at all.
 14. Target-install dependencies (warning): third-party addon widgets, foreign
     shortcodes and unrecognised widget types this page needs. The deliverable is
     imported by someone else, often onto a host we cannot reach -- a missing plugin
     renders as an empty gap and the client finds it first. Cross-checked against the
     kit manifest's own plugin list where a kit exists. Elementor Pro is assumed
     present on every target and is deliberately NOT reported.
 15. Internal links (warning): root-relative links whose target is not in the kit's
     page inventory or the site's built pages -- i.e. links to pages that do not exist
     yet. Forward-links to planned pages are legitimate, so this informs, never blocks.

Checks 1-9 are blockers (exit 1). Checks 10-15 are warnings: they report real problems
but do not fail the gate, because they encode design/SEO/deployment convention rather
than import invariants -- a page can ship with one outstanding if that is a deliberate
call. Nothing here can fail a page that passed before these checks existed.

Usage:  python3 scripts/validate-page.py path/to/page.json
Exit code: 0 = clean, 1 = issues found, 2 = unreadable/not JSON.  Works under any
runtime (plain dependency-free Python 3) — Claude, Codex, Gemini CLI, a human, CI.
"""
import json, sys, re, os, pathlib, importlib.util

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import elementor_meta
except Exception:      # the gate must keep working even if a helper is missing
    elementor_meta = None

# The pass/fail markers below are non-ASCII. On a Windows console defaulting to cp1252
# printing them raises UnicodeEncodeError *after* validation has already run — so the
# gate would crash on success and report nothing. Force UTF-8 where we can.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _load_sibling(filename, modname):
    """Import a hyphenated sibling script as a module (they are CLIs first, libraries
    second, so they cannot be imported by name)."""
    p = pathlib.Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(modname, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_responsive_audit():
    return _load_sibling("responsive-audit.py", "responsive_audit")


def _load_contrast_audit():
    return _load_sibling("contrast-audit.py", "contrast_audit")


def _site_dir(page_path):
    """projects/<site> for a page at projects/<site>/pages/<slug>/<slug>.json."""
    d = os.path.dirname(os.path.abspath(page_path))
    for _ in range(5):
        if os.path.isdir(os.path.join(d, "current-theme")) or \
                os.path.exists(os.path.join(d, "tokens.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def _built_page_slugs(site_dir):
    """Pages this repo has built for the site -- a link target may legitimately point
    at a sibling page that exists here but not yet in the client's kit."""
    out = set()
    pages = os.path.join(site_dir, "pages")
    if os.path.isdir(pages):
        for name in os.listdir(pages):
            if os.path.isdir(os.path.join(pages, name)) and not name.startswith("_"):
                out.add("/" + name.lower())
    return out


def _check_dependencies(doc, site_dir, warnings):
    """What the page needs from the target install, vs what the kit says it has."""
    if elementor_meta is None:
        return
    req = elementor_meta.requirements(doc)
    facts = elementor_meta.kit_facts(site_dir) if site_dir else None

    # Elementor Pro widgets are NOT reported: Pro is on every target install we build
    # for, so flagging them is noise. They are still classified as Pro upstream, which
    # is what keeps them out of the "unrecognised" bucket below.

    for pack, widgets in sorted(req["third_party"].items()):
        listed = ", ".join("%s(%d)" % (w, n) for w, n in sorted(widgets.items()))
        have = facts and any(pack.split()[0].lower() in p.lower() for p in facts["plugins"])
        warnings.append("deps: needs the %s plugin for %s%s"
                        % (pack, listed,
                           " (kit lists it)" if have else " — NOT found in the kit's plugin list"))

    for code in req["shortcodes"]:
        warnings.append("deps: embeds a shortcode %s — it renders only if the plugin that "
                        "provides it is active on the target" % code)

    if req["unrecognised"]:
        listed = ", ".join("%s(%d)" % (w, n) for w, n in sorted(req["unrecognised"].items()))
        warnings.append("deps: unrecognised widget type(s) %s — verify they exist on the "
                        "target install" % listed)


def _check_link_targets(doc, site_dir, warnings):
    """Root-relative links whose target is not a page the kit knows about."""
    if elementor_meta is None or not site_dir:
        return
    facts = elementor_meta.kit_facts(site_dir)
    if not facts or not facts.get("pages"):
        return                      # no inventory (e.g. onboarded from HTML) -> no claim
    known = elementor_meta.known_paths(facts) | _built_page_slugs(site_dir)

    targets = {}

    def walk(e):
        if isinstance(e, dict):
            st = e.get("settings", {}) or {}
            link = st.get("link")
            if isinstance(link, dict) and (link.get("url") or "").startswith("/"):
                targets.setdefault(link["url"], 0)
                targets[link["url"]] += 1
            for key in ("editor", "title", "text"):
                v = st.get(key)
                if isinstance(v, str):
                    for m in re.finditer(r'href="(/[^"]*)"', v):
                        targets.setdefault(m.group(1), 0)
                        targets[m.group(1)] += 1
            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(doc.get("content", []))
    missing = sorted(u for u in targets
                     if elementor_meta.normalise_path(u) not in known
                     and not u.startswith("/#"))
    if missing:
        warnings.append("links: %d internal target(s) not found among the %d pages the kit "
                        "knows about — they may be planned pages, or typos: %s"
                        % (len(missing), len(facts["pages"]), ", ".join(missing[:8])))


# Theme Builder parts import through the same pipeline as pages but are not pages:
# a header/footer legitimately has NO H1, so the single-H1 rule must not apply to them.
_DOC_TYPES = ("page", "header", "footer", "single", "archive", "section", "container")


# ---------------------------------------------------------------- structure
def _bandkey(s):
    """Identity of a section's background, for the adjacent-duplicate check."""
    bg = s.get("background_background")
    if bg == "classic":
        img = (s.get("background_image") or {}).get("url")
        if img:
            return ("image", img)
        return ("color", (s.get("background_color") or "").upper())
    if bg == "gradient":
        return ("gradient", (s.get("background_color") or "").upper(),
                (s.get("background_color_b") or "").upper(),
                str((s.get("background_gradient_angle") or {}).get("size")))
    if bg:
        return (bg,)
    return ("none",)


def _band_label(key):
    if key[0] == "color":
        return key[1] or "classic with no colour set"
    if key[0] == "gradient":
        return "gradient %s -> %s" % (key[1], key[2])
    return key[0]


def _is_card(s):
    """A self-contained card legitimately carries its own padding: it has a fill, a
    border, a radius or a shadow. A bare layout row/column/grid has none of those."""
    return bool(s.get("background_background") or s.get("border_border")
                or s.get("box_shadow_box_shadow_type") or s.get("border_radius"))


def _has_padding(s):
    p = s.get("padding")
    if not isinstance(p, dict):
        return False
    return any(str(p.get(k) or "0").strip() not in ("0", "", "0.0")
               for k in ("top", "right", "bottom", "left"))


def _check_structure(content, errors, warnings):
    """Standard #1: full-width Section -> ONE boxed content container -> content,
    plus padding discipline and band rhythm."""
    prev_key = None
    for i, sec in enumerate(content):
        if not isinstance(sec, dict):
            continue
        s = sec.get("settings", {}) or {}
        kids = [k for k in (sec.get("elements") or []) if isinstance(k, dict)]
        boxed = [k for k in kids
                 if (k.get("settings", {}) or {}).get("content_width") == "boxed"]

        if s.get("content_width") != "full":
            errors.append("structure: section %d (%s) is not full-width -- every section "
                          "is a 100%% band holding one boxed container"
                          % (i + 1, sec.get("id", "?")))
        if len(kids) != 1 or len(boxed) != 1:
            errors.append("structure: section %d (%s) must hold exactly ONE boxed content "
                          "container (found %d child container(s), %d boxed)"
                          % (i + 1, sec.get("id", "?"), len(kids), len(boxed)))

        key = _bandkey(s)
        if prev_key is not None and key == prev_key:
            warnings.append("rhythm: sections %d and %d share the same background (%s) -- "
                            "bands should alternate" % (i, i + 1, _band_label(key)))
        prev_key = key

    def walk(e, in_box=False):
        if isinstance(e, dict):
            s = e.get("settings", {}) or {}
            if e.get("elType") == "container":
                is_boxed = s.get("content_width") == "boxed"
                if is_boxed and in_box:
                    errors.append("structure: boxed container %s is nested inside another "
                                  "boxed container -- one boxed container per section"
                                  % e.get("id", "?"))
                if in_box and not is_boxed and _has_padding(s) and not _is_card(s):
                    warnings.append("padding: container %s is a nested layout row/column/grid "
                                    "carrying padding -- padding belongs on the boxed "
                                    "container and on self-contained cards only"
                                    % e.get("id", "?"))
                for k in (e.get("elements") or []):
                    walk(k, in_box or is_boxed)
                return
            for v in e.values():
                walk(v, in_box)
        elif isinstance(e, list):
            for x in e:
                walk(x, in_box)

    walk(content)


# ------------------------------------------------------------- SEO handoff
_META_BULLET = re.compile(
    r"^\s*[-*]\s*\*\*(?:meta|seo)\s+(title|description):?\*\*:?\s*(.+?)\s*$", re.I | re.M)
_META_ROW = re.compile(
    r"^\s*\|\s*(?:meta|seo)\s+(title|description)\s*\|\s*(.+?)\s*\|\s*$", re.I | re.M)
_LIMITS = (("title", 60), ("description", 155))


def _clean_meta(v):
    """Take the backticked value when the note quotes one, and drop a trailing
    '(52 chars)' / '(151)' annotation the handoff may carry."""
    m = re.search(r"`([^`]+)`", v)
    if m:
        return m.group(1).strip()
    return re.sub(r"\s*\((?:\d+|\d+\s*chars?)\)\s*$", "", v).strip()


def _check_handoff_meta(json_path, warnings):
    """Elementor JSON cannot hold WP meta, so the handoff note is where it lives --
    length-check it there instead of leaving it to be counted by hand."""
    note = pathlib.Path(json_path).with_name("HANDOFF-notes.md")
    if not note.exists():
        return
    try:
        txt = note.read_text(encoding="utf-8")
    except Exception:
        return
    found = {}
    for m in list(_META_BULLET.finditer(txt)) + list(_META_ROW.finditer(txt)):
        found.setdefault(m.group(1).lower(), _clean_meta(m.group(2)))
    for field, limit in _LIMITS:
        val = found.get(field)
        if val is None:
            warnings.append("seo: HANDOFF-notes.md records no meta %s -- set it before publish"
                            % field)
        elif len(val) >= limit:
            shown = val[:70] + ("..." if len(val) > 70 else "")
            warnings.append("seo: meta %s in HANDOFF-notes.md is %d chars (keep it under %d): %s"
                            % (field, len(val), limit, shown))


def validate(doc, path=None):
    errors = []
    warnings = []

    doc_type = doc.get("type") if isinstance(doc, dict) else None

    # 2. wrapper
    if doc_type not in _DOC_TYPES:
        errors.append('wrapper: top-level `type` must be one of %s (got %r)'
                      % (", ".join(_DOC_TYPES), doc_type))
    if not isinstance(doc.get("content"), list) or not doc.get("content"):
        errors.append("wrapper: `content` must be a non-empty list of sections")
    if "page_settings" not in doc:
        warnings.append("wrapper: no `page_settings` (usually {\"template\":\"default\"})")
    if not doc.get("title"):
        warnings.append("wrapper: no `title`")

    content = doc.get("content", [])
    ids, h = [], {"h1": 0, "h2": 0, "h3": 0, "h4": 0}
    gates = [0]
    bad_links = []

    def walk(e):
        if isinstance(e, dict):
            if "id" in e and "elType" in e:
                ids.append(e["id"])
            s = e.get("settings", {}) or {}
            if "display_condition_list" in s:
                gates[0] += 1
            if e.get("widgetType") == "heading":
                hs = s.get("header_size")
                if hs in h:
                    h[hs] += 1
            # links on buttons / link fields
            link = s.get("link")
            if isinstance(link, dict):
                u = (link.get("url") or "").strip()
                if u in ("#", ""):
                    bad_links.append("dead button link (%s)" % (u or "empty"))
                elif "localhost" in u or "127.0.0.1" in u:
                    bad_links.append("environment link: %s" % u)
            for v in e.values():
                walk(v)
        elif isinstance(e, list):
            for x in e:
                walk(x)

    walk(content)

    # 3. unique ids
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append("ids: %d duplicate element id(s): %s" % (len(dupes), ", ".join(dupes[:8])))

    # 4. single H1 — pages only. A header or footer carrying an H1 would steal the
    #    document outline from every page it is attached to, so there the rule inverts.
    if doc_type == "page":
        if h["h1"] != 1:
            errors.append("headings: exactly one H1 required, found %d" % h["h1"])
    elif h["h1"]:
        errors.append("headings: a %s must not contain an H1 (found %d) — it would "
                      "override the H1 of every page it is applied to" % (doc_type, h["h1"]))

    # 5. subscriber gates
    if gates[0]:
        errors.append("gates: %d `display_condition_list` found — remove them (they hide content on import)" % gates[0])

    # 6. links
    for b in bad_links:
        errors.append("links: " + b)

    # 8, 10, 11. section structure, band rhythm, padding discipline
    if isinstance(content, list) and content:
        _check_structure(content, errors, warnings)

    # 9. every image carries alt text
    missing_alt = []

    def walk_alt(e):
        if isinstance(e, dict):
            if e.get("widgetType") == "image":
                st = e.get("settings", {}) or {}
                if not (st.get("image") or {}).get("alt"):
                    missing_alt.append(e.get("id", "?"))
            for v in e.values():
                walk_alt(v)
        elif isinstance(e, list):
            for x in e:
                walk_alt(x)

    walk_alt(content)
    if missing_alt:
        errors.append("media: %d image widget(s) without alt text: %s"
                      % (len(missing_alt), ", ".join(missing_alt[:6])))

    # 12. SEO handoff lengths (warning only -- they live outside the JSON).
    #     Pages only: a header/footer theme part has no WP meta to set.
    if path and doc_type == "page":
        _check_handoff_meta(path, warnings)

    # 13. contrast (delegate; warnings only -- a brand's own palette can fail AA and
    #     that is a decision to make, not an import failure)
    try:
        ca = _load_contrast_audit()
        failures, _passes, _skipped, _styled = ca.audit(doc)
        for f in failures:
            warnings.append("contrast: " + ca.format_row(f))
    except Exception as ex:
        warnings.append("contrast: could not run contrast-audit.py (%s)" % ex)

    # 14/15. what the target install must provide, and whether links land anywhere
    if path:
        site_dir = _site_dir(path)
        try:
            _check_dependencies(doc, site_dir, warnings)
            _check_link_targets(doc, site_dir, warnings)
        except Exception as ex:
            warnings.append("deps: dependency/link check failed (%s)" % ex)

    # 7. responsive (delegate)
    try:
        ra = _load_responsive_audit()
        for issue in ra.audit(doc):
            errors.append("responsive: " + issue)
    except Exception as ex:  # pragma: no cover
        warnings.append("responsive: could not run responsive-audit.py (%s)" % ex)

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            doc = json.load(f)
    except Exception as ex:
        print("✗ Could not read/parse JSON: %s" % ex)
        sys.exit(2)

    errors, warnings = validate(doc, sys.argv[1])
    for w in warnings:
        print("  ⚠︎ " + w)
    if not errors:
        print("✅ validate-page: PASS — %s is import-ready." % sys.argv[1])
        sys.exit(0)
    print("❌ validate-page: %d issue(s):" % len(errors))
    for e in errors:
        print("   - " + e)
    sys.exit(1)


if __name__ == "__main__":
    main()
