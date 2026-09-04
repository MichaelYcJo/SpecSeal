# 1788491830-a-segments-record-says-what-it-cost — review round 1

| Field | Value |
|---|---|
| Target SHA | 77eb59d |
| Ran by | specseal:warden on Opus — the orchestrator spawned it with `model: opus` and filled this row, because the spawn prompt handed the reviewer no model name and the rule forbids a segment sourcing that value from its own idea of what it is |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — this round's fixes are not yet read; the round that opens them sets this cell |
| Contract changes | `declared` went from `(repo, item, body)` to `(repo, item, *bodies)` → `test_an_absent_row_fails_after_the_cutoff`, `test_an_absent_row_only_prints_before_the_cutoff`, `test_a_work_item_with_no_timestamp_prefix_is_grandfathered`, `test_the_row_is_read_on_every_record_not_only_the_last`, `test_the_cutoff_is_the_work_items_own_second`, `test_the_form_the_templates_show_passes`, `test_a_model_name_may_carry_spaces_and_brackets`, `test_backticks_do_not_change_the_answer`, `test_unknown_with_a_reason_is_an_answer`, `test_a_bare_unknown_is_not_an_answer`, `test_an_empty_cell_is_not_an_answer`, `test_one_thing_named_is_not_two`, `test_the_on_must_stand_alone`, `test_a_row_inside_a_comment_is_not_the_row` |
| New units | `test_the_behaviour_spec_carries_a_subsection_for_this_refusal` (depth 1); `test_the_documents_say_why_older_records_are_excused` (depth 1); `test_the_spec_states_the_two_halves_and_the_unknown_answer` (depth 1); `test_a_work_item_with_no_timestamp_prefix_is_grandfathered` (depth 1); `test_the_row_is_read_on_every_record_not_only_the_last` (depth 1); `test_the_arm_order_changes_the_reading_and_never_the_verdict` (depth 1) |
| Needs a fix | yes — five 🟡: the behaviour spec has no subsection for the refusal this branch adds, two of its choices are pinned by nothing, and two sentences say something the branch's own measurements disprove |
| Loses a record or crashes | no |

- [ ] Pass

<!-- This record was written AFTER the fix pass rather than before it, which is
the orchestrator's process error and cost something measurable: the reviewer's
drafted subsection and replacement paragraph lived only in its report, so the
implementer could not read them and wrote its own. The two should be compared
rather than one assumed to be the other. The two work items before this one
both had their round record committed before the fixes began. -->

## What this round was asked

The whole branch against `release/v0.8.0`, with seven surfaces named in order,
four of which the implementer had raised itself when it handed over: the branch
order inside `runner_problem`, whether the row should be read on every record
or the last, `RUNNER_FROM` against the three cutoffs beside it, and whether
`docs/review-chain-spec.md` was rightly left untouched.

Three were the orchestrator's: a third instance of the class the implementer
had named — *a case whose input or needle is satisfied by something other than
the thing it means to pin* — the self-contradiction it had already fixed at
`473765d`, and whether this branch's own records can be written honestly under
the rule, since they are its first real use.

