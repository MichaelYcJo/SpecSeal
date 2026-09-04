# 1788486395-the-roll-opens-the-next-log-with-no-body — review round 1

| Field | Value |
|---|---|
| Target SHA | b1f7340 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — this round's fixes are not yet read; the round that opens them sets this cell |
| Contract changes | `find_baseline_issue` returned a number or `None` and now returns a number-and-note pair → `open_issue`; `_ladder_harness` returned the create list alone and now returns it paired with the sleeps → `test_a_milestone_that_cannot_be_set_does_not_fail_the_release`, `test_both_best_effort_arguments_failing_still_opens_the_issue`, `test_a_create_that_landed_despite_a_failed_call_is_not_retried`, `test_the_issue_main_just_closed_does_not_count_as_the_create_landing`, `test_the_landed_create_guard_retries_an_empty_reading`, `test_every_attempt_failing_still_exits_loudly`, `test_the_ambiguous_ledger_note_reaches_the_issue_it_is_about` |
| New units | `landed_create` (depth 1); `BASELINE_AMBIGUOUS_NOTE` (depth 1) |
| Needs a fix | yes — 🔴 1 the ladder's landing guard reads the issue `main` has just closed as proof the create landed, so a version's log is never created and the workflow goes green; five 🟡 beside it |
| Loses a record or crashes | yes — 🔴 1: on the fallback path the ladder exists for, a stale reading ends the release with no rolling log open, `main` printing `opened …`, and nothing red until the release after that |

- [ ] Pass

<!-- The six test functions this round's fixes planted are deliberately not in
`New units`, following the convention `1788472135/rounds/round-1.md` set and
this session accepted: a per-case function is shown whole by the diff, and
listing them buries the two units the verifying round has to open.

Depth was checked rather than assumed, on two independent grounds the
implementer gave: `templates/sdd-round.md:64` defines depth 1 as a unit added
by a fix answering a finding in code that predates the run, and
`skills/code-review/SKILL.md:347` makes depth 2 specifically a finding inside
a unit an EARLIER ROUND'S FIXES created. This is round 1, so no fix-pass unit
exists to be inside; `open_issue` is stronger still, since it exists at the
branch base `f187b39:155`. A build phase is not a fix pass. -->

## What this round was asked

The whole branch against `release/v0.8.0`, with seven named surfaces in order.
Four of them the implementer had named itself when it handed over, and the
prompt said to take those as leads to verify rather than as findings already
made: the best-effort ladder's step attribution being inference rather than a
parse of `gh` stderr; a shipped skill pointing at a `.github/` path that does
not exist in an installed repository; nothing checking `flow-baseline`'s
exactly-one-open; and the re-read guard the implementer added for a hazard the
plan had not named — a create that fails after GitHub accepted it, retried,
opening a second issue.

Three more were the orchestrator's: the blast radius of `open_issue` gaining a
third argument, whether the seven pins already reading that skill section
survived the new prose, and the two zeroes — a label with no history against a
label with history and nothing open.

