# 1789621028-nothing-reads-a-record-against-the-tree — review round 3

| Field | Value |
|---|---|
| Target SHA | f2e8a010 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 435 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `fda0797dcd67400cb1f9db7069b37f320df0693c..825d5c65c9b056311c82d4963663a8d6a557af6e`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last round of the run, at `f2e8a010`, over the fix range `d34ef317..f4e7d768`, three commits. Round 2's verdicts closed on a fix, so this record ends the run whatever it finds — which the spawn stated as a reason to say plainly of anything opened whether it must be fixed before shipping or belongs in an issue with a named answerer, and not as a reason to pass anything. The round had built both of the mutations that produced round 2's two findings, so it was asked to re-run its own rather than reconstruct them, and to quote what each printed.

One closure was singled out because its grounds were a claim about the generator rather than a judgment: `⬜ 8` closed `answered` on the argument that planting a case for `close`'s `isdigit()` guard would put a new unit in the file whose unit an earlier record names, making it depth 2 and refused before a cell was written, with `test_a_depth_two_refusal_names_the_finding_whose_fix_added_the_unit` named as the shipped case that drives it. The round was told to open that case and judge whether it says what the grounds claim, and that an answer whose grounds do not hold is a finding. The orchestrator had generated and committed round 2's record, run `close` with the eight-row fix table, confirmed the three-commit count, and filed #437; it had re-run none of the fix pass's own checks.

## Verdicts

