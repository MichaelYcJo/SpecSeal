# Pact review — <work-item-id>

<!-- seal/pact-reviews/<work-item-id>.md, at the pact's repository: the
record of one pact review (`docs/the-pact.md`). A pact review is an ordinary
work item here, opened when `pact-check` reports a `NOT TAKEN` from a
signer's pact change, and routed like any other.

**One row per record of pact changes this review takes.** `Signer` is the
signer's origin remote URL as the pact's `| Signer |` table lists it.
`Change` is the signer's work-item id, `@`, and the content hash of its
`seal/pact-changes/<work-item-id>.md`, exactly as `pact-check` prints it on
the `NOT TAKEN` line. `Verdict` is one of two words:

  holds    the clause stands as written, and the signer's change keeps it
  amended  this work item amends the clause to take the change

**A record is taken at the hash this row names, and no other.** A record that
gains rows after its review reads `NOT TAKEN` again, naming both hashes, and
takes a new row here at the hash it holds now. A commit SHA is never the key:
the signer's feature branch squashes, and the SHA stops resolving.

**What `pact-check` refuses here, at exit 2**: a signer the pact does not
list, a record that signer does not hold, a verdict other than the two,
and `amended`, at the record's current hash, where a clause it cites still
has the hash the record recorded — the clause was not amended. A row at an
older hash is not judged again against rows the record gained since.

The builder judges each change against its clause in the signer's
checkout, at the paths `pact-check` printed, and the review chain's warden
verifies those judgments there. -->

| Signer | Change | Verdict |
|---|---|---|
| <the signer's origin remote URL> | <work-item-id>@<content hash> | <holds or amended> |
