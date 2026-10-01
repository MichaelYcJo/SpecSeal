# the reading segments batch again, and the opening lives in a file — questions for the planner

<!-- seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** The owner pressed
`automation` for the whole release on 2026-10-01 (`routing.md`), and the one
question the ticket addressed to the owner — item 3, *separate model from
instruction* — is a measurement (Q1 and Q2 below): one spawn and one
`session_cost.py` reading settle it, and an opinion is the wrong instrument.
Two values this frame set are written as assumptions, overturnable by the
owner in a fix pass without reopening the frame.

**Judgments #640 left open that the tree answered.** Listed so nobody reopens
them; the grounds are in `spec.md` §*Grounding* and §*Scope* and in
`plan.md`'s Alternatives table.

- The opening goes into `agents/framer.md` and not into
  `skills/implement/orchestration.md` or a spawn prompt: the protocol's
  §*What every spawn prompt used to carry* says where a rule reaches an
  agent from, and the framer's own definition is where the warden's and the
  smith's numbers already live.
- The rewording bounds the burst and forbids nothing: every reading at
  1.00–1.12 carried the prohibition, and the readings without it on the
  same model line (#456, `claude-opus-5[1m]`) read 1.48–1.64. The model is
  not what separates 0.12.2 from 0.12.3.
- The grade is per kind, keyed on the spawn's `subagent_type` basename, and
  lives on the `--segments` page only. The plain reading keeps `< 1.2` and
  its protocol sentence; a lone transcript carries no kind.
- The warden bar is the protocol's 1.8, not the definition's 1.89. The
  framer bar is the ticket's 1.4. Smith is exempt by the protocol's
  implementing row. `sealer` and `scribe` have no bar and print as
  ungraded, counted and named.
- A verifying warden round is exempt by the protocol and is not detected:
  the page prints the exemption and a reader applies it.
- The block is additive — under the table, before the §6 block — and no
  number on the page moves, so no comparability line is added.
- The protocol's draft number is not bumped (Q5 lets the work overturn
  that).
- `docs/review-handoff-protocol.md` gains a `framing` row: the bars table is
  the only place a bar is defined per kind, and the script's constants are
  cross-pinned to it rather than read from it.
- Both README editions and `skills/verify/SKILL.md` step 1 say what the
  page now prints, because the first frame of `agents/framer.md` left both
  READMEs out of scope and phase 1 hit it.

**Assumptions, written down and continued on** — each would change one
number in prose, not what gets built, so neither is a row.

- **A1.** The bound on one read batch is *about six reads or ranges*. This
  frame sent five to seven calls on every turn of its gather and did not
  stall; the 0.15.1 framers at 2.3–3.1 finished. Q1 reads the exact figure.
- **A2.** The framer bar is 1.4, the ticket's *How to verify* target, under
  the five-release band of 1.46–1.79.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What did this frame's own segment read — tools per turn, calls, turns, and the largest number of calls in one turn — on Fable 5.1, with no prohibition in its prompt and no opening in its definition? It is the control for the ticket's model confound: the first framer on the current model without the sentence | a measurement | the tree cannot answer it at framing time: the transcript is written as this frame runs and `session_cost.py` has not read it. One command answers it — the tip's `--segments` over the orchestrating session's transcript (`plan.md` phase 4), with `--json` for the per-turn maximum. If the largest batch is well above six and nothing stalled, A1's number is loose and the owner may raise it; if the ratio is under 1.4, A2 is the bar a framer without the opening already misses, which is the ticket's shape | A1 stays at about six; A2 at 1.4. The numbers go into `phases/phase-4.md` and the changelog entry as one reading | ✅ measured 2026-10-01 in phase 4 (executed): 50 calls over 12 turns, 4.17 tools per turn, largest batch 11 calls, and the frame finished. The largest batch is well above six, so A1 is loose and the owner may raise it; the ratio is far over 1.4. One reading, `phases/phase-4.md` |
| Q2 | Does a framer spawned after this ships — current model, the bounded opening in `agents/framer.md`, no prohibition typed — batch above 1.4 and finish without a watchdog loss? This is the ticket's item 3 as filed, *run one framer spawn on the current model with the reworded opening and read its tools per turn before setting the framer bar* | a measurement | no such spawn exists until phase 1 is merged, so no reading can be taken inside this item. The first framer of a later 0.17.0 item, or of the next release, is the spawn; its `--segments` row is the reading and it is posted to the open `flow-measurement` log (#695) the way every segment is. If it stalls, the bound in A1 is the first thing to lower; if it reads under 1.4, the bar is a lens and the next log's median is what the ticket's *How to verify* reads | the bar is set from the band (A2) before the reading, which is the ticket's own ordering reversed on purpose: a bar that waits for one spawn is a bar set from one spawn | ⬜ |
| Q3 | Do the 0.17.0 flow log's framer and warden medians rise to the ticket's targets (framer ≥ 1.4, warden ≥ 1.3) with no watchdog stall? | a measurement | the tree cannot answer it before the release that carries this ships and its segments are measured. The 2026-09-28 sweep's method over #695's metered blocks is the instrument. Nothing in `spec.md` promises the rise (`agents/framer.md` §*Do not promise a saving*) | no acceptance criterion rests on it; the row exists so the next sweep knows where the number was expected to appear | ⬜ |
| Q4 | Which ledger rows does the edit drift at the tip? | the work | `spec.md` §*Data & interfaces* counts the expected set at `cd24f516`, but items A (#641) and B (#638) land in parallel on the same release branch and re-stamp some of the same rows (`session_cost.py` units under B's `broad_gate` neighbour, `skills/verify/SKILL.md`'s section under either). Only `evidence-check` at the merged tip answers it | re-read every row it names; a row outside the expected set is explained in `phases/phase-4.md`. The one correction in place (`seal/releases/0.4.0.md`, the bars-beside-the-meter row) is known now | ✅ answered by phase 4 (executed): nothing had landed on the release branch, and `evidence-check` named 22 rows in nine files, each re-read and re-stamped; two corrected in place. `phases/phase-4.md` lists them |
| Q5 | Does adding a row to the protocol's bars table bump the document's draft number, and does a case in `tests/test_the_handoff_before_round_one.py` pin an adjacency on the `--segments` page that moves the block from between the table and the §6 block? | the work | the frame read the draft case (title and Status must agree, nothing more) and #639's edit to the same table, which bumped nothing; it read the page's test names and not every assertion body. Phase 2 and phase 3 meet both while building | no bump; the block sits between the table loop and `report_breaches`. Either moved is a divergence row in that phase's record with the case that forced it | ✅ answered by phases 2 and 3: no bump, and no case pinned the adjacency; a new case now pins the block between the table and the §6 block. `phases/phase-2.md`, `phases/phase-3.md` |

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
