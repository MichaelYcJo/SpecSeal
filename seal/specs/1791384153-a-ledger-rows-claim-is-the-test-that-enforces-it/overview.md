# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     pending — filled when the build closes
· evidence: pending — filled when the build closes
· verified: pending — filled when the build closes

## Why this work exists

A ledger row may name the test that holds its claim instead of a hash over
the code, so the row never drifts and nobody re-reads it after every edit;
the suite says whether the claim still holds.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How a node id is resolved | `spec.md` D2: "resolved through `evidence_check.py#resolve_unit`'s Python branch … the qualified name `py_spans` already keys on" / a walk of its own, `unit_kinds`, keyed by the same qualified names | `unit_kinds` | D2 also says "a `def` or `class`" and "a function beginning `test`, a class beginning `Test`": `py_spans` returns spans and keys constants under the same names, so it cannot tell a test from `TEST_X = 1`. `parsed_spans` is left as it was, so no row citing it drifts |
| Which units change | `spec.md` §*The seam*: "`malformed_rows`, `malformed_remedy`, `check_ledger`, `reverify_into` (one sentence), and one new function" / `malformed_rows`, `check_ledger`, `reverify`, `reverify_into`, seven new functions; `malformed_remedy` unchanged | as built | S8 asks for a `left` line naming a gone test, and `reverify` prints the in-place run's `LEFT` lines. `malformed_remedy` answers a coordinate that does not parse; the two forms are named in the *cites no coordinate* remedy, `MIXED_ROW` and `NOT_A_TEST` instead (`phases/phase-1.md`) |
| Where S12 runs | `spec.md` S12: "`tests/test_evidence_check.py`'s `vendored_copy` fixture" / a three-line helper in the new module, every S1–S5 case parametrised over both copies | the new module | `vendored_copy` is a plain function of another test module; importing across test modules is a dependency the suite has nowhere else |
| When `--into` names the test row | `spec.md` D5: "names the option once per run, in its summary line, unconditionally" / S9 and §*Data & interfaces*: "printed once per run that writes a `Re-read ·` row" | once per run that writes one | the scenario and the interface section agree with each other, and a run that wrote nothing owes no reader a second repair |
| What the new section states | `spec.md` D7: "It states D1–D5 as the rule" / five statements, the fifth D6's one resolver | D1–D6 | a reader of `fold-check` meets the resolver as much as a reader of the ledger, and `spec.md` §*Scope* D6 is a decision of the same standing as the five |
| Seams written before #867 | `plan.md` §*Seams*, written before #867 landed / #867's grammar exports (`ANCHOR_LOCATOR`, `ANCHOR_HASH`, `ANCHOR_QUOTED`) and heading rule are not used | not used | a node id is a different token from a coordinate (`spec.md` §*Data & interfaces*: "no new regular expression for a coordinate is added anywhere, and `ANCHOR_RE` is not touched"); `grounds_cells`, `ledger_table_rows` and `place`, which this does use, are where the frame found them |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |

## Not done

nothing yet

## Fed back into the spec

none yet
