# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, and not reopened here.** `spec.md` §*The judgments
the tickets left open, decided from the tree* gives the grounds for each, and
`plan.md` §*Alternatives considered* gives what each was chosen over.

- **#603: which removed rows take the exit.** A live ledger row the range
  removed, where at least one anchor resolves at `a` and not at `b`. It is not
  every removed row line, because a row corrected in place is one and that is
  a correction. It is not "every anchor left", which was measured to fix none
  of #587's 8 places (the three rows kept 4, 4 and 1 live anchors).
  `docs/the-evidence-ledger.md` permits both kinds of removal, and both
  follow an anchor leaving.
- **#603: what a ledger file is.** The four locations
  `evidence_check.py#default_patterns` reads, as committed path shapes.
- **#603: a row in a fence or an HTML comment** stays measured, read through
  `live_lines` as the gathered marker is.
- **#591: whether to fix at all, given the measurement.** On #581's range the
  fold carried no statement verbatim into `docs/`, and moving the retired side
  into the pairing changes nothing: 0 n-grams, 0 survivors either way. It is
  built anyway: it is #563's class, it only moves toward reporting, and #603
  needs the same pair-then-drop order.
- **#592: how the departure is chosen.** Affinity, then gone at `b`, then
  path order.
- **The report prints nothing new**, and the `docs/` statements are corrected
  in place with no marker.

No row below needs a person. The owner pressed `automation` for this
milestone, and nothing left here would change what gets built.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Do the pinned coordinates in `RELEASE_RANGES` (`test_the_four_real_ranges_report_their_prose_and_none_of_their_code`) move under phases 1–3? Phase 1 can change which departure is a source, and so the coordinate a row names. Phase 3 can take removed ledger rows out of a range that removed one. **Why the tree cannot answer:** only running the four ranges at each phase's commit settles it | a measurement (the one case, run at each phase boundary) | Unchanged: nothing to do. Moved: the pin is updated coordinate for coordinate, and each move is explained in that phase's `phases/phase-N.md` as a departure re-chosen (phase 1) or a removed row's exit (phase 3). A place that disappears for any other reason is a finding, not a pin to update | Each phase runs the case and records the result | ⬜ |
| Q2 | What do the other pull requests squashed into `release/v0.15.3` report after phase 3? #603 names only #587, and nobody has measured the rest. **Why the tree cannot answer:** only a run over each range says whether a removed row was the source there too | a measurement (`survivor-check --range <squash>^..<squash>` for each pull request's squash commit on `release/v0.15.3`, run with the script at the base and at phase 3's commit) | Nothing changes beyond #587: recorded. Another range loses survivors: each lost place is checked to have come from a removed row whose anchor left. Anything else is a finding for the review | Phase 3 runs it for the squashes of #588, #589, #593, #594 and #595 and records both outputs in `phases/phase-3.md`. The build does not wait on it | ⬜ |
| Q3 | Does `docs/review-chain-spec.md` hold the three clauses within its 38 remaining lines (962 of 1000)? **Why the tree cannot answer:** the wording is the builder's | the work (each phase that edits it) | Fits: nothing to do. Does not fit: tighten the same two statements. Never move a sentence to another document to make room, because the statement's `Enforced by:` line and its fold markers belong to this one | Each phase keeps its own addition to the fewest lines that state it, and `bin/fold-check` is the check | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person**: what the product should be, or a value somebody has to be
  accountable for. Only this kind blocks the build, and there is none here.
- **a measurement**: a probe, a command or a count settles it.
- **the work**: it cannot be known at framing time. The phase that meets it
  decides it there and records a divergence row; it does not travel back to
  the framer.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
