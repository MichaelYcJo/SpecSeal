# Round 2 — the verifying round

| Field | Value |
|---|---|
| Target SHA | `e29a0e51` |
| Fix range verified | `e7d4ff8c..1956474a`, four commits |
| Also reviewed | `871b02f6` and `e29a0e51`, the orchestrator's own two commits above the fix range |
| Base | `release/v0.12.1` at `5bf22ddb` |
| Reviewed in | a `git clone --no-local` at the target SHA |

## What this round found

All eight of round 1's findings are genuinely closed, and I re-derived each of
them rather than reading the fix pass's account. The two 🔴 closures are the
strongest: the exact tree that produced round 1's failures now produces the
opposite reading.

**One new defect, and the fix for 🔴 1 created it.** The decline was put in
front of *both* halves of the class reader's case, and only one of them needed
it. On a tree with a test module mid-edit, a newly planted unguarded scope —
the seventh helper the whole of phase 4 exists to catch — now goes unnamed and
the run exits 0. That is round 1 🔴 1's own shape inverted: then the case
failed where it should have declined, now it declines where it should judge.

Nothing else opened. The orchestrator's `seal/follow-up.md` append is accurate
and correctly placed; one small thing about where the correction sits is a ⬜.

---

## 🟡 1 · The decline was placed in front of the offender half, so a mid-edit tree hides a seventh helper

**Location** — `tests/test_a_shrunken_corpus_declines_to_judge.py:311`
(`classified_scopes`), consumed at `:380` NAME NOT IN TREE
(`test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`).

`classified_scopes` computes `found`, then declines before returning: NAME NOT IN TREE

```python
    found = derivers(present, root=root)
    vanished = set(PATH_LIST_CALLS) - set(found)
    if vanished:
        gone = {key.split("#", 1)[0] for key in vanished}
        if gone <= set(missing):
            decline_if_shrunken(sorted(gone), DECLINES_CLASS)
    return found
```

The caller then asks two different questions of `found`, and only the second
needs a whole corpus:

- `set(found) - set(PATH_LIST_CALLS)` — **a scope the reader found that no
  table accounts for.** A found scope is in a module that is on disk, so this
  is a positive sweep and needs nothing else.
- `set(PATH_LIST_CALLS) - set(found)` — **a classified scope that vanished.**
  This is the liveness half, and it is the one round 1 asked to decline.

Because the decline sits inside the helper, it fires before the caller
evaluates either. The offender half is silenced along with the liveness half.

**Executed.** One unguarded scope planted in a tracked test module, and the
same tree with one other test module deleted from disk and the removal
unstaged:

| Tree | Result | The planted scope named? |
|---|---|---|
| plant only, whole tree on disk | exit 1, `1 failed` | **yes** |
| plant, and one tracked test module off disk | exit 0, `13 passed, 2 skipped` | **no** |
| neither | exit 0, `1 passed` | no |

**What it costs.** `spec.md` §*Is a skip a weakening* settles this direction
for the whole work item: *the positive sweeps do not skip themselves. They run
on what remains and report on it. A whole sweep that declines to judge at the
moment a release is about to be committed is the silent nothing the paragraph
above refuses.* The reader written to close the class now does exactly that,
on an ordinary mid-edit tree.

It also takes a second protection down with it. `git_listing`'s docstring
records that the listing words stay at the call site on purpose, because
moving them into the helper would take every scope out of the class. Nothing
pins that convention except this same equality assertion — so on a mid-edit
tree, a refactor that moved `ls-files` into the helper would also pass in
silence.

**Mitigating, and worth stating.** The run prints `2 skipped` rather than
going wholly quiet, and the skip reason names the missing module. A person
reading the count line has something to pull on. The gate's verdict is still
green.

---

## ⬜ 2 · The follow-up row's corrected pointer sits at the far end of the cell from the stale one

**Location** — `seal/follow-up.md`, the row beginning *Writing a
`survivors.md` row silences its survivor a SECOND way*, commit `e29a0e51`.

