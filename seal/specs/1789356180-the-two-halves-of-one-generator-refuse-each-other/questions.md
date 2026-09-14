# the two halves of one generator refuse each other — questions for the planner

<!-- seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What is a verdict row that commissions nothing — a row with no finding id, a numbered row the generator leaves alone, or neither? | **a person** | **(a) `close` accepts a row with no id** and never asks a fix table for it. This is #321's answer 2, and its comment of 2026-09-14 is the argument: when the unnumbered rows outnumber the findings, renumbering makes a six-finding round read as a twelve-row one, and (a) is the only answer of the three that leaves the count honest. It also generalises — an earlier round's closure (#341) and a `❓ out of verified scope` marker (#353) are both rows no fix table can reference — so one mechanism closes three tickets. What it costs is stated in `plan.md` §*Technical context*: a reviewer who forgets an id on a row that IS a finding has written a finding nobody will be asked to close. **(b) `new` validates what `close` will refuse**, #321's answer 1: every row keeps a number, the refusal moves to where the author is, and the count still inflates. #341 and #353 need their own mechanisms. **(c) documents only**, #321's answer 3: it cannot reach a report already written, and the tree holds 54 records whose `#` cell carries no digit | **(a)** — answered by the repository owner on 2026-09-14, in one batch with Q2, Q3 and Q4, confirming the default: `close` accepts an id-less row and requires no fix-table row for it, with `new` validating the ids that ARE written. **(a), with (b) kept for the rows that do carry an id.** They compose — a row with no id is admitted, and a row with a malformed one is still refused, now at `new` as well as at `close`. Only (c)-alone is excluded | ✅ |
| Q2 | Is the SHA in `answered — corrected at <sha>` meant to be machine-readable? | **a person** | **(a) No — `docs/review-chain-spec.md` is corrected** to the spelling `agents/smith.md:156` already carries: `answered`, with `corrected at <sha>` in the grounds cell. Three records in this release already write it that way. `tests/test_the_rules_have_one_owner.py#test_a_correction_row_closes_answered_and_never_fixed` asserts both sentences today and is rewritten to assert one. Nothing in the tree loses a reader: `chain_check.py:2426` skips every row whose verdict is not a fix word before it looks for a commit. **(b) Yes — `fix_table` learns the suffix**, validates the SHA the way it validates a `fixed` commit, and the verdict column gains a fourth shape. This is the answer if a later check is meant to find the correcting commit from the cell. It is the larger change and it makes the verdict cell a place where two kinds of thing are parsed | **(a)** — answered by the repository owner on 2026-09-14, confirming the default: the spec is corrected to `answered` with the correcting commit in the Grounds cell. **(a).** The grounds cell is free text and the verdict cell is vocabulary, and nothing reads a SHA out of an `answered` cell today. Choosing (b) means naming the check that will read it | ✅ |
| Q3 | #323's answer 1 shipped at `c84f259` as `round_record.py#seal`, and its answer 3 shipped with it in `skills/code-review/orchestration.md`. Does the ticket close as covered, or does its residue land here? | **a person** | **(a) Close it as covered**, with the grounds in the pull request body: the refusal text the ticket quotes returns nothing from the tree, the sealer is the documented route, and the one arm still naming `close --broad-gate` describes the gate-then-close order, which is runnable. **(b) Keep it and run phase 5**, which rewords that second arm and pins the wording. One commit, one case, and it is the ticket's answer 2 | **(a)** — answered by the repository owner on 2026-09-14, confirming the default. **Closed as covered on the same day**, with the grounds in a comment on the ticket: `seal` at `c84f259`, `git tag --contains` putting it in v0.10.0, the quoted refusal text returning nothing from any shipped file, and the sealer executed twice in this release. Phase 5 does not run. **(a).** A ticket whose defect the tree no longer holds is closed on the tracker rather than carried as a phase | ✅ |
| Q4 | Six tickets is the largest set this release carries, and `docs/issues-and-milestones.md` sizes a release by what has to be in effect before the next work item starts. Does #273 part 1 — the stale `Fixes checked by` reason — have to be in effect now? | **a person** | **(a) It ships here**, as phase 4. The argument for now: it is one function away from phases 1 and 3, all three are `close`'s write pass, and a capped run's last record keeps a false reason permanently because there is no next `new` to correct it. **(b) It moves to 0.11.5**, where #344 (*a record says something the tree does not*) and #342 (*a record states the previous round's findings as open*) are already open and are the same family. The argument for moving it: `round_record.py#landing_values`'s docstring states the current behaviour as deliberate — *the cell stays at the landing value for `new` of the next round to set* — so this is a design reversal rather than a defect repair, and it is the one item of the six that touches `chain_check`'s fix-surface arm, a second gate. Nothing in phases 1 to 3 waits on it | **(a)** — answered by the repository owner on 2026-09-14, confirming the default: it lands here, as phase 4. **(a), as phase 4.** The next work item reads round records, and a permanently false cell on a capped run's last record is read by whoever opens it. But this is the one row of the six where the case for moving is real, which is why it is asked rather than assumed | ✅ |
| Q5 | Does changing the reason `close` writes into `Fixes checked by` turn any arm of `chain_check` red? The arm at issue refuses `none — the fixes are not yet written` in the surface row beside a `Fixes checked by` naming a later round, and it reads the reason text rather than the row alone | **a measurement** | One fixture record and two runs of `chain_check`, before and after the phase-4 edit, both arms. Asking a person is the wrong instrument — the answer is in the output of a command that takes seconds | The phase that builds it runs the measurement before writing the reason text, and records the result in `phases/phase-4.md` | ⬜ |
| Q6 | The tree holds 66 verdict rows whose Grounds cell is its home repeated and nothing else, and 103 carrying an empty code span beside a fix commit. Does the phase-3 repair carry a migration arm over them? | **the work** | `spec.md` §Scope argues no: a round record asserts a past state, which is the property that lets it live beside the contract, and a row rewritten now would assert a state that was not true at its own `Target SHA`. What the phase has to settle is the narrower thing the counts cannot say — whether any of those 66 rows lost prose a reader still needs, which is one open of the fixes file beside each. Unknowable at framing time; the phase that opens `close`'s write pass is where it is cheap | **No migration arm.** The phase records a divergence row if what it finds overturns that | ⬜ |

