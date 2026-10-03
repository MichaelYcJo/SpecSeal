# the commit gate's policy is cut into files by question (#727) — questions for the planner

<!-- seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/questions.md
     The run is unattended (routing.md: Automation yes, Answer pressed
     automation), and the owner answered once, for all of milestone 52. So no
     row here waits on a person. Each row a person would decide is decided by
     this frame, with the answer written in and the grounds in spec.md, and a
     person may overturn it by opening what the frame opened. -->

**Judgments the ticket left open that the tree answered.** They are listed so nobody reopens them. Each one's grounds are in `spec.md`.

- **The file names and which headings go where.** `docs/the-record-layout.md` F1 is policy and fixes both (D1).
- **The ledger anchors that move.** Two released rows, three coordinates, each re-pointed by a `Corrected ·` row. The anchors that stay are untouched, provided the parent's index sits before `## Registration` (K3, D4).
- **Riders.** There are none to follow. `rider_check.py#RIDER_ROOTS` keeps riders out of `docs/`, and a rider hashes its own file (K4).
- **The precedent for the citations and the absence reader.** #526's S2 and S3 rows (D6, D10).
- **The fold markers.** 18 markers, carried whole because statements end at headings. The digest leaves with the row (K1).
- **D7's *each is under 500 lines*.** It is false for the parent, which is 576 lines before its index. The ceiling, 1,000, is the requirement, and the figure is corrected where the record layout states it (D9).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Do the moved headings and paragraphs move byte for byte, or may they be re-levelled and reflowed to suit their new file? | a person: decided by frame | **Verbatim, plus a `##` wrapper in the arms file.** Hashes stay, so each `Corrected ·` row shows the content is the same. Three test slices change only their path, and survivor-check reads the move as a move. **Re-level and reflow.** Every moved unit's hash changes, three tests need new slice markers, and every reworded heading becomes a survivor to chase | Verbatim (D2, D3) | decided by frame 2026-10-03 |
| Q2 | Is the `Over the ceiling` row deleted, or set to `none`? | a person: decided by frame | **`none`.** *Declared, nothing listed*: the check keeps running, as #526 left it. **Deleted.** *Not declared*: `fold-check` stops checking that half and prints one line saying so | `none` (D8). The task's *the row for it is removed* is read as the entry removed | decided by frame 2026-10-03 |
| Q3 | Which references to the old path are re-pointed? | a person: decided by frame | **Every reference whose subject moved, bare or `§`, in every live file.** One rule. Its cost is ledger drift on the code units those comments sit in (K3's upper bound, about 13 released rows). **Only `§*…*` citations.** Less drift, but bare mentions such as *the standing waiver `docs/commit-review-gate-spec.md` refuses* send a reader to a file that no longer says it | Every reference whose subject moved (D6). References whose subject stays are not touched | decided by frame 2026-10-03 |
| Q4 | Is a permanent test planted that resolves every `§*…*` citation? | a person: decided by frame | **No.** S1 and S5 are verified by `test_tmp_*` probes, run once and deleted, as #526 verified its 36 citations. **Yes.** That is new mechanism in a move, and nothing like it exists today; it would want its own issue and frame | No (D11) | decided by frame 2026-10-03 |
| Q5 | Does the parent's `Authority for` paragraph get rewritten, given that S2's minor anchor (`seal/releases/0.15.1.md` line 96) then drifts? | a person: decided by frame | **Rewrite it, keeping its first words.** The paragraph claims *the two opt-in arms, and the routing declaration*, which after the cut is false. The cost is one `Re-read ·` row, and the claim still holds. **Leave it and add a paragraph.** No drift, but a false authority claim stands at the top of the file | Rewrite it (D4) | decided by frame 2026-10-03 |
| M1 | How many released rows do the K5 edits drift, beyond the 2 `Corrected ·` and 2 `Re-read ·` rows K3 counts for the document's own anchors? | a measurement | `bin/evidence-check` after phase 2 names each. The upper bound, read off the anchors, is about 13: `hooks/commit-review-gate.py#main` 6, `#touches_code` 1, `#DOC_ROOTS` 1, `chain_check.py#restored_from` 1, `tests/conftest.py` 1, `tests/test_docs_line_wrap.py#COVERED` 2, agent contract §17 1. Add one row in work item `1790993137`'s fragment, which is re-stamped in place | Phase 3 writes whatever the tool names | ⬜ smith, phase 3 |
| M2 | Does a module-level comment above `DOC_ROOTS` (two hook files) or above a test function (`tests/test_the_commit_gate_decides_at_the_commit.py` 439, 594) fall inside that unit's hash? | a measurement | The same `evidence-check` run answers it. It changes M1's count and nothing that gets built | Re-point either way (D6) | ⬜ smith, phase 3 |
| M3 | What does `bin/survivor-check --range 2b1dcb1f...HEAD` report? | a measurement | The verbatim move cancels itself out (K7). The candidates are the reworded lines: K6's six, the preambles, the record-layout and evidence-ledger sentences, and each re-pointed citation | Correct each, or exempt it in `survivors.md` with its quote | ⬜ smith, before hand-back |
| W1 | The wording that replaces each K6 crossing reference, and whether any of the 19 other *above* and *below* lines turn out to cross once the files exist | the work | Phase 1 reads each against the file as it lands. Only the wording varies. D5 fixes the shape (file and section) | The citation shape in D5 | ⬜ smith, phase 1 |
| W2 | The exact text of the two new H1s' `Authority for` paragraphs and of the parent's index lines | the work | D3 and D4 fix what each must name and where it sits. The sentences are the builder's | As D3 and D4 | ⬜ smith, phase 1 |

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