The append itself is right, and I say that first. Appending rather than
rewriting is this row's own established shape — it already carries *round 2
corrected it* and *the rider clause this row first carried was wrong and is
corrected here by whoever wrote it*. Leaving to the owner whether #371's
closure was meant to cover the range half is the correct place to stop, and
`CLAUDE.md`'s fragment rule names `CHANGELOG.md` and `seal/ledger.md` and not
this file, so a shared-file append here breaks no rule. The measurement in it
matches what I executed in round 1.

What is left is where the correction sits. The sentence *so this row stays
open and is tracked as #371* is mid-cell; the correction saying that pointer
is now false is roughly fifteen hundred characters further on, at the end. The
append names this problem itself — *a reader meeting it today is told a live
defect is done* — and then leaves the reader to meet it. Four words at the
stale sentence would close that without taking the owner's judgment.

---

## Carried forward, each re-derived

I ran every closure rather than reading it. None was accepted on the fix
pass's account.

**Round 1 finding 1 — the class reader now declines.** The identical
reproduction from round 1: `tests/test_release_hygiene.py` removed from disk,
removal unstaged, the class reader run.

| | round 1, at `539d32df` | round 2, at `e29a0e51` |
|---|---|---|
| result | exit 1, `2 failed, 12 passed` | exit 0, `13 passed, 2 skipped` |

Mutating `if gone <= set(missing)` to `if True` turns
`test_a_test_module_the_tree_deleted_is_not_a_scope_somebody_removed` red at
exit 1 and restoring it turns it green — so the half that keeps a real removal
from being carried away by a neighbour is genuinely pinned, not merely
written. That was the assertion most at risk and it holds.

**Round 1 finding 2 — the contract is restored.** Over `5bf22ddb..HEAD` at the
tip:

| Exemption | Result |
|---|---|
| none | **exit 1**, `tests/test_the_payload_meter_says_what_it_measured.py:835` named with both shared phrases |
| `--exempt …/survivors.md` | **exit 0**, one `exempt` line printed with the grounds |

At the reviewed SHA both readings were exit 0 with nothing under `exempt`,
which was the finding. The new anchor, `where the other spelling arrives`, is
text the check prints as standing and is not a phrase the check matched, so
quoting it cannot subtract anything from what is looked for — that is why this
anchor works where the first one did not. I also verified the overview's claim
about `2c83b2bb` directly, with that commit's own `survivors.md`: exit 1
without the flag, exit 0 with one `exempt` line. The claim is true.

**Round 1 finding 3 — the decline no longer carries a finding away.** Mutating
`if absent and not unexplained:` back to `if absent:` turns
`test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit` red at exit
1; restored, green. The helper returns the paths the tree does not explain and
declines only when every absent path is explained.

**Round 1 finding 4 — what stands is coordinate-only.** The paragraph is gone.
What replaces it states why the refresh is forced, says it is bookkeeping, and
points at `overview.md` and `phases/phase-5.md` for the substance. No count,
no claim about the build's own reading. That is the whole of what I asked for.

*On the one word the fix pass changed from my draft* — *takes `--strict` to
NOT SEALED* became *takes `--strict` to exit 2 — the reading `broad-gate`
reports as NOT SEALED*. The correction is right and my draft was loose.
`phases/phase-5.md` records `--strict` at exit 2 on the drifted tree, and I
measured exit 0 on the clean one; `NOT SEALED` is a word printed by something
else reading that code. Naming both the exit code and who turns it into that
phrase is more useful than either alone, and it is still coordinate-only.

**Round 1 finding 5 — the overview now describes the tree it is about.** It
separates the two ways the report went quiet, gives the measurement at
`539d32df`, and says which half was the branch's to fix and which is the
class. Verified against my own round 1 readings.

