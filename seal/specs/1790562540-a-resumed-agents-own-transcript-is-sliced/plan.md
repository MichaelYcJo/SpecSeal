# Implementation Plan: a resumed agent's own transcript is sliced (#637)

<!-- seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

`--segments` given a resumed agent's own transcript prints that file's
slices, where it prints `0 segments found` today. The plain reading of the
same file keeps every line and adds one that points at `--segments`. That is
the ticket's option 1 with option 3 beside it. One file of code,
`skills/verify/scripts/session_cost.py`, plus its cases, eleven sentences
across five documents and two test docstrings (`spec.md` D1–D11), the
changelog fragment and the ledger.

## Technical context

**What it builds on (read at `ab116d1e`):**

- `session_cost.py#measure_segments` walks `subagent_transcripts(path)`,
  joins each file to a spawn and calls `segment_slices` per file. With
  nothing found it returns `rows: []`, and that is the whole defect.
- `session_cost.py#segment_slices(transcript, labels)` already does
  everything the own file needs: cuts at `resume_cuts`, drops empty windows,
  lets the first kept slice carry the file's tokens, and names the idle gap.
  It is reused **unchanged**.
- `session_cost.py#report_segments` prints the join counts, the legend, the
  unnamed paragraph, the resumed paragraph, the idle floor, the table,
  `report_breaches`, the token note and two comparability lines.
  `report_breaches` prints the §6 list and then a reconciliation of calls
  against `unnamed`.
- `session_cost.py#main` computes `subagent_transcripts(path)` for the token
  walk. It calls `measure_segments` under `--segments` or `--json`, and it
  renders the plain report through a local `render()` that calls `report`.

