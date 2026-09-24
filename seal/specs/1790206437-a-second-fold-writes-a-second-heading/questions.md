# 1790206437-a-second-fold-writes-a-second-heading — questions for the planner

<!-- seal/specs/1790206437-a-second-fold-writes-a-second-heading/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered

Listed so nobody reopens them; the grounds are in `spec.md` §*Judgments the
tree answered*, one number each.

1. #540's claim that nobody has run the fold twice on this tree is false:
   `seal/ledger.md` heads `0.9.3` twice, written by `4ac9bf35` thirty-one
   minutes after the 0.9.3 preparation commit `bee7ae99` (1).
2. A second fold joins the section and keeps its date; it is not refused (2).
3. The doubled-heading refusal lives in `fold_ledger.py --check` AND as a
   real-tree case in `tests/test_release_hygiene.py` (3).
4. The `0.9.3` repair is the deletion of the second heading line and its
   blank; the sections are adjacent (4).
5. #542's third part is decided: the written `broad-gate.md` comment is
   pinned by a case over the written file, not left unpinned (5).
6. #366's second half is the reviewing convention — a finding whose
   coordinates sit at two depths is written as two findings — in the three
   carriers the reviewer copies from, pinned; `depth_two` is untouched (6, 7).
7. Ledger row A11 is corrected in place with a `Corrected <date>` note (8).
8. The fold's `date = args.date or …` line is left byte-identical; the kept
   date is decided beside it (9).
9. #542's class has two more carriers than the ticket names — the handoff
   protocol's `Broad gate` row and the orchestration skill's sealer
   paragraph — read and brought to the template's clause in phase 3 (10).

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | #366 offered two answers and this frame took the cheaper one: the reviewer splits a finding whose coordinates sit at two depths. Does the owner also want the finer `depth_two` — one that attributes each added unit to the coordinate it pins rather than to the finding — built? It is a gate change (a heuristic over which names a unit references, with a false-positive argument to make and `CONTRIBUTING.md`'s four answers), which the milestone calls design and sends to 0.16.0. **Does not block this build**; the four phases are the same whichever answer comes, and #366 closes with this pull request either way | a person — the repository owner | **convention only** — #366 closes here; `depth_two` keeps refusing the whole set, and its refusal already names the finding to split next time · **the finer check, later** — a new ticket in 0.16.0 beside #159 and #526, carrying the four answers; this branch is unchanged · **the finer check, here** — moves this item off the patch-release criterion and into design; not recommended | convention only | ✅ **convention only**, answered by the repository owner 2026-09-24: #366 closes with this pull request on the reviewing convention; no finer `depth_two` is built and no 0.16.0 ticket is opened for it now |
| Q2 | The doubled-version reader exists twice after phase 2: `duplicated_version_headings` in `tests/test_release_hygiene.py` (the changelog's, reused by the ledger's real-tree case) and `doubled_versions` in `fold_ledger.py` (the `--check` arm's; a script cannot import a test; NAME NOT IN TREE until phase 2 adds it). Is one of them dropped — the hygiene case loading the script's reader by `importlib`, as `test_the_ledger_fragments_fold_at_release.py` already loads `evidence_check.py`? | the work — phase 2 decides it and `phases/phase-2.md` records it | two readers of one regex, both pinned (the changelog's by `test_a_version_heading_appears_once_in_a_changelog`, the script's by S8) · one reader in the script, loaded by the hygiene module for the ledger case | two readers; the changelog case keeps its own so `test_release_hygiene.py` does not start depending on a release script | ⬜ |
| Q3 | Ledger row A11 (§0.15.0, `1790174138`) says the written comment is *a code comment no test pins*, and phase 3 makes that false while every anchor of the row still resolves. `CLAUDE.md` §*House rules* has an arm for a claim whose code changed and an arm for a claim whose anchor was removed, and `seal/follow-up.md` holds the open question of a third arm for exactly this shape. Which shape does the correction take? | the work — phase 3 decides it and `phases/phase-3.md` records it | **in place** — a `Corrected <date>` note on the row naming S10's case, the shape A9 in the same section already carries and `correction_check.py` reads · **removal** — the row deleted from the shared file and rewritten in this item's fragment, the act `1790076050` took for its instance | in place — the smallest hunk in a file three parallel branches re-stamp | ⬜ |
| Q4 | Does `survivor-check --range origin/release/v0.15.1...HEAD` report the gatherer's `existing_date(…) or args.date or datetime…` line, or anything else, as a survivor of wording this branch removed? The date line is left byte-identical to avoid the one instance the frame can foresee; the docstring sentences phase 2 and phase 3 replace have folded copies nowhere (executed: `grep -rn "a run taken again\|count of runs" docs/ agents/ skills/ templates/` at `9f846733` hits `round_record.py` alone). Step A (#543) is fixing the code-idiom class in parallel and may land first | a measurement — one run at the verify phase | assume none; a `survivors.md` row with the quote and the grounds for anything reported | ⬜ |
| Q5 | The kept date on a second fold: the gatherer keeps the section's own date over `--date`. Does any test or document read the fold's `--date` as authoritative on a re-run? (Executed at the frame: `grep -n "\-\-date" tests/test_the_ledger_fragments_fold_at_release.py` shows `--date` passed only through the `fold()` helper and the twice/already cases, none asserting a re-dated heading.) | a measurement — the fold module's first run after phase 2; a case that expected the second date would go red there | the first fold's date wins, as the gatherer's does | ⬜ |

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
