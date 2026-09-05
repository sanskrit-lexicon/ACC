_Created: 22-05-2026 · Last updated: 05-09-2026_

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `acc.txt`.

I ran the same two-job recipe over `csl-orig/v02/acc/acc.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `accissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — acc.txt is remarkably clean; no auto-fixes were needed and all audit checks returned 0. The output is byte-identical to the source.

## Markup fixer + audit for `acc.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` (guard for future overlay passes) |
| `<symbol>★ </symbol>` | `<symbol>★</symbol>` |
| `<F> note </F>` | `<F>note</F>` |

Whitespace trimming applies to the 2 paired tags that actually occur in `acc.txt`: `<symbol>` and `<F>`. The original file is never modified — output goes to `acc_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). **Output is byte-identical to source** (no auto-fixes triggered).

### Closing-tag inventory in current `acc.txt`

| Tag | Count |
|---|---:|
| `</symbol>` | 9,288 |
| `</F>` | 24 |

No self-closing tags. Both paired tags are balanced. `acc.txt` uses only 2 paired tag types — far simpler than other Cologne dictionaries. The many unpaired tags (`<L>`, `<pc>`, `<k1>`, `<k2>`, `<LEND>`, `<HI1>`, `<HI>`, `<H>`, `<P>`, `<e>`) are structural record-delimiter tags, not inline markup pairs.

### What it found in current `acc.txt`

- **0** nested `<ab>` — not applicable (no `<ab>` tag in acc.txt). The nesting guard is retained for re-runs after any future overlay pass.
- **0** whitespace trims — acc.txt is already clean on all paired tags.
- **0** `<ab n="…">` attributes — no abbreviation markup in acc.txt.
- **0** nested `<symbol>` or `<F>` — clean.
- **0** boundary collisions — acc.txt is clean on all collision patterns.
- **36** `{{old → new || …}}` correction records present; no nested tags inside them.

### Broader cleanup checklist (in `markup_audit.txt`)

1. **`<F>` tag** (24 occurrences) — footnote markers; visual review is cheap at this count (`grep -n '<F>' acc.txt`).
2. **`<symbol>` tag** (9,288 occurrences) — encodes special characters; verify content is well-formed.
3. **Structural unpaired tags** — `<HI1>` (26,982), `<HI>` (5,271), `<H>` (37), `<P>` (20), `<e>` (7) — these are formatting/structure markers not covered by this fixer; a separate structural audit may be warranted.
4. **Nested `<ab>` guard** — 0 currently; retained so any future overlay pass can be re-validated automatically.

### Usage

```
cd accissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/acc/acc.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `acc_fixed.txt` (byte-identical to source), `markup_fix_changes.txt` (empty), `markup_audit.txt`.

### Summary

`acc.txt` uses only 2 paired tag types (`<symbol>`, `<F>`), both balanced. The file is clean on all standard markup checks: 0 auto-fixes applied, output is byte-identical to source. No abbreviation markup (`<ab>`, `<ls>`, `<lex>`) is used in this bibliography dictionary. The fixer is retained as a re-runnable baseline for any future overlay passes.

### Severity

`minor`

_Dr. Mārcis Gasūns_
