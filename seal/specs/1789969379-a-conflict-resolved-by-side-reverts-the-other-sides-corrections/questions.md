# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — questions for the planner

<!-- Decisions only a human can make, extracted so nothing ships on a silent
assumption. Rows whose answer the tree already gives are NOT here; the ones
the framing settled from the tree are listed under the table so nobody
reopens them. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The rider at `evidence_check.py#reverify` asks whether `--reverify` should refuse a row whose `Checked` predates the hash it is about to replace, or print the ones it left. #424's second direction lands on the same surface. Is it answered here? | a person | **(a)** leave it — this work adds a check beside `--reverify` and touches neither the column nor the command; the rider stands. **(b)** answer it here — `--reverify` gains a reader for `Checked`, which is mechanism the rider says its finder could not add, and this work grows a second subject. **(c)** answer it as its own work item, with the rider's own measurement (#120 round 1, six rows) as the frame | **(a)**. The rider records that adding either answer is adding mechanism, and this work already adds a check, a wrapper, a CI leg and two document sentences. `spec.md` §Out names it | ⬜ |
| Q2 | Does the new CI leg block a pull request into `release/*`, or report? | a person | **block** — a lost correction stops the merge, which is what a gate is for, and the cost is a false refusal stopping somebody. **report** — it prints and exits 0, which nobody is obliged to read, and `CLAUDE.md` §*The goal a design is chosen against* is about exactly this being the cheaper-looking and weaker answer | **block**. Every other arm of the hygiene workflow blocks, a lost correction is silent by construction, and A3 exists so the check does not fire on correct work. If A3 cannot be met, this answer changes with it | ⬜ |
| M1 | How many merges of `seal/ledger.md` exist in this repository's reachable history, and how many of them dropped a marker? | a measurement | A count over `git log --merges` and the two markers. If the answer is zero the check ships with no historical instance and A1's fixture is its only evidence; if it is more than one, the ticket's incident is not the only one and the numbers belong in the closing memo | **Measured in phase 1: 37 merge commits reachable from every ref, 24 with a parent carrying a ledger with markers; the spec's rule reports 1 merge and 5 markers, all one deliberate re-anchoring rewrite, and the shipped rule reports 0.** `overview.md` §*What the measurements answered* carries it, and it is what added the merge-base test | ✅ |
| M2 | Does the check's range form survive the squash — that is, are the merge commits still reachable at the pull request, where the leg runs? | a measurement | `origin/<base>...HEAD` on a pre-squash branch. `spec.md` §*What this repair cannot see* claims they are reachable only before the squash; the leg's placement rests on it | **Measured in phase 4: yes.** The branch's own merge is reachable from the merge ref a `pull_request` job checks out, and gone after the squash — two cases in `tests/test_a_merge_cannot_silently_drop_a_correction.py` read the check's answer at each. The leg did not move | ✅ |
| W1 | Which exit code and which output shape — one line per lost marker, or a grouped report per merge commit? | the work | The sibling checks in `skills/` differ, and matching the nearest one is worth more than choosing freshly | **Followed.** Exit 0 / 1 / 2 as the sibling has them, one entry per loss with the standing text quoted, and a closing line saying what to do. What differs is the empty case: this one says it examined no merges, because a range with no merge in it is the common case here and the sibling has no equivalent | ✅ |

**What the framing settled from the tree, so nobody reopens it.**

- **`Checked` is read by no machine.** `grep -n "Checked"` over
  `evidence_check.py` returns two lines and both are the rider's comment. The
  ticket's *a column a machine already reads* is wrong, and `spec.md` says so
  in a section of its own.
- **Both markers count, not only `Corrected`.** Measured: 10 `Corrected`
  against 189 `Re-read` across the shared file and the one live fragment. A
  check watching the rare one would have ignored every row the previous work
  item re-read.
- **Markers are matched on the leading verb and date.** At least three
  spellings of `Corrected <date>` exist, and the sentence after the date is
  prose somebody will reword.

  **CORRECTED at round 1, finding 1.** The variation is not only after the
  date. 39 of the 404 markers `seal/ledger.md` carried when round 1 measured
  it put a qualifier between the verb and the date — `again` 19 times and
  nine other spellings — and one row carries no other. A marker is matched on
  the verb and the date, with any short run of lowercase words between them
  read as part of it.

  <!-- CORRECTED 2026-09-22 by work item 1789996780 (#470). What stood here:
  "39 of seal/ledger.md's 404 markers". The count is right for the moment it
  was taken and the sentence did not say there was one: a8bf2a86 folded three
  ledger fragments into that file and this branch wrote a marker into it, so
  a bare present-tense figure over that corpus goes stale at every release.
  The moment is named now. Corrected in place with the issue named, never
  deleted silently: a record of a past state that quietly becomes true is a
  record nobody can audit. -->

- **Fragments are watched from the start**, because `fold_ledger.py` moves
  them into the shared file at the release and a check watching one file goes
  blind there.
- **Row survival is what separates a loss from a `REMOVED` row**, which is
  `CLAUDE.md`'s own rule rather than a judgment this work makes.
- **The protected act stays a person's.** Reading both sides of a hunk cannot
  be automated, so every candidate was weighed on whether it tells a person
  they lost something, not on whether it prevents the loss.
