<!-- seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **An agent's own wall clock was in no column of any row, and
  `session-cost --segments` is the column.** Every other kind of chain
  segment can be measured — the cost of a smith, a warden, an orchestrator's
  spawn cycles — and the one number nobody could print was how long a spawned
  agent actually ran. On this harness the `Agent` tool result is written when
  the spawn is **accepted**, so the `--spawns` table's `delegated` reads a few
  seconds while the agent goes on working for a median of about a thousand.
  That interval sat between two rows and inside none of them. It was always in
  the agent's own transcript; nothing opened it.

  The new mode does. It walks every transcript under the run's
  `<session-id>/subagents/`, joins each to the spawn whose result it opened
  at, and prints one row per segment — the agent, its own span, calls, tools
  per turn, mean gap and tokens. On a real run of this repository that is six
  rows reading 5.9m to 8.9m, beside a `--spawns` table that reported the same
  six agents as seconds.

  - **What changes for you.** One command replaces one `session_cost.py` per
    transcript at every segment boundary, and
    `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*
    now names it instead of prescribing the by-hand method. Both README
    editions gain the row.
  - **What does not change — nothing.** No existing printed line, key or
    number moves. The plain reading and `--spawns` print exactly what they
    printed, which is the condition `analyse`'s own docstring sets and the
    reason #200 and #202 were expensive to discover. `delegated_s` keeps the
    meaning every published `--spawns` reading was taken with; the repository
    owner answered that deliberately rather than by default, and may revisit
    it now that there is a reading to look at.
  - **A resumed agent is one row per stretch of work, not one per file.** The
    coordinator sends a running agent a new message and the agent goes on in
    the same transcript, so the idle gap between two stretches belongs to
    neither. Read whole, such a file reports a span covering the wait — 140.1
    minutes for an agent that worked for 37 seconds, on this repository's own
    fixture. The cut is the coordinator's own message row, and it was measured
    before it was built: across the 350 segment transcripts on one machine, 41
    hold an idle gap at or above the fifteen-minute ceiling, and the marker is
    the harness's own sentence rather than the row's shape — the same shape
    also carries a cut-off-response notice and a background-task
    notification, and splitting at those would cut one stretch of work in
    half.
  - **Where it cannot split, it says so.** A file with an idle gap and no
    coordinator message prints one row and the report names the gap and what
    it does to the span. That is also how a harness rewording the marker
    fails: loudly, on the page, rather than by quietly reporting two hours of
    waiting as work.
  - **It refuses to render an empty table.** The mode prints the transcripts
    it walked, the spawns it found, the tolerance it joined within and the
    count unmatched on each side — even when they agree — and where it found
    no segment it prints the count and no table. An empty table reads as *this
    run spawned nothing*, and a run that did spawn reads exactly the same way
    the moment a harness moves the directory. That is #200's failure shape,
    repaid the way #200 was.
  - **The join tolerance was re-measured rather than inherited.** One second
    stands: over the 43 runs on the machine that built this, 296 of 349
    segment transcripts are named at 1.0s and 301 at 2.0s, and the remainder
    is structural — 44 of them have no `Agent` call in their parent to be
    named by at any tolerance, because a subagent of a subagent is spawned
    from a transcript the parent never sees. Those get a row labelled by their
    file rather than being dropped.
  - **A reading is comparable with readings taken since 0.9.4 and not before
    it**, and the report says so on the page. #200 charged this repository's
    own test runner to the `other` family and #202 counted a streamed message
    at its first partial row; both are repaired in the code this builds on.
  - **The token column covers each segment's own file**, and the report says
    that too, because a column that looks summable and is not is #200's
    failure shape in a new place.

- **A segment that spawned another agent now says so, with the count and the
  section it broke.** `skills/agent-contract/SKILL.md` §6 withholds four acts
  from every agent whatever its own definition says, and one of them is
  spawning. Delivery was never the problem: one review round spawned two
  agents and disclosed neither, with the rule already in that agent's startup
  payload, in a section the same agent was reviewing a diff of. So this is not
  a second place to put the rule — it is a place the act shows up whether or
  not anybody mentions it, found by the walk the new mode already does.

  - **What it is, and what it deliberately is not.** It notices and stops
    nothing. That is the claim the evidence's location permits rather than a
    softer one chosen on taste: the transcript is under the home directory of
    the machine that ran the agent, it is in no commit, and it reaches no CI
    runner, so a check would run exactly where a person already is. Making the
    line an exit code stays open and is cheap once the number exists — and it
    will then be chosen against readings rather than against a guess.
  - **The mode exits 0 whether or not it finds one.** A measurement command
    that fails on a discovery is a gate wearing a report's shape, nothing
    consumes its exit code today, and the posting step that would carry the
    finding is the step that would break on it.
  - **Both counts of one breach print, and the page says whether they agree.**
    A spawn made inside a segment arrives twice — as an `Agent` call in that
    segment's own file, and as a transcript with no call in the parent to name
    it. Where the two part, either a child's transcript is missing or a
    segment is unnamed for the other reason, and nothing in the reader can
    tell which.
  - **It is not hypothetical.** Run across all 43 runs with a `subagents/`
    directory on the machine that built it: 13 of the 43 carry a finding, one
    of them a `specseal:warden`.

- **`segment` is brought to one meaning, and checked.** Naming the mode
  `--segments` beside `--spawns` put a second job within reach of a word this
  repository's whole measurement vocabulary rests on. Three shipped files said
  *an orchestrator's segments are spawn cycles*, which under the new flag
  reads as the first mode printing what the second one prints. A segment is
  one agent's own stretch of a chain and has a transcript of its own; the
  spawn cycles inside the orchestrator's file are bands over its own minutes,
  never segments in their own right. `skills/verify/SKILL.md` states it, the
  other two files are brought to it, and `tests/test_one_word_one_meaning.py`
  holds both halves — the pinned phrasing and the absence of the loose one.
