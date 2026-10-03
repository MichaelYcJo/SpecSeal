# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — review round 3

| Field | Value |
|---|---|
| Target SHA | 794cc6a28760176210ac2c48f817317aab944202 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 744 |
| Broad gate | 93ebd459 against 9511f6cd |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `794cc6a2` over round 2's fix range `70680f16..f7b31c42`. It was asked whether 🟡 4's paragraph states only what is true, executed by deleting the `Over the ceiling` row; whether C5's second re-stamp, C2's corrected note and the overview table hold; and whether the whole-tree checks are clean.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 4 is closed — F1 no longer says the `none` row keeps the ceiling check running; it names `Document line ceiling` as the ceiling | `docs/the-record-layout.md:179-182` | confirmed | executed: `fold-check` with the row deleted gives exit 0 on the tree and exit 1 on a padded arms file, the same output as with `none`; read: `skills/settle/scripts/fold_check.py#parse_over`, `#run`, `#declared`, `seal/config.md`, the cited section of `docs/the-evidence-ledger.md` |
| 🟢 | C5 re-stamped in place with a second dated Corrected note | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C5) | confirmed | executed: `evidence-check --strict` exit 0, 0 drifted; `correction-check` exit 0; read: the note, and the qualifier rule in `skills/evidence-check/scripts/correction_check.py` |
| 🟢 | round 2's finding 5 is closed — C2's note no longer says an absent row turns the check off | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C2) | confirmed | executed: the absent-row probe above; read: the note against `spec.md` D8 and the code |
| 🟢 | round 2's finding 6 is closed — K3 and D5 each have four cells, and K3 has its Grounds back | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27-28` | confirmed | executed: `awk` cell count, four on lines 22–28 (24 counts its escaped pipe); read: the diff of `f7b31c42` |
| 🟢 | the four checks over `794cc6a2` pass | `794cc6a2` | confirmed | executed: `evidence-check --strict .` exit 0, 0 drifted, 0 refused; `correction-check --range origin/release/v0.18.0...HEAD` exit 0; `survivor-check --range 2b1dcb1f...HEAD --exempt survivors.md` exit 0; `fold-check --root .` exit 0 |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check --strict .` | exit 0: 4080 ok, 0 drifted, 0 broken; records arm 5 work items read, 1217 names read, 0 refused, 0 drifted |
| `bin/correction-check --range origin/release/v0.18.0...HEAD` | exit 0: one merge commit examined in `9511f6c..794cc6a`, no correction marker dropped, no released ledger file changed |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt` this item's `survivors.md` | exit 0: 679 files against 66 removed sentences; one exempt place, 1790815613's overview line 49 |
| `bin/fold-check --root .` | exit 0: 157 statements in 18 documents, 0 listed over the ceiling of 1000 |
| a one-file `test_tmp_*` probe, run once and deleted: `fold-check` with `Over the ceiling` at `none` and with the row deleted, each on the tree and with the arms file padded to 2,650 lines | `none` and deleted gave identical output: exit 0 on the tree; exit 1 on the padded file, naming the arms file over the ceiling of 1000. Both files restored, clone status empty |
| `awk` cell count over `overview.md:18-30`, the pipe as separator | 4 cells on lines 22, 23 and 25–28; 5 on line 24, from its escaped pipe |
| `bin/test -q` over the docs line-wrap, fold-room and no-real-identifiers modules | 83 passed |
| the broad gate: full suite, repository-wide lint, typecheck | not yet. It belongs to the sealer and runs once after the rounds settle. Nothing in this round ran it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/the-record-layout.md:177` | round 1's 🟡 1 — fixed |
| round-1 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C1) | round 1's ⬜ 2 — answered |
| round-1 | `docs/the-commit-gate-inside-git.md:176` | round 1's ⬜ 3 — answered |
| round-1 | `docs/the-commit-gate-inside-git.md`, `docs/the-review-and-parity-arms.md`, `docs/commit-review-gate-spec.md` | round 1's 🟢 — confirmed |
| round-1 | the three files | round 1's 🟢 — confirmed |
| round-1 | live tree | round 1's 🟢 — confirmed |
| round-1 | `skills/settle/scripts/fold_check.py#ceiling_problems` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/`, `seal/releases/` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-record-layout.md` | round 1's 🟢 — confirmed |
| round-2 | `docs/the-record-layout.md:179` | round 2's 🟡 4 — fixed |
| round-2 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C2) | round 2's ⬜ 5 — answered |
| round-2 | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27` | round 2's ⬜ 6 — answered |
| round-2 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C5) | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | live tree outside `seal/specs/`, `seal/releases/`, `CHANGELOG.md` | round 2's 🟢 — confirmed |
| round-2 | ledger row C1; `phases/phase-1.md:68-76` | round 2's 🟢 — answered |
| round-2 | `overview.md:28` | round 2's 🟢 — answered |
| round-2 | `e8b487f0` | round 2's 🟢 — confirmed |
| round-2 | `b779daf2` | round 2's 🟢 — confirmed |
| round-2 | `rounds/round-1-report.md:141` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
