# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**The tree settled these judgments, which the tickets left open. Do not
reopen them here.** `spec.md` holds the grounds for each.

- **#774's fix records the newest reading's hash.** The ticket asked for *no
  record*; this item records the move `h2 → h1` instead, and records nothing
  only where the two hashes agree. Grounds: *a pact change is never lost*
  (`docs/the-evidence-ledger.md`), and `record_pact_changes`'s docstring, which
  records a revert.
- **#772 is fixed by ordering the one walk by dependency.** A kind order would
  miss the `0.10.0`/`0.9.0` case. A narrowed run names a citing row it cannot
  reach, by the narrowed-run principle in `docs/the-evidence-ledger.md`.
- **A citation re-stamp is not a pact change.** `family_view` keeps citations
  apart from code coordinates.
- **#775: `templates/config.md` points at the home rather than pasting
  round 3's text.** Grounds: the paste ratchet, and the one-home rule.
- **#775: the pact paragraph's `Enforced by:` line names the cases for the
  clause this item touched.** `skills/settle/SKILL.md` says the line *names
  what reads the rule*. Only codifying that for every future edit is left
  open (Q1).
- **#775: the 0.18.0:79 row gets a `Corrected ·` row, not a second
  `Re-read ·` row.** The claim's cited section states no Notes trace, and the
  in-place writer writes none. Only the exact wording is left to the work
  (Q3).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | When a work item edits a folded statement's rule, does it owe the statement's `Enforced by:` line the targets of what it added, as a written rule in `skills/settle/SKILL.md` §*A standing statement has one shape*? The tree cannot settle this because it is a rule for every future work item, not a reading of this one. `fold-check` reads only presence and resolution, so no check can make the choice. Round 3 of #771 sent it to the orchestrator for the same reason. | a person | (a) Write it as a rule: one sentence in the settle skill, and every later edit of a folded statement owes its line. (b) Leave it as each item's reading: this item applies it, and nothing obliges the next. | (b). This item updates the pact paragraph's line (D6) and writes no new rule sentence. | ⬜ |
| Q2 | Is the 0.18.1 trap the mechanism read here? `--reverify --checked` re-stamped about 13 rows in 4 fragments that `--strict` read OK. Reading points to `reverify` re-stamping an outranked family member while `--strict` grades the family OK. Reading cannot confirm that, because the trap's tree was rolled back and is gone. And if it is confirmed, is it this item's? | a measurement | Phase 2's probe, specified in `plan.md`. Confirmed: a different mechanism from #772, filed by the orchestrator as its own issue, with the probe's result as its coordinate. Not confirmed: the probe's output goes in `overview.md` §*Not done*, unexplained, and nothing else moves. | **Not folded in, whatever the probe shows.** Fixing it changes which rows the in-place writer touches and dates, so it needs its own frame. | ⬜ |
| Q3 | The exact claim of the `Corrected ·` row over `seal/releases/0.18.0.md:79`, and its coordinates. The tree cannot settle the wording ahead of time, because the coordinates must carry the hashes of the code as phases 1–2 leave it. | the work | Phase 3 re-reads `reverify_into`'s Notes cell, `reverify`'s date-only re-stamp, and `docs/the-evidence-ledger.md`'s *Without the row* paragraph, then states what holds. | A `Corrected ·` row whose claim is narrowed to: `--into` writes `Re-read <date>` in the Notes of each row it writes, and without the freeze the policy re-stamps a released row in place with a dated note, which the checker does not write. It cites those three coordinates. | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
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