**The units this item touches, stated for item B (#642).** B is framed in
parallel and built after this item squashes into `release/v0.15.7`.

| Touched here | Not touched here (B's) |
|---|---|
| module docstring: the `--segments` usage line and the *Why `--segments`* / *A spawn cycle is not a segment* paragraphs (D6) | `FAMILIES` and its comment, `family`, `runs_git`, `command_words`, `without_heredoc_bodies`, `HEREDOC` |
| `#measure_segments`: the own-file branch, and its docstring (D7) | `#analyse` and its docstring |
| `#report_segments`: the own-file header and legend at its TOP, and its docstring (D8) | `#report`, including the `by family` block and the `other` note |
| `#report_breaches`: leaving out the reconciliation line when `own_file` is set | `#report_segments`' two closing comparability prints (0.9.4 and #377) and their comments |
| `#main`: the plain hint inside `render()`, and reusing `subagent_transcripts`' result | `skills/verify/SKILL.md`'s #377 family paragraph |
| `#emit`: its docstring only (D9) | |
| `skills/verify/SKILL.md` §*Measure the segment*, step 1's resumed, *measured on its own* and segment/spawn-cycle paragraphs (D1–D3) | |

The only file both items edit is `session_cost.py`, plus `SKILL.md` if B
adds a family paragraph. In both, this item's hunks sit away from B's, so
B's rebase meets no conflicting hunk. **The builder must not reflow or
re-wrap any line in the right-hand column.** A reflow there is a conflict
created for nobody.

**Failure scenario, six months out.** A harness rewords *The coordinator
sent a message while you were working:*. The own file then has no marker,
takes the empty branch again, and the plain hint disappears. That is today's
behaviour, and no line says it happened. The plain reading's `idle` share
is the only sign left. `COORDINATOR_MESSAGE`'s comment already names this
failure, choosing *loud* for the walked route (the idle-gap floor). The own
file's empty branch is not loud. Accepted: the other direction would slice
on `isMeta` alone, which the same comment rejects on measured grounds.

**Second failure scenario.** A harness starts writing an agent's children
under `agent-<id>/subagents/`. A resumed agent that spawned would then take
the walked path, print its children and not its own slices, and the plain
hint would stay silent (it uses In 1's condition). The reading is not
wrong, but it does not include the own file's slices. Measured absent today
(`spec.md` §*Harness layout*). The walked path's own `§6` reconciliation
line would be what shows it first.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Option 1, triggered by the marker** (no transcripts beside, and `resume_cuts(path)` non-empty) | as above: a reworded marker falls back to today | **chosen**. The marker is the fact the split rests on. It leaves every marker-less file's empty branch byte-identical, the ticket's *must not break* |
| Option 1 as the ticket words it, **triggered by the directory** (the file sits under `subagents/`) | a marker-less agent file's `--segments` stops printing the empty branch, which the ticket says must not break. A resumed file copied out of `subagents/` still reads `0 segments found`, which is the bug | rejected |
| Directory **and** marker | the only case it excludes beyond the marker rule is the copied resumed file, and excluding it is the bug again | rejected |
| Option 2: plain mode prints one reading per slice | every plain reading of a resumed file changes shape. `#analyse`'s docstring forbids that, and #200 and #202 are what breaking it cost | rejected (the ticket's own verdict, and the docstring's) |
| **Option 3: plain mode adds one line pointing at `--segments`** | a reader who never reads past the numbers still quotes the whole-file span | **chosen beside option 1**. `SKILL.md`'s *One segment measured on its own is still `session_cost.py <transcript>`* sends a lone segment to the plain reading, and #601's five whole-transcript readings are that route taken. The line is on the page at the moment of misreading, and it moves no number |
| A document-only fix: tell the orchestrator to run `--segments` on the run's main transcript | `SKILL.md` step 1 already says *against the **run's** transcript*, and five releases of flow logs measured the agent's file anyway. #535 says why: the harness's task output is the path the orchestrator holds | rejected. A sentence already failed here, and a mechanism does not rely on it |
| Branch in `report_segments` only, leaving `measure_segments` empty | `--json` and the page disagree about the same file, and `--post` of `--json` is refused anyway, so the JSON would be the one reading that is missing | rejected. `measure_segments` is the one place rows come from |
| Name the own-file rows from `agent-<id>.meta.json`, or by walking up to `<session>.jsonl` and joining | adds a read of a harness file whose format nobody here owns, or a second route to a name the join already provides from the run's transcript | out of this item (`spec.md` *Out*). The orchestrator decides whether to file it |
| Count the own file in `unnamed` | `report_breaches` then prints *against 1 segment the parent could not name, and the two do not agree* for an agent that spawned nothing. That sends a reader looking for a child transcript that was never missing, which is the failure `measure_segments`' comment on `unnamed` records | rejected. `unnamed` counts walked files, and the own-file branch prints no join counts |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **`--segments` slices an own file.** The own-file branch in `measure_segments` (`own_file`, `unnamed` 0, rows from `segment_slices`). The own-file header and legend in `report_segments`. `report_breaches` leaves out its reconciliation line when `own_file` is set. Cases S1, S2, S2b, S3, S4, S5, S6, S7, S9. The sentences this phase makes false, in the same commit: D1, D3–D11, with S11's pin for D1. The changelog fragment's entry, with the published readings named (`spec.md` In 6) | S1–S3, S5–S7 red at `ab116d1e` and green after. S4 red under the mutant that drops the marker condition. S9 red under the mutant that skips `emit`'s substitution. S11's D1 pin red with the new sentence deleted. S10's cases pass unchanged. Narrow modules: `tests/test_session_cost.py`, `tests/test_session_cost_post.py`, `tests/test_a_segment_feeds_the_flow_log.py`, `tests/test_one_word_one_meaning.py`, `tests/test_a_derived_number_reaching_an_int_carries_a_guard.py`, and every module that reads `README.md`, `README.ko.md` or `skills/verify/SKILL.md` (`git grep -l` at the tip) | 162b3754 |
| 2 | **The plain hint.** `main`'s `render()` prints the line under In 1's condition, after `--latest`'s path line and before `span`. The hint reuses the `subagent_transcripts` result `main` already holds. Case S8. D2 in the same commit, with S11's pin for D2 in `tests/test_a_segment_feeds_the_flow_log.py`. The changelog entry extended with the hint | S8 red at `ab116d1e`. The S11 pin red with the new sentence deleted. `test_no_existing_printed_line_moves_when_the_mode_is_not_asked_for` passes unchanged. The same narrow modules as phase 1 | cf2eb9d3 |
| 3 | **The ledger and the real transcript.** `evidence-check` at the tip names the drifted rows. Found by grep before the build: `seal/releases/0.11.3.md` (`#measure_segments`, `#report_breaches`, two `SKILL.md` §*Measure the segment* rows), `seal/releases/0.15.6.md` (`#report_segments` with that section), `seal/releases/0.13.1.md` (`#emit` with `test_the_posted_body_does_not_carry_the_transcripts_path`, plus two section rows), and the section's rows in `0.8.0`, `0.8.2` (two) and `0.9.5` (four). Each is re-read against the edit and re-stamped in its own file with a dated note, and `Corrected <date>` goes on any claim the edit made false. New rows go in `seal/ledger/1790562540-a-resumed-agents-own-transcript-is-sliced.md`: the trigger, the `own_file` key, `unnamed` over walked files, and the hint's condition. S12: the ticket's three commands on a real resumed agent transcript on this machine (`questions.md` Q1) | `evidence-check`'s exit code, read directly (contract §1), with no DRIFTED row of this work's left un-re-read. S12's three outputs in `phases/phase-3.md`, with the slices from both routes shown equal | 53c55a21 |

What each phase finds that the next needs goes in
`seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

The suite, the repository-wide lint and the format check are not run in any
phase. They are the broad gate, run once by `sealer` after the review rounds
settle (`seal/config.md`, *Broad gate*).

## Operational impact

None to deploy. No migration, environment variable or dependency.
`session_cost.py` stays standard-library only and copyable alone.

What a person running the meter sees:

- `--segments <resumed agent file>` prints slices instead of
  `0 segments found`.
- The plain reading of that file gains one line.
- `--json` of that file gains rows and an `own_file` key.

Every other invocation's output is byte-identical.
