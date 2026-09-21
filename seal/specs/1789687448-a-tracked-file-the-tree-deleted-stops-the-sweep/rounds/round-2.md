# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — review round 2

| Field | Value |
|---|---|
| Target SHA | e29a0e51 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 440 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `ed85fc2a234f1d9f755fc7bc131e3394862cd9af..2970f694f64a33f14a11a4ed311e237f0fa83e6c`, 2 commits |
| Contract changes | none |
| New units | vanished_scopes (depth 1); miscounted_scopes (depth 1); test_an_unguarded_scope_is_named_although_a_module_is_mid_edit (depth 1); SELF (depth 1); GUARDED_CASE (depth 1); test_the_positive_halves_are_asked_before_the_decline (depth 1) |
| Needs a fix | yes — 🟡 1, the decline sits in front of the offender half, so a mid-edit tree hides a newly planted unguarded scope and the gate exits 0 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of round 1's eight findings, at `e29a0e51`, over the fix range `e7d4ff8c..1956474a`, four commits. `close` had ticked `Pass` beside `nobody`, so the round was told what brought it here and that a round opening nothing needing a fix ends the run. Two commits above the range were named as the orchestrator's rather than the fix pass's: the record's own close, and a correction to `seal/follow-up.md`.

Four places a closure most easily goes wrong were named at the spawn. The half of 🔴 1's repair that keeps a real removal from being carried away by a neighbour being mid-edit, because that is the difference between declining and going quiet. 🟡 3, the same shape one module over, where the round's own finding had been that a decline over one path carried another finding away. 🟡 4, where the frame paragraph is gone and one word of the reviewer's drafted replacement was changed on stated grounds. And ⬜ 8, closed by sharing one spelling of a block while deliberately leaving the listing words at each call site, with the reason that the class reader finds a deriving scope by the string constants the call names.

The orchestrator had executed the restored `survivor-check` contract at both readings and the state of the two ticket pointers, and had re-run none of the fix pass's own figures. One item in the diff was the orchestrator's own work and was handed to the round as reviewable on the same terms as the rest.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The decline sits inside `classified_scopes`, in front of both halves of the case, so on a mid-edit tree a newly planted unguarded scope is not named and the run exits 0 — the offender half is a positive sweep and must judge what remains | `tests/test_a_shrunken_corpus_declines_to_judge.py:311`, consumed at `:380` | **fixed** `a04d2818` | fixed at a04d2818; Executed: plant alone, exit 1 and the scope named; plant plus one tracked test module off disk, exit 0, `13 passed, 2 skipped`, the scope named nowhere. `spec.md` §*Is a skip a weakening* — *the positive sweeps do not skip themselves* · NAME NOT IN TREE |
| ⬜ 2 | The corrected pointer for #371 sits at the end of a very long cell while the stale *tracked as #371* stays mid-cell, so a reader meets the wrong pointer first | `seal/follow-up.md`, the survivor-exemption row, `e29a0e51` | **fixed** `2970f694` | fixed at 2970f694 — The orchestrator's row rather than the fix pass's: the sentence calling #371 the tracker home now says it is closed and points at the correction, so a reader meets the fact where the claim is rather than fifteen hundred characters later. The owner's judgment about what that closure covered is still untaken; Read. The append itself is accurate, correctly placed and correctly stops short of the owner's judgment; this is only where the correction sits |
| carried | Round 1's first finding — the class reader did not decline on a shrunken corpus | `tests/test_a_shrunken_corpus_declines_to_judge.py` | confirmed | Executed: the identical round 1 reproduction now gives exit 0, `13 passed, 2 skipped` where it gave exit 1, `2 failed`. Mutating `if gone <= set(missing)` to `if True` turns the new case red and restoring it turns it green |
| carried | Round 1's second finding — the survivors record silenced the check that reported it | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md` | confirmed | Executed over `5bf22ddb..HEAD` at the tip: exit 1 with no exemption and the file named; exit 0 with the exemption and one `exempt` line printed. The new anchor is standing text the check prints and is not a phrase it matched |
| carried | Round 1's third finding — the coverage decline carried a real finding away | `tests/test_no_document_names_the_old_roots.py` | confirmed | Executed: mutating `if absent and not unexplained:` to `if absent:` turns `test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit` red at exit 1; restored, green |
| carried | Round 1's fourth finding — the build's verdict sat in the frame | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md` | confirmed | Read. The paragraph is gone; what stands states why the refresh is forced and points at `overview.md` and `phases/phase-5.md`. The one reworded clause is more accurate than my draft, and the note is still coordinate-only |
| carried | Round 1's fifth finding — the overview described the survivor report as it stood before the fix | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` | confirmed | Read against my own round 1 measurements, and its claim about `2c83b2bb` executed separately with that commit's own exemption file: exit 1 without the flag, exit 0 with one `exempt` line |
| carried | Round 1's sixth finding — the checklist preamble was wrong about a mid-edit `tests/` tree | `docs/release-checklist.md` step 3 preamble | confirmed | Read, and true only because the first finding was fixed: a mid-edit `tests/` now produces the skipped case the sentence describes |
| carried | Round 1's seventh finding — the running version came from `ROOT` and was read twice | `tests/test_release_hygiene.py` | confirmed | Executed: mutating `version(root)` back to `version()` turns `test_the_running_version_comes_from_the_root_being_swept` red at exit 1; restored, green. The caller now reads `plugin.json` once |
| carried | Round 1's eighth finding — the git-listing block was copied six times | `tests/conftest.py`, and the six helpers | confirmed | Read, and the argument for keeping the listing words at each call site checked against `_path_list_words` rather than accepted: swallowing the subcommand would take all seven scopes out of the class the reader enumerates |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer` |