<!-- Orchestrator, 2026-09-17: the eight carried rows arrived from the report with a number in the `#` cell and round 2's own verdict word, and both columns are corrected here to the shape this tree uses for a carried closure — a bare marker and `confirmed`. `closed_with_a_fix` reads every verdict cell, so inheriting `fixed` made this record read as one that closed on a fix and the cap refused it; 3 of the 71 work items with two or more records have a last record of that shape. Findings, coordinates, grounds and terminal lines are the reviewer's, untouched. -->

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Round 2's ⬜ 8 closed `answered` on the claim that `close` refuses a new unit in that file at depth 2 before writing a cell. It does not — it writes the cell at depth 1 — and the case the grounds cite uses underscore-free names, which is the one shape the mechanism can reach | `seal/specs/1789621028-…/rounds/round-2.md` · ⬜ 8's `Grounds`; `seal/specs/1789621028-…/overview.md` · §*Not verified*, the `isdigit()` row | answered | corrected at `825d5c65`; the record-side half rode in `fda0797d`, as a comment beside round 2's cell rather than over it. The defect the corrected row now describes is #438; Executed: the record put back to its pre-close state, one new top-level unit committed into `tests/test_the_fixes_close_the_record.py`, the same eight-row fix table — `close` reported `7 fixed, 1 answered`, wrote `New units \| … (depth 1)` and the record changed. Cause is the `# RIDER:` at `round_record.py:3417` — `chain.EMPHASIS` strips every underscore from `units_named_earlier`'s keys while `location_units` returns them raw, so the lookup misses. Measured: 502 of the 542 units any `New units` row in this tree names carry an underscore. No issue tracks it; #333 and #222 are other `depth_two` defects |
| ⬜ 2 | The ⬜ 5 repair states `` `survivor-check --range d35c874...ce0f9fe` reports two places today `` — a present-tense claim that is exit 2 in any fresh clone, because `ce0f9fe` is reachable from no ref and does not travel | `seal/specs/1789034970-…/survivors.md:5`; `seal/ledger.md` · R7's `Verified behavior` | answered | corrected at `825d5c65`. The figure is left standing and labelled a past reading, because the commit its range names resolves in no clone and re-pinning is therefore not available. The decision between keeping it labelled, dropping it, and re-measuring against something a ref reaches is #439, with the repository owner as answerer; Executed: in a `--no-local` clone the command exits 2, `` `ce0f9fe` does not resolve ``. `d35c874` resolves in the clone and is reachable from 1 ref; `ce0f9fe` resolves in the working checkout and is reachable from 0. Re-pinning is not available — the object is gone from any clone — so this is the owner's call rather than a correction |
| ⬜ 3 | The HTML comment between the sentence's halves opens an HTML block, so the repaired sentence renders as two paragraphs and the tail begins with an em dash | `seal/specs/1789034970-…/survivors.md:5` | answered | corrected at `825d5c65`; Executed through GitHub's own markdown renderer: paragraph 0 ends `Sixteen were reported across this branch's life`, paragraph 1 begins `— fifteen at the head it was first run against`. Older than either repair and not what round 2 raised; one line to move |
| 🟢 | round 2's blocking finding is closed — the case that reddened after the squash | `tests/test_chain_check_at_the_pull_request.py` · `test_the_records_in_this_repository_are_not_failed_by_the_new_row` | confirmed | Executed with round 2's own mutation, three ways: the repair with the record untouched exit 0; the repair under the mutation exit 0; round 1's arithmetic restored under the same mutation exit 1, `assert 230 == (231 - 2)`. Also executed in the real post-merge state — BOTH records carrying the row made unresolvable at once — exit 0. The repair counts notices over the group with no row rather than subtracting, so any number of carrying records may print |
| 🟢 | round 2's second finding is closed — the assertion that could not fail | `tests/test_the_fixes_close_the_record.py` · `test_a_record_with_no_fix_range_row_is_told_which_row_to_add` | confirmed | Executed with round 2's own clobbering mutation: `close` altered to overwrite every `round-*.md` before raising now gives exit 1, `AssertionError: the refusal wrote anyway`, naming the clobbered bytes against the record it expected. Unmutated exit 0, restored exit 0. The same mutation passed silently in round 2 |
| 🟢 | ⬜ 3 of round 2 — the exemption file's moving range | `seal/specs/1789621028-…/survivors.md:3` | confirmed | Read: the heading reads `` `b38bd920..bf693bc1` ``, both ends commits, matching the sibling file's pinning |
| 🟢 | ⬜ 4 of round 2 — the retired `8 spellings` figure | `seal/ledger/1789621028-…md` · R8 `Notes`; `seal/specs/1789621028-…/overview.md:26` and `:59` | confirmed | Read: all three coordinates now read 12 sentence forms, and `overview.md:59` names the command beside it. The two remaining holders are `phases/phase-3.md` and `phases/phase-4.md`, records of a moment that already carry the correction |
| ⬜ | ⬜ 5 of round 2 — the doubled phrase | `seal/specs/1789034970-…/survivors.md:5` | confirmed | Executed: the doubling is gone — the sentence no longer says `across this branch's life` and `across this branch` on either side of the command. What the repair left is the rendering break, ⬜ 3 above, and the claim itself, ⬜ 2 above |
| 🟢 | ⬜ 6 of round 2 — the wrong finding cited in shipped code | `skills/code-review/scripts/chain_check.py:4271` | confirmed | Read: the comment now reads `(round 1's ⬜ 4)`, and `round_record.py:3797` still cites `(round 1's 8)` for the guard, so the two no longer collide |
| 🟢 | ⬜ 7 of round 2 — the `0 git calls` figure | `seal/specs/1789621028-…/rounds/round-1.md` · ⬜ 9's `Grounds` | confirmed | Read: the cell carries the HTML-comment correction giving 1 call beside the 0, with the execution and the reason the answer is unaffected |
| ⬜ | ⬜ 8 of round 2 — two closures pinned by no case | `templates/sdd-round.md`; `skills/code-review/scripts/round_record.py` · `close` | confirmed | **The answer is not accepted.** Its grounds are a claim about the generator and the generator does the opposite — ⬜ 1 above carries the execution. The template half stands: pinning it needs a walk, and a walk is on the list a fix pass may not add. The `isdigit()` half's stated reason is false, and the row it produced in `overview.md` §*Not verified* is precedent a future pass will read |

## Paste-ready fixes

