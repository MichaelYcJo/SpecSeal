# 1790260566-a-row-inside-a-fence-reads-as-live — review round 2

| Field | Value |
|---|---|
| Target SHA | 32fb90bd1d11d241398b223fb831945f8622aa1b |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 593 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790260566 is the verifying round: the diff of round 1's fixes, 70fe19ca..91fcb4e5, at 32fb90bd, together with the merge of release/v0.15.3 (#588, #587). Its job is whether round 1's verdicts are closed, whether the two new cases are correct, and whether settle.py's changes from both sides compose and the notes union was kept.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — the record generator's fence walk takes the closer and backtick-info rules | `skills/code-review/scripts/round_record.py:1324` | confirmed | read; the new case red with `fd16c522^`'s file restored and green at the target, executed |
| 🟢 | round 1's finding 2 is closed — the re-point matches in `unquoted` and splices from the original | `hooks/root-migrate.py:419` | confirmed | read, and offsets hold (`unquoted` keeps each character's position); the new case red with `fd16c522^`'s file restored and green at the target, executed |
| 🟢 | round 1's finding 3 is closed — six carriers narrowed and the readers outside the rule named | `skills/verify/scripts/unverified_check.py:238` | confirmed | read; a tree search for the old phrasings finds only scoped or config-reader sentences; the named readers exist |
| carried | The correction check reads a fenced example row as a row | `skills/evidence-check/scripts/correction_check.py:356` | deferred #584 | already deferred in round 1; untouched by the fix diff, and now named in `fence_opener`'s docstring |
| carried | The release fold's demote walk keeps its own fence rule | `.github/scripts/fold_ledger.py:245` | deferred #584 | already deferred in round 1; untouched by the fix diff, and now named in `fence_opener`'s docstring |
| 🟢 | round 1's ⬜ 6 still holds — no empty comment of that shape in the tree | `skills/evidence-check/scripts/evidence_check.py:2242` | confirmed | executed: a search of `seal/specs/` finds no instance; the fix diff changes no code in that file |
| 🟢 | round 1's ⬜ 7 still holds — both ledger walks split the same way | `skills/evidence-check/scripts/evidence_check.py:223` | confirmed | read; `quoted_lines` and `unquoted` are unchanged by the fix diff |
| 🟢 | round 1's ⬜ 8 is closed — phase 1's failure direction names both directions | `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md` | confirmed | read; the refusal it cites is `NEVER_CLOSED` at `round_record.py:457` |
| 🟢 | The merge composes `first_cell`'s container class with this branch's `settle.py` docstrings | `skills/settle/scripts/settle.py:450` | confirmed | read: no common line; executed: the settle module passes on the merged tree |
| 🟢 | The merge keeps both sides' notes on D1 and E1, and each anchor's hash is the editing side's | `seal/releases/0.15.1.md` | confirmed | executed: a row-by-row compare over base, both parents and merge; `correction-check` over the merge reports no dropped marker; `evidence-check` 0 drifted |
| ⬜ 1 | `repoint`'s line-count comment names `follow`, which the fix removed | `hooks/root-migrate.py:435` | open | read; a stale name in a comment and no behaviour change |
| ⬜ 2 | The opener half of `fenced_after`'s fix has no case; R1-1 claims it | `tests/test_the_record_is_generated.py:1995` | open | executed: with that half removed, 129 of 129 pass; the proposed case is red there and green at the target |
| ⬜ 3 | The merge note on D1 and E1 says one unit carries both sides' edits; each unit carries one side's edit | `seal/releases/0.15.1.md` | open | a correction to paperwork; read: this branch's hunk is in `CONTRIBUTING.md`, and the release side's is at `docs/the-evidence-ledger.md:71` |
| ❓ | Behaviour on Linux and Windows | the fix diff | ❓ out of verified scope | macOS only here; CI's matrix answers it at the pull request |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `test_the_record_is_generated`, `test_the_root_migrates_itself`, `test_settle_reads_before_it_removes`, `test_a_merge_cannot_silently_drop_a_correction`, `test_unverified_rows_close` at `32fb90bd` | 504 passed, exit 0 |
| `bin/test tests/test_release_hygiene.py` at `32fb90bd` (the #588 fragment-row rules, over this branch's new R1-1 and R1-2) | 51 passed, exit 0 |
| The two new cases with `fd16c522^`'s `round_record.py` and `root-migrate.py` restored in the clone | both failed, exit 1: prose copied and a fix line lost; the fenced `.specseal/` path rewritten to `seal/`. The files were restored and the status is clean |
| `fenced_after` mutated in the clone, each half removed in turn, then the whole record-generator module run | closer half off: 1 failed (the new case), 128 passed; opener half off: 129 passed |
| The proposed opener-half case, appended to the module from a probe | green at the target, red with the opener half off; appended text and mutation removed, status clean |
| A row-by-row compare of the eleven ledger files the merge changed, over `c52e8350`, both parents and `32fb90bd` | no note lost at the merge; D1 and E1 hashes are each the editing side's; S1 removed on the release side and kept removed |
| `bin/correction-check --range c52e8350..32fb90bd` | exit 0; 1 merge examined, no correction marker dropped |
| `bin/evidence-check .` at `32fb90bd` | exit 0; 2,157 ok, 0 drifted, 0 broken; records arm 474 names, 0 refused |
| `bin/fold-check` at `32fb90bd` | exit 0; 14 documents held to 1,000 lines, 0 listed over it |
| The broad gate (full suite, lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, after the rounds settle |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
