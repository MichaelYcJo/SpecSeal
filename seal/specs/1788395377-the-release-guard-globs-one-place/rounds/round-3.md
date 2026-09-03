# 1788395377-the-release-guard-globs-one-place — review round 3

<!-- The verifying round for round 2's fixes (target: the diff 1fb5507..2f8b12a).
It closed all five and opened three, one of them a 🔴 that would have turned
CI's windows leg red — so the bound is five rather than three while it is
open, and round 4 verifies the fixes that close it. Written by the review
orchestrator, which is also this work item's implementer. -->

| Field | Value |
|---|---|
| Target SHA | 2f8b12a (the fix diff from 1fb5507); HEAD afb3217 at review time, record-only |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | nobody — the fixes landed at d21b13a and round 4, the verifying round, is what opens them; this cell is set to it when that record exists |
| Contract changes | none — the fixes are one argument in a test, and two sentences |
| New units | none |
| Needs a fix | yes — 🔴 1 (`tests/test_chain_hooks.py:215` builds its expected path with `os.path.join` around a literal `/`, so the windows leg fails on the first iteration), 🟡 2 (the changelog credits the chain spec with a reason only the skill gives), 🟡 3 (the memo's `Fed back into the spec` says Nothing beside a header naming three documents this branch changed) |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 1 | the sentinel became an OR | `tests/test_the_set_a_work_item_always_has.py:343-348` | answered — the fix is round 2's, this round reproduced its closure | reviewer executed both halves: moving only the `evidence-todo.md` files reddens the first assertion with its own message, moving only the `tests-todo.md` files reddens the second with its own |
| r2 2 | the skill said the guard reads both files | `skills/code-review/SKILL.md:141-144` | answered — reproduced | reviewer read |
| r2 3 | three paths at two bases | `hooks/review-history-guard.py:206-210` | answered — reproduced, and the case that pins it carries this round's 🔴 1 | reviewer executed: the reminder renders three paths from one base; reverting the hook reddens only the new case, which is the case doing its job |
| r2 4 | the rung grounds answered one clause of five | `overview.md:4-9` | answered — reproduced; the same section's later paragraph is this round's 🟡 3 | reviewer read the ladder's five clauses against the branch's diffstat |
| r2 5 | the changelog described the move alone | `changelog.md` | answered — reproduced; one clause in the new paragraph is this round's 🟡 2 | reviewer read |
| 🔴 1 | `expected = os.path.join("seal", "specs", item.name, name)` with `name` holding `rounds/round-N.md` builds `seal\specs\<id>\rounds/round-N.md` on Windows, while the hook prints all backslashes. `.github/workflows/test.yml` runs the whole file on `windows-latest` and nothing skips it, and `rounds/round-N.md` is the loop's first item, so the case dies on the first iteration. `hooks/review-history-guard.py:152-158` records CI's windows leg catching exactly this mixing once already — the fix that removed it from the hook wrote it into the test that pins the fix | `tests/test_chain_hooks.py:215` | fixed at d21b13a | reviewer simulated with `ntpath`: match False before, True after. Orchestrator reproduced the same two spellings and applied the repository's existing idiom, `*rel.split("/")` — used at `tests/test_gates_do_not_fail_open.py:37` and `hooks/root-migrate.py:145`, and nowhere else in `tests/` was a literal `/` inside an `os.path.join` argument |
| 🟡 2 | the changelog says the chain spec and the skill both say the rule "with the reason", and the spec's cell gives the rule and a different reason — why to write it now, not why this location. The fragment folds into `CHANGELOG.md` at the next release, so a reader who opens the spec looking for the promised reason does not find it | `changelog.md` | fixed at d21b13a — the spec says the same rule, the skill says why | reviewer executed `grep` over the spec for the reason's words: one unrelated hit |
| 🟡 3 | `overview.md`'s `Fed back into the spec` reads Nothing with an explanation about the file move, forty lines below a header naming three documents this branch changed. Both readings are defensible — `templates/sdd-overview.md:60` scopes the section to clauses this work inferred and added, and repeating an existing rule is not one — and a reader meeting the two gets the impression round 1 was faulted for | `overview.md:50-53` | fixed at d21b13a — the section keeps its answer and says which sense of it, and names the three documents as a change rather than a clause | reviewer read the template's definition |
| 🟡 4 | one ledger row anchored on the twice-edited section has been re-hashed twice with no re-read note, while its sibling on the same anchor gained one both times. The claim is honest — this round opened it — but a reader cannot tell that from the row | `seal/ledger/1788360817-…md:48` | deferred — issue #97 already holds this axis, and round 2 put it there | reviewer executed the hash history over three commits |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the two test files | 33 passed |
| reviewer: the sentinel with each file kind moved away in turn | each assertion reddens for its own file, with its own message |
| reviewer: the reminder rendered verbatim; the hook reverted | three paths from one base; reverting reddens the new case alone |
| reviewer: `ntpath` simulation of both spellings | match False before the fix, True after |
| reviewer: `evidence_check --strict .`, `unverified_check --baseline`, `chain_check --baseline`, `fold_ledger --check`, `gather_changelog --check` | 357 ok · 0 drifted; exit 0; exit 0; exit 0; exit 0 |
| reviewer: the ledger hash history across three commits | row 48 re-hashed twice with no note, row 67 noted both times |
| orchestrator: the same `ntpath` reproduction, then the fix | `seal\specs\item\rounds/round-N.md` against the hook's all-backslash spelling; after the fix they match |
| orchestrator after the fixes: the two test files, the line-wrap tests, `evidence_check --strict .` | 33 passed, 13 passed, 357 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–2 | `tests/test_chain_hooks.py`'s new case, `tests/test_the_set_a_work_item_always_has.py`'s case, `hooks/review-history-guard.py`'s posting branch | the three units this run has now changed three times |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 4 — a ledger row re-hashed twice with no re-read note | issue #97, on 0.6.0, where round 2 put the axis | the repository owner |
| 🟡 6 of round 1 — five prose mentions of the old path | round 1's record and the pull request body | the repository owner, at the release |
| The guard refusing a real release with a real open row | `overview.md` §Not verified | the repository owner, at the first release that meets one |
