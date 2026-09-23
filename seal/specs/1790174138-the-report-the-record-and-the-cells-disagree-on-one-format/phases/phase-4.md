# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 20ceba4f |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The `Broad gate` cell holds every run — #174. `seal` writes the new entry
first and keeps the cell's earlier entries, for both homes;
`new_broad_gate_file`'s comment, `templates/sdd-round.md`'s cell comment,
and the six documents listed in `spec.md` §Data & interfaces say *newest
first, one entry per run*. `chain_check.broad_gate`'s docstring says why
`named[0]` is the run. Cases A12, A13, A14. Ledger G2 and the `direct_seal`
row re-read. `skills/verify/SKILL.md`'s run-level row reads the count off
the cell. Decide Q4, the separator.

## What this phase found

**The frame holds for this phase.** `seal`'s six refusals, `new_broad_gate_file`,
`broad_gate`'s `named[0]` and `direct_seal`'s delegation were each where
`plan.md` put them, and the seven documents were where `spec.md` listed
them. One more carrier turned up and moved with them: `skills/code-review/SKILL.md`'s
files table describes the cell as *the SHA the one full-suite run happened
at*, and is now the eighth.

**Q4 answer: `; earlier run: `**, the frame's default. Against the three
constraints the readers impose — no `|`, no SHA-shaped word, no `<!--`,
newest SHA first — it holds on reading and on execution: `broad_gate` and
`direct_seal` run over a two-entry cell with `WORKTREE` on return no error
and no notice, which is the assertion inside A12 and A14. The constant is
`EARLIER_RUN` in `round_record.py`, with the constraints beside it.

**The writer reads its other home before it writes.** `seal` used to build
`broad-gate.md` from the new value alone; keeping an earlier run there means
reading the file that is already there, for that one row and nothing else.
The `n is None` branch does that now, and the mutation that skips the read
is red on the direct case alone — which is what says the direct case pins
the read rather than the write.

**Seen red at `48acddf6`** (executed), with `EARLIER_RUN` present and the
writer unchanged, so the red is the cell rather than a missing name:

```
E       assert '48a76cf against base' == '48a76cf agai... against base'
E       assert '351b123 against base' == '351b123 agai... against base'
FAILED tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest
FAILED tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_direct_home_takes_the_same_shape_on_a_re_seal
2 failed, 4 passed
```

Before the constant existed all three were red on `AttributeError`, and
with it `test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list`
was green — A13's control, byte-identical before and after.

**Then green** (executed): `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q`
124 passed; `tests/test_chain_check_at_the_pull_request.py -k "broad_gate or
direct or gate"` 21 passed. Fourteen document-pinning modules over the files
this and the earlier phases edited: 484 passed, 8 skipped, one red —
`test_docs_line_wrap.py` at `skills/code-review/orchestration.md:529`, a
97-character line this phase's own edit produced, rewrapped; the module is
31 passed after.

**Four mutations, restored from kept bytes** (executed): M1 the old
replacing writer — the two re-seal cases red; M2 the earlier run written
first — the same two; M3 `not yet` kept as an earlier run — seven red, every
first seal in the module; M4 `broad-gate.md` not read before the write — the
direct case alone.

**Ledger:** A5 in the fragment. Twenty-six rows drifted — ten anchored on
`seal` or `broad_gate` (G2, S6, S9, S10, S13, the two last-record rows, the
one-word row, the no-second-reader row, C3) and the rest on document
sections the eight carriers sit in — and each carries a dated note. One
line the anchor grep matched, `seal/ledger.md:2535`, is the continuation of
a note rather than a row and was left alone.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the one-entry `Broad gate` cell that every `seal` replaced — the writer's overwrite, and the sentence *one SHA with the base it was compared against* in `skills/verify/SKILL.md`'s run-level table | the newest-first cell and the eight documents that now say *one entry per run, newest first*; #159's principle that a landed value is not overwritten is met for this one cell, and its sketch for the rest stays in `plan.md` §Alternatives |
