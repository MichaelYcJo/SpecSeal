# 1788449488-measure-what-flow-finds — review round 1

<!-- seal/specs/<unix-epoch-seconds>-<slug>/rounds/round-<N>.md — what this round of the
review chain did, written by the review orchestrator right after it posts. -->

| Field | Value |
|---|---|
| Target SHA | 0d59003dcec63d7d6af8c1dc68ba34d11a083538 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 `.github/scripts/roll_flow_measurement_issue.py:170-173`, close-then-open ordering left no recovery hint in the failure message when `open_issue` fails after `close_issue` succeeds |

- [ ] Pass

## What this round was asked

Fresh work item, no earlier round. Read `spec.md`, `plan.md`, `questions.md`,
`overview.md`, and all three `phases/phase-{1,2,3}.md` first.

Ten things named to attack, in order: (1) the release script's core
invariant, mutation-checked from the reviewer's side — `next_version`'s
purity and correctness including edge cases (`0.9.9`, `0.10.2`) the
branch's own tests might have missed; the retry logic firing only on a
zero-open reading, never on two-or-more; `main()` actually failing loudly
after the retry; (2) the workflow wiring — same trigger, same checkout, env
vars actually set for the new step; (3) the skill instruction's honesty
about the no-op case and the transcript-path mechanic; (4) a LIVE query
confirming the label state is exactly `#89`; (5) `docs/flow.md`'s edit —
section actually deleted, both checkboxes ticked, `#89`'s own line correctly
left alone; (6) test-pass claims, re-run fresh plus mutation of at least 3
cases; (7) gate/hook boundary; (8) English-only; (9) `plan.md`'s Status
column; (10) the "no ledger row" judgment, checked against the actual
docstring and test rather than trusted.

One extra axis named for this branch specifically, beyond the standard
table: this branch calls an external service (`gh`) with side effects
(closing/opening a real issue) at release time, so "what happens if `gh`
itself fails mid-operation" was named as a real axis worth a finding if the
script doesn't address it — not a security/concurrency axis in the usual
sense, but the equivalent for a script whose two writes are not atomic.

Facts handed as coordinates: the target SHA, branch/base, the specific file
and line ranges to open first. Left to the reviewer: whether the account's
claims (49→wait, 48 at this SHA, pre-fix — passed, exit 0; the retry
asymmetry; the ledger judgment) actually held, none adopted on the
implementer's word.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Close-then-open ordering in the release rollover script has no recovery hint in the failure message when the open half fails after the close half already succeeded — an operator debugging a red release step would have to separately check GitHub state to know what actually happened | `.github/scripts/roll_flow_measurement_issue.py:170-173` (pre-fix) | **fixed** `2b2003b` | Round 1's own reading: neither the docstring (which thoroughly documents the retry-asymmetry trade-off) nor `overview.md`'s divergence table addressed this ordering at all — a genuine gap, not a documented and accepted trade-off. Round 2 (verifying) confirmed the fix by reading the code directly: `main()` now wraps `open_issue` in `try/except SystemExit`, re-raises naming the closed issue's number and a by-hand recovery instruction; `number` and `next_v` are both correctly in scope at the point of use |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` from `origin` at the given Target SHA | commit not found on `origin` — see Deferred; cloned the local checkout directly instead |
| Full read of `.github/scripts/roll_flow_measurement_issue.py`, `.github/workflows/close-issues-on-release.yml` | confirmed both, no issues beyond the one 🟡 above |
| `next_version` executed directly for `"0.9.9"`, `"0.10.2"`, `"9.99.99"` | `"0.10.0"`, `"0.11.0"`, `"9.100.0"` — all correct, `int()`-parsed, no string-slicing bug |
| 3 mutations against `roll_flow_measurement_issue.py` (drop minor bump; retry-on-two-or-more; let-zero-through) | all 3 confirmed red on the expected test each; restored, `git diff`/`git status` clean after |
| `uvx --with pytest python3 -m pytest tests/test_a_segment_feeds_the_flow_log.py tests/test_a_release_rolls_the_flow_measurement_issue.py tests/test_release_hygiene.py tests/test_docs_line_wrap.py -q` | 48 passed, exit 0 |
| `gh issue list --repo MichaelYcJo/SpecSeal --label flow-measurement --state open --json number,title` (live) | exactly `#89` |
| `git diff origin/release/v0.7.0...HEAD --name-only` | no `hooks/`, `chain_check.py`, `unverified_check.py`, `evidence_check.py` |
| `grep -rnP '[\x{AC00}-\x{D7A3}]'` across every diffed file | zero Hangul |
| `docs/flow.md` — `## While the flow runs` deleted, both checkboxes ticked, `#89`'s line untouched | confirmed by direct read |
| `.github/scripts/roll_flow_measurement_issue.py:35-47` docstring, and `test_two_open_issues_fails_loudly_without_retrying` | the retry-asymmetry reasoning is stated in full; the test is correctly named for it (confirmed by the mutation above) |

## Inherited coordinates

N/A — round 1, nothing to inherit.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Branch `feat/measure-what-flow-finds` had not been pushed past its routing-only commit when this round started — the given Target SHA did not resolve on `origin` | orchestrator error, disclosed in `#89`; fixed immediately (pushed `0d59003` and later `2b2003b` before the PR opens) | orchestrator — done, no further action |
