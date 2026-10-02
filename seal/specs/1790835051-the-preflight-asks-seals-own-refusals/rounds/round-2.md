# 1790835051-the-preflight-asks-seals-own-refusals — review round 2

| Field | Value |
|---|---|
| Target SHA | a0c66d18ab7f7783d2fc14526dcbe8fb81d132a0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 714 |
| Broad gate | 3e9af52c against 5180b89e |
| Fixes checked by | no fixes to check |
| Fix range | `9438e00ebf108cc2e4784d39317270bbf04b73fe..c4c1780cfba3e407c755e4e09ea8b244eae2f401`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round at `a0c66d18`. Its diff is round 1's fix range `090cb32f..bab8dc4a`, plus the release merge `f3b18cff`, which no round had read. It was asked, for each of round 1's four `fixed` verdicts, whether the finding and its class are closed. The two that mattered most were whether `seal --check` now raises every refusal on the write path with nothing refusing between its return and `write_record`, and whether a full `seal` writes byte-identical output. It was also asked to judge the excused survivor, and to treat the six depth-1 units round 1's fixes added as a finding surface.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's yellow finding 1 is closed — `seal --check` asks `field_index`, `cell` and `hiders_close` above its return, and nothing between the return and `write_record` refuses | `skills/code-review/scripts/round_record.py:4602` | confirmed | Executed: 7 new or changed cases red at `090cb32f`; removing the `hiders_close` call killed the position and open-comment cases; a full `seal` byte-identical to `090cb32f` over five shapes; the write path's refusals identical with and without `--check`. Read: the guard at `:4606`, `write_record` at `:4611` |
| 🟢 | round 1's finding 2 is closed — each of the 48 re-stamped release rows carries a dated note naming #702 | `seal/releases/0.10.0.md` | confirmed | Read: 56 rows rewritten, 48 in release files all naming the work item, 8 in its own fragment; seven notes checked against the code. Executed: `test_one_word_one_meaning.py` exit 0 |
| 🟢 | round 1's finding 3 is closed — the text says `item_dir` reads the working tree and the chain arm reads HEAD, which is true, and the behaviour is right to keep | `skills/verify/scripts/broad_gate.py:2862` | confirmed | Read: `hooks/routing.py:290-370` against `skills/code-review/scripts/chain_check.py:1242` and `:1307` |
| 🟢 | round 1's finding 4 is closed — the ask names a record only where it is on disk, and the not-asked line says none or more than one | `skills/verify/scripts/broad_gate.py:2988` | confirmed | Executed: three cases red at `090cb32f`; the direct case red with `on_disk` reduced to `record is not None` |
| 🟢 | The survivor `bab8dc4a` excused is true as it stands | `docs/commit-review-gate-spec.md:765` | confirmed | Read: it names the commit gate alone, whose `for_branch` reads the working tree |
| 🟢 | The merge `f3b18cff` changes nothing this branch's code or documents do or say | `seal/releases/0.15.1.md` | confirmed | Read: rows G1, N3 and N4 from the branch, N2 from the release; the `SKILL.md` preflight sentence intact. Executed: `evidence-check .` 0 drifted; `correction-check` exit 0 over 2 merges |
| 🟢 | The six new units are correct and each case fails on its defect | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4535` | confirmed | Executed: red at `090cb32f` and under two mutations; the `cell` refusal is pinned by name only, and the preflight's value cannot reach it |
| ⬜ 1 | `spec.md` S1 counts seven refusals where `--check` now asks ten | `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md:35` | answered | corrected at c4c1780c: this work item's own spec.md, a correction rather than a fix; Read. Paperwork; a correction closing `answered` with `corrected at <sha>`, outside `Needs a fix` |

## Paste-ready fixes

```diff
--- a/seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md
+++ b/seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md
@@ -40,2 +40,6 @@
   verify-and-exit flag in this repository takes (`seal.py mode --check`,
   `fold_ledger.py --check`, `claude_block.py --check`).
+  **Corrected 2026-10-02 by round 2 (⬜ 1):** the refusals are ten, not
+  seven. The write path's callees `field_index`, `cell` and `hiders_close`
+  refuse too, and `--check` asks them since round 1's fix pass
+  (`eec243df`), which composes the record above its return.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check .`, unscoped, at `a0c66d18` | exit 0; 3451 ok, 0 drifted, 0 broken, 0 malformed, 0 overflow; records: 8 work items read, 0 refused, 0 drifted |
| `bin/correction-check --range 821e592d...a0c66d18 --root .` | exit 0; 2 merge commits examined, no correction marker dropped |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "write_path or check_returns or seal_check or preflight or direct_item or two_declarations or detached or undeclared or settled_item_preflights"` at the target | exit 0; 27 passed |
| The seven new or changed cases (`-k "write_path_refuses or check_returns or direct_item_preflights or settled_item_preflights or two_declarations"`) with `090cb32f`'s `round_record.py` and `broad_gate.py` copied over the clone's | exit 1; 7 failed; files restored by `git checkout` |
| The same seven with two mutations: the `hiders_close` call above the return removed, and `on_disk` reduced to `record is not None` | exit 1; 3 failed (the position case, `open-comment`, the direct case), 4 passed; files restored |
| A one-run probe file in the clone's tests (deleted after): a full `seal` by `090cb32f`'s tree and by the target's over copies of five shapes (settled, settled sealed twice, direct, direct sealed twice, capped) | first run exit 1 only on the temporary payload name `run_check` prints; rerun with that name normalised: exit 0, 5 passed, with the same exit, the same output and the same record bytes |
| The same probe: the three hand-edited shapes sealed in full by both trees and with `--check` by the target, and a pipe in `--broad-gate` | exit 0, 4 passed: exit 2 everywhere, identical text, record bytes unchanged, `--check`'s output equal to the full run's |
| `bin/test tests/test_one_word_one_meaning.py` | exit 0; 18 passed |
| The broad gate (full suite, repository-wide lint, typecheck) over this branch | not yet: it is the sealer's, and it comes due once this round's record is written |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:4579` | round 1's 🟡 1 — fixed |
| round-1 | `seal/releases/0.16.0.md` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2861` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2770` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2967` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2984` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2968` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/overview.md` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
