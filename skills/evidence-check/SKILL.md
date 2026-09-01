---
name: evidence-check
description: |
  Verify that the evidence ledger's spec-to-code coordinates still resolve —
  broken links fail, ranges touched since the baseline demand re-verification.
  Use when: checking ledger health, before merging spec-driven work, wiring
  the check into CI, or after large refactors.
  NOT for: judging whether the code is CORRECT — this checks that the
  evidence still points somewhere, not that the claim is still true.
---

# evidence-check — does the ledger still point at what it claims?

Specs rot silently: code moves, the ledger's coordinates keep claiming grounds
that are no longer there, and the next reader trusts them. This skill makes
that rot mechanical to catch — the same way a broken test catches a
regression.

## A coordinate names content, never a position

```
path#anchor@hash
```

- **anchor** — a symbol name where the language offers one, otherwise a
  distinctive line of text in quotes. `.py` is read with the stdlib `ast`, so
  `Class.method` names a span exactly and nothing is installed to do it.
- **hash** — eight hex characters over the anchored region, with trailing
  whitespace and blank lines removed.

A row stores **no line number and no commit**. A line number moves for edits
that have nothing to do with the claim, so a coordinate built from one rots on
contact and everything downstream is compensation: the row is re-anchored, so
whatever it was measured from resets, so a stamp is needed to clear it, so a
squash orphans the stamp. None of that exists here, and the checker calls git
for nothing.

```
| CLAUSE | `hooks/routing.py#parse@3f9a2c1b` | ... |
| CLAUSE | `docs/rules.md#"## When the gate fires"@a71b0e42` | ... |
```

Escape a pipe inside a quoted anchor as `\|`, or the row splits the table it
lives in.

## Run

```bash
evidence-check [ROOT]          # on PATH while the plugin is enabled
evidence-check --strict .
evidence-check --reverify .    # after re-reading: rewrite each row's hash
```

| Flag | Meaning |
|---|---|
| `--ledger GLOB` | ledgers to scan (default `.specseal/map.md` and `.specseal/map/*.md`) |
| `--default-repo PATH` | migration ledgers cite the ORIGINAL repo with unprefixed paths — resolve them against this checkout |
| `--map NAME=PATH` | resolve `NAME/...` prefixed coordinates against another checkout |
| `--strict` | drift exits 2, the broken-coordinate code, instead of 1 |
| `--reverify` | rewrite every resolvable row's hash to what its anchor holds now |

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | the anchor is not in the file, or is in it more than once | fix the coordinate now — a broken ground is worse than none |
| `DRIFTED` (exit 1; 2 under `--strict`) | the anchor is there and the content under it changed | re-open it, re-read the claim, then `--reverify` |
| `EXTERNAL` | path resolves in no known checkout | pass `--map`/`--default-repo`, or accept as out of scope |
| `OK` | the content is what the row recorded — the current line numbers are printed for you to open |

**An ambiguous anchor is BROKEN, loudly, and never a measurement.** With two
places to look, an `OK` would be a claim about whichever one the code happened
to reach first.

## Re-verifying is recomputing the hash

```
evidence-check --reverify .
```

It rewrites the hash of every row whose anchor resolves, and names each one it
changed. That is a person saying they have re-read the code, which is why it
is a separate command: a check that refreshed what it was checking would
report `OK` for ever. A row whose anchor is gone is left alone — silently
renaming its hash would hide the one row somebody has to look at.

## What the region is

| Anchor | Region |
|---|---|
| a symbol in `.py` | the whole `def`/`class` span, **decorators included** — a decorator carries behaviour |
| a markdown heading | down to the next heading at its level or above, which is what a reader means by a section |
| any other line | the contiguous run of non-blank lines it sits in — a paragraph, a table, a block of code |

**The heading rule is markdown-only.** `#` opens a comment in Python, shell and
YAML, and reading one as a heading made a 23-line comment block resolve to its
first line alone.

**Indentation is content.** Trailing whitespace and blank lines are normalised
away, so a reformat is not a change; leading whitespace is not, because in
Python a dedent moves a statement out of the block it belonged to, and a
checker that shrugged at that would go quiet exactly where the edit matters.

## One fragment per work item

A work item's rows go in `.specseal/map/<work-item-id>.md`, which the default
globs already read. Two branches never queue at one file, because no two work
items share an id. Fragments are never gathered back — a row is checked against
the code it cites, not concatenated.

A row citing a range that spans several definitions becomes several
coordinates, one per definition. That is not a loss: it is the row saying which
pieces of code it is actually about.

## Known limits

- An anchor cited as a bare filename (`service.py#f`, no directory) cannot be
  resolved and is reported EXTERNAL — the tool never guesses by fuzzy matching,
  because a wrong resolution would validate the wrong evidence.
- `DRIFTED` means "someone must re-read this", not "the claim is wrong".
- Renaming a symbol reads as `BROKEN` rather than as a rename. That is the
  honest answer — the checker cannot know the new name is the same thing — and
  fixing the row is a one-word edit.

## CI

`/specseal:evidence-ci` does the wiring: it vendors `scripts/evidence_check.py`
to `tools/` and writes `.github/workflows/evidence-check.yml`, resolving the
plugin's own path so nobody has to know where it is installed. Re-running it
diffs the vendored copy against the current one.

Vendoring over fetch-at-run keeps CI deterministic and offline-safe, and puts
the checker in the diff where a reviewer can see it change.
