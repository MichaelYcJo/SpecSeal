# Feature Specification: a resumed agent's own transcript is sliced (#637)

<!-- seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/measuring-a-run.md` §*What a measurement must survive, and what it must not invent*, the clause *A reading that was published is still wrong after it is published* (`Enforced by: nothing — a session's act`) | this work item says which published readings the change bears on. It moves no number the meter already computes: it produces a reading where `--segments` produced none. The fix-pass readings posted as a whole resumed transcript, and the ones taken from the harness's notice, are named in the changelog fragment (§*Scope*, In 6) |
| `docs/measuring-a-run.md` §*The unit is a segment, and a segment has its own transcript* | a slice of an agent's own file is a segment's own stretch of work. It is never a spawn cycle, and nothing here joins it to a spawn: no parent transcript is in view, so the join the clause asserts is not attempted and not claimed |
| `skills/verify/scripts/session_cost.py#analyse`, its docstring: *Changing what the plain reading prints would make every reading this repository has already published incomparable with the next one* | the plain reading keeps every number and every line it prints today. What it gains, only for a file `--segments` would now slice, is one added line that points there (In 4). This is the ticket's option 3. Its option 2, one plain reading per slice, stays rejected on this clause |
| `skills/verify/scripts/session_cost.py#segment_slices` docstring and `#measure_segments`' comment on `unnamed` (*Over TRANSCRIPTS, never over rows*) | the slices come from `segment_slices` unchanged, so the token figure rides the first kept slice and an empty window is not a row. `unnamed` stays a count over the transcripts walked beside the given file. The given file itself is not one of them |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | every sentence stating the current behaviour is corrected in the commit that makes it false (§*Scope*, *The class*). Every changed line a person reads is pinned. Every new case is seen red at the base `ab116d1e` before it is planted |
| `CLAUDE.md` *a change writes fragments, never the shared file* | the changelog goes in `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/changelog.md`, and new ledger rows go in `seal/ledger/1790562540-a-resumed-agents-own-transcript-is-sliced.md`. A row this edit drifts is re-read in the file it lives in |

## Scope

### What happens today (read at this tree, `ab116d1e`)

`measure_segments` asks `subagent_transcripts(path)` for the files under
`<basename>/subagents/` beside the given file. An agent's own transcript has
none, so `found` is empty, no row is made, and `report_segments` takes its
empty branch: `0 segments found beside <path>`. `resume_cuts` is reached only
through `segment_slices`, and only `measure_segments` calls `segment_slices`,
for the files it found. The plain path in `main` calls `analyse` on the whole
file and never cuts it.

The ticket named these units at `2037cf0`. None of `resume_cuts`,
`segment_slices`, `measure_segments`, `subagent_transcripts` or `main` has
changed since (`git diff 2037cf0 HEAD` hunk list, read). `report_segments`
gained #377's comparability line at its tail, and this work does not touch
that line.

What that costs is the ticket's claim, and it was not re-derived here. Since
0.14.0, every fix-pass reading in the flow logs came from the harness's notice
or from a whole resumed transcript. #601's comments were opened for this frame
(read): 0.15.4's fix passes for work items A, B, C, D and E each say *this
reading is the whole transcript*.

### Harness layout, measured on this machine (executed, 2026-09-28)

- Every `subagents/` directory under `~/.claude/projects/` sits at
  `<project>/<session>/subagents/` (52 of 52). None sits under an agent's own
  `agent-<id>/`. So an agent's own file never has transcripts beside it
  (`found` is always empty), and a child of an agent is written into the same
  flat session directory as its parent agent.
- Every `agent-<id>.jsonl` under a `subagents/` directory has an
  `agent-<id>.meta.json` beside it (637 of 637). That file carries
  `agentType` and `description`. Nothing in this repository reads it. See
  *Out*.

### In

1. **`--segments` given a file with no transcripts beside it, whose own
   `resume_cuts` is non-empty, prints that file's slices.** The rows come
   from `segment_slices(path, labels)` exactly as a walked file's do. The
   trigger is the marker and not the directory. A resumed agent's file
   copied elsewhere is still sliced. A file with no marker, under
   `subagents/` or anywhere else, keeps today's empty branch byte for byte,
   which is the ticket's *must not break*.
