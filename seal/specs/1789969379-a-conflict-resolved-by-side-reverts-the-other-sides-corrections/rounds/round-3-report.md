# Review round 3 — the verifying round of `1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections`

Target SHA `31b320e5f0e8742f1b76104d527173b186755dd8`, PR 467, base
`release/v0.12.2`. The range under review is `7073a881..cb7d1f4a`, three
commits, closing round 2's findings 6, 7 and 8.

Rounds 1 and 2 were read in full — both records and both reports. Their eight
numbered findings and one deferral are inherited; none is reopened.

## The three fixes do what their cells say

**Finding 6 — the bound and the census.** Verified with my own instrument,
built without reference to the shipped pattern: for every `\b(Corrected|Re-read)\b`
take the rest of its line, find the first date on it, and require the text in
between to be whitespace and lowercase words, with no upper bound on how many.

Every figure the fix states about `seal/ledger.md` is exact. 404 candidate
marker sites, 401 of them in table cells and 3 in prose, across 190 rows. The
run-length histogram is `{0: 365, 1: 19, 2: 9, 3: 10, 5: 1}` — **there is no
run of four**, and the single run of five is `Re-read and re-stamped a third
time` at `seal/ledger.md:1172`, exactly as claimed. The ten qualifier
spellings and their counts match the enumeration in the code comment name for
name: `again` 19, `and re-executed` 5, `a third time` 4, `a fourth time` 3,
`and re-stamped` 2, `a fifth time` 2, and one each of `and re-stamped again`,
`and re-stamped a third time`, `and widened` and `and re-measured`.

The pattern invents nothing. Its match count equals my independent census
exactly on all three ledger files — 404, 4 and 5 — so every match is a site
the census also found, and every site the census found is matched.

**Finding 7 — the dedup key.** `loss.standing.raw` is sound and it cannot
crash: `losses` skips a row whose survivor is `None`, so `loss.standing` is
never `None` where the tag is built. Restoring `loss.row.key` turns the new
case red.

**Finding 8 — the parent rule.** Swapping `max` for `min` turns the new case
red, which is what round 2 asked for.

**No seventh green-while-broken unit.** Each of the three new cases goes red
under the exact mutation it was written for, and the streak this work item
carried at every previous round and pass is broken here.

## Finding 9 — the fix's own commits made its three-file census stale

`skills/evidence-check/scripts/correction_check.py:223` states the bound
comparison as *411 across the three ledger files, against 412 at five*. At
this SHA the same sweep gives **412 and 413**.

Both figures are one low, and the cause is the fix range itself. `f58e350d`
wrote **Corrected again 2026-09-21 by review round 2, finding 6** into ledger
row C1 — one new marker with a one-word qualifier — into
`seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md`,
which is one of the three files the census counts. The number was true when
it was measured in the clone and false by the time the commit that carries it
landed beside the commit that changed the corpus.

The comparison the sentence exists to make survives: a bound of three reaches
412 and a bound of four reaches 412, so four still matched exactly what three
matched. Only the two absolute figures are wrong.

This is the third time a stated measurement in this work item is false about
the tree, and it is a new mechanism rather than a repeat of the first two.
Round 1's was a census over one side of the date; round 2's was a census taken
with the instrument under test; this one is a census whose corpus includes the
file the finding is recorded in. **Any figure spanning the ledger fragments is
invalidated by the act of writing a correction marker into a fragment**, and
the comment does not say so.

The figures over `seal/ledger.md` alone are stable — 403 at a bound of three,
403 at four, 404 at five — because that file is untouched by the branch. That
is the same argument over a corpus that cannot move under it.

## Finding 10 — "404 marker occurrences on 190 rows" is 401 on 190 rows

Six tracked files state that the file carries 404 marker occurrences on 190
rows. Measured through the module's own `rows` and `markers`: 190 rows carry a
marker, those rows carry **401** occurrences, and the remaining 3 are in the
file's prose.

The distinction is not cosmetic, because the check acts on the 401 and never
on the 3. `correction_check.py`'s own module docstring says so under *Markers
in prose are out of scope, by construction* — text outside a table row has no
row, so the survival test has nothing to decide there. A reader who takes
*404 on 190 rows* at face value believes the survival test watches three
markers it cannot see.

One of the six states both halves inside one sentence and so contradicts
itself: ledger row C1 reads *404 occurrences on 190 rows, 401 in cells and 3
in prose*. The code comment at `correction_check.py:189` is the only site that
gets it right.

The sites:

| Where | What it says |
|---|---|
| `skills/evidence-check/scripts/correction_check.py:47` | 404 marker occurrences on 190 rows |
| `tests/test_a_merge_cannot_silently_drop_a_correction.py:108` | 404 marker occurrences on 190 rows |
| `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md:3` | 404 occurrences on 190 rows, 401 in cells and 3 in prose |
| `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md:40` | 404 marker occurrences on 190 rows |
| `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md:121` | 404 occurrences on 190 rows, 39 qualified |
| `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/changelog.md:27` | 404 marker occurrences on 190 rows |

## Finding 11 — finding 8's fix pinned half of the sentence it was about

Ledger row C9's Notes and `examine`'s comment state one rule in one sentence:
*the parent named is the one that lost the most occurrences … ties fall to the
first parent, the side the person resolving had checked out.*

Round 2's finding 8 was that no case held that rule, and its fix planted
`test_the_parent_named_is_the_one_that_lost_the_most`. That case pins the
first clause. Nothing pins the second.

**The tie is the common path, not the rare one.** Round 1's finding 2 rests on
the observation that every marker older than the fork is carried by both
parents — so both parents lose the same count of it, and the parent choice is
a tie in the ordinary case. The case that exists exercises the uneven case,
where one side carries the marker in two cells.

Executed: a constructed merge where both parents carry one marker and the
resolution drops it exits 1, prints one entry, and names the first parent. So
the code does what C9 says. What is missing is anything that would notice if
it stopped: rebuilding `carried` in any other order — a sort, a set, a
reversed walk — changes the SHA a reader is sent to open and leaves all 48
cases green. Verified by mutation.

`agent-contract` §14 is the rule under it. The parent SHA is a line a person
reads and acts on, and it is the line that decides which hunk they open.

## Corrections

**The dedup key's alternative is unpinned, and `Row`'s docstring has not
caught up.** Replacing `loss.standing.raw` with `loss.standing.key` leaves all
48 cases green. The shipped choice is the right one and I am not asking for it
to change: `_index` drops a shared first cell from `by_key` but the anchor
route can still reach two different surviving rows that share one, and keying
on the first cell would collapse their losses into a single report.
`seal/ledger.md` carries 123 rows sharing a first cell today, so the argument
is not hypothetical. `Row`'s docstring still says it holds *the three things
it is judged by* and names `key`, `anchors` and `markers`; `raw` is now a
fourth and it is load-bearing.

**#469's own measurement table mixes two corpora.** Its histogram reads 373
runs of 0, 19 of 1, 9 of 2, 10 of 3, none of 4 and 1 of 5. The 373 is the
three-file count and the 19 is the `seal/ledger.md`-only count, so the table
sums to 412 — which is neither file set's total. Over the three files it is
`{0: 373, 1: 20, 2: 9, 3: 10, 5: 1}` = 413; over `seal/ledger.md` alone it is
`{0: 365, 1: 19, 2: 9, 3: 10, 5: 1}` = 404. The issue is the durable home for
this work, and it is the table the next session will build the corpus walk
from. Its conclusion — no run of four — holds on either corpus.

**Both deferrals are named without their numbers.** `overview.md` §*Not done*
says *Answerer: the repository owner, as an issue opened from this pull
request* and §*What that does not close* says *Answerer: the repository owner,
as an issue*. #468 and #469 are both open. The round records carry the
numbers, so a reader who has the records can reach them; a reader who has only
the work item after the release cannot.

**Round 2's four unpinned `MARKER` directions are still unpinned at the new
bound.** Widening the whitespace class to `\s`, opening the word class to
digits, and dropping the `(?!\d)` boundary each leave 48 green. Round 2
recorded these as a correction with the grounds that none is reachable through
`Row.markers`, which reads one table line at a time. I re-ran them at the
bound of five and the grounds still hold. Carried forward, not re-opened.

## On the two open issues

**#468 is correctly scoped.** It names the gap as the gate's arm list being
maintained by hand rather than as one missing arm, and it names the wider
subject — nothing holds the gate's list against the workflow's. That is the
part that stops the seventh arm arriving the same way.

**#469 is correctly scoped.** It refuses both wrong answers explicitly —
removing the bound, and pinning another literal spelling — and it asks for the
property rather than the value. Its one defect is the histogram above.

Neither is wrongly scoped, and neither is reopened here.

## What this round did not run

