# 1790381327-an-automation-run-creates-its-worktrees-without-asking — review round 2

| Field | Value |
|---|---|
| Target SHA | fb9c17700c607ebbccef4b97e46e3bac54de8580 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 622 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790381327 is the verifying round. It opens round 1's fixes, `cc48effe..c6ee7a3c`, at fb9c1770. The classes are each round-1 finding beyond its named example: every typed answer that is not an option label, every field type the reader indexes, every place stating when the guard asks for an Agent or naming consent, and every message claiming a count it did not take. Plus the seven test units the fix pass added.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — a typed `Other` answer is no longer read as the preset, for the whole class: only an exact option label passes, and exactly one label can carry the phrase `automation` | `hooks/worktree_consent.py:226` | confirmed | executed: M1 and PRE turn `test_a_typed_answer_that_qualifies_the_preset_is_not_consent` red; read: the membership test plus the three-phrase equality |
| 🟢 | round 1's finding 2 is closed — the reader raises on no JSON shape, and the guard keeps its deny through `dispatch.py` | `hooks/worktree_consent.py:348` | confirmed | executed: 0 of 255 shapes raised when the reader was called directly; M3, M4 and M5 each turn exactly their own case red; PRE turns the dispatch case red. The catch-all hides no reader bug from the suite (18 direct cases, and every guard-only negative has a direct twin) |
| 🟢 | round 1's finding 3 is closed — both README rows describe the Bash and Agent paths and name both consent sources | `README.md:188` | confirmed | read against `guard_worktree_creation` and `main`'s Agent block; `git grep -i isolation` sweep found no other stale sentence; `README.ko.md:184` matches |
| 🟢 | round 1's finding 4 is closed — the count sentence is not printed in the detection-unusable state | `hooks/worktree-guard.py:1754` | confirmed | executed: M6 and PRE turn the new case red in both languages; read: the closing deny is reached only with every count taken and empty |
| 🟢 | round 1's note 5 is closed — the docstring says which lines are parsed | `hooks/worktree_consent.py:267` | confirmed | read at the target SHA |
| 🟢 | round 1's note 6 is closed — ledger A1 is corrected in place and matches the code | `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md` | confirmed | read against the code; `evidence-check --strict` 27 ok, 0 drifted; 0.9.1 137 ok and 0.9.4 34 ok |
| 🟢 | round 1's question is answered — a sidechain entry is refused | `hooks/worktree_consent.py:311` | confirmed | executed: M2 turns `test_a_sidechain_entry_is_not_consent` red; the orchestrator's answer, recorded in `overview.md` and the doc's condition 2 |
| 🟢 | the fix's seven new test units are correct and each case was seen red | `tests/test_the_guard_asks_once_per_session.py:1391` | confirmed | executed: PRE plus M1–M6; no case reads the real projects root; the dispatch case does not depend on the environment |
| ⬜ 1 | the sidechain refusal accepts an absent or non-bool `isSidechain`, against the module's own rule for unmeasured shapes | `hooks/worktree_consent.py:311` | deferred #624 | executed: 7 non-`True` values read as consent; census 136 of 136 linked results and 11016 of 11016 user entries carry `false`; `is not False` passes 151 of 151 in two modules. No real shape reaches it |
| ⬜ 2 | the switch direction's row 3 says *Single-stream tree* in the detection-unusable state under `[shared-tree-ok]` | `hooks/worktree-guard.py:2304` | deferred #624 | executed: `ask` with that sentence at `reliable=False`; dates from the initial commit, outside this branch; a candidate for a new issue that the owner answers |
| ⬜ 3 | the repaired `[worktree-ok]` sentence says *no other Claude session is working* when idle sessions, which include unattributed leases, are present | `hooks/worktree-guard.py:1751` | deferred #624 | executed: idle-only with `reliable=True` gets `ask` with that sentence; the idle list is what *cannot be shown to be working* |

## Paste-ready fixes

