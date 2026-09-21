# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — review round 2

| Field | Value |
|---|---|
| Target SHA | 02db392915e1f2bf9814a6c5622ab96b8ce58e8f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 467 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `7073a881d89cff5d1caadf4e04dd07cbe20d8077..cb7d1f4a32bdb0e26a11491cf0647ab552f2e5b6`, 3 commits |
| Contract changes | none |
| New units | test_the_longest_qualifier_the_tree_carries_is_seen (depth 1); test_a_marker_both_parents_carried_is_reported_once_across_a_rewritten_key (depth 1); test_the_parent_named_is_the_one_that_lost_the_most (depth 1) |
| Needs a fix | yes — findings 6, 7 and 8. Finding 6 is the one that matters: the census that set the qualifier bound was taken with the bound under test, so the file's own longest spelling was invisible to it, and three statements including a ledger row say the check sees every marker the file carries. |
| Loses a record or crashes | no — nothing here writes to a ledger, nothing crashed in any run, and no record leaves the root that would not have left without this branch. Findings 6 and 7 under-detect and over-report; the branch is still strictly better than the tree without it. |
<!-- New units: .github/workflows/hygiene.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 2, the verifying round: round 1's fixes, opened by somebody. The
reviewer inherited round 1's committed record, was told its five verdicts are
closed and not to be reopened unless a fix does not do what its cell says, and
was given the range — `27535c8f..d9a2e57d`, five commits.

What each fix CLAIMS was listed per finding so the round could check the claim
rather than rediscover the finding, and two of those claims were named as
things to verify against the REAL `seal/ledger.md` rather than against the
fixtures: that the widened pattern sees 403 of 403 and invents no qualifier,
and that the class of the false statement is nine and nine is the whole of it.

Four judgments were handed over rather than stated. Whether the builder was
right to ANSWER a sub-point of round 1's paste-ready fix instead of applying
it — it argued the case would have been red against round 1's own patch, so
either round 1's reading was wrong or the code bends the wrong way. Whether a
sixth green-while-broken unit exists, since this work item had produced one at
every round and at every pass, including the builder's own first needle.
Whether `seal/ledger.md` is untouched across the whole branch, which is the
one thing a work item about losing ledger corrections must get right about
itself. And whether each of the three survivor exemptions holds.

On the reviewer's own account: whether the widened `MARKER` can match
something nobody would write in a ledger this repository will actually have;
whether the bound's three pins can all pass while the pattern is wrong in a
fourth direction; and whether the two new ambiguity guards can refuse a row
the check should have named.

`evidence_check.py .` unscoped, `correction-check` against real history as
well as fixtures, exit codes read directly. `seal/ledger.md` was declared
off-limits to a whole read. The report's verdict-table shape was spelled out
after two earlier rounds in this session were sent back by the generator for
an unkeyed row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 6 | The file carries a tenth qualifier spelling of five words that the bound cannot see, and the census that set the bound was taken with the bound under test | `skills/evidence-check/scripts/correction_check.py#MARKER` | **fixed** `444fa3ae` | fixed at 444fa3ae — the bound and the census method, f58e350d the statements — fourteen across nine files, not the three the round named; Executed: `markers()` returns `{}` for the sentence at `seal/ledger.md:1172`, and a constructed merge reverting it exits 0 · silent. Measured: `{0,4}` 411 matches over the three ledger files, `{0,5}` 412, `{0,6}` and `{0,8}` also 412. Three statements false about the tree, one of them ledger row C1. Not 🔴 — line 1172 is prose, so no row is invisible today |
| 7 | One lost marker is reported twice again where the two parents spell the first cell differently — the dedup is keyed on the identity a correction changes | `skills/evidence-check/scripts/correction_check.py#examine` | **fixed** `444fa3ae` | fixed at 444fa3ae; Executed through the CLI: one row, one marker, two entries, `2 correction marker(s)`. Ledger row C4's Notes says the anchors exist for exactly that case. Not 🔴 — measured, 0 of 190 marked rows share a first cell, so it inflates a number rather than hiding a loss |
| 8 | The rule choosing which parent to name is documented in ledger row C9 and in `examine`'s comment, and no case holds it | `skills/evidence-check/scripts/correction_check.py#examine` | **fixed** `444fa3ae` | fixed at 444fa3ae; Executed: `max` swapped for `min` leaves 45 of 45 green. `agent-contract` §14. C9's Claim cell is pinned; it is the Notes' rule that is not |
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

## Paste-ready fixes

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — already deferred in round 1; the issue it names is #468 and it is OPEN | the repository owner |
