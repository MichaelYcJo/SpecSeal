# the seal stamp is a letter with the seal on its corner — questions for the planner

<!-- seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row below needs a person before the build, and none blocks it.** The
owner decided the design, the scale, the colours, the rows and the release
on 2026-10-02 (issue #717 §*The design the owner chose*; `spec.md` §*What the
owner decided*), and `routing.md` records `automation`. The issue and the
spawn prompt left the following judgments open; the tree answered them, the
grounds are in `spec.md` (§Grounding, §*What was measured*, §Scope) and
`plan.md`'s Alternatives table, and they are listed here so nobody reopens
them as questions:

- **Where the budget is measured and applied.** In the hook, over the whole
  message, one rung for every block in it; not per block, and not in
  `dispatch.py`, which assembles the final message but cannot re-render a
  stamp. *One rung for every block* was replaced by the owner on
  2026-10-02 (Q6): each block at its own rung, as many as fit with the
  disc, the rest left pending. A reserve of at least 1,000 characters inside `MESSAGE_BUDGET`
  covers what `dispatch.py#report` prepends.
- **What happens past the last rung.** Nothing: the sheet without its seal
  fits every panel the tree can produce, and that is stated as a bound with
  its arithmetic (`spec.md` S1) rather than guarded by a mechanism that
  would cut the deferred homes or leave a file pending forever.
- **Whether the threshold is measured or read.** Measured, by the probe
  `plan.md` phase 1 describes; the bracket the harness has already drawn —
  9,919 < limit ≤ 10,090 characters, from 25 drawn and 7 persisted messages
  in this project — is the fallback where a nested session cannot run, and
  the constant's comment says which it was.
- **Whether the limit counts characters or bytes.** Characters: the issue's
  *9.9KB* is 10,090 / 1024; the byte count would have printed 11.0. The
  transcripts bracket both units and do not settle it alone; the label does.
- **What the letter twin becomes.** It stays, at the block form's footprint:
  `|`, `.---.` and `'---'` where the block form paints the sheet's edge and
  its blank first and last lines, the text as itself, five characters for
  the seal's colours. Dropping it would lose the one console the twin exists
  for, make `0.10.0` S2 false and move every case that renders through
  `shape=True`, for no saving — the hook never draws the twin.
- **Whether the blank rows stay in the data.** They go: `panel` emits none,
  because the chosen sheet draws none and the values file should not claim a
  row nothing draws. Both forms skip a `null` an older file carries.
- **Whether the `CI also` row prints at 0.** It does; a row that goes quiet
  reads as a gate that stopped looking, which is the stderr line's own
  reason for not going quiet.
- **The gap between the text and the wax.** Two clear parchment cells on
  every text line. The prototype asked for two and enforced it on the disc's
  equator alone, so the owner's rendering shows zero on one row; two is the
  prototype's intent and costs under 50 characters. This is the one judgment
  here that changes a cell the owner looked at, which is why it is named
  first in the report.
- **Whether `broad_gate.py#gate` changes.** No. The terminal branch's call
  is `stamp.stamp(rows, args.scale, shape)` and keeps its arguments; the
  fifteen ledger rows anchored on `gate` are expected not to drift.
- **Whether a values file's `scale` is rewritten when the hook steps down.**
  No. The file records what the gate asked for, as a terminal draws at
  `--scale` without recording it.
- **Where the compositor lives.** In `seal_stamp.py`, beside `build`,
  `letter` and the writers; `hooks/sealer-stamp.py#STAMP` names one module.
- **How the drawing is pinned.** By its properties — the budget, the
  footprint, the gap, the overhang, the kept trailing cells, the colour
  codes — and by `test_the_disc_draws_the_same_bytes_in_every_process` for
  reproducibility; not by a golden file.
- **What the installed 0.16.0 hook does with a 0.17.0 values file.** It
  draws the rows with its own renderer — rope and gold, under the pre-#666
  label — because the hook loads the `seal_stamp.py` beside itself. Whether
  that message clears the limit is Q3.
- **The READMEs.** Neither names a row or the drawing; both keep their hook
  table row unchanged.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The exact number of characters past which the harness persists a `Stop` hook's `systemMessage`. The harness has already bracketed it — 25 messages of 9,886 to 9,919 characters drawn, 7 of 10,090 to 10,270 persisted, across three sessions of this project (`spec.md` §*What was measured*) — and the issue asks for 9,990 and 10,010 to pin it | **a measurement** — the smith, in phase 1: a scratch directory with a `Stop` hook printing a message of N characters, one headless turn (`claude -p`) at each N, and the scratch project's `tool-results/` read for a `hook-*-systemMessage.txt`. No person's opinion is the instrument | **9,990 drawn and 10,010 persisted:** `MESSAGE_LIMIT = 10000`, labelled executed. **Both drawn, or both persisted:** the limit is outside (9,990, 10,010]; the probe moves by the bracket's remaining width and the comment says so. **The nested session cannot run** (no `claude` on the path, or the harness refuses a child): `MESSAGE_LIMIT = 10000`, labelled read, with the bracket as its ground and the probe named for the next reader | 10,000, labelled read, with the bracket | ⬜ |