```python
                # A subagent has no `AskUserQuestion`, and every main-transcript
                # user entry on disk carries `isSidechain: false`. Anything else
                # -- true, absent, or not a bool -- is a shape nobody measured,
                # refused the way `_routing_preset` refuses an absent
                # `multiSelect`.
                if entry.get("isSidechain") is not False:
                    continue
```
```python
def test_a_sidechain_entry_is_not_consent(projects, repo):
    """A subagent has no `AskUserQuestion`, so no real click can carry
    `isSidechain: true`; every main-transcript entry on disk carries `false`,
    so an absent or non-bool value is refused as an unmeasured shape."""
    for value in (True, "true", 1, None, "absent"):
        use, result = ask_entries(repo)
        if value == "absent":
            del result["isSidechain"]
        else:
            result["isSidechain"] = value
        write_transcript(projects, "me", [use, result])
        assert not wc.automation_answered(str(repo), "me"), value
```
```python
                + (
                    tr(
                        "No other Claude session can be shown to be working in "
                        "this tree, but ",
                        "이 트리에서 작업 중임이 확인되는 다른 Claude 세션은 없지만 ",
                    )
                    if reliable
                    else ""
                )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_guard_asks_once_per_session.py tests/test_worktree_guard.py tests/test_worktree_guard_signals.py -q` (the modules the fix touched, plus the one the Agent path shares) | 170 passed, 1 skipped |
| `ruff check` and `ruff format --check` on `hooks/worktree_consent.py`, `hooks/worktree-guard.py` and the two changed test files | all checks passed; 4 files already formatted |
| M1 — the label-membership test removed | only `test_a_typed_answer_that_qualifies_the_preset_is_not_consent` red |
| M2 — the sidechain refusal removed | only `test_a_sidechain_entry_is_not_consent` red |
| M3 — the string check on `tool_use_id` removed, catch-all kept | only `test_the_reader_itself_answers_both_shapes_without_raising` red |
| M4 — `ValueError` dropped from the reader's except, catch-all kept | only `test_the_reader_itself_answers_both_shapes_without_raising` red |
| M5 — the catch-all in `consent` removed, narrow repairs kept | only `test_consent_fails_closed_on_any_exception` red |
| M6 — the count sentence printed regardless of `reliable` | only `test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken` red |
| PRE — hooks at `cc48effe`, tests at the target | all six new cases red; `test_the_routing_preset_is_consent` and the reworded-reasons case pass |
| Shape probe — 25 indexed fields × 8 values, 6 whole-line shapes, 49 argument pairs through both `automation_answered` and `consent`, all called directly | 255 shapes, 0 raised; 7 read as consent, all of them non-`True` `isSidechain` (⬜ 1) |
| `isSidechain` census over 67 local main transcripts (aggregates only) | 136 linked results, all `false`; 11016 prefiltered user entries, all `false` |
| `is not False` in place of `is True`, run against two modules | 151 passed |
| Switch probe — `git switch other  # [shared-tree-ok]`, dirty tree, `reliable=False` and then `reliable=True` | `ask`, and both reasons say *Single-stream tree* (⬜ 2) |
| Idle probe — `[worktree-ok]` creation, one idle session, `reliable=True` | `ask`, and the reason says *No other Claude session is working* (⬜ 3) |
| `evidence-check --strict --ledger` on the work item's fragment, `seal/releases/0.9.1.md` and `seal/releases/0.9.4.md` | 27, 137 and 34 ok; 0 drifted, 0 broken |
| Test census — which transcript cases call the reader directly | 18 direct; 9 only through the guard, each either positive, off the consent path, or with a direct twin |
| Full suite, repository-wide lint and typecheck (the broad gate) | not yet — the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree_consent.py:220` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/worktree_consent.py:299` | round 1's 🟡 2 — fixed |
| round-1 | `README.md:188` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1757` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree_consent.py:261` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md` | round 1's ⬜ 6 — answered |
| round-1 | `hooks/worktree_consent.py:238` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree_consent.py:267` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:1648` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:1972` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.1.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree_consent.py:297` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A switch written after a creation in one command is never judged when consent is present | already deferred in round 1: #620, filed before round 1 (spec Q3) | the owner, in the milestone that takes #620 |
