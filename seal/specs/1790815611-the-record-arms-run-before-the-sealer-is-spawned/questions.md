# the record arms run before the sealer is spawned — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Answered before the first edit

**#638's one open question is answered by the repository owner, 2026-10-01**,
in the routing batch for release 0.17.0: `templates/config.md`'s example
`Broad gate` row changes to the lint-first order, `uvx ruff check . && uvx
ruff format --check . && bin/test -q`, the same order this repository's own row
took in #634 (`7a39f2f7`). It is in scope (`spec.md` S9) and nobody reopens it.

## Judgments the tree answered

Each of these the ticket left open or did not state, and the tree settled.
The grounds are in `spec.md` §Scope or `plan.md` §*Alternatives considered*;
this list exists so a reader can tell a question that was decided from one
that was never met.

1. **Who runs the preflight — the orchestrator, before the spawn.** Not the
   sealer: its definition is four acts and one write, the one test that counts
   definitions assigning the gate keys on that file alone, and a refusal found
   inside the sealer still returns to the orchestrator one spawn later
   (plan.md, alternative C). Not a new agent either: contract §6 withholds a
   spawn from every agent, and the orchestrator already runs the same scripts
   in every round.
2. **It is a flag, not a command.** `bin/broad-gate` and its `.cmd` twin pass
   arguments through, and the tree-copy redirect hands an unknown flag to the
   tree's gate (plan.md, alternative D).
3. **It adds no arm and names no second list.** The branch skips the
   `checks[SUITE]` assignment by condition; `PARTITION`, `SKIPPED_AT_MAIN` and
   the three AST-reading cases are untouched (spec.md S5).
4. **The row's refusals still apply, and the row is not run.** A row refusal
   is the cheapest the sealer gives and costs a spawn when it arrives there;
   applying it in the preflight costs nothing (spec.md S6).
5. **`--preflight --record` is a refusal.** A preflight that accepted
   `--record` would either write the cell, which the ticket forbids, or ignore
   the flag, which is a flag that does nothing (spec.md S4).
6. **The output carries no `SEALED` or `NOT SEALED` line.** A preflight that
   printed either would be read as a seal by the sealer's own tests and by a
   person (spec.md §*Data & interfaces*).
7. **The coverage line is not printed in a preflight.** It says what *this
   seal* answers, and a preflight seals nothing. The moved-base, running-copy
   and skipped-at-main lines are, because they are facts about the run.
8. **`agents/sealer.md`, `docs/the-broad-gate.md`, both READMEs, `hooks/`,
   `hygiene.yml` are out of scope**, each with its reason in `spec.md` §Scope.
9. **A dry run of `seal`'s record refusals is not built.** The ticket scopes
   the preflight to arms 2–7; #456's unchecked-`Pass` instance therefore still
   reaches the sealer. Named for the owner in the report as a possible
   follow-up, not as a row here, because the ticket already answered the
   scope (plan.md, alternative E).
10. **The orchestration edit is a paragraph, not a heading**, so the acts
    table needs no new row; its existing `Grounds` cell for that section names
    the preflight (spec.md S8).
11. **The `templates/config.md` sentence that lists four of the six arms by
    hand is corrected while it is being edited**, to point at
    `broad_gate.py`'s docstring rather than carry a list that has been short
    since #468.

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which record shape reproduces #535's `chain` exit 1 over `fixed at` in a verifying round under the draft payload? The tree names one candidate — `chain_check.py#closed_with_a_fix`, a `fixed at` verdict beside `Fixes checked by: no fixes to check`, which is not gated on `strict` — and the ticket's wording leaves the exact shape to whoever builds the fixture | the work (phase 2) | (a) `closed_with_a_fix`, built with `generate` and a verdict row reading `fixed at <sha>` on round 2, then `Fixes checked by` set to `no fixes to check` · (b) another ungated refusal `chain_check` raises over a `fixed at` verdict — the phase names which and why. Either way the case is seen red first and the row is shown not to have run | (a) | ⬜ |
| Q2 | What does a preflight cost in wall clock, on the fixture and on this repository? The ticket's bound is under 10 s for the fixture. A timing assertion in a case flakes on a loaded runner, so the bound is measured rather than pinned | a measurement (phase 2, written to `phases/phase-2.md` and `overview.md`) | the number, once, with the machine and the moment. If this repository's own preflight is over 10 s, that is a finding about an arm (which one, and why) and goes to `overview.md` §*Not verified* with the owner named, not a reason to drop the bound | measure and record; no case asserts a time | ⬜ |
| Q3 | Over the next release, how many `NOT SEALED` runs had only a record arm (2–7) failing? The ticket's target is 0; it was 1 of 6 in 0.15.0 and 1 of 2 in 0.15.3. This work cannot answer it, because the runs it counts have not happened | a measurement (the flow-log sweep that follows 0.17.0, by whoever runs it — the owner's sweep, per #51) | the count, read from the 0.17.0 flow logs, posted where the sweep posts | nothing to assume; the preflight ships either way | ⬜ |
| Q4 | How is the preflight verdict rendered — a `head` keyword on `seal_stamp.not_sealed` with the old first line as its default, or a form built in `broad_gate.py` from `failure_lines`? Both keep the two existing `not_sealed` cases green and both satisfy S1 and S3; the choice is about where the first line lives | the work (phase 1) | (a) a keyword on `not_sealed`: one renderer, one place the failure words live · (b) a form in `broad_gate.py`: `seal_stamp.py` untouched. The phase picks and says why in `phases/phase-1.md` | (a) | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This work item has none**: the one such question
  #638 carried was answered in the routing batch, above.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
