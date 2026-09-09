<!-- specs/1788912166-red-for-following-the-documents-green-for-ignoring-one -->

### Fixed

- **A draft pull request was failed for doing exactly what a document told it
  to do.** `skills/code-review/orchestration.md` opens the draft pull request
  at the end of the build, before round 1, because a reviewer needs a pull
  request to review. So the first thing that happened after the draft opened
  was `chain-check` running against a `rounds/` directory that is empty by
  design — and the arm counting round records failed it. That window was
  documented as *the window's expected state, not a failure to chase*, which
  is a check teaching people to route around it.

  The `Pass` arm a hundred lines down the same walk had been draft-aware since
  the draft state was first read, and its own message says *"Open it as a
  draft while the rounds run"*. The record-count arm now reads the same value:
  on a draft the missing record is printed and the run exits 0, and the notice
  names `ready_for_review` as what re-arms the check. Nothing that can reach
  `main` is exempt — pressing *Ready for review* re-runs the workflow and the
  arm applies.

  **`unknown` stays strict**, and that is the fix's whole safety property.
  `pull_request_state` has three answers, not two: no payload, a payload that
  will not parse, one naming no pull request, and one whose `draft` is a
  string all land on `unknown`, which is judged as ready. A parametrised case
  pins all four, because a harness that stopped writing the flag would
  otherwise turn this fix into a way past the round-record requirement itself.

- **A documented deletion cost 153 written sentences, so nobody was ever going
  to write them.** `survivor-check` reports every place still carrying wording
  a range removed, and a branch that DELETES a shipped section leaves every
  sentence of it standing in the durable copies that are supposed to survive a
  deletion. Measured on one release's own range: **153 places at similarity
  1.60–1.62**, every one correct as a report and not one of them a defect. The
  escape was one row per survivor, which at that size is not an escape — the
  branch turns the step off instead, which is the outcome the escape exists to
  prevent.

  `seal/specs/<work-item-id>/survivors.md` now takes a second row shape,
  `| Range | Grounds |`, alongside the per-survivor `| Path | Quote | Grounds |`.
  The first cell tells them apart, and a path can never be read as a range
  because the dots need a non-space word on both sides. The spec is resolved
  rather than compared as text, because CI spells the range
  `origin/<base>...HEAD` and a person spells it as two commits — those are one
  range.

  **The row is anchored on the range and on the work item it lives in, and the
  second anchor is why the first is not enough.** `origin/<base>...HEAD` is not
  a range, it is a relation, and it resolves to whatever range the checkout it
  is read on is over. Every work item's `survivors.md` in the tree is handed to
  every run, and one lives until the release that ships it, so a single merged
  row in that spelling excused every later branch cut from the same base and
  turned the step off for the rest of the release — the outcome the escape
  exists to prevent, arriving through the escape. A declaration now holds only
  over a range that touches its own work item's directory, which a work item's
  own range always does.

  Both anchors fail loudly. A spec that no longer resolves prints under
  `unresolved`, one refused for belonging to another work item prints under
  `not yours` with that work item named, and neither refuses the run — a
  deleted release branch in an old declaration cannot turn every later check
  into a refusal. Grounds are not optional, and every excused survivor is
  still printed with them: what this removes is the cost of writing 153 rows,
  never the cost of reading 153 lines.

### Added

- **The `Broad gate` cell is read now, and until this release nothing read
  it.** Every round record carries the row and `grep -n broad` over the
  checker matched no line at all, so the one full-suite run this whole design
  turns on could be skipped, or spent before the round it was meant to seal,
  and no gate in the repository had an opinion about either.

  At a **ready** pull request `chain-check` reads the cell on the last round
  record, and it tells four states apart. `not yet` — or no row at all — is
  the run that never happened. A SHA the record's own `Target SHA` descends
  from is the run spent before the round it was meant to seal, and the refusal
  names both commits; that is the more expensive of the two, because the cell
  claims a run happened. A cell with no SHA-shaped word in it names no run and
  fails too: above the cutoff `round_record.py new` writes the row on every
  record and `close --broad-gate` is the only thing that changes the value, so
  such a cell is a choice — and left as a notice, writing `skipped` was a
  shorter way past the arm than deleting the row. Below the cutoff it is still
  reported rather than failed, because records written before it hold free
  text.

  Equal is not premature — `git merge-base --is-ancestor X X` succeeds — so
  the resolved commits are compared before any ancestry question. The passing
  condition is asked directly, *the gate ran at the reviewed commit or after
  it*, rather than as the complement of *premature*: written the other way it
  admitted a gate commit on an unrelated line of history in silence. That case
  is reported now, and a gate SHA this repository cannot see makes no claim at
  all, which is the ordinary state after a squash.

  **A draft is excused it**, for the reason the rounds are still running: the
  broad gate runs once, after they settle.

  **It is bounded by a cutoff, and that is not optional.** Every round record
  ever written defaults to `not yet`, so an arm reading the cell without one
  would be red on every work item in the tree and every one in flight. The
  cutoff is keyed on a work item's id the way the seven before it are, and the
  reasoning is the one they share: a check whose first production act is red
  on history nobody can fix is a check people learn to skip.

### Changed

- **`Broad gate`'s label and its `not yet` sentinel moved** from the script
  that writes the row to the one that now reads it, and the writer imports
  both. Two copies drift silently in the direction that matters — rename the
  row in the writer alone and it keeps writing a row the reader no longer
  finds, which the new arm reads as *no run was named*.
