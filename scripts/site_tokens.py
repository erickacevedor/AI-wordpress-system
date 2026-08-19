# -*- coding: utf-8 -*-
"""
Canonical reader for any site's tokens.json.

The problem this solves: across the sites onboarded so far there are 46 distinct
top-level keys and only 7 that every site shares, and the colour roles are named
differently on every one --

    dolan       blue, white, black, accent, text
    gcreliable  primary, secondary, accent, dark, dark_red, white, black, text, grey
    magnolia    primary, secondary, accent, dark, white, black, text
    petitt      primary, secondary, accent, text, white, soft_gray, blue_2, red_2, text_2

Nothing generic can read that. Rather than force a migration (which would touch every
build.py and risk changing built output), this module NORMALISES on read: it maps
whatever a site calls things onto a canonical view, so cross-site tooling -- the
contrast checker, a site-wide audit, a future shared brand base -- works today, on
every site, with no change to any tokens.json.

A site can make the mapping explicit and exact by adding an optional `_roles` block:

    "_roles": {"primary": "blue", "text": "text", "surface": "white"}

Without it, the heuristics below infer roles from the usual names. Explicit always
wins over inferred.

Usage:
    import site_tokens
    t = site_tokens.load("projects/dolan")
    t.hex("primary")      -> "#F27122"     (None if the site has no such role)
    t.font("heading")     -> "Ruda"
    t.raw                 -> the untouched dict, for anything site-specific
"""
import json
import os

# Canonical role -> the names sites actually use, best first. Inference only; a
# site's own `_roles` block overrides all of it.
ROLE_ALIASES = {
    "primary":   ("primary", "blue", "brand", "main", "cta-bg"),
    "secondary": ("secondary", "orange", "gold", "red", "purple"),
    "accent":    ("accent", "cta", "highlight", "cta-bg"),
    "dark":      ("dark", "navy", "black", "ink", "dark-bg"),
    "text":      ("text", "body", "ink", "black", "text-primary"),
    "surface":   ("white", "surface", "bg", "background", "bg-primary"),
    "muted":     ("grey", "gray", "soft_gray", "neutral", "muted", "text-secondary"),
}

# A shade ramp ({"50": "#..", ..., "900": "#.."}) collapses to its base step.
RAMP_BASE = ("500", "600", "400", "DEFAULT", "base")


class Tokens(object):
    def __init__(self, raw, path):
        self.raw = raw
        self.path = path
        # A site may carry semantic roles separately from its raw palette (Lenz maps
        # `colors` shade ramps -> a `roles` block). Semantic wins: it is the site
        # saying what a colour is FOR, which is exactly what a role lookup wants.
        self._colors = {}
        for block in ("colors", "roles"):
            b = raw.get(block)
            if isinstance(b, dict):
                for k, v in b.items():
                    self._colors[k] = v
        self._explicit = raw.get("_roles") or {}

    # ---- colours ---------------------------------------------------------
    def _color_entry(self, key):
        v = self._colors.get(key)
        if v is None:
            return None
        # sites store either {"hex": "#..", "global": "globals/..."} or a bare string
        if isinstance(v, str):
            return {"hex": v}
        if isinstance(v, dict):
            if v.get("hex"):
                return v
            # a shade ramp: take the base step
            for step in RAMP_BASE:
                if isinstance(v.get(step), str) and v[step].startswith("#"):
                    return {"hex": v[step], "_from_ramp": step}
            return v
        return None

    def role_key(self, role):
        """Which of THIS site's colour keys plays `role`, or None."""
        explicit = self._explicit.get(role)
        if explicit and explicit in self._colors:
            return explicit
        for name in ROLE_ALIASES.get(role, ()):
            if name in self._colors:
                return name
        return None

    def hex(self, role):
        key = self.role_key(role)
        if not key:
            return None
        entry = self._color_entry(key)
        return (entry or {}).get("hex")

    def global_ref(self, role):
        key = self.role_key(role)
        if not key:
            return None
        return (self._color_entry(key) or {}).get("global")

    def all_hexes(self):
        """Every colour the site declares, as {key: hex} -- for 'is this hex on brand?'"""
        out = {}
        for k in self._colors:
            e = self._color_entry(k)
            if e and e.get("hex"):
                out[k] = e["hex"]
        return out

    def band_hexes(self):
        """Section-background colours: the `bands` block where a site has one, plus
        any surface/light roles. Used by the contrast checker to know what text sits on."""
        out = {}
        bands = self.raw.get("bands")
        if isinstance(bands, dict):
            for k, v in bands.items():
                if isinstance(v, str) and v.startswith("#"):
                    out[k] = v
                elif isinstance(v, dict):
                    for kk in ("hex", "from", "color"):
                        if isinstance(v.get(kk), str) and v[kk].startswith("#"):
                            out["%s.%s" % (k, kk)] = v[kk]
        for role in ("surface", "dark", "primary"):
            h = self.hex(role)
            if h:
                out.setdefault(role, h)
        return out

    # ---- type ------------------------------------------------------------
    def font(self, which="heading"):
        f = self.raw.get("fonts") or {}
        if isinstance(f, dict):
            if which in f and isinstance(f[which], str):
                return f[which]
            for k in ("heading", "body", "primary", "family"):
                if isinstance(f.get(k), str):
                    return f[k]
        elif isinstance(f, str):
            return f
        return None

    def content_width(self):
        w = self.raw.get("content_width")
        if isinstance(w, dict):
            return w.get("size") or w.get("value")
        return w

    def site_name(self):
        return self.raw.get("site") or os.path.basename(os.path.dirname(self.path))

    # ---- conformance -----------------------------------------------------
    def missing_core(self):
        """Which canonical pieces this site cannot answer. Advisory -- a site missing
        one still builds fine; it just can't be read by generic tooling."""
        missing = []
        for role in ("primary", "text", "surface"):
            if not self.hex(role):
                missing.append("colors.%s (no key matched %s)"
                               % (role, "/".join(ROLE_ALIASES[role])))
        if not self.font("heading"):
            missing.append("fonts.heading")
        if not self.content_width():
            missing.append("content_width")
        for k in ("type_scale", "button"):
            if k not in self.raw:
                missing.append(k)
        return missing


def load(site_dir):
    """site_dir = projects/<site> (or a direct path to a tokens.json)."""
    path = site_dir
    if os.path.isdir(site_dir):
        path = os.path.join(site_dir, "tokens.json")
    with open(path, encoding="utf-8") as f:
        return Tokens(json.load(f), path)


def find_for_page(page_json_path):
    """Walk up from a built page to its site's tokens.json. Returns None if the page
    lives outside the projects/<site>/pages/... convention."""
    d = os.path.dirname(os.path.abspath(page_json_path))
    for _ in range(6):
        cand = os.path.join(d, "tokens.json")
        if os.path.exists(cand):
            try:
                return load(cand)
            except Exception:
                return None
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None
