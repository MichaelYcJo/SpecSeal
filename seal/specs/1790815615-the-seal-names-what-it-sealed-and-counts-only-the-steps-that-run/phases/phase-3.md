# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — phase 3

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8a724d2d |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 3 (S4): `broad_gate.py` reads the item's last record from the
working tree through `chain_check.py` loaded by path, the way
`round_record.seal` does: `Needs a fix` through `field`, the verdict rows
through `verdict_table`/`verdict_of`, homes deduplicated in table order;
`rounds <R> . capped` and the `<k> deferred -> <homes>` continuation; the
`PR` read of phase 1 moves onto this reader if phase 1 wrote a narrower one;
`round_count` stays the count. Docs: `agents/sealer.md`'s exit-0 bullet, the
`broad_gate.py` module docstring. `questions.md` Q2's measurement is taken
here and recorded in this file.

## What this phase found

- **Q2, measured** (a probe, `test_tmp_q2_capped.py`, run once over every
  `seal/specs/*/rounds/` on this branch with `chain_check`'s own `PASS_RE`,
  `field(rows, NEEDS)`, `verdict_table` and `verdict_of`, then deleted):
  36 work items' last records have `Pass` checked. 14 read `Needs a fix |
  yes`, and **every one of the 14 holds a `deferred <home>` verdict** — no
  record reads `yes` without a deferral. 24 hold a deferral, so **10 read
  `no` and hold one anyway** (e.g. `1790297086-the-broad-gate-says-what-ci-says`,
  `1790745049-the-guard-and-consent-stop-depending-on-the-walks-order`).
  Q2's options say exactly what that means: those print the continuation
  and not `capped`, which S4 allows; and nothing found is a `yes` record
  `seal` accepted that is not a capped run, which is the only thing that
  would move the definition. S4 stands as written. `questions.md` Q2 is
  marked answered with this measurement.
- **`verdict_of` does not return the home** (the frame correction phase 1
  named). `deferred_home` reads it off the same cell, after the same
  normalisation (`chain_check.EMPHASIS`, `MARKER`) and up to the same
  `SEPARATORS`, and only for a row `verdict_of` already called `deferred`,
  so the vocabulary is still `chain_check`'s; what it adds is *the first word
  after the word is the home*.
- **No second record reader.** Phase 1's `sealed_record` already found the
  record through `round_record.seal_home` and read it with `chain_check`'s
  `table_rows`; `rounds_rows` asks the same `Record` for `Needs a fix` and
  the verdict table. The `PR` read did not move: it was on this reader from
  the start.
- **Half an answer is `<R>` alone.** S4 lists *no `## Verdicts` section, no
  `Needs a fix` row, or a `broad-gate.md` home* as printing `rounds <R>`
  alone, and the code takes that literally: without both the row and a
  readable table, neither `capped` nor a count is printed.
- **Homes are joined with `, `** (Q4's spelling for several homes), and the
  continuation passes through `fit` like every value, so three homes, one a
  path, elide at the frame with `...` rather than widen the row
  (`test_no_value_on_the_panel_is_wider_than_the_frame_gives`, extended).
- **Seen red (§15):** the 14 new and extended cases run against `998adaea`'s
  scripts and `agents/sealer.md` (restored from kept bytes after): all 14
  failed. 14 mutations, one at a time, bytecode cleared between them; none
  survived.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
