"""Synthetic tests for 08_markup_fix.py (ACC)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
mod = import_module("08_markup_fix")
fix_nested_ab = mod.fix_nested_ab
fix_trim_whitespace = mod.fix_trim_whitespace

PASS = 0
FAIL = 0

def check(desc, got, want):
    global PASS, FAIL
    if got == want:
        print(f"  PASS  {desc}")
        PASS += 1
    else:
        print(f"  FAIL  {desc}")
        print(f"        got:  {got!r}")
        print(f"        want: {want!r}")
        FAIL += 1

print("=== nested <ab> fixes (guard) ===")
line, n = fix_nested_ab("<ab><ab>word</ab></ab>")
check("exact-dup flattened", line, "<ab>word</ab>")
check("exact-dup count", n, 1)

line, n = fix_nested_ab("<ab>no nesting here</ab>")
check("no-op", line, "<ab>no nesting here</ab>")
check("no-op count", n, 0)

print("\n=== whitespace trims ===")
line, n = fix_trim_whitespace("<symbol>★ </symbol>")
check("<symbol> trailing trim", line, "<symbol>★</symbol>")
check("<symbol> trailing count", n, 1)

line, n = fix_trim_whitespace("<F> footnote </F>")
check("<F> leading+trailing trim", line, "<F>footnote</F>")
check("<F> trim count", n >= 1, True)

line, n = fix_trim_whitespace("<symbol>clean</symbol>")
check("<symbol> clean no-op", line, "<symbol>clean</symbol>")
check("<symbol> clean count", n, 0)

print(f"\n{'='*40}")
print(f"Results: {PASS}/{PASS+FAIL} passed", ("✓" if FAIL == 0 else "✗"))
if FAIL:
    sys.exit(1)