The prompt also stated the narrowing as answered rather than open: the outcome
column is #149 on 0.9.0 and was not to be opened as a gap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The behaviour spec has a subsection for every row `chain_check.py` refuses at the pull request, with its cutoff beside it, and names neither `Ran by` nor `RUNNER_FROM` | `docs/review-chain-spec.md` | fixed at `d4b3307` | Executed: `grep -c "Ran by"` → 0. The implementer's grounds — *it owns the cap and the floor, and this is neither* — do not survive reading the file: `Contract changes` and `New units` make no claim about when a run stops either and have a subsection at `:638`. What the file owns is the refusals. The same class cost the previous work item its 🟡 7 and 🟡 8 |
| 🟡 2 | Nothing pins the every-record choice, which the checker states as a deliberate decision twice | `chain_check.py:2451` | fixed at `d4b3307` | Executed by both: narrowing `ran_by` to the last record left 215 cases green for the reviewer and 272 for the implementer on a different suite set — same conclusion. The choice is right; a work item whose rounds ran under different runners is the comparison the row exists to make |
| 🟡 3 | This branch closed the no-prefix arm in all three sibling suites and left none for itself | `tests/test_a_record_says_what_ran_it.py` | fixed at `d4b3307` | The case exists as `test_a_work_item_with_no_timestamp_prefix_is_grandfathered` in three files; this branch made their `record()` helpers always emit the row, so none of them reaches the arm any more. Executed: the arm is correct, and removing `began is None` crashes on `None < int` with nothing red |
| 🟡 4 | `runner_problem`'s docstring calls an ordering load-bearing; the branch's own ledger row R1 already recorded that it is not | `chain_check.py:1817`, `phases/phase-2.md`, ledger R1 | fixed at `d4b3307` | The reviewer compared the two orders over **302,104 inputs — zero mismatches**, on verdict and on message, and reversing the arms in the real file left 215 cases green. The implementer reproduced it over 1,536 constructed cells, same answer. True by construction too: the `unknown` arm refuses when nothing follows the separator, and nothing following means no ` on ` in the tail. Two durable records disagreeing about one fact is the shape this repository refuses everywhere else |
| 🟡 5 | `test_a_row_inside_a_comment_is_not_the_row` is satisfied by its `Target SHA` rather than by what it pins | `tests/test_a_record_says_what_ran_it.py:330` | fixed at `d4b3307` | Executed by both: move the row out of the comment so it is a legitimate answer and the case still exits 1, because the hand-built fixture's SHA is forty zeroes. The needle caught the mutation, so it was not a hole — it is the third instance of the class the implementer named in phase 4, this time on the exit code |
| 🟢 6 | The contradiction the implementer fixed at `473765d` — the round template's *never the segment itself* copied into the phase template, where the segment holds the pen | `templates/sdd-phase.md`, `templates/sdd-round.md` | answered | The two templates read differently and correctly: the round record is the orchestrator's to write, so *yours* ends it; the phase record's writer is the segment, so authority and keystrokes are separated. The reviewer confirmed no old wording survives in either |
| 🟢 7 | Whether this branch's own records can be written honestly under the rule | `phases/phase-1.md`–`phase-4.md` | answered | All four carry the row and `evidence-check --strict` reports 9 ok. The ❓ the reviewer left is answered below rather than deferred |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: real vs. reversed `runner_problem` over 302,104 inputs | zero mismatches on verdict or message |
| reviewer: arms reversed in the real file, four suites | 215 passed — nothing caught |
| reviewer: `ran_by` narrowed to the last record, four suites | 215 passed — nothing caught |
| reviewer: the comment case's row moved out of the comment | still exit 1, on the SHA |
| reviewer: §15 audit — the new case file against the pre-branch checker | 31 failed, 15 passed |
| implementer: the same five findings measured before fixing | each confirmed independently |
| implementer: eight mutations plus a control | no survivors |
| the three spec pins, red at `77eb59d` with the change stashed | then green |
| `evidence-check --ledger 'seal/ledger/1788491830-*.md' --strict .` | 10 ok, exit 0 |
| `unverified-check` · `uvx ruff check tests/ skills/` | exit 0 · exit 0 |

## Inherited coordinates

Round 1 — nothing to inherit. What it was handed instead were the implementer's
own four leads, and the correction that `--ledger` narrows `--reverify` to a
fragment.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `ran_by`'s `read_record`-returns-`None` arm has no case, and neither does the same early return in `fix_surface` and `stopping_floor` — three functions wide rather than this branch's alone | `overview.md` §Not done, for round 2 | the repository owner |
| Where the `Ran by` value in the four phase records came from | answered below, not deferred | — |
| The full suite, repository-wide lint and typecheck | `overview.md` §Not verified | the orchestrator's single broad run |
| `seal/ledger.md` S8 | work item `1788472135`'s memo | the repository owner |

## The ❓ the round left, answered

The reviewer could not fill its own `Ran by` and said so: the spawn prompt
handed it no model name, and the rule forbids a segment sourcing that value
from its own idea of what it is. **That is the rule working rather than
failing**, and the row above is the orchestrator filling it, which is what the
spec subsection this round added says to do.

The four phase records are the mixed case and the implementer answered it
plainly. The spawn prompt said *"You are `specseal:smith` on Opus"*, so the
agent half and the model family came from the orchestrator; the implementer
expanded `Opus` to `Opus 5 (1M context)` from its own system prompt. **Half
the value was sourced the way the rule permits and half the way it does not**,
and no check can see the difference — which is the limit the spec subsection
records rather than closes.

They are left as written. Overwriting four records to make a version string
marginally more precise would spend more than it buys, and the fact is here.
