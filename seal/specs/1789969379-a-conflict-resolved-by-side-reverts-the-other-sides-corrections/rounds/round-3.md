# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — review round 3

| Field | Value |
|---|---|
| Target SHA | 31b320e5f0e8742f1b76104d527173b186755dd8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 467 |
| Broad gate | 41e351c against release/v0.12.2 |
| Fixes checked by | no fixes to check |
| Fix range | `31b320e5f0e8742f1b76104d527173b186755dd8..31b320e5f0e8742f1b76104d527173b186755dd8`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 9, 10 and 11. Finding 9 is the one that matters: the bound comparison is arithmetically false at this SHA, and it went false because the fix range's own commit wrote a marker into a file its census counts. |
| Loses a record or crashes | no — nothing in this range writes to a ledger, `seal/ledger.md` is byte-identical to the base across the whole branch, no run crashed, and the new dedup key cannot dereference `None` because `losses` skips a row whose survivor did not stand. All three findings are false or unheld statements; none of them drops a record. |

- [x] Pass

## What this round was asked

Round 3, and the chain's arithmetic had already made it the last record: round
1 met the floor, round 2's verdicts closed on a fix, and the reopening is one.
The reviewer was told that before it began, with the reason — not to look less
hard, but because severity is the only thing left that changes an outcome once
the record after this one cannot exist.

Its target was one range, `7073a881..cb7d1f4a`, three commits closing round 2's
findings 6, 7 and 8. The bound's new census was named as the **third** census
of this work item and the first two were both circular, so the histogram was
asked for by the reviewer's own instrument rather than accepted.

Four things were handed over as judgments. Whether a seventh green-while-broken
unit exists, since this work item had produced one at every round and every
pass — six so far. Whether the class ratio is closing or continuing, given
round 1 named six where nine existed and round 2 named three where fourteen
did. Whether `seal/ledger.md` is still byte-identical to the base across the
whole branch after three more `--reverify` runs, which is the one thing a work
item about losing ledger corrections must get right about itself. And whether
the old-format trap the builder reported — a path-and-line form inside a
ledger cell read as an old coordinate — is real and untripped elsewhere.

The two issues opened between rounds, #468 and #469, were named as closed and
not the reviewer's to reopen, with a request to say if either is wrongly
scoped.

