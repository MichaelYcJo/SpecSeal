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
path#major                     the enclosing unit
path#major>minor               ... narrowed to the place a claim is about
```

Both carry a hash: `path#major@3f9a2c1b`, `path#major>minor@a71b0e42`.

**A coordinate's job is to put a reader in the right logic, not to pin a
line.** So the address is the enclosing unit, which is stable against every
edit that does not change what the unit *is*.

| Level | What it is | Where it comes from |
|---|---|---|
| **Major** | a function or class for code, a heading path for a document | `ast` for `.py`; otherwise the declaration rule below; `## A / ### B` for markdown |
| **Minor**, optional | the statement the claim is actually about | the name it references (`ast` for `.py`), or a quoted line as a last resort |

```
| CLAUSE | `hooks/routing.py#parse@3f9a2c1b` | ... |
| CLAUSE | `agents/smith.md#"## Boundaries"@a71b0e42` | ... |
| CLAUSE | `hooks/gate.py#run>overlaps@5d1e7c04` | ... |
```

Escape a pipe inside a quoted anchor as `\|`, or the row splits the table it
lives in.

### The rule that decides everything else

**An anchor degrades to DRIFTED, never to BROKEN.**

The two cost different things. `BROKEN` says *I cannot find it, go edit the
ledger* — the bookkeeping this design exists to remove. `DRIFTED` says *it
changed, go re-read the claim* — the work the ledger exists for.

So the minor level narrows what is hashed and **never decides whether the row
resolves**. A minor anchor that stopped matching, or that now matches several
places, means that place changed: the row widens to its major unit and reports
`DRIFTED`. Only the major level can be `BROKEN`.

That is how *specific* and *not strict* stop fighting. Precision buys a
smaller hash and a row that says what it is about; it never buys a new way to
fail.

### The minor level is an escape hatch, not a habit

The default is that a row cites a symbol and the hash covers the whole symbol.
If a function changes, re-reading a claim about that function is a
conservative and honest signal rather than a false alarm — re-reading a row is
cheap, and being strict enough to MISS is not.

The cost, on the record: the most-cited symbols in this plugin's own ledger
carry four rows each, so an edit to one means re-reading four claims.

**Reach for a minor anchor only where a unit is large enough that whole-unit
hashing has been MEASURED to drift rows on unrelated edits** — never where it
merely looks as though it might. The instinct is to reach for precision, and
that instinct is what makes a ledger expensive.

### A document anchor is a heading path

`agents/smith.md#"## Boundaries"`, never a sentence. A sentence breaks on any
rewording, which is a `BROKEN` and a ledger edit; a heading is the document's
own structure and survives the prose beneath it being rewritten, while the
hash still reports that prose changing. Where one heading repeats, name its
parent: `"## Verify / ### Scope"`.

### Resolving a unit without a parser

`ast` is an exactness upgrade for `.py`, not the only road — most projects
adopting this are mostly code that is not Python.

The generic rule needs no parser and no dependency: **the name followed by
`(`, `{` or `:`, then the block to the next line at the same or lower
indentation.** That closes a suite in an indentation language and lands on the
closing brace in a brace language, because the brace sits at the
declaration's own indent.

Where it cannot resolve a unit, that is `BROKEN` and a person looks. Loud and
honest beats a per-language parser nobody maintains.

### Marker comments in the source are not the mechanism

An adopting project will ask whether to tag cited places with a marker comment
so the checker can find them. **No**, on four grounds:

- **ownership** — the ledger is this plugin's artifact and the code is the
  project's. An anchor scheme requiring writes into the observed source
  inverts that.
- **decay** — a teammate deletes or duplicates a marker they do not
  recognise, silently.
- **coverage** — markers only cover marked places, while the ledger's value is
  citing arbitrary ones, including pre-adoption and vendored code. The derived
  anchor is needed anyway, so a marker can only ever be an optimisation.
- **measured cost** — this repository's rider comments (the `RIDER` marker)
  carried commit SHAs, a squash orphaned them, and a patch release exists
  because of it.

**The one permitted use** is a place with no structure at all — a magic
constant in a config, one line inside a large literal — where neither a symbol
nor a heading exists to derive from. There a bare identifier comment is the
last resort. It carries a name and nothing else: no SHA, no date, no
verification state. Verified-ness lives in the ledger only.

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
| `BROKEN` (exit 2) | the MAJOR unit is not in the file, or is in it more than once | fix the coordinate now — a broken ground is worse than none |
| `DRIFTED` (exit 1; 2 under `--strict`) | the content changed, or a minor anchor's place is gone | re-open it, re-read the claim, then `--reverify` |
| `EXTERNAL` | path resolves in no known checkout | pass `--map`/`--default-repo`, or accept as out of scope |
| `OK` | the content is what the row recorded — the current line numbers are printed for you to open |

**An ambiguous MAJOR unit is BROKEN, loudly, and never a measurement.** With
two places to look, an `OK` would be a claim about whichever one the code
happened to reach first. An ambiguous minor anchor widens instead — see the
rule above.

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
| a symbol elsewhere | the declaration line to the next line at its indent or lower, so a closing brace ends it |
| a markdown heading path | down to the next heading at its level or above, which is what a reader means by a section |
| a minor anchor | the statement it names, capped so a claim cannot quietly grow to a whole unit |
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
- The generic unit rule stops AT a closing brace rather than including it. The
  brace carries no claim, and a language-aware rule for what closes a block is
  the per-language parser this deliberately does not have.

## CI

`/specseal:evidence-ci` does the wiring: it vendors `scripts/evidence_check.py`
to `tools/` and writes `.github/workflows/evidence-check.yml`, resolving the
plugin's own path so nobody has to know where it is installed. Re-running it
diffs the vendored copy against the current one.

Vendoring over fetch-at-run keeps CI deterministic and offline-safe, and puts
the checker in the diff where a reviewer can see it change.
