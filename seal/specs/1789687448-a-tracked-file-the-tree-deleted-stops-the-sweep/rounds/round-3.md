# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — review round 3

| Field | Value |
|---|---|
| Target SHA | 2c7de851 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 440 |
| Broad gate | 640489c9 against release/v0.12.1 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last round of the run, at `2c7de851`, over the fix range `ed85fc2a..2970f694`, two commits. Round 2 opened something and closed on a fix, so this record ends the run whatever it finds, and anything opened here is a deferral candidate rather than work to commission — stated at the spawn as a reason to say plainly of each whether it must be fixed before shipping, and not as a reason to pass anything.

Three things were named as worth opening. The fix pass had taken the round's own drafted split and carried it one assertion further on its own argument, removing `assert found == PATH_LIST_CALLS` rather than reordering it, on the grounds that a call count is evidence about a module the reader has just read; the round was asked to judge the argument and not only the code, because if the dict equality belonged in front of the decline then its draft was short by one, and if it did not then a half it had not asked for was removed. The pass had also built one unit beyond the split — an AST case asserting the positive halves are evaluated before the decline, because the defect lived in a sequence and no unit-level case could see it — with the grounds that this was the last pass that could build anything. And it had marked five lines of two round records `NAME NOT IN TREE` after a rename, which is the first use of that marker in this repository; the orchestrator had checked the grounds in `skills/evidence-check/SKILL.md` and confirmed the choice, leaving the placement convention to the round. One row in the fix range was the orchestrator's own and was handed over on the same terms as the rest.

## Verdicts

<!-- Orchestrator, 2026-09-18: the two deferrals arrived closed as `deferred` with no issue number, because the round that wrote them had no way to open one. #441 and #442 were opened from this report's own paste-ready forms and the numbers written into the two cells; nothing else was touched. -->

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The AST-ordering case asserts on the first body statement that mentions a name rather than on the assertion, so moving an assert away from its assignment is not seen | `tests/test_a_shrunken_corpus_declines_to_judge.py:587` | deferred #441 | Executed: red at exit 1 under the mutation it was built for; green at exit 0 under the mutation that moves only the assert, while the guarded case goes quiet on a mid-edit tree. Tightening it is mechanism, which a run past its reopening may not add · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| ⬜ 2 | The five lines introducing `NAME NOT IN TREE` use two spellings — ` · ` before it in table cells, a bare space in prose — and two prose lines put it between a colon and the fence that colon introduces | `rounds/round-2.md:31`, `rounds/round-2-report.md:33, 36, 209, 254` | deferred #442 | Read, and the refusal verified clear: `evidence-check --strict .` exit 0, `0 refused`. The rule is satisfied at all five; this is the convention the next rename will copy · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| carried | Round 2's first finding — the decline sat in front of the halves that must judge what remains | `tests/test_a_shrunken_corpus_declines_to_judge.py` | confirmed | Executed: the identical round 2 probe gives exit 1 with the planted scope named, where it gave exit 0 with the scope named nowhere. The liveness half still declines on the same tree |
| carried | Round 2's second finding — the stale `#371` pointer sat ahead of its correction | `seal/follow-up.md` | confirmed | Read. The words are at the first occurrence, and the second occurrence is left alone because the correction quotes the stale wording on purpose |
| carried | The removal of `assert found == PATH_LIST_CALLS` in favour of a third question | `tests/test_a_shrunken_corpus_declines_to_judge.py:400` | confirmed | Executed: over 3000 random readings, every reading differing from the table is caught by at least one of the three questions — 0 holes, so the three partition what the dict equality caught. The count half is evidence about a module the reader has just read, so it belonged in front of the decline and my draft was short by one |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer`, whose spawn is what follows this record |

## Paste-ready fixes

```python
def test_the_positive_halves_are_asked_before_the_decline():
    """The ORDER is the fix, and no unit-level case can see it.

    `vanished_scopes` skips the rest of the function when it declines, so what
    keeps the two positive halves judging is that their ASSERTIONS sit in
    front of it. Round 2 🟡 1 was that ordering the other way round.

    Indexed on the `assert` statements rather than on the first mention of
    each name: an assignment carries the name first, so a case reading
    mentions passes while the assertion it is about has moved behind the
    decline -- measured in round 3, green under exactly that mutation.
    """
    body = _function(_tree_of(SELF), GUARDED_CASE).body
    decline = next(
        (i for i, node in enumerate(body) if "vanished_scopes" in ast.dump(node)),
        None,
    )
    assert decline is not None, (
        f"{GUARDED_CASE} no longer calls `vanished_scopes`, so this case is "
        "measuring an order that no longer exists"
    )
    asserted = {
        name: i
        for i, node in enumerate(body)
        if isinstance(node, ast.Assert)
        for name in ("unaccounted", "miscounted")
        if name in ast.dump(node.test)
    }
    for name in ("unaccounted", "miscounted"):
        at = asserted.get(name)
        assert at is not None, f"{GUARDED_CASE} no longer asserts on `{name}`"
        assert at < decline, (
            f"`{name}` is ASSERTED after `vanished_scopes`, so a tree that is "
            "merely mid-edit turns that half of this case off. It is evidence "
            "about a module the reader has just read, and a skip explains "
            "nothing about it — round 2 🟡 1"
        )