**`Who can answer` takes one of three values and nothing else**, and all three
are used above. Q1 to Q4 are a person's and block the build. Q5 is a
measurement and must not be queued behind a person — the answer arrives faster
than the reply would. Q6 is the work's, and it does not travel back to the
framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

**What was not made a question, and why.** Four things that would have been
rows had reading not settled them, recorded here so nobody re-opens them:

- **How many records the corpus holds in the shapes this work admits** — read,
  not asked: 1,992 verdict rows committed, 253 refused by the id rule, 199 of
  those round-prefixed, **54** carrying no digit at all, and **21** bare `—`
  cells in reviewers' reports.
- **Whether any verdict word other than `deferred` reduces its cell** — read,
  not asked: `answered` discards the reviewer's grounds too, and `fixed` is the
  only one of the three that preserves what stood. #391 raised this as an item
  for whoever builds it; it is answered in `spec.md` §5 and is in scope.
- **Whether a document tells a reviewer to write `already deferred` in a
  verdict cell** — read, not asked: no. `agents/warden.md:235` says it about
  the **Deferred** table, and the two records that met it already wrote
  `deferred <home>` in the verdict cell with `already deferred` as grounds.
- **Whether a round-prefixed id should be admitted** — settled by policy, not
  asked: `docs/review-chain-spec.md` §*The finding id* measured the corpus both
  ways and the rule takes away two wrong answers and no right one. #341's own
  body agrees.

Answered rows feed back into `docs/` — `docs/review-chain-spec.md` for Q1 and
Q2 — before this directory's work merges.
