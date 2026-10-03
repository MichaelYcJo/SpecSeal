# Pact review — <work-item-id>

<!-- seal/pact-reviews/<work-item-id>.md, at the pact's repository: the
record of one pact review (`docs/the-pact.md`). A pact review is an ordinary
work item here, opened when `pact-check` reports a `NOT TAKEN` from a
signatory's pact change, and routed like any other.

**One row per record of pact changes this review takes.** `Signatory` is the
signatory's origin remote URL as the pact's `| Signatory |` table lists it.
`Change` is the signatory's work-item id, `@`, and the content hash of its
`seal/pact-changes/<work-item-id>.md`, exactly as `pact-check` prints it on
the `NOT TAKEN` line. `Verdict` is one of two words:

  holds    the clause stands as written, and the signatory's change keeps it
  amended  this work item amends the clause to take the change

**A record is taken at the hash this row names, and no other.** A record that
gains rows after its review reads `NOT TAKEN` again, naming both hashes, and
takes a new row here at the hash it holds now. A commit SHA is never the key:
the signatory's feature branch squashes, and the SHA stops resolving.

**What `pact-check` refuses here, at exit 2**: a signatory the pact does not
list, a record that signatory does not hold, a verdict other than the two,
and `amended` where a clause the record cites still has the hash the record
recorded — the clause was not amended.

The builder judges each change against its clause in the signatory's
checkout, at the paths `pact-check` printed, and the review chain's warden
verifies those judgments there. -->

| Signatory | Change | Verdict |
|---|---|---|
| <the signatory's origin remote URL> | <work-item-id>@<content hash> | <holds or amended> |
