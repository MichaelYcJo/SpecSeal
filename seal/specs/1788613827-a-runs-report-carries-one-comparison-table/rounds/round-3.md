# 1788613827-a-runs-report-carries-one-comparison-table — review round 3

| Field | Value |
|---|---|
| Target SHA | 2aef226 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 173 |
| Broad gate | 15ab83d, against a9a827b — 2287 passed, 2 skipped, 4 failed: the four macOS export cases of #160, reproduced identically at the base in a clean clone. `uvx ruff check .` and `format --check .` clean |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no — nothing this branch wrote. Finding 5's two crashes are byte-identical at the base `a9a827b`, and 299 real transcripts produce neither shape |

- [x] Pass

## What this round was asked

Round 3, a verifying round, against `2aef226`, targeting the diff of round 2's
fixes — `73e83d4..f21a176`, seven files. It was told the run had already been
reopened once, so the bar was the floor rather than a hunt: stop when the round
finds nothing that leaves the root and nothing that crashes.

Five probes were handed over as re-checks — the two crash shapes now exiting 0,
the eight modules, ruff, and the unscoped ledger read with the reason the
scoped form is a writer's narrowing. Six claims of the fix pass were named as
claims under §5, each with the instruction to judge the METHOD and not only the
result: the 288-variant enumeration, the mutation that proves the guard belongs
at the source rather than at the reported crash site, whether the refusal's
docstring is honest about what it does not reach, whether the corrected
assertions fail on the old sentence, whether ⬜ 4's grounds hold, and the two
re-stamped shared-ledger rows.

One thing was settled before the round rather than left to it: the four macOS
export failures are #160, confirmed identical at the base in a clean clone, and
the fix pass's guess that the date roll caused them is wrong.

The verdict table was asked to number continuously from 1, inherited findings
included — a second row numbered 1 makes the generator refuse, which had cost a
round trip at round 2's record.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's 🟡 1 — a `tool_use` name that is not a name ends the whole report, with two crash sites rather than one | `skills/verify/scripts/session_cost.py#tool_name` | answered | executed: all eight shapes of `block["name"]` exit 0 on the report and on `--json`, each charged to `?`. Mutation A, guarding only the reported `(list, dict)` site, leaves 1 failed / 30 passed, so the `null` half is pinned by a case that fails without it. The class was re-derived independently before the account was opened: 20 `.get(` sites, 16 distinct transcript fields, all guarded |
| 2 | Round 2's ⬜ 2 — the widened `TABLE_ROWS` refusal does not reach the lowercase gloss round 1's finding 8 removed | `tests/test_the_handoff_before_round_one.py#test_the_bars_and_the_run_level_table_judge_different_things` | answered | executed: mutation C adds the gloss beside the sentence — the shape that passed every case in the module before this fix — and the module now reports 1 failed / 13 passed. The docstring's admission is honest: neither check reaches a freshly written gloss, and no literal string can |
| 3 | Round 2's ⬜ 3 — the `Location` row defines a record as anything under `seal/`, broader than the policy it cites | `skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` | answered | executed: mutation B restores the old sentence verbatim and `tests/test_a_segment_feeds_the_flow_log.py` reports 1 failed / 25 passed, where the old `` `seal/` `` substring assertion had stayed green over it. Read: the row's three paths match `docs/review-chain-spec.md`'s three exactly |
| 4 | Round 2's ⬜ 4 — `turn` carries two meanings in one printed report, answered rather than fixed | `skills/verify/scripts/session_cost.py#report` | answered | the grounds hold and I checked each. `tests/test_one_word_one_meaning.py`'s docstring states its standard as a coordinate where the reader cannot tell which meaning is intended, and `turn` is not one of its five words. Both computation sites and both printed lines name their own denominator and scope |
| 5 | The enumeration closed the **type** axis; the rule it cites is about **values**, and two value-shaped odd rows still end the report — `span_s == 0` raises `ZeroDivisionError`, and a transcript mixing zone-aware and naive timestamps raises `TypeError` with stdout empty | `skills/verify/scripts/session_cost.py#report`, `skills/verify/scripts/session_cost.py#analyse` | deferred #175 | executed at `2aef226` and byte-identical at the base `a9a827b`, so neither is this branch's — the orchestrator reproduced both at both revisions before opening the issue. Measured over 299 real transcripts: 0 calls with `start == end`, 0 transcripts with `span == 0`, and 0 naive stamps in 94,514. Not a shipping defect for this harness, which is why it is ⬜ — but the fix pass's *no survivor* is true of the axis it ran, not of `parse_time`'s rule |
| 6 | The ledger note calls `name` *the one field in `load` that had no type check*; `row.get("timestamp")` has none either, and is guarded by `parse_time`'s `except` instead | `seal/ledger.md` | answered — corrected at `15ab83d` | read at the re-stamped row, against `load` lines 143–207. Round 2's own probe recorded `timestamp` as a list exiting 0 through `parse_time`, so the file agrees; the sentence was one clause loose. A record-located correction, so it rides the closing commit rather than a fix pass — the clause now reads *the one field in `load` whose readers had no guard of any kind* |
| 7 | The docstring says `rounds` *occurs twice in that section legitimately*; inside `bars_section` it occurs four times as a word, five as a substring | `tests/test_the_handoff_before_round_one.py#test_the_refused_rows_are_the_owners_own` | answered — corrected at `15ab83d` | executed: `bars_section(read("docs","review-handoff-protocol.md"))` gives 4 word matches and 5 substring matches. The count was wrong in the direction that strengthens the argument. Corrected to *four times*; the fragment row anchoring that docstring was re-stamped scoped to this work item's own ledger |

