# Survivors — settle leaves twelve directories with no way out

`bin/survivor-check --range origin/release/v0.14.0...HEAD`, run at phase 7,
reported fifteen places. Each was opened and judged; every one is correct
where it stands. What this branch removed is the range row's use **by a
fold** (`skills/settle/SKILL.md` §*What a fold branch owes*) and two sentences
of `settle.py` that moved rather than went; the range row itself, and the
rule that a branch deleting a shipped section takes one, are unchanged for
every branch that is not a fold, so the places stating that rule are right.

| Path | Quote | Grounds |
|---|---|---|
| `docs/review-chain-spec.md` | A range that removes a shipped section whole takes one row for the range | The spec of the range row, which still ships in `survivor_check.py` and still serves any branch that deletes a shipped section. This branch removed only its use by a fold, whose retired directories the sweep now leaves out of the range (phase 4) |
| `docs/review-chain-spec.md` | Writing 153 rows is not an escape anybody takes | The same section's measurement of why the range row exists; true of any deletion, and the row still exists |
| `docs/review-chain-spec.md` | The row is anchored on the range and on the work item whose | The range row's two anchors, unchanged in `survivor_check.py#whole_range`; the removed copy was the settle skill handing a fold that row, which a fold with no directory cannot hold |
| `skills/code-review/scripts/survivor_check.py` | Every sentence of the section stands in the durable copies that are supposed to survive a deletion | The module's own §*A deletion is one row*, which still describes the mechanism it implements. Phase 4 added §*A retirement is out of the range* beside it rather than retiring it |
| `skills/code-review/scripts/survivor_check.py` | Writing 153 rows is not an escape anybody takes | The same comment block's measurement, true of the mechanism that still ships |
| `skills/code-review/scripts/survivor_check.py` | A branch that DELETES a shipped section leaves every sentence of it standing | `read_exemptions`'s docstring for the range-row shape it still parses |
| `agents/smith.md` | Every sentence of the section stands in the durable copies that are supposed to survive a deletion | smith's fix-pass instruction for a range that deletes a shipped section — a review fix pass, never a fold, which after #517 opens no work item and so runs no fix pass |
| `skills/code-review/orchestration.md` | because per-survivor rows do not scale to that case | The review orchestrator's statement of the same mechanism, for the same branch shape; unchanged by this work |
| `CHANGELOG.md` | 153 places at similarity 1.60 | A released changelog entry, a record of what that release did; a released entry is not rewritten |
| `tests/test_a_corrected_sentence_survives_elsewhere.py` | one of them correct as a report and none of them a defect | The comment above the case that pins the range row, which still ships and is still pinned |
| `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/survivors.md` | This branch removes four released work items' directories whole | The previous fold's own range row, anchored on its range and its work item; it states what that fold did, and the directory goes with the next fold |
| `skills/settle/scripts/settle.py` | This command folds work items, and a repository with none | The refusal for a repository with no `seal/` root at either place, which still exits 2. The removed copy was the refusal for a present root with no `seal/specs/`, which is now the settled state and exits 0 (phase 5) |
| `.github/scripts/fold_ledger.py` | table.append(lines[n]) n += 1 if len(table) >= 2 | The evidence-todo rule's copy in this repository's release automation, which a shipped script may not depend on and which keeps its own spelling for that reason. The removed copy is `settle.py`'s, which moved to `unverified_check.py#todo_open_rows` (phase 3) |
| `seal/ledger.md` | The phase commit that carried this is in the work item's | A different row's Notes stating the ledger's general convention, that a row records what was read and the commit lives in `plan.md`. The removed row shared the phrasing, not the claim |
| `hooks/worktree-guard.py` | asks the same question of a command that | A comment about the worktree consent hook, which shares a phrase with a test comment this branch rewrote in `tests/test_a_finding_id_is_a_bare_integer.py` and nothing else |
