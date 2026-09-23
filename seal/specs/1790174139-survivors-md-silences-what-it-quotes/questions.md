# 1790174139-survivors-md-silences-what-it-quotes — questions for the planner

<!-- seal/specs/1790174139-survivors-md-silences-what-it-quotes/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered

Listed so nobody reopens them; the grounds are in `spec.md` §*Judgments the
tree answered*, one number each.

1. #308 and #507 are the two halves of one defect and land in one phase (1).
2. The exemption file leaves the sweep on both sides, and the `seal/follow-up.md`
   row's argument against it does not hold — exclusion is per path (2).
3. A phase record is excluded whole, not by a correction marker (3), and being
   edited while the work item is live does not keep it in (4).
4. A deeper exemption file is owned by the `seal/specs/<id>` prefix at any
   depth and then asked the ownership question; it is neither refused with a
   new state nor kept at the old reach (5).
5. #366 is a different subject; its default home is work item A (6).
6. #371 needs nothing in the tree — it was closed with no change, and #507 is
   the same defect, open (7).

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Where does #366 land? It is in this milestone step's ticket list, and it is not about the survivor sweep: its module is `tests/test_a_release_is_sized_by_a_criterion.py`, and its open question is `round_record.py#depth_two`'s handling of a finding whose `Location` spans two depths — a file work item A owns. **Does not block this build**; the four phases above are the same whichever answer comes | a person — the repository owner | **A** — the depth question is decided where `round_record.py` is already being changed, and the two drafted cases pinning `STATES_A_SIZE` and `SCANNED` ride that branch as a test-only change · **here** — a fifth phase touching `round_record.py` while A builds against it, and a pull request about two subjects · **its own item** — the two cases are below the SDD ladder's top rung on their own, so it would be a closing memo and no frame | A | ⬜ |
| Q2 | After phase 1, how many of the 36 path rows across the three pull requests' `survivors.md` files still match a reported survivor, and how many are dead — quote no longer contiguous in the standing text, or the place no longer carrying the removed wording? #308's own *Not verified* row asks this. A dead row silences nothing by design and is not edited; the count says whether any should be re-judged rather than carried to the release | a measurement — the S5 runs of phase 1, counting `exempt` lines against rows | the count goes into `phases/phase-1.md` and `overview.md`; no row is edited | ✅ measured 2026-09-24 at `af5c4044` and again at `e88cdebc`: #525 **14 of 29** consulted, #528 **0 of 4**, #527 **0 of 3** — 14 consulted, 22 dead, none edited. #528's and #527's rows match nothing over the squash range at any floor down to 1.0. `phases/phase-1.md` |
| Q3 | After phase 1, does any survivor of the three pull requests still vanish through a live file the range wrote — `overview.md`, `changelog.md`, the ledger fragment — quoting the old wording? The instrument: in a scratch clone, blank those files' quoting sentences in a probe commit and compare the report without `--exempt` against the unblanked tip. If a survivor appears only when they are blanked, that is the out-of-scope class `spec.md` §*Out* names, and the count goes to `overview.md` §*Not done* with the repository owner named | a measurement — one probe in phase 1, driven from Python, deleted after | assume none; record the count either way | ✅ measured 2026-09-24, in-process rather than by a probe commit (a blanking commit inside the range makes the blanked sentences removed wording, so it measures a different range; `overview.md` §*diverged*): #525 **five** places appear only when its `overview.md`, `changelog.md` and ledger fragment also leave the sweep, listed in `overview.md` §*Not done* for the repository owner; #528 and #527 none. `phases/phase-1.md`, re-checked in `phases/phase-2.md` |
| Q4 | The predicate's name, and whether the class is one function or `records_a_past_round` plus a wider one that calls it. `records_a_past_round` is anchored by ledger row S6 of `1788873640` and its body need not change; the test's `PREDICATE` constant follows whatever `corrected` and `corpus` call | the work — phase 1 decides it and `phases/phase-1.md` records it | one wider predicate that calls `records_a_past_round`, so the anchored function is untouched | ✅ decided 2026-09-24 by phase 1: `records_a_past_state`, one function that calls `records_a_past_round` and adds the two new members; `corrected` and `corpus` call it, `PREDICATE` follows, and S6 of `1788873640` still anchors on the untouched function. `phases/phase-1.md` |
| Q5 | Phase 2 stops the sweep reading phase records, and with that it stops catching the shape #423's pass found in `phase-4.md` — a correction inside an HTML comment while the false claim rendered in bold. Nothing else checks that shape. Is a marker-shape checker worth building? **Does not block this build**; the row exists so the loss is somebody's rather than nobody's | a person — the repository owner, through the `seal/follow-up.md` row phase 2 writes | **a checker** — a new gate, its own work item, carrying `CONTRIBUTING.md`'s four requirements · **no checker** — the shape is caught by a reviewer reading the record, which is what caught it in #423 | no checker; the follow-up row stands until the owner closes it | ⬜ |

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
