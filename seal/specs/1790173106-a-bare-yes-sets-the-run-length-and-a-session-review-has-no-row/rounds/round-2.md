# 1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row — review round 2

| Field | Value |
|---|---|
| Target SHA | 097634a4b0a24aef46f24f534654b4390f184055 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 537 |
| Broad gate | bcd49935 against cbb58091 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no — the one thing opened is a paperwork correction under `seal/specs/` (⬜ 1), and it goes to the orchestrator before the sealer is spawned, because `evidence-check --strict` refuses the record at `097634a4` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #138 and #241, the verifying round at round 1's fixes: the range `4f596a77..506b030a` on `design/138-241-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row`, three commits, plus the record commit that closed round 1. It asked whether 🟡 1 is closed as the record says — the F4 note in `seal/ledger.md` no longer names the removed F8, carries a dated `Corrected` marker pointing at fragment B2, and the hygiene form of the sweep (`survivor_check.py --range origin/release/v0.15.0...HEAD` with every `survivors.md`) exits 0 on the committed tree — and whether the three paperwork rows were answered truthfully: the memo's mutation count, `terminal_value`'s refusal sentence with A5 still green and the two re-stamped ledger rows holding, and the six `survivors.md` rows kept on the grounds that the round's one-place reading was the sweep silencing itself through the rows' own quotes (#507/#308, work item B). It also asked whether anything the fix range touched outside those three files changed behaviour. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's 🟡 1 — the F4 note in `seal/ledger.md` no longer names the removed F8, carries a dated `Corrected` marker pointing at fragment B2, and the CI form of the sweep exits 0 on the committed tree | `seal/ledger.md:777`, `seal/ledger.md:786` | answered | verified closed this round — executed: `survivor_check.py --range <base>...HEAD` with every `survivors.md` at `097634a4` — exit 0, one survivor (`chain_check.py:2960`) exempt; `correction-check` exit 0; read: both paste-ready edits applied as given, `F8` on no other line of the file |
| 🟢 | round 1's first ⬜ — `overview.md` counts thirteen mutations | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/overview.md:12` | answered | verified closed this round — read: *the thirteen mutations M1–M13 tabled in `phases/`* |
| 🟢 | round 1's second ⬜ — the six `survivors.md` rows kept, on the grounds that the sweep silenced itself through the rows' own quotes | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:3` | answered | executed: CI form at `b871c3c7` (rows dropped) — five places, exit 1; at `097634a4` (rows back) — one exempt, exit 0; with this item's file withheld from `--exempt` — `chain_check.py:2960` alone, exit 1. read: `corrected` collects the added sentences' n-grams, `wanted` subtracts them, and `records_a_past_round` excludes only `rounds/`; the six table rows are byte-identical across the range |
| 🟢 | round 1's third ⬜ — `terminal_value`'s refusal names each row's own reason, A5 green, both re-stamped rows hold | `skills/code-review/scripts/round_record.py:1365-1376` | answered | verified closed this round — read against `stopping_floor`'s two refusals; executed: 284 passed over five modules including the pin `carries no reason`; `evidence-check --strict` at `506b030a` 1565 ok, 0 refused, so `terminal_value@53032294` is the committed unit's hash |
| ⬜ 1 | the record's Grounds cell (`097634a4`) and the survivors header (`506b030a`) name `removed_sentences`, a function `survivor_check.py` does not have; the evidence checker refuses the record — exit 2 in CI's `ledger` job form and under `--strict` (NAME NOT IN TREE) | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/rounds/round-1.md:34`, `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:15` | answered — corrected at 916d1ba5 | paperwork under `seal/specs/`, kept out of `Needs a fix` per `agents/warden.md`; executed: `evidence-check --strict` exit 0 with 0 refused at `506b030a`, exit 2 with 1 refused at `097634a4`; the units are `corrected` and `wanted`. Must be corrected before the sealer runs, because `broad-gate` passes `--strict` |
| 🟢 | the fix range changed no behaviour outside the three files: the one code edit is a message string, and lint is clean | `skills/code-review/scripts/round_record.py:1365-1376` | not a defect | read against the diff; executed: `uvx ruff check` and `ruff format --check` clean |
| ❓ | the broad gate — full suite, repository-wide lint, typecheck | — | out of verified scope | the sealer's, after the rounds settle; the prompt labelled it unverified and ordered no run. This round leaves nothing needing a fix, so the sealer's spawn is due — once ⬜ 1 is corrected, or the strict form refuses the record |

## Paste-ready fixes

