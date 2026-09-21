# 1789956662-the-gate-and-ci-ask-about-different-ranges — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 42be239e |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The documents and the records: `agents/sealer.md` §*The command*,
`skills/verify/SKILL.md` §*The broad gate*, `changelog.md`, and the
`seal/ledger/1789956662-*.md` fragment. The documents' own cases stay green;
the ledger fragment's anchors resolve under `evidence-check --strict`.

## What this phase found

**The first form of the document pin was a check that could not fail, for
one of its three files.** It walked each file's `\n\n`-separated blocks
looking for one carrying both `origin/` and `upstream`. That is right for the
two markdown documents and wrong for `broad_gate.py`, whose `REMOTE_BASE` and
`UPSTREAM_BASE` constants sit in one block and answer for the whole file.
Measured: deleting the docstring's paragraph left the case green. The gate's
docstring is now read through `ast.get_docstring`, which is red for the same
deletion, and `test_the_block_reader_can_fail` drives the reader both ways so
nothing built on it is asserting something nothing can break.

**A mutation that cuts part of a block is not a mutation of the block.** The
first sealer.md mutation replaced only the paragraph's bold opener and stayed
green, which reads exactly like a vacuous pin. It was not: the paragraph's
body still carried both words. Settled by finding every qualifying block —
there is exactly one in that file — and deleting it, which turns the case
red.

**Four existing ledger rows drifted, and every one of their claims holds.**
Three cite `broad_gate.py#gate` and one cites
`agents/sealer.md#"## The command"`, both of which this work changed.

| Row | Why it still holds |
|---|---|
| S7, the draft judgment | `draft_env` and its call site are byte-identical and the resolution sits above them |
| S12, both of `seal`'s non-zero exits | the two-exit reading and the `sealed` discriminator are byte-identical; what moved is the VALUE handed to `seal_record` |
| the `Broad gate` value read before a shell gets it | `not_as_written` still stands between the row being read and the first `run`, with the resolution inserted BELOW it |
| the absent-row refusal | the paragraph the row is about is unchanged word for word; three paragraphs were added above it |

Each was re-read before its hash moved — `evidence-check --reverify` after
the reading, never as the reading — and each carries the re-read note and the
date it was read.

**A `--reverify` rewrites hashes and writes no note, so the note is the
implementer's.** The command names what it changed and nothing more; a row
whose hash moved with no sentence saying who re-read it and against what is a
row that re-dates itself, which is the failure `seal/ledger.md`'s own header
warns about for the file-level stamp.

**`gather_changelog.py --check` exits 1 on this branch and that is the
correct state.** The fragment is ungathered until the release gathers it, and
that step exits early on any base but `main`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `broad_gate.py` from the document pin's block-walk list | its docstring, checked through the parsed module by `test_the_gates_own_docstring_says_the_base_is_resolved` |
| the four drifted hashes | the same rows, re-verified, each with the note and the date of the reading that justified it |
