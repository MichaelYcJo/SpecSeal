# 1791384162-the-macos-test-leg-runs-in-shards — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | af700273 (the budget is 3aac7d8f) |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Read run 37700567455, which the orchestrator dispatched at 3a946dd0 after
phase 1's push and which concluded `success` with every job green. Read the
summary lines and the `--durations=50` heads from the job logs, then build
`plan.md`'s phase 2: S1's sum against ubuntu, S2's slowest shard against 12
minutes, the budget by the inherited rule, and the records — this file, the
ledger rows, the re-reads phase 1 listed, the two `plan.md` citations that
read drifted, the changelog entry and the closed overview. If S2 sent the
count to four, stop after the edit and hand back the run to start.

## What this phase found

**The measurement, run 37700567455 at 3a946dd0** (executed 2026-10-08: `gh
run view --json jobs` for the times, each job's log for its summary line).

| Job | `startedAt` → `completedAt` | Time | Summary line |
|---|---|---|---|
| macOS group 1 of 3 | 23:09:14 → 23:14:36 | 5 m 22 s | 6,164 passed, 9 skipped in 303.14 s |
| macOS group 2 of 3 | 23:09:13 → 23:15:37 | 6 m 24 s | 3,630 passed, 75 skipped in 364.49 s |
| macOS group 3 of 3 | 23:09:13 → 23:16:09 | 6 m 56 s | 2,945 passed, 4 skipped in 399.63 s |
| ubuntu | 23:09:09 → 23:17:33 | 8 m 24 s | 12,747 passed, 80 skipped in 487.48 s |
| Windows group 1 of 4 | 23:09:08 → 23:20:33 | 11 m 25 s | 2,720 passed, 17 skipped in 652.89 s |
| Windows group 2 of 4 | 23:09:08 → 23:16:04 | 6 m 56 s | 6,712 passed, 35 skipped in 390.49 s |
| Windows group 3 of 4 | 23:09:08 → 23:18:14 | 9 m 06 s | 1,021 passed, 101 skipped in 517.94 s |
| Windows group 4 of 4 | 23:09:09 → 23:21:01 | 11 m 52 s | 2,155 passed, 66 skipped in 675.82 s |

- **S1 holds.** The three macOS shards ran 12,739 passed and 88 skipped,
  12,827 in all. ubuntu ran 12,747 + 80 = 12,827, and the four Windows
  shards 12,827. That is eight more than 0.20.0's 12,819, which matches the
  eight cases phase 1 added to the helper's module.
- **S2 holds, and the count stays three (Q1, Q2).** The slowest macOS shard
  took 6 m 56 s, under the inherited 12 minutes with five to spare. The
  plan's arithmetic gave 7.3 minutes at balance and 10.5 at its 1.45 factor
  on the slower pace. The shards held 6,173, 3,705 and 2,949 cases, against
  the plan's 6,173, 3,698 and 2,948. By pytest's own time the slowest is
  1.12 times the mean (399.6 s on 355.8 s). macOS is off the run's critical
  path: the Windows shards finished last, at 11 m 25 s and 11 m 52 s.
- **S3: the budget is 15.** 1.5 times 6 m 56 s is 10 m 24 s, rounded up to
  5 minutes. The rule's base is one run here, where #841's had four; the
  unsharded leg varied 1.35 times across the plan's six runs, which would
  put the slowest shard at 9 m 23 s, still under 15.

**The `--durations=50` heads** (executed, from each macOS job's log; the top
three and the sum of the fifty):

- Group 1, 216.0 s in the fifty: 12.06 s
  `test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count`,
  10.26 s
  `test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base`,
  10.00 s
  `test_a_corrected_sentence_survives_elsewhere.py::test_a_run_that_removed_nothing_is_silent_and_says_what_it_read`.
- Group 2, 265.1 s in the fifty: 16.70 s and 14.78 s, the shell oracle
  `test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_cuts_every_admitted_body_where_the_reader_does`
  under zsh directly and through `eval`, and 15.91 s
  `test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent`.
  The oracle lands whole in group 2, as `plan.md` predicted.
- Group 3, 184.3 s in the fifty: 13.61 s
  `test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records`,
  6.20 s of setup for
  `test_the_seal_is_taken_once_by_the_sealer.py::test_a_repository_shipping_no_gate_runs_the_invoked_copy`,
  5.64 s
  `test_the_seal_is_taken_once_by_the_sealer.py::test_values_that_cannot_be_written_leave_the_seal_standing`.

**The records.**

- `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` gains one
  row per scenario, S1 to S5.
- 0.20.0's S8 said macOS 35, so it takes a `Corrected ·` row rather than a
  re-read.
- `evidence-check --reverify --into … --checked 2026-10-08` wrote five
  `Re-read ·` rows: 0.8.2's R3, 0.16.0's P1-1, 0.18.0's R3, and 0.20.0's S1
  and S2. Each claim was read first and holds. Pinned versions are still
  compared on the pip line, and the floor is still read from every matrix
  entry, now through `pytest_matrix`.
- `plan.md` lines 152 and 153 now quote the two released hashes without the
  coordinate form, which is the framer's sentence with only that changed.
- After these, `evidence-check --strict .` exits 0.

**A defect outside this work: a heading unit is cut at a `#` line inside a
fence.** 0.20.0's S9 and 0.8.2's R3 anchor
`CONTRIBUTING.md#"## Running the checks"`. Neither drifted, although phase 1
changed three sentences in that section (executed: `evidence-check .` after
ea43bac7). Reading `skills/evidence-check/scripts/evidence_check.py`, both
`heading_path` and `text_regions` end a section at the next line matching
`^#{1,6}\s`, with no fence check. That section has
`# or: pip install …` inside a ```` ``` ```` block at line 166, so the unit
holds lines 104 to 165. Everything after line 166 in the section is
invisible to every row that cites it. This work's S5 cites the two changed
paragraphs by their own lines instead. Whether the cut is the bug is a
judgment for whoever owns `evidence-check`. It is named in the hand-back for
the orchestrator to file, because this work item may not file an issue.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the macOS shards' provisional budget of 35 and the comment that said it was provisional | the measured 15 and its run id in `test.yml`'s `timeout` comment |