The full suite, the repository-wide lint and the typecheck. `agent-contract`
§2 leaves the broad gate to the agent whose definition assigns it, and
`agents/warden.md` assigns it to nobody here. With this report's findings
answered, **the gate has come due** — what comes due is the sealer's spawn,
not a run for the session reading this.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | The bound comparison reads 411 against 412; at this SHA it is 412 against 413, because `f58e350d` wrote a marker into one of the three files the census counts | `skills/evidence-check/scripts/correction_check.py#MARKER` | open | Executed: the shipped pattern swept over bounds 0-8 across the three ledger files gives 373, 393, 402, 412, 412, 413, 413, 413, 413. The comparison the sentence makes still holds — three and four both reach 412 — and only the two absolute figures are wrong. The `seal/ledger.md`-only figures are stable because the branch does not touch that file |
| 10 | Six tracked files say the file carries 404 marker occurrences on 190 rows; 401 are on those rows and 3 are in prose the survival test never acts on | `skills/evidence-check/scripts/correction_check.py` module docstring | open | Executed through the module's own `rows` and `markers`: 732 rows parsed, 190 carrying a marker, 401 occurrences inside rows, 404 over the whole file text. The module docstring's own §*Markers in prose are out of scope, by construction* is the rule that makes the 3 unwatched. Ledger row C1 states both halves in one sentence and contradicts itself |
| 11 | Finding 8's fix pins the first clause of C9's parent rule and not the second; ties fall to the first parent, nothing holds it, and the tie is the common path | `skills/evidence-check/scripts/correction_check.py#examine` | open | Executed: a constructed tie exits 1, prints one entry and names the first parent, so the code does what C9 says. Mutation: rebuilding `carried` in reversed order leaves 48 of 48 green. `agent-contract` §14 — the parent SHA is the line that decides which hunk a reader opens. A proposed case was driven green on the shipped code and red on that mutation before it was written down |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Both bound fixes pin one literal spelling each, so an eleventh spelling at six words would be invisible with every case green | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*What that does not close* — already deferred in round 2; the issue is #469 and it is OPEN. Its histogram needs the correction recorded above | the repository owner |
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — already deferred in rounds 1 and 2; the issue is #468 and it is OPEN | the repository owner |

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

Needs a fix: yes — findings 9, 10 and 11. Finding 9 is the one that matters: the bound comparison is arithmetically false at this SHA, and it went false because the fix range's own commit wrote a marker into a file its census counts.

Loses a record or crashes: no — nothing in this range writes to a ledger, `seal/ledger.md` is byte-identical to the base across the whole branch, no run crashed, and the new dedup key cannot dereference `None` because `losses` skips a row whose survivor did not stand. All three findings are false or unheld statements; none of them drops a record.

## Proof block

Opened and read in full:

- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/rounds/round-1.md`
- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/rounds/round-2.md`
- `skills/evidence-check/scripts/correction_check.py` — the module docstring, `MARKER` and its census comment, `markers`, `Row`, `_index`, `standing`, `Loss`, `losses`, `marker_counts`, `honoured`, `parents`, `ledger_listing`, `examine`, `report`
- `tests/test_a_merge_cannot_silently_drop_a_correction.py` — the helpers `ledger`, `run`, `merged`, `check`, and the three cases the range adds
- `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` — rows C1 through C9
- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` — §*Not verified*, §*Not done*, §*Where spec and implementation diverged*, §*What that does not close*
- `git diff 7073a881..cb7d1f4a` in full, all nine files
- `bin/test`
- issue #468 and issue #469, both bodies in full

Read in part, by coordinate:

- `seal/ledger.md` — line 1172, and the whole file through `grep`, `sed` and the two census scripts. Never opened whole; 2364 lines and 1.07 MB
- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md`, `plan.md`, `questions.md`, `changelog.md`, `survivors.md` — the hunks the range touches, and the sites the `190 rows` sweep named
- `.github/workflows/hygiene.yml` — the leg's comment, the line the range changes
- `skills/evidence-check/SKILL.md` — searched for the census figures; it carries none

Carried from rounds 1 and 2 without re-deriving: the coordinates of the eight
closed findings, the three survivor exemptions, and the reach measurements for
the ambiguity guards. Every verdict in the table above is this round's own.

All work ran in a `git clone --no-local` of the repository at the target SHA.
Probes, their virtual environment and the clone are deleted. Nothing was
committed, nothing was fixed, and the only file written outside the clone is
this report.
