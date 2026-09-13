# Implementation Plan: a segment's own wall clock is in no column

<!-- seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Add one report mode to `skills/verify/scripts/session_cost.py` that opens each
spawned segment's own transcript and prints a row for it. The join key is
measured and already written down in the tree: a segment transcript opens at
its spawn's `tool_result` stamp, and the spawn's `input` carries
`subagent_type`. Everything the mode needs but time is already there —
`subagent_transcripts` walks the directory, `token_totals` sums the tokens,
`analyse` produces the numbers for any call list.

The same walk answers #343. A spawn made inside a segment shows up twice — as
an `Agent` call in that segment's own transcript, and as a nested transcript
the parent cannot name — and the mode prints both, because the two counts
disagreeing is itself a reading.

Nothing existing changes shape. The plain report and `--spawns` print what
they printed, which is the condition `analyse`'s own docstring sets and the
reason #200 and #202 were expensive.

## Technical context

**What exists** (all coordinates in `skills/verify/scripts/session_cost.py`
unless named otherwise):

| Coordinate | What it gives this work |
|---|---|
| `#subagent_transcripts` (:817) | every `*.jsonl` under `<session-id>/subagents/`, walked recursively and sorted; a missing directory returns `[]` |
| `#spawn_cuts` (:583) | the `Agent` calls sorted by result arrival, each carrying `spawn` labels from `#spawn_labels` (:257) |
| `#analyse` (:426) | span, calls, `call_turns`, `tools_per_turn`, `gap_mean_s`, `by_family`, for any call list |
| `#token_totals` (:839) | the token fields for a list of paths, with the post-#202 maximum-per-message rule |
| `#load` (:300) | calls and per-turn input counts — **paired tool calls only**, which is why the join needs a new reader |
| `#report_spawns` (:1131) | the shape a refusal takes when the table would be empty, and the sentence this work item exists to answer |
| `tests/test_session_cost.py#write_run` (:377), `#spawn` (:1621), `#orchestrator` (:1647) | the fixture builders, including a tree with a nested segment |

**The one new reader.** `load` returns only paired tool calls, so a
transcript's opening row is not in anything this script currently produces.
The join is against the file's first parseable `timestamp`, because that is
what the measurement was taken against — *each subagent's transcript OPENS at
its spawn's result stamp*. Joining on the segment's first **tool call**
instead would be late by however long the agent read and thought first, which
`#265` measured as a payload of about 110,000 characters before an agent's
first call. The new reader stops at the first usable stamp rather than
scanning the file.

**Constraints that decide the shape.**

- A published number's meaning may not move. `#analyse`'s docstring states it
  and #200 and #202 are what breaking it cost. So: a new flag, a new key, and
  no edit to any existing printed line.
- The evidence lives outside the repository. A transcript is under
  `~/.claude/projects/`, never in a commit, so nothing in CI can read one.
  That is what makes #343's answer a report line rather than a check.
- `segment` is a load-bearing word with a checked meaning
  (`tests/test_one_word_one_meaning.py`). Naming the mode `--segments` means
  the word gets a case.
- Fixtures use `tmp_path`. `tests/test_no_real_identifiers.py` refuses a real
  domain, user path or org name, and a transcript fixture is exactly where one
  leaks in. Every path in a new fixture is built from `tmp_path`, and any
  literal path in prose or a docstring is `/Users/x/` or `example.com`.

