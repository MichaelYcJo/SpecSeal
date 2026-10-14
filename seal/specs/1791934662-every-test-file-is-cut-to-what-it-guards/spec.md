# Feature Specification: every test file is cut to what it guards

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here asks a person. A removal, a rebuilt file and a kept case are each proven by a run; a bound is a row CI reads |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The one row this item adds (`slowest-job`) is a gate: its case seen red, the direction (it blocks more), a prompt budget of zero, a `Reads:` line per unit. A decision extracted into a pure function is a code change reviewed like any, with its battery red before and after |
| `docs/the-evidence-ledger.md` §*A claim held by a test*; §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | Every released row citing a test id a batch removes or renames gets one `Corrected ·` row in `seal/ledger/1791934662-….md`, naming the new case; one row per citation, never a bulk pass; no released file changes |
| `docs/the-reader-registry.md` §*Who declares*; §*A frame names what its work removes* | Every unit a batch adds to shipped code carries a `Reads:` line; `## Removes` below |
| #929's `seal/specs/1791876666-…/spec.md` §*A case names what it guards*, §*The regrowth check*, §*Rows for seal/budgets.md* (cc4ab070) | The `Kills:` line, `case_check.py`, `tests/unguarded-files.txt` and the five rows, read not changed; the proof model this item assumes is its Q2 (i), one run per function reading the killer set, which the orchestrator passes to #929's smith as the default |
| #930's `seal/specs/1791876665-…/spec.md` §*The budgets* (661dc60b) | The ratchet; `ci-minutes:*` and the new `slowest-job` row lowered to the measured value in the pull request that lowers it |
| #931's `test.yml` `durations` job (a8335041) | Each batch downloads its run's union (`gh run download <id> -n test-durations`) |
| #923's `seal/specs/1791933022-…/spec.md` §*The boundary with #929* (6969c487) | A case asserting on this tree's prose is lined here and never removed or re-pointed here |
| `skills/agent-contract/SKILL.md` §7, §15 | A battery run leaves nothing and is bounded by `--timeout`; a new case is seen red first |
| `skills/implement/SKILL.md` §*3. The SDD file set* | Rows, a list and shipped units change, which is the top rung |

## Scope

**In.** The 180 test files #929's phases do not open, rebuilt or cut per shipped module so that the suite protects no less than today and a pull request waits no longer than a few minutes. Two strategies, chosen per file by measurement (`## The two strategies`): **rebuild** for a file that is heavy, redundant or whose proof alone would hold the `cases` job past 5 minutes — 65 files; **cut** per case under #929's criterion for a file already fast and thin — 115 files. Where a module's decision is tangled with git, filesystem or process calls, the batch first extracts it into a pure function in the shipped code. Every kept or new function carries a `Kills:` line; every batch leaves `tests/unguarded-files.txt`, lowers its rows and commits its run's durations union. The whole item lands in 0.22.0 (the owner, 2026-10-14).

**Out, and whose.** #929's five files and mechanism; the strategy applied to #929's remaining phases (`questions.md` Q1, a row for its smith; its frame is not edited here). Prose-pinning cases' removal or re-pointing (#923, #940, #941). Which legs run (item B). `.test_durations`' cadence (#931). The budget mechanism (#930). A suite-wide census job.

## What the remaining suite is

`executed` 2026-10-14 at f35e1f57 on macOS arm64; commands in `plan.md` §*Technical context*.