`evidence_check.py .` unscoped, `correction-check` against real history as well
as fixtures, exit codes read directly, `seal/ledger.md` off-limits to a whole
read. The verdict-table shape was spelled out again after two rounds in this
session were sent back by the generator for an unkeyed row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | The bound comparison reads 411 against 412; at this SHA it is 412 against 413, because `f58e350d` wrote a marker into one of the three files the census counts | `skills/evidence-check/scripts/correction_check.py#MARKER` | deferred #470 | Executed: the shipped pattern swept over bounds 0-8 across the three ledger files gives 373, 393, 402, 412, 412, 413, 413, 413, 413. The comparison the sentence makes still holds — three and four both reach 412 — and only the two absolute figures are wrong. The `seal/ledger.md`-only figures are stable because the branch does not touch that file |
| 10 | Six tracked files say the file carries 404 marker occurrences on 190 rows; 401 are on those rows and 3 are in prose the survival test never acts on | `skills/evidence-check/scripts/correction_check.py` module docstring | deferred #470 | Executed through the module's own `rows` and `markers`: 732 rows parsed, 190 carrying a marker, 401 occurrences inside rows, 404 over the whole file text. The module docstring's own §*Markers in prose are out of scope, by construction* is the rule that makes the 3 unwatched. Ledger row C1 states both halves in one sentence and contradicts itself |
| 11 | Finding 8's fix pins the first clause of C9's parent rule and not the second; ties fall to the first parent, nothing holds it, and the tie is the common path | `skills/evidence-check/scripts/correction_check.py#examine` | deferred #471 | Executed: a constructed tie exits 1, prints one entry and names the first parent, so the code does what C9 says. Mutation: rebuilding `carried` in reversed order leaves 48 of 48 green. `agent-contract` §14 — the parent SHA is the line that decides which hunk a reader opens. A proposed case was driven green on the shipped code and red on that mutation before it was written down |
| ⬜ | `loss.standing.key` in place of `loss.standing.raw` leaves 48 green, and `Row`'s docstring still names three things it is judged by | `skills/evidence-check/scripts/correction_check.py#Row` | correction | Executed. The shipped choice is right and stays: `_index` drops a shared first cell from `by_key`, but the anchor route can reach two surviving rows that share one, and keying on the cell would collapse their losses. 123 rows of `seal/ledger.md` share a first cell |
| ⬜ | #469's histogram mixes the three-file count of zero-word runs with the one-file count of one-word runs, and sums to neither corpus | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*What that does not close* | correction | Executed: three files `{0: 373, 1: 20, 2: 9, 3: 10, 5: 1}` = 413; `seal/ledger.md` alone `{0: 365, 1: 19, 2: 9, 3: 10, 5: 1}` = 404. The issue's table reads 373 and 19 together, totalling 412. Its conclusion — no run of four — holds on either corpus |
| ⬜ | `overview.md` names both deferrals as *an issue* with no number, and both issues are open | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* | correction | Read, and confirmed against the tracker: #468 OPEN, #469 OPEN. The round records carry both numbers; the work item's own prose carries neither |
| ⬜ | Round 2's four unpinned `MARKER` directions are still unpinned at the bound of five | `skills/evidence-check/scripts/correction_check.py#MARKER` | correction | Executed at the new bound: `[ \t]`→`\s`, `[a-z-]`→`[a-z0-9-]` and dropping `(?!\d)` each leave 48 green. Round 2's grounds — none is reachable through `Row.markers`, which reads one table line at a time — still hold. Carried forward from round 2, not re-derived as a verdict |
| 🟢 | Finding 6's census — every figure the fix states about `seal/ledger.md` | `skills/evidence-check/scripts/correction_check.py#MARKER` | not a defect | Executed with an instrument that is not the pattern and has no bound: 404 sites, 401 in cells, 3 in prose, 190 rows, histogram `{0: 365, 1: 19, 2: 9, 3: 10, 5: 1}`, no run of four, one run of five at `seal/ledger.md:1172`. The ten spellings and their counts match the code comment name for name |
| 🟢 | Finding 6's pattern invents no qualifier the file does not carry | `skills/evidence-check/scripts/correction_check.py#MARKER` | not a defect | Executed: the shipped pattern matches 404, 4 and 5 on the three ledger files and the independent census finds 404, 4 and 5 candidate sites. Exact agreement on every file, so no match is manufactured and no site is missed |
| 🟢 | Finding 6's fix is pinned in both directions | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_longest_qualifier_the_tree_carries_is_seen` | not a defect | Executed: the bound narrowed to four or to three turns one case red, and widened to six or twelve turns `test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier` red. Five is the only bound that leaves 48 green |
| 🟢 | Finding 7's fix closes the shape it was reported in, and cannot crash | `skills/evidence-check/scripts/correction_check.py#examine` | not a defect | Executed: restoring `loss.row.key` turns the new case red. Read: `losses` skips a row whose survivor is `None`, so `loss.standing` is never `None` where the tag is built |
| 🟢 | Finding 8's fix is pinned | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_parent_named_is_the_one_that_lost_the_most` | not a defect | Executed: `max` swapped for `min` turns that case red, where round 2 measured 45 of 45 green |
| 🟢 | No seventh green-while-broken unit in this pass | `tests/test_a_merge_cannot_silently_drop_a_correction.py` | not a defect | Executed: each of the three new cases goes red under the exact mutation it was written for. The streak this work item carried at every earlier round and pass is broken here |
| 🟢 | `seal/ledger.md` is untouched across the whole branch, after three more `--reverify` runs | `seal/ledger.md` | not a defect | Executed, and stronger than an empty diff: the blob hash is `2f885a09` at `release/v0.12.2` and `2f885a09` at the target SHA. The file is byte-identical, not merely diff-clean |
| 🟢 | The old-format trap the builder reports is real, and the rewording avoids it | `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` | not a defect | Executed in a throwaway copy: writing the path-and-line form into row C1's Notes makes `evidence_check.py` exit 2 and print `1 old-format`. The shipped cell says *line 1172 of* instead and the same run exits 0. No other cell on this branch trips it — the unscoped run reports `0 old-format` over 1385 anchors |
| 🟢 | Widening the bound to five causes no regression over real history | `skills/evidence-check/scripts/correction_check.py#examine` | not a defect | Executed: 31 reachable merges walked at the new bound, exit 0, `no correction marker was dropped at a merge`. The branch's own range holds no merge, exit 0 |
| 🟢 | The class of round 2's finding 6 is complete | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md` | not a defect | Executed: `git grep` over `403`, `38 of`, `nine spelling`, `bound is four`, `bound of four` and `365` across the tree. Every surviving occurrence is a historical quotation inside a CORRECTED block or a round record. Fourteen statements is the whole of what the round named, and the fourteen are corrected |
| 🟢 | The fix range leaves no removed wording standing | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/survivors.md` | not a defect | Executed: `survivor_check.py` over `7073a881..cb7d1f4a` exits 0 against 37 removed sentences, `no removed wording is still standing`. The three exemptions round 2 checked are not reached by this range |
| 🟢 | #468 and #469 are each correctly scoped | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* | not a defect | Read both issue bodies. #468 names the hand-maintained arm list rather than the one missing arm, and names the case that would hold the two lists against each other. #469 asks for the property rather than another literal spelling and refuses removing the bound. Neither is reopened |

## Paste-ready fixes

```python
# Five words is the bound and lowercase is the gate. A qualifier is a phrase
# inside the sentence, so a capital letter is the next sentence and a digit is
# the date itself. The longest run the tree carries is five -- `Re-read and
# re-stamped a third time <date>` at line 1172 of `seal/ledger.md` -- and the
# distribution has a hole where the old bound sat: runs of 0, 1, 2, 3 and 5
# words occur and **no run of 4 does**, so a bound of four matched exactly
# what a bound of three matched (403 in `seal/ledger.md`, against 404 at five)
# and bought nothing at all. Six and eight also match 404, so five is the last
# bound that changes an answer; going past it would turn
# `test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier` green for
# nothing.
#
# The figures here are over `seal/ledger.md` alone, deliberately. A count
# spanning `seal/ledger/*.md` moves whenever a work item records a correction
# in its own fragment -- this comment's first version said 411 against 412
# over the three files, and the commit that wrote round 2's correction marker
# into this work item's fragment made it 412 against 413 before it shipped.
# The shared file is the only part of the corpus a branch does not move.
#
# The bound is what keeps the verb from reaching across a clause to a date
# nobody wrote it against, which would manufacture a marker and then report
# its loss. The identity stays `(verb, date)`, so the spellings of one reading
# compare equal and a reword is not a loss.
```
```text
The six statements of `404 ... on 190 rows`. The file carries 404 marker
occurrences; 401 of them are on the 190 rows and 3 are in the file's prose,
which the survival test never acts on -- `correction_check.py`'s module
docstring says so under *Markers in prose are out of scope, by construction*.

