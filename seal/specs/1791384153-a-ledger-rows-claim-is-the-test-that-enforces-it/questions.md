# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — questions for the planner

<!-- seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**What the tickets left open and the tree answered**, listed so nobody
reopens them here; `spec.md` §*Judgments the tree answered* holds the grounds
of each. The issue named three things for the frame to decide, and the tree
decided all three: a row's evidence is the test alone (D1); drifting is a
state a test row cannot enter, and the claim turning false is the suite's
finding (D2, §*What drifting means*); a released row migrates by one
`Corrected ·` row on demand (D5). The frame also decided, from the tree, that
the forms do not mix (D4), that a node id is read in the grounds cell only
(D3), that only a test is accepted (D2), and that `fold_check.py`'s resolver
is the copy that goes (D6).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is a bulk pass spent over the released rows that already cite a test — 1,042 of 1,308 claim rows at 5623d728, 139 of them citing nothing but test units — writing one `Corrected ·` test row per released row so that the families stop drifting at once rather than one by one as edits reach them? **Why the tree cannot answer it:** it is a value somebody is accountable for — about a thousand rows written in one fragment, each asserting that the test a row cites is the test that holds its claim, which for a row citing several grounds is a judgment per row. The tree says only that a feature branch must not do it (D5) and that the vehicle, if taken, is a fold fragment at a release. It does not block the build: on-demand migration is built either way | a person | **(a) No bulk pass**: families migrate as edits reach them, which is where a person is reading the row anyway; the drift cost falls over releases rather than at once. **(b) A fold fragment at a release**, written by one session after every branch has squashed, over the 139 rows citing only test units first, the rest by reading. **(c) The same, tool-assisted**: `--reverify` prints, per drifted released row, the test units it cites, and a person decides each | (a) | ✅ (a), the repository owner, 2026-10-08: no bulk pass — released rows migrate to a `Corrected ·` test row as edits reach them |
| Q2 | Does `family_view` already grade a `Corrected ·` row whose grounds hold the citation and no code coordinate as a family with nothing to grade, and does `--reverify --into` write no `Re-read ·` row for the released root it supersedes after that root's unit is edited? Reading says yes (`superseded`, and `left_alone`); reading is not the instrument. **Why the tree cannot answer it at framing:** it is a run of the checker over a planted fixture, and framing runs nothing | a measurement | S7's case in phase 2. If it passes against the unfixed checker, the mechanism is already there and the case is kept as the pin (seen red by removing the superseding). If it fails, phase 2 names the one branch that changes and `phases/phase-2.md` records it | the reading above | ✅ yes, measured by the work in phase 2 (5c24f534): S7's case passed against 48d201ad with `family_view` and `left_alone` unchanged, and went red with the superseding removed (`phases/phase-2.md`) |
| Q3 | For each released row that phases 1–4 drift — the rows citing `evidence_check.py#malformed_rows`, `#grounds_cells`, `#malformed_remedy`, `#check_ledger`, `#reverify_into`, `fold_check.py#target_problem`, `skills/evidence-check/SKILL.md#"## Verdicts and what to do"` and `#"## Re-verifying is recomputing the hash"` — is its claim held by a test it already cites, so that the citing row is the `Corrected ·` test row of D5, or not, so that it is a `Re-read ·` row as today? **Why the tree cannot answer it at framing:** it is a reading of each claim against the code as phases 1–4 leave it, which is phase 5's act, and the set of drifted rows is `evidence-check`'s answer at that head | the work | Phase 5 runs `evidence-check --strict .` at its head, reads each named row, and writes one citing row per released row. The choice per row and its grounds go in `phases/phase-5.md`; a row whose cited test is one ground among several takes the `Re-read ·` row | `Re-read ·` where in doubt | ✅ answered by the work in phase 5 (124cd1a6): 38 released rows read; five take a `Corrected ·` test row, each held whole by a test it already cited, and 33 the `Re-read ·` row (`phases/phase-5.md`) |
| Q4 | Does `hooks/evidence-advisor.py` carry a repair sentence of its own — one that names `Re-read ·` or `--into` in words the hook writes rather than the checker's output — that must learn the `Corrected ·` test row, or does it print the checker's lines? **Why the tree cannot answer it at framing:** the framer read part 7's row 1, which names the hook as a reader, and did not open the hook; opening it is one read in phase 2, where S9's sentence is written | the work | Phase 2 opens the hook. If it prints the checker's output, nothing changes. If it carries its own sentence, that sentence gains the option in the same commit as S9 and is pinned (§14) | nothing changes | ✅ it carries its own, answered by the work in phase 2 (5c24f534): `FROZEN_REPAIR` names the test row beside the coordinates a correction carries, pinned (`phases/phase-2.md`) |

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
