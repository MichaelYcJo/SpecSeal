# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — review round 3

| Field | Value |
|---|---|
| Target SHA | 50520de |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 332 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of #30 is the verifying round after the run's one reopening, at the diff of round 2's fixes, `cd7ea2f..bd08f52` (six commits), not the branch. Its job is the answers: for each of the four `fixed` verdicts in `rounds/round-2.md` — 🟡 11, 12, 13, 14 — is it actually closed, re-derived by reverting the fix the way round 2's grounds describe rather than by reading the diff. Three of them need a further question. 🟡 11's repair tells a refusal before the write from a check that failed after it by a discriminator the message carries rather than by the exit code; ask whether that discriminator can appear in a message it does not mean to mark. 🟡 13's repair was rebuilt once: its first form added a module-level pattern constant — NAME NOT IN TREE, the fix removed it — and `round_record.py close` refused the fix table because that unit sat at depth 2, and the pattern moved inside `suite_counts` — so the surface to judge is a function that gained logic rather than a module that gained a name, and the question is whether the two reds the fix pass names still bind it. 🟡 14 gave `quote` a platform argument and left a residual its docstring names: `cmd.exe` expands `%VAR%` inside double quotes, so a path carrying a percent still breaks; judge whether naming it is the right treatment or whether it is a finding. Then the surface nobody has reviewed, which round 2's record names under `New units`: `SCALE_NOT_A_NUMBER`, `SEAL_EXCLUDED`, `set_checked_by` and the cases beside them, judged as code — `SEAL_EXCLUDED` in particular replaced two units the previous round created, so ask whether the replacement carries what both of them did. **This round is bounded**: `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* has been spent — round 1 met the floor and round 2 closed on a fix after it — so anything this round opens is reported as a `deferred #N` candidate with the issue it would become, never as a fix to commission, and `Needs a fix: no` is what ends the run. Facts handed over as executed by the orchestrator at the fix head: three modules 78 passed; `evidence-check .` unscoped 1,103 ok · 0 drifted · 0 broken; `survivor-check` over both the fix range and the branch range exit 0; ruff clean; and the mis-attribution the fix pass measured in `round_record.py#depth_two` is now issue #333, out of this work item's scope. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 11 | the gate tells the reader no cell was written, under a line saying `sealed` | `skills/verify/scripts/broad_gate.py:620` | answered | executed — `5a20202` reverse-applied to the source file alone; `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` red on `assert "the cell WAS written" in out.err`. Closed. Its pair stays green under the revert, correctly. The unpinned coupling is A below |
| 🟡 12 | a `Fixes checked by` nobody can read reaches the write | `skills/code-review/scripts/round_record.py:3022` | answered | executed — `0cbd6ad` reverse-applied; all three parametrisations of `test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary` red on `assert 1 == 2`, each printing `round-record: sealed …` and then the chain check refusing that row. Closed for values outside the shape; the shape itself is B below |
| 🟡 13 | a linter's error count still lands on the suite row, and an all-skipped run reports `exit 0` | `skills/verify/scripts/broad_gate.py:429` | answered | executed — `bd08f52` then `c0a139b` reverse-applied; `test_the_suite_row_reads_pytests_counts_and_not_a_linters` red on `assert '2 errors' == '1 passed'`, and the reverted unit returns `None` for `3 skipped in 0.10s` where `'3 skipped'` is asserted. The rebuild inside the function did not cost either red |
| 🟡 14 | `quote` has no case behind either branch, and the Windows branch does not quote for `cmd.exe` | `skills/verify/scripts/broad_gate.py:317` | answered | executed — `67cdbda` reverse-applied; all three parametrisations of `test_a_path_is_quoted_for_the_shell_of_either_platform` red on `TypeError: quote() got an unexpected keyword argument 'windows'`. The `%VAR%` residual is named rather than closed, and naming it is right for this unit — the close is `shell=True` one level up, which is D's neighbour and its own issue |
| 🟡 A | the gate's `sealed` discriminator is a literal whose other end is a `print` in another package, and nothing pins them | `skills/verify/scripts/broad_gate.py:620`, `skills/code-review/scripts/round_record.py:3066` | open | executed — the print changed from `sealed` to `wrote`; three modules 130 passed, exit 0, nothing red. With that in the tree the gate tells a reader `no cell was written` on the ending 🟡 11 exists for. The only case driving the discriminator stubs `seal_record` and supplies the literal itself (`tests/…:1243`), and ledger row S12 anchors only `broad_gate.py` |
| 🟡 B | `seal` accepts any `round-N` shaped checker, and on a last record every one of them is a lie | `skills/code-review/scripts/round_record.py:3022` | open | executed — `round-1`, `round-9`, `round-2.md` and `ROUND-1` each exit 1 with the cell written and `round-record: sealed …` printed, the post-write chain check then refusing on that same row. Same class as 🟡 12, one value over |
| ⬜ C | the sweep's exclusion guard reports an absent span as a last-`##` span | `tests/test_one_word_one_meaning.py:268` | open | executed — the exclusion pointed at a heading `skills/verify/SKILL.md` does not carry; the assert fires with *is the last `##` in the file*. `partition` returns `""` for both states and the guard reads only one of them |
| ⬜ D | the suite row's clock axis narrows the class rather than closing it, and an all-skipped run still seals | `skills/verify/scripts/broad_gate.py:429` | open | executed — `suite_counts("1 passed in 1s\nsomething took 2 errors in 3s\n")` is `'2 errors'`; no tool in this repository's row prints that shape. The second half is read: `3 skipped` now renders truthfully and nothing refuses the seal over it |
| ⬜ E | the vocabulary refusal names `nobody — <why>` as a permitted value and then refuses it | `skills/code-review/scripts/round_record.py:3026` | open | read — the sentence is true of the row and false of this subcommand. The instruction that follows is correct, so a reader who finishes the message is not stuck |
| ⬜ F | `rounds/round-2.md` carries the superseded module-level block for 🟡 13 beside a verdict row naming `bd08f52` | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2.md` §Paste-ready fixes | open | read — correction, out of `Needs a fix`. The trail is in `bd08f52`'s message and `survivors.md`, not in the record |
| ⬜ G | `rounds/round-2.md`'s 🟡 12 block shows a `removesuffix` the shipped predicate does not have | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2.md` §Paste-ready fixes | open | read — correction, harmless: `CHECKER_RE` accepts the `.md` suffix, so the two agree on every input |
| ⬜ H | the handoff's `three modules → 78 passed` does not match the module list the record names | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-3-asked.md` | open | executed — the three modules `round-2.md`'s probe row names give 130 passed in 25.33s at the fix head, which is 123 at `a46e642` plus round 2's seven new cases |
| ⬜ I | `rounds/round-3-asked.md:1` names a unit the tree does not carry, without the marker that exempts the line | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-3-asked.md:1` | open | executed — `evidence-check .` in the clone at `50520de` reports `1103 ok · 0 drifted · 0 broken` and one `NOT-IN-TREE` refusal, on that line. `round_record.py new` copies the paragraph into `round-3.md` verbatim, so the record inherits it. Correction, out of `Needs a fix` |
| 🟢 J | `SCALE_NOT_A_NUMBER` and the branch order in `check_scale` | `skills/verify/scripts/seal_stamp.py:154` | answered | executed — `nan` gets the not-a-number sentence, `-inf` the floor sentence, `inf` the ceiling sentence, `0.5` and `1.5` their own. The case pins the message it says and the message it must not say |
| 🟢 K | `SEAL_EXCLUDED` carries both units it replaced | `tests/test_one_word_one_meaning.py:181` | answered | read — each exclusion keeps its own file and span, so neither widened to a file; the rewrite also stops dropping the `" ## "` separator, which the old form could use to glue two words into a phrase. C is its diagnostic, not its logic |
| 🟢 L | `set_checked_by` | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1084` | answered | read — it returns what the module's own `read_bytes` returns, so the `before` it hands back compares cleanly, and nothing else in the module duplicates it |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_one_word_one_meaning.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` at `50520de` | 130 passed in 25.33s |
| `5a20202` reverse-applied to `skills/verify/scripts/broad_gate.py` alone, then its two cases | `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` red on `assert "the cell WAS written" in out.err`; `test_the_gate_with_record_prints_no_stamp_when_the_record_refuses` green |
| `0cbd6ad` reverse-applied to `skills/code-review/scripts/round_record.py` alone, then its cases | four red — three parametrisations on `assert 1 == 2` with `round-record: sealed …` in the output, and `test_seal_refuses_while_the_fixes_have_been_read_by_nobody` on `assert "read by no LATER round" in out` |
| `bd08f52` then `c0a139b` reverse-applied, then `test_the_suite_row_reads_pytests_counts_and_not_a_linters` | red on `assert '2 errors' == '1 passed'` |
| `suite_counts` read off the reverted unit for `3 skipped in 0.10s` | `None`, where `'3 skipped'` is asserted — the second red binds |
| `67cdbda` reverse-applied, then `test_a_path_is_quoted_for_the_shell_of_either_platform` | three red on `TypeError: quote() got an unexpected keyword argument 'windows'` |
| `round_record.py`'s write line changed from `round-record: sealed` to `round-record: wrote`, then the three modules | 130 passed, exit 0 — nothing red, and the gate's message flips to `no cell was written` on a written cell |
| `round_record.py seal` on a fixed-but-unread record with `Fixes checked by` set to `round-1`, `round-9`, `round-2.md`, `ROUND-1` | exit 1 on all four, cell written on all four, `round-record: sealed …` printed on all four, the post-write chain check refusing that row on all four |
| `suite_counts` over six shapes at the fix head | `'1 passed'`, `'3 skipped'`, `'768 passed, 1 skipped'`, `None`, `None`, and `'2 errors'` for a clock-carrying line after pytest's summary |
| `quote` over `tests/test_%PATH%.py`, `tests/a%b.py` under `windows=True` | percent signs returned live inside the double quotes, as the docstring says |
| the sweep's first exclusion pointed at a heading `skills/verify/SKILL.md` does not carry | the guard fires with *the excluded span … is the last `##` in the file* |
| `check_scale` over `nan`, `-inf`, `inf`, `0.5`, `1.5` | the not-a-number sentence, the floor sentence, the ceiling sentence, and the floor and ceiling sentences |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone at `50520de` | `total: 1103 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, and one `NOT-IN-TREE` refusal on `rounds/round-3-asked.md:1` |
| `bin/test tests/test_no_real_identifiers.py -q` with this report copied into the clone at its own path | 2 passed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:504-516` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2960-2971` | round 1's 🔴 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:373` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:315-338` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:344-349` | round 1's 🟡 5 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:186` | round 1's 🟡 6 — fixed |
| round-1 | `.github/scripts/run_tests.py:42-44` | round 1's 🟡 7 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:2988-2997` | round 1's 🟡 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:469`, `agents/sealer.md:132` | round 1's 🟡 9 — fixed |
| round-1 | `docs/one-root-by-lifetime.md:135` | round 1's 🟡 10 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:565-583` | round 2's 🔴 1 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2989-3010` | round 2's 🔴 2 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:415-425` | round 2's 🟡 3 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:331-380` | round 2's 🟡 4 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:386-395` | round 2's 🟡 5 — answered |
| round-2 | `skills/verify/scripts/seal_stamp.py:188-202` | round 2's 🟡 6 — answered |
| round-2 | `.github/scripts/run_tests.py:42-45` | round 2's 🟡 7 — answered |
| round-2 | `skills/code-review/scripts/chain_check.py:2992-2999` | round 2's 🟡 8 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:525-531` | round 2's 🟡 9 — answered |
| round-2 | `docs/one-root-by-lifetime.md:135`, `tests/test_one_word_one_meaning.py:166-182` | round 2's 🟡 10 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:570-583` | round 2's 🟡 11 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:3000-3010` | round 2's 🟡 12 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:313-322` | round 2's 🟡 14 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 A — the gate's `sealed` discriminator has no case tying it to the line `round_record.py seal` prints | `deferred #N` candidate, a new issue | the sealer, at the release — the run's one reopening is spent |
| 🟡 B — `seal` accepts any `round-N` shaped checker, including this round and one git does not carry | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ C — the sweep's exclusion guard reports an absent span as a last-`##` span | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ D — the broad gate seals over a suite in which nothing ran, and the clock axis leaves one displacing shape | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ E — `seal`'s vocabulary refusal lists a value it refuses | `deferred #N` candidate, a new issue | the sealer, at the release |
| the `%VAR%` residual in `quote`, closed only by removing `shell=True` from `compare_at_base` | ledger row S15's second tidy-up, labelled read | unowned — a candidate for the same issue as D |
| ⬜ F, ⬜ G — corrections in `rounds/round-2.md` | the record, not the tool | the orchestrator |
| ⬜ H — the handoff's suite count | this report | the orchestrator |
| ⬜ I — the missing marker in `rounds/round-3-asked.md` | the paragraph, before `round_record.py new` copies it | the orchestrator |
