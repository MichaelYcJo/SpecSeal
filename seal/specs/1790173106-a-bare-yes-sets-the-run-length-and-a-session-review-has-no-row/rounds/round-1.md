# 1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row — review round 1

| Field | Value |
|---|---|
| Target SHA | 7604e522ade45a51dbbb89589b85905e56b7040c |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 537 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `4f596a7719ae5757880bb9dea06555e55596d701..506b030ad911eee0bcb5fe533c3b0d4176247ecd`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the F4 note in `seal/ledger.md` that still names the removed F8 and turns the hygiene workflow's survivor-check step red at the pull request |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #138 and #241, the whole branch `design/138-241-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row` against `release/v0.15.0`. Stage 1 asked whether the build follows `spec.md`'s two decisions: a bare `yes` in `Needs a fix` is refused by the reader (`chain_check.py#says_reopened`) and the writer (`round_record.py#terminal_value`) in the floor row's words, under `NEEDS_FROM`'s grandfathering, and no longer stops the count walk; and no third `Review` answer is added, because `straight to the PR` has owed the sealer's `broad-gate.md` at a ready pull request since 0.12.0, so the seven sentences saying the direct route requires nothing are rewritten and pinned as gone/stands pairs. Stage 2 asked four things:

- whether the seven new cases in the floor-and-depth module fail under the mutations the phase files name, and whether `floor_and_fixes` still reads through the one reader rather than a local `== FLOOR_YES`
- whether the F8 removal from `seal/ledger.md` and its re-founding in the fragment leave every claim about the permissive row true, and whether the eighteen re-read rows still hold
- whether the gate prompt's option 1 wording, rendered, matches the pin in `tests/test_routing_is_recorded.py`, and whether restoring any one of the seven old sentences turns the new module red
- whether the six `survivors.md` rows excuse what they quote on grounds that hold, and whether the five points work item A inherits (`plan.md` Alternatives) remain true of the landed code

