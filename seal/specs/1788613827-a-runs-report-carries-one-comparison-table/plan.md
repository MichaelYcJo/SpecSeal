# Implementation Plan: a run's report carries one comparison table

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/plan.md -->

## Summary

Two halves, and only one of them is code. The **token line** is the row of
the table nobody can produce by hand: #161's run summed `usage` over its
transcript and its subagents with a script written for that one occasion, and
the number is worthless for comparison unless the next run sums it the same
way. `session_cost.py` already opens exactly those files and already reads
`usage` — it throws away everything but `input_tokens` and
`cache_read_input_tokens`, and it reads one file where a run has several. The
**table** is prose: three documents state its rows, its sources, and where it
goes.

The order is the code first, because the last document to be written names the
command the first phase makes true.

## Technical context

- `skills/verify/scripts/session_cost.py#load` (`:64-135`) builds `turns`
  from messages that carry a `tool_use`, keyed by message id with the row uuid
  as a fallback, and records `input_tokens + cache_read_input_tokens` and
  `output_tokens` per turn. `analyse` (`:148-…`) turns that into
  `context_growth` thirds and `tools_per_turn`. **Neither `output_tokens` nor
  `cache_creation_input_tokens` reaches a printed line today**, and
  `cache_creation_input_tokens` is not read at all.
- `session_cost.py#newest` (`:293`) already knows the transcript layout: a
  run's subagents live under `<project-dir>/<session-id>/subagents/*.jsonl`,
  which is the directory named after the main transcript's own basename.
- `skills/verify/SKILL.md:312-420` owns where a reading goes; its step 1
  already names the subagent path. `tests/test_a_segment_feeds_the_flow_log.py`
  pins fourteen sentences of it, including
  `test_the_shipped_skill_names_no_repository_specific_tracker_state` — the
  table's rows must therefore name no issue number and no milestone.
- `skills/commit-pr-convention/SKILL.md` is under `tests/test_docs_line_wrap.py`'s
  `COVERED`: **88 display columns**. `skills/verify/SKILL.md` and
  `docs/review-handoff-protocol.md` are not covered; wrap them to match their
  neighbours anyway.
- `tests/test_session_cost.py`'s `message()` helper writes `usage` with
  `input_tokens` only, so every existing fixture sums to zero output and zero
  cache. New fields default to `0`, and the existing cases must not move.

**What breaks in six months.** A harness that stops writing
`cache_creation_input_tokens`, or writes the run's subagents somewhere else,
makes the line print a smaller number rather than fail — the same silence
`--latest` had on Windows before `newest` was fixed. The mitigation is the
transcript count printed beside the numbers: a run whose line says
`1 transcript` when six segments were spawned is visibly wrong to the person
who spawned them, which is the only reader who can tell.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A check that refuses a report with no table | The table lives in a pull request body and an issue comment. CI would have to fetch both, and a fetch that fails opens the gate | **rejected** — the owner's call, and the sources are outside the tree |
| Token line behind a `--tokens` flag | The flagless run stays the one everybody types, so the number the table needs is the one nobody prints | **rejected** — #170 asks for one command |
| Reuse `turns` for the token count | Its denominator sets `tools_per_turn`, and the bars in `docs/review-handoff-protocol.md` are calibrated against it. Widening it moves a published threshold silently | **rejected** — two counters, and the script says why |
| A separate `run_cost.py` over a whole run | Two scripts reading the same transcripts, and the second one is the only one anybody would need | **rejected** — `session_cost.py` already walks the directory |
| The table as a template under `templates/` | A template is copied into a work item's directory; this table is written into a pull request body | **rejected** — assumption 7 in `questions.md` |

## Phases

Vertical slices — each ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `session_cost.py` sums `output_tokens`, `cache_creation_input_tokens` and `cache_read_input_tokens` over the given transcript and every `<session-id>/subagents/*.jsonl` beside it, prints the token line with the transcript count, and reports the same under `--json`. Per-message dedup, and the existing counters untouched | `uv run pytest tests/test_session_cost.py -q` — new cases for the hand sum with one subagent, the three-field split, the split-message dedup, the no-subagents case; every existing case still green. Each new case seen red first | `2800051` |
| 2 | `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* states the comparison table — its nine rows, what each is taken from, the counting rule, and the partial-coverage sentence — naming no issue number | `uv run pytest tests/test_a_segment_feeds_the_flow_log.py tests/test_docs_line_wrap.py -q`, with new cases for the table's rows, the token counting rule, and the run-versus-segment distinction | |
| 3 | `docs/review-handoff-protocol.md` §*After the run — the per-segment bars* names the run-level table and says the bars judge a segment while the table judges a run; `skills/commit-pr-convention/SKILL.md` §*Pull request bodies* states the chain section's shape | `uv run pytest tests/test_the_handoff_before_round_one.py tests/test_docs_line_wrap.py -q` plus the new pins for both sentences | |
| 4 | The closing set: `seal/ledger/1788613827-….md`, `seal/specs/…/changelog.md`, `overview.md`, and `docs/flow.md`'s #170 box ticked | `uv run pytest tests/ -q` once, plus `uvx ruff check .` and `evidence-check` | |

## Operational impact

No migration, no new dependency, no env var. `session_cost.py --json` gains a
`tokens` object; nothing reads that output today except a person, so no
compatibility break. The `session-cost` wrapper in `bin/` needs no change.