**Round 1 finding 6 — the checklist sentence is now true.** It reads *one
appears when the tree is also mid-edit somewhere a check like that reads,
under `docs/`, `skills/`, `templates/`, `tests/` or a shipped `.py`*. Adding
`tests/` is correct **because** finding 1 was fixed: before that fix a
mid-edit `tests/` produced a red build, and now it produces a skipped case,
which is what the sentence says. The two fixes were made to agree rather than
the sentence being written around the defect.

**Round 1 finding 7 — the root is used for both inputs.** `version` takes a
root, `timer_offenders` passes its own, and the caller reads `plugin.json`
once and hands the value to both consumers. Mutating `version(root)` back to
`version()` turns `test_the_running_version_comes_from_the_root_being_swept`
red at exit 1; restored, green. The case is well chosen — it declares a
fixture version below both numbers in the fixture's documents, so reading the
wrong root would make both numbers history and the sweep would report nothing.
That is the direction where a wrong root hides rather than fails.

**Round 1 finding 8 — I accept the argument, and it is better than what I
proposed.** The block is shared as `tests/conftest.py#git_listing` and the
listing words deliberately stay at each call site. I checked the reasoning
against the reader rather than taking it: `_path_list_words` collects string
constants among a call's own children and skips nested calls, so
`git_listing(root, "ls-files", *SCANNED)` still reads as a deriving scope,
while a helper that swallowed the subcommand would take all seven out of the
class. `tests/conftest.py` is itself inside the reader's corpus and
`git_listing` is correctly absent from `PATH_LIST_CALLS`, because its own
`subprocess.run` names no listing word. The suite agrees: the class reader
passes at the tip. Recording the reason in the helper's docstring is the right
place for it.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The decline sits inside `classified_scopes`, in front of both halves of the case, so on a mid-edit tree a newly planted unguarded scope is not named and the run exits 0 — the offender half is a positive sweep and must judge what remains | `tests/test_a_shrunken_corpus_declines_to_judge.py:311`, consumed at `:380` | open | Executed: plant alone, exit 1 and the scope named; plant plus one tracked test module off disk, exit 0, `13 passed, 2 skipped`, the scope named nowhere. `spec.md` §*Is a skip a weakening* — *the positive sweeps do not skip themselves* · NAME NOT IN TREE |
| ⬜ 2 | The corrected pointer for #371 sits at the end of a very long cell while the stale *tracked as #371* stays mid-cell, so a reader meets the wrong pointer first | `seal/follow-up.md`, the survivor-exemption row, `e29a0e51` | open | Read. The append itself is accurate, correctly placed and correctly stops short of the owner's judgment; this is only where the correction sits |
| carried | Round 1's first finding — the class reader did not decline on a shrunken corpus | `tests/test_a_shrunken_corpus_declines_to_judge.py` | confirmed | Executed: the identical round 1 reproduction now gives exit 0, `13 passed, 2 skipped` where it gave exit 1, `2 failed`. Mutating `if gone <= set(missing)` to `if True` turns the new case red and restoring it turns it green |
| carried | Round 1's second finding — the survivors record silenced the check that reported it | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md` | confirmed | Executed over `5bf22ddb..HEAD` at the tip: exit 1 with no exemption and the file named; exit 0 with the exemption and one `exempt` line printed. The new anchor is standing text the check prints and is not a phrase it matched |
| carried | Round 1's third finding — the coverage decline carried a real finding away | `tests/test_no_document_names_the_old_roots.py` | confirmed | Executed: mutating `if absent and not unexplained:` to `if absent:` turns `test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit` red at exit 1; restored, green |
| carried | Round 1's fourth finding — the build's verdict sat in the frame | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md` | confirmed | Read. The paragraph is gone; what stands states why the refresh is forced and points at `overview.md` and `phases/phase-5.md`. The one reworded clause is more accurate than my draft, and the note is still coordinate-only |
| carried | Round 1's fifth finding — the overview described the survivor report as it stood before the fix | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` | confirmed | Read against my own round 1 measurements, and its claim about `2c83b2bb` executed separately with that commit's own exemption file: exit 1 without the flag, exit 0 with one `exempt` line |
| carried | Round 1's sixth finding — the checklist preamble was wrong about a mid-edit `tests/` tree | `docs/release-checklist.md` step 3 preamble | confirmed | Read, and true only because the first finding was fixed: a mid-edit `tests/` now produces the skipped case the sentence describes |
| carried | Round 1's seventh finding — the running version came from `ROOT` and was read twice | `tests/test_release_hygiene.py` | confirmed | Executed: mutating `version(root)` back to `version()` turns `test_the_running_version_comes_from_the_root_being_swept` red at exit 1; restored, green. The caller now reads `plugin.json` once |
| carried | Round 1's eighth finding — the git-listing block was copied six times | `tests/conftest.py`, and the six helpers | confirmed | Read, and the argument for keeping the listing words at each call site checked against `_path_list_words` rather than accepted: swallowing the subcommand would take all seven scopes out of the class the reader enumerates |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The corpus half and the range half of the survivor-exemption silence | already deferred in round 1, to `deferred #308`; `seal/follow-up.md`'s survivor-exemption row now carries the live measurement and names #308 as the open home | the repository owner |
| Whether #371's closure was meant to cover the range half | `seal/follow-up.md`, the same row, `e29a0e51` | the repository owner |
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | already deferred in round 1, to `overview.md` §*Not done*, which still names no durable home | the repository owner |
| Q1 — whether a path missing from disk should have its index content swept | already deferred in round 1, to `questions.md` Q1 | the repository owner |

