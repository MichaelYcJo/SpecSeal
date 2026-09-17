# 1789621028-nothing-reads-a-record-against-the-tree — review round 2

| Field | Value |
|---|---|
| Target SHA | 6522c19f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 435 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `d34ef3177711c20e5955465a59136d70d2297f01..f4e7d768bbfc9d7ab482e371bfc2376e143c5c80`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🔴 1, the rewritten case that reddens on the release branch once this branch squash-merges; and 🟡 2, the new case's assertion that cannot fail |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of round 1's ten findings, at `6522c19f`, over the fix range `b38bd920..bf693bc1`, six commits. `close` had ticked `Pass` beside `nobody`, so the round was told what brought it here: a run cannot claim to have passed while the fixes that closed its findings were opened by nobody, and this round is the one that opens them. It was asked to revert each of the seven `fixed` alone, run the case it names and quote what it breaks on; to judge the two `answered` on their grounds rather than on the code, an answer it does not accept being a finding; and to check only that #436 exists and says what the deferral claims.

Four places a closure most easily goes wrong were named at the spawn, each as the fix pass's own claim rather than as a fact: that 🟡 3's repair named a command instead of changing numbers, so the same command giving 5 and then 4 is the repair working rather than a contradiction, and that every other place carrying those figures followed; that the pass narrowed a ledger claim its own fix had made false, because this work item's `round-1.md` is the first record in the tree to carry the new row; that five survivor-check hits were exempted and one corrected inside shipped code; and that 🟡 2's repair left `close`'s behaviour alone and fixed the message and two documents instead. The orchestrator had verified the tip, the clean tree, the six-commit count and #436's existence, and had run none of the fix pass's own checks.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The rewritten repository-wide case asserts that a record carrying the row prints no notice, which the checker's own docstring calls the ordinary state of a merged record — so the case turns red on `release/v0.12.1` at the first run after this branch squash-merges | `tests/test_chain_check_at_the_pull_request.py:2843` · `test_the_records_in_this_repository_are_not_failed_by_the_new_row`, the `printed == len(records) - len(carrying)` assertion | **fixed** `879b0e35` | fixed at 879b0e35; Executed: the record's ends pointed at commits this repository does not hold, everything else untouched — exit 1, `230 notices over 229 records with no row`, `assert 230 == (230 - 1)`; restored exit 0. `fix_range` answers unresolvable ends with a NOTICE, `.github/workflows/test.yml` checks out at `fetch-depth: 0` which never fetches `refs/pull/*`, and the repository rule squashes a feature branch into its release branch |
| 🟡 2 | The new case's `the refusal wrote anyway` assertion compares two post-run reads of one file, so it cannot fail | `tests/test_the_fixes_close_the_record.py:2537` · `test_a_record_with_no_fix_range_row_is_told_which_row_to_add` | **fixed** `879b0e35` | fixed at 879b0e35; Executed: `close` altered to overwrite every `round-*.md` under the work item before raising — the case still passed, exit 0, and the assertion whose message is `the refusal wrote anyway` said nothing. The helper reads the record after the subprocess and the test reads the same path again |
| ⬜ 3 | The exemption file this fix pass created states its range as `b38bd920..HEAD`, a moving end, in the work item that exists to refuse them — while the sibling file the same pass repaired was pinned | `seal/specs/1789621028-…/survivors.md:3` | **fixed** `879b0e35` | fixed at 879b0e35; Executed: both `..bf693bc1` and `..HEAD` exit 0 with one row used, so the stated result is true today and re-runnable under only one of them |
| ⬜ 4 | The retired `8 spellings` figure survives in R8's `Notes` cell and in two places in `overview.md`, two of them cells of the very rows the fix pass corrected to `12` | `seal/ledger/1789621028-…md:10` · R8 `Notes`; `seal/specs/1789621028-…/overview.md:26` and `:59` | **fixed** `879b0e35` | fixed at 879b0e35; Read: R8's `Verified behavior` says 12 distinct sentence forms and its `Notes` argues from 8; `overview.md`'s divergence row says 12 in `Chosen` and 8 in `Grounds`. The three records of a moment that hold the old figure all carry a correction beside it; these do not |
| ⬜ 5 | Round 1's ⬜ 6 repair reworded the first half of a sentence and left the second half, which was written to continue it | `seal/specs/1789034970-…/survivors.md:5` | **fixed** `879b0e35` | fixed at 879b0e35; Executed, the file with HTML comments stripped: `across this branch's life by <command>` is followed by `across this branch — fifteen at the head…`, so the phrase is doubled and the tail begins as a fragment |
| ⬜ 6 | A comment in shipped code cites `round 1's 8` for what is round 1's ⬜ 4, while `round_record.py` cites the same number correctly for ⬜ 8 | `skills/code-review/scripts/chain_check.py:4271` · the `fix_range` comment block in `main` | **fixed** `879b0e35` | fixed at 879b0e35; Read: the separation of the two comment blocks is ⬜ 4; ⬜ 8 is the `isdigit()` guard at `round_record.py:3797`, which cites `(round 1's 8)` correctly. Every other citation in these two modules carries the severity marker or the word `finding` |
| ⬜ 7 | ⬜ 9's `answered` grounds state `0 git calls`, and the commit that wrote the sentence is the commit that made it false | `seal/specs/1789621028-…/rounds/round-1.md:37` · ⬜ 9's `Grounds` cell | **fixed** `879b0e35` | fixed at 879b0e35; Executed: `fix_range` over all 230 records with the git helper instrumented makes **1** call, `rev-list --count` for `round-1.md`'s own range, in 0.120 s. The answer it supports is unaffected |
| ⬜ 8 | Two of the seven closures — the template's closing pipe and the `isdigit()` half of `close`'s count guard — are pinned by no case | `templates/sdd-round.md` · the `\| Fix range \|` row; `skills/code-review/scripts/round_record.py` · `close` | answered | Neither case may be planted by this pass, and the grounds are the tree's rather than the pass's. The `isdigit()` guard's case would add a unit to `tests/test_the_fixes_close_the_record.py`, whose only unit named by round 1's `New units` row is the very unit round 2's 🟡 2 sits inside — so adding one while closing that finding `fixed` is depth 2, and `close` refuses before writing a cell. The behaviour is read off a shipped case rather than judged: `test_a_depth_two_refusal_names_the_finding_whose_fix_added_the_unit` <!-- Round 3, 2026-09-17: executed, and the generator does the opposite. `close` run against this record's pre-close state with one new top-level unit committed into `tests/test_the_fixes_close_the_record.py` and the same eight-row fix table wrote `New units | <the unit> (depth 1)` and changed the record; there was no depth-2 refusal. `units_named_earlier` strips underscores from its keys (`# RIDER:` at `round_record.py#units_named_earlier`) so `depth_two` reaches no snake_case unit, and the case cited here uses `alpha` and `beta`, which carry none — #438. The template half of this answer stands; the `isdigit()` half's reason does not. -->, named in `overview.md` for whoever checks it. The template's closing pipe needs a walk over every field row, and a walk is on the list a fix pass may not add. Both are rows in `overview.md` §*Not verified* with an answerer named, which is where `unverified-check` reads them; today's cost of each is zero, `split_row` tolerating the open cell; Executed, each reverted alone: the pipe gives 181 passed exit 0 over the three modules reading the template, the guard gives 102 passed exit 0 over `tests/test_the_fixes_close_the_record.py`. Both are cleanups round 1 recorded as breaking nothing; the guard is a new refusal path rather than a cosmetic change |
| 🟢 9 | 🟡 1 of round 1 — the pending `Fix range` no arm reads back | `skills/code-review/scripts/chain_check.py` · `fix_range`, the `says_none` early return | deferred #436 | Executed: issue #436 exists and is `OPEN`, titled `fix: chain-check never names a Fix range still saying the fixes are not yet written`. Its body carries the orchestrator's execution, points at round 1's record for the paste-ready arm, names the cutoff question as the builder's judgment, and lists what not to build. The row's claim holds |
| 🟢 10 | 🟡 2 of round 1 — `close`'s refusal names no repair | `skills/code-review/scripts/round_record.py` · `close` | fixed | Executed: the `try`/`except` reverted to the bare `field_index` write reddens the new case at exit 1, `assert 'no \| Fix range \| … \| row' in 'round-record: the record has 0 … rows and needs one'`; restored exit 0. Read: the behaviour argument holds, and `docs/review-chain-spec.md` §*The grandfathering is the checker's and not the generator's* and the changelog's split `What changes for a caller` now say which side grandfathers |
| 🟢 11 | 🟡 3 of round 1 — a corpus count with no command | `docs/review-chain-spec.md` · §*The fix range* | fixed | Executed: the document's own command run in the clone gives 39 / 15 / 5 / 12 at `56945007` and 39 / 15 / 4 / 12 at `6522c19f`, matching the document, the changelog fragment and R8 exactly. The document states the moving figure as the point rather than as a caveat. The constant comment in `chain_check.py` no longer carries the method-less count. Where the propagation stopped short is ⬜ 4 above |
| ⬜ 12 | ⬜ 4 of round 1 — stacked comment blocks | `skills/code-review/scripts/chain_check.py` · `main` | fixed | Read: each block now sits above its own call and states that arm's cutoff correctly. The citation inside it is ⬜ 6 above |
| ⬜ 13 | ⬜ 5 of round 1 — the template's missing pipe | `templates/sdd-round.md` | fixed | Read: the row closes. Executed: nothing pins it — ⬜ 8 above |
| ⬜ 14 | ⬜ 6 of round 1 — a pinned command beside a number it does not produce | `seal/specs/1789034970-…/survivors.md` | fixed | Read: the sixteen is now attributed to the branch's life rather than to one run of the pinned command, which answers the substance. The wording it left behind is ⬜ 5 above |
| 🟢 15 | ⬜ 7 of round 1 — the ledger re-stamp had no divergence row | `seal/specs/1789621028-…/overview.md` · §*Where spec and implementation diverged* | fixed | Read: the row exists and states the right thing — the exclusion's grounds were about removal, and a drifted row takes the tree to NOT SEALED under `--strict`, so leaving them was not available |
| ⬜ 16 | ⬜ 8 of round 1 — half a guard the neighbouring module writes in full | `skills/code-review/scripts/round_record.py` · `close` | fixed | Read: `counted is None or not counted.strip().isdigit()` now matches `fix_range`. Executed: nothing pins it — ⬜ 8 above |
| ⬜ 17 | ⬜ 9 of round 1 — the arm's git cost | `skills/code-review/scripts/chain_check.py` · `fix_range` and `resolves_to` | answered | The reasoning is accepted: memoizing a function five arms share is mechanism a fix pass may not build, and the cost becomes measurable when it becomes real. Executed: the figure beside it is stale — 1 call, not 0, which is ⬜ 7 above and does not change the answer |
| ⬜ 18 | ⬜ 10 of round 1 — two surviving `..HEAD` fix tables | `seal/specs/1789598366-…/rounds/round-1-fixes.md` and `round-2-fixes.md` | answered | Accepted. Read: `spec.md` §Out does exclude records of other work items, `RANGE_FROM` does excuse them, and recording the survival is the right handling for a branch that was not asked to touch them. The branch then wrote a new moving range of its own, which is ⬜ 3 above |

