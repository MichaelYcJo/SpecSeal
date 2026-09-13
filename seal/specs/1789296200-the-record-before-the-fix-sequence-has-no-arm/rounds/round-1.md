# 1789296200-the-record-before-the-fix-sequence-has-no-arm — review round 1

| Field | Value |
|---|---|
| Target SHA | edb4578ae2e567e5e5813d8c6a0efee6037a2529 |
| Written late | no |
| Ran by | warden on claude-opus-5 |
| PR | 381 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | test_the_failure_names_the_fourth_exit (depth 1); BEHIND (depth 1); test_one_commit_between_reads_as_one_commit (depth 1); test_a_tree_behind_the_reviewed_commit_gets_neither_false_reading (depth 1) |
| Needs a fix | yes — 🟡 1 and 🟡 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the work item, against the whole branch: no earlier round to inherit.

The reviewer was told it is reviewing the machinery that records its own review — the record for this round is written by the `new` this branch modifies — and that running the modified `new` is narrow verification and therefore its own to do.

It was pointed at nine claims to open rather than accept: the measurement that flipped the design (40 of 152), the population it was taken on, the two differing records opened by hand, the existing case said to be unmodified, the fourteen mutations, the A7 probe, the two spent words, the template/generator window, and the `seal/ledger.md` re-verification — with an instruction not to inherit the sibling branch's verdict on that last one.

**The orchestrator verified both 🟡 independently before this record was written.**

Finding 1 by reading `chain_check.py:2542-2557`: the refusal a late record meets names neither `Written late`, nor `--written-late`, nor the fourth exit, and ends with *Commit the record when the round posts* — advice the person meeting it cannot act on, because their record is already committed.

**The orchestrator met that exact message in this session, on the sibling branch for #354**, having batched round 2's record with the one fix that round commissioned. The repair was available only because the commit was unpushed and could be split into three — the record with its verdicts open, the fix, then the closing update. A session that had pushed, or that met the line at the pull request, would have reached the dead end work item 1789034970 reached. That is first-hand evidence for finding 1 rather than a reading of it: the message was read by someone who needed the escape and it did not tell them the escape exists.

Finding 2 by reading `round_record.py#head_moved`: it computes `git log <reviewed>..<head>`, which is empty when HEAD is an ANCESTOR of the reviewed commit rather than a descendant. `head != reviewed`, so `head_moved_line` prints with count 0 and no listing, and both readings it offers — the fix pass already ran, or HEAD moved during the review — are false for a tree that is simply behind.

