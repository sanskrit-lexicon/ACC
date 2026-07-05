# ACC

_Created: 16-05-2026 · Last updated: 05-07-2026_

Aufrecht's *Catalogus Catalogorum* is the closest thing pre-digital Sanskrit
studies had to a union catalogue: a 19th-century, three-volume alphabetical
register of Sanskrit **manuscripts and their authors**, listing which work is
attested in which library collection, under which variant title/spelling. It
predates any modern authority-file or union catalog for Sanskrit
manuscripts, and remains a standard first stop for "does a manuscript of this
text exist, and where" — the reason it was digitized at all as part of the
Cologne Digital Sanskrit Dictionaries (CDSL) project, alongside the
dictionaries proper.

This repo is that digitization's **home repository**: it is where the
digitized ACC entries live (via [csl-orig](https://github.com/sanskrit-lexicon/csl-orig),
the shared source tree — see the corrections workflow in the
[org CLAUDE.md](../CLAUDE.md)) and where corrections to it are tracked as
GitHub issues under the shared Sanskrit Lexicon taxonomy. Corrections
actually applied so far live as an audit trail in
[CORRECTIONS/dictionaries/ACC](../CORRECTIONS/dictionaries/ACC) — see below
for a real example.

## What's actually in this repo

At the root level, ACC carries only the org-standard project metadata — no
entry text, no scripts. That is not an oversight: the raw ACC text lives in
`csl-orig`, and per-dictionary correction records live in
[CORRECTIONS](../CORRECTIONS). This repo is the issue-tracking and citation
home for the ACC dictionary specifically, not a data mirror.

| File | Role |
|---|---|
| [CITATION.cff](CITATION.cff) | Citable-dataset metadata — title, license (CC-BY-SA-4.0), preferred citation for Aufrecht 1962 |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | The four markup tags used in the source text (`<L>`, `<k1>`, `<lex>`, `<ls>`) |
| [changelog.md](changelog.md) | SemVer release history |
| [CLAUDE.md](CLAUDE.md) | Issue taxonomy for agents working this repo |

## A real correction, verified against the audit trail

Corrections to ACC are logged, not applied blind. One entry from
[CORRECTIONS/dictionaries/ACC/ACC_correctionform.txt](../CORRECTIONS/dictionaries/ACC/ACC_correctionform.txt)
(read directly, not invented):

```
Case 23811: 09/11/2017 dict=ACC, L=37452, hw=vESvatmyarahasya, user=dhaval
old = vESvatmyarahasya
new = vESvAtmyarahasya
comment = typo
status =  Corrected 09/11/2017
```

As of that file's last count: **155 correction records, 0 pending** for ACC.
A second file in the same directory,
[acc-fuzzyalpha.txt](../CORRECTIONS/dictionaries/ACC/faultfinder/acc-fuzzyalpha.txt),
holds a fuzzy-alphabetization consistency check specific to ACC's
manuscript-title sort order — the kind of structural check a catalogue needs
that a normal dictionary doesn't.

## Issue taxonomy

This repo uses the Sanskrit Lexicon unified issue taxonomy:

- **9 type labels**: link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **3 severity levels**: minor, medium, hard
- **4 milestones**: Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See [CLAUDE.md](CLAUDE.md) for full definitions and the
[org-level runbook](../CLAUDE.md).

---

_Dr. Mārcis Gasūns_