```
```
(`classified_scopes`), consumed at `:380` · NAME NOT IN TREE
```
```
`classified_scopes` computes `found`, then declines before returning · NAME NOT IN TREE:
```
```
`classified_scopes` with · NAME NOT IN TREE:
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local`, checked out at `2c7de851` | clean tree, tip confirmed `2c7de85` |
| `bin/test -q` over the eight modules this work item touches | exit 0, `181 passed` |
| round 2's own probe: an unguarded scope planted in a tracked test module, one other test module off disk with the removal unstaged | exit 1, `2 failed, 14 passed, 1 skipped`, the planted scope named |
| the same probe on a clean tree, after restoring both files | exit 0, `17 passed`, nothing named |
| mutation: the decline moved back in front of everything | the AST-ordering case **red**, exit 1 |
| mutation: only `assert not unaccounted` moved after the decline, its assignment left in front | the AST-ordering case **green**, exit 0 — and the guarded case skips instead of naming the scope |
| 3000 random readings compared against `PATH_LIST_CALLS`, asking whether any differs from it and is caught by none of the three questions | 0 — the three partition the old dict equality |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0, records arm `367 names read · 0 refused · 0 drifted`, so all five markers hold |
| `python3 skills/code-review/scripts/survivor_check.py --range 5bf22ddb..HEAD` | exit 1, the payload-meter file named |
| the same with `--exempt …/survivors.md` | exit 0, one `exempt` line printed |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; it is the sealer's one act, and it comes due now |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_shrunken_corpus_declines_to_judge.py:296`, consumed at `:345` and `:391` | round 1's 🔴 1 — fixed |
| round-1 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md:8` | round 1's 🔴 2 — fixed |
| round-1 | `tests/test_no_document_names_the_old_roots.py:139` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md:238` | round 1's 🟡 4 — fixed |
| round-1 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` §*Not done* | round 1's ⬜ 5 — fixed |
| round-1 | `docs/release-checklist.md` step 3 preamble | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_release_hygiene.py:477` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/conftest.py`, and the six helpers | round 1's ⬜ 8 — fixed |
| round-1 | `seal/ledger.md` | round 1's ⬜ — verified |
| round-1 | repository-wide | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_a_shrunken_corpus_declines_to_judge.py:311`, consumed at `:380` | round 2's 🟡 1 — fixed |
| round-2 | `seal/follow-up.md`, the survivor-exemption row, `e29a0e51` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/test_a_shrunken_corpus_declines_to_judge.py` | round 2's carried — confirmed |
| round-2 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md` | round 2's carried — confirmed |
| round-2 | `tests/test_no_document_names_the_old_roots.py` | round 2's carried — confirmed |
| round-2 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md` | round 2's carried — confirmed |
| round-2 | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` | round 2's carried — confirmed |
| round-2 | `tests/test_release_hygiene.py` | round 2's carried — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Tighten the AST-ordering case to index the `ast.Assert` statements rather than the first mention of a name | this round, ⬜ 1 — a `deferred #N` candidate with no issue yet; the suggested form is below | the repository owner |
| Settle one spelling for `NAME NOT IN TREE` and apply it to the five lines that introduce it | this round, ⬜ 2 — a `deferred #N` candidate with no issue yet | the repository owner |
| The corpus half and the range half of the survivor-exemption silence | already deferred in round 1, to `deferred #308`; `seal/follow-up.md`'s survivor-exemption row carries the live measurement and now flags its own stale pointer | the repository owner |
| Whether #371's closure was meant to cover the range half | already deferred in round 2, to `seal/follow-up.md`, the same row | the repository owner |
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | already deferred in round 1, to `overview.md` §*Not done*, which still names no durable home | the repository owner |
| Q1 — whether a path missing from disk should have its index content swept | already deferred in round 1, to `questions.md` Q1 | the repository owner |
