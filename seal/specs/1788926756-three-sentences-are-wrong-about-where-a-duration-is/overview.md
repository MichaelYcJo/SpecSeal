# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` · `CLAUDE.md`
            §*a ledger coordinate names content*, §*a change writes fragments*,
            §*the merge method is fixed per direction* · `seal/config.md`
            (no `Record language` row → English) · #145's `rounds/round-3.md`
            findings 1, 2, 5 and `rounds/round-3-report.md` §*Paste-ready
            fixes* and §*Executed probes* · `seal/follow-up.md`
· evidence: `seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md`
            — 5 rows added. 14 existing rows re-read and re-stamped across
            `seal/ledger.md` (7) and
            `seal/ledger/1788908215-…​.md` (7), covering 7 drifted anchors and
            18 stamps; 3 sentences in the #145 fragment corrected in place
· verified: **executed** — `bin/test tests/test_session_cost.py` (68 passed),
            the two modules the skill change touches (105 passed with the
            first), `evidence-check` (1033 ok · 0 drifted, exit 0),
            `survivor-check` over the fix range, both span rules over every
            transcript on this machine at run and row level, 11 mutations one
            at a time. **read** — `analyse`, `spawn_cuts`, `in_windows`,
            `spawn_cycles`, `measure_cycles`, `report`, `report_spawns`,
            `share`, `load`. **unverified** — the full suite, the
            repository-wide lint and the typecheck, which are the
            orchestrator's, once, after the rounds settle

## Why this work exists

Three printed sentences said where a duration was and none of them was right
about the code beside it; the third was a span that could come out shorter
than a single call inside it, in the path every published segment reading uses.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What item 3 closes | `spec.md`: *then `span_s` is 1000 and `command` is at or under 100%*, and its scope row: *That closes the plain report's `command 16.8m 101%`* | The span half was built; the share half was measured false and the spec corrected | **Executed.** On that exact shape the span moves 995 → 1000 and the share stays 101%: `command_s` is 1007s against 1000s of wall clock because the three calls overlap. #145's round 3 finding 5 diagnosed one of two causes. The residual is `questions.md` Q3, with the owner and three costed answers |
| The handoff's measurement of what moves | The prompt: *No transcript on this machine has a span that moves under `max(end)` — 15 transcripts … every delta 0.0s* | Re-measured, widened twice, and the claim narrowed to *no printed figure moves* | **Executed.** This project's directory: 16 transcripts, 0 moving spans — the handoff is right there. Machine-wide: one run span moves by 0.006s, and at ROW level, which a run-level sweep does not reach, 8 of 599 rows move and 2 change a printed figure. All 8 are in other projects. Nothing published moves; the literal claim needed the word *printed* |
| The reviewer's grounds for not naming the figure an overlap | Round 3's text: *`analyse` takes a span as the last call TO BEGIN's end … so the outliving call shortens the RUN's span too and the difference carries both errors* | The conclusion kept, the grounds rewritten | Phase 1 removed those grounds — the run's span is now correct. New grounds: every row's interval sits inside the run's, so the difference is the gaps minus the overlap. Refusing to paste is what both prior fix passes on this file did, correctly, twice |
| The reviewer's paste-ready assertion | `assert "the rows' spans sum to 33.1m against the run's own 16.6m"` | `16.7m`, and the magnitude 16.4m rather than 16.5m | The pinned shape's run span moves 995 → 1000 under phase 1, so every figure copied from that report had to be recomputed |
| The reviewer's paste-ready `SKILL.md` text | It dropped *leave the between-the-rows share out of the reading rather than substituting the sum* | Kept and widened to *either sum* | That is the one actionable sentence a person taking a reading needs; dropping it would have traded an instruction for a shorter paragraph |
| Where item 1's clause in `skills/verify/SKILL.md` lands | `plan.md` puts all of that file in phase 3 | Moved to phase 2, with the code it describes | Leaving a sentence there naming a cause the code had stopped naming would put a false sentence in the tree across a phase boundary, which is the class this work item closes |
| The exact-cover boundary case | `spec.md`: *the existing boundary case, still green* | Planted a new one | There was no existing case for `outside == 0`; the only boundary case covers the positive branch at `outside == 304`, and #145's round 3 probed the exact cover without planting anything. Seen red under `> 0` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck — `skills/agent-contract/SKILL.md` §2 keeps them off this segment | the orchestrator, once, after the rounds settle |
| What the report should print where `command` exceeds 100% of the span — `questions.md` Q3, measured and costed, not built | the owner |
| Whether the span's disclosure belongs in the report's own output as well as in `skills/verify/SKILL.md` — `questions.md` §*Open, and it is small* | the owner |
| Windows | nobody has run it — #103's standing gap |

## Not done

**`command_s` was left summing overlapping calls.** Taking it to the union of
the call intervals would make the share unable to pass 100%, and it would also
change what the number means — from command time to wall clock with a command
running — breaking the comparability `analyse`'s own docstring exists to
protect. It is a printed-output decision, so it is the owner's and a work item
of its own. `questions.md` Q3 carries it with the measurement.

**The `>= 0` branch's own imprecision was left standing and named instead.**
What it prints is the gaps between the rows minus their overlap, so *N of the
run is BETWEEN the rows* is a floor rather than an exact figure wherever a
small overlap is netted against larger gaps. The word `mostly` already hedges
it, `spec.md` requires that sentence to stay as it is, and the comment now
says which direction the figure errs in. Turning it into an exact figure needs
a union computation, which is mechanism this work item was not asked for.

**No `# RIDER:` was planted in `analyse` or `report_spawns`.** Both carry
ledger anchors — 7 rows between them — and a comment inside either drifts
them. The facts went to `questions.md` and to the fragment rows instead, which
is where #145's round 3 put the same judgment.

## Fed back into the spec

Two clauses, both inferred during implementation and both open to being
overturned:

- **A window's span can never be shorter than a single call the window
  counts.** This is the invariant the new rule establishes and it is what the
  case asserts, rather than the weaker *the span equals 1000 on this fixture*.
  `spec.md`'s scenario row was rewritten to it.
- **A share above 100% of a span is a true reading, not a broken number**,
  because command time is a sum over calls and calls can run concurrently. The
  span rule narrows it and cannot close it. Stated in
  `skills/verify/SKILL.md` where a reader meets a published share, and left
  as Q3 for the owner to decide what the report itself should say.
