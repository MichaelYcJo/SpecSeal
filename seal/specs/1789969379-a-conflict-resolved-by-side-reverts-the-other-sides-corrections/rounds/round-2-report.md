# Round 2 — review report (the verifying round)

| Field | Value |
|---|---|
| Work item | `1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections` (#424) |
| Branch | `fix/a-conflict-resolved-by-side-reverts-the-other-sides-corrections` |
| Base | `release/v0.12.2` |
| Target SHA | `02db392915e1f2bf9814a6c5622ab96b8ce58e8f` |
| Round | 2 — verifying, over the fix range `27535c8f..d9a2e57d`, 5 commits |
| Reviewed in | a `git clone --no-local` at the target SHA, under the session scratchpad |

Round 1's four `fixed` closures all do what their cells say, and the fifth is
carried forward as deferred. I re-ran every mutation round 1 named and each
goes red; the three pins the builder claims for the qualifier bound are real;
the skill case now fails for its own subject; and `seal/ledger.md` is
byte-identical to the base across the whole branch.

Three things are open, and two of them are the same defect one shape over.

## 🟡 6 — the file carries a tenth qualifier spelling, and the census that set the bound could not see it

`skills/evidence-check/scripts/correction_check.py#MARKER`

The bound is four lowercase words. `seal/ledger.md:1172` spells a marker with
**five**:

```
**Re-read and re-stamped a third time 2026-09-08**, by work item …
```

Executed: `cc.markers("Re-read and re-stamped a third time 2026-09-08.")`
returns `{}`. Put that sentence on a row, revert it at a constructed merge,
and the check answers `no correction marker was dropped at a merge`, exit 0.
That is round 1's finding 1 reproducing, in a spelling this repository has
actually written.

**Three statements are false about the tree because of it**, and one of them
is a ledger row:

| Statement | What it says | What the file carries |
|---|---|---|
| `seal/ledger/1789969379-…md` row C1, Notes | *The check now sees 403 of 403* | 403 of **404** |
| `correction_check.py#MARKER`, the comment | *the longest the tree carries is three words* | five |
| `spec.md` §*What the markers actually look like*, the CORRECTED table | *markers the file actually carries · 403* | 404 |

**Why it was missed, which is the part that matters.** The census was taken
with the widened pattern itself, so a spelling the widened pattern cannot see
was invisible to the measurement that justified it. That is the same circle
round 1's finding 1 described in the frame — *the frame counted the spellings
after the date and stated it with a count, which made "the variation lives
after the date" read as measured when only one side had been looked at.* The
repair for a bound is to measure with the run unbounded and derive the bound
from what comes back, never to count with the bound under test.

**Not 🔴.** Line 1172 is prose, not a table row, and `rows()` keeps only lines
that open with `|` — so `losses()` never reads it and no row of the tree is
invisible today. What ships is a false ledger fact on a branch whose subject
is ledger truth, and a bound one word short of what this repository's own
editors write.

**The measured answer is `{0,5}`, not a guess.** Executed over `seal/ledger.md`
and both live fragments: `{0,4}` matches 411, `{0,5}` matches 412, and `{0,6}`
and `{0,8}` also match 412 — so five is the true longest and `{0,5}` adds
exactly the one genuine spelling and invents nothing. `{0,5}` also leaves both
needles of `test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier` red,
where `{0,6}` would turn *Re-read once the base had moved past …* green. The
paste-ready fix below is `{0,5}` with the three facts corrected.

## 🟡 7 — finding 2's fix is keyed on the first cell, which is the identity a correction changes

`skills/evidence-check/scripts/correction_check.py#examine`

The new grouping is `tag = (loss.row.key, loss.marker)`, and `loss.row` is the
row **as that parent carried it**. Where the two parents spell the first cell
differently, the two tags differ and one lost marker is reported twice again.

Executed, through the CLI, against a constructed merge — base carries the row
uncorrected, one parent corrects the claim cell *and* adds the marker, the
other adds the marker alone, and the resolution drops it:

```
seal/ledger.md
  lost        Corrected 2026-09-21
  row         R1 · the gate resolves the base CI will read
seal/ledger.md
  lost        Corrected 2026-09-21
  row         R1 · the gate resolves the base

2 correction marker(s) a parent carried are gone from the merge result
```

One row, one marker, two hunks to open and a closing count of two — which is
round 1's finding 2 verbatim.

**This is not an exotic shape; it is the shape the anchor route was built
for.** Ledger row C4's Notes says so in the branch's own words: *the anchors
are for the case where the claim itself is what was corrected.* The identity
the design already knows can move under a correction is the identity the dedup
was keyed on.

**Not 🔴**, because `phase-1.md` records that all three of #424's own
corrections landed in a cell after the first, and I measured the tree: 0 of
the 190 marked rows in `seal/ledger.md` share a first cell. The over-report
inflates a number rather than hiding a loss.

The surviving row is what every parent's loss converges on, so it is the
identity that does not move. `(loss.standing.raw, loss.marker)` is the fix.

## 🟡 8 — the rule that picks which parent to name is documented and pinned by nothing

`skills/evidence-check/scripts/correction_check.py#examine`

The fix replaced *print both parents* with *print the one that lost the most
occurrences, ties to the first parent*. Ledger row C9's Notes states that rule
and `examine`'s comment argues for it — *that is the side whose text most
needs reading*.

Executed: swapping `max` for `min` in that line leaves all 45 cases green. The
rule that decides which hunk a reader is sent to is held by nothing, and
`agent-contract` §14 is the rule it is owed — *a fix that changes what a
person sees documents it and pins it, in the same commit.*

Weakest of the three: the behaviour is right today, and C9's **Claim** cell
(one report, and the closing count says one) is genuinely pinned. It is the
Notes' rule that has no case.

## ⬜ four directions of `MARKER` that no case holds

`skills/evidence-check/scripts/correction_check.py#MARKER`

You asked whether the bound's three pins can all pass while the pattern is
wrong in a fourth direction. They can. All four of these mutations leave 45 of
45 green:

| Mutation | What it would allow |
|---|---|
| `[ \t]` → `\s` | the qualifier and the date to cross a newline |
| `[a-z-]` → `[a-z0-9-]` | a qualifier word carrying a digit |
| `(?!\d)` removed | `2026-09-055` read as `2026-09-05` |
| `\b` removed | the verb matched inside a longer word |

None is reachable through `Row.markers`, which reads one line of a table at a
time, and neither `[ \t]` nor `\s` can cross a `|`. Raised as a correction
because the bound's three pins were presented as holding the axis, and the
axis has more directions than three.

## ⬜ `plan.md`'s Summary keeps the superseded sentence with no correction beside it

`seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md:14`

The file carries a **CORRECTED at round 1, finding 1** block under *Technical
context*, which is the convention. The Summary's *matches on the leading verb
and date rather than on the sentence* stands twenty lines above it with
nothing pointing at it. The sentence is not false — the verb still leads and
the identity is still the verb and the date — so this is a correction and not
a finding. A reader who stops at the Summary meets the pre-round-1 framing.

# Verification — the five closures, checked rather than accepted

**Finding 1, the pattern.** Verified against the real file, not the fixtures.
The shipped `MARKER` matches 403 occurrences in `seal/ledger.md`, and the
qualifier histogram is exactly the nine spellings the builder reports, with
the counts he reports: `again` ×19, `and re-executed` ×5, `a third time` ×4,
`a fourth time` ×3, `and re-stamped` ×2, `a fifth time` ×2, and one each of
`and re-stamped again`, `and widened`, `and re-measured`. **No invented
match**: every one of the 403 is either a bare `<verb> <date>` or one of those
nine. The three pins are real — narrowing the bound to zero turns 3 cases red,
widening it to twelve turns 1 red, opening the lowercase gate turns 1 red.
Finding 6 above is the tenth spelling, which is a new finding rather than this
closure failing.

**Finding 1, the class.** Nine is the whole of it. `git grep` over the tree
for *leading verb*, *at least three spelling*, *353* and *365* returns nothing
uncorrected outside the round-1 records themselves, except the `plan.md`
Summary line raised as a correction above. The six round 1 enumerated plus
`changelog.md`, `overview.md` and the two test docstrings is the full set.

**Finding 2.** Closed for the shape it was reported in: both parents carrying
the same first cell now produce one entry and `1 correction marker(s)`, and
restoring the per-parent append turns that case red. Finding 7 is the shape it
does not reach.

**Finding 3.** The guard is on both sides of both identities. Removing it from
`_index` turns `test_a_row_ambiguous_on_both_identities_is_not_identified`
red; removing the `ambiguous_keys` test from `standing` turns
`test_two_rows_sharing_a_first_cell_decide_nothing_either` red. Measured for
reach: of the 190 marked rows in `seal/ledger.md`, 0 have a duplicated first
cell, 3 carry no anchors, and **0 are silenced on both identities** — so the
new guards refuse no row the check should have named, in this tree.

**Finding 3, the sub-point the builder answered rather than applied.** The
builder is right and round 1 was wrong. In that fixture the parent's row is
unambiguous, exactly one result row carries its anchors, and that row no
longer carries the marker — the correction *was* dropped. Round 1 asked for
silence there, and its own paste-ready `standing` does not produce silence:
the shipped `standing` and `_index` are round 1's patch verbatim, so round 1's
`== []` would have been red against round 1's own code. Suppressing that
report would refuse a row that can be named, which is the opposite of what the
guard is for. The split into two cases is the repair.

**Finding 4.** Genuinely fixed, and I drove it red. Deleting the whole *Its
moment is the pull request* paragraph from `skills/evidence-check/SKILL.md`
now fails the case; deleting the later *Migrating a pre-anchor ledger* mention
as well still fails it; restoring the file passes. Worth one sentence for the
next editor: the section split works because `read()` collapses all whitespace
to single spaces, which is what turns the line-anchored `\n## ` into the
`" ## "` the case splits on. A `read()` that stopped collapsing would silently
widen the case back to the whole file.

**The ledger is untouched.** `git diff --stat release/v0.12.2..HEAD --
seal/ledger.md` prints nothing across the whole branch, not just the fix
range. No `--reverify` in the pass wrote to it.

**The three survivor exemptions.** All three hold. The `spec.md` cell is
corrected in place under a CORRECTED block, which is what keeps the correction
auditable; the `correction_check.py` clause about three spellings after the
date is still true and is the argument for the half of the rule it sits under,
and round 1 falsified the wider inference rather than this clause; the
`phases/phase-1.md` line asserts a past state, which is what a phase record is
for. `survivor-check` over the fix range exits 0 with `every survivor is
excused by a row above (3)`.

**#468.** Carried forward unchanged. The branch's own range still holds no
merge, so its seal and its leg still agree.

**CORRECTED by the orchestrator when this report was recorded.** This
paragraph and the two rows below said the issue *still does not exist*. It
does: #468 was opened between round 1 and this round, and `gh issue view 468`
reports it OPEN. The sentence was carried forward from round 1's report, where
it was true, without being re-checked — which is the class this whole work
item is about.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 6 | The file carries a tenth qualifier spelling of five words that the bound cannot see, and the census that set the bound was taken with the bound under test | `skills/evidence-check/scripts/correction_check.py#MARKER` | open | Executed: `markers()` returns `{}` for the sentence at `seal/ledger.md:1172`, and a constructed merge reverting it exits 0 · silent. Measured: `{0,4}` 411 matches over the three ledger files, `{0,5}` 412, `{0,6}` and `{0,8}` also 412. Three statements false about the tree, one of them ledger row C1. Not 🔴 — line 1172 is prose, so no row is invisible today |
| 7 | One lost marker is reported twice again where the two parents spell the first cell differently — the dedup is keyed on the identity a correction changes | `skills/evidence-check/scripts/correction_check.py#examine` | open | Executed through the CLI: one row, one marker, two entries, `2 correction marker(s)`. Ledger row C4's Notes says the anchors exist for exactly that case. Not 🔴 — measured, 0 of 190 marked rows share a first cell, so it inflates a number rather than hiding a loss |
| 8 | The rule choosing which parent to name is documented in ledger row C9 and in `examine`'s comment, and no case holds it | `skills/evidence-check/scripts/correction_check.py#examine` | open | Executed: `max` swapped for `min` leaves 45 of 45 green. `agent-contract` §14. C9's Claim cell is pinned; it is the Notes' rule that is not |
| ⬜ | Four directions of `MARKER` that no case holds — `[ \t]`→`\s`, `[a-z-]`→`[a-z0-9-]`, `(?!\d)` dropped, `\b` dropped | `skills/evidence-check/scripts/correction_check.py#MARKER` | correction | Executed: each mutation leaves 45 of 45 green. None is reachable through `Row.markers`, which reads one table line at a time, and neither character class can cross a `\|` |
| ⬜ | `plan.md`'s Summary keeps the pre-round-1 sentence with no correction beside it, twenty lines above the CORRECTED block | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md` §*Summary* | correction | Read. The sentence is not false, so this is paperwork rather than a defect: a reader who stops at the Summary meets the superseded framing |
| 🟢 | Finding 1's pattern — the widened `MARKER` sees the nine spellings the real file carries and invents none | `skills/evidence-check/scripts/correction_check.py#MARKER` | not a defect | Executed against `seal/ledger.md` itself, not the fixtures: 403 matches, histogram exactly the nine reported spellings with the reported counts, every match a bare `<verb> <date>` or one of the nine. The three pins each turn their own case red |
| 🟢 | Finding 1's class — nine statements, and nine is the whole of it | `skills/evidence-check/scripts/correction_check.py` module docstring | not a defect | `git grep` for *leading verb*, *at least three spelling*, *353*, *365* over the whole tree: nothing uncorrected outside the round-1 records, bar the `plan.md` Summary raised as a correction |
| 🟢 | Finding 2's fix closes the shape it was reported in | `skills/evidence-check/scripts/correction_check.py#examine` | not a defect | Executed: one entry and `1 correction marker(s)` where both parents carry the same first cell; restoring the per-parent append turns that case red |
| 🟢 | Finding 3's fix — both identities guarded on both sides | `skills/evidence-check/scripts/correction_check.py#_index` | not a defect | Executed: either guard removed turns its own case red. Measured for reach — 190 marked rows, 0 with a duplicated first cell, 3 with no anchors, 0 silenced on both identities |
| 🟢 | Finding 3's sub-point — the split is the repair and round 1's reading was wrong | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_key_two_result_rows_share_falls_through_to_the_anchors` | not a defect | Read: the shipped `standing` and `_index` are round 1's paste-ready patch verbatim, so round 1's own `== []` would have been red against round 1's own code. The anchor route names one surviving row and that row lost the marker — a real loss, and asserting silence would suppress it |
| 🟢 | Finding 4's fix — the skill case now fails for its own subject | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_skill_says_what_the_command_is_for_and_when_it_runs` | not a defect | Executed: deleting the *when it runs* paragraph fails the case; also removing the later section's mention still fails it; restoring passes. The section split works because `read()` collapses whitespace, turning `\n## ` into the `" ## "` it splits on |
| 🟢 | `seal/ledger.md` is byte-identical to the base across the whole branch | `seal/ledger.md` | not a defect | Executed: `git diff --stat release/v0.12.2..HEAD -- seal/ledger.md` prints nothing. No `--reverify` in the pass wrote to it |
| 🟢 | The three survivor exemptions are each justified | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/survivors.md` | not a defect | Executed: `survivor-check` over the fix range exits 0, `every survivor is excused by a row above (3)`. Read each: a `spec.md` cell corrected in place under a CORRECTED block, a docstring clause round 1 did not falsify, and a phase record asserting a past state |
| ⬜ | `broad_gate.py` does not mirror the new hygiene arm | `skills/verify/scripts/broad_gate.py#gate` | deferred #468 | Carried forward from round 1. The branch's own range still holds no merge, so its seal and its leg agree. The issue exists: #468, OPEN — the report's *still does not exist* was carried from round 1 unchecked and is corrected here |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py -q`, in the clone at the target SHA | 45 passed |
| `python3 skills/evidence-check/scripts/evidence_check.py .` — unscoped, exit code read directly | exit 0 · `total: 1385 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `correction_check.py --range origin/release/v0.12.2...HEAD` | exit 0 · `no merge commit in 755629d..02db392` |
| `correction_check.py --range <root commit>..HEAD` over real history, 31 merges | exit 0 · `no correction marker was dropped at a merge` |
| `survivor_check.py --range 27535c8f..d9a2e57d --exempt …/survivors.md` | exit 0 · 39 sentences removed, 3 survivors, `every survivor is excused by a row above (3)` |
| `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py -q` | 23 passed |
| Marker census over the real `seal/ledger.md` with the shipped pattern | 403 matches · nine qualifier spellings, counts exactly as reported · no invented match |
| Census with the qualifier run unbounded (`{0,10}`) over all three ledger files | 404 in `seal/ledger.md` — one more than the shipped pattern sees, a five-word qualifier at line 1172 |
| Bound sweep over the three ledger files | `{0,4}` 411 · `{0,5}` 412 · `{0,6}` 412 · `{0,8}` 412 — five words is the true longest |
| Constructed merge reverting a five-word-qualifier marker | exit 0 · `no correction marker was dropped` — silent |
| Constructed merge where one parent also corrected the claim cell | exit 1 · one marker printed twice · `2 correction marker(s)` |
| Mutation: bound narrowed to `{0,0}` | 3 failed — pinned |
| Mutation: bound widened to `{0,12}` | 1 failed — pinned |
| Mutation: lowercase gate opened to `[A-Za-z]` | 1 failed — pinned |
| Mutation: `[ \t]`→`\s`; `[a-z-]`→`[a-z0-9-]`; `(?!\d)` dropped; `\b` dropped | 45 passed each — four unpinned directions |
| Mutation: `_index`'s key guard removed | 1 failed — pinned |
| Mutation: `standing`'s `ambiguous_keys` test removed | 1 failed — pinned |
| Mutation: per-parent append restored in `examine` | 1 failed — pinned |
| Mutation: `max` → `min` on the parent choice | 45 passed — unpinned |
| Mutation: the skill's *when it runs* paragraph deleted, then the later section's mention too | 1 failed both times; restored, 1 passed |
| The three paste-ready fixes applied in the clone, with their cases | before: 2 failed (findings 6 and 7) · after the two one-line changes: 48 passed · with `max`→`min`: only finding 8's case red |
| Ambiguity census over the three ledger files | 190 marked rows · 0 with a duplicated first cell · 3 with no anchors · 0 silenced on both identities |
| `git diff --stat release/v0.12.2..HEAD -- seal/ledger.md` | empty |
| the full suite, the repository-wide lint, the typecheck | not yet — `agent-contract` §2 leaves the broad gate to the sealer, and `agents/warden.md` assigns it to nobody here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — already deferred in round 1; the issue it names is #468 and it is OPEN | the repository owner |

## Paste-ready fixes

Finding 6 — the bound, measured rather than guessed:

```python
# Four words was the bound and it was one short. The census that set it was
# taken WITH the widened pattern, so a spelling the pattern could not see was
# invisible to the measurement justifying it -- the same circle round 1 found
# in the frame, which counted only the spellings after the date. Re-measured
# with the run unbounded: `seal/ledger.md:1172` spells a marker `Re-read and
# re-stamped a third time <date>`, five lowercase words. Over the shared file
# and both live fragments: {0,4} matches 411, {0,5} matches 412, and {0,6}
# and {0,8} also match 412 -- five is the longest the tree carries, and five
# is therefore the bound. {0,6} would buy nothing and would turn
# test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier green.
VERBS = ("Corrected", "Re-read")
MARKER = re.compile(
    r"\b(" + "|".join(VERBS) + r")"
    r"(?:[ \t]+[a-z][a-z-]*){0,5}"
    r"[ \t]+(\d{4}-\d{2}-\d{2})(?!\d)"
)
```

```python
def test_the_longest_qualifier_the_tree_carries_is_seen(tmp_path):
    """`seal/ledger.md:1172` spells five lowercase words between the verb and
    the date, and the bound was four -- so the file's own longest spelling was
    invisible to the check watching that file. Round 1's finding 1, one
    spelling further out, and found the same way it was: by measuring with the
    run unbounded instead of with the bound under test."""
    assert cc.markers("Re-read and re-stamped a third time 2026-09-08.") == {
        ("Re-read", "2026-09-08"): 1
    }
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. | none |"
    corrected = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read and re-stamped a third time 2026-09-08. | none |"
    )
    root, start, head = merged(
        tmp_path, ledger(row), ledger(corrected), ledger(row), ledger(row)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert "Re-read 2026-09-08" in out, out
```

```text
correction_check.py#MARKER, the comment
    "the longest the tree carries is three words; the bound is four"
  -> "the longest the tree carries is five words -- `Re-read and re-stamped a
     third time <date>` at seal/ledger.md:1172 -- and the bound is five.
     Measured with the run UNBOUNDED, because a census taken with the bound
     under test cannot see what the bound excludes."

  and in the census paragraph above it:
    "403 marker occurrences on 190 rows ... sees 365"
  -> 404 occurrences, of which 401 are on the 190 table rows and 3 are prose;
     a `<verb> <date>` pattern sees 365, a four-word bound 403, a five-word
     bound 404.

seal/ledger/1789969379-...md row C1, Notes cell
    "The check now sees 403 of 403 and invents no qualifier the file does not
     carry"
  -> "sees 404 of 404" once the bound is five. The count came from the
     pattern itself, which is why it read 403 both times. Re-stamp the row
     with `evidence-check --reverify` and name the new case in Verified
     behavior.

spec.md §*What the markers actually look like*, the CORRECTED table
    "markers the file actually carries | 403"
  -> 404, with a line saying the 403 was measured with the bound under test
     and the 404 with the run unbounded.
```

Finding 7 — key the dedup on the row that did not move:

```python
                    # The SURVIVING row, not the parent's, because the
                    # parent's first cell is exactly what a correction
                    # changes -- which is why the anchor route exists at all
                    # (ledger row C4). Keyed on the parent's key, two parents
                    # that spell the first cell differently produce two tags
                    # for one lost marker, and the closing line says two.
                    # Every parent's loss converges on the same result row,
                    # so that row's text is the identity that cannot move.
                    tag = (loss.standing.raw, loss.marker)
                    carried.setdefault(tag, {}).setdefault(parent, []).append(loss)
```

```python
def test_a_marker_both_parents_carried_is_reported_once_across_a_rewritten_key(
    tmp_path,
):
    """Finding 2 one shape over. One parent corrected the claim cell while
    adding the marker and the other only added it; the resolution dropped it.
    Keyed on the parent's first cell, that is two tags for one lost marker and
    a closing count of two -- a reader sent to open two hunks when there is
    one, which is the defect finding 2 reported."""
    base = "| R1 · the gate resolves the base | `a/b.py#f@11111111` | Read. | none |"
    ours = (
        "| R1 · the gate resolves the base CI will read | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | none |"
    )
    theirs = (
        "| R1 · the gate resolves the base | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | none |"
    )
    got = "| R1 · the gate resolves the base | `a/b.py#f@11111111` | Read. | none |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert out.count("lost        Corrected 2026-09-21") == 1, out
    assert "1 correction marker(s)" in out, out
```

Finding 8 — pin the parent the report names:

```python
def test_the_parent_named_is_the_one_that_lost_the_most(tmp_path):
    """`examine` picks the parent that lost the most occurrences of the marker,
    because that is the side whose text most needs reading, and ledger row C9
    states it. Nothing held it: swapping `max` for `min` left the whole module
    green, and the line a reader acts on is the one that decides which hunk
    they open (`agent-contract` §14).

    `ours` carries the marker in two cells and `theirs` in one, so the two
    sides lose different amounts of the same marker and the choice is visible.
    """
    base = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    ours = (
        "| R1 · a claim | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | Corrected 2026-09-21. |"
    )
    theirs = "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | none |"
    got = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    ours_sha = run(root, "rev-parse", head + "^1").stdout.strip()
    assert f"from parent {ours_sha[:7]}" in out, out
```

**All three fixes above were executed before this report was written**, in the
clone at the target SHA. The two new cases for findings 6 and 7 are red
against the code as it stands and green with the two one-line changes applied,
and the two changes together leave all 45 existing cases green — 48 passed.
Finding 8's case is green either way, because the behaviour it pins is already
right; `agent-contract` §15 is satisfied by the mutation instead, and it was
seen red with `max` swapped for `min` while the other 47 stayed green.

Needs a fix: yes — findings 6, 7 and 8. Finding 6 is the one that matters: the
census that set the qualifier bound was taken with the bound under test, so
the file's own longest spelling was invisible to it, and three statements
including a ledger row say the check sees every marker the file carries.

Loses a record or crashes: no — nothing here writes to a ledger, nothing
crashed in any run, and no record leaves the root that would not have left
without this branch. Findings 6 and 7 under-detect and over-report; the branch
is still strictly better than the tree without it.

# Proof block — what I opened

**Executed** (in a `git clone --no-local` at `02db392`, venv built by `bin/test`)

- `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py` — 45 passed
- `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py` — 23 passed
- `skills/evidence-check/scripts/evidence_check.py .` — exit 0
- `skills/evidence-check/scripts/correction_check.py --range …` — three ranges, exits 0
- `skills/code-review/scripts/survivor_check.py --range 27535c8f..d9a2e57d` — exit 0
- eleven source mutations and two document mutations, each restored
- one probe module, two constructed merges, deleted before handover
- four census scripts over `seal/ledger.md` and both live fragments

**Read**

- `seal/specs/1789969379-…/rounds/round-1.md`, `rounds/round-1-report.md`
- `seal/specs/1789969379-…/survivors.md`, `spec.md`, `plan.md`, `questions.md`
- `seal/ledger/1789969379-…md` (whole), `seal/ledger.md` (by `grep` and `sed -n` only)
- `skills/evidence-check/scripts/correction_check.py`, `skills/evidence-check/SKILL.md`
- `tests/test_a_merge_cannot_silently_drop_a_correction.py`
- `bin/test`, `bin/survivor-check`
- `git diff 27535c8f..d9a2e57d` in full, across all ten files

**Unverified**

- the broad gate — not run, and not mine to run. Answerer: the sealer.
