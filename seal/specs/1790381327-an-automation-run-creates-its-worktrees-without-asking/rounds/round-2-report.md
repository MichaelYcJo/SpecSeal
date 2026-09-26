# Round 2 report — an automation run creates its worktrees without asking (#604, #8)

- Target SHA: `fb9c1770` · Fix range verified: `cc48effe..c6ee7a3c` (`7edc628b`, `2eb566c1`, `c6ee7a3c`); `fb9c1770` only closes round 1's record
- Ran by: specseal:warden on claude-opus-5-5
- A verifying round. The target is round 1's fix diff, not the branch. Every round-1 verdict gets an answer below, and the fix commit's new units are judged as code.
- Worked in a `git clone --no-local` at the target SHA under the session scratchpad. Nothing was written in the user's checkout except this file.
- The fix account was read in full and treated as claims: the commit messages, `overview.md`'s two new divergences, `survivors.md`'s new row, ledger row A1's correction note, and the round-1 fix table. Ledger A1 says *the three new cases and the dispatch case were seen red against the unfixed reader, and each repair was then undone alone and turned its own case red*. I re-ran that myself (probe M1–M6 and PRE below), and it holds.

## Summary

All four round-1 yellows are closed. They are closed for the example round 1 named and for the class the prompt asked about. Each repair is pinned by a case I saw go red when that repair alone was undone. The two ⬜ corrections and the ❓ answer hold as well.

Three ⬜ notes follow. None of them changes a verdict the guard prints.

1. The sidechain refusal accepts every `isSidechain` value except the literal `true`. That goes against the module's own rule for a shape nobody measured.
2. The switch direction has an older sibling of round 1's finding 4: *Single-stream tree* is printed where nothing was counted. It dates from the initial commit and sits outside this branch.
3. The repaired `[worktree-ok]` sentence still says *no other Claude session is working* when only idle sessions are present. The idle list includes a lease whose owner cannot be identified.

## Round 1's findings, one by one

### Finding 1 — a typed answer read as the preset: closed

`hooks/worktree_consent.py:215-228`. `_routing_preset` now keeps the raw labels and reads the answer only if it `is in labels`. The fix therefore closes the class by construction, and not just the three phrasings round 1 listed:

- Only a string that equals an option label byte for byte gets past the membership test.
- Exactly one label can have the leading phrase `automation`, because the three leading phrases have to equal `ROUTING_LABELS` exactly. A fourth label, or a duplicate, fails that sort comparison first.
- A person who types the exact label into `Other` writes the same bytes a press writes, and the words mean the same thing. Any other typed text fails closed, including a case variant, a trailing space, a bare `automation` next to a decorated label, or any qualifier.

Pinned by `test_a_typed_answer_that_qualifies_the_preset_is_not_consent`. It goes red with the membership test removed (M1) and red against the hooks at `cc48effe` (PRE). The updated `test_the_routing_preset_is_consent` now supplies options that match the answer, which is the only shape a press can produce.

### Finding 2 — the consent read raising, and the deny dropped: closed

`hooks/worktree_consent.py:316` (a string `tool_use_id`), `:328` (`ValueError` caught beside `OSError`), `:348-351` (the catch-all in `consent`).

The class is every malformed field type in every field the reader indexes. I checked it by executing, not by reading. I called `automation_answered` directly, below the catch-all, on 25 indexed fields. Each field was replaced by a dict, a list, an int, a float, a bool, `None`, a string with a NUL, and a 200-digit int. I added six whole-line shapes, including a 5000-deep nest, and 49 pairs of odd `session` and `transcript_path` values, each run through both `automation_answered` and `consent`. None of the 255 shapes raised. `granted`, which sits outside the try, is covered by the argument pairs: `consent_path` coerces with `str()`, and `os.path.isfile` swallows the NUL.

**Does the catch-all hide a real bug from a test? No.** Of the 27 cases that build a transcript, 18 call `automation_answered` directly. None of them passes through the catch-all, so a raise there turns the case red. The other nine go through the guard:

- Six expect `allow` or silence. A raise would become *no consent* and the verdict would change, so the case goes red.
- `test_the_answer_does_not_reach_the_switch_direction` exercises a path that never calls `consent`.
- `test_an_unreadable_transcript_leaves_the_old_verdict` has a direct twin, `test_an_unreadable_transcript_is_no_consent`, which calls the reader directly.
- `test_a_shape_the_reader_did_not_expect_keeps_the_guards_deny` exists to go through `dispatch.py`.

The three layers are pinned separately, so no layer can hide the undoing of another:

- `test_the_reader_itself_answers_both_shapes_without_raising` goes red with the string check removed (M3) and red with the `ValueError` catch removed (M4), with the catch-all left in place both times.
- `test_consent_fails_closed_on_any_exception` goes red with the catch-all removed (M5).
- The dispatch case goes red against `cc48effe` (PRE), which is the round-1 P8 failure (`deny` became no decision) reproduced as a test.