| | Value |
|---|---|
| The suite | 13,914 cases · 185 files · 5,475 functions · 157,736 lines in `tests/test_*.py` (160,228 in `tests/*.py`) · 7,861 Windows seconds priced. Run 38487467049 (c98576a7): slowest job 12.3 min (Windows shard 3; shards 7.9–12.3), ubuntu 8.5 as one job, macOS shards 5.0–7.3 |
| **The 180 remaining** | **8,850 cases · 5,071 functions · 142,559 lines · 5,316 s** · 3,591 released ledger citations of their ids (24 files with none) · 466 `Enforced by:` ids (79 files with none) · 45 files carry `skipif`/`pytest.skip` |
| Prose-pinning (#929's measure, errs over) | 998 functions · 1,470 cases · 31 files over half prose. Own: 7,380 cases · 4,073 functions |
| **Rebuild set, 65 files** | 5,978 cases · 2,432 functions · 80,721 lines · **4,441 s** · 2,062 ledger citations · 259 `Enforced by:` ids. Of them the fourteen heavy files: 2,085 cases · 1,086 functions · 36,604 lines · 2,702 s · 949 citations |
| **Cut set, 115 files** | 2,872 cases · 1,641 functions · 61,838 lines · 876 s · 1,529 citations · 207 ids |
| How two heavy files are built (`executed`, `ast`) | `test_chain_check_at_the_pull_request.py`: 148 functions, 138 take the `repo` fixture (a git repository each), 138 spawn, 38 call a module unit directly and 27 of those call `git`; `chain_check.py` has 93 units, 72 of them pure. `test_the_fixes_close_the_record.py`: 96 functions, 88 take `repo`, 75 spawn, 83 go through `fix_table` and 70 through `close`, which run `round_record.py` as a process; `round_record.py` has 105 units, 79 pure. Each case builds a repository and runs a script to test a decision over a record's text |
| Tangled decisions (`executed`, errs over: a unit that reads a file then decides counts) | units with I/O and ≥ 3 branches: `chain_check.py` 13 · `round_record.py` 13 · `evidence_check.py` 15 · `seal.py` 15 · `broad_gate.py` 12 · `worktree-guard.py` 12 · `survivor_check.py` 7 · `unverified_check.py` 6 · `commit-review-gate.py` 4 · `session_cost.py` 4 · `config.py` 3 · `worktree_consent.py` 2 · `optin.py` 2 · `gate.py` 1 · `review-history-guard.py` 1 · `cmdline.py` 0 · `issue_claims_check.py` 0 — 110 |
| The port list (`executed`, errs over: a docstring or name citing `#NN`, a round, a platform, CRLF, quoting, locale, `env`, `PATH`, a symlink, encoding) | 597 of the fourteen files' 1,086 functions; per file in `## Targets` |
| Sample of five files, operator-swap mutants (`executed`) | every killed mutant had ≥ 3 killers, median 10–15 or the whole file; no sampled mutant had one killer; 4–5 of 8 survive one file against a module other files also load. A battery is a module's; a single file's survivors are not its own |

## The two strategies

**Rebuild** — the file is heavy (≥ 60 Windows s), parametrized (≥ 3 cases a function), twinned (≥ 20 % of its functions share a body shape), or its lining alone would run the `cases` job past 5 minutes at one run a function. Per shipped module, in this order, each step in the phase record:

1. **Baseline.** The module's mutant battery — one mutant per sentence of the module its tests name, bounded by `--timeout` — is run once against the **old** files that load the module. The set of mutants killed is the baseline, committed in `phases/phase-N.md` with each mutant's killers.
2. **Reference.** The old file's cases that encode a real bug of a platform, a path, CRLF, shell quoting or the environment — the port list, read case by case from the measured list, which errs over — are ported, one each, with their `Kills:` line.
3. **Extraction.** Where a decision the tests need is tangled with git, filesystem or process calls, the batch extracts it into a pure function in the shipped module (inputs in, verdict out), with a `Reads:` line, the caller left thin; the module's battery is red before and after, so the behaviour is unchanged. The frame names the modules (`## What the remaining suite is`); the phase names the units.
4. **New tests, per unit**: the decision as a pure function over an input → output table, and one end-to-end case per real path — git, hooks, filesystem, process. Every function carries a `Kills:` line. A thin old case that alone kills a mutant stays as it is.
5. **Non-inferiority, then deletion.** The new file kills every mutant the baseline killed; a miss gets a case. Only then is the old content deleted. The new tests live at the old path, so every citation is re-pointed by unit, one `Corrected ·` row each, and every `Enforced by:` line in the same pull request.
6. **Proof on the run.** The `cases` job proves each new function at one run a function on the fast file; under 5 minutes by the file's seconds target.

**Cut** — the file is fast and thin: #929's criterion unchanged, a case removed only where the file without it still kills every mutant it killed, every kept function lined.

## Targets

**Bounds every pull request of this item meets.** The `cases` job ≤ 5 minutes (`questions.md` Q1 asks #929's smith for the job's `timeout-minutes` and the message *restructure: test the decision directly*). No `pytest` job slower than the previous pull request's slowest: `ci-minutes:*` lowered to the measured leg after each cut, and a new row **`slowest-job`** — the longest `pytest` job's minutes on the run, read by the `budgets` job beside `ci-minutes:*`, one-sided — lowered the same way. End of item: `slowest-job` ≤ 5 min.

**The path there**, in Windows seconds (`executed` today; the rest estimated and re-set by each phase's record): 7,861 today → ≈ 6,497 after #929 (the commit-gate and sealer files' own figures, the enumerations at half) → ≈ 2,549 after this item: the fourteen heavy files 2,702 → ≤ 253, the 51 other rebuilt files 1,739 → ≤ 370, the 115 cut files 876 → ≈ 745. Scaled on run 38487467049, the slowest Windows shard 12.3 → ≈ 4.0 min, ubuntu 8.5 → 2.8, macOS 7.3 → 2.4.

**Per-file seconds targets for the fourteen** — the smaller of ten end-to-end paths at today's per-case price plus one second, and what keeps the `cases` job under 5 minutes at half today's functions; re-set from the phase's path inventory (Q4):

| File | Cases · functions | Today s | Target s | Port list |
|---|---|---|---|---|
| `test_chain_check_at_the_pull_request.py` | 186 · 148 | 374.9 | ≤ 19 | 59 |
| `test_the_fixes_close_the_record.py` | 119 · 96 | 482.1 | ≤ 38 | 62 |
| `test_a_released_row_is_read_again_in_a_fragment.py` | 464 · 120 | 216.6 | ≤ 6 | 65 |
| `test_a_corrected_sentence_survives_elsewhere.py` | 177 · 145 | 293.0 | ≤ 18 | 82 |
| `test_the_record_is_generated.py` | 131 · 118 | 188.0 | ≤ 15 | 51 |
| `test_the_record_is_held_to_the_floor_and_the_depth.py` | 86 · 65 | 165.4 | ≤ 20 | 22 |
| `test_the_guard_asks_once_per_session.py` | 103 · 88 | 97.9 | ≤ 11 | 24 |
| `test_settle_reads_before_it_removes.py` | 132 · 106 | 106.6 | ≤ 9 | 50 |
| `test_a_row_points_by_content.py` | 200 · 135 | 58.6 | ≤ 4 | 70 |
| `test_a_record_precedes_the_fixes_it_commissions.py` | 56 · 53 | 161.1 | ≤ 30 | 19 |
| `test_a_fix_of_a_fix_is_counted.py` | 61 · 22 | 331.0 | ≤ 55 | 13 |
| `test_the_last_rounds_fixes_are_checked.py` | 76 · 55 | 125.6 | ≤ 18 | 20 |
| `test_unverified_rows_close.py` | 198 · 117 | 47.0 | ≤ 4 | 41 |
| `test_the_records_can_be_carried_out_and_in.py` | 96 · 78 | 53.7 | ≤ 7 | 19 |

**Rows at the item's end**, against #929's end values, each re-set by the ratchet from the batch's table: `test-cases` ≤ 10,500 → **≤ 8,000** (the rebuild set's 5,978 cases to about half, the cut set by shape twins, bare functions and a tenth); `test-lines` ≤ 150,000 → **≤ 125,000**; `unguarded-files` ≤ 175 → **0**; `suite-seconds` → ≈ 2,550; `slow-file:*` empty of this item's files; `ci-minutes:*` and `slowest-job` at the measured end.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the shape on one module | phase 1's `hooks/cmdline.py` batch: baseline, port list, new tests, deletion, the cut of its two thin files, the `slowest-job` row | `phases/phase-1.md` with cases, lines, seconds, the `cases` job's minutes and the slowest job before and after |
| S2 the baseline is taken once from the old tests | a module's battery against the old files | the killed set and each mutant's killers in the phase record, before any file changes |
| S3 nothing protects less | the new file against the baseline | every baseline mutant red; a miss gets a case seen red first |
| S4 regressions are ported | the file's port list | each case ported with its `Kills:` line, or named with why no mutant and no platform needs it |
| S5 a tangled decision is extracted first | a module in the tangled list | the pure function with its `Reads:` line; the module's battery red before and after the extraction commit |
| S6 one end-to-end case per real path | the new file | the phase's path inventory: each path (git, hooks, filesystem, process) with its one case |
| S7 the file meets its seconds | a rebuilt file | ≤ its target in the run's durations, or the inventory's figure with the reason |
| S8 every function declares and the file leaves the list | any batch | `Kills:` on every function; the files out of `tests/unguarded-files.txt`; `case_check.py` exit 0 |
| S9 the rows move | any batch | `test-cases`, `test-lines`, the per-file rows, `slow-file:*`, `ci-minutes:*`, `slowest-job` lowered; the union committed; `budget_check.py` exit 0 |
| S10 every pull request fits | any batch's run | `cases` job ≤ 5 min; no `pytest` job slower than the previous pull request's slowest |
| S11 the ledger and the docs follow, row by row | a cited id removed or renamed | one `Corrected ·` row per citation naming the new case; `Enforced by:` re-pointed; `evidence-check --strict .` exit 0; `tests/test_a_folded_statement_names_what_enforces_it.py` green |
| S12 prose pins move with the text | a prose-pinning function | lined, not removed; listed for #923 |
| S13 a cut file is cut by #929's criterion | a file in the cut set | the table: every mutant red before and after; a bare function removed on its run |
| S14 nothing asks a person | the whole change | no `AskUserQuestion`, no prompt |

## Data & interfaces

`seal/budgets.md`: one row `slowest-job` (minutes, one-sided, gate) with its measurer in `budget_check.py` reading the run's `pytest` jobs as `ci-minutes:*` does; its case seen red. Per batch: rebuilt test files at their old paths, cut files, extracted pure functions in the shipped modules named above; rows out of `tests/unguarded-files.txt`; ceilings lowered; `.test_durations` from the run's `test-durations` artifact; `Corrected ·` rows in `seal/ledger/1791934662-every-test-file-is-cut-to-what-it-guards.md`; `Enforced by:` lines re-pointed in place; `changelog.md` here; `phases/phase-N.md` with the baseline table, the port list, the path inventory and the three lists (removed · ported · left to #923).

## Removes

nothing — the frame names no unit: a rebuilt file keeps its path and the functions that leave it are each batch's baseline table, so every removed function is a divergence row in `overview.md` citing that table, with its `Corrected ·` ledger row where a released row cites it, as `docs/the-reader-registry.md` §*A frame names what its work removes* has it and as #929's frame does.

## Open questions → questions.md

Framed 2026-10-14 by framer, before the build.
