# Feature Specification: the orchestrator segment is measured by the whole session

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The boundary has to be derivable from a transcript. A split a person has to label is the more expensive design and loses to one a script can take |
| `skills/verify/SKILL.md` §*Where a log is open, do the two steps* step 1 | Already prescribes a split for a **resumed** agent — *"split it at the user lines where the coordinator sent it a new message"*. This work writes the sentence beside it for the orchestrator, whose boundary is not a user line |
| `skills/verify/SKILL.md` §*A comparison against a run whose transcript covered only part of its branch says so beside the number* | A slice covers less than the run, so the reading it produces has to say so where it is posted |
| `docs/flow.md` §*0.9.5 — what the readings answer, and what a green gate means* | Orders this first in the release and states why: #51's observation 1 has bands for three segment kinds and none for this one |
| #145 §*Not this* | A cost target and a cost reduction are both out. There is nothing to target until a comparable reading exists |

## Scope

**In.**

- `session_cost.py` gains a mode that slices a transcript into **spawn
  cycles** and reports each as its own segment row — the same numbers a
  `smith` or `warden` row carries (span, command time, model time, calls,
  tools per turn, mean turn gap), so an orchestrator row can sit beside them.
- The **delegated interval** — the `Agent` call's own duration — is excluded
  from the orchestrator's model time and reported as its own number. A
  subagent's thinking is already counted in that subagent's row; charging it
  to the orchestrator too is the double count that makes a cumulative
  reading look like a slow orchestrator.
- The work the run does **outside** any cycle is reported rather than
  dropped: the framing before the first spawn, and the closing work after the
  last report.
- `skills/verify/SKILL.md` gains the instruction, beside the resumed-agent
  one it parallels.
- **A first reading, posted.** Not a conclusion — a band per act of one
  release line's own orchestrator cycles, which a later one can be compared
  against, in the durable log #51.

**Out.**

- A **cost target** for the orchestrator, and any change aimed at making it
  cheaper. #145's own *Not this* refuses both, and #110's does the same on
  the review side.
- Re-testing the spawn-prompt hypothesis (#265's half). It becomes measurable
  with this mode and measuring it is a separate reading.
- The **per-act** split — framing · prompt-writing · verifying a report ·
  writing a record · writing an issue. It is #145's second candidate and it
  needs a person to label the acts, which the goal clause above refuses until
  a cycle-level reading exists to argue against.
- An outcome column (#149). It is the next row of this release.
- The interpreter-floor guard `seal/follow-up.md` asks for on
  `session_cost.py` among four other scripts. That row waits on a decision
  about **where the class belongs** — this file's tracker or that file — and
  a five-script class does not become this work item's because one of its
  members is open in the editor.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A cycle is found where a spawn happened | Given a transcript with two `Agent` calls / when the mode runs / then it reports two cycles, each naming the `subagent_type` it spawned | a case over a fixture transcript |
| A cycle's row is comparable to a segment's row | Given one cycle / when it is reported / then it carries span, command time, model time, calls, tools per turn and mean turn gap, computed by the same function that computes a whole transcript's | a case asserting the cycle row's keys equal the whole-run row's keys |
| The subagent's time is not charged to the orchestrator | Given a cycle whose `Agent` call ran 20 minutes / when the cycle is reported / then that interval is absent from the cycle's model time and present as its delegated number | a case with a fabricated 20-minute `Agent` call: model time unchanged, delegated = 1200s |
| No spawn, no false slice | Given a transcript with no `Agent` call / when the mode runs / then it says so and reports nothing as a cycle | a case over a spawn-free fixture |
| Nothing the run did falls off the table | Given a transcript with one spawn / when the mode runs / then the calls before the first spawn and after the last report are each reported as their own row, and every call in the transcript lands in exactly one row | a case summing the rows' call counts to the transcript's total |
| The instruction reaches whoever measures a segment | Given `skills/verify/SKILL.md` / when a session reaches step 1 / then the orchestrator's boundary is stated there, not only in this work item | the sentence is in the file, beside the resumed-agent one |
| A reading exists to compare the next one against | Given this release line's own transcripts / when the mode is run over them / then a band per cycle is posted to #51 with what it covers stated beside it | the comment, and its `gh issue comment` call |

## Data & interfaces

No schema. One new CLI mode on `skills/verify/scripts/session_cost.py` and
one new key in its `--json` output. The transcript facts it rests on, each
read at the coordinate rather than assumed:

| Fact | Coordinate | Label |
|---|---|---|
| A spawn is a `tool_use` block named `Agent`, whose `input` carries `subagent_type` and `description` | `~/.claude/projects/<project>/*.jsonl` — 131 such blocks across this project's transcripts | executed (`grep -ho '"name":"Agent"'`) |
| A call already carries `start`, `end`, `tool`, `command`, `turn`, so a cycle is a **filter** over the existing call list | `session_cost.py#load` | read |
| `analyse` is a pure function of `(calls, turns)`, so a slice reuses it whole | `session_cost.py#analyse` | read |

## Open questions → questions.md

Two assumptions and one thing that is genuinely undecidable from a
transcript are written there. None of them changes what gets built.
