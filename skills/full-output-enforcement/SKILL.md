---
name: full-output-enforcement
description: >
  Enforces complete, untruncated output — with specific rules for Elementor
  page/template JSON, which is long, deeply nested, and breaks on import if
  abbreviated. Use whenever generating or editing Elementor JSON, full code files,
  or any deliverable where partial output is a broken output. Bans placeholder
  patterns and handles token-limit splits cleanly.
---

# Full-Output Enforcement

## Baseline

Treat every task as production-critical. A partial output is a broken output. Optimize for completeness, not brevity. If the user asks for a full file, deliver the full file. If they ask for 5 sections, deliver 5 sections.

## Elementor JSON (primary use here)

Elementor page and template exports are large, deeply nested JSON trees. They are especially unforgiving of truncation — an incomplete file simply fails to import. When producing or editing them:

- Emit the **entire** JSON tree. Never stub sections with `"... rest of widgets ..."`, `// same as above`, or a comment describing what should be there.
- Every element needs a unique `id` and a complete `settings` object (with inline colors/typography, per the VitalAir UI design system).
- Preserve required keys at every level: `elType`, `widgetType` (for widgets), `elements`, `settings`.
- Do not collapse repeated widgets (e.g. three icon-boxes) into one example plus a note — write all of them out in full.
- Keep the JSON valid: matched braces/brackets, correct commas, proper escaping of quotes and HTML inside `editor` fields.

## Banned output patterns

Hard failures — never produce these:

**In JSON / code:** `// ...`, `/* ... */`, `"...": "rest of content"`, `// same pattern`, `// add more as needed`, bare `...` standing in for omitted structure, a skeleton when a full implementation was requested.

**In prose:** "the rest follows the same pattern," "similarly for the remaining sections," "for brevity," "I'll leave that as an exercise," "let me know if you want the rest."

**Structural shortcuts:** showing the first and last section while skipping the middle; replacing repeated logic/widgets with one example and a description; describing what the JSON should contain instead of writing it.

## Execution process

1. **Scope** — count the distinct deliverables expected (files, sections, widgets, repeated blocks). Lock that number.
2. **Build** — generate every one completely.
3. **Cross-check** — re-read the request, compare against the scope count, add anything missing before responding.

## Handling long outputs

When a response approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Write at full quality up to a clean breakpoint (end of a section/container/file).
- End with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue," resume exactly where you stopped. No recap, no repetition.

## Quick check

Before finalizing: no banned patterns anywhere; every requested item present and finished; JSON valid and complete (unique ids, required keys, matched brackets); nothing shortened to save space.