2. **The page says what these rows are.** The own-file case prints its own
   header in place of the join counts, because no join was attempted. The
   header names the file, how many coordinator messages cut it and into how
   many slices. The `agent` legend line does not claim a spawn was joined.
   The *named by nobody* paragraph and `report_breaches`' two-count
   reconciliation line (*… against N segments the parent could not name, and
   the two do (not) agree*) are not printed, because both reconcile against a
   parent this case never saw. The §6 breach list IS printed: an `Agent` call
   in an agent's own slice is exactly what it exists to name. The resumed
   paragraph, the idle-gap floor, the table, the token-column note and both
   comparability lines print as they do for a walked run.
3. **`--json` carries the same rows.** `measure_segments` is the one place
   rows come from, so `--json` on a resumed agent's file gains the rows the
   page prints. The key set of every existing case is unchanged (§*Data &
   interfaces*).
4. **The plain reading of such a file adds one line and changes nothing
   else.** The condition is exactly In 1's: markers, and no transcripts
   beside. The line says the file holds N coordinator messages and that
   `--segments` prints it one row per stretch of work. It is printed after
   `--latest`'s `# <path>` line where there is one and before the `span`
   line, because the span is the number that gets quoted. The file is read
   for markers only when nothing is beside it, so a run's main transcript
   pays nothing.
5. **`--post` is unchanged in what it strips.** The own-file page reaches the
   body through `emit`, and the posted body carries the basename and not the
   path (S9).
6. **The changelog fragment says which published readings this bears on.**
   The fix-pass readings posted as a whole resumed transcript: #577 (four
   passes) and #601 (ten). The ones taken from the harness's notice because
   `--segments` found nothing: #496, #535 and #619. None of them becomes
   wrong by this change. What becomes possible is re-deriving them, which is
   its own work (the policy's own sentence).

### The class — every sentence that states the current behaviour

§12 asks for the class, not the example. The ticket names one
(`skills/verify/SKILL.md`, *A resumed agent is one row per slice*). A search
over every tracked `*.md` and `*.py` outside `seal/specs/`, `seal/releases/`,
`seal/ledger*` and `CHANGELOG.md` for `resum`, `--segments`,
`measured on its own`, `plain reading` and `segments found` (executed) finds
these. Each is corrected in the commit that makes it false.

| # | Where | Says today | Why it goes false |
|---|---|---|---|
| D1 | `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, step 1, *A resumed agent is one row per slice…* | the split is taken when `--segments` walks the run's transcript | it also happens given the agent's own resumed file. The sentence is extended, and `one row per slice` stays (`tests/test_a_segment_feeds_the_flow_log.py#test_the_section_says_the_mode_takes_the_resume_split` pins it) |
| D2 | same step, *One segment measured on its own is still `session_cost.py <transcript>` with no mode flag. That plain reading is unchanged, and every row of the per-segment table is that same reading of another file.* | send a lone segment to the plain reading, which never changes | a resumed lone segment is `--segments <its file>`, and the plain reading of it gains In 4's line. *Every row is that same reading of another file* is already false for a slice, which is the plain reading of a stretch of a file and not of the file |
| D3 | same step, *`--segments` opens the transcripts of the agents this run spawned, one row each* | the mode only ever opens other files | given a resumed agent's own file, it reads that file. The segment ↔ spawn-cycle distinction the paragraph exists for is kept (`tests/test_one_word_one_meaning.py`, the `segment` block) |
| D4 | `README.md` §*Cheat sheet*, the `session-cost --segments <transcript>` row | *one row per agent the run spawned … A resumed agent is one row per stretch of work* | same as D1. The Korean edition's row is D5 |
| D5 | `README.ko.md` §*치트시트*, the same row | the same claim in Korean | the same. Both editions change in one commit |
| D6 | `skills/verify/scripts/session_cost.py`, module docstring: the `Usage` line for `--segments` (*one row per segment this run spawned*) and the paragraph *`--segments` opens the OTHER transcripts, one row per agent this run spawned* | the mode only opens other files | as D3 |
| D7 | `session_cost.py#measure_segments` docstring, *One row per spawned segment of this run* | the same | as D3 |
| D8 | `session_cost.py#report_segments` docstring, *One row per spawned segment, or the count and no table* and *this opens the OTHER transcripts, one row each* | two shapes | a third shape now exists |
| D9 | `session_cost.py#emit` docstring, *the empty branch that fires whenever the named transcript has no subagents beside it — which is every segment measured on its own* | every lone segment reaches the empty branch | a resumed lone segment no longer does |
| D10 | `tests/test_session_cost_post.py#test_the_posted_body_does_not_carry_the_transcripts_path` docstring, the same sentence | the same | the same. The case's fixture has no marker, so it still exercises the empty branch, and only the sentence narrows |
| D11 | `tests/test_session_cost.py#test_a_run_with_no_segments_reads_rather_than_raising` docstring, *the reading is empty* | a lone segment's `--json` segments are empty | not for a resumed one. The fixture has no marker, so the assertion stands and the sentence narrows |

**Read and not in the class, because they stay true:** the empty branch's
printed text in `report_segments`, which the ticket says must not break;
`#subagent_transcripts`' docstring (*a missing directory is the ordinary
case*, which is about that function); `SKILL.md` step 1's *Run
`session_cost.py --segments` against the **run's** transcript*, which stays
the instruction for a run; `SKILL.md`'s `--latest` paragraph; and
`docs/review-handoff-protocol.md` §*After the run*, which names the meter and
not the mode.

