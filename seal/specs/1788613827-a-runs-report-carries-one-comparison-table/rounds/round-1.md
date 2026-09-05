# 1788613827-a-runs-report-carries-one-comparison-table — review round 1

| Field | Value |
|---|---|
| Target SHA | 4d277f1 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 173 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | count (depth 1); message_key (depth 1); report_tokens (depth 1); labelled (depth 1); test_the_location_buckets_are_the_repositorys_own_definition_of_a_record (depth 1); test_the_broad_gate_row_asks_for_what_the_cell_actually_carries (depth 1); test_the_section_says_which_transcript_is_the_runs_own (depth 1); odd (depth 1); test_a_transcript_with_usage_and_no_tool_call_still_reports_its_tokens (depth 1); test_a_usage_value_that_is_not_a_number_contributes_zero (depth 1); test_a_message_id_that_is_not_a_key_does_not_end_the_report (depth 1); test_a_tool_call_whose_id_is_not_a_key_loses_its_pairing_only (depth 1); test_a_row_that_is_not_the_shape_the_readers_assume_is_dropped (depth 1); test_the_report_tells_its_two_turn_counts_apart (depth 1); TABLE_ROWS (depth 1); test_the_refused_rows_are_the_owners_own (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the finding round, against `4d277f1` with base `a9a827b`. The
handoff named eight things to attack, in order, on the grounds that a spawn
prompt naming specific things to break bought the cheapest round this
repository has measured: the token line computed after `analyse`'s guard;
what `subagent_transcripts` can miss or double, including `--latest` landing
on a segment; the dedup and whether one word now carries two turn counters;
the claim that every degradation prints a smaller number rather than raising;
the table's four `Location` buckets against this repository's own definition
of a record; the three sentences under the table against #170's own words;
whether the pointer-instead-of-a-copy refusals rot loudly; and the seven
re-stamped `seal/ledger.md` rows, each opened at the target.

The two forms of the ledger check were named with what each is for, and the
unscoped read was the form asked for — a read narrowed to the work item's own
fragment is what let three rounds of an earlier work item report a clean
ledger while the pull request found fifteen drifted rows.

Facts arrived as coordinates with executed/read labels; the runner and the
`git -C` requirement were given in the form the round was to run them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The token line is computed after `analyse`'s guard, so a transcript with `usage` and no paired tool call prints nothing — the segment-token row's own source | `skills/verify/scripts/session_cost.py#main` | **fixed** `511d6b2` | fixed at 511d6b2 — `` — `token_totals` is summed before `analyse`'s guard, and the exit is kept only for a transcript carrying neither a paired tool call nor `usage`. A transcript with `usage` alone prints the token block and exits 0; executed: exit 1, stdout empty, and `--json` empty, on a two-row usage-only transcript |
| 🟡 2 | `token_totals` raises `TypeError` on a string `usage` field and on an unhashable `message.id`, against the docstring's *"Every way this degrades makes the totals SMALLER rather than raising"* | `skills/verify/scripts/session_cost.py#token_totals` | **fixed** `511d6b2` | fixed at 511d6b2 — `` — `count` and `message_key` carry the type check both readers assumed. The class had six members, four of them pre-existing in `load`; all six are guarded and the docstring now says what is true; executed: both tracebacks reproduced; no real transcript in ten sessions writes either shape |
| 🟡 3 | The `Location` row splits `record` from `ledger`, and *Records' share* counts only `seal/specs/**`, against the record definition in `docs/review-chain-spec.md` and `skills/code-review/SKILL.md` | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | **fixed** `a306d18` | fixed at a306d18 — `` — the buckets follow `docs/review-chain-spec.md`, and `overview.md` gains a divergence row quoting #170's cells and the policy sentence verbatim with the 45 %/48 % measurement; read, with the diff measured: 729 / 39 / 831 lines, so the share row reads 45 % or 48 % depending on which rule fills it |
| 🟡 4 | `Broad gate: how many times, at what SHA` names a cell that carries at most one SHA and no count, and that `round_record.py` replaces rather than appends | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | **fixed** `a306d18` | fixed at a306d18 — `` — the narrow half: the row reads `Broad gate: whether it has run, and at what SHA` and names what the cell holds. `templates/sdd-round.md` is untouched; the wide half is issue #174; read at `templates/sdd-round.md:33`, `docs/review-handoff-protocol.md:131`, `round_record.py:619,1348,1392` |
| 🟡 5 | The printed report carries `turns` in two meanings and two scopes with nothing distinguishing them | `skills/verify/scripts/session_cost.py#report` | **fixed** `511d6b2` | fixed at 511d6b2 — `` — `analyse` returns `call_turns`; the token line says a turn is any assistant message in every transcript counted, the batching line names its own denominator and scope; executed on a real transcript: 1.08 tools per turn printed beside 659 turns over 211 calls, which divides to 0.32 |
| ⬜ 6 | `transcripts` counts a file that opened and yielded nothing, while the docstring makes that count the coverage cross-check | `skills/verify/scripts/session_cost.py#token_totals` | **fixed** `511d6b2` | fixed at 511d6b2 — `` — the docstring says `transcripts` counts the files the walk opened rather than the files that contributed, and names `turns` as where a doubled run shows. No counting rule changed; executed: `transcripts: 2` with one unparseable subagent contributing zero; pinned as intended by an existing case |
| ⬜ 7 | `--latest` can land on a subagent transcript, and the skill names no way to find a run's main transcript | `skills/verify/scripts/session_cost.py#newest` | **fixed** `a306d18` | fixed at a306d18 — `` — one paragraph in `skills/verify/SKILL.md`: the run's main transcript is the `*.jsonl` directly under the project directory, and `--latest` usually lands on a segment; executed: the walk picks the segment and `subagent_transcripts` returns `[]`; the header keeps it visible |
| ⬜ 8 | The handoff protocol's new paragraph restates five row names in prose, which no case guards | `docs/review-handoff-protocol.md#"### After the run — the per-segment bars"` | **fixed** `a306d18` | fixed at a306d18 — `` — the gloss of five row names is gone; the refusal beside it covers all nine of the owner's labels, held to `skills/verify/SKILL.md` by `test_the_refused_rows_are_the_owners_own`; read |
| ⬜ 9 | Ledger row R1 records finding 2's overstatement as verified behavior | `seal/ledger/1788613827-a-runs-report-carries-one-comparison-table.md` | **fixed** `b34374e` | fixed at b34374e — `` — a record correction, so it drove no fix pass of its own: R1's overstatement is replaced by what the code now does, and the same claim was corrected in the changelog fragment and `plan.md`; executed, via finding 2 — a correction, not a round |

## Executed probes

| What was run | Result |
|---|---|
| `pytest` over the six modules the change touches | 91 passed |
| `uvx ruff check` over the five changed Python files | all checks passed |
| `evidence_check.py .` unscoped, from the worktree | exit 1 — 584 ok · 1 drifted · 0 broken; the drifted row is `templates/config.md#"# Repository config"` |
| `git diff --quiet a9a827b HEAD -- templates/config.md` | exit 0 — the drifted row is not this branch's |
| `session_cost.py` on a real 14-transcript session | 14 transcripts, 659 turns, 198,759 / 2,956,451 / 121,860,912; `calls` 211, `tools_per_turn` 1.08 |
| Scan of ten real sessions for `usage` message-id overlap | zero overlap main↔subagent and subagent↔subagent; 216 ids over 408 rows in one main transcript; `.meta.json` sidecars beside every transcript |
| Probe A — usage-only transcript, no tool call | exit 1, stdout empty, `--json` empty (finding 1) |
| Probe B — `output_tokens` as the string `12` | `TypeError: unsupported operand type(s) for +=` at `:309` (finding 2) |
| Probe C — `message.id` as a list | `TypeError: unhashable type: 'list'` at `:305` (finding 2) |
| Probe D — `output_tokens: 1.5` | prints `1.5`, no raise |
| Probe E — subagent transcript newer than its main | the walk picks the segment; `subagent_transcripts` returns nothing; `1 transcript` (finding 7) |
| Probe F — unparseable subagent transcript | `transcripts: 2`, `output: 100` (finding 6) |
| `git diff --numstat a9a827b..4d277f1`, bucketed | `seal/specs` 729 · `seal/ledger*` 39 · rest 831 (finding 3) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, the repository-wide lint and the typecheck | the broad gate, after the rounds settle — §2 and §3 keep them out of this round | the orchestrator |
| `subagent_transcripts` and `newest` on the Windows leg | `overview.md` §Not verified, unchanged by this round — I ran on darwin only | the Windows leg of the pull request's checks |
| The table as a thing a person actually fills, every row taken for one real run | `overview.md` §Not verified — this branch states the rows and prints one; findings 3 and 4 are what the first filling will hit | the orchestrator, in this branch's own pull request body |
| `templates/config.md#"# Repository config"` drift | pre-existing on `a9a827b`, not this branch's | the repository owner |
