# Implementation Plan: every copy out of `raw` meets the hider question

<!-- seal/specs/1788873610-every-copy-out-of-raw-meets-the-hider-question/plan.md -->

## Summary

**Ask the question at the destination.** Every copy the record generator
makes out of `raw` lands in one artefact, so the record's own text is the one
place where every copy path — the three the grid names, the fourth it does
not, and the fifth somebody adds next year — is answerable at once. One
function writes a record; it reads the record back through the shared reader
first and refuses one no reader can read.

That is the whole of part 1. It is also the cell the `# RIDER:` in
`swallowed` left open: a comment balanced in the report and half in the
record is exactly a record the reader cannot read, and *balance across the
slice* asked of the destination needs no knowledge of which slice.

## Technical context

`skills/code-review/scripts/round_record.py`, 2670 lines. What this builds on:

- `swallowed`, lines 839–970: the report-wide rule, two never-closed
  questions and three positional loops. Its first two questions move into
  the shared function and its messages keep their bytes.
- `build`, lines 1399–1530: composes the record and asks the round paragraph
  the same two questions inline. Same move.
- `new` / `reach_back` / `close`: the three functions that call
  `open(..., "w")`. All three come to go through `write_record`.
- `reader.strip_comments` / `blank_fences` / `readable`,
  `skills/verify/scripts/unverified_check.py` lines 105–158: indices intact,
  comments blanked before fences. The order of the two questions is a
  property of that pass order and not of any one text, which is why one
  function can hold it for every text.

**What breaks in six months.** A record legitimately quoting an unbalanced
marker. A reviewer of this generator pastes record-shaped and report-shaped
blocks into a report, and a report-shaped block carrying `<!--` with no
closer would now be refused at the record rather than at the report — the
tool stopping inside its own review rounds, which
`REQUIRED_HEADINGS`' own comment names as the thing this guard must never
do. Two things bound it. A fenced block is copied whole, so a balanced
comment inside one stays balanced in the record; only a SLICE can take half,
and a slice taking half is the defect. And it is measured rather than
argued: all **163** records committed under `seal/specs/*/rounds/round-*.md`
were read through both passes at `8114937` and none has an open hider.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Ask the question of the record being written** (chosen) | a record that legitimately ends inside a hider is refused, and the only way out is to fix the report. Bounded above: 163 committed records, none affected | **chosen.** One call per writer, no enumeration of copies, and a fifth copy path is caught rather than described |
| Add a fourth row to the grid — the hider question asked of every earlier record `inherited_rows` reads | it is a whole-text question on an input read for named sections, so it refuses a file this repository already has (`round-1-fixes.md`'s code-span marker). Narrowed to the section, it is `swallowed` parameterised over three constants — a refactor of the one function five ledger anchors name, for a copy the reader's own arithmetic already refuses loudly | rejected. It is the count answer with one more row, and the ticket's own diagnosis is that a row axis chosen by listing sources is what failed twice |
| Teach `strip_comments` about code spans, so a marker inside backticks is not a hider | it is the shared reader. Every comparison in this plugin agrees only because both sides run the same passes, and a change here moves `evidence-check`, `unverified-check` and `chain_check` at once | rejected, and out of scope by `spec.md` §Out |
| Leave the message wrong and document the straddle | §14 exists because a message a person acts on is behaviour. A refusal naming a fence that closes sends a reviewer to look for something that is not there, which round 2 of the same chain already paid for once | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `open_hider` with its third answer, `opens_at`, `hiders_close`, and the two straddle messages. `swallowed` and `build` ask through it | the two straddle cases seen red at `8114937`, then green; the 94 cases of `tests/test_the_record_is_generated.py` | 4f4e83f |
| 2 | `write_record`, the three writers through it, the record message set, and the AST property case | the flag case and `close`'s case seen red, then green; the AST case seen red (no `write_record` exists at `8114937`); the module, and `tests/test_the_fixes_close_the_record.py` | c6ba3b2 |
| 3 | the four documents, `seal/ledger.md` F2 re-verified, this work item's fragments, `docs/flow.md`'s own row | `evidence-check --reverify` on the rows this change drifted; `tests/test_the_record_is_generated.py` for the grid comment's replacement | 6da4c4b |

## Operational impact

**One behaviour change a person meets.** `round_record.py new` and `close`
now refuse a record whose text the shared reader cannot read end to end, and
print which line opens the hider. No migration, no new flag, no new
dependency. A record already on disk is untouched — the question is asked of
what is about to be written, never of what is there.
