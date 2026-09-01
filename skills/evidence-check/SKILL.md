---
name: evidence-check
description: |
  Verify that the evidence ledger's content anchors still resolve — a missing
  or ambiguous unit fails the build, changed content demands re-verification.
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
`(`, `{`, `=` or `:`, with only declaration keywords before it, then the block
to the next line at the same or lower indentation.** That closes a suite in an
indentation language and lands on the closing brace in a brace language,
because the brace sits at the declaration's own indent.

`=` is there because a module-level constant is a unit too, and a common one to
cite. The colon is stricter — it declares only when the name opens the line —
because `if v not in NAME:` also ends in one, and without that a row citing a
constant reads BROKEN for a use somewhere else in the file. A statement
keyword before the name — `return render(y);`, `await render(y)` — makes the
line a use for the same reason: it is the commonest shape in every brace
language, and reading it as a second declaration made an ordinary
one-declaration-one-call file BROKEN-ambiguous. A line with nothing at all
before the name whose statement ends — `render(1);` — is a call on structure
rather than on vocabulary, and is refused whatever the keyword list says.

Swift, Kotlin, Go, Ruby and Lua end no statement with a semicolon, so that
guard never reached them. **A line with nothing before the name, an opening
paren, and a span of ONE line is treated as uncertain in every language**, and
the span is what bounds it: `render() {` opens a block and stays a declaration
the rule is sure of, while `render(y)` alone does not.

**The rule reports how sure it is rather than being asked to be right.** Where
the certain candidates would leave the set empty, the uncertain ones come back —
a C# `public new void Render(int x)` and a Swift `case loading(String)` are
declarations whose modifiers are statement keywords elsewhere — and the
answer is marked as having survived only that way. What the marking buys is
that nothing downstream has to tell the two apart. The check accepts such a
place only where its content reconstructs the row's recorded hash, and
otherwise treats the unit as GONE: `BROKEN` with the repo-wide scan naming the
destination, which is the answer `ast` already gives `.py`. `--reverify`
refuses to write onto such a place at all, because it is the command that
MAKES the hash and has none to compare against. `--migrate` answers the same
way, with one exception it can prove: where the old stamp's commit holds the
cited lines unchanged, the person's own line numbers vouch for that place and
the row migrates.

**A row citing such a unit is still written by hand.** The check names the
place and the hash it holds — `1-2@a1b2c3d4` — so recording it is a copy
rather than a computation somebody has to do themselves.

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
| `--reverify` | rewrite every resolvable row's hash to what its anchor holds now — and re-anchor every BROKEN row that exactly one unit reconstructs, path and locator both |
| `--migrate` | rewrite old `path:line` rows to `path#unit@hash`; what it cannot prove is left and named |

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | the MAJOR unit — or its whole file — is not there, or the unit is there more than once | fix the coordinate now. Where the content still exists the line names the destination, graded by proof: `identical content at <where> (renamed?/moved?)` is content identity across a repo-wide scan and `--reverify` acts on it; `same name at <path> (content differs)` is a labelled fact only; several matches are counted, never named |
| `OLD-FORMAT` (exit 2, `--strict` or not) | an old `path:line` row from before content anchoring, which nothing measures any more | run `evidence-check --migrate .` — a red build naming the migrator beats a green build checking nothing |
| `DRIFTED` (exit 1; 2 under `--strict`) | the content changed, or a minor anchor's place is gone | re-open it, re-read the claim, then `--reverify` |
| `EXTERNAL` (exit 0) | the path resolves in no known checkout, in a repository that has DECLARED cross-repo intent — a parity config, `--map`, or `--default-repo` | pass `--map`/`--default-repo`, or accept as out of scope. Without such a declaration a missing path is `BROKEN` instead: a deleted or renamed directory must fail the build, not read as somebody else's repo |
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

- A missing file is `BROKEN` with the same graded scan hints as a missing
  symbol — a renamed file or directory is findable by content. `EXTERNAL`
  needs declared cross-repo intent, and where intent is declared but a row's
  file is in none of the named checkouts, the scan stays OFF: searching this
  repository for a row that may cite the other one manufactures evidence.
  Intent is read per ROW where it can be: a row whose prefix is not among the
  `--map` names is a local row and keeps its scan. What cannot be read per row
  is an UNPREFIXED row in a repository declaring `.specseal/parity.md` or
  `--default-repo` — it may be citing the original, and nothing in the
  coordinate says which. Such a row loses the scan for any move, not just for
  a renamed directory: no `(moved?)` hint and no `--reverify` heal, so it is
  fixed by `--map` or by hand.
