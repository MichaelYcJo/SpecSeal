# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 6f8c94db |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The cut, in one commit. Write `docs/the-commit-gate-inside-git.md` and
`docs/the-review-and-parity-arms.md` from base lines 41–277 and 760–994 with a
script that asserts each boundary heading before it copies, and take the lines
out of the parent the same way. Add the H1s, the `Authority for` paragraphs and
the arms file's `## The two arms of the commit gate` (D3); rewrite the parent's
preamble as its index, before `## Registration` (D4). Turn the K6 crossing
lines into citations (D5), and answer W1 (does any other positional line cross)
and W2 (the preamble and index wording). Set `Over the ceiling` to `none`,
rewrite the evidence ledger's fold statement and the fold pin's docstring (D8).
Make every K2 site follow its text (D10).

## What this phase found

**The move script asserted ten boundaries** — the blank line 40, the headings
at 41, 194, 268, 278, 760, 955 and 995, and the blank lines 277, 759 and 994 —
and dropped the trailing blank line of each moved block. It counted 236, 234
and 575 base lines. `spec.md` §*Data & interfaces* says 576 for the parent;
40 + 482 + 53 is 575.

**The three files' sizes at 6f8c94db**, by `wc -lc`:

| File | Lines | Bytes |
|---|---|---|
| `docs/commit-review-gate-spec.md` | 586 | 39,500 |
| `docs/the-commit-gate-inside-git.md` | 254 | 21,263 |
| `docs/the-review-and-parity-arms.md` | 250 | 16,761 |

**W1.** The six K6 lines crossed as the frame said, and one more did: line
152, *the PreToolUse reading in the next section stands aside*. K6's command
matched `above` and `below`, and `next section` matches neither. In its new
file no section follows, so it became a citation in D5's shape. The other 19
lines were re-read against the files as they landed, and each points within its
own part: in the arms file, 764 (*see below*) and 765 (*The declaration*
below) reach `#### Where the marker goes` and `#### The declaration`, 767 and
802 reach the paragraph that follows them, 868's *row above* is the
declaration table, and 925's *paragraph below the review arm's table* is in the
same file. In the parent, 738 and 740 cite *Two operators consume one, not one*
and *A file edit goes through the `Edit` tool*, both of which stay. 925's *of
this document* is left verbatim: the paragraph it says was reversed sits in the
arms file now, beside it.

**W2.** The new files say what each holds and name the parent, the other new
file, `docs/review-chain-spec.md` and `docs/round-record-spec.md`, and close
*Update spec and code together*. The parent keeps its first line, so the
`"Authority for"` minor anchor of `seal/releases/0.15.1.md` S2 still finds it,
and indexes the two new files as a two-item list, one question each (what git
decides; what each arm wants), all before `## Registration`.

**One crossing line sits inside an anchored unit.** Base line 199 is in
`### Known limits of the commit gate inside git`, which `seal/releases/0.17.0.md`
G17 cites. Re-pointing it changes the unit's hash, so G17's `Corrected ·` row
records a new hash, not the released one. D2's *every moved unit hashes as
before* holds for the arms' two headings and not for this one. Phase 3 writes
the row.

**Verified, executed.**

- The S1 probe, `test_tmp_s1_the_cut_is_a_move.py`, run once from the
  scratchpad and deleted: `difflib` over each moved block against `git show
  2b1dcb1f:docs/commit-review-gate-spec.md`. The only differing lines are the
  three preambles and base lines 91, 152, 199, 273, 274, 283 and 284.
- `bin/fold-check --root .`: exit 0, 157 statements in 18 documents, every
  document at or under 1,000 lines, 0 listed over it. Markers per file 6, 8
  and 4, by `grep -c '^<!-- specs/'`.
- The 13 K2 modules, `tests/test_a_document_has_room_for_the_next_fold.py`,
  `tests/test_docs_line_wrap.py` and the six other `REVIEW_CHAIN_DOCS`
  consumers, one `bin/test` command: 1153 passed, 78 skipped, 1 failed. The
  failure was `test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
  because this work item had no `overview.md` yet; it was opened in the same
  commit, and the case passed when run again.
- `uvx ruff check` and `uvx ruff format --check` over the nine touched test
  files: clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| base lines 41–277 and 760–994 of `docs/commit-review-gate-spec.md` | `docs/the-commit-gate-inside-git.md` and `docs/the-review-and-parity-arms.md`, verbatim but for the K6 lines |
| the `Over the ceiling` entry and its digest `cb5d441b51a4` | none: no document is over the ceiling, and the row reads `none` |
| the parent preamble's claim to *the two opt-in arms, and the routing declaration* | `docs/the-review-and-parity-arms.md`'s `Authority for` paragraph |
