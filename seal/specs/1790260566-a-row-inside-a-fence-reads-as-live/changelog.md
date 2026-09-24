### Fixed

- Every gate that reads a record through the shared reader now recognises a
  fenced code block the way CommonMark does (#491). A run of backticks or
  tildes indented four spaces or more is no longer read as a fence, so it no
  longer hides every table row below it. A line such as ```` ```python ````
  inside an open block no longer closes the block. A backtick line whose info
  string holds a backtick no longer opens one. The review-record generator,
  the pull-request chain check, the unverified-record check and the
  review-history guard all read through this reader.
- `evidence-check` no longer checks a ledger row shown inside a fenced code
  block that closes (#444). A ledger that explains its own row format can show
  an example row without failing the build, and `--reverify` and `--migrate`
  leave the example byte for byte. A row in a fence that never closes, or in
  an HTML comment, is still checked. **A real claim written inside a closed
  fence is no longer checked either**, and nothing reports that, so a ledger
  row meant as a claim belongs outside any fence. A copy of the checker
  vendored alone into `tools/` applies the same rule.
