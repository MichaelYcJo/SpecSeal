- **A round record no longer has to number the rows it verified (issues #321,
  #341, #353).** A reviewer who confirmed six things and opened one had to put
  a finding number on all seven, because the generator refused any `#` cell
  that was not digits. The record then read back as a seven-finding round, and
  the count is what the next round and the pull request go by. Worse, each of
  those six had to be given a closing word by the fix pass — so the record
  ended up asserting that the round had settled things it had merely looked at.

  **A cell that says the row commissions nothing is now admitted.** It is
  copied into the record exactly as written, never keyed to a finding, never
  asked for a closure, and never counted toward `Pass`. Three kinds of row are
  that shape and all three were being renumbered by hand: a confirmation the
  round verified, an earlier round's closure carried forward, and a
  `❓ out of verified scope` marker.

  **A 🔴 or a 🟡 with no number is refused, and so is an empty cell.** Those two
  severities mean somebody owes the row an answer, so such a row is not one
  that commissions nothing whatever its `#` cell says — and because an admitted
  row is never counted toward `Pass`, the record would otherwise be written
  with `Pass` ticked beside an open finding in its own verdict table. Of the 51
  no-digit cells in the committed records, 44 are a severity marker and a single
  letter — a finding id in the wrong alphabet — and all 26 carrying 🔴 or 🟡 are
  genuine findings.

  **A cell that carries digits and is still not an id is refused as before**,
  because it was reaching for a number and missed. What changed is where and
  how loudly: the refusal now lands at `round-record new`, where the reviewer
  who chose the numbering is, instead of two commands later at the
  orchestrator — and it names every offending row of the table rather than the
  first, which used to cost two round trips per repair.

  **Which way this fails is written down where the reviewer picks the number.**
  Writing 🟢, ❓ or ⬜ with no number on a row that really is an open finding
  still writes a finding no fix table will be asked to close, and nothing
  catches that — the check reaches the two markers that owe an answer and
  cannot reach a wrongly chosen one. Numbering a confirmation row costs an
  inflated count in one record. The change is toward the cheaper mistake, and
  the documents now say so.

- **`❓ out of verified scope` is a verdict that closes without commissioning
  anything (issue #353).** It means the reviewer looked and could not judge,
  because judging was outside the round's scope — there is no defect, and none
  of the three words a fix pass may write is true of it. The generator counted
  it as an open finding, refused to run until the fix table carried a row for
  it, and then wrote that row's word over the marker. Measured twice inside one
  run: the record claimed the round had settled the one check neither round
  ran, the next round found exactly that, and it could only close its own copy
  by replacing the marker a second time in a different word.

  A severity marker now leads a verdict cell without being part of it, the same
  rule the `#` cell has always used. Over all 1,989 committed verdict rows that
  changes the reading of exactly one cell, and that cell is this one.

- **Two documents prescribed a verdict spelling the generator refuses (issues
  #341, #321, #273).** `docs/review-chain-spec.md` told a fix pass to close a
  correction as `answered — corrected at <sha>` in a single cell, and
  `agents/smith.md` told it to put the word in the Verdict cell and the commit
  in the Grounds beside it. Only the second works. So the repository shipped
  both readings, a test asserted both sentences — which pinned the
  disagreement rather than catching it — and anyone who followed the owner met
  a refusal listing three words, one of which their cell had begun with.

  The owner is corrected to the spelling that works, one string is now asserted
  in both files, and the refusal names the two-cell shape and prints the row to
  write. `deferred <home>` is unchanged: the home is what makes a deferral
  readable, so it is the one word that carries its own suffix.

  **A repair made outside the tree gets a spelling too.** Answering a finding by
  editing a ticket or a pull request body produces no commit in the branch, and
  a commit somebody can open is the whole of what `fixed` asserts — so the word
  was unusable and nothing said what to write instead. It closes `answered`,
  with where the repair is in the grounds.

  **`already deferred` is grounds, never a verdict.** No document ever told a
  reviewer to put the phrase in a Verdict cell, and none said which cell it was
  not for either — while a cell holding it reads as still open, which reopens
  the finding and invites a fix row that overwrites the reviewer's verdict.

- **A fix pass no longer overwrites the reviewer's own reasoning (issue #391).**
  The Grounds cell holds why a finding was opened, and a fix pass is asked what
  it did about the finding — two sentences by two authors. `fixed` kept both.
  `answered` and `deferred` replaced the reviewer's with their own, so the
  original survived exactly one of the three words.

  **A deferred row lost the most and had the most to lose.** Its grounds were
  reduced to the issue number alone, discarding why the finding could not be
  closed on the branch and what a reader should open — and a deferred finding
  is the one verdict whose reasoning is the whole of its value, because nothing
  else in the tree will explain why it left. Measured over the committed
  records: 66 rows read as nothing but their own home, and for 51 of them the
  discarded prose is not recoverable from anything in the repository.

  **The empty code span beside a fix commit is gone.** The commit was cut out of
  the middle of its own code span and both backticks were left standing, so a
  cell landed as `fixed at e7d3447 — `` — widened`. It appears on 210 committed
  verdict rows. The cut now takes the span, so a second code span in the same
  cell survives untouched.

- **A closed record no longer says its fixes are not yet written beside the
  commits that wrote them (issue #273).** `Fixes checked by` starts at
  `nobody — the fixes are not yet written`, which is true while a round runs.
  The fix pass then writes those commits into the record's own verdict cells
  and the row was left alone, so the record contradicted itself two rows apart.
  On a run that ends at the round cap it stayed that way permanently, because
  no later round exists to correct it.

  `nobody` is kept — a checker has to be a later round, and at that moment none
  exists — and only the reason is replaced. A cell that already names a round
  is a later round's reading and is not touched.