### Finding 3 — the README guard row: closed

`README.md:188`, `README.ko.md:184`. Both rows now say that a Bash `git worktree add` is what the single-stream deny and the choice rows judge. They say an Agent call with `isolation: "worktree"` counts no sessions and asks once. They also name both consent sources: a creation that already ran, and a press of `automation`. The English and Korean rows say the same things. I read every claim against the code: `guard_worktree_creation` runs its ladder only for Bash, and `main`'s Agent block asks without consent and stays silent with it.

I swept the class with `git grep -i isolation` over `README*`, `CONTRIBUTING.md`, `CLAUDE.md`, `docs`, `skills`, `agents`, `templates` and `hooks`. Round 1 searched for the other phrasings; I carried that search and did not repeat it. The results:

- `README.md:289` and `README.ko.md:280` (*asks outright instead*) are still true.
- The `implementer-mark.py` docstring (*retrying without `isolation`*) describes what a session might do, and it names no guard verdict.
- The `dispatch.py` comment is about crash isolation.

No other sentence says when the guard asks for an Agent or names a consent source.

### Finding 4 — the `[worktree-ok]` sentence in the unusable state: closed for that state

`hooks/worktree-guard.py:1747-1756`. The sentence that claims a count is now printed only `if reliable`. `test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken` pins it in both languages, and it goes red when the condition is forced true (M6) and red against `cc48effe` (PRE).

For the class inside the creation ladder, I followed the flow in the code. The closing deny, *No other session is working in this tree (= single-stream)*, is reached only with `active`, `idle` and `not reliable` all false. That is because `choose` always ends in `respond`, and `respond` exits. The ACTIVE row names sessions it counted, and the idle row names idle sessions it counted. So in this ladder, the unusable state no longer reaches any sentence that claims a count. Two siblings outside that narrow reading are ⬜ 2 and ⬜ 3 below.

### ⬜ 5, ⬜ 6 and the ❓: closed