correction_check.py:47
    "**404 marker occurrences on 190 rows.**"
  -> "**404 marker occurrences, 401 of them on 190 table rows and 3 in the
     file's prose.**"

tests/test_a_merge_cannot_silently_drop_a_correction.py:108, in
test_both_verbs_count_because_re_read_is_the_common_one
    "404 marker occurrences on 190 rows, since a row can"
  -> "401 marker occurrences on 190 rows -- 404 in the file, 3 of them in
     prose this check does not read -- since a row can"

seal/ledger/1789969379-...md row C1, Notes cell
    "they read **404 occurrences on 190 rows**, 401 in cells and 3 in prose"
  -> "they read **404 occurrences in the file**: 401 on 190 table rows and 3
     in prose, which the survival test does not read"

seal/specs/1789969379-.../plan.md:40
    "The file carries 404 marker occurrences on 190 rows, and 39 of them"
  -> "The file carries 404 marker occurrences, 401 of them on 190 rows, and
     39 of them"

seal/specs/1789969379-.../overview.md:121
    "404 occurrences on 190 rows, 39 qualified, ten spellings"
  -> "404 occurrences -- 401 on 190 rows and 3 in prose -- 39 qualified, ten
     spellings"

seal/specs/1789969379-.../changelog.md:27
    "repository: 404 marker occurrences on 190 rows, at least three spellings"
  -> "repository: 404 marker occurrences, 401 of them on 190 rows, at least
     three spellings"
