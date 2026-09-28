# the verifying round is bounded, not the cheapest (#639) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build. No row needs a person.**

The judgments below were left open by #639 or by the spawn prompt, and the
tree answered them. They are listed so nobody reopens them. The grounds are
in `spec.md` and in `plan.md`'s Alternatives table.

- **Where the measured figure lives.** Only in `docs/review-chain-spec.md`
  (C3). `skills/code-review/orchestration.md` defers the rule to it twice
  (plan A2/A3).
- **What grounds the protocol's `verifying: exempt`.** The round's target and
  job, which is #51 observation 1's own ground. The ticket suggested "segment
  size", but #456's 46–58-call verifying rounds show that is false, so the
  row's "a segment that small" clause goes too (plan A4).
- **Whether `agents/warden.md` is a carrier.** It is: "the whole reason the
  round is affordable … exists to be cheaper than" makes the same claim in
  other words (plan A5).
- **Whether `skills/code-review/SKILL.md`'s "cheapest round on record" is in
  scope.** It is not. It is about #81's round 1, a finding round, and the
  issue's reading is confirmed. A separate doubt about its truth is routed
  to the orchestrating session (spec *Out*).
- **Whether "costs no round" is a carrier.** It is not. It is cap
  arithmetic, and the rule makes it true (spec, *Met and left alone*).
- **Whether a `<!-- specs/<id> -->` marker goes on the edited docs.** It does
  not. That is `settle`'s act (spec, Grounding).
- **Whether the exemption itself is still right.** Out of scope here. It is
  named in spec *Out* with its answerer.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does #639's figure reproduce? The figure is a median of 0.83 × round 1 over 29 verifying rounds of 0.14.0–0.15.5, with a range of 0.26–1.27 and five at or above round 1. C3 will print it. **Why the tree could not answer it:** the figure is an aggregate computed over free-form comments in five issues (#496, #535, #577, #601, #619). This frame read those comments but did not re-derive the 29 ratios, because pairing each verifying round with its own round 1 means reading every metered block, and the issue says its author already executed that | a measurement | (a) It reproduces: C3 stands as written. (b) It differs: C3 carries the re-derived figure, and #639 gets a comment saying so. In neither case does anything but one number in one paragraph change | C3 prints #639's figure with its five source issues beside it. The phase-1 record labels it *read from #639, executed by its author* | ⬜ |
| Q2 | Does `survivor-check --range` name the new module's gone halves, which are the removed sentences kept verbatim in string literals, as survivors? **Why the tree could not answer it:** whether the range's own writing is subtracted depends on how the check pairs a sentence removed from a `.md` with the same sentence written into a `.py` in the same range (`docs/review-chain-spec.md` §*What the sweep reads*). Reading does not settle that, and running it now would mean running it on an empty range | the work | (a) Silent: nothing to add. (b) It names them: one row per gone half in `survivors.md`, each anchored on its content, saying the pin is a deliberate carrier | Phase 2 runs it and does whichever applies | ✅ (a) silent: `survivor-check --range origin/release/v0.15.7..HEAD` exits 0, "no removed wording is still standing", over 454 files and 20 removed sentences, so no `survivors.md` was written (`phases/phase-2.md`) |

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
