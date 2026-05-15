# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ACC** is the corrections repository for the Cologne digitization of Aufrecht's *Catalogus Catalogorum* (1891–1903), a bibliography of Sanskrit manuscripts and their locations. The canonical source lives in `csl-orig/v02/acc/acc.txt`.

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/ACC/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh acc ../../ACCScan/2020
sh xmlchk_xampp.sh acc
```

## Dependencies

- **Python 3**
- **acc.txt** — in `$BASE/cologne/csl-orig/v02/acc/acc.txt`
