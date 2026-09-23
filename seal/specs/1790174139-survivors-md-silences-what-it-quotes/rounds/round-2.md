# 1790174139-survivors-md-silences-what-it-quotes — review round 2

| Field | Value |
|---|---|
| Target SHA | 84c6c5ffde5bfd6969e620c2d3358d8bd773f483 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 539 |
| Broad gate | 0f6c7b1f against cbb58091 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no — ⬜ a is a correction to a ledger fragment and a phase record under `seal/`, and the rule keeps it out of this line |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of the survivor sweep, the verifying round at round 1's fixes: the range `e7dacbf8..09292fa8` on `fix/308-survivors-md-silences-what-it-quotes`, two commits, plus the record commit that closed round 1. It asked whether 🟡 1 is closed as the record says — `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` now runs on a 4-file and a 33-file pool, and with the `phases/` arm of `records_a_past_state` removed each arm goes red on its own assertion, the small pool on exit code and the large pool on the record named beside `guide.md` — and whether the three paperwork corrections state what the tree holds: the `Ran by` row closed in `overview.md`, the mutation counts at 6/6 in `phases/phase-4.md` and ledger E1, the memo's red-run count as eleven over ten cases, and E3 re-read with the mutation in the phase-2 table. It also asked whether the fix range touched anything outside the test module and the work item's own records. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's 🟡 1 is closed: the pool case runs on 4 and 33 files and each arm goes red on its own assertion with the `phases/` arm removed | `tests/test_a_corrected_sentence_survives_elsewhere.py` `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` | answered | Executed: module 70 passed; arm removed → `[0]` exit 0 nothing named, `[29]` names `guide.md` and the phase record at 1.60, `2 failed`; restored `2 passed`, bytes equal |
| 🟢 | The `Ran by` row is closed and read as closed; the memo's eleven-over-ten count follows from the phase records; E3's re-read and the phase-2 bullet match the executed output message for message | `overview.md` §*Not verified* row 2 and line 12; `phases/phase-2.md`; ledger row E3 | answered | Executed: `unverified-check` reads `2 open · 1 closed`, `evidence-check --strict` exit 0 with `@e64fda0b`; read: 6 + 4 + 1 over ten names, the two arm messages verbatim |
| ⬜ | E1 and phase-4 say *6 and 6 over the whole module*; on the committed module the `corpus` reversion turns 7 red, both arms of the parametrised pool case among them | `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` E1; `phases/phase-4.md` §*Mutations* | answered — corrected at 664309f0 | Correction; executed counts 7 and 6 over the 70-case module; the figures written were round 1's, measured before the parametrisation the same fix pass committed |
| 🟢 | The fix range touched the test module and this work item's own records and nothing else; the record commit touched `round-1.md` alone; no unit added | the fix range `e7dacbf8..09292fa8` and `84c6c5ff` | answered | Read: five paths in the range, one of them the ledger fragment outside `seal/specs/<id>/`; `survivor_check.py` byte-identical to the worktree's and untouched since `8dc9390` |
| 🟢 | Round 1's six 🟢 verdicts stand — five carried on untouched files, the branch's own sweep re-executed in the CI spelling | `skills/code-review/scripts/survivor_check.py`; the branch's own range | answered | Carried: the predicate, call sites, `OWNER_DIR`, follow-up rows and the five places rest on files outside the fix range. Executed: nine `exempt` at exit 0 with 14 `--exempt` files, nine standing at exit 1 without |
| ❓ | Tree-wide `ruff check` and `ruff format --check`, and the full suite | the repository | out of verified scope | Not run in this round on §2 grounds; the hand-back labels them the sealer's and the orchestrator says it ran ruff at `09292fa8`. The sealer answers, and this round leaves nothing open, so that spawn is due |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:cacheprovider` in the clone at `84c6c5ff` | exit 0, 70 passed |
| mutation: `phases/` arm removed from `records_a_past_state`, the pool case's two arms selected by `-k` | exit 1, `2 failed`: `[0]` exit 0, `no removed wording is still standing` · `[29]` names `guide.md` and the phase record, both at 1.60 |
| the same selection with the bytes restored | exit 0, `2 passed`; SHA-256 equal to the committed bytes; `git status` empty; `HEAD` at the target before and after |
| mutation: `corpus` back on `records_a_past_round`, whole module | 7 red — S1, S2, S3, the added phase-record case, pool `[0]` and `[29]`, the path-list case |
| mutation: `corrected` back on `records_a_past_round`, whole module | 6 red — S1, S3, S4, the added and edited phase-record cases, the path-list case |
| `bin/evidence-check --strict .` | exit 0, 1569 ok, 0 drifted, 0 broken |
| `bin/unverified-check --baseline cbb58091… seal/specs/` | exit 0; this memo `2 open · 1 closed` |
| CI spelling: `python3 skills/code-review/scripts/survivor_check.py --range cbb58091…...HEAD` with the 14 `--exempt` files of `hygiene.yml`'s bash array | exit 0, 9 `exempt`, 0 standing, `every survivor is excused by a row above (9)`, 371 files, 36 removed sentences |
| the same without `--exempt` | exit 1, 9 standing |
| `bin/correction-check --range cbb58091…...HEAD` | exit 0, no merge commit in the range |
| `uvx ruff check` and `uvx ruff format --check` on the edited test file | exit 0, exit 0 |
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py tests/test_no_real_identifiers.py -q` (coverage probe over the record commit and the new prose) | exit 0, 77 passed |
| the first clone, named without the work item id in the shared scratch directory | module exit 1, 9 failed 61 passed; its reflog shows `HEAD` moved to `8ab72d81` at 00:50:54 and back at 00:51:49 by commands this session did not issue; result discarded, clone removed, everything above re-run in a clone named after the work item |
| the probe's leavings | two probe files in the scratch directory deleted; both clones removed; the worktree untouched except this file |
| Broad gate — full suite, tree-wide `ruff check`, `ruff format --check` | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py` `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py` `#records_a_past_state`, `#corpus`, `#corrected` | round 1's 🟢 — answered |
| round-1 | the branch's own range, `seal/specs/1790174139-survivors-md-silences-what-it-quotes/survivors.md` | round 1's 🟢 — answered |
| round-1 | `phases/phase-1.md`, `phases/phase-2.md`, ledger row E2 | round 1's 🟢 — answered |
| round-1 | `survivor_check.py#OWNER_DIR`, the parametrised case | round 1's 🟢 — answered |
| round-1 | `seal/follow-up.md` | round 1's 🟢 — answered |
| round-1 | `overview.md` §*Not done* | round 1's 🟢 — answered |
| round-1 | `seal/specs/1790174139-survivors-md-silences-what-it-quotes/overview.md`, *Not verified* row 2 | round 1's ⬜ — answered |
| round-1 | `phases/phase-4.md` §*Mutations*; `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` E1 | round 1's ⬜ — answered |
| round-1 | `overview.md` line 12 | round 1's ⬜ — answered |
| round-1 | `survivor_check.py#records_a_past_state` | round 1's ⬜ — not a defect |
| round-1 | the repository | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