The hand-back labelled the broad gate unverified; the sealer answers that after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal/ledger.md`'s F4 note says F8 carries its claim forward; this branch removed F8 from that file, so the note is false and the hygiene workflow's `survivor_check.py --range origin/<base>...HEAD` exits 1 on it at the pull request | `seal/ledger.md:777`, `seal/ledger.md:785` | **fixed** `9493d34c` | fixed at 9493d34c — the two paste-ready edits applied as given: `seal/ledger.md` line 777 lists F8 as *until #138 removed it*, and the F4 note carries `**Corrected 2026-09-24 by work item 1790173106 (#138)**` pointing at the fragment's B2. Verified on the committed tree with the CI form (`survivor_check.py --range origin/release/v0.15.0...HEAD` with every `survivors.md`): exit 0, re-run by the orchestrator at `506b030a`. The three ⬜ paperwork rows went in `b871c3c7` and `506b030a`: the memo counts thirteen mutations; `terminal_value`'s refusal names each row's own reason; and the six `survivors.md` rows stay, because the round's *one place* reading was the check silencing itself — a row's quote is an added sentence whose n-grams `corrected` collects and `wanted` subtracts, which is #507/#308, work item B of this release; executed: CI form exit 1 at `7604e522` on `seal/ledger.md:784`; exit 0 with the paste-ready correction committed in the clone; the smith's range `659b4229..HEAD` does not surface it |
| ⬜ | `overview.md` says ten mutations; the phase files table thirteen (M1–M13) | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/overview.md:12` | not a defect | read; paperwork correction under `seal/specs/`, kept out of `Needs a fix` |
| ⬜ | `survivors.md` excuses six reports; at the target SHA the same range produces one (`chain_check.py:2960`), so five rows anchor nothing | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:3` | not a defect | executed: `survivor-check --range 659b4229..HEAD` reports one place |
| ⬜ | `terminal_value`'s refusal for the floor line explains `Needs a fix`'s count, one row off | `skills/code-review/scripts/round_record.py:1365` | not a defect | read; the behaviour and the fact are right, the sentence is one row off |
| 🟢 | one reader for the reopening question, three callers, no local `== FLOOR_YES` left on the `Needs a fix` cell | `skills/code-review/scripts/chain_check.py:2392`, `:3147`, `:3262`; `skills/code-review/scripts/round_record.py:1931` | not a defect | read and executed grep; M1 and M3 killed |
| 🟢 | a bare `yes` refused at the reader in the floor row's words under `NEEDS_FROM`'s grandfathering, and it stops the count of nothing | `skills/code-review/scripts/chain_check.py:3256-3309` | not a defect | executed: A1, A2, A3 green; M1, M2, M3 killed |
| 🟢 | `round_record.py new` refuses a bare `yes` on either terminal line, and the printed bound reads through the gate's reader | `skills/code-review/scripts/round_record.py:1359`, `:1931` | not a defect | executed: M5 killed both parametrised cases, M6 killed the bound case alone |
| 🟢 | the three #138 carriers and the seven #241 places say what stands and no longer say what is gone; the gate's option pinned through the rendered prompt | `tests/test_the_direct_answer_owes_the_sealers_record.py`, `tests/test_routing_is_recorded.py:255`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:1297` | not a defect | executed: M4, M7, M8, M10, M12 killed; the standing phrase occurs once per file, twice in the orchestration skill |
| 🟢 | the declaration table row's three excusals match `direct_seal`; no third `Review` answer, no change to `hooks/routing.py` | `docs/review-chain-spec.md:743`, `skills/code-review/scripts/chain_check.py:3910-3935` | not a defect | read against the code and the diff stat |
| 🟢 | F8 removed and re-founded as B2; seventeen rows re-read with dated notes; `evidence-check --strict` green; Q1 is zero | `seal/ledger.md`, `seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md` | not a defect | executed: 1565 ok · 0 drifted · 0 broken; grep for a bare `yes` cell finds none |
| 🟢 | the five points work item A inherits remain true of the landed code | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/plan.md:89-109` | not a defect | read |
| ❓ | the broad gate — full suite, repository-wide lint, typecheck | — | out of verified scope | the sealer's, after the rounds settle; the prompt labelled it unverified and ordered no run |

## Paste-ready fixes

```
seal/ledger.md:777 — replace
only mutation or a review round found (F3, F6, F8, F9, F10, F11). F12 is the
with
only mutation or a review round found (F3, F6, F9, F10, F11, and F8 until
#138 removed it — see the F4 note below). F12 is the
```
```
seal/ledger.md:784-786 — replace
is REMOVED rather than re-pointed and its claim is carried forward by F8 —
which says more than F4 did, because the reason for the rename is part of the
claim now. -->
with
is REMOVED rather than re-pointed. **Corrected 2026-09-24 by work item
1790173106 (#138)**: F8 carried F4's claim forward, and F8 has left this file
too — its bare-`yes` reading went with the code — so the claim now lives in
`seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md`
B2, which the fold moves under this file's `### 1790173106` heading. -->
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over twelve modules in the clone at `7604e522`: the floor-and-depth module, `test_the_record_is_generated.py`, `test_a_record_precedes_the_fixes_it_commissions.py`, `test_the_direct_answer_owes_the_sealers_record.py`, `test_routing_is_recorded.py`, `test_waiver_decided_at_start.py`, `test_docs_line_wrap.py`, `test_one_word_one_meaning.py`, `test_chain_check_at_the_pull_request.py`, `test_the_run_stops_at_the_last_finding.py`, `test_a_record_says_why_it_was_written_late.py`, `test_no_real_identifiers.py` | `540 passed in 225.90s`. The status of that call was read through `\| tail`, so the summary line is the evidence and the status is not; the mutation probe's baselines over the same modules returned 0 directly |
| mutation probe, one file `test_tmp_mutations.py` (NAME NOT IN TREE: deleted after the run), each mutation applied by an exact single-match substitution, the module run through the clone's venv with the exit code read directly, the file restored from git and `git status` clean after each | M1 — 4 failed (`…fails_after_the_cutoff`, `…prints_before_the_cutoff`, `…does_not_stop_the_count`, `test_says_reopened_is_the_one_reader_of_the_reopening_question`); M2 — 3 failed (the three walk and row cases); M3 — 1 failed (`…does_not_stop_the_count` alone); M4 — 1 failed (`test_each_carrier_says_a_bare_yes_is_refused[parts1]`); M5 — 2 failed (both labels); M6 — 1 failed (`…is_no_reopening_here_either`); M7 — 1 failed (`…requires[parts2]`); M8 — 1 failed (`…requires[parts0]`); M10 — 1 failed (`test_the_first_option_says_what_the_direct_answer_owes`); M12 — 1 failed (`…why_two_answers_and_not_three`). All killed |
| `bin/evidence-check --strict` at `7604e522` | exit 0; `total: 1565 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records: 1 work item read, 128 names read, 0 refused |
| `bin/survivor-check --range 659b4229..HEAD --exempt seal/specs/1790173106-…/survivors.md` (the smith's range) | exit 0; one survivor, `chain_check.py:2960`, exempt; *every survivor is excused by a row above (1)* |
| `python3 skills/code-review/scripts/survivor_check.py --range cbb58091...HEAD` with every `seal/specs/*/survivors.md` (the hygiene workflow's form) | exit 1; `seal/ledger.md:784` shares *the rename is part* / *of the claim* with removed F8, score 1.77 — 🟡 1 |
| the same form at a probe commit carrying the paste-ready fix for 🟡 1, committed from Python in the clone and reset afterwards | exit 0; `correction-check --range cbb58091...HEAD` exit 0; `evidence-check --strict` 1565 ok; `test_docs_line_wrap.py`, `test_a_merge_cannot_silently_drop_a_correction.py`, `test_no_real_identifiers.py` — 86 passed with the edit in the tree |
| Q1: `grep -rn -E '^\| *Needs a fix *\| *\**yes\**\.? *\|' seal/specs/*/rounds/*.md tests/` | no match (exit 1); no live cell reads `yes` alone |
| `uvx ruff check` and `uvx ruff format --check` over the seven changed `.py` files | `All checks passed!`; `7 files already formatted` |
| the broad gate — full suite, repository-wide `ruff`, typecheck | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
