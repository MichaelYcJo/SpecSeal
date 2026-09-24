# 1790263216-the-older-statements-name-what-enforces-them — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 835268a4 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

Lower the cutoff to `0`, in one commit with every sentence that states or
relies on the old one:

- `seal/config.md`'s `Fold shape from` row;
- the first two statements of `docs/the-evidence-ledger.md` §*The fold …*;
- the module docstrings of `tests/test_a_folded_statement_names_what_enforces_it.py`
  and `tests/test_a_document_has_room_for_the_next_fold.py`.

The first statement had to keep ``from work item `N` on`` for the pin's
regular expression and the settle link with its line break. It had to state
what the cutoff was, that #565 lowered it, and the 115 with its command and
its date. Its `Enforced by:` line names `fold_check.py::bound` and the
real-tree case. Then `bin/fold-check --shape-from 0` runs over the whole
tree. S1 to S4 and a clean `evidence-check`, the stacked fragment's rows
included, verify it.

## What this phase found

**The first statement's new opening** is *Every folded statement has the
fold's shape: the cutoff binds every statement from work item `0` on*. The
words `from work item` and `` `0` on`` sit on one line, because the pin's
regular expression has literal spaces and a line break inside the phrase
would not match. The count is given as the spec asked: `fold-check
--shape-from 0` on 2026-09-25, 136 statements, 115 without the line. It
carries a date and not a SHA, because the branch squashes.

**One ledger claim became false, and it is the stacked item's.** F6 in
`seal/ledger/1790260563-…md` claimed *this repository declares `Fold shape
from` `1790154761`*. It was corrected in place to `0`, with the old value
kept in brackets, and a `Corrected 2026-09-25` note. Its anchors are test
functions, which this phase did not touch, so `evidence-check` names no drift
there. The claim was found by searching the ledger files for the old value,
not by the checker. F3 and F5 in the same fragment record runs at
`1790154761` with their dates. They are records of those runs, and they
stay true.

**What else carries the old value, and stays.** `templates/config.md`'s
example row keeps `1790154761`, by `spec.md` §*Out, and why*. The stacked
item's changelog fragment says the repository declares `1790154761`. It is
that work item's, and it is named in the overview's *Not done*.

**The survivor sweep, run over the whole branch** (`e9dfe623..HEAD`), named
two places still carrying the rider sentence phase 5 corrected:

- `docs/one-root-by-lifetime.md` §*The dependency rule*, with its Korean
  edition. It was corrected in both editions in `835268a4`. It is unmarked
  prose, and the same false half as D89.
- `CLAUDE.md`. `survivors.md` exempts it, with a quote and the ground that
  this work item does not edit it.

With the exemption, the sweep exits 0.

`4ba7472b` lowered the cutoff, and `835268a4` is the survivor correction.
The phase closes at the second. After it, `bin/fold-check`, `bin/fold-check
--shape-from 0` and `bin/evidence-check .` were run again with the same
results as above. 17 modules that read the one-root documents, the overviews,
the changelog fragments or this work item's records ran: 1045 passed.

**What the common checks returned** (executed 2026-09-25):

- S1: `bin/fold-check --shape-from 0` exits 0: 136 statements read, the
  cutoff 0 binds 136.
- S2: `bin/fold-check` exits 0. Its first line reads *the cutoff 0 binds
  136*.
- S9: 14 documents are held to 1000 lines, and 0 are listed over.
- S11: `bin/evidence-check .` gives 2094 ok, 0 drifted, 0 broken, and
  records 2 work items read with 0 refused.
- S3: 32 modules ran in one command, 1691 passed. They are the modules that
  read `seal/config.md`, `docs/the-evidence-ledger.md` or either edited test
  module, and the base set. Both pin modules are among them.
- `uvx ruff check` and `uvx ruff format --check` passed on the two test
  modules.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `4ba7472b`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M22 | S4: one retrofitted line (`docs/the-broad-gate.md`'s first) deleted | `test_every_bound_statement_in_docs_has_the_shape` | red, 1 failed |
| M23 | `seal/config.md`'s row moved back to `1790154761` alone | `test_the_evidence_ledger_states_the_values_the_config_rows_hold` | red, 1 failed |
| M24 | a named target, `test_every_ast_constructor_is_classified`, renamed | `test_every_bound_statement_in_docs_has_the_shape` | red, 1 failed |

M24 is the commoner rot `plan.md`'s failure scenario says the design does
catch: a target renamed under its line fails the next suite run.

**Across the seven phases:** 115 decisions, D1–D115. 103 name targets and
12 say `nothing`: 7 of case 1, 0 of case 2, 2 of case 3 and 3 of case 4.
24 mutations were executed and restored. 20 decisions were mutated, and the
other 83 decisions with targets were read.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the prose sentence *the 101 folded before it … Those 101 were written with no line* | the rewritten statement, which states the old cutoff and the 115 with the command and its date |
| the rider half of `docs/one-root-by-lifetime.md`'s coupling sentence, in both editions | corrected in place; `test_no_rider_stamp_names_a_commit` holds the true state |