## Paste-ready fixes

```python
def vanished_scopes(found, missing):
    """The classified scopes the reader no longer finds, or `pytest.skip` when
    every one of them is in a module the working tree deleted.

    **Only this half declines.** The offender half -- a scope the reader DID
    find that no table accounts for -- is a positive sweep over modules that
    are on disk, so it needs no whole corpus and judges what remains, which is
    what `spec.md` §*Is a skip a weakening* asks of a positive sweep. Round 2
    measured the alternative: with the decline in front of both halves, a
    planted unguarded scope went unnamed on a tree with one test module
    mid-edit and the case exited 0 -- the gate going quiet on exactly the
    seventh helper it exists to catch.

    Conditional on EVERY vanished scope being explained, so a genuine removal
    is still reported beside a skipped one.
    """
    vanished = sorted(set(PATH_LIST_CALLS) - set(found))
    if vanished:
        gone = {key.split("#", 1)[0] for key in vanished}
        if gone <= set(missing):
            decline_if_shrunken(sorted(gone), DECLINES_CLASS)
    return vanished
```
```python
def test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard():
    present, missing = suite_modules()
    found = derivers(present)

    # The offender half first. A scope the reader FOUND is in a module that is
    # on disk, so this judges what remains rather than declining over it.
    unaccounted = sorted(set(found) - set(PATH_LIST_CALLS))
    assert not unaccounted, (
        f"the suite derives a path list from git in {unaccounted} that this "
        "case does not account for. Classify it: it either applies "
        f"`{SHARED_GUARD}`, or it belongs in one of the five tables above "
        "with the grounds a reader can weigh"
    )

    vanished = vanished_scopes(found, missing)
    assert not vanished, (
        f"this case accounts for {vanished}, which no longer derives a path "
        "list although its module is on disk. Classify the difference: it "
        f"either applies `{SHARED_GUARD}`, or it belongs in one of the five "
        "tables above with the grounds a reader can weigh"
    )

    assert found == PATH_LIST_CALLS, (
        f"the suite derives path lists at {found} and this case accounts for "
        f"{PATH_LIST_CALLS}. The unit is the CALL SITE: a second list inside a "
        "scope that already holds one is classified nowhere, and the grounds "
        "recorded above are about the call this case counted"
    )
```
```python
def test_the_reader_finds_the_helpers_this_work_guarded():
    present, missing = suite_modules()
    found = derivers(present)
    # Declines when the tree explains the gap; judges otherwise.
    vanished_scopes(found, missing)
```
```python
    present, missing = suite_modules()
    thinned = derivers([p for p in present if p != rel])
    with pytest.raises(pytest.skip.Exception) as declined:
        vanished_scopes(thinned, [rel, *missing])
```
```python
    try:
        partial = vanished_scopes(thinned, [])
    except pytest.skip.Exception as declined:
        raise AssertionError(
            "a scope that vanished with its module still on disk was declined "
            f"rather than reported: {declined}"
        ) from None
    assert key in partial, partial
```
```python
def test_an_unguarded_scope_is_named_although_a_module_is_mid_edit():
    """The offender half is a positive sweep and does not decline.

    Measured in round 2 against the shape this replaces: with the decline in
    front of both halves, a planted unguarded scope went unnamed on a tree
    with one test module deleted from disk and the case exited 0.
    """
    key = sorted(APPLIES_THE_SHARED_GUARD)[0]
    rel = key.split("#", 1)[0]
    present, missing = suite_modules()
    found = dict(derivers([p for p in present if p != rel]))
    planted = "tests/test_tmp_seventh.py#sweep"
    found[planted] = 1

    # The offender is named although the same inputs would make the liveness
    # half decline, which is the whole of the split.
    assert sorted(set(found) - set(PATH_LIST_CALLS)) == [planted]
    with pytest.raises(pytest.skip.Exception):
        vanished_scopes(found, [rel, *missing])
```
```
so this row stays open and is tracked as #371 (closed; see the correction at
the end of this row)
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local`, checked out at `e29a0e51` | clean tree, tip confirmed `e29a0e5` |
| `bin/test -q` over the eight modules the fix range touches | exit 0, `179 passed` |
| `bin/test -q` over `tests/test_a_rider_reaches_its_file.py` and every module that reads `seal/follow-up.md` | exit 0, `726 passed, 1 skipped` |
| the round 1 reproduction: `tests/test_release_hygiene.py` off disk, removal unstaged, class reader run, then restored | exit 0, `13 passed, 2 skipped` — it was exit 1, `2 failed, 12 passed` in round 1 |
| mutation: `if gone <= set(missing):` to `if True:`, then restored | green `1 passed` → **red exit 1** → restored green |
| mutation: `if absent and not unexplained:` to `if absent:`, then restored | green `1 passed` → **red exit 1** → restored green |
| mutation: `version(root)` to `version()`, then restored | green `1 passed` → **red exit 1** → restored green |
| an unguarded scope planted in a tracked test module, whole tree on disk | exit 1, `1 failed`, the planted scope named |
| the same plant with one tracked test module off disk, removal unstaged | exit 0, `13 passed, 2 skipped`, the planted scope named nowhere |
| `python3 skills/code-review/scripts/survivor_check.py --range 5bf22ddb..HEAD` | exit 1, the payload-meter file named with both shared phrases |
| the same with `--exempt …/survivors.md` | exit 0, one `exempt` line printed |
| `--range 5bf22ddb..2c83b2bb`, with and without that commit's own exemption file | exit 1, then exit 0 with one `exempt` line — the overview's claim holds |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0, `1353 ok · 0 drifted · 0 broken`, records arm `3 stamps read · 0 drifted` |
| `git ls-files` filtered to paths containing a space | none, so `git_listing`'s whitespace split misclassifies nothing in this tree |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; it is the sealer's one act |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The corpus half and the range half of the survivor-exemption silence | already deferred in round 1, to `deferred #308`; `seal/follow-up.md`'s survivor-exemption row now carries the live measurement and names #308 as the open home | the repository owner |
| Whether #371's closure was meant to cover the range half | `seal/follow-up.md`, the same row, `e29a0e51` | the repository owner |
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | already deferred in round 1, to `overview.md` §*Not done*, which still names no durable home | the repository owner |
| Q1 — whether a path missing from disk should have its index content swept | already deferred in round 1, to `questions.md` Q1 | the repository owner |
