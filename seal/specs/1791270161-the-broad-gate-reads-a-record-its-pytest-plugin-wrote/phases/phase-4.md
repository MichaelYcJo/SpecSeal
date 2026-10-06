# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 56b4c705 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The regression corpus (`spec.md` S20): `REGRESSED_WORDS` re-derived from
each layout's `at_base`, `word_for` reduced, the phase-4 skip removed, and
every new or changed case seen red (§15). Q2 stays the owner's, with (a) as
built.

## What this phase found

**The corpus found a defect in the recorder, and it is #789's class.**
The words were written first, by construction from each layout's base:
`on` where the base's own run fails a test collected from the file, `new`
where it collects the file and passes it or ends 0 without collecting it,
and `not-reached:<exit>` where the row ended non-zero before any session
collected the file. 46 of 55 cases read exactly those words on the first
run. The nine that did not — Q4 under both rows, N1 and N1-xdist under both,
N1b under both, and N1c — each read `failing on base too` for a file the
base passes.

The cause is `report.location[0]`, which the recorder used for a test's
path. pytest builds it from `reportinfo()`, which names the file that
DEFINES the test function, so a test a module inherits from a base class, or
imports from another module, was written under the defining module: the
base's `test_users.py` failing an inherited `test_shared` was recorded as a
failure of `test_api.py`. `spec.md` R4 and §*The class* read it the other
way ("a test a module inherits from a helper is reported under the module
that collected it"); `overview.md` holds the divergence row. The recorder
now writes `report.fspath`, the node id's path — the collecting module —
as its `collect` lines already did.
`test_a_test_is_recorded_under_the_module_that_collected_it` holds it, plain
and under `-n 2`: red with `location[0]` (both failures collected in
`test_collects.py` written under `test_defines.py`), green with `fspath`;
it and S1 also pass under pytest 7.4, 8.0 and 8.1 through `uvx`. After the
fix all 55 corpus cases pass, so no layout of the corpus gives
`failing on base too` to a file its `at_base` passes (S20).

**The words, and what moved.** Every layout whose base row is red for a
reason other than the compared file reads `new?` naming the exit — P1 and
its six variants (Q5, Qf ×3, R1 ×2), P2, Q1, Q3b, Q4, R2 and R2b under both
rows, Q3, R3 and N3 under their own rows, and every `sub` file of the three
P7 layouts under both, whose base root runner stops `&&` before `sub`. That is `questions.md` Q1's trade, built as (a).
Q3 under the files-only row reads exit 5: its base run is `pytest -q a`,
which collects no test. P3 ×2, Q8 and Qs2 read `new` (the root runner passes
the file at the base), R3 and N3 under the files-only row read `new` (that
run collects `gen` and `vendor` only and passes), N1 ×4 and N1b ×2 read
`new` (the base passes `test_api.py`'s own test), N1c reads `new` for
`test_api.py` and `failing on base too` for `test_users.py`, whose own
inherited test the base fails, and N7 reads `failing on base too` under both
rows. `word_for` is reduced to `new`, `on`, `not-reached:<exit>` and
`no-record`.

**Seen red, executed:** the nine inheritance cases against the
`location[0]` recorder, and the new recorder case against it. With
a9d7b0e5's `broad_gate.py` put in place at 56b4c705 and restored from it
afterwards, 49 of the 55 corpus cases were red; the six green there — R3,
N3, N1, N1-xdist, N1b and N7 under the files-only row — read the same word
at a9d7b0e5, so their rows did not change.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the corpus case's `skip` mark and `word_for`'s `beyond`, `multi` and `company` kinds | nowhere: the words they spelled retired in phase 2 |
| the recorder's read of `report.location[0]` | `report.fspath` |