```
```python
def test_a_tie_falls_to_the_first_parent(tmp_path):
    """The other half of the sentence the case above pins, and the half that
    runs in the common case: every marker older than the fork is carried by
    BOTH parents, so both lose the same count of it and the choice is a tie.

    Ledger row C9's Notes and `examine`'s comment both say ties fall to the
    first parent -- the side the person resolving the conflict had checked
    out -- and nothing held it, so rebuilding `carried` in any other order
    would change the SHA a reader is sent to open while the whole module
    stayed green (`agent-contract` §14).
    """
    base = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    ours = "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | ours |"
    theirs = (
        "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | theirs |"
    )
    got = "| R1 · a claim | `a/b.py#f@11111111` | Read. | merged |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    first = run(root, "rev-parse", head + "^1").stdout.strip()
    second = run(root, "rev-parse", head + "^2").stdout.strip()
    assert f"from parent {first[:7]}" in out, out
    assert f"from parent {second[:7]}" not in out, out
    assert "1 correction marker(s)" in out, out
```
```text
#469's histogram table, the `1 word` row
    "| 1 | 19 |"
  -> the 373 above it is the count over the three ledger files and the 19 is
     the count over `seal/ledger.md` alone, so the table sums to 412 and is
     neither corpus. Say which corpus the table is, then use its numbers:

     over the three ledger files at this SHA -- 0: 373, 1: 20, 2: 9, 3: 10,
     4: none, 5: 1, total 413
     over `seal/ledger.md` alone -- 0: 365, 1: 19, 2: 9, 3: 10, 4: none,
     5: 1, total 404

     The conclusion is unchanged on either: there is no run of four.

seal/specs/1789969379-.../overview.md §*Not done* and §*What that does not
close*
    "Answerer: the repository owner, as an issue opened from this pull
     request." / "Answerer: the repository owner, as an issue."
  -> name the numbers, since both are open: #468 for the broad gate's arm
     list, #469 for the bound being pinned one literal spelling at a time.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py -q`, in the clone at the target SHA | 48 passed |
