# Implementation Plan: what the 0.15.5 rounds deferred (#626, #625)

<!-- seal/specs/1790550713-what-the-0.15.5-rounds-deferred/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

Two deferred issues, three phases. Phase 1 closes #626: one docstring
bullet, one shipped spec's bullet, five restored or new pins, and one case
that holds the docstring's examples to the pins. Phase 2 closes #625: two
comments and five re-wrapped lines. Phase 3 writes the fragment and runs the
sweeps that say the class is closed. Nothing changes behaviour. Every edit is
to a sentence, a comment, a layout or a case. So the one risk is a sentence
that stays false somewhere else, which is what the enumerations in `spec.md`
and the sweeps in phase 3 are for.

## Technical context

- `skills/evidence-check/scripts/evidence_check.py#refused_coordinate`, its
  third docstring bullet, and `#GLUED_MARKS_RE`, the pattern it restates
  (`#(?:"(?:[^"\\\n]|\\.)*"|[^\s"#])*@`, searched).
- `tests/test_a_row_points_by_content.py#GIVEN_UP`, `#TAKEN_UP`,
  `#examples`, `#test_what_rule_a_gives_up_is_silent_and_says_so` and
  `#test_what_the_dotless_openers_take_up_is_named_and_says_so`. The two
  cases assert `` f"`{shape}`" in ec.refused_coordinate.__doc__ `` and the
  verdict through a ledger run beside a good anchor.
- `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md`,
  the five-rule trade list under *Part 2*.
- `seal/specs/1790381328-…/rounds/round-3-report.md` §*Paste-ready fixes*:
  the rule-3 bullet and the `GIVEN_UP` dict, each seen red then green in a
  clone at `c802aca0`.
- `seal/specs/1790381329-the-deferred-sentences-and-pins/rounds/round-2-report.md`
  §*Paste-ready fixes* ⬜ 1. It is on `main` and on this branch. The spawn
  prompt said the directory holds only `changelog.md`, and it holds the whole
  work item, round reports included.
- `skills/code-review/scripts/round_record.py#run_check` (a draft payload
  unless `pull_request_is_ready`) and `chain_check.py#checked_by` (the
  pair prints when `strict` is false, fails when it is true).
- `skills/evidence-check/scripts/evidence_check.py#content_hash`: a unit's
  hash covers its docstrings and comments, with trailing whitespace and blank
  lines dropped. So every re-wrap drifts the rows that cite its unit, and
  `spec.md` §*Data & interfaces* lists the fourteen expected.

**What breaks in six months.** The completeness case reads backticked shapes
out of one docstring section. A later rule whose example is a shape without
`#` or `@` escapes it. A reword that moves an example out of the section after
"What #614 changed" escapes it too. The case's docstring says where it reads,
so the reader who moves the heading meets it. The other failure is a
re-stamp conflict with chain A or C in a `seal/releases/*.md` file at the
squash, which `questions.md` Q4 carries.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Rewrite `CHANGELOG.md` §0.15.5 and the gathered fragment to add the order condition, as the issue lists | policy says a released entry is not rewritten (`docs/review-chain-spec.md` §*What the sweep reads*), and `survivor-check` skips both copies for that reason. The 0.15.5 note that users read would change after they read it | **rejected**; this work's fragment carries the correction |
| Leave 1790381328's `spec.md` as a record and exempt it in `survivors.md` | `settle` folds a released spec's still-true text into `docs/`, so the incomplete bullet becomes policy at the next fold | **rejected**; corrected in place, marked with the date and this work item, as #621 did to `1790297087-…/questions.md` |
| Round 3's paste-ready bullet as written ("no `@` before its `#`") | `@alice#299@abcdef12` has an `@` before its `#` and is named, because `#299@` is glued. The sentence would be false of a shape the code names | **amended**: the builder words the condition as the `@` coming after its `#`, and S2 holds it |
| Restore only the issue's three pins | two more rule examples (`docs/a.md#1장@abcdef12`, `src/a.py#handler @abcdef12`) have no case either. The next rebuild of the dicts drops pins with nothing to notice, which is how the issue's three were lost | **rejected** |
| Plant the five by hand and stop there | the same as the row above, one rebuild later: nothing ties the docstring's examples to the dicts | **rejected** |
| Five pins plus one completeness case over the rules section | reads a docstring by section and by backtick, so a shape with neither mark escapes it (see *What breaks*) | **chosen** |
| #625 item 1: tighten the assertion to `code == 0` | the case is about the exit-2 refusal on the second `close`. The draft exit of the first is already pinned by `test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag` (`assert code == 0` with the pair printed), so this couples an unrelated case to `run_check` for no new coverage | **rejected**; the assertion stays `in (0, 1)` |
| #625 item 1: round 2's paste-ready comment as written | it says the pair prints, and for `answered` and `deferred` the cell is `no fixes to check`, so nothing prints | **amended** (S7) |
| Leave `test_a_fix_commit_carries_no_empty_code_span`'s "Not `code == 0`:" opener | its clauses are true, but it gives a reason for not asserting 0 in a run that exits 0. It is the same misreading at a second site | **rejected**; reworded in the S7 shape |
| #625 item 2: the issue's three lines only | `round_record.py#landing_values` (99 columns) and the `--baseline` help string in `unverified_check.py#main` (95) were left by the same range, and §12 owes the class | **rejected** |
| #625 item 2: every prose line over 88 in the tree (153 in 58 files) | not left by the #623 range; many are assertion needles and data; that is a sweep with a gate behind it | **rejected**; out, with its answerer in `spec.md` |
| Skip the `unverified_check.py#main` re-wrap because it drifts five rows | it leaves a known instance of the class to save five `Re-read` notes, and argparse renders the help the same either way, so the notes are mechanical | **rejected** |

## Phases

Commit at the end of every phase at least, and earlier where a step stands on
its own. Each phase runs only the narrow cases it touched, then
`bin/evidence-check .` to find the rows it drifted. None runs the broad gate,
which is the sealer's.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#626.** Re-run the glued-rule enumeration of `spec.md` first. `refused_coordinate`'s third bullet states that the `@` comes after its `#` (true of `@alice#299@abcdef12`, S2) and names `@alice#299` among the silent shapes. The same condition goes into `seal/specs/1790381328-…/spec.md`'s trade list, with a dated note naming this work item and #626. `GIVEN_UP` gains `docs/a.md#1.2`, `src/a.py#1>"x"`, `Makefile#1x` and `@alice#299` under their rules (round 3's paste-ready dict, keys as the builder finds true). The two named examples join `TAKEN_UP`, or a sibling dict with its own case where the ledger run's output for them does not fit `TAKEN_UP`'s assertion (Q1). `GIVEN_UP`'s comment and both cases' docstrings stop saying "one or two" and "the verdicts #614 moved". One completeness case: every backticked shape holding `#` or `@` in the rules section is a parameter of `GIVEN_UP` or `TAKEN_UP`. Re-read and re-stamp S8–S12 (`0.15.5.md`) and the `MALFORMED` row (`0.15.4.md`). Write the two new rows in the fragment | `bin/test tests/test_a_row_points_by_content.py tests/test_evidence_check.py tests/test_dispatch.py tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` (the four reader modules). Red first: `@alice#299` against the old bullet; round 3's three mutants, each red on its own restored parameter; both named examples red with their example deleted from the docstring and with their branch disabled; the completeness case red against today's dicts. `bin/evidence-check .`: none drifted | 48c36b1 |
| 2 | **#625.** Re-run the pair-class enumeration of `spec.md` first. Rewrite the comment above the first `close` in `test_re_closing_a_half_restored_record_is_refused_for_every_word` (S7). Reword the opener of the comment in `test_a_fix_commit_carries_no_empty_code_span` the same way (S8). Re-wrap the five sites of `spec.md`'s ragged-line table under 88 columns with no word changed. For `unverified_check.py#main`, the help renders the same (S10). Re-read and re-stamp every row `evidence-check` names, twelve expected | `bin/test tests/test_the_fixes_close_the_record.py tests/test_a_script_copied_alone_exits_2.py tests/test_the_gate_hands_cmd_a_path_it_can_run.py tests/test_unverified_rows_close.py`. S7's temporary `code == 0` (green ×3) and the `run_check` mutant (the `fixed` parameter exits 1), both restored. A `test_tmp_*` probe (contract §7), deleted after: each re-wrapped paragraph's words equal before and after, and no prose line the #623 range added is over 88 at the tip. `--help` before and after compared byte for byte. `uvx ruff check` and `uvx ruff format --check` on the five Python files. `bin/evidence-check .`: none drifted | 756926a |
| 3 | **Records and sweeps.** `changelog.md` (`spec.md` §*Data & interfaces*). `overview.md` from `templates/sdd-overview.md`. The sweeps over the whole range | `bin/survivor-check --range origin/release/v0.15.6...HEAD` exits 0, or every survivor answered in this work item's `survivors.md` with grounds. `bin/correction-check --range origin/release/v0.15.6...HEAD` exits 0. `bin/evidence-check .`: 0 drifted, 0 broken, 0 malformed. `python3 .github/scripts/gather_changelog.py --check` exits 0 | 61fbc03 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

What a phase discovers while it is being built, and needs the next phase to
know, goes to `seal/specs/1790550713-what-the-0.15.5-rounds-deferred/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. Re-read the Status
column after any rebase.

## Operational impact

None. No migration, environment variable, dependency or compatibility
change. No command's output, verdict or exit code moves. Release files under
`seal/releases/` are edited only by dated `Re-read` notes and re-stamped
hashes. Chains A and C edit other rows in some of the same files, and they
squash in the order A, B, C.
