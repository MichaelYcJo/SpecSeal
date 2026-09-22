- **`settle` shipped one release ago and had folded nothing; this is the
  first fold, and it removes 88 work item directories (issue #497).** The
  standing statements of 88 released work items are written into `docs/`,
  every check that counted the record corpus is answered, and
  `settle --retire` removes the directories the prose now covers. Measured
  before and after: 99 directories and 1,379 files under `seal/specs/`
  become 12 and 51, and the round-record corpus goes from 263 to 7. Eleven
  directories are kept by name — ten because they wrote no `spec.md` and so
  state no rule, and one because a permanent `seal/ledger.md` row anchors
  into its round record and the repository's own rule refuses a re-point.
  Five other `seal/ledger.md` rows anchored into a retired `spec.md`, so the
  ledger is edited: the three whose only anchor that was are removed, and the
  two with a live code anchor keep it and drop the dead one.

  **A reader of this release meets four new policy documents, and that is a
  change to the repository's policy surface rather than a side effect of a
  cleanup.** `docs/the-evidence-ledger.md`, `docs/the-broad-gate.md`,
  `docs/measuring-a-run.md` and `docs/the-agent-set.md` are new, and a
  `docs/` file outranks the SDD set from the moment it lands. Each area was
  checked for an existing owner first: a fifth document about the gates a
  session meets was planned and **not** written, because
  `docs/review-chain-spec.md` already carries a section per gate and the
  plan forbids a second document for a covered area. Whether four is the
  right shape is the owner's to overturn at the merge — each new file is its
  own phase and each folded item sits on a named section, so merging two of
  them afterwards is one edit and a marker move.

  **No floor literal was lowered.** Nine checks carried a population floor
  over `seal/specs/` that the fold turns red, and every one of them was
  re-pointed rather than reduced — `assert len(records) > 200` becomes *the
  walk covers the records `git ls-tree HEAD` carries and the tree still
  has*, and `> 100` becomes *the corpus covers every work item whose
  `rounds/` holds a committed record*, derived from `os.listdir` rather than
  from git.
  Both hold at 263 records and at 7, and both are stronger than the floors
  they replace: `> 200` was green over a listing that had lost a whole work
  item, and neither of these is. Of the same nine, three moved to fixtures
  that plant their own specimens, and two cutoff constants ask whether their
  work item is **traceable** — its directory in the tree, or `docs/`
  recording the fold — so a directory removed with no marker behind it still
  fails, which is the typo they were written for. One floor the frame
  expected to re-point was measured instead and declined: the teeth survive,
  in four of the seven remaining records.

  **The pull request's chain check now tells a retirement from a
  deletion.** `chain_check.py` prints `retired: …` for a `routing.md` that
  `settle --retire` removed, where a top-level `docs/` file carries the work
  item's `<!-- specs/<work-item-id> -->` marker on a live line, and it still
  refuses a removed declaration where no such marker stands. Before this, the
  first fold's 88 retired declarations were refused, every one of them.

  **The wrap limit and the fold marker collided, and the limit moved.**
  `<!-- specs/<id> -->` is matched whole by the reader, so wrapping it makes
  it stop being a fold record and the retirement refuses the directory it
  covers — and its length is decided by a directory name chosen months
  earlier in another work item. Of the 88 markers one reaches 89 columns.
  `tests/test_docs_line_wrap.py` now skips a marker on a line of its own,
  exactly one line wide, with cases pinning both halves.
