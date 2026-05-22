Counterpart of PWG/pwgissues/issue174/08_markup_fix.py
(see https://github.com/sanskrit-lexicon/PWG/issues/175
 and https://github.com/sanskrit-lexicon/PWK/issues/113).

Files in this folder:
  08_markup_fix.py        -- fixer + audit script for acc.txt
  test_markup_fix.py      -- synthetic tests (10/10 pass)
  acc_fixed.txt           -- copy of acc.txt (byte-identical, 0 auto-fixes)
  markup_fix_changes.txt  -- updateByLine log (empty — no changes)
  markup_audit.txt        -- audit findings (all checks: 0 matches)
  ISSUE_COMMENT.md        -- GitHub issue body
  comment_markup_fix.md   -- same as ISSUE_COMMENT.md
  readme.txt              -- this file

Usage:
  python 08_markup_fix.py            # uses csl-orig/v02/acc/acc.txt by default
  python 08_markup_fix.py IN OUT     # custom paths
  python test_markup_fix.py          # run synthetic tests