## Paste-ready fixes

```python
    assert len(records) > 200, f"the walk found {len(records)} records"
    failed, printed_without_a_row, carrying = [], 0, []
    for rel in sorted(records):
        errors, notices = check.fix_range(reader, ROOT, rel)
        failed.extend(errors)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            carries = f"| {check.FIX_RANGE} |" in f.read()
        if carries:
            carrying.append(rel)
        else:
            printed_without_a_row += len(notices)
    assert not failed, f"records the new row would fail: {failed[:5]}"
    # The population, split the way the tree is actually split. Until this
    # work item's own round 1 there was no record carrying the row at all and
    # this read `printed == len(records)`; the first record to carry one made
    # that false, which is the case being right rather than the tree being
    # wrong. What has to hold is that a record WITHOUT the row is printed and
    # never failed, and that the two groups account for every record -- a walk
    # that quietly read nothing would report no failures too.
    #
    # The notices are counted over that group ALONE, never as a subtraction
    # from the whole. A record that HAS the row prints whenever its ends stop
    # resolving, which `fix_range`'s own docstring calls "the ordinary state
    # of a merged record and not a fault in it" -- and the squash that merges
    # this branch makes it the state of the one record carrying the row. A
    # subtraction asserts that such a record prints nothing, which is the
    # opposite of what this module documents (round 2's 1).
    assert carrying, "no record in this tree carries the row, so nothing is read"
    assert printed_without_a_row == len(records) - len(carrying), (
        f"{printed_without_a_row} notices over {len(records) - len(carrying)} "
        "records with no row: a record that predates the row has to print, "
        "not go quiet"
    )
```
```python
    stripped = text.replace(row + "\n", "")
    path.write_text(stripped, encoding="utf-8")
```
```python
    # The bytes from BEFORE the run, never a second read of the file the run
    # may have written. `close` in this module returns the record it read
    # AFTER the subprocess, so comparing that against another read of the
    # same path compares the file to itself and passes however much `close`
    # wrote -- shown by making `close` clobber every record before raising
    # and watching this line stay green (round 2's 2).
    assert record == stripped, "the refusal wrote anyway"
```
```markdown
## Round 1's fix pass — `b38bd920..bf693bc1`
```
```markdown
None of them changes a decision — 15 files in 12 sentence forms refuses the
parser more firmly than 11 in eleven did — and what matters is that the
measured figures are what shipped into the specification, with the command
that produces them named beside them.
```
```markdown
Sixteen places were reported across this branch's life by
`survivor-check --range d35c874...ce0f9fe`
```
```markdown
`survivor-check --range d35c874...ce0f9fe` reports two places today. Sixteen
were reported across this branch's life
```
```python
            # (round 1's ⬜ 4). Whether an arm has a cutoff is the load-bearing
```
```markdown
the arm run over all 230 records in this tree makes 0 git calls in 0.057 s
<!-- Round 2, 2026-09-17: 1 call, not 0 — `rev-list --count` for this
record's own range, which this record is what introduced. Executed with
`chain_check`'s git helper instrumented, 0.120 s over the same 230 records.
The answer is unaffected: 1 is as good as 0 for the argument that memoizing
is not owed yet. -->
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone at `6522c19f` | 229 passed, exit 0 — the baseline every mutation below was taken against |
| `close`'s `try`/`except` reverted to the bare `field_index` write, then restored | exit 1 mutated, exit 0 restored — the new case reddens on the exact old message |
| the record's range ends pointed at commits this repository does not hold, then restored | exit 1, `230 notices over 229 records with no row`, `assert 230 == (230 - 1)`; exit 0 restored — 🔴 1 |
| `RANGE_FROM` moved to `1`, then restored | exit 1 on `assert not failed`, naming five records of work items begun before the cutoff — ledger R6's own claim, reproduced |
| `close` altered to overwrite every `round-*.md` before raising, then restored | **exit 0, 1 passed** — the `the refusal wrote anyway` assertion never fires — 🟡 2 |
| the `isdigit()` half of `close`'s count guard reverted, then restored | 102 passed, exit 0 — nothing pins it |
| the template's closing pipe reverted, then restored | 181 passed, exit 0 over the three modules that read the template — nothing pins it |
| the command `docs/review-chain-spec.md` §*The fix range* states, at `56945007` and at `6522c19f` | 39 / 15 / **5** / 12 and 39 / 15 / **4** / 12 — every shipped figure reproduces |
| `fix_range` over all 230 `round-N.md` files with `chain_check`'s git helper instrumented | 0 errors, 229 notices, **1** git call in 0.120 s |
| `bin/survivor-check --range b38bd920..bf693bc1 --exempt <this item's survivors.md>` | exit 0, 1068 files against 31 removed sentences, one exemption row used, `every survivor is excused by a row above (1)` |
| `bin/survivor-check --range b38bd920..HEAD --exempt <the same>` — the range the file literally states | exit 0, same result at `6522c19` |
| `bin/evidence-check` in the clone | exit 0, **1340 ok**, 0 drifted, 0 broken |
| `gh issue view 436` | `OPEN`, and the body says what `round-1.md`'s deferred row claims |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer and this round ran none of them. They are not due yet either: 🔴 1 and 🟡 2 are open, so a fix pass and one further verifying round come first |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py` · `fix_range`, the `says_none` early return | round 1's 🟡 1 — deferred |
| round-1 | `skills/code-review/scripts/round_record.py` · `close`, the `field_index(reader, lines, chain.FIX_RANGE)` write | round 1's 🟡 2 — fixed |
| round-1 | `docs/review-chain-spec.md` · §*The fix range — `Fix range`*, the *Measured over this repository* paragraph | round 1's 🟡 3 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py` · `main`, above `range_errors, range_notices = fix_range(...)` | round 1's ⬜ 4 — fixed |
| round-1 | `templates/sdd-round.md` · the `\| Fix range \|` row | round 1's ⬜ 5 — fixed |
| round-1 | `seal/specs/1789034970-…/survivors.md` · the line under `## Over the whole branch — what CI reads` | round 1's ⬜ 6 — fixed |
| round-1 | `seal/specs/1789621028-…/overview.md` · §*Where spec and implementation diverged* | round 1's ⬜ 7 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py` · `close`, `spanned = int(counted.strip())` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py` · `fix_range` and `resolves_to` | round 1's ⬜ 9 — answered |
| round-1 | `seal/specs/1789598366-…/rounds/round-1-fixes.md` and `round-2-fixes.md` | round 1's ⬜ 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |
