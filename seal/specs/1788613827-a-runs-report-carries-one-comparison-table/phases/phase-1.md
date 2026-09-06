# 1788613827-a-runs-report-carries-one-comparison-table — phase 1

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 2800051 |
| Ran by | |

## What this phase was asked

`skills/verify/scripts/session_cost.py` prints a token line and reports the
same numbers under `--json`, summed over the transcript it was given **and**
every `*.jsonl` under the `<session-id>/subagents/` directory beside it —
always, not behind a flag. Three fields in their own columns
(`output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`),
plus a turn count and the number of transcripts the line covers.

Four constraints came with it. `tools_per_turn`, `context_growth`, `model_s`,
`command_s` and the `repeat_*` numbers do not move, and the script says in a
comment why its two turn counters differ. A message's `usage` counts once
however many rows it is split across. A malformed line, an unreadable subagent
file, or a missing `subagents/` directory degrades to a smaller number rather
than a traceback. And the phase does not touch the documents phases 2–4 own.

## What this phase found

**`os.walk` never hands a directory to the file loop, so a fixture built out
of one cannot reach the `open()` guard.** The first draft of
`test_an_unreadable_segment_shrinks_the_count_rather_than_raising` made a
directory named `gone.jsonl` under `subagents/` and asserted the report still
printed. It did — but `subagent_transcripts` filters `files`, and `os.walk`
sorts that name into `_dirs`, so the path was excluded by the walk rather than
by the `except OSError`. Mutation-testing caught it: replacing `except OSError`
with `except ValueError` left all 23 cases green. The guard is now pinned by a
case that calls `token_totals` directly with a path that does not exist, which
is also the only shape of that case that is root-proof — a `chmod 000` fixture
passes for the wrong reason when the suite runs as root.

**The transcript count validates itself against a number the same report
already prints.** Run against a real 20-hour transcript, the line read
`18 transcripts` while the by-family table read `Agent 17 calls` — one main
plus one per spawned segment. A reader who doubts the count has that
cross-check in the same output, without opening a directory.

**The subagents directory holds a `.json` sidecar beside every `.jsonl`.** That
real directory had 34 entries for 17 segments. The `.jsonl` filter is
load-bearing rather than cosmetic; dropping it would double every count.

**`plural()` is named that way because `counted` was taken.** Both `load` and
`token_totals` hold a local set called `counted`, so a module-level function
of that name is shadowed inside the two functions most likely to want it.

**For phases 2–4.** The JSON key names are `transcripts`, `turns`, `output`,
`cache_write`, `cache_read` under a `tokens` object, matching `spec.md`
§*Data & interfaces*. The printed line is four lines — a `tokens` header
carrying the transcript and turn counts, then `output`, `cache write` and
`cache read` right-aligned in 15 columns with thousands separators — and it
sits between the span block and `by family`. `bin/session-cost` and
`bin/session-cost.cmd` needed no change. Phase 3 should know that
`tests/test_the_handoff_before_round_one.py`'s
`test_the_advisory_and_the_tying_paragraph_name_one_value` reads
`data["tools_per_turn"] < 1.2` out of this script by regex; that expression is
untouched, so the tying sentence in `docs/review-handoff-protocol.md` still
names the right value.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds. `message()` in `tests/test_session_cost.py` lost its inline clock to the new `stamp_at()` helper, which the same file keeps | none |