The prompt also corrected an inherited fact rather than letting the round
re-derive it: `evidence-check --reverify` has no row selector but `--ledger`
narrows it to a file, 11 anchors against 481, verified by the orchestrator
before the round started.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The ladder's landing guard reads `list_open_issues` without excluding the issue `main` just closed. A `gh issue list` lagging that close answers with it still open, the guard reads that as *the create landed*, and no issue is created for the next version while `main` prints `opened …` | `roll_flow_measurement_issue.py:298` | fixed at `1ead0b1` | The module's own docstring at `:44` is what the guard leans on — *a lag can only produce a reading short a result, never one with an extra issue in it* — and it was written about a reading taken after a **label add**. This branch created one taken after a **close**, where the same lag produces exactly the extra issue that sentence rules out. `phases/phase-4.md` records the implementer reproducing that lag on `flow-baseline` the same day. Not an exceptional path: the first rung always fails whenever the milestone cannot be resolved, which is the case the ladder exists for. The reviewer executed both halves in a probe |
| 🟡 2 | The same guard trusts an empty reading with no retry, where `open_flow_measurement_issues` retries for exactly this lag | `roll_flow_measurement_issue.py:298` | fixed at `1ead0b1` | Closed by the same unit. Louder than the 🔴 — a second issue opens and the next release fails on two-or-more — which is why it was not one |
| 🟡 3 | The recovery message asserts the log has zero open issues, when a create that reported failure may already have landed. Somebody following it opens the second | `roll_flow_measurement_issue.py` `main` | fixed at `1ead0b1` | `list_open_issues` uses `run`, which exits, so a stumble mid-ladder reaches that message. The two cases reading it check only `89`, `0.8.0` and `LABEL`, so the wording could move |
| 🟡 4 | The section's first sentence still names one destination — the sentence #136's own body quotes as the defect | `skills/verify/SKILL.md:313-317` | fixed at `1ead0b1` | Imperative and complete, with the two-logs paragraph only after it. The reviewer confirmed none of the twelve cases read that sentence, so it could be reworded and now has a pin |
| 🟡 5 | `flow-baseline`'s zero was folded into *always harmless*, so a durable ledger somebody closed by hand reads exactly like a repository that never measured | `skills/verify/SKILL.md:356-358` | fixed at `1ead0b1` | The prose four paragraphs earlier gives both labels the same invariant. `overview.md` records that nothing machine-checks it, which is a different statement; the fold had grounds nowhere |
| 🟡 6 | Two records: `phases/phase-4.md` read `<pending>` while `plan.md` carried the commit, and `docs/flow.md`'s tick arrived undeclared | `phases/phase-4.md:10`, `docs/flow.md` | fixed at `1ead0b1` | The tick's content is true and the release checklist wants it, but it is a shared file changed outside the plan and recorded nowhere. Taken off this branch rather than declared — PR #144 was already open on its own branch for that one character, and two pull requests carrying it is a conflict waiting for whichever merges second |
| 🟡 7 | `find_baseline_issue` picked `issues[0]` where two are open — the guessing the skill's own prose refuses | `roll_flow_measurement_issue.py:239` | fixed at `1ead0b1` | Raised by the round as a note rather than a finding. The implementer took it as 🟡 5's class one file over (§12) and separated the two silences: no durable ledger stays silent, because a note about that would print on every rolling log in every repository |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: probe reproducing the stale-positive reading | `try_run` creates 1, `run` creates 0 — a version's log never created, `main` printing success |
| reviewer: probe reproducing the stale-empty reading | two issues open |
| reviewer: `.venv/bin/pytest` × 3 modules at `b1f7340` | 53 passed |
| reviewer: `uvx ruff check` and `format --check` on the three changed Python files | clean |
| implementer: three cases red at `b1f7340`, two more red after the return-shape change, two skill cases red before the prose moved | as named in its report |
| implementer: 14 mutations | 2 survived, both closed, then 14 killed |
| `evidence-check --ledger 'seal/ledger/1788486395-*.md' .` | 18 ok, 0 drifted, exit 0 — and `--ledger` scoping kept `--reverify` off S8, which still reads `45edf260` |
| `fold_ledger.py --version 0.8.0 --dry-run` · `bin/unverified-check` | exit 0 · exit 0 |

## Inherited coordinates

Round 1 — nothing to inherit. What it was handed instead was the implementer's
own four leads and the corrected `--reverify` fact.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `gh issue create --milestone`'s failure ordering, and whether the body renders as intended | `overview.md` §Not verified | the repository owner, at the 0.9.0 roll |
| The full suite, repository-wide lint and typecheck | `overview.md` §Not verified | the orchestrator's single broad run, after the rounds settle |
| `seal/ledger.md` S8, still the one row `evidence-check .` stops at | work item `1788472135`'s memo | the repository owner |