| Q2 | How the sheet reads on a light terminal background as well as a dark one: the parchment (230, `(255, 255, 215)`) and its edge (187, `(215, 215, 175)`) are painted backgrounds, and on white the edge may be hard to see | **a measurement** in two halves. The arithmetic half is the smith's, in phase 3: the contrast ratio of 230, 187, 94 and 124 against black and against white, in `phases/phase-3.md`. The reading half is the repository owner's, on the first real seal of 0.17.0 on each background — no case, hook or workflow can observe a screen (`docs/the-broad-gate.md` §*Where the stamp is drawn*, second paragraph) | **Legible on both:** nothing. **The edge vanishes on light:** one constant moves (187 to a darker tan) in a follow-up, with a second look. **The sheet itself vanishes on light:** the palette question reopens with the owner, and the dark rendering stands meanwhile | The chosen palette, carried as an `overview.md` `## Not verified` row with the owner as answerer | ⬜ |
| Q3 | What the installed 0.16.0 `Stop` hook draws over a values file this branch's gate writes, during this very release run: its own 0.16.0 renderer over the new rows, under the pre-#666 label. Reading says about 9,900 characters — the current 10,090 less the three rows and the three blanks that leave the panel, which shortens the stamp from the panel's height to the disc's 20 lines — inside the band the harness has drawn unpersisted (up to 9,919) and under the lowest message it persisted (10,090), with little room either way | **a measurement**, on the first real seal of this branch, read by the owner the way #666's Q3 was: drawn whole, or a persisted preview | **Drawn:** nothing; the fix lands when 0.17.0 installs. **Persisted:** the `SEALED` line's `seal-stamp --from` runs the installed copy too, so the owner draws the letter with the tree's `skills/verify/scripts/seal_stamp.py --from <path>` by path, once; nothing in the tree changes, because the window closes at the install | Drawn, carried as an `overview.md` `## Not verified` row with the owner as answerer | ⬜ |
| Q4 | The names of the fitting function and the compositor; the five characters `KEY` gives the seal's colours in the letter twin; the `CI also` row's wording where `<n>` is 0; the reserve's exact size; the sheet's width where the text and not the seal sets it | **the work** — fixed by the cases that pin them (contract §14), within `spec.md` S1–S4's constraints: the budget is `MESSAGE_LIMIT` less at least 1,000; the twin's characters are distinct and the field keeps `.`; the row prints at 0 and says a count; the sheet's edge is one cell each side | Constrained by `spec.md` §*Data & interfaces*; the phase that writes each records it in its `phases/phase-N.md` | As `spec.md` states | ⬜ |
| Q5 | Which existing cases read a panel row, the drawing or the hook's bytes and so go red when each surface changes. Found by `grep` at framing and listed in `spec.md` §*What was measured*, last-but-one row: the sealer test's Part 1 and its A5, suite, ledger, width and sample cases; the stamp test's `ROWS` and byte comparisons; the partition test's A6, `HISTORICAL_ROWS` and real-workflow cases; the range test's frame regex and `letter` width cases; `test_a_gate_that_fails_says_so.py`'s S9 | **the work** — each phase meets its own and moves it, saying in `phases/phase-N.md` which pins moved and which were seen red first; a case the grep missed surfaces as a red run in that phase's slice and is handled there | Phases 1–3 move the listed ones; a vacuous assertion left behind — one that passes because the row or the rope it reads no longer exists — is a finding for the warden, so each moved case asserts the new surface positively | As listed | ⬜ |
| Q6 | What the hook draws when several seals are pending at one `Stop` and not all of them fit `MESSAGE_BUDGET` with their disc. S1 drew every block at one rung for the whole message, and round 1 measured what that does: two seals of #702's size (9,356 characters together at 0.75) both lose the disc, and eight print 10,118 characters, past the limit (`rounds/round-1.md` 🟡 1 and ⬜ 2) | **a person** — the repository owner, because it trades the disc against drawing every seal in the turn it was sealed. Opened by round 1's fix pass rather than by the framer: S1's rule was a frame judgment the owner had not seen | **One rung for the whole message (S1):** every pending seal is drawn in the turn it was sealed, all at one rung, so two of a real run's size both lose the disc and eight pass the limit. **As many as fit with the disc, oldest first, each at the highest rung it can take, the rest left pending:** no seal is truncated and none loses its disc because other seals share the turn; a session that ends right after leaves the remaining seals undrawn until `seal-stamp --from` draws them | The second, as answered. The rung with no disc stays only for a single seal that cannot fit at 0.75 alone, and the first pending file is always drawn, so the queue cannot stall | ✅ answered by the owner, 2026-10-02 — built as `seal_stamp.admitted` and `hooks/sealer-stamp.py#drawings` in round 1's fix pass |

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
