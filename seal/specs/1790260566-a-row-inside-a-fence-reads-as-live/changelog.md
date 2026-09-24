### Fixed

- Every gate that reads a record through the shared reader now recognises a
  fenced code block the way CommonMark does (#491). A run of backticks or
  tildes indented four spaces or more is no longer read as a fence, so it no
  longer hides every table row below it. A line such as ```` ```python ````
  inside an open block no longer closes the block. A backtick line whose info
  string holds a backtick no longer opens one. The review-record generator,
  the pull-request chain check, the unverified-record check and the
  review-history guard all read through this reader.
