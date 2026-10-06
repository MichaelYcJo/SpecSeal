### Changed

- A review run whose fixes are themselves the next round's finding twice now
  stops its fix passes and sends the work item back to its framer (#823). In
  two 0.18.3 chains a fix pass wrote code, the next round found a regression
  inside that code, and it happened again one round later; nothing counted
  it, and each run filed its third fix as an issue that begot another.

  `round-record new` now writes a `Fix of a fix` row on every round record.
  It reads the previous record's fix range and asks whether an open finding
  that owes a fix sits inside a top-level function, class or constant those
  fixes added or changed. The first such finding in a run reads `first`; the
  second reads `second`, and `new` prints that no fix pass is to be
  commissioned. The record's open findings close `deferred the frame`, the
  pull request is labelled `chain: reframed`, and the framer is spawned again
  with the run's round records. The next record is refused until the framer
  has added `Reframed <date> by <who>, after round <N>.` under the `Framed`
  line of `spec.md`, and the redesign's rounds start a new run: the floor, the
  printed bound, the count and the depth of new units do not reach back
  across the stop.

  `chain-check` refuses, for work items begun from this release, a record
  without the row, a value outside `no`, `first — …` and `second — …`, a
  count that disagrees with its run in either direction, a run that counted
  past the stop or wrote a fix under it, and a record after the stop with no
  `Reframed` line for it. Notes, confirmations and out-of-scope rows never
  count, nor does a finding in prose, a code name mentioned beside the path
  of any non-Python file the repository tracks (a document, a `bin/`
  wrapper, a `.cmd`, a `Makefile`), a bare name more than one touched file
  defines, or one the reader cannot place.

  Replayed over the committed round records of the four 0.18 releases, with
  the pull request heads fetched (119 of 122 records resolve), the stop
  would have reached 26 of 64 work items, #814 and #801 among them, both at
  round 3. A reviewer opened 11 of those stops: 10 were real fixes of fixes,
  one a defect written by the fix pass before the previous one, and none a
  false stop.