### Out

- **The rows' agent name.** An own-file row is labelled by its file's name,
  the way a walked file nobody could name already is. The name could be
  recovered from `agent-<id>.meta.json` (measured present on 637 of 637), or
  by walking up to `<session>.jsonl` and joining there. Both read a file this
  mode does not read today, and the meta file's format is the harness's,
  owned by nobody here. The ticket asks for the numbers, and the numbers
  carry no name. Whether it is worth an issue is for the orchestrator of this
  release to decide at the pull request.
- **`--spawns` on an agent's own file.** It prints *0 spawns found* for an
  agent that spawned nothing, which is true. It is not the ticket's case.
- **An own file that has transcripts beside it** (an agent's own
  `agent-<id>/subagents/`). On this machine none exists (Harness layout,
  above), and such a file takes the walked path unchanged. In 4's hint uses
  In 1's condition, so it never promises a split `--segments` would not make.
- **Re-deriving the published fix-pass readings.** In 6 names them. Opening
  each resumed transcript again and posting the slices is its own work, and
  the transcripts of runs taken on another machine are not here.
- **The family code: `FAMILIES`, `family`, `runs_git`, `command_words`,
  `analyse`, `report`'s `by family` block and `report_segments`' two closing
  comparability lines.** Item B (#642) edits them after this item squashes
  into `release/v0.15.7` (milestone 50's description). `plan.md`
  §*Technical context* lists the units this item touches.
- **The harness rewording its coordinator sentence.** `COORDINATOR_MESSAGE`'s
  comment already owns that failure. Here it lands on today's behaviour, not
  on a wrong reading.

## User scenarios & acceptance *(mandatory)*

The fixture helpers are `tests/test_session_cost.py`'s: `write_run`,
`worked`, `coordinator_message`, `spawn`, `segments_of`, `segment_report`.
"Own file" below means `tmp/main/subagents/agent-x.jsonl` passed straight
to the script.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The acceptance row | Given an own file with two stretches of work and one coordinator message between them. When `--segments <own file>` runs. Then two rows print, `1/2` and `2/2`, their calls sum to the file's calls, and their spans sum to well under the file's own span | a case, red at `ab116d1e` (today it prints `0 segments found`) |
| S2 | Three stretches | Given an own file with two coordinator messages, each followed by calls. Then three rows print and their calls sum to the file's. The ticket's fixture sentence (*two coordinator messages … two slices*) holds only where the messages are adjacent. That is `test_two_coordinator_messages_in_a_row_do_not_invent_a_slice`'s shape, and it is re-run on the own-file route as S2b | cases, red at the base |
| S3 | Same numbers by either route | Given one run whose smith file is resumed. When `--segments main.jsonl` and `--segments main/subagents/agent-smith.jsonl` both run. Then the slices' span, calls, tools per turn, mean gap and tokens are identical, row for row. This is the ticket's *the second must print the slices the third prints*, taken on a fixture | a case comparing the two `--json` row lists minus the label fields, red at the base |
| S4 | No marker, no change | Given an own file with no coordinator message, under `subagents/`. When `--segments` runs. Then the output is today's empty branch, byte for byte | a case. It is green at the base, so it is seen red under the mutant that slices every file under `subagents/` whatever its markers |
| S5 | The page says what the rows are | Given S1's file. Then the header names the file and its coordinator-message and slice counts. `named by nobody`, `segment transcripts beside this one` and `the parent could not name` do not appear | a case pinning the header's words (§14), red at the base |
| S6 | A spawn inside an own slice | Given an own file whose second stretch holds an `Agent` call. Then the §6 block names that row with its `2/2` suffix, and no *do (not) agree* line prints | a case, red at the base |
| S7 | `--json` | Given S1's file. Then `--json`'s `segments.rows` holds the two slices, `unnamed` is 0 and `own_file` is `true`. Given a file with no marker, `segments` is exactly today's dict, and `test_a_run_with_no_segments_reads_rather_than_raising` passes unchanged | a new case, red at the base, plus the existing one |
| S8 | The plain hint | Given S1's file. When the plain reading runs. Then one added line names the file's coordinator-message count (1 here) and `--segments`, and every other line equals the base's output. Given a file with no marker, or `run_with_segments`' main transcript, no such line prints and `test_no_existing_printed_line_moves_when_the_mode_is_not_asked_for` passes unchanged | a case pinning the line's words, red at the base. Equality of the rest is shown by comparing against the output with the hint line removed |
| S9 | `--post` from an own file | Given S1's file under a directory. When `--segments --post --says f` runs against a stubbed `gh`. Then the body carries the basename and neither the path nor its directory | a case in `tests/test_session_cost_post.py` beside `test_the_posted_body_does_not_carry_the_transcripts_path`. Red under the mutant that skips `emit`'s substitution |
| S10 | The existing resumed cases | `test_a_resumed_segment_is_one_row_per_slice_not_one_per_file`, `test_two_coordinator_messages_in_a_row_do_not_invent_a_slice`, `test_a_files_tokens_are_carried_by_its_first_slice_only`, and the rest of the resume block | pass unchanged (the ticket's *must not break*) |
| S11 | The documents | D1–D11 are corrected. The D1/D2 sentences a session reads are pinned in `tests/test_a_segment_feeds_the_flow_log.py` | a case red with the new sentence deleted. `test_the_section_says_the_mode_takes_the_resume_split` passes unchanged |
| S12 | The real transcript | The ticket's three commands, re-run on a real resumed agent transcript on this machine. The second prints the slices the third prints for that agent | executed by the builder, recorded in the phase record (`questions.md` Q1) |

## Data & interfaces

**`measure_segments(path, calls)`**, the own-file case. It applies when
`subagent_transcripts(path)` is empty and `resume_cuts(path)` is not. The
return keeps every existing key with its existing meaning and adds one:

| Key | Own-file case |
|---|---|
| `tolerance_s` | unchanged |
| `transcripts` | `0`, the files beside, as today |
| `spawns` | the `Agent` calls in the given file, as today |
| `unnamed` | `0`. It counts walked transcripts, and the given file is not one |
| `unclaimed` | as today's arithmetic yields: every spawn, since nothing was walked to claim one |
| `rows` | `segment_slices(path, {"agent": "", "description": "", "named": False, "transcript": <basename>})` |
| `own_file` | `true`. **Present only in this case**, so every existing case's dict, and the equality case in S7, stays byte-identical |

A row's `transcript` is the basename, which is what `os.path.relpath`
against the file's own directory already yields. So `segment_label` prints
it the way it prints any unnamed row, cut from the left.

**`report_segments`** branches on `segments.get("own_file")` before the join
counts. **`report_breaches`** reads the same key to leave out its
reconciliation line. It already receives `segments`, so no signature changes.

**`main`'s plain path**: the hint's condition is computed only when
`subagent_transcripts(path)` is empty. `main` already calls that function
for the token walk, so the result can be reused.

**A new `int()` or `round()` on a derived number** has to be discharged for
`tests/test_a_derived_number_reaching_an_int_carries_a_guard.py`. Every
count this work prints is a `len()`, which needs no conversion, so none
should be added.

## Open questions → questions.md

No row needs a person. Q1 is a measurement and Q2 is the work's.

Framed 2026-09-28 by framer, before the build.