- ⬜ 5: `automation_answered`'s docstring now says which lines are parsed, and it cites round 1's measurement as a measurement.
- ⬜ 6: ledger row A1 is corrected in place, with a `Corrected 2026-09-26` note. Its clause now states the four conditions the code requires: a string id, not a sidechain entry, an exact label, and `consent` answering "" on any exception. `evidence-check --strict` reads all 27 rows of the fragment OK, and the 137 and 34 rows of `seal/releases/0.9.1.md` and `seal/releases/0.9.4.md` too.
- ❓ (the orchestrator's answer: refuse `isSidechain: true`): implemented at `:311`, and pinned by `test_a_sidechain_entry_is_not_consent`, which goes red with the refusal removed (M2). `docs/worktree-guard-spec.md` condition 2 and `overview.md` both record it. ⬜ 1 is about its boundary.

## New units (from round 1's `New units` row), judged as code

All seven are test code. `dispatch_pre_bash` is a helper, and the other six are cases. Every case was seen red, against `cc48effe` and when its own repair alone was undone (table below). None of them reads the real `~/.claude/projects`:

- The in-process cases use the `projects` fixture or the autouse `_NO_TRANSCRIPTS` patch in `tests/conftest.py`.
- The subprocess dispatch case passes a `transcript_path` whose basename matches, so `transcript_for` never globs.

The dispatch case asserts only `deny`. That holds whether the subprocess's session detection works (the single-stream deny) or not (the first `choose` deny), and each call uses a fresh session id, so the case does not depend on the environment. `ruff check` and `ruff format --check` pass on all four changed Python files.

## Findings from execution

### ⬜ 1 — the sidechain refusal accepts every value except the literal `true`

`hooks/worktree_consent.py:311`: `if entry.get("isSidechain") is True: continue`. In the shape probe, the only mutations that were still read as consent were the seven non-`True` values of `isSidechain`: a dict, a list, an int, a float, `None`, a NUL string, and a huge int. An absent field is read as consent too.

The same module refuses an unmeasured shape everywhere else. Its own docstring requires `multiSelect` to be `False` *rather than merely absent: an absent field is a shape nobody measured*. The census supports the stricter reading at no cost. In 67 local main transcripts, all 136 linked `AskUserQuestion` results carry `isSidechain: false`, and so do all 11016 user entries the reader's prefilter admits. The suite already writes `"isSidechain": False` in `ask_entries`. With `is not False`, `tests/test_the_guard_asks_once_per_session.py` and `tests/test_worktree_guard.py` pass 151 of 151.

Why ⬜: the harness writes a bool, and the model cannot write a transcript entry, so no shape a real session produces reaches this path. The release ships no defect if this stands. The change would make the one rule the orchestrator decided refuse unmeasured shapes, the way the module's other rules do.

### ⬜ 2 — the switch direction says *Single-stream tree* where nothing was counted

`hooks/worktree-guard.py:2304` (English) and `:2308` (Korean), in row 3 of the switch ladder. Executed: `git switch other  # [shared-tree-ok]` on a dirty tree with `sessions_in_tree` returning `([], [], False)` gets `ask` with *Single-stream tree, so the switch is allowed*. `[shared-tree-ok]` skips rows 1-b and 2, so this is the same unusable state round 1's finding 4 named, in the other direction.

`git log -S` dates the sentence to the initial commit. It is outside this branch's diff and outside the fix diff. It is also closer to an echo of the person's own answer: the token says they chose to switch in the shared tree. So the release changes nothing here. It belongs to the class, and so I name it: a candidate for a new issue, with the owner deciding whether it is worth a sentence. It needs no fix on this branch.

### ⬜ 3 — the repaired `[worktree-ok]` sentence overstates what the idle state measured

`hooks/worktree-guard.py:1749-1756`. Executed: `[worktree-ok]` with `sessions_in_tree` returning one idle session and `reliable=True` gets `ask` with *No other Claude session is working in this tree*. Round 1 saw the same output and named only the unusable state, and the fix's comment (*the count is named only where one was taken*) is true: a count was taken.

What the count measured is weaker than the sentence, though. The switch direction's own idle row describes the idle list as sessions that *cannot be shown to be working*, which includes *a lease whose owning session cannot be identified*. A session holding such a lease can be working. Rewording the sentence to what was measured makes it true in both reliable states. Why ⬜: the verdict is `ask` either way. A person who believes the sentence and declines ends up in the switch direction, which judges the same idle list on its own terms.

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
| ⬜ 1 | the sidechain refusal accepts an absent or non-bool `isSidechain`, against the module's own rule for unmeasured shapes | `hooks/worktree_consent.py:311` | open | executed: 7 non-`True` values read as consent; census 136 of 136 linked results and 11016 of 11016 user entries carry `false`; `is not False` passes 151 of 151 in two modules. No real shape reaches it |
| ⬜ 2 | the switch direction's row 3 says *Single-stream tree* in the detection-unusable state under `[shared-tree-ok]` | `hooks/worktree-guard.py:2304` | open | executed: `ask` with that sentence at `reliable=False`; dates from the initial commit, outside this branch; a candidate for a new issue that the owner answers |
| ⬜ 3 | the repaired `[worktree-ok]` sentence says *no other Claude session is working* when idle sessions, which include unattributed leases, are present | `hooks/worktree-guard.py:1751` | open | executed: idle-only with `reliable=True` gets `ask` with that sentence; the idle list is what *cannot be shown to be working* |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A switch written after a creation in one command is never judged when consent is present | already deferred in round 1: #620, filed before round 1 (spec Q3) | the owner, in the milestone that takes #620 |

## Paste-ready fixes

None of the three is 🔴 or 🟡, so none is required. They are here so a smith who takes one has nothing to rebuild.

### ⬜ 1 — `hooks/worktree_consent.py`, the sidechain refusal

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

### ⬜ 3 — `hooks/worktree-guard.py`, the `[worktree-ok]` row

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

With ⬜ 3 taken, the two string assertions in `tests/test_worktree_guard.py` (`test_the_two_reworded_reasons_are_pinned_in_both_languages` and the new count case) move to the new wording.

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round, at `fb9c1770` unless noted:

- `seal/specs/1790381327-an-automation-run-creates-its-worktrees-without-asking/rounds/round-1.md` and `round-1-report.md` (whole); `changelog.md`, `overview.md`, `survivors.md` (fix-range diffs)
- `hooks/worktree_consent.py` (whole); `hooks/worktree-guard.py` (fix-range diff, lines 1690-1860 and 2095-2325, `choose`, `respond`, and the `sessions_in_tree` returns); `hooks/dispatch.py` (lines 85-102, and its raise policy); `hooks/implementer-mark.py` (lines 15-35)
- `README.md`, `README.ko.md`, `docs/worktree-guard-spec.md` (fix-range diffs)
- `tests/test_the_guard_asks_once_per_session.py` (fix-range diff, `ask_entries`, `write_transcript`, `projects`, `grant`, `decide`); `tests/test_worktree_guard.py` (fix-range diff); `tests/conftest.py` (the `PROJECTS_ROOT` patch and `decision_of`)
- `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md` (row A1); `seal/releases/0.9.1.md` and `seal/releases/0.9.4.md` (word diff of the fix range)
- `ruff.toml`, `.github/workflows/test.yml` (lint lines), `bin/test` (head)
