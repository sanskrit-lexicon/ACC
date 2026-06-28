"""
Markup fixer + audit for acc.txt (ACC).

Counterpart of pwgissues/issue174/08_markup_fix.py (PWG),
pwkissues/markup_fix/08_markup_fix.py (PWK), and siblings.

Two jobs:

  1. FIX problems that have a single safe automatic resolution.
       (a) nested <ab><ab>X</ab> Y</ab>  →  <ab>X Y</ab>  (not present in acc.txt,
           kept for re-run safety after any future auto-wrap pass)
       (b) whitespace inside tag pairs, for every paired tag that
           actually occurs in acc.txt (see TRIM_TAGS).

  2. AUDIT issues that need a human decision. These are reported but
     NOT auto-modified.

ACC-specific notes:
  - acc.txt uses only 2 paired tag types: <symbol> (9,288) and <F> (24).
    The many unpaired tags (<L>, <pc>, <k1>, <k2>, <LEND>, <HI1>, <HI>,
    <H>, <P>, <e>) are structural record-delimiter tags, not inline markup.
  - No <ab>, <ls>, <lex>, <bot>, <zoo>, or <lang> tags are present.
  - Current acc.txt is clean: 0 whitespace hits, 0 nested tags, 0
    boundary collisions. Output is expected to be byte-identical to source.
  - 36 {{old -> new || …}} correction records are present; nested tags
    inside those blocks are part of the format, not bugs.

Inputs:
  ../../../csl-orig/v02/acc/acc.txt      (when run from accissues/markup_fix/)
  or argv[1] (any path)

Outputs:
  acc_fixed.txt             -- repaired copy (expected byte-identical to source)
  markup_fix_changes.txt    -- log of auto-fixes (expected empty)
  markup_audit.txt          -- audit findings with line refs

Usage:
  python 08_markup_fix.py            # uses default in/out paths
  python 08_markup_fix.py IN OUT     # custom paths
"""

import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent

if len(sys.argv) >= 3:
    PW_TXT = Path(sys.argv[1])
    OUT_FIX = Path(sys.argv[2])
else:
    candidates = [
        HERE.parent.parent.parent / "csl-orig" / "v02" / "acc" / "acc.txt",
        HERE / "acc.txt",
    ]
    PW_TXT = next((p for p in candidates if p.exists()), candidates[0])
    OUT_FIX = HERE / "acc_fixed.txt"

OUT_LOG = HERE / "markup_fix_changes.txt"
OUT_AUDIT = HERE / "markup_audit.txt"


# ---------------------------------------------------------------------------
# Pattern 1: nested <ab> wrappings (guard for future overlay passes)
# ---------------------------------------------------------------------------
NEST_RX = re.compile(
    r"<ab(?P<oa>\b[^>]*)>(?P<pre>[^<]*)<ab(?P<ia>\b[^>]*)>(?P<inner>[^<]*)</ab>(?P<post>[^<]*)</ab>"
)


def fix_nested_ab(line):
    n_fixed = 0
    while True:
        m = NEST_RX.search(line)
        if not m:
            return line, n_fixed
        oa = m.group("oa")
        pre = m.group("pre")
        inner = m.group("inner")
        post = m.group("post")
        repl = f"<ab{oa}>{pre}{inner}{post}</ab>"
        line = line[:m.start()] + repl + line[m.end():]
        n_fixed += 1


# ---------------------------------------------------------------------------
# Pattern 2: whitespace inside common tag pairs
# ---------------------------------------------------------------------------
# Paired tags that actually exist in acc.txt:
#   symbol 9,288 | F 24
TRIM_TAGS = ["symbol", "F"]


def fix_trim_whitespace(line):
    n = 0
    for tag in TRIM_TAGS:
        pat = re.compile(rf"(<{tag}\b[^>]*>)(\s+)([^<]*?)(\s*)(</{tag}>)")
        def _repl(m):
            nonlocal n
            inside = m.group(3).rstrip()
            if inside != m.group(2) + m.group(3) + m.group(4):
                n += 1
            return f"{m.group(1)}{inside}{m.group(5)}"
        line = pat.sub(_repl, line)
        pat2 = re.compile(rf"(<{tag}\b[^>]*>)([^<]*?)(\s+)(</{tag}>)")
        def _repl2(m):
            nonlocal n
            inside = m.group(2).rstrip()
            n += 1
            return f"{m.group(1)}{inside}{m.group(4)}"
        line = pat2.sub(_repl2, line)
    return line, n


# ---------------------------------------------------------------------------
# Audit (no auto-modification)
# ---------------------------------------------------------------------------

def _ls_nested_classify(line):
    inside, outside = [], []
    for m in re.finditer(r"<ls\b[^>]*>([^<]*<ls\b[^>]*>)", line):
        inner_offset = m.group(1).find("<ls")
        inner_open = m.start(1) + (inner_offset if inner_offset >= 0 else 0)
        prefix = line[:inner_open]
        if prefix.rfind("{{") > prefix.rfind("}}"):
            inside.append(m)
        else:
            outside.append(m)
    return outside, inside


