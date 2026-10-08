# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     this work item's `handoff.md`, `routing.md`, `spec.md` (D1–D8, S1–S14), `plan.md`, `questions.md`; `docs/the-evidence-ledger.md` §*A row is a content anchor*, §*A released row is read again in the branch's fragment*; `CONTRIBUTING.md` §*What a change to a gate must carry* (direction: blocks more; prompt budget: zero); `skills/agent-contract/SKILL.md` §12, §14, §15
· evidence: `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md` — T1–T13, each a row held by a test; five `Corrected ·` test rows moving released rows onto their tests (0.15.4 ×2, 0.15.5 S6, 0.18.0 L10, 0.18.3 A2); 33 `Re-read ·` rows written by `--reverify --into` after each claim was read; nine rows of `1791384154` and `1791384156` re-stamped in place
· verified: executed — every new case seen red through `bin/mutation-check` and green after, phase by phase; each phase's touched modules; `bin/fold-check` exit 0; `bin/evidence-check --strict .` exit 0 (0 drifted, 0 refused); `bin/survivor-check --range origin/release/v0.21.0...HEAD --exempt …` exit 0; `bin/correction-check --range origin/release/v0.21.0...HEAD` exit 0; the eight modules the orchestrator named, 437 passed; `uvx ruff check` and `uvx ruff format --check` on every changed `.py`. Read — each of the 38 drifted released rows' claims and the six sibling rows on `agents/warden.md` against the diffs. Unverified — the full suite (the sealer's)

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
| How many released rows phase 5 owed | `spec.md` D8: "2, 3, 1, 0, 6, 2, 4 and 2 claim rows at 5623d728, the bookkeeping rows citing them on top" / 114 drifted findings, 38 released families and 9 sibling rows | as measured | `reverify` (cited by 106 coordinates) and `FROZEN_REPAIR` were edited, for S8 and Q4, and the frame's count did not reach them; 8 of the 114 were the base's own `agents/warden.md` drift (`phases/phase-5.md`) |
| Seams written before #867 | `plan.md` §*Seams*, written before #867 landed / #867's grammar exports (`ANCHOR_LOCATOR`, `ANCHOR_HASH`, `ANCHOR_QUOTED`) and heading rule are not used | not used | a node id is a different token from a coordinate (`spec.md` §*Data & interfaces*: "no new regular expression for a coordinate is added anywhere, and `ANCHOR_RE` is not touched"); `grounds_cells`, `ledger_table_rows` and `place`, which this does use, are where the frame found them |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |
| The new cases on the Windows and Linux legs (the vendored copy, the node-id paths with `/`) | CI at the pull request |
| `bin/evidence-check --strict .` after `origin/release/v0.21.0` is merged in: its head carries 22 drifted coordinates this branch does not (`templates/config.md#"# Repository config"`, `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS`), and #870 edits `evidence_check.py` beside this | the orchestrator, at whichever merge of the release branch lands second (`plan.md` §*Sequencing with the siblings*) |

## Not done

**No bulk pass over the released rows that cite a test**, by the owner's
answer to Q1 (a): only the five released rows this branch's edits drifted
and a test already held moved onto their tests.

**`hooks/evidence-advisor.py`'s heading line still says *anchors broken***
when the broken row is a test row. The line counts BROKEN findings, and a
test that is gone is also a citation that does not resolve; it was left.

**`malformed_remedy` is unchanged**: its remedy is for a coordinate that does
not parse, and the test form is named in the three remedies that answer a
cell with no coordinate or a cell naming a test.

## Fed back into the spec

`spec.md` §*Out*, the pytest-configuration row, carries ` · NAME NOT IN
TREE` (inferred during implementation): the records arm refuses
python_classes, pytest's key and no name of this tree, once the item has a
fragment. No clause was added to the spec.