- `DRIFTED` means "someone must re-read this", not "the claim is wrong".
- A place the rule is unsure of — a C# `new`, a Swift `case`, a one-line
  bare-name declaration — is never re-anchored by `--reverify`, and is
  migrated only where the old stamp vouches for the cited lines. Where its
  content changed in place and no destination is provable, both commands leave
  the row and print the hash to record by hand. Accepting it instead is how a
  call site left behind by a move becomes the row's permanent anchor.
- Every row the check calls `BROKEN` or `DRIFTED` gets a line back from
  `--reverify`, whether or not it could heal it. Silence there reads as a heal
  that happened.
- A nested `def` is anchored by its qualified name — `outer.inner` — and the
  short name alone resolves to nothing. Such a row reads `BROKEN` with the
  qualified unit named on the same line, and `--reverify` re-anchors it.
- Reconstruction proves identity of content, not history. Deleting a unit
  that has a boilerplate twin — an `__init__`, a trivial getter, a thin
  wrapper, and most readily of all a one-line constant, where the name
  substitution leaves nothing but the value — reads as `renamed?` pointing at
  the twin, and `--reverify` would re-anchor to it. Deleting `TIMEOUT = 10`
  beside an unrelated `RETRIES = 10` is the cheapest way to see it. The line says *identical content*, which is the whole of
  what was proven; the deletion is yours to spot in the diff.
- Renaming a symbol reads as `BROKEN` — but where exactly one unit
  reconstructs the recorded content, the line names it and `--reverify` fixes
  the row. The proof substitutes the candidate's name with the row's locator
  and compares against the RECORDED hash, so content that changed AND moved
  matches nothing and stays a plain BROKEN.
- The rename scan is bounded so the clean path stays fast: same-extension
  files only, files over 256 KB skipped, and past 200 candidate files it
  degrades to the row's own file and says so on the line. Measured: one
  BROKEN row against 200 files costs ~110 ms; past the cap, ~36 ms.
- A name match with different content never fixes anything — `main`,
  `resolve` and `check` collide across files as a matter of course.
- The generic unit rule stops AT a closing brace rather than including it. The
  brace carries no claim, and a language-aware rule for what closes a block is
  the per-language parser this deliberately does not have.

## Migrating a pre-anchor ledger

**The default is that nobody runs anything**: at the first session start after
updating, an opted-in repository's ledger migrates itself and prints one line
ending *review the diff and commit*. Once per repository; never over an
uncommitted ledger file — the dirty check covers exactly the files the
migration would rewrite, and a dirty one is skipped with one line and retried
at the next clean session start. The write is licensed by ownership (the
ledger is the plugin's artifact) and bounded by visibility: deterministic,
idempotent, all-or-nothing per row, old text in git history.

A recorded line number is trusted only as far as it can be vouched for. Where
git can produce the file at a row's old stamp, a cited range whose content
changed since that commit is LEFT rather than rewritten onto whatever sits at
those lines now. Where the proof is unavailable — no git, no stamp, a commit
a squash orphaned — the row migrates against the current tree alone and the
summary says how many did, so those rows are reviewed in the diff rather than
assumed.

For CI, for a skipped tree, or by hand:

```
evidence-check --migrate .
```

One command, once. Each `path:line` row is resolved against
the current tree to its enclosing unit and rewritten as `path#unit@hash`; the
commit stamp drops and the date stays. The run prints the same faithfulness
report this repository's own 51-coordinate migration was held to: how many
converted, and every row left named with why — a line past the end of its
file, a file that is gone, a range no single unit contains. A left row keeps
failing the plain check as `OLD-FORMAT`, so nothing is silently dropped, and
running the command twice is a no-op.

## CI

`/specseal:evidence-ci` does the wiring: it vendors `scripts/evidence_check.py`
to `tools/` and writes `.github/workflows/evidence-check.yml`, resolving the
plugin's own path so nobody has to know where it is installed. Re-running it
diffs the vendored copy against the current one.

Vendoring over fetch-at-run keeps CI deterministic and offline-safe, and puts
the checker in the diff where a reviewer can see it change.
