# Implementation Plan: the delegated note compares what it prints

<!-- seal/specs/1790835050-the-delegated-note-compares-what-it-prints/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-01 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

One comparison, one case, and the ledger kept true. `report_spawns` decides
the *never reaches a minute* note on the value the `delegated` column prints
— `round(delegated_max / 60, 1) < 1.0` in place of `delegated_max < 60` —
which is the fix #640's round 3 left paste-ready and the shape #640 used
twice for the tools-per-turn ratio. A case in `tests/test_session_cost.py`
pins both edges of the band: 59.6 s prints `1.0m` and no note, 57.0 s prints
`0.9m` and the note. The edit drifts seven ledger rows anchored at
`report_spawns`, which are re-read and re-stamped; the fragment gains the new
claim and the changelog fragment names the band and the class sweep's result.
No number on any page moves and `--json` is untouched.

## Technical context

**The defect.** `skills/verify/scripts/session_cost.py` `report_spawns`
(`:2170-2333`): `delegated_max` is taken at `:2216-2218` as the largest
`delegated_s` over the rows, compared raw at `:2219`, and printed in the note
at `:2221` with `.0f`; the column prints each row's `delegated` through
`minutes` at `:2251`, and `minutes` (`:1970-1971`) is `f"{seconds / 60:.1f}m"`.
The comment above the block (`:2209-2215`) says why the note exists — a
column of near-zeroes on the ACCEPTED harness reads as *nothing was
delegated* — and stays as it is; the new comment names the cause and #701 in
the shape of the two #640 left at `:2102-2108` and `:2503-2507`.

**The precedent.** `report` compares `round(data["tools_per_turn"], 2) < 1.2`
(`:2109`) and `>= 1.2` (`:2141`); `report_grades` compares
`round(row["numbers"]["tools_per_turn"], 2) < row["bar"]` (`:2519`). Both
fixes came with a case and a changelog sentence naming the band the verdict
moves in, [1.195, 1.2), and no comparability line on the page
(`seal/specs/1790815612-…/changelog.md:29-33`, `plan.md:36-42`).

**Rounding agreement, executed by the framer.** At 56.9, 57.0, 57.02, 59.5,
59.6, 59.99 and 60.0, `round(x / 60, 1)` and `f"{x / 60:.1f}"` agree; 57.0
gives `0.9` on both (57/60 in binary sits just under 0.95) and 57.02 gives
`1.0`. So the note's presence moves for `delegated_max` in (57.0, 60) and
the seconds figure the note prints is at most `57s`.

**The existing cases.** `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is`
(`tests/test_session_cost.py:2608-2635`) pins the 3 s arm (*3s at most*, the
ACCEPTED sentence) and the `orchestrator` fixture's absence of the note;
`test_the_delegated_wait_is_in_no_column_of_any_row` (`:2638`) follows it.
Helpers: `spawn(uid, start, end, subagent_type)` at `:2175`, `call(uid, start,
end, command)` at `:77`, `run(args)` at `:105`. The round-3 report's case is
the S1 half as written; S2 adds the 57.0 s half and asserts the column cell
(`0.9m`) beside the note, so the case ties the comparison to what `minutes`
prints rather than to the number 60.

**`--json`.** `main` runs `report_spawns` only when `args.spawns and not
args.json` (`:3116`) and prints `data` at `:3179-3180` with `delegated_s`
raw. Nothing in the fix reaches it.

