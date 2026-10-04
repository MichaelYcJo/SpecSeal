### Fixed

- A pact change `evidence-check --reverify` records no longer moves a hash
  to itself (#774). Under the freeze, a released row's family can hold a
  newer reading in a fragment `--ledger` left out. Where the code went back
  to the released hash, the run recorded the move from the released row's
  hash, which is the hash the code already had, so the record read
  `h1 → h1`. A recorded move now starts at the hash the coordinate's newest
  reading holds, so the same tree records `h2 → h1`, the move the code made.
  A part whose two hashes agree is not recorded by any writer, and a row
  with nothing else to record is neither recorded nor left.

- One `--reverify` without the freeze leaves no citation it moved DRIFTED
  (#772). Re-stamping a released row in place moves the line that a
  fragment's `Re-read ·` row cites. The walk read files in name order, so a
  fragment, or `seal/releases/0.10.0.md` before the `0.9.0.md` it cites, was
  hashed against the old line, and `--strict` exited 2 until a second run.
  The walk now reads a cited file before every file citing it. A run
  narrowed with `--ledger` that moves a line cited from a file it left out
  names that citing row on a `LEFT` line and exits 1. A re-stamped citation
  is a ledger line rather than code, so it records no pact change.

- The pact-change trigger is stated whole where a signatory reads it (#775).
  `templates/config.md` §*Pact* pointed at only two of the three cases that
  record a pact change. It now points at `docs/the-pact.md` §*A signatory
  records a pact change*, whose first sentence is the whole trigger. The
  usage text, the evidence-check skill and the template each have their
  sentence pinned, and the pact paragraph's `Enforced by:` line names the
  cases that hold its refused-row and newest-reading clauses.
