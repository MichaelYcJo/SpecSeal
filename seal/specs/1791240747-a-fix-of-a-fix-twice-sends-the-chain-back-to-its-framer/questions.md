# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — questions for the planner

<!-- seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the ticket left open that the tree answered

Listed so nobody reopens them. Each one's grounds are in `spec.md` or in
`plan.md`'s Alternatives table.

| Judgment | Answer | Where the grounds are |
|---|---|---|
| Mechanical rule or orchestrator judgment | **Mechanical.** The owner delegated the decision to the orchestrator, which decided it before this frame was spawned; the tree agrees — the orchestrator noticed once in four chances, and `CLAUDE.md`'s first goal is verification that runs unattended. Recorded as answered; not reopened here | `plan.md` Alternatives A |
| How *lands in a unit the previous fix pass created or changed* is read | From round K-1's `Fix range` (both ends parsed, a unit with a different `ast.dump` is changed) and its `New units`, against round K's open `Location`s resolved at round K's `Target SHA` through `location_units`. The grain is the top-level unit | `spec.md` §Scope *The reading*; `plan.md` Alternatives B, C |
| Which fix pass — the previous only, or any earlier one | The previous. Round K verifies round K-1's fixes; a landing in K-2's untouched units is K-1's miss | `plan.md` Alternatives D |
| Why two and not the 3+ Fix Rule's three | The first landing is the signal, the second its confirmation; both chains in the ticket filed their third fix as an issue that begot another | `plan.md` Alternatives F; `spec.md` Grounding row 1 |
| Whether the row needs a companion `Changed units` row | No. `new` runs where `close` ran, so the range resolves when the units are needed | `plan.md` Alternatives B |
| What the stop writes into `round-N.md` | `Fix of a fix \| second — …`, the open findings closed `deferred the frame` through `close`, `Fixes checked by \| no fixes to check`, `Pass` ticked over deferrals, the pull request labelled `chain: reframed` | `spec.md` §Scope *The stop* |
| What permits the records after the stop | `Reframed <date> by <who>, after round <N>.` at `spec.md`'s foot, written by the framer; `frame_mark` reads the foot block; `<who>` is held to `Planning` as the `Framed` line is | `spec.md` §Scope *The reframe*, *The gate*; `plan.md` Alternatives E |
| What `chain-check` refuses | The eight rows of the gate table: absent after the cutoff, malformed at any age, a miscounted `first`, a third landing in a run, a fix word on a `second`, a record after a `second` with no `Reframed` line, a `Reframed` line disagreeing with `Planning` | `spec.md` §Scope *The gate* |
| Whether the walks and the cap reach across the stop | No. A record after a `second` is not a later record of any record at or before it; the cap's prose count restarts | `spec.md` §Scope *The walks stop at the boundary* |
| Where the rule lives | Owner: a `###` in `skills/code-review/orchestration.md` beside *The cap is a ceiling*. `docs/review-chain-spec.md` is at 994 of 1000 lines and takes a three-line link. The field is documented in `docs/round-record-spec.md`, the protocol and the template | `spec.md` Grounding, §Scope *The documents* |
| The acts-table row | `check: skills/code-review/scripts/chain_check.py`, grounds naming what `new` prints and what the check cannot see (whether the landing was real) | `spec.md` §Scope *The documents* |
| The cutoff | `REFRAME_FROM = 1791240747`, this work item's id, traceable by `conftest.cutoff_item_is_traceable` | `spec.md` §Data & interfaces |
| Fragments under the freeze | New rows in `seal/ledger/1791240747-….md`; released rows whose anchors move are re-read with `evidence-check --reverify --into`; `seal/releases/*` and `seal/ledger.md` unchanged | `spec.md` Grounding; `plan.md` phase 4 |
| Whether `CLAUDE.md`'s 3+ Fix Rule line changes | No. The relation is stated at the owner; a link from `CLAUDE.md` is a one-line follow-up for the repository owner once the home exists | `spec.md` §Out |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How often would the row have read `first` and `second` over the committed corpus — every `round-N.md` under `seal/specs/` at `v0.18.3` whose `Fix range` resolves through the pull request heads this clone carries? The two chains in the ticket are the only instances anybody has measured, and the grain (the top-level unit) is the trade most likely to be wrong. The tree holds the records and the ranges but nobody has run the reading over them, which is why this is not already answered | a measurement — phase 4's replay, widened from the two chains to every record whose range resolves; the number goes into the changelog entry and the overview | A count at or near two says the grain is right. A count well above it on runs nobody remembers as stuck says the grain is too coarse, and the overturn is Alternatives C's hunk-level overlap, with the squash problem it carries | the unit grain, as the spec says | ✅ the measurement, phase 4 (executed; `phases/phase-4.md` holds the method): over every committed record whose previous `Fix range` this clone resolves — 76 at `v0.18.0` and 7 at `v0.18.3`; the 23 at `v0.18.1` and `v0.18.2` resolve nowhere here — the shipped reading writes `first` on 26 records and stops **18 of 57 work items** (15 of 53, and 3 of 4). Counting ⬜ notes as well would have stopped 24, which is why phase 4 made 🟢, ❓ and ⬜ land nowhere. The hunk grain of Alternatives C stops 10, and misses #801, one of the two chains the rule exists for: one of its two landing findings sits inside the function the previous fixes changed and outside every hunk they changed. So the count is well above two and the overturn the row names loses a measured instance. Which way that goes is a person's call, opened as Q4; the build keeps the unit grain |
| Q4 | Is 18 of 57 the stop rate the owner wants? The replay says the unit grain would have sent 18 work items back to their framers, nearly all at round 3, the round the cap ends anyway; the hunk grain sends 10 and misses #801. Nobody here can tell which of the 18 were runs the owner would call stuck | a person — the repository owner | *Keep the unit grain*: every run in which a fix's own function is found wrong twice goes back to the framer, #801 included. *Hunk grain*: Alternatives C, fewer stops, #801 missed, and a `path#unit` `Location` never lands. *Raise the count to three*: Alternatives F, matching the 3+ Fix Rule, and both ticket chains are missed because both ended at round 3 | the unit grain at two, as built | ⬜ |
| Q2 | For a file the AST cannot read (`measure`'s heuristic arm — not Python, or Python that does not parse at one end), does a `Location` in it ever land? The heuristic names ADDED units from `+` lines and knows nothing about changed ones, and no record in the tree has a finding located in such a file by unit | the work — phase 1 decides it where it meets the arm and records a divergence row if it departs from the default | *Never lands* keeps the reading honest about what it measured. *Lands when the heuristic added the unit* reaches the `New units` half only | never lands; the record's existing heuristic comment already says which files were read that way | ✅ the work, phase 1: **never lands**, the default. `round_record.py#fix_pass_units` reads Python files the AST parses at both ends and nothing else, so a file the heuristic reads contributes no unit, and the record's heuristic comment already names such files |
| Q3 | What does `round_record.py#reach_back` write into a previous record whose `Fixes checked by` already reads `no fixes to check`? The redesign's first record follows exactly such a record — the `second` closed on deferrals — and the only committed shape of a record after a `no fixes to check` is none: every capped run ends there. Reading `reach_back` settles it, but the right answer may need a line, so it is the phase's | the work — phase 2 reads `reach_back` and either leaves it (a `round-N` over a `no fixes to check` is false and `checked_by` would refuse it) or guards it, and pins whichever in S10's fixture | *Leave the cell* where it reads `no fixes to check`; *overwrite* would claim round N+1 read fixes round N never wrote | leave the cell | ✅ the work, phase 2: **leave the cell**, the default, and it needed no line. `reach_back` already keeps a `no fixes to check` cell and prints `left … at no fixes to check`; `tests/test_a_fix_of_a_fix_is_counted.py`'s reframed-record case pins the cell and the line |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This frame has none**: the one decision the ticket
  left to a person was delegated to the orchestrator and decided before the
  frame was spawned, and everything after it the tree answered.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