## Executed probes

| What was run | Result |
|---|---|
| `tool_use` `"name"` as list, object, `null`, int, bool, float, `""`, and absent — paired, report and `--json` | all 16 runs exit 0; `by_family` keys `['?', 'test']` in every case |
| Mutation A — `tool_name` guards only `(list, dict)`, the reported site | 1 failed, 30 passed — killed |
| Mutation B — the old `Location` sentence restored verbatim in `skills/verify/SKILL.md` | 1 failed, 25 passed — killed |
| Mutation C — the lowercase gloss added beside the sentence in the bars section | 1 failed, 13 passed — killed |
| The 18 modules that read the changed files, one command | 490 passed |
| `uvx ruff check` over the four changed Python files | all checks passed |
| `evidence_check.py .` unscoped, exit read directly | exit 1 — 598 ok · 1 drifted · 0 broken |
| `git diff --quiet a9a827b HEAD -- templates/config.md` | exit 0 — the drifted row is not this branch's |
| One paired call, `tool_use` and `tool_result` sharing a timestamp | exit 1, `ZeroDivisionError`, 36 bytes of stdout — identical at base `a9a827b` |
| A zone-aware stamp and a naive stamp in one transcript | exit 1, `TypeError` naive/aware, 0 bytes of stdout, report and `--json` — identical at base `a9a827b` |
| Scan of 299 real transcripts for `start == end` and `span == 0` | 281 with a paired call; 0 and 0 |
| Scan of the same 299 for naive timestamps | 94,514 zone-aware, 0 naive, 0 transcripts mixing |
| `.get(` enumeration of `session_cost.py`, re-derived independently | 20 sites, 16 distinct transcript fields, all guarded |
| `bars_section` `rounds` count, via the module's own function | 4 word matches, 5 substring |
| Clone tree after all three mutations restored | clean; probes deleted, worktree untouched |

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
| round-2 | `skills/verify/scripts/session_cost.py#load` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_the_handoff_before_round_one.py#TABLE_ROWS` | round 2's ⬜ 2 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 5 — the two value-shaped crashes `report` and `analyse` still carry | **issue #175**, opened by the orchestrator after reproducing both at `2aef226` and at the base, milestone 0.8.3 | the repository owner |
| `tests/test_the_records_can_be_carried_out_and_in.py`'s four macOS failures | issue #160, scheduled for 0.8.3 — settled before this round and not re-derived; the broad gate reproduced exactly those four | the repository owner |
| `subagent_transcripts` and `newest` on the Windows leg | `overview.md` §Not verified — darwin only, unchanged by this round | the Windows leg of the pull request's checks |
| The table as a thing a person actually fills | `overview.md` §Not verified — already deferred by rounds 1 and 2 | the orchestrator, in this branch's pull request body |
| A `Broad gate` cell that can hold more than one entry | issue #174 — already deferred | the repository owner |
| `templates/config.md#"# Repository config"` drift | pre-existing on `a9a827b` — already deferred by round 1 | the repository owner |
