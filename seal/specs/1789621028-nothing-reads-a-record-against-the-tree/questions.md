# nothing reads a record against the tree — questions for the planner

<!-- seal/specs/1789621028-nothing-reads-a-record-against-the-tree/questions.md — decisions
only a human can make, extracted so nothing ships on a silent assumption.
Before adding a row, check the inheritance rule: if policy is silent but
existing behavior answers it, inherit and record — only genuinely NEW rules
belong here. -->

## What the tickets left open and the tree answered

A reader cannot tell a judgment that was decided from a question nobody met.
These four were open in the tickets, were decided from the tree during the
framing, and the grounds are in `spec.md` §*The shape #344 left open, decided
from the tree* and in `plan.md`'s Alternatives table. **Reopen one by opening
what it was decided against, not by asking again.**

1. **Which of #344's three shapes the work takes.** Decided: *a rule that a
   range is pinned when it is written*, plus a reader in `chain_check` for the
   one other thing a checker can see. The second option — a checker that
   re-reads records — turned out to be half built already, in
   `evidence_check`'s records arm from #190, and to be at its own limit,
   because that checker calls git for nothing and a range is a claim about
   commits.
2. **Whether the rule can be enforced on the fixes file's prose header.**
   Decided: no. 39 fix-table files, 11 of which state a range in their first
   eight lines, in eleven different spellings, two naming `HEAD`. There is no
   convention there to enforce.
3. **Whether the two #427 halves are one fix.** Decided: no — the write half
   and the read half are two phases, because the ticket says a repair that
   stops the second write and leaves the standing duplicates unreadable has
   closed the instance and not the class.
4. **Whether any `seal/follow-up.md` row was waiting on this work.** Decided:
   none of the eleven. The two nearest, rows 1 and 9, are about the **ledger's**
   anchors and about `evidence_check`; this work item changes neither. No row
   is deleted.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should a round record's `Location` cell become a content anchor — #344's first option, which this frame refuses? | a person | **Migrate**: 223 committed records and ~90 work items re-anchored, largely by people who did not write them; `templates/sdd-round.md:293` stops prescribing `path:line`; `tests/test_a_record_states_what_the_tree_has.py:508`, which exists to keep the records arm from reading that cell as a coordinate, is rewritten. **Leave**: a `Location` stays a position and keeps rotting — #344's own bullets 1 and 4 point at lines that no longer hold what they name, which is the cost stated at its worst | **Leave**, and open it as its own work item if the owner wants it. This does not block: the branch builds the pinning rule and the reader either way, and neither conflicts with a later migration | ⬜ |
| Q2 | #344's fifth bullet — *a verdict attributes a fix to a commit that carries half of it, and whose other half was reverted as broken in the next commit* — names **no coordinate at all**. Which verdict row is it? | a measurement | Walk every `fixed` row of `1789034970-…`'s three round records, resolve the commit each names, and read the commit after it for a revert. One command and a read; the answer is a row number or the finding that no row matches | Phase 5's first act. If no row matches, the bullet is recorded as unreproducible against the tree at this date rather than guessed at | ⬜ |
| Q3 | `survivors.md:5` of `1789034970-…` says `survivor-check --range origin/release/v0.10.0...HEAD` reports sixteen places, and #344 says a re-run gives three. What does it say today, and does that range still resolve? | a measurement | Re-run the command at the branch tip. Three outcomes: the range resolves and the count differs, so the row is corrected to a pinned range and the number it was measured at; the range resolves and sixteen still holds, so #344's bullet is recorded as false today; the range no longer resolves, which is the same defect one level up and is what the row then says | Phase 5. **Do not write a number the run did not print** — the whole class here is a record asserting what nobody measured | ⬜ |
| Q4 | Where exactly does the new refusal sit inside `close`, and does it refuse or overwrite the doubled `Grounds` cell? | the work | The round that raised #427 left a paste-ready guard that **refuses**, and says it is unmeasured. #427 itself allows either — *a guard in `close` that refuses, or overwrites*. Refusing tells the author the record is half-restored; overwriting silently discards the reviewer's grounds, which is the thing `close` was written not to do | **Refuse**, ahead of the write, so nothing reaches disk. Phase 2 measures it and records what it found; if refusing turns out to block the documented way out of a record written wrong, the phase says so and overwrites instead | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build. **One row here,
  Q1, and its default is the one the branch builds**, so this run does not
  wait on it.
- **a measurement** — a probe, a command or a count settles it. Q2 and Q3.
  Neither goes to a person: an opinion is the wrong instrument for both, and
  the answer arrives faster than a reply would.
- **the work** — unknowable at framing time. Q4. The phase that meets it
  decides it there and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
