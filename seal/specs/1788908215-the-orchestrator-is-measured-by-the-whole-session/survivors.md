# the orchestrator is measured by the whole session — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

Seven of the eight survivors this range reports are the same one fact in the
same three files, and it is deliberate. `spec.md`, `plan.md` and
`questions.md` are the **approved contract** for this work item: the owner
passed `plan.md` at the Design Gate on 2026-09-09, and its premise — *a
spawn's result arriving is the report* — is what building it measured false.

Editing that wording out of the contract is the one thing that must not
happen. It would leave the tree with no record that the plan said something
else, which is the whole point of `overview.md`'s divergence section and of
`questions.md` Q4. The corrected wording is in the code, the shipped skill and
the two fragments, where a reader acts on it; the contract keeps what it
said, and the divergence is recorded against it.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/plan.md` | `Cycle *N* runs **from the arrival of report *N-1* to the arrival of report *N***` | The approved plan's own definition, measured false while building it. Kept as written and recorded as a divergence in `overview.md`, with the three costed answers in `questions.md` Q4. Rewriting it would delete the evidence that the gate approved this premise |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/plan.md` | `The run's head (before report 1) and tail (after the last report) are their own rows.` | Same file, same reason. This half is also the one place the plan and `spec.md` disagreed BEFORE any measurement — `spec.md` §Scope and its acceptance row both bound the head by the first spawn, and that is what was built. `overview.md` carries both quotes |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/plan.md` | `Between report *N-1* and spawn *N* the orchestrator does two different acts` | The plan's own statement of what the boundary cannot separate. Two acts is now three — the waiting the measurement found sits in the same window — and `spawn_cycles`' corrected paragraph says so. Kept here because it is the approved contract, and because *the plan named two and building it found a third* is the finding rather than a typo to tidy |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/plan.md` | `so verifying report *N-1* is counted in the cycle after it` | The residual the plan states, and it is still true — only the name of the boundary changed. The corrected sentence in `spawn_cycles` says the same thing about the same window and adds the waiting the plan did not know was in it |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/spec.md` | `the closing work after the last report` | The approved scope statement. What it asks for is exactly what was built — a row for the work outside any cycle — and only the word for the boundary is superseded |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/spec.md` | `the calls before the first spawn and after the last report are each reported as their own row` | The acceptance row that decided the head's boundary, against `plan.md`'s parenthetical. It is the criterion the partition case asserts, so it is load-bearing as written rather than stale |
| `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md` | `Between taking report *N-1* and spawning *N*, the orchestrator verifies one report and frames the next prompt.` | The undecidable-from-a-transcript note, written before the first edit. Still true and now understated: the same window also holds the waiting. Q4, added to the same file by this range, is where the measurement and its consequence are stated |
| `CHANGELOG.md` | `Normalising at `parse_time` closes eight sites rather than the four the plan counted: six subtractions and two orderings.` | A **shipped** entry, and it was true at the release that shipped it. This branch added four orderings over `parse_time`'s output, so `seal/ledger.md`'s row — a present-tense claim about the code — is corrected to twelve, and the changelog is not: a released entry records what was true then, and rewriting one falsifies the history a reader dates their own numbers against. `CONTRIBUTING.md`'s merge-direction table exists for the same reason one release over |
| `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/changelog.md` | `Normalising at `parse_time` closes eight sites rather than the four the plan counted: six subtractions and two orderings.` | The fragment the shipped entry above was gathered from, for another work item, already released. Same grounds, and editing another work item's fragment would rewrite a second copy of the same history |
| `seal/specs/1788873630-the-orchestrator-sections-leave-the-reviewers-payload/overview.md` | `` `templates/sdd-phase.md` makes the value the spawning session's `` | **Another work item's open row, and it is true.** Round 1's fix pass closed THIS work item's `Ran by` row against `e389fc1`, and the sweep matched the shared phrase in a row about a different work item's five phase records. Those records were not opened here and their value was not verified, so closing that row would be the unproven closing `skills/implement/SKILL.md` §4 names — a check mark beside the original answerer. The claim itself is what `templates/sdd-phase.md` says, so there is nothing to correct: the row stays open with the orchestrator as its answerer |
| `skills/verify/scripts/session_cost.py` | `spawn spent are in the subagent's own transcript, so a per-cycle` | A false positive on the two-word phrase `the subagent's own`. The removed sentence said a spawn's interval is *a subagent thinking, already the whole of that subagent's own row*; this comment says a cycle carries no token column because the tokens live in the subagent's own transcript. Different claim, still true, and the range's own new row in the ledger fragment rests on it |
