# 1788449488-measure-what-flow-finds — review round 2 (verifying)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/rounds/round-<N>.md — what this round of the
review chain did, written by the review orchestrator right after it posts. -->

| Field | Value |
|---|---|
| Target SHA | 2b2003b0ab4c12ebd2115cbc4789d23efb28f157 |
| PR | not yet opened |
| Broad gate | ran at 05b4258 vs. base origin/release/v0.7.0 — 1853 passed · 1 skipped (4 pre-existing failures, unrelated, same #127 as #121+#119); ruff check/format clean; evidence-check 451 ok · 0 drifted · 0 broken |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 1's one fix landed (`2b2003b`),
targeted at the diff of that fix only — not the whole branch. Job: the
answer, not new findings. Specifically: (1) is round 1's 🟡 actually closed —
read the new code directly, not just confirm something changed near the
line; (2) any new unit the fix created, treated as a finding surface per
this repo's own rule (a unit the fixes create has been reviewed by nobody);
(3) run the new regression test fresh and mutate the fix to confirm the test
targets its actual claim; (4) re-run the full 4-module set from round 1 as a
regression check; (5) read `overview.md`'s new divergence-table row and judge
whether it honestly describes the issue and the fix, or minimizes it; (6)
English-only on the touched files.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|

No findings. Round 1's 🟡 (see round-1.md) is fixed — verified by reading
`.github/scripts/roll_flow_measurement_issue.py:186-197` directly:
`main()` wraps `open_issue` in `try/except SystemExit`, re-raises via
`sys.exit` naming the already-closed issue's number and a by-hand recovery
instruction (label + title). `number` is bound before `close_issue` runs and
still in scope in the `except` block; `next_v` is computed once and reused
for the recovery title, so the recovery message names the same version the
script would otherwise have opened. New units: none — the fix is a
`try/except` inside the existing `main()`, no new top-level function. The
new test (`test_close_succeeds_but_open_fails_names_both_in_the_message`)
was mutated (issue number dropped from the message) and confirmed to go red
specifically on that assertion, not on anything else nearby.
`overview.md`'s new row was read directly and found to state the issue, the
prior behavior, the fix, and the grounds without minimizing.

## Executed probes

| What was run | Result |
|---|---|
| `git show 2b2003b` (full diff) | read in full |
| `.github/scripts/roll_flow_measurement_issue.py` post-fix | read in full |
| `uvx --with pytest python3 -m pytest tests/test_a_release_rolls_the_flow_measurement_issue.py::test_close_succeeds_but_open_fails_names_both_in_the_message -q` | 1 passed, exit 0 |
| Mutation: drop the issue number from the recovery message, re-run the same test | 1 failed, exit 1, on the specific number assertion; restored, clean after |
| `uvx --with pytest python3 -m pytest tests/test_a_segment_feeds_the_flow_log.py tests/test_a_release_rolls_the_flow_measurement_issue.py tests/test_release_hygiene.py tests/test_docs_line_wrap.py -q` (warden, then re-run independently by the orchestrator) | 49 passed, exit 0, both times |
| Non-ASCII scan on the three touched files | em-dashes only, no Hangul, no other non-English text |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/roll_flow_measurement_issue.py:186-197` | the fixed code — re-opened directly this round rather than trusted from the commit message |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |
