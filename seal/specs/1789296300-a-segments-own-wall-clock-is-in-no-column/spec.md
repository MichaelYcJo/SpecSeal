# Feature Specification: a segment's own wall clock is in no column

<!-- seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

This work item carries **#350 and #343 together**. Both land on one unbuilt
thing: a reader that opens a spawned segment's own transcript. #350 wants that
segment's span, calls and gaps in a column. #343 wants an `Agent` call made
*inside* such a segment noticed by something other than a person reading a
transcript afterwards. The nested transcript #350 must count as unnamed and
the spawn #343 must notice are the same fact arriving twice, which is why one
join answers both.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md:146` §6 | The rule #343 is about, in its own words: *post nothing, push nothing, open no pull request, and **spawn no agent***. The breach line cites this section by number, and §*How the sections are numbered* is why a number is safe to cite |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* (:426–530) | The rule that becomes a command. It already names the hand method this replaces — one `session_cost.py` per transcript, and for a resumed smith *split it at the user lines where the coordinator sent it a new message, and measure only the slice that belongs to the segment just watched*. The resume slice is therefore a documented transcript fact rather than a new invention |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides the shape of #343's answer against the shape that stops to ask. It does not settle it alone — what settles it is where the evidence lives, below |
| #145's `questions.md` §Q4, third row | The join is one of three costed answers to a question the owner has open, and its verdict line is *it belongs to a work item of its own*. **This work item is that home for the join and not for `delegated_s`** — Q4 is reproduced as Q1 of `questions.md` here, unchanged in substance |
| `skills/verify/scripts/session_cost.py#analyse` docstring | *Changing what the plain reading prints would make every reading this repository has already published incomparable with the next one* — the rule that makes this a new mode rather than a wider `--spawns` |
| `docs/review-handoff-protocol.md:552–570` | The per-segment bars. The `t/turn` column of the new table is the number those bars are read against, and today a person applies them one transcript at a time |
| `CLAUDE.md` §*a thing more than one party can have is named with whose*, with `tests/test_one_word_one_meaning.py` | `segment` is load-bearing before this work starts. Naming the mode makes it a checked word |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to this directory's `changelog.md` and the ledger rows to `seal/ledger/1789296300-…​.md`. Neither `CHANGELOG.md` nor `seal/ledger.md` is touched — nothing here removes code an existing row cites |
| `skills/agent-contract/SKILL.md` §15 | Every case this work plants is seen red first. `plan.md` says how for each |

## Scope

### In

- **A new report mode, `--segments`**, printing one row per spawned segment of
  a run — the agent it was, its own span, calls, tools per turn, mean gap and
  tokens — read from that segment's own transcript rather than from the
  parent's columns. This is #350's first `Done when` bullet.
- **The join, asserted rather than assumed.** A segment is named by matching
  its transcript's opening stamp to a spawn's `tool_result` stamp, within a
  stated tolerance the report prints. The spawn's `input` carries
  `subagent_type`, which is the name on the row.
- **Segments the parent cannot name are counted and printed, never dropped.**
  A subagent of a subagent has no `Agent` call in the parent transcript at
  all, so no stamp can name it. It gets a row labelled as named by nobody, and
  the count of such rows is stated in prose. This is the direction `tool_name`
  and `count` already take one function over: a smaller answer rather than
  none.
- **A run with no `subagents/` directory prints a reading rather than
  raising** — the ordinary case for a segment measured on its own.
- **A resumed segment's transcript is sliced**, so one row is one segment
  rather than one file. `skills/verify/SKILL.md` already prescribes this split
  by hand and names its marker; a mode that inherits the whole-file reading has
  not solved the problem it was built for.
- **#343's answer: each segment row carries its own spawn count, and a
  non-zero one prints a line naming the agent, the count and §6.** The section
  below says what that was chosen over.
- **The sentence becomes a command.** `skills/verify/SKILL.md` §*Measure the
  segment, and feed the flow log* names the new mode in place of the hand
  method, and both README editions gain it in the `session-cost` row.
- **`segment` is brought to one meaning and pinned**, because naming the mode
  `--segments` is what puts a second job within reach of the word.

### Out, each with the reason

- **`delegated_s` keeps the meaning it has.** Changing it is #145's Q4, it
  moves a number in every reading this repository has published, and it is the
  owner's. The new mode is additive: no existing output changes shape, no
  existing number changes meaning. `questions.md` Q1 is where that sits, with
  a default that does not block.
- **How a call is assigned to a window.** Assignment by start is what makes
  the calls partition, two ledger rows are anchored on that property, and #145
  spent three rounds establishing it. Nothing here touches `in_windows`.
- **The `--spawns` cycle table.** It answers a different question — where the
  orchestrator's own minutes went — and its rows are the parent's calls. The
  two modes sit beside each other.
- **Any gate that fails on a spawn.** This work item produces the number. Whether
  the number ever fails a build is a decision nobody can make before anybody
  has seen one, and the section below says why it cannot be a CI check at all.
- **Preventing a spawn.** #343 asks for something that notices, and says why:
  the rule already arrived by mechanism before the agent's first tool call and
  the act still went the other way. A `PreToolUse` hook denying `Agent` would
  also fire in the orchestrator session, which spawns legitimately.
- **#354 and #345**, the other two work items of 0.11.3. Different scripts,
  their own branches.

## What #343's shape is, and what it was chosen over

#343 leaves its own shape open: *whether that becomes a check, a line in the
segment report, or a field the handover has to carry is the open question.*

**Chosen: a line in the segment report**, carried by the per-segment row this
work item is building anyway.

Two of the three options are eliminated by facts rather than by preference,
which is why this is decided here and not put to a person.

- **A check cannot exist in the automated form this repository prefers.** The
  evidence is a transcript under `~/.claude/projects/`, on the machine that
  ran the agent. It is in no commit, reaches no pull request, and is not on a
  CI runner. A checker that reads one runs exactly where a person already is.
- **A field the handover carries is delivery again.** #343's own reasoning is
  that delivery worked: the rule was in the agent's payload, through the
  `skills:` frontmatter, in a section that same agent was reviewing a diff of,
  and round 1 spawned two and disclosed neither. Asking the agent that broke
  the rule silently to fill in a field about it adds a second thing for the
  same silence to skip.

What the report can do that neither can: it runs at the boundary where the
breach has to be noticed. `skills/verify/SKILL.md` §*Measure the segment* puts
a `session_cost.py` reading at the end of every smith and warden segment
already, and #350's mode is that reading. The spawn is found by the same walk
that has to count nested transcripts regardless.

**What the choice gives up, stated rather than left to be found.** A line in a
report is read by a person who can skip it, so this notices and does not stop
anything. That is a smaller claim than a gate, and it is the claim the
evidence's location permits. The escalation stays open and is cheap once the
number exists: a later work item can make the line an exit code, and it will
be choosing against readings rather than against a guess.

**The mode exits 0 whether or not it finds a spawn.** A measurement command
that fails on a finding is a gate wearing the shape of a report, nothing
consumes its exit code today, and the orchestrator's own posting step would
break on the finding it is meant to post. Rejected with that consequence named
rather than on taste.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A spawned segment gets its own row | Given a parent transcript with two spawns and a transcript for each under `<session-id>/subagents/` / when `--segments` runs / then two rows print, each named by its spawn's `subagent_type`, each carrying span, calls, tools per turn, mean gap and tokens read from its own file | a case asserting both rows' names and numbers against the fixture's own stamps, red first because the mode does not exist |
| The join is asserted against the measured stamp | Given a segment transcript whose first row's stamp equals its spawn's `tool_result` stamp / when the join runs / then that segment carries that spawn's name, and a segment whose opening stamp matches no spawn result within the tolerance carries none | a case pinning both directions, including one segment moved outside the tolerance so the match is shown to be able to fail |
| A segment the parent cannot name is counted, not dropped | Given a nested transcript under another segment's directory, with no `Agent` call in the parent / when `--segments` runs / then it gets a row marked as named by nobody, and the printed count of such rows says how many there were | a case on the nested tree, asserting both the row and the stated count |
| A run with no `subagents/` directory reads rather than raises | Given a transcript measured on its own / when `--segments` runs / then it prints that it found no segment and why, and exits 0 | a case asserting the exit code and the sentence, in the shape `report_spawns` already uses for zero spawns |
| A resumed segment is one row per segment, not one per file | Given one segment transcript holding two runs separated by an idle gap and a coordinator message / when `--segments` runs / then two rows print and neither span covers the idle gap | a case on a two-slice fixture, asserting each slice's span against the fixture's stamps and asserting the sum is less than the file's own span |
| Where the slice cannot be taken, the reading says so | Given a segment transcript with an idle gap above the model-time ceiling and no slice marker / when `--segments` runs / then one row prints and the report names the gap and what it means for the span | a case on a marker-less fixture, asserting the named gap |
| A spawn inside a segment is named | Given a named segment whose own transcript holds an `Agent` call / when `--segments` runs / then the report prints a line naming that agent, the count, and §6 | a case asserting the line, red first |
| A clean run prints no such line | Given segments with no `Agent` call in any of them / when `--segments` runs / then no §6 line prints | the negative half of the same case — a check that cannot fail is a counterfeit seal |
| No existing output changes | Given any transcript / when the plain report and `--spawns` run / then every number and every line is what it was | the existing cases in `tests/test_session_cost.py`, still green, named in the phase record |
| The rule is a command a session can type | Given `skills/verify/SKILL.md` §*Measure the segment* / when a session reads it / then it names the mode and no longer prescribes one invocation per transcript | cases in `tests/test_a_segment_feeds_the_flow_log.py`, which already pins that section |
| `segment` has one meaning | Given the documents this work touches / when they are read / then a spawn cycle is not called a segment | a case in `tests/test_one_word_one_meaning.py`, asserting the pinned phrasing and the absence of the loose one, which is that module's established shape |

## Data & interfaces

No schema and no new file. One new flag, one new key in `--json`, and a table.

| Fact | Coordinate | Label |
|---|---|---|
| `subagent_transcripts` already walks `<session-id>/subagents/` recursively and returns the files sorted; a missing directory returns nothing rather than raising | `skills/verify/scripts/session_cost.py#subagent_transcripts` (:817) | read |
| `token_totals` already sums a list of transcripts and reports how many it opened. Time is the one thing not carried across — it takes paths and returns token fields only | `skills/verify/scripts/session_cost.py#token_totals` (:839) | read |
| `spawn_cuts` returns the `Agent` calls sorted by when each result arrived, and each call carries `spawn` labels holding `subagent_type` and `description` | `skills/verify/scripts/session_cost.py#spawn_cuts` (:583), `#spawn_labels` (:257) | read |
| The join measurement: an `Agent` call's own tool_use-to-tool_result interval is 1.5–3.7 s across 67 spawns of three runs, and each subagent transcript opens at its spawn's result stamp — 61 of 67 within one second, the six misses being subagents of subagents, which have no call in the main transcript at all | the block comment above `#DELEGATING` (:219–253), and #145's `questions.md` §Q4 table | **read, at the coordinate.** The 67 and the 61 are aggregates, not coordinates: what this work asserts is the join on a fixture it builds, and `questions.md` Q3 re-measures the tolerance on current transcripts |
| `load` records only **paired tool calls**, so a transcript's opening row is not in what it returns. The join needs the file's first parseable `timestamp`, which nothing in this script reads today | `skills/verify/scripts/session_cost.py#load` (:300) | read — this is the one genuinely new reader the join needs |
| `analyse` takes a window's span as `max(end) - calls[0]["start"]` over the calls it is given, and its model walk drops any gap of 900 s or more. Handed a resumed transcript's whole call list it returns a span covering the idle gap, while the mean gap excludes it | `skills/verify/scripts/session_cost.py#analyse` (:426) | read — this is the resumed-transcript defect, confirmed in the code and not only in the run log |
| The hand method, including the resume split: *a resumed smith's transcript holds several segments in one file — split it at the user lines where the coordinator sent it a new message* | `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* (:490–493) | read |
| The fixture machinery exists: `write_run(tmp_path, main_lines, subagents=None)` builds a transcript tree, `spawn(uid, start, end, subagent_type, …)` builds an `Agent` call and its result, and a nested-segment case already ships | `tests/test_session_cost.py#write_run` (:377), `#spawn` (:1621), `#test_a_segment_of_a_segment_is_still_part_of_the_run` (:487) | read — #350's fourth bullet asks for a tree with a named, an unnamed and a nested segment, and two thirds of that builder is already here |
| §6's list, to cite exactly | `skills/agent-contract/SKILL.md:146` | read |

## The two instrument defects — both closed, and the frame says so

The task handed me #200 and #202 as live defects whose readings this work
would have to be careful around. **Both are closed, shipped in 0.9.4, and
fixed in the code this work item builds on.** Nothing here is owed a
work-around, and no reading this mode produces carries either error.

| Defect | State | Where the fix is |
|---|---|---|
| #200 — the `test` family does not know this repository's runner | CLOSED, milestone `release: 0.9.4` | `#FAMILIES` (:69) matches `bin/test` and `scripts/test` by path, plus eight more runners by name. The comment above it carries the measurement and cites #200 |
| #202 — a streamed message is counted at its first partial row | CLOSED, milestone `release: 0.9.4` | `#token_totals` (:839) keeps the **largest** count each field reaches per message id, not the first row. The comment at the loop carries the measurement and says why maximum rather than last-row-wins |

That matters for one column of the new table. The per-segment token figures
are produced by the repaired `token_totals`, so they are comparable with every
reading taken since 0.9.4 and not with the ones taken before it. A per-segment
`test` row likewise names this repository's runner.

**Each segment row's tokens cover that segment's own file only.** The run
total already sums the tree, so a reader adding the column across the rows and
the parent gets the run's total once. The mode states this, because a column
that looks summable and is not is #200's failure shape in a new place.

## Open questions → questions.md

Three rows: one for a person that does not block, and two a measurement
settles inside the work. `questions.md` holds them with their defaults.