```
seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/rounds/round-1.md:34 — inside the 🟡 1 Grounds cell, replace
a row's quote is an added sentence whose n-grams `removed_sentences` subtracts, which is #507/#308
with
a row's quote is an added sentence whose n-grams `corrected` collects and `wanted` subtracts, which is #507/#308
```
```
seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:15-16 — replace
artefact, not a fact about the tree: `survivor_check.py#removed_sentences`
subtracts the n-grams of every sentence the range ADDED, and a row here quotes
with
artefact, not a fact about the tree: `survivor_check.py#corrected` collects the
n-grams of every sentence the range ADDED and `wanted` subtracts them, and a row here quotes
```

## Executed probes

| What was run | Result |
|---|---|
| `python3 skills/code-review/scripts/survivor_check.py --range cbb58091...HEAD` with all seven `seal/specs/*/survivors.md` as `--exempt`, at `097634a4` (the hygiene workflow's form) | exit 0; 403 files examined against 65 removed sentences; `exempt skills/code-review/scripts/chain_check.py:2960`; *every survivor is excused by a row above (1)* |
| the same at `097634a4` with this item's `survivors.md` withheld from `--exempt` (six exempt files, the file still in the tree) | exit 1; one place, `chain_check.py:2960` (`written_late_reason` against `run_reopened`'s old body at `:3099`, 2.00); the five F8 places do not appear |
| the same at `b871c3c7`, where the fix pass had dropped the five rows | exit 1; `chain_check.py:2960` exempt; five places reported — `docs/review-chain-spec.md:1418` (2.88), `chain_check.py:2374` (2.77), `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:356` (2.00), `seal/ledger.md:820` (2.00), `chain_check.py:2370` (1.88) |
| `bin/correction-check --range cbb58091...HEAD` at `097634a4` | exit 0; no merge commit in the range |
| `bin/evidence-check --strict` at `506b030a` | exit 0; `total: 1565 ok · 0 drifted · 0 broken`; `1 work item read · 165 names read · 0 refused` |
| `bin/evidence-check --strict` at `097634a4` | exit 2; `total: 1565 ok · 0 drifted · 0 broken`; `NOT-IN-TREE …/rounds/round-1.md:34 removed_sentences`; `167 names read · 1 refused` |
| `python3 skills/evidence-check/scripts/evidence_check.py .` at `097634a4` (the form `.github/workflows/test.yml:94` runs) | exit 2, the same refusal |
| `python3 skills/code-review/scripts/chain_check.py --baseline cbb58091…` at `097634a4` | exit 1 on this work item: `Broad gate` is `not yet` on a record judged as a ready pull request, and `Pass` is checked beside `Fixes checked by: nobody — the fixes are written and no round has opened them`. Both are the states this round's record replaces; the pull request is a draft |
| `bin/test tests/test_the_record_is_generated.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_a_merge_cannot_silently_drop_a_correction.py -q` at `097634a4` | 284 passed |
| `uvx ruff check` and `uvx ruff format --check` on `skills/code-review/scripts/round_record.py` | `All checks passed!`; `1 file already formatted` |
| `grep -n -E '\bF8\b' seal/ledger.md` at `097634a4` | two lines, 777 and 787, both inside the corrected note |
| `git diff 4f596a77..506b030a -- <survivors.md>` filtered to table lines | no table line changed; the header comment alone |
| grep for `removed_sentences` over `skills/` and `seal/` (NAME NOT IN TREE) | no definition anywhere; two mentions, `round-1.md:34` and `survivors.md:15` |
| the broad gate — full suite, repository-wide lint, typecheck | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/ledger.md:777`, `seal/ledger.md:785` | round 1's 🟡 1 — fixed |
| round-1 | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/overview.md:12` | round 1's ⬜ — not a defect |
| round-1 | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:3` | round 1's ⬜ — not a defect |
| round-1 | `skills/code-review/scripts/round_record.py:1365` | round 1's ⬜ — not a defect |
| round-1 | `skills/code-review/scripts/chain_check.py:2392`, `:3147`, `:3262`; `skills/code-review/scripts/round_record.py:1931` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/chain_check.py:3256-3309` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/round_record.py:1359`, `:1931` | round 1's 🟢 — not a defect |
| round-1 | `tests/test_the_direct_answer_owes_the_sealers_record.py`, `tests/test_routing_is_recorded.py:255`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:1297` | round 1's 🟢 — not a defect |
| round-1 | `docs/review-chain-spec.md:743`, `skills/code-review/scripts/chain_check.py:3910-3935` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger.md`, `seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md` | round 1's 🟢 — not a defect |
| round-1 | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/plan.md:89-109` | round 1's 🟢 — not a defect |
| round-1 | — | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the sweep silences a survivor through the `survivors.md` row that quotes it, whether or not the file is passed as `--exempt` | already deferred: #507/#308, work item B of this release (`fix/308-survivors-md-silences-what-it-quotes`) | the owner of `survivor_check.py`, in that work item |
