# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 48d201ad |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The reader: one new function in `evidence_check.py` that reads node ids from
the Code grounds cell through `grounds_cells`, resolves each through the
Python reading with the parts joined by `.`, and grades OK / BROKEN /
MALFORMED as `spec.md` D2 says; `malformed_rows` no longer refusing a
node-id-only cell and refusing a mixed one (D4); `check_ledger` adding the
findings. Scenarios S1–S6, S8's `--reverify` half, S11 and S12, each seen red
against the unfixed checker. The orchestrator added that #867 had landed on
`release/v0.21.0` and was merged into the branch, and that #870 is being
built at the same time against `generic_units` and the generic arms of
`file_units` and `resolve_unit`, which this phase was to stay out of.

## What this phase found

**#867 moved nothing this phase reaches for.** `grounds_cells`,
`ledger_table_rows`, `CODE_SPAN_RE` and `place` are where the frame found
them. The coordinate grammar #867 exported (`ANCHOR_PATH`, `ANCHOR_LOCATOR`,
`ANCHOR_HASH`) is not used: a node id is a different token, as `spec.md`
§*Data & interfaces* says, and `ANCHOR_RE` is untouched.

**`py_spans` cannot say what a unit is**, and D2 needs to: a test is a
`def` or a `class`, and `py_spans` also keys module- and class-level
constants under the same qualified names. So the resolver is a walk of its
own, `unit_kinds`, written as `parsed_spans`' walk with the kind recorded
instead of the span, memoised on the text and handing each caller a fresh
dict the way `py_spans` does. `parsed_spans` itself is not edited, so none of
the released rows citing it drift. `named_unit(text, names)` is the
`path::name` resolver phase 3 points `fold_check.py` at, and
`collected(names, kinds)` is the ledger's acceptance: every outer part a
class named `Test…`, the last a `def` named `test…` or a class named
`Test…`, each defined once.

**The new arm is `held_by_tests`, and it reads every row, citing or not.**
`check_ledger` blanks a citing row's line before `check_text`, but
`malformed_rows` and this arm read the text whole, so a `Corrected ·` row
holding its citation and a node id is graded here — which is what S5's
second half and phase 2's S7 lean on.

**`reverify` changed as well, which the frame did not list.** S8 asks for a
`left` line naming a test that is gone, and `reverify` is where the in-place
run prints its `LEFT` lines; a test row's non-OK finding joins them, and the
run exits 1 as it does for a malformed row. The frame's "units it changes"
list in `spec.md` §*The seam* names `malformed_rows`, `malformed_remedy`,
`check_ledger`, `reverify_into` and one new function; this phase changed
`malformed_rows`, `check_ledger` and `reverify`, and added `node_tokens`,
`_parsed_kinds`, `unit_kinds`, `named_unit`, `collected`, `node_finding`
and `held_by_tests`. `malformed_remedy` is not changed: it is the remedy for
a coordinate that does not parse, which is plainly a coordinate attempt, and
the two forms are named instead in the *cites no coordinate* remedy and in
the new `MIXED_ROW` and `NOT_A_TEST` sentences. Phase 5 reads the drift of
`reverify`'s rows on top of the frame's list.

**No new function is named `test…`.** The frame's text calls the reader of
one token a *test node*, and a function spelled `test_node` in a module a
test imports by attribute is one rename away from pytest collecting it. It
is `node_finding`.

**S12 runs through a helper of the new module rather than
`tests/test_evidence_check.py`'s `vendored_copy`**, which is a plain
function in another test module; the helper is its three lines, and every
S1–S5 case is parametrised over the plugin copy and the vendored one.

**Seen red (§15).** Every unit added or changed was broken through
`bin/mutation-check` against 48d201ad with the whole module as its cases,
and every verdict was `red`:

| Break | Case that went red |
|---|---|
| `check_ledger` without `held_by_tests` | S1 and 25 others |
| `malformed_rows` without `and not tests` (the unfixed *cites no coordinate*) | S1 and 26 others |
| a gone unit returned `OK` | S2, S8 |
| no bare-method hint | S3 bare |
| `named_unit` keyed on the last name | S3, resolver |
| `collected` skipped | S4 (all four kinds) |
| no mixed refusal | S5 |
| a citing row's citation counted as code | S5 citing |
| every cell read for node ids | S6, S11 |
| `reverify` naming no test left | S8 |
| bare words read as node ids | S11 |
| `unit_kinds` handing out the memo | resolver |
| a unit defined twice accepted | twice |
| outer classes not checked | S4 `Holder::test_d` |
| any extension accepted | the `.txt` token |
| any `def` accepted | S4 `helper` |
| a missing file returned `OK` | file gone |

Executed, with this phase's output read: the new module, 35 passed;
`tests/test_evidence_check.py` and
`tests/test_a_released_row_is_read_again_in_a_fragment.py`, 516 passed,
unchanged; the six other modules that read MALFORMED, 385 passed;
`uvx ruff check` and `uvx ruff format --check` on both files.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
