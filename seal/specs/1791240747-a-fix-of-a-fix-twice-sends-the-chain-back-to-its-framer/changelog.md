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
  printed bound and the count do not reach back across the stop.

  `chain-check` refuses, for work items begun from this release, a record
  without the row, a value outside `no`, `first — …` and `second — …`, a run
  that counted past the stop or wrote a fix under it, and a record after the
  stop with no `Reframed` line for it. Notes, confirmations and out-of-scope
  rows never count, nor does a finding in prose or one the reader cannot
  place.

  Replayed over every committed round record whose fix range this clone
  still carries (83 records of 57 work items, at the `v0.18.0` and `v0.18.3`
  tags), the stop would have reached 18 work items, #814 and #801 among
  them, both at round 3. That count is the repository owner's to weigh
  against a finer grain; `questions.md` of the work item holds the numbers.
