# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — review round 1

| Field | Value |
|---|---|
| Target SHA | 539d32df |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 440 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 the class reader does not decline on a shrunken corpus; 🔴 2 the survivors record silences the check that reported it; 🟡 3 the coverage decline carries a real finding away; 🟡 4 the build's verdict sits in the frame rather than in the record the template gives it |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 at `539d32df`, on `fix/432-282-a-tracked-file-the-tree-deleted-stops-the-sweep` against `release/v0.12.1` (`5bf22ddb`), draft pull request #440, fourteen commits. The frame settled something both tickets got wrong — a silent skip holds for a positive sweep and not for a case reading the corpus to prove an entry is still alive — so the round was asked to judge the built work against that decision and the decision against its grounds.

One question was put ahead of the code: the builder edited `spec.md`, the framer's document. The orchestrator had opened the diff and separated the halves — three evidence stamps re-stamped to what those units hold after the work, which the records arm forces, and a paragraph disclosing that the frame's count of three was nine. What was asked is whether a builder disclosing the frame's own undercount inside the frame is right, or whether it belongs only in the build's records, weighed against `agents/framer.md`'s argument that a `spec.md` the builder writes stops being a contract.

Three of the build's own claims were handed over as claims: that the class is six helpers rather than five, the sixth found by the reader the last phase built because it lists with `git ls-tree` rather than `git ls-files`; that there are three liveness cases rather than two; and that `plan.md` was wrong about a fold producing skipped cases, so the checklist sentence was written to the measurement instead. Two further places were named as earning the review — the re-stamp of nine anchors in the shared ledger, which is a claim about reading that is checkable at the anchors, and a `survivors.md` written for one survivor the build judged a false positive. The orchestrator had executed the tip, the clean tree, the commit count and the `spec.md` diff, and had re-run none of the build's checks.

## Verdicts

<!-- Orchestrator, 2026-09-18: the four ⬜ corrections arrived from the report with a bare marker and a verdict of `open`, which the generator refuses — a row that is open commissions a fix-table row and so needs a number. They are numbered 5 through 8 in the order the report lists them; nothing else was touched. -->

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The class reader's two liveness assertions do not decline on a shrunken corpus, so a tracked test module the tree deleted turns the module red and the refusal tells the reader to delete a live classification row | `tests/test_a_shrunken_corpus_declines_to_judge.py:296`, consumed at `:345` and `:391` | open | Executed in the clone: clean tree `14 passed` exit 0; with `tests/test_release_hygiene.py` off disk and the removal unstaged, `2 failed, 12 passed` exit 1. `plan.md` §*Alternatives considered* rejects failing on a shrunken corpus in its own words |
| 🔴 2 | `survivors.md`'s Grounds cell reproduces the two shared phrases the check matched, and adding that file is what stopped the survivor being reported at all — issue #365's class, one file over | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md:8` | open | Executed: exit 1 with one survivor at `f8cf32e5..5ffa5dfb`; exit 0 and nothing under `exempt` at `f8cf32e5..539d32df` with the exemption passed. `114b78f1` changes that one file only. `seal/specs/1789211172-a-round-record-disarms-survivor-check/spec.md` states the same mechanism for `rounds/` records |
| 🟡 3 | `uncovered` declines whenever any named path is merely off disk, so a named path that genuinely left the corpus is reported nowhere | `tests/test_no_document_names_the_old_roots.py:139` | open | Executed: with one `COVERED` path missing and the other genuinely absent, the helper declines and the reason names only the missing one |
| 🟡 4 | The paragraph added to the frame asserts the build's own diligence inside the document its spec compliance is judged against, and `templates/sdd-overview.md:58` gives that paragraph a home the branch is already using | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md:238` | open | `agents/framer.md` §*Why the frame is not the builder's to draw*, and its *comes back as a written record and a hand-back*. The same correction is already in `overview.md`'s divergence table and in `phases/phase-5.md`. The three re-stamped hashes are forced and are not part of this finding |
| ⬜ 5 | `overview.md` §*Not done* states the check names the payload-meter file and exits 0 because of the exemption; at the reviewed SHA it names nothing with or without it | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` §*Not done* | open | Executed, and it follows from 🔴 2 |
| ⬜ 6 | Step 3's new preamble says a mid-edit tree produces a skipped case; under `tests/` it produces a red build | `docs/release-checklist.md` step 3 preamble | open | Follows from 🔴 1, executed |
| ⬜ 7 | `timer_offenders` resolves the running version from `ROOT` rather than its own `root`, and the version file is now read twice per run | `tests/test_release_hygiene.py:477` | open | Read. No present caller is affected |
| ⬜ 8 | The git-listing `subprocess.run` block is copied into six helpers; only the predicate was shared | `tests/conftest.py`, and the six helpers | open | Read |
| ⬜ | Confirmed: the shared-ledger re-stamp is 9 distinct anchors across 8 rows, and the checker is clean | `seal/ledger.md` | verified | Executed: 11 changed anchor cells over 8 changed rows, 9 distinct; `evidence_check.py --strict .` exit 0, `1353 ok · 0 drifted · 0 broken` |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer`, spawned by the orchestrator once the rounds settle |

