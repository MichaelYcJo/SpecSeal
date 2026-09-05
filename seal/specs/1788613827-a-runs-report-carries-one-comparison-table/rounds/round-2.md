# 1788613827-a-runs-report-carries-one-comparison-table — review round 2

| Field | Value |
|---|---|
| Target SHA | c048548 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 173 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | tool_name (depth 1); test_a_tool_name_that_is_not_a_name_does_not_end_the_report (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | yes — 🟡 1 crashes: `session_cost.py` exits 1 with a `TypeError` traceback and prints nothing, the token block included. Round 1 answered `no` on the same class of reproduced traceback; the reviewer read the question as covering a reproduced crash, and names the difference so it can be settled rather than inherited |

- [x] Pass

## What this round was asked

Round 2, the verifying round, against `c048548`, targeting the diff of round
1's fixes — `ae9c64d..b34374e`, twelve files. It was told what a verifying
round is not: round 1 read the whole change first-hand, its *What I checked
and found clean* section was carried rather than re-derived, and re-deriving
it is the loop measured at gain ≥ 1 on an earlier branch.

Six probes were handed over as re-checks rather than discoveries — the
usage-only transcript, the two type shapes, the eleven modules, ruff, and the
unscoped ledger read with the reason the scoped form is a writer's narrowing.
Seven claims of the fix pass were named as claims under §5, each with the
instruction to open it: the six-member class and whether a seventh exists,
whether the two turn counts can still be divided into each other, whether the
divergence from #170 is quoted on both sides, whether `templates/sdd-round.md`
is untouched, whether a rename leaves the widened refusal guarding nothing,
two named mutations to re-run, and the five re-stamped shared-ledger rows.

The `sed -i` edit the fix pass disclosed was handed over as disclosed: judge
only whether the text that landed is what the cases pin, the rule breach
being already on the record.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Finding 2's class has a seventh member: `load` stores `block["name"]` with no type check and `analyse` uses it as a `by_family` key, so a non-string tool name ends the whole report — the token block included | `skills/verify/scripts/session_cost.py#load` | **fixed** `0143a55` | fixed at 0143a55 — `` — guarded at the source, `tool_name` in `load`, so every reader of `call["tool"]` is covered. The class was re-enumerated by substituting each of seven JSON types into eighteen field paths in both output modes, 288 variants: it has one field with **two** crash sites, not the one the finding named — a `null` name is hashable, passes `analyse`'s dict key, and dies at `report`'s format spec after 350 bytes are already printed. A guard at the reported site would have shipped with that standing. 288 variants, no survivor after the fix; executed at `c048548`: `TypeError: unhashable type: 'list'` at `:228`, exit 1, stdout empty, on both the report and `--json`; a `dict` name raises at the same line |
| ⬜ 2 | The widened `TABLE_ROWS` refusal catches verbatim row labels, not the lowercase prose gloss round 1's finding 8 actually was | `tests/test_the_handoff_before_round_one.py#TABLE_ROWS` | **fixed** `0143a55` | fixed at 0143a55 — `` — reproducing the probe split the finding: *replacing* the paragraph with the gloss was already red, and only *adding* the gloss beside it passed. The removed wording is now refused verbatim, the pattern this module already uses, and the docstring says what the label list does and does not reach — including that a freshly written gloss is caught by neither, because the words are lowercase and generic; executed: the deleted sentence re-inserted into the bars section leaves 59 passed across the three modules that read it |
| ⬜ 3 | The `Location` row defines a record as *anything under `seal/`*, which is broader than the three paths in the policy it cites — `seal/config.md`, `seal/follow-up.md` and `seal/README.md` fall inside one and outside the other | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | **fixed** `0143a55` | fixed at 0143a55 — `` — the row names `seal/specs/`, `seal/ledger/` and `seal/ledger.md` one at a time. The existing assertion searching for `` `seal/` `` had stayed green over the corrected wording, so it was pinning nothing; it now refuses the old sentence verbatim; read at `skills/verify/SKILL.md:438` against `docs/review-chain-spec.md:155-157`; `ls seal/` lists the three files the enumeration does not cover |
| ⬜ 4 | `turn` still carries two meanings in one printed report; the fix labels the two rather than renaming either, and `tests/test_one_word_one_meaning.py`'s standard is one word one meaning | `skills/verify/scripts/session_cost.py#report` | answered | The premise is that the grounds live only in `token_totals`' docstring. They do not: the divergence is stated at both computation sites — `analyse`'s comment on `call_turns` and `token_totals`' docstring — and at both printed lines, each naming its own denominator and scope. `test_one_word_one_meaning.py`'s standard is a coordinate where the reader cannot tell which meaning is intended, and after round 1's finding 5 no such coordinate remains. Renaming either counter is what the module cannot have: `tools_per_turn`'s denominator is what the bars in `docs/review-handoff-protocol.md` are calibrated against, so widening it moves a published threshold silently — `questions.md` assumption 5 records that decision |
| ✅ 5 | Round 1's finding 1 — the token line computed after `analyse`'s guard | `skills/verify/scripts/session_cost.py#main` | answered | executed: usage-only transcript exits 0, prints the token block; the mutation restoring the old order kills one case |
| ✅ 6 | Round 1's finding 2 — `TypeError` on a string `usage` field and an unhashable `message.id` | `skills/verify/scripts/session_cost.py#token_totals` | answered | executed: both shapes now contribute zero / key by position, exit 0. Six of the class closed; the seventh is 🟡 1 above |
| ✅ 7 | Round 1's finding 3 — the `Location` buckets and the share row against the record definition | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | answered | read: `ledger` is gone as a bucket, the share row reads *the record paths above*, and `overview.md` quotes both sides verbatim. The residue is ⬜ 3 |
| ✅ 8 | Round 1's finding 4 — `Broad gate: how many times, at what SHA` | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | answered | executed: `templates/sdd-round.md` untouched; the row is true of the cell; the wide half is #174 |
| ✅ 9 | Round 1's finding 5 — `turns` in two meanings with nothing between them | `skills/verify/scripts/session_cost.py#report` | answered | executed on a real transcript: each count names its own denominator and scope. The strict standard is ⬜ 4 |
| ✅ 10 | Round 1's finding 6 — `transcripts` counts a file that yielded nothing | `skills/verify/scripts/session_cost.py#token_totals` | answered | read: the docstring says the count covers the files OPENED and names `turns` as where a doubled run shows; no counting rule moved |
| ✅ 11 | Round 1's finding 7 — no way to find a run's main transcript | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | answered | read: the new paragraph names the `*.jsonl` directly under the project directory and says `--latest` usually lands on a segment |
| ✅ 12 | Round 1's finding 8 — five row names restated in prose | `docs/review-handoff-protocol.md#"### After the run — the per-segment bars"` | answered | read: the gloss is gone and the paragraph says what the table asks. The refusal that replaced it does not close the class — ⬜ 2 |
| ✅ 13 | Round 1's finding 9 — ledger row R1 recorded an overstatement as verified behavior | `seal/ledger/1788613827-a-runs-report-carries-one-comparison-table.md` | answered | executed: unscoped read 595 ok · 1 drifted · 0 broken; the corrected claim matches what the code now does |

## Executed probes

| What was run | Result |
|---|---|
| Usage-only transcript, no paired tool call | exit 0; the token block, `1 transcript, 1 turn`, `output 7`, `cache read 70`; `--json` `tokens.output == 7` |
| `"output_tokens": "12"` with `"cache_read_input_tokens": true` | exit 0; both contribute zero, no traceback |
| `message.id` as a list | exit 0; `calls: 2`, keyed by row position |
| `tool_use` `"name": ["Bash"]`, paired | **exit 1** — `TypeError: unhashable type: 'list'` at `session_cost.py:228`; stdout empty on both the report and `--json` |
| `tool_use` `"name": {"n": 1}`, paired | exit 1 — `TypeError: unhashable type: 'dict'`, same line |
| `timestamp` as a list | exit 0 — `parse_time` catches it; not a member of the class |
| The lowercase gloss re-inserted into the bars section | 59 passed across the three modules that read it |
| The `Broad gate` row label renamed in `skills/verify/SKILL.md` | 3 failed. No rename hole |
| Mutation: `message_key` always the row position | 5 failed — killed |
| Mutation: `main` sums the tokens after the guard again | 1 failed, exit 1 — killed |
| `pytest` over the 23 modules that read the four changed non-test files | 660 passed |
| `uvx ruff check` over the five changed Python files | all checks passed |
| `evidence_check.py .` unscoped, exit read directly | exit 1 — 595 ok · 1 drifted · 0 broken |
| `git diff --quiet a9a827b HEAD -- templates/config.md` | exit 0 — not this branch's |
| `git diff --quiet a9a827b HEAD -- templates/sdd-round.md` | exit 0 — untouched |
| `session_cost.py` on a real 8-transcript session | `422 turns` in the token block, `1.00 tools per turn — 64 calls over 64 turns that sent one, in this transcript alone` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py#main` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#token_totals` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#report` | round 1's 🟡 5 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#newest` | round 1's ⬜ 7 — fixed |
| round-1 | `docs/review-handoff-protocol.md#"### After the run — the per-segment bars"` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/ledger/1788613827-a-runs-report-carries-one-comparison-table.md` | round 1's ⬜ 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, the repository-wide lint and the typecheck | the broad gate, after this round. `Broad gate` reads `not yet` and is now due | the orchestrator |
| The exact eleven-module list the fix pass ran | not recorded in any file (§5). I ran the 23 modules reading the changed files instead, a superset over those paths | the orchestrator, if the exact list matters |
| `subagent_transcripts` and `newest` on the Windows leg | `overview.md` §Not verified, unchanged by this round — darwin only | the Windows leg of the pull request's checks |
| The table as a thing a person actually fills | `overview.md` §Not verified — already deferred by round 1 | the orchestrator, in this branch's own pull request body |
| A `Broad gate` cell that can hold more than one entry | issue #174 — already deferred by the fix pass | the repository owner |
| `templates/config.md#"# Repository config"` drift | pre-existing on `a9a827b` — already deferred by round 1 | the repository owner |