## Paste-ready fixes

**🟡 1** — split the two halves so only the liveness one declines. In
`tests/test_a_shrunken_corpus_declines_to_judge.py`, replace
`classified_scopes` with: NAME NOT IN TREE

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

Then judge the offender half first, and never behind the decline:

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

and, in the vacuity case, keep the decline seam and drop the helper that no
longer exists:

```python
def test_the_reader_finds_the_helpers_this_work_guarded():
    present, missing = suite_modules()
    found = derivers(present)
    # Declines when the tree explains the gap; judges otherwise.
    vanished_scopes(found, missing)
```

The case added for round 1 moves to the same seam:

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

And the case §15 owes, pinning the half that must not decline:

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

**⬜ 2** — in `seal/follow-up.md`, make the stale pointer say that it is
corrected further down, and change nothing else:

```
so this row stays open and is tracked as #371 (closed; see the correction at
the end of this row)
```

---

Needs a fix: yes — 🟡 1, the decline sits in front of the offender half, so a
mid-edit tree hides a newly planted unguarded scope and the gate exits 0

Loses a record or crashes: no

---

## Proof block

**Executed** — `bin/test -q` over the eight modules the fix range touches
(exit 0, 179 passed) and over the rider check plus every module reading
`seal/follow-up.md` (exit 0, 726 passed, 1 skipped); the round 1 reproduction
against the fixed reader; three mutate-run-restore cycles driven from one
Python script that asserts each substitution matched exactly once and compares
the restored bytes; the planted-scope probe on a whole tree and on a mid-edit
tree; `survivor_check.py` at the tip with and without the exemption and at
`2c83b2bb` with that commit's own exemption file; `evidence_check.py --strict
.`; `git ls-files` for paths containing a space. Every exit code was read from
`$?` or from a `returncode`, never through a pipe.

**Read** — the whole fix range diff, code and documents; `round-1.md`;
`seal/follow-up.md`'s survivor-exemption row before and after `e29a0e51`;
`spec.md`, `overview.md`, `survivors.md`, `docs/release-checklist.md`;
`survivor_check.py`'s exemption path.

**Unverified** — the fix pass's own figures that I did not re-run: 1009 passed
over 26 modules, 161 over seven, `ruff`. Answered by `specseal:sealer`. The
full suite, the repository-wide lint and the typecheck are out of this agent's
scope under `agent-contract` §2.

**Scope** — a verifying round, scoped to the fix diff. I widened once, to run
the checks that read `seal/follow-up.md`, because the orchestrator asked for a
judgment on its own commit to that file.
