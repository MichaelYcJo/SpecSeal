# 1790260566-a-row-inside-a-fence-reads-as-live — review round 3

| Field | Value |
|---|---|
| Target SHA | 6c538abc7c46ec820249d6e2fc631e4bc0a2be69 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 593 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `1df2947930bcc15a50c59de8ed86526b7291c59c..1df2947930bcc15a50c59de8ed86526b7291c59c`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790260566 is the last, verifying round: the diff of round 2's fixes, ff112c0d..e8fbe7b9, at 6c538abc, with the record correction ff112c0d. Round 2 closed on a fix and spent the one reopening, so this record ends the run.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's note 1 is closed — `repoint`'s line-count comment names the splice, not the removed `follow` | `hooks/root-migrate.py:435` | confirmed | read: the comment names the splice at line 421, no `follow` helper remains, and nothing but the comment changed |
| 🟢 | round 2's note 2 is closed — the opener half of `fenced_after` has its case | `tests/test_the_record_is_generated.py:2014` | confirmed | executed: green at the target; red with the opener half removed, green with the closer half removed; the round 1 case is red only for the closer half |
| 🟢 | round 2's note 3 is closed — the D1 and E1 merge note says which side edited which anchored unit | `seal/releases/0.15.1.md` | confirmed | executed: per-parent hunks from `c52e8350` put this branch's only House rules hunk at line 298 and the release side's only anchored evidence-ledger hunk at line 71; a record correction, corrected at ff112c0d |
| 🟢 | The new unit is correct — the case pins the backtick-info opener rule and nothing else | `tests/test_the_record_is_generated.py:2014` | verified | read and executed: CommonMark §4.5 is cited correctly; the discriminating assertion is the prose one |
| 🟢 | The fix's ledger edits keep every claim true | `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` | verified | executed: evidence-check 0 drifted, 0 broken; release-hygiene module green; S8 and 0.13.1's section row carry dated re-read notes |
| ❓ | Behaviour on Linux and Windows | the fix diff | ❓ out of verified scope | macOS only here; CI's matrix answers it at the pull request |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the new case and round 1's case at `6c538abc` | 2 passed, exit 0 |
| The same two cases with `fenced_after`'s opener condition reduced to a bare match, in the clone | exit 1: the new case failed, round 1's case passed |
| The same two cases with the closer's empty-info condition removed instead | exit 1: round 1's case failed, the new case passed; file restored, clone status clean |
| `bin/test` over `test_the_record_is_generated`, `test_release_hygiene` and `test_the_root_migrates_itself` at `6c538abc` | 222 passed, exit 0 |
| `bin/evidence-check .` at `6c538abc` | exit 0; 2,158 ok, 0 drifted, 0 broken; records arm 525 names, 0 refused |
| `bin/correction-check --range 5e3aab5c..6c538abc` | exit 0; no merge commit in the range |
| `git diff -U0` from `c52e8350` to each parent of `32fb90bd`, over `CONTRIBUTING.md` and `docs/the-evidence-ledger.md` | this branch: House rules line 298 and the fold section line 300; release side: the content-anchor section line 71 and two hunks past it |
| The broad gate (full suite, lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, and with this round it has come due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:1319` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/root-migrate.py:419` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py:123`, `skills/verify/scripts/unverified_check.py:237`, `skills/evidence-check/SKILL.md:295`, `skills/evidence-check/SKILL.md:427` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py:356` | round 1's ⬜ 4 — deferred |
| round-1 | `.github/scripts/fold_ledger.py:276` | round 1's ⬜ 5 — deferred |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2242` | round 1's ⬜ 6 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:229` | round 1's ⬜ 7 — answered |
| round-1 | `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md` | round 1's ⬜ 8 — answered |
| round-1 | the whole diff | round 1's ❓ — out of verified scope |
| round-2 | `skills/code-review/scripts/round_record.py:1324` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/unverified_check.py:238` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/fold_ledger.py:245` | round 2's carried — deferred |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:223` | round 2's 🟢 — confirmed |
| round-2 | `skills/settle/scripts/settle.py:450` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.15.1.md` | round 2's 🟢 — confirmed |
| round-2 | `hooks/root-migrate.py:435` | round 2's ⬜ 1 — fixed |
| round-2 | `tests/test_the_record_is_generated.py:1995` | round 2's ⬜ 2 — fixed |
| round-2 | the fix diff | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
