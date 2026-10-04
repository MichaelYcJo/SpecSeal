### Added

- A signatory that changes code a pact clause binds now leaves a record of
  it (#647, step C). When `evidence-check --reverify` moves the hash of a
  ledger row citing a clause of a pact the signatory's `Pact` row names, or
  leaves a coordinate of one BROKEN, the same command appends a pact change to
  `seal/pact-changes/<work-item-id>.md` and says so. `Pact notify` decides
  what is recorded: `when the pact is touched` records rows citing a clause,
  `always` also records every other row whose code moved, and `never` records
  nothing. The work item is the `--into` fragment's, or the one the branch's
  `routing.md` declares; with neither, the row is named and the run exits 1.
  The ledger is written exactly as before.

- `pact-check` reads every signatory's pact changes (#647, step D). A change
  citing a clause of the pact is `NOT TAKEN`, exit 1, until a pact review at
  the pact's repository takes it; the line names the record, the clause, the
  work item and the record's content hash. A pact review is an ordinary work
  item whose record, `seal/pact-reviews/<work-item-id>.md` (begun from the new
  `templates/pact-review.md`), takes a record at that hash with the verdict
  `holds` or `amended`. A record that grows after its review reads
  `NOT TAKEN` again. A change citing no clause, recorded under `always`, is
  `NOTED` and moves no exit. A review row that cannot be true is refused at
  exit 2. `skills/implement/orchestration.md` describes the act.

### Fixed

- The pact's `| Signatory |` table is read the way GitHub renders it. A
  signatory written as an autolink, `<https://…>`, used to end the table and
  go unread while `pact-check` exited 0; a thematic break was refused as a
  row; a header, delimiter or row indented one to three spaces was refused for
  the wrong cause; and a table GitHub does not render at all, under a list item
  or an open HTML block, was read. One table walker now reads all three pact
  tables, and the suite holds it to cmark-gfm (`cmarkgfm`, pinned test-only)
  over 16,364 shapes enumerated from the CommonMark and GFM block kinds.

- `pact-check` refuses a pact anchor whose `/` went missing, which had been
  read by nobody, and its refusal names a fenced code block as the way to show
  the anchor's shape. The grammar is now stated in `docs/the-pact.md`.

- Every path `pact-check` prints is in one form on every platform: relative to
  its repository, `~/`-relative under the home directory, and with `/`. The
  `UNREADABLE` line for a signatory's config used to mix separators on
  Windows.
