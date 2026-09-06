# Feature Specification: a run's report carries one comparison table

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/spec.md -->

Closes #170.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | the table is read by a person, so its cost is one comment per run rather than a gate; what is automated is the row nobody can produce by hand — the tokens |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* | already owns where a reading goes and what fills `Ran by`. The table is the run-level reading, so it belongs to the same section rather than to a new one |
| `docs/review-handoff-protocol.md` §*After the run — the per-segment bars* | the bars judge one segment against its kind; the table judges a run against the last run. Two instruments, and the document that owns the first names the second |
| `skills/agent-contract/SKILL.md` §14 | the token line is text a person reads and acts on, so it ships with a case that pins it |
| `skills/agent-contract/SKILL.md` §15 | every case here is seen red before it is planted, against the code at `f02cb11` |

## Scope

**In.**

1. `skills/verify/scripts/session_cost.py` prints a token line — turns,
   output, cache write, cache read — summed over the transcript it was given
   **and** every transcript under its `<session-id>/subagents/` directory, and
   the same numbers appear under `--json`.
2. `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*
   states the comparison table as the shape every run's report takes, names
   what each row is taken from, and states the counting rule for the token
   row.
3. `docs/review-handoff-protocol.md` §*After the run — the per-segment bars*
   names the run-level table beside the per-segment bars and says which
   judges what.
4. `skills/commit-pr-convention/SKILL.md` §*Pull request bodies* names the
   chain section's shape: the table, then what the rounds found.
5. Cases pinning each of the above, and a ledger fragment for the claims.

**Out.**

- **A checker that refuses a report with no table.** The owner's call of
  2026-09-05: documents and the token line only. The table's source is a pull
  request body and an issue comment, neither of which is in the tree, so a
  gate would read something CI does not have. Reopen it with a measurement,
  not with a preference.
- **Reading a verdict from the numbers** (#170 §*Not this*). The table makes
  two runs comparable; what a row means on one branch goes in the prose
  beside it.
- **A second segment-level meter.** The bars in the handoff protocol already
  judge a segment; nothing here changes them.
- **Changing `tools_per_turn` or `context_growth`.** They count turns that
  carry a tool call, the bars in `docs/review-handoff-protocol.md` are set
  against that definition, and the token line needs a different one. The two
  live side by side and the script says so.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The token row is one command | Given a run's main transcript with subagent transcripts beside it · when `session-cost <transcript>` runs · then the output carries turns, output tokens, cache write and cache read summed over all of them, and says how many transcripts it covered | `tests/test_session_cost.py`, hand sum over a fixture with one subagent |
| The sum is the three fields | Given a transcript whose `usage` blocks carry `output_tokens`, `cache_creation_input_tokens` and `cache_read_input_tokens` · when the line prints · then each column equals the hand sum of its own field | same file, fixture with known values |
| A message counts once | Given one assistant message written as several rows under one id · when the tokens are summed · then its `usage` is counted once | same file, split-message fixture |
| A segment measured alone still reports | Given a subagent transcript with no `subagents/` directory beside it · when the script runs · then the token line covers that file alone and names one transcript | same file |
| The old numbers do not move | Given the existing fixtures · when the script runs · then `tools_per_turn`, `model_s`, `command_s`, `repeat_*` and `context_growth` are unchanged | the existing cases in `tests/test_session_cost.py` stay green |
| A session finds the table where it already looks | Given a session that has just finished a run · when it reads `skills/verify/SKILL.md`'s measurement section · then the table's rows and each row's source are there | `tests/test_a_segment_feeds_the_flow_log.py` |
| The bars and the table are told apart | Given a reader of `docs/review-handoff-protocol.md` §*After the run* · when they reach the bars · then the text says the bars judge a segment and the table judges a run, and names where the table lives | a case in the same module as the other handoff pins |
| A PR body has one chain section | Given someone writing a pull request body for a chain-routed work item · when they read `skills/commit-pr-convention/SKILL.md` §*Pull request bodies* · then the chain section's shape is stated: the table first, then what the rounds found | `tests/test_the_pull_request_language_is_the_repositorys.py` or a new module |

## Data & interfaces

`session_cost.py --json` gains one object. Nothing existing is renamed or
removed — the moratorium on parsed fields (`tests/test_the_rules_have_one_owner.py`)
is about fields checkers read, and these are new:

```json
"tokens": {
  "transcripts": 4,
  "turns": 1245,
  "output": 790000,
  "cache_write": 9800000,
  "cache_read": 224000000
}
```

`turns` here counts assistant messages carrying a `usage` block, which is not
`tools_per_turn`'s denominator (messages carrying a tool call). Both stay, and
the script states the difference where it computes them.

## Open questions → questions.md
