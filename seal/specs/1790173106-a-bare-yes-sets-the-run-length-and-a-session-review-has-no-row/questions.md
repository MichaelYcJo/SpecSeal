# a bare `yes` sets the run length, and a session review has no row — questions for the planner

<!-- seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered

Listed so nobody reopens them. The grounds are in `spec.md` §Scope and
`plan.md` §Alternatives; each is overturnable there, not here.

- **#138's three options → option 1**, refuse a bare `yes`, at the reader and
  at the writer, under `NEEDS_FROM`'s existing grandfathering. Grounds: the
  parser's own *one reader for both* design, the refusal already written for
  the row beside it, and zero committed records affected.
- **Whether a bare `yes` still stops the count** → no; it reads as `None`,
  the value an unreadable cell already has, because a cell the checker
  refuses must not be the thing that quiets a refusal.
- **Whether the refusal needs a new cutoff** → no; `NEEDS_FROM` grandfathers
  the row whole, and nothing at or after it carries a bare `yes`.
- **#241's proposed third `Review` answer → not added.** The chain's record
  is worth something because someone other than the author wrote it
  (`Fixes checked by` refuses the author; `Ran by` is the spawning session's
  row; contract §6). What a session's own check leaves that CI can read is
  the broad run, and `straight to the PR` has owed that record
  (`broad-gate.md`) since 0.12.0. The defect is seven documents saying the
  answer requires nothing.
- **The release-preparation commit** → stays a `[no-review]` commit, named
  as the routing question's `no work item` answer. #517's D1 decided the
  same for the fold, and the preparation commit is the same class.
- **Whether documentation-only changes get a lighter tier** → decided by
  #518 (no), not re-decided here.
- **Ship here or inside A** → here, alone. A inherits the five items listed
  in `plan.md` §Alternatives.

## Residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How many records refused by the new bare-`yes` arm exist at or after `NEEDS_FROM` — in `seal/specs/*/rounds/`, in the fixture corpora under `tests/`, and on the branches currently open against `release/v0.15.0`? The framer read 20 live records and the tests tree and found none; the tree could not answer for branches not yet merged | a measurement | 0 — no cutoff, ship as framed · more than 0 on a merged record — the ticket's grandfathering argument applies and the phase adds a cutoff in the shape of `REOPEN_FROM`, set to this work item's id · more than 0 only on an open branch — the branch repairs its cell, and the phase says so in its record | 0 | ✅ 0, measured 2026-09-23 by phase 1 (`phases/phase-1.md`): no cell reading `yes` alone in `seal/specs/*/rounds/*.md` or under `tests/`, no remote branch beyond `main` and the two release branches, no open pull request. Shipped as framed, no cutoff |
| Q2 | Where exactly the *why two answers and not three* paragraph lands in `docs/review-chain-spec.md` — beside the declaration table under §*Review arm*, or under §*Two records, and what each of them says* — and which existing ledger rows anchored on those headings drift as a result. The framer could not settle it because the answer depends on how the phase words the row, and `evidence-check` names the drift only once the edit exists | the work | beside the declaration table — the reader who meets *nothing required* is there; the other section is about what a record says, not what an answer owes | beside the declaration table | ✅ beside the declaration table, directly under it, by phase 3. One ledger row drifted as a result — the one anchored on the `### Review arm — opt-in` heading, which had already drifted once for phase 1's table row — and it was re-read twice with a dated note each time; the `## Two records` region is untouched |
| Q3 | Does `chain_check.py#runner_problem` accept `the session on <model>` as a `Ran by` value? Read: it splits on ` on ` and refuses only an empty half, so it should. Nothing this work item builds depends on the answer — it is here because #241's grounds say the row is *the spawning session's*, and a later reader asking whether the vocabulary already admits a session as its own reviewer deserves a measured answer rather than a read one | a measurement | accepted — the vocabulary admits it and only the chain's other rows (`Fixes checked by`) refuse the state; refused — nothing changes here either, and the grounds for *no third answer* gain one more row | accepted, read not executed | ✅ accepted, executed 2026-09-23 by phase 1: `runner_problem("the session on Python 3.12")` returns `None`, as does `the session on claude-example`; `the session` alone is refused for naming one thing. The vocabulary admits a session as the runner, and only the chain's other rows (`Fixes checked by`) refuse the state — as the frame read |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This batch has none**: both tickets' open judgments
  were answered by policy already in the tree, and the approval of `plan.md`
  is where a person overturns any of them.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