## Paste-ready fixes

```python
DECLINES_CLASS = "the suite-wide enumeration of scopes that list paths from git"


def suite_modules():
    """`(every `tests/*.py` on disk, the tracked ones that are not)`."""
    out = subprocess.run(
        ["git", "ls-files", "tests/*.py"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return on_disk(ROOT, out)


def classified_scopes(present, missing, root=ROOT):
    """What the reader found over `present`, or `pytest.skip` when every scope
    that vanished is in a module the working tree deleted.

    The inverse direction the three call sites in the other modules answer,
    in the module that enumerates the class. To this half a module the tree
    deleted and a scope somebody removed are the same evidence -- and the
    refusal below tells the reader to classify the difference, which on a
    mid-edit tree means editing a live row out of a table on evidence about
    the working tree. Conditional on EVERY vanished scope being explained, so
    a genuine removal is still reported beside a skipped one.

    The pair is a parameter rather than fetched here, so the case below can
    hand it a tree it chose without deleting a file the suite is running from.
    """
    found = derivers(present, root=root)
    vanished = set(PATH_LIST_CALLS) - set(found)
    if vanished:
        gone = {key.split("#", 1)[0] for key in vanished}
        if gone <= set(missing):
            decline_if_shrunken(sorted(gone), DECLINES_CLASS)
    return found
```
```python
def test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard():
    found = classified_scopes(*suite_modules())
```
```python
def test_the_reader_finds_the_helpers_this_work_guarded():
    found = classified_scopes(*suite_modules())
```
```python
def test_a_test_module_the_tree_deleted_is_not_a_scope_somebody_removed():
    """The inverse direction in the module that enumerates the class.

    An unstaged `git mv` of a test module would otherwise report its scope as
    no longer deriving a path list, and the instruction that comes with that
    report is to classify the difference -- a live row edited out of a table
    on evidence about a working tree.
    """
    key = sorted(APPLIES_THE_SHARED_GUARD)[0]
    rel = key.split("#", 1)[0]
    present, _ = suite_modules()
    with pytest.raises(pytest.skip.Exception) as declined:
        classified_scopes([p for p in present if p != rel], [rel])
    reason = str(declined.value)
    assert rel in reason, reason
    assert DECLINES_CLASS in reason, reason
    assert "not judging" in reason, reason

    # A scope that vanished for any other reason is still a finding.
    assert classified_scopes(present, [rel]) == derivers(present)
```
```
| `tests/test_the_payload_meter_says_what_it_measured.py` | `skills: [alpha, beta]` | The range rewrote `test_the_scan_covers_something`, whose two named-path assertions became a `COVERED` tuple and a declining helper. The two phrases the check matched are not quoted here, because a `survivors.md` is in the pool the check searches and quoting them is what silenced the report (#365's class, one file over). They fall across a seam between an assertion and a skill path on one side, and a YAML flow-form frontmatter fixture on the other. The standing line is about a meter reading an inline list; it is not a copy of any sentence this work removed, and nothing about it would become false if the rewritten case were reverted |
```
```bash
python3 skills/code-review/scripts/survivor_check.py --range 5bf22ddb..HEAD \
  --exempt seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md \
  > /tmp/survivor.txt 2>&1; echo $?
grep -c '^  exempt' /tmp/survivor.txt
```
```python
def uncovered(files, missing):
    """The named paths the scan no longer covers, or `pytest.skip` when every
    one of them is a file the working tree deleted.

    Q3's third case, found by reading the five modules rather than by either
    ticket. `skills/implement/SKILL.md` leaving the corpus through a `git mv`
    that has not been staged is exactly the state this work is about, and
    without this the case reports the scan as no longer covering a file that
    is merely somewhere else -- a verdict about coverage taken from evidence
    about the working tree.

    **Conditional on every absent path being explained.** A named path absent
    for another reason is a real loss of coverage, and declining over a
    neighbour that is merely mid-edit would report it nowhere.
    """
    absent = [rel for rel in COVERED if rel not in files]
    unexplained = [rel for rel in absent if rel not in missing]
    if absent and not unexplained:
        decline_if_shrunken(sorted(set(absent) & set(missing)), DECLINES_COVERAGE)
    return unexplained
```
```python
def test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit():
    """The decline must not carry a finding away with it."""
    assert uncovered(files=[], missing=[COVERED[0]]) == [COVERED[1]]
```
```
**The three stamps above are refreshed to what those units hold after the
work,** because the records arm of `evidence-check` resolves a stamp in a live
work item as it resolves a ledger row, and a stamp naming content that moved
takes `--strict` to NOT SEALED. The refresh is bookkeeping and nothing else.
What actually drifted, how far, and on what grounds is the build's to state:
`overview.md` §*Where spec and implementation diverged* and
`phases/phase-5.md` carry it.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository, checked out at `539d32df` | clean tree, tip confirmed `539d32d` |
| `bin/test -q` over the seven modules the diff touches | exit 0, `158 passed` |
| `bin/test -q tests/test_a_shrunken_corpus_declines_to_judge.py`, clean tree | exit 0, `14 passed` |
| the same module with `tests/test_release_hygiene.py` removed from disk, removal unstaged, then restored | exit 1, `2 failed, 12 passed`; both failures are the two liveness assertions |
| a temporary probe calling `uncovered` with one named path missing from disk and one genuinely absent | declined; the reason names only the missing path and never the other |
| `bin/test -q tests/test_one_word_one_meaning.py` | exit 0, `18 passed` |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0, `1353 ok · 0 drifted · 0 broken`, records arm `3 stamps read · 0 drifted` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..5ffa5dfb` | exit 1, one survivor at `tests/test_the_payload_meter_says_what_it_measured.py:835` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..HEAD` | exit 0, `no removed wording is still standing` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..HEAD --exempt <this work item>/survivors.md` | exit 0, and no `exempt` line printed |
| `git show --stat 114b78f1` | one file changed, `survivors.md`, 9 insertions |
| a script comparing the anchor cells of every changed row of `seal/ledger.md` | 11 changed cells over 8 rows, 9 distinct anchors |
| `git ls-files -s` filtered to mode `120000` | no tracked symlinks, so `os.path.isfile` misclassifies nothing in this tree |
| grep for the two new fixture literals in `tests/test_no_real_identifiers.py` across the tree | both confined to that module, which excludes itself from its own corpus |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; it is the sealer's one act, and it comes due once these findings are answered |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | `overview.md` §*Not done*, which names no ticket and no durable home for it — it says only that it belongs to whoever opens that file next | the repository owner, if it is to have a home |
| Q1 — whether a path missing from disk should have its index content swept | `questions.md` Q1, default `Skip it`, a person's row | the repository owner |
| Whether a skip reason renders in full in the release runner's quiet output | `overview.md` §*Not verified* | the repository owner, at the next release |