**The ledger.** Seven rows anchor at `session_cost.py#report_spawns@15595f59`:
`seal/releases/0.9.5.md` lines 11, 13, 14, 16, 45, 46 and
`seal/releases/0.11.3.md` line 50. All seven drift on hash alone; the claims
hold (`spec.md` §*Data & interfaces*). Row 13's note ends *The `delegated_max <
60` block and its sentence are untouched; `#report_spawns` drifted for the
refusal branch* (its #300 re-read), and this edit is to that block, so its
`Re-read 2026-10-01` note says the comparison now runs on the printed minute
and the sentence is unchanged. `evidence-check --reverify --checked 2026-10-01 .`
recomputes the hash and dates every row it moves; read each row first
(`skills/implement/SKILL.md` §2).

**Two module-reading cases to keep green.**
`tests/test_a_derived_number_reaching_an_int_carries_a_guard.py` walks every
call in this module that converts a number to an int — #640's two `round(x,
2)` calls passed it, and this `round(x, 1)` has the same shape, but the module
is the one it reads. `tests/test_the_handoff_before_round_one.py:596-620`
reads the `round(data["tools_per_turn"], 2) < 1.2` literal by regex; the new
comparison is on a different line and must not disturb that pattern.

**Failure scenario, six months out.** Somebody changes the column's unit —
`minutes` to two places, or the cell to seconds — and the comparison's `, 1`
no longer matches what the cell prints, which is the same defect with the
roles swapped. S2's assertion on the printed cell (`0.9m`) beside the note is
what turns red then; a case asserting the note alone would not.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. `round(delegated_max / 60, 1) < 1.0` — the round-3 paste-ready fix | The comparison and `minutes` round separately and could disagree at an edge. Executed at both edges: they agree, and S2 at 57.0 s pins it | **chosen** — the shape #640 used at `:2109` and `:2519`, so the three sites read alike |
| B. A shared value: `minutes` built on `round(seconds / 60, 1)` and the comparison on the same helper | Touches the function every page prints through, for a defect in one line; a later caller of the helper for a two-place print would have to split it again | rejected — overturnable if Q1 ever finds a disagreement A cannot survive |
| C. Compare against the column's printed string, `minutes(delegated_max) == "1.0m"` or a parse of it | Parses the page's own output; `1.1m` and above would need their own arm, and a widened `minutes` format breaks the parse silently | rejected |
| D. Change the note to print minutes (*0.9m at most*) | The seconds figure is the note's precision at the values it exists for — `3s` beside `0.0m` — and the existing case pins `3s at most`; after A the figure is bounded at `57s` and contradicts nothing | rejected |
| E. Also align `:2115` `tools_per_turn <= 1.0` to the `.2f` print | At a ratio in (1.0, 1.005) the page prints `1.00` with *most turns send a single call*, which `1.00` does not contradict; aligning it would print *one at a time* where a turn sent two, trading a true sentence for one the raw data refutes | rejected — checked and left, named in the changelog fragment |
| F. Round the existence checks at `:2096`, `:2100`, `:2316` to one place | A 2 s repeat vanishes from the page; `0.0m … is BETWEEN the rows` is already a true sentence. Zero is not a threshold the print can contradict; the comment at `:2279-2283` chose two sums over a rounded difference for the same reason | rejected |
| G. Fix the coordinate and skip the sweep | Contract §12; one work item closed this class three times one name apart, and this ticket is the third instance of #640's cause | rejected — sweep recorded in `spec.md`, re-read by the build |
| H. A comparability line on the page | #640's S10 ruling: a line exists where a number moved, and none does here; `--json` is byte-identical | rejected — the changelog fragment names the band |
| I. Widen the band deliberately (e.g. `< 55`) so the note never sits near the edge | A value nobody measured, and 57–60 s is where the two prints disagree, not where the harness behaviour changes | rejected |
| J. Touch a document | None states 60 s (`skills/verify/SKILL.md:683`, `:755-760`; `docs/measuring-a-run.md:31-36`; neither README) | rejected — nothing to correct |

## Phases

Vertical slices — each phase ends with something runnable and verified.

Each phase runs the module it edits and the modules that read what it
edited, named in its row; the new case is seen red first (contract §15) and
the phase record says how. No phase runs the full suite, lint or typecheck
(contract §2); the sealer owns that.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The fix and its case. `report_spawns` compares `round(delegated_max / 60, 1) < 1.0` with a comment naming the cause and #701; `tests/test_session_cost.py` gains one case beside `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is`: a 59.6 s spawn prints `1.0m` and no *never reaches a minute* (red at the base), and a 57.0 s spawn prints `0.9m` and *57s at most* (shown red with the comparison mutated to `< 0.9`, then restored). `phases/phase-1.md` records both reds and the `--json` reading of the S1 fixture | `tests/test_session_cost.py` — the new case, the two delegated cases at `:2608` and `:2638`, and the module's `--json` and `--spawns` cases; `tests/test_a_derived_number_reaching_an_int_carries_a_guard.py`; `tests/test_the_handoff_before_round_one.py` | |
| 2 | The records. The seven rows anchored at `report_spawns` re-read against the diff and re-stamped by `evidence-check --reverify --checked 2026-10-01 .`, row 13 of `seal/releases/0.9.5.md` with a `Re-read 2026-10-01` note on what moved; `seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md` with the new claim anchored at the fixed unit and the case; `changelog.md` naming the band (57.0, 60), that every other threshold comparison in the module was checked, and `:2115` as checked and left with the reason; `phases/phase-2.md` and this table's Status cells | `python3 skills/evidence-check/scripts/evidence_check.py .` exit 0, read directly (§1); `python3 skills/evidence-check/scripts/correction_check.py --range origin/release/v0.17.0...HEAD` exit 0 over the re-read notes; the changelog fragment read against `seal/specs/1790815612-…/changelog.md`'s shape | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. What a phase discovers while
it is being built, and needs the next phase to know, goes to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes. Where feature branches squash, these commits stop
resolving at the merge, and a rebase during the work does the same thing
earlier; re-read the column after any rebase.

## Operational impact

None. No migration, no new dependency, no environment variable, no
compatibility break: `session_cost.py` exits 0 before and after, `--json` is
byte-identical, and the one printed line that moves is a note whose presence
changes for a `delegated` maximum in (57.0, 60) seconds. Not a gate
(`CONTRIBUTING.md` §*What a change to a gate must carry* does not apply).