**The failure scenario in six months.** The harness stops writing a spawn as
an `Agent` `tool_use` block, or stops opening a subagent transcript at its
spawn's result, or moves the directory. The join then matches nothing, and an
empty table reads as *this run spawned nothing* — which is #200's failure
shape exactly. The mode is built to fail the other way: it prints the number
of transcripts it walked, the number of spawns it found, the tolerance it
joined within, and how many segments each side left unmatched, and it refuses
to render a table when it found no segment. This is the same repair
`#report_spawns` already took for the zero-spawn case, and it is why the
counts are printed even when they agree.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Add a second table to `--spawns` rather than a new flag | Every existing `--spawns` invocation changes what it prints, including the ones the release's measurement loop runs at each boundary. A reader comparing two readings across versions cannot tell a format change from a measurement change, which is what made #200 and #202 expensive to discover | rejected — `#analyse`'s docstring sets the condition, and a new flag costs one `add_argument` line |
| Name the flag `--subagents`, after the directory | A person measuring a segment has to know the harness's directory name to find the flag. Everything else in this repository's measurement vocabulary — `skills/verify/SKILL.md` §*Measure the segment*, the bars in `docs/review-handoff-protocol.md`, the flow log — says *segment* | rejected; `--segments` is chosen, with the cost paid openly by pinning the word (phase 2) |
| Join on the segment's first **tool call** instead of the file's first row | Late by the agent's whole startup read — about 110,000 characters before the first call, measured in #265 — so the tolerance would have to widen from one second to minutes, and a wide tolerance matches the wrong spawn in a batch of two | rejected — the measurement was taken against the file's opening, so the join is too |
| Match a segment to its spawn by a field inside the transcript rather than by a stamp | No such field has been measured. A defence against a rename that has not happened is a defence nothing can test — the `#DELEGATING` comment settles this for `subagent_type` already, on the same grounds | rejected; the stamp join is measured and the report names what it could not match |
| #343 as a field the handover must carry | The agent that broke §6 silently is the agent asked to fill the field. Round 1 of #120 spawned two agents and disclosed neither, with the rule already in its payload — a second thing for the same silence to skip | rejected — #343's own reasoning is that delivery worked and the act still went the other way |
| #343 as a CI check, or any check that fails a build | There is nothing for it to read. The transcript is on the machine that ran the agent and reaches no runner, so the check would run exactly where a person already is | rejected as impossible rather than as unwanted |
| #343 as a `PreToolUse` hook denying `Agent` | It fires in the orchestrator session too, which spawns legitimately, and prevention is not what the issue asks for. A hook that has to tell an agent from its orchestrator is a new classification problem in the deny path | rejected; recorded here so the next reader does not re-open it |
| Leave a resumed segment's transcript as one whole-file row | The reading covers two runs and the idle gap between them. The hand method was to subtract the first reading, and a mode that inherits the behaviour has not solved the problem it was built for | rejected — phase 3 slices, with a named floor when the marker is absent |
| Move the joined span into `delegated_s` (#145's Q4, third answer) | It changes what a published column means, in every `--spawns` reading taken so far, with nothing on the page saying so | out of scope, and it is the owner's — `questions.md` Q1, default *leave it* |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The join. A reader for a transcript's first stamp, and `measure_segments()` matching each transcript under `subagents/` to a spawn result within the tolerance — named where it matches, named by nobody where it does not, one spawn claimed at most once. `--json` gains a `segments` key beside `spawns` | Cases on a tree built by `write_run`: a named segment, an unnamed nested one, a segment moved outside the tolerance, and a run with no `subagents/` directory. Each red first — the key does not exist before this phase | `dea1e7c` |
| 2 | The printed mode. `--segments` prints one row per segment (agent · span · calls · t/turn · gap · tokens), states the unnamed count, names the tolerance it joined within, prints the transcripts-walked and spawns-found counts even when they agree, and refuses a table when it found no segment. `segment` brought to one meaning where a spawn cycle is currently called one | Output cases pinning each printed line, red first (contract §14 — a change to what a person reads is documented and pinned). The word case in `tests/test_one_word_one_meaning.py`, asserting the pinned phrasing **and** the absence of the loose one, which is that module's established shape | `47a1959` |
| 3 | The resume slice. Split a segment transcript at the coordinator's own message rows and emit one row per slice, named by inheritance from the file's first slice. Where no marker is found and an idle gap above `analyse`'s 900-second ceiling is, one row prints and the report names the gap and what it does to the span | A two-slice fixture: each slice's span asserted against the fixture's stamps, and their sum asserted to be less than the file's own span — the assertion the whole-file reading fails. A marker-less fixture for the floor. `questions.md` Q2 is settled by a probe at the top of this phase, before the shape is fixed | `8c01e9a` |
| 4 | #343. Each segment row carries its own spawn count, taken from that segment's own `Agent` calls; a non-zero count prints a line naming the agent, the count and §6. The count of nested transcripts is reconciled against it, and a disagreement is printed rather than resolved | A fixture where a named segment's transcript holds an `Agent` call and a nested transcript sits under it: the line names the agent and the count. The negative case — segments with no `Agent` call print no line — is what keeps this from being a check that cannot fail, and it is planted in the same commit | `fce9ba0` |
| 5 | The sentence becomes a command. `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* names the mode in place of one invocation per transcript and of the hand split; the script's module docstring gains the mode; both README editions gain it in the `session-cost` row; `changelog.md` and `seal/ledger/1789296300-…​.md` are written | Cases in `tests/test_a_segment_feeds_the_flow_log.py`, which already pins that section, red first. Both README editions checked for the parity cases that read them before either is edited | |

**Why the order.** Phase 1 is the only phase that can be wrong in a way the
others cannot repair — if the join does not hold, every row is named wrong and
nothing downstream is worth building. Phases 2 and 4 both print, and 4 is
separated because it is a second issue with a negative case of its own: a
breach line nobody has seen fail is a counterfeit seal. Phase 3 sits between
them because it changes what a *row* is, and phase 4's per-row count has to be
per segment rather than per file for the line to name the right agent. Phase 5
is last because a document naming a mode that does not print yet is a document
that lies for four phases.

**What every phase runs.** The module's own cases —
`bin/test tests/test_session_cost.py -q` — plus the document module a phase
touches. The full suite, the repository-wide lint and the typecheck are the
broad gate, they are one act with one owner, and no phase of this plan runs
them (contract §2).

**Red first, per contract §15.** Phases 1, 2 and 4 add behaviour that does not
exist, so each new case is red against the module as it stands and the phase
record says so with the failure it showed. Phase 3's slice cases are the
exception worth naming: the mode will already print a row for a resumed file
before the slice lands, so those cases are shown red against **that** row — one
row where two are owed, and a span covering the idle gap — rather than against
a missing key.

## Operational impact

No migration, no new environment variable, no new dependency, and no
compatibility break. One new flag on a script already on PATH as
`session-cost`, and one new key in `--json`.

Two things a reader of the output must not miss, and the mode prints both
rather than leaving them to be inferred:

- **A segment row's tokens cover that segment's own file only.** The run total
  sums the whole tree, so the two are not the same number and the column is
  summable only with the parent's own row.
- **A reading is comparable with readings taken since 0.9.4 and not before
  it.** #200 and #202 both moved what the token and family rows mean, and both
  are fixed in the code this builds on.