| `evidence_check.py .` — unscoped, exit code read directly, never through a pipe | exit 0 · `total: 1385 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `correction_check.py --range origin/release/v0.12.2...31b320e5` | exit 0 · `no merge commit in 755629d..31b320e` |
| `correction_check.py --range <root commit>..31b320e5` over real history | exit 0 · 31 merges examined · `no correction marker was dropped at a merge` |
| `correction_check.py --range` against a ref that does not resolve | exit 2 · names the ref and the root, and examines nothing |
| `survivor_check.py --range 7073a881..cb7d1f4a --exempt …/survivors.md` | exit 0 · 1134 files at `cb7d1f4` against 37 removed sentences · `no removed wording is still standing` |
| Independent census over the three ledger files — verb, then the next date on the same line, run unbounded | `seal/ledger.md` 404 sites (401 cells, 3 prose, 190 rows); fragments 4 and 5 |
| The same census, run-length histogram for `seal/ledger.md` | `{0: 365, 1: 19, 2: 9, 3: 10, 5: 1}` — no run of four; one run of five at line 1172 |
| The same census, ten qualifier spellings with counts | `again` 19, `and re-executed` 5, `a third time` 4, `a fourth time` 3, `a fifth time` 2, `and re-stamped` 2, and one each of `and re-stamped again`, `and re-stamped a third time`, `and widened`, `and re-measured` — matching the code comment name for name |
| Shipped pattern against the independent census, per file | 404 / 4 / 5 against 404 / 4 / 5 — exact agreement, so nothing invented and nothing missed |
| Bound sweep with the shipped pattern over the three ledger files | `{0,0}` 373 · `{0,1}` 393 · `{0,2}` 402 · `{0,3}` 412 · `{0,4}` 412 · `{0,5}` 413 · `{0,6}` 413 · `{0,8}` 413 |
| Bound sweep over `seal/ledger.md` alone | 365 · 384 · 393 · 403 · 403 · 404 · 404 · 404 — stable, because the branch does not touch that file |
| The module's own `rows` and `markers` over `seal/ledger.md` | 732 rows parsed · 190 carrying a marker · 401 occurrences inside rows · 404 over the whole file text · 3 unwatched |
| Mutation: bound back to four, and to three | 1 failed each — pinned |
| Mutation: bound widened to six, and to twelve | 1 failed each — pinned |
| Mutation: dedup key back to `loss.row.key` | 1 failed — pinned |
| Mutation: dedup key to `loss.standing.key` | 48 passed — unpinned |
| Mutation: `max` → `min` on the parent choice | 1 failed — pinned |
| Mutation: `carried` walked in reversed order, so a tie falls to the last parent | 48 passed — unpinned |
| Mutation: `[ \t]`→`\s`; `[a-z-]`→`[a-z0-9-]`; `(?!\d)` dropped | 48 passed each — still unpinned at the bound of five |
| Constructed merge, both parents carrying one marker and the resolution dropping it | exit 1 · one entry · the FIRST parent named · `1 correction marker(s)` |
| The proposed case for finding 11, against the shipped code and against the reversed-order mutation | 1 passed, then 1 failed — seen red before it was written down |
| `seal/ledger.md` blob hash at `release/v0.12.2` and at the target SHA | `2f885a09` and `2f885a09` — byte-identical |
| The path-and-line form written into ledger row C1's Notes, in a throwaway copy | exit 2 · `1 old-format` · `OLD-FORMAT seal/ledger.md:1172`. The shipped wording exits 0 |
| the full suite, the repository-wide lint, the typecheck | not yet — `agent-contract` §2 leaves the broad gate to the agent whose definition assigns it, and `agents/warden.md` assigns it to nobody here |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/correction_check.py#MARKER` | round 1's 1 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py#examine` | round 1's 2 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py#_index` | round 1's 3 — fixed |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_skill_says_what_the_command_is_for_and_when_it_runs` | round 1's 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#gate` | round 1's 5 — deferred |
| round-1 | `CLAUDE.md#"## Repo rule — a change writes fragments, never the shared file"` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py#reverify` | round 1's 🟢 — not a defect |
| round-1 | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Where spec and implementation diverged* | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/correction_check.py#honoured` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/correction_check.py#standing` | round 1's 🟢 — not a defect |
| round-1 | `.github/workflows/hygiene.yml` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` | round 1's 🟢 — not a defect |
| round-2 | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md` §*Summary* | round 2's ⬜ — correction |
| round-2 | `skills/evidence-check/scripts/correction_check.py` module docstring | round 2's 🟢 — not a defect |
| round-2 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_key_two_result_rows_share_falls_through_to_the_anchors` | round 2's 🟢 — not a defect |
| round-2 | `seal/ledger.md` | round 2's 🟢 — not a defect |
| round-2 | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/survivors.md` | round 2's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Both bound fixes pin one literal spelling each, so an eleventh spelling at six words would be invisible with every case green | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*What that does not close* — already deferred in round 2; the issue is #469 and it is OPEN. Its histogram needs the correction recorded above | the repository owner |
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — already deferred in rounds 1 and 2; the issue is #468 and it is OPEN | the repository owner |