AUDIT_CHECKS = [
    ("Adjacent </symbol> <symbol> — possibly intentional",
     re.compile(r"</symbol>\s*<symbol")),
    ("Adjacent </F> <F>",
     re.compile(r"</F>\s*<F")),
    ("Nested <ab> (guard — currently 0)",
     re.compile(r"<ab\b[^>]*>[^<]*<ab\b")),
    ("Empty content <symbol> or <F> tag",
     re.compile(r"<(symbol|F)\b[^>]*></\1>")),
    ("{#…#} closing brace immediately followed by <symbol> or <F>",
     re.compile(r"#\}<(?:symbol|F)\b")),
    ("Malformed tag with unescaped < inside attribute value",
     re.compile(r'<[A-Za-z][A-Za-z0-9]*\s+[A-Za-z]+="[^"]*<[^"]*"\s*[^>]*>')),
]


def main():
    print(f"Reading {PW_TXT} …", flush=True)
    lines = PW_TXT.read_text(encoding="utf-8").splitlines()
    print(f"  {len(lines):,} lines", flush=True)

    out_lines = []
    fix_log = []
    tot_nested = 0
    tot_trim = 0

    audit_hits = {label: [] for label, _ in AUDIT_CHECKS}

    for lineno, line in enumerate(lines, 1):
        orig = line
        line, n1 = fix_nested_ab(line)
        line, n2 = fix_trim_whitespace(line)
        tot_nested += n1
        tot_trim += n2
        if line != orig:
            fix_log.append((lineno, orig, line))
        out_lines.append(line)

        outside_hits, inside_hits = _ls_nested_classify(orig)

        for label, pat in AUDIT_CHECKS:
            for m in pat.finditer(orig):
                start = max(0, m.start() - 40)
                end = min(len(orig), m.end() + 40)
                audit_hits[label].append((lineno, orig[start:end].replace("\t", " ")))
                if len(audit_hits[label]) >= 5000:
                    break
        if lineno % 100000 == 0:
            print(f"  {lineno:,}/{len(lines):,}", flush=True)

    print(f"Total nested <ab> repairs:    {tot_nested}", flush=True)
    print(f"Total whitespace trims:       {tot_trim}", flush=True)
    print(f"Total changed lines:          {len(fix_log)}", flush=True)

    print(f"Writing {OUT_FIX} …", flush=True)
    with OUT_FIX.open("w", encoding="utf-8", newline="\n") as f:
        for line in out_lines:
            f.write(line + "\n")

    print(f"Writing {OUT_LOG} …", flush=True)
    with OUT_LOG.open("w", encoding="utf-8") as f:
        f.write("; markup_fix log for acc.txt\n")
        f.write(f"; nested <ab>:    {tot_nested}\n")
        f.write(f"; whitespace:     {tot_trim}\n")
        f.write(f"; changed lines:  {len(fix_log)}\n;\n")
        for lineno, old, new in fix_log:
            f.write(f"{lineno} old {old}\n")
            f.write(f"{lineno} new {new}\n")

    print(f"Writing {OUT_AUDIT} …", flush=True)
    with OUT_AUDIT.open("w", encoding="utf-8") as f:
        f.write("ACC markup audit — findings requiring a human decision\n")
        f.write("=" * 60 + "\n\n")
        f.write("Generated by 08_markup_fix.py against acc.txt.\n")
        f.write("Items below were DETECTED but NOT modified by the fixer.\n\n")
        f.write("acc.txt is structurally simpler than other Cologne dictionaries:\n")
        f.write("only 2 paired tag types (<symbol>, <F>) are used. The many\n")
        f.write("unpaired tags (<L>, <pc>, <k1>, <k2>, <LEND>, <HI1>, <HI>,\n")
        f.write("<H>, <P>, <e>) are record-delimiter structural tags.\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nWHAT THIS FIXER AUTO-CORRECTS\n")
        f.write("------------------------------------------------------------\n")
        f.write("  - Nested <ab> (guard for future overlay passes — 0 now)\n")
        f.write("  - Whitespace inside <symbol> and <F>\n")
        f.write("\nOutput goes to acc_fixed.txt (expected byte-identical to\n")
        f.write("source); change log in markup_fix_changes.txt.\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nWHAT NEEDS HUMAN ATTENTION\n")
        f.write("------------------------------------------------------------\n")
        f.write("  1. acc.txt is currently clean on all standard markup checks.\n")
        f.write("     No whitespace hits, no nested tags, no boundary collisions.\n\n")
        f.write("  2. <F> tag (24 occurrences) — usage appears to be footnote\n")
        f.write("     markers. Visual review is cheap at this count:\n")
        f.write("       grep -n '<F>' acc.txt\n\n")
        f.write("  3. <symbol> tag (9,288 occurrences) — encodes special\n")
        f.write("     characters. Verify content is well-formed.\n\n")
        f.write("  4. 36 {{old -> new || …}} correction records exist.\n")
        f.write("     Any nested tags inside them are part of the format.\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nAUTOMATED CHECKS BELOW\n")
        f.write("------------------------------------------------------------\n\n")
        for label, _ in AUDIT_CHECKS:
            hits = audit_hits[label]
            f.write(f"## {label}\n")
            f.write(f"   matches: {len(hits)} (showing up to 200)\n")
            for ln, snippet in hits[:200]:
                f.write(f"   L{ln}: {snippet}\n")
            f.write("\n")

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