```markdown
| The `isdigit()` half of `close`'s count guard is pinned by no case, and round 2's fix pass did not add one. Reverted alone it is 102 passed, exit 0 | the repository owner, as its own work item. **The reason first given here was wrong and is corrected**: the pass argued that `close` would refuse the new unit at depth 2, because round 2's 🟡 2 sits inside a unit `rounds/round-1.md`'s `New units` names and the case would land in that unit's file. Round 3 executed it — one new top-level unit committed into that file, the same eight-row fix table — and `close` did **not** refuse: it closed the record and wrote `New units \| <the unit> (depth 1)`. The cause is the `# RIDER:` at `skills/code-review/scripts/round_record.py#units_named_earlier`, which strips every underscore from that function's keys while `location_units` returns them raw, so `depth_two` reaches no snake_case unit — 502 of the 542 units named by a `New units` row in this tree carry one. So the case WAS available to that pass and was simply not written; what is owed is the case, not a rule |
```
```markdown
<!-- Round 3, 2026-09-17: executed, and the generator does the opposite. `close` run against this record's pre-close state with one new top-level unit committed into `tests/test_the_fixes_close_the_record.py` and the same eight-row fix table wrote `New units | <the unit> (depth 1)` and changed the record; there was no depth-2 refusal. `units_named_earlier` strips underscores from its keys (`# RIDER:` at `round_record.py#units_named_earlier`) so `depth_two` reaches no snake_case unit, and the case cited here uses `alpha` and `beta`, which carry none. The template half of this answer stands; the `isdigit()` half's reason does not. -->
```
```markdown
`survivor-check --range d35c874...ce0f9fe` reports two places today. Sixteen
were reported across this branch's life — fifteen at the head it was first
run against, and a sixteenth once the note explaining a removed ledger row
landed, which put the sentence that row carried into the range's removed set.
None of the sixteen is a stale copy of a corrected claim standing where a
reader would act on it.
…and the comment that already stands in the file follows unchanged, opening
at `The range read origin/release/v0.10.0...HEAD until 2026-09-17`.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone at `f2e8a010` | 229 passed, exit 0 — the baseline every mutation was taken against |
| round 2's squash mutation — the record's range ends made unresolvable — against round 3's repair | **exit 0**, 1 passed |
| the same mutation with round 1's arithmetic restored | **exit 1**, `230 notices over 229 records with no row`, `assert 230 == (231 - 2)` |
| the same mutation applied to **both** records carrying the row, the real post-merge state | **exit 0**, 1 passed |
| round 2's clobbering mutation — `close` overwriting every `round-*.md` before raising — against round 3's repair | **exit 1**, `AssertionError: the refusal wrote anyway`, naming the clobbered bytes |
| `close` re-run against the pre-close record with one new top-level unit committed into the file ⬜ 8 names | **no depth-2 refusal** — `7 fixed, 1 answered`, `New units \| … (depth 1)`, record changed |
| `units_named_earlier` and `location_units` asked for their key shapes | `testarecordwithnofixrangerowistoldwhichrowtoadd` against `test_a_record_with_no_fix_range_row_is_told_which_row_to_add`; membership `False` |
| every `New units` entry in the tree counted for underscores | **502 of 542** carry one |
| `bin/survivor-check --range d35c874...ce0f9fe` in the clone | **exit 2**, `` `ce0f9fe` does not resolve `` |
| both pinned ends checked for reachability | `d35c874` — resolves in the clone, 1 ref; `ce0f9fe` — does not resolve in the clone, 0 refs |
| the survivors section put through GitHub's markdown renderer | two paragraphs, the second beginning `— fifteen at the head it was first run against` |
| `gh issue list --state all` searched for the underscore defect | #333 and #222 are other `depth_two` defects; nothing tracks this one |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer and this round ran none of them. They come due now: this round opens nothing needing a fix, so the sealer's spawn is what follows this record |

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
| round-2 | `tests/test_chain_check_at_the_pull_request.py:2843` · `test_the_records_in_this_repository_are_not_failed_by_the_new_row`, the `printed == len(records) - len(carrying)` assertion | round 2's 🔴 1 — fixed |
| round-2 | `tests/test_the_fixes_close_the_record.py:2537` · `test_a_record_with_no_fix_range_row_is_told_which_row_to_add` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1789621028-…/survivors.md:3` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1789621028-…md:10` · R8 `Notes`; `seal/specs/1789621028-…/overview.md:26` and `:59` | round 2's ⬜ 4 — fixed |
| round-2 | `seal/specs/1789034970-…/survivors.md:5` | round 2's ⬜ 5 — fixed |
| round-2 | `skills/code-review/scripts/chain_check.py:4271` · the `fix_range` comment block in `main` | round 2's ⬜ 6 — fixed |
| round-2 | `seal/specs/1789621028-…/rounds/round-1.md:37` · ⬜ 9's `Grounds` cell | round 2's ⬜ 7 — fixed |
| round-2 | `templates/sdd-round.md` · the `\| Fix range \|` row; `skills/code-review/scripts/round_record.py` · `close` | round 2's ⬜ 8 — answered |
| round-2 | `skills/code-review/scripts/round_record.py` · `close` | round 2's 🟢 10 — fixed |
| round-2 | `docs/review-chain-spec.md` · §*The fix range* | round 2's 🟢 11 — fixed |
| round-2 | `skills/code-review/scripts/chain_check.py` · `main` | round 2's ⬜ 12 — fixed |
| round-2 | `templates/sdd-round.md` | round 2's ⬜ 13 — fixed |
| round-2 | `seal/specs/1789034970-…/survivors.md` | round 2's ⬜ 14 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |
