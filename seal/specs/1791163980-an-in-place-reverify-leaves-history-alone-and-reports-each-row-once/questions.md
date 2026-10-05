# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**The tree settled these judgments, which the tickets left open. Do not
reopen them here.** `spec.md` and `plan.md`'s *Alternatives* table hold the
grounds for each.

- **#785 is judged once, before the first walk, with `family_view`'s own
  `held`.** A live judgment would depend on walk order, because a re-stamp's
  date can promote a reading to newest.
- **A superseded family is inside #785's class.** `docs/the-evidence-ledger.md`
  says its coordinates *are not checked again*, and `released_drift` already
  skips it.
- **A tie on the newest date counts as held.** Readings on one date are a
  union, which is the family paragraph's rule.
- **A *drifted* family keeps today's re-stamp of every member whose hash
  moves.** The `--into` paragraph tells the reader to read every row citing a
  drifted coordinate, and #785 asks only for a family that already holds.
- **The `left` lines print once the walks end, outside `told`.** A `left`
  claims no write. The fold that decides them is `walked_move`'s, the same
  one MOVES uses.
- **#792's remedy is chosen per coordinate, by reason, not by whether
  `--ledger` was passed.** A `--ledger` naming every file is narrowed and
  still writes everything.
- **#781: the document changes and the writer does not.** The owner decided
  this on 2026-10-05, in the routing batch.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The exact words of D3's (ii) clause and of D4's corrected sentence. The tree cannot fix the wording ahead of time. The new text must share no 15-word run with another file (`tests/test_no_passage_is_pasted_into_a_second_file.py`), must fit the 88-column wrap, and must keep `test_the_ledger_rules_have_one_home`'s needle *Without the row, a released row is kept true where it stands.* intact. Only drafting against those checks settles it. | the work | Phase 2 drafts the clause and phase 3 drafts the sentence, each run against the three checks before its pin is written. | (ii): `— still DRIFTED: this run left <coordinates> where they stand; the line naming each says why`. D4: *re-stamps a re-read row in place, adding the date of the reading to its `Checked` cell*. | ⬜ |
| Q2 | Which released rows this item's edits drift, and which of their claims the edits make false. The tree cannot know before the edits exist. A claim about `reverify`'s printing or about the *Without the row* sentence may be among them, beside `seal/releases/0.18.2.md:91`, which the frame already found. | a measurement | `bin/evidence-check .` after phase 2 and again after phase 3's doc edit, then each named row read against the diff. | `Re-read ·` rows through `--into` for each claim that holds. A `Corrected ·` row for 0.18.2:91 and for each other claim found false. Each row's verdict goes in `phases/phase-3.md`. | ⬜ |
| Q3 | Can an owed family reach `main`'s `LEFT` line with neither reason (i) nor (ii)? Reading found no such path: after an unnarrowed in-place walk, every drifted member is re-stamped and dated, so it holds unless the walk left it. But `reading_date`'s ordering of a calendar-invalid date, and a member in a file reached only through a citation, were not traced. | a measurement | Phase 2 builds those two shapes in a scratch repository (§7) and records whether `owed` is non-empty with neither reason. | The line names the coordinates, says they are still DRIFTED, and names no remedy. A shape found is recorded in `phases/phase-2.md` and becomes a case. | ⬜ |

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