One ⬜ was taken out of the round's hands before the fix pass ran, because it was perishable. The forty differing records are named in no committed file; `overview.md:29` says `phases/phase-1.md` names them and it names two. The full list, 131 lines, existed only in the session scratchpad, which does not outlive the session — in a work item about a fact that survived only in a session that had ended. The orchestrator copied it onto the branch before dispatching the fix pass.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the refusal at the pull request never names the fourth exit, so the record that needs it is sent back to the three repairs this branch replaced | `skills/code-review/scripts/chain_check.py:2585` | **fixed** `1468e48` | fixed at 1468e48 — ``; executed — the shipped refusal captured and searched: `Written late`, `--written-late` and *fourth* all absent |
| 🟡 2 | `head_moved_line` prints *0 commits stand between them* with an empty listing and two readings that are both false, when HEAD is behind the reviewed commit | `skills/code-review/scripts/round_record.py:1548` | **fixed** `eceedfd` | fixed at eceedfd — ``; executed — scratch repository, HEAD detached one commit back, line captured verbatim |
| ⬜ 3 | *1 commit stand between them* — the singular arm is written for the noun and not the verb, and no case exercises it | `skills/code-review/scripts/round_record.py:1556` | **fixed** `89ecf36` | fixed at 89ecf36 — ``; executed — same probe, diverged-branch scenario |
| ⬜ 4 | the forty differing records are named in no committed file, and `overview.md` says `phase-1.md` names them | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29` | answered | Corrected at `9127c94`. `overview.md` and `phases/phase-1.md` now point at `phases/phase-1-measurement.txt` for all forty, and the rescued file is byte-identical to the original with its header counts intact — 310 / 158 / 152 / 112 / 40. **The finding's grounds were false and are corrected rather than repeated.** It said the population is gone because `git for-each-ref 'refs/remotes/pull/*'` returns nothing; that pattern is one path component short and `for-each-ref` matches components, not substrings. The orchestrator re-ran it: the starred form returns 0, `refs/remotes/pull` returns 138, `'refs/remotes/pull/*/head'` returns 138, and `a0f0e9a` — the adding commit `phase-1.md` names first — is an ancestor of `refs/remotes/pull/364/head`. The number can be retaken in this clone. What is true is narrower and is what the record now says: those refs reach no clone that has not fetched `refs/pull/*`, and the named list is what makes the forty checkable either way |
| ⬜ 5 | `written_late_reason` is called on every record whether or not anything is late, costing one uncached `git show` each | `skills/code-review/scripts/chain_check.py:2537` | **fixed** `0d4bbaf` | fixed at 0d4bbaf — ``; read |
| ❓ 6 | the run's only new arm is one the orchestrator holds, and nothing counts how often it is reached for | `skills/code-review/orchestration.md:415` | deferred seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md | seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md |


## Checked and found clean

Axes the round opened, measured, and closed with nothing to fix. They
carry no finding number because they are not findings — `round_record.py`
refuses a `#` column that is not a bare integer, and a round-prefixed or
marker-only id is how eight findings once collapsed into one.

| What was checked | Location | Grounds |
|---|---|---|
| hostile `--written-late` values cannot corrupt a record — a pipe, a newline and an unclosed HTML comment are each refused before the write | `skills/code-review/scripts/round_record.py:829`, `skills/code-review/scripts/round_record.py:593` | executed — all three refused, exit 2, no record written. `write_record` asks the hider question of the composed artefact, so the new flag inherits the guard without a guard of its own |
| A6's pin is the existing case, genuinely unmodified and it still fires | `tests/test_a_record_precedes_the_fixes_it_commissions.py` | executed — the case body is absent from the diff; only the `record` and `late_run` helpers gained a defaulted parameter it does not pass. Turning the error branch into a notice reddens it |
| the four new units each die alone | `skills/code-review/scripts/round_record.py:1486`, `skills/code-review/scripts/round_record.py:1517`, `skills/code-review/scripts/round_record.py:1548`, `skills/code-review/scripts/chain_check.py:2435` | executed — five mutations in a throwaway clone, every one killed, each reddening the cases its own phase record claims |
| no red window between `templates/sdd-round.md` and the generator | `templates/sdd-round.md`, `skills/code-review/scripts/round_record.py:1865` | executed — both land in `6d4f30f`, and five further modules that generate or read a record are green at 302 passed |
| `close` and `seal` keep the new row | `skills/code-review/scripts/round_record.py:2892` | read — both assign into rows they find by `field_index` and never rebuild the block, which is what A7's probe found and what its case now holds |
| the ten re-stamped `seal/ledger.md` rows are honest, and the new claims went to the fragment | `seal/ledger.md`, `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md` | executed — `evidence-check .` exit 0, 1161 ok · 0 drifted · 0 broken. Re-verification is neither the appending `CLAUDE.md` forbids nor the removal it carves out: the three new claims are in the branch's own fragment and `seal/ledger.md` gained no row |
| neither spent word was coined with | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/spec.md:150` | executed — no added line in `skills/`, `templates/`, `docs/` or `tests/` uses *arm* in any sense, and the one use of *declaration* is `routing.md`'s established meaning in a docstring; `tests/test_one_word_one_meaning.py` green |
| the A7 probe and its scratch repository really are gone | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/phases/phase-3.md` | executed — nothing named for it survives in the repository, in the session scratchpad, or as a worktree or branch. The one `test_tmp_*` file still in the scratchpad belongs to a sibling work item's session and reads that item's own measurements, not this one's |

## Paste-ready fixes

```python
        else:
            errors.append(
                (
                    rel,
                    line_no,
                    message + ". Where the fix pass really did run before this "
                    "record reached a commit, the record may SAY so and this "
                    f"prints instead of failing: a `| {WRITTEN_LATE} | "
                    f"{FLOOR_YES} — <why> |` row in its field table, written by "
                    '`round_record.py new --written-late "<why>"`, or added by '
                    "hand and committed like any other correction to a record "
                    "already on the branch. A bare `yes` buys nothing — the "
                    "reason is the whole of what the row is for",
                )
            )
```
```python
def test_the_failure_names_the_fourth_exit(repo):
    """`agent-contract` §14. The record refused here is the only one that
    needs the row, and it is refused for not having it — so the refusal is
    the one text where naming the row changes what anybody does."""
    late_run(repo, NEW_ITEM)
    code, out = run(repo)
    assert code == 1, out
    assert check_module().WRITTEN_LATE in out, (
        "the record that needs the fourth exit is not told it exists"
    )
    assert "--written-late" in out, out
    assert "added by hand" in out, (
        "the flag alone names an exit a committed record can no longer take"
    )
```
```python
def head_moved_line(reviewed, head, between):
    """The line `new` prints when the two differ. Read by a person, so
    `agent-contract` §14 pins every sentence of it in a case."""
    if not between:
        # HEAD reaches nothing the reviewed commit does not, and the two are
        # still different commits: HEAD is BEHIND the record's own target, or
        # sits on another branch entirely. Neither reading below describes
        # that, and printing them would send the reader to a repair for a
        # state they are not in.
        return (
            f"round-record: {HEAD_MOVED} {DASH} the round read {reviewed[:7]}, "
            f"HEAD is {head[:7]}, and HEAD reaches no commit the round did "
            "not.\n"
            "  So nothing landed after the review on THIS tree: HEAD is "
            "behind the commit this record names, or on another branch. "
            "Neither of the usual two readings applies.\n"
            f"  Check that `--target` names the commit this tree's HEAD stood "
            "at when the round ran, and that you are in the tree the round "
            "reviewed. Nothing is refused here, and the record is written."
        )
    count = len(between)
```
```python
        f"is {head[:7]}, and {count} commit{'' if count == 1 else 's'} "
        f"{'stands' if count == 1 else 'stand'} between them.{listing}\n"
```
```python
    if not late:
        return [], []
    began = item_began(rel)
    said = written_late_reason(reader, root, rel)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_new_says_when_head_is_not_the_target.py tests/test_a_record_says_why_it_was_written_late.py tests/test_a_record_precedes_the_fixes_it_commissions.py -q` | 67 passed in 46.92s |
| `bin/test tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py tests/test_a_record_says_what_ran_it.py tests/test_the_reopening_is_one.py -q` | 302 passed, 1 skipped in 174.95s — the modules that generate or read a record and were not named in the account's verification table |
| `bin/test tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py -q` | 38 passed |
| `bin/test tests/test_a_probe_does_not_outlive_its_round.py tests/test_a_probe_that_commits_says_so.py -q` | 10 passed |
| `bin/evidence-check .` | exit 0 — 1161 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| mutation, throwaway clone at `edb4578`: the three calling lines removed from `new` | 5 failed, 1 passed — killed |
| mutation: `head_moved_line`'s listing blanked | 1 failed, 5 passed — killed |
| mutation: `written_late_cell`'s emptiness test disabled | 5 failed, 6 passed — killed |
| mutation: `written_late_reason` returns a reason for a bare `yes` | 2 failed, 48 passed — killed |
| mutation: `written_late` never consults the cell | 1 failed, 49 passed — killed |
| mutation: `written_late` records the late record as a notice rather than an error | `test_a_record_added_after_its_own_fix_fails_after_the_cutoff` failed — A6's pin fires |
| probe: `new --written-late` with a pipe, a newline, and an unclosed HTML comment | exit 2 each, no record written, each refused by name |
| probe: `new` with HEAD detached one commit behind the reviewed commit | `and 0 commits stand between them`, empty listing, both readings printed — 🟡 2 |
| probe: `new` with the reviewed commit and HEAD on diverged branches | `and 1 commit stand between them` — ⬜ 3 |
| `git show a0f0e9a` and `git log 5ce162e..a0f0e9a^` | phase 1's first named differing record re-derived: parent `b46ff77`, one commit between, subject as `phase-1.md` quotes it |
| `git for-each-ref 'refs/remotes/pull/*'` | no refs — the measurement's population is not reconstructible from this tree |
| `git status --porcelain`, `git worktree list`, `git branch -a` | tree clean at `edb4578`; no worktree, branch or file left by this branch's probes. This round's own clone and probe files are deleted |
| the full suite, the repository-wide lint, the typecheck | **not yet — not run, and not this round's** (`agent-contract` §2). The sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `new --target <a revision that is not a full SHA>` writes the revision verbatim into `Target SHA`, and the cell then names no commit | already deferred by the branch: `overview.md` §Not done, the docstring of `test_a_target_given_as_a_revision_is_named_by_its_sha`, and an issue the orchestrator filed on the tracker | the repository owner — I confirmed the deferral is honest, since `new` ends in the very check that reports the state, so it is loud rather than silent. Recorded here so a later round does not re-open it as new |
