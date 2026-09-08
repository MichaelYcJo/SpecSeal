<!-- specs/1788904490-every-published-reading-carries-three-wrong-rows -->

### Fixed

- **A test run this repository actually makes was charged to the row that
  names nothing, and a file write was charged to `test` in the same reading.**
  The meter decided a command was a test run by looking for five names —
  `pytest`, `jest`, `vitest`, `go test`, `cargo test`, `mvn test` — and a
  project that ships `bin/test` matches none of them. Every run of it landed
  in `other`, the row nobody reads because it is the row everything falls
  into. The family now knows a script named `test` invoked by path
  (`./bin/test`, `scripts/test.sh`) and the runners a language's own
  convention names (`make test`, `npm test`, `tox`, `rspec`, `dotnet test` and
  their siblings), so a repository that has said what its test command is in
  the filesystem is read correctly without configuring anything. Measured over
  180 transcripts: **157 calls whose first word is this repository's own
  runner went from 0 charged to `test` to all 157.**

  **The other direction was larger.** A command's whitespace is flattened
  before the family is taken, so a `cat > file <<'EOF' … EOF` that writes a
  document arrives as one line with the whole document in it — and any runner
  named inside it took the call. The classifier now stops at the heredoc
  operator, which answers it for every family at once instead of one word at a
  time: **644 calls the old family charged to `test` are not test runs**, and
  `lint/type` and `build` lose the same kind of false positive. A `<<`
  followed by a lowercase unquoted word is left alone, because in a real
  command line that is more often a quoted comparison than a heredoc and
  cutting there would charge a real run to `other`.

  **What the table still cannot name, it now says out loud.** A runner called
  `bin/check` or `./run-suite` is a name nobody outside that repository can
  guess, and the failure was silent: an empty `test` row reads exactly like a
  run with no tests in it. When `other` leads the table by time, the report
  now says that the largest family names nothing and prints the slowest
  command charged there — the exact string a family would have to learn. It is
  absent when a named family leads. (#200)

- **A round that wrote a full report read as 62 output tokens.** A streamed
  assistant message reaches the transcript as several rows sharing one
  `message.id`, and its `output_tokens` grows across them — the last row
  carries the completed count. The totals kept the first row, so the `output`
  figure was the sum of however much of each message had been written when its
  first row landed. Measured over the same 180 transcripts: 9,098 of 13,425
  messages are split, and the reported total was 4,976,637 against a real
  8,683,844. **The error is not a scale factor**, which is why no reader could
  correct for it — two segments taken the same day were out by 3.2× and 556×,
  with nothing in the printed report saying which.

  Each field is now summed at the **largest** count its message reached. Not
  the last row, though last and largest agree on every one of those 13,425
  messages and no rows arrive out of order: `output_tokens` grows within a
  message, so the largest is the completed count under any row order, where
  last-row-wins is only right under one the format does not promise. The dedup
  itself was right and stays — a message written as one row per content block
  repeats its usage on each, and per-row summing would multiply a run's
  headline number.

  `load`'s per-turn tuple carried a third element, that message's
  `output_tokens`, that **nothing in the file read**. It is removed rather than
  repaired, because what sat there was the same first partial count: a wrong
  number waiting for its first reader, which is exactly how this defect was
  written. The input-side fields it does read are fixed when the request is
  made and repeat unchanged on every row, which is why that reader was never
  affected. (#202)

- **A third the meter could not compute was charged 0, and the line below took
  that 0 for a baseline.** The context line prints when the last third of a
  run's input counts exceeds the first third by half, and any positive number
  clears a threshold of zero. So a transcript whose first third overflowed
  printed `0 → 10 input tokens; later calls cost more than the same call would
  have earlier` — the input had collapsed by 307 orders of magnitude and the
  line said it grew. With the uncomputable third **last** the line was
  suppressed instead, so which direction the reader was told depended on which
  third overflowed. The threshold now requires a first third above zero, the
  same shape as the positive-span guard two functions up.

  A second shape, one function earlier: the filter deciding which turns enter
  the mean was a truthiness test on a signed number, so it **dropped a zero
  and kept a negative**. Six turns whose first three carry minus ten input
  tokens gave a growth of `[-10, 0, 10]` and printed the line off a baseline
  no harness can mean. Zero goes on being dropped and that is not a
  regression: the counter answers 0 both for a field a harness never wrote and
  for one it wrote as 0, so the file cannot tell a turn that spent nothing
  from a turn nobody measured, and a mean is the wrong place to guess. (#193)

### Changed

- **Readings taken before this release and readings taken after it are not
  comparable, and nothing in either says so.** Every per-segment reading this
  repository has published carries all three defects above. The transcripts
  still exist, so any of them can be retaken; whether they are re-derived or
  simply marked is `questions.md` Q1 on this work item, and the marking is
  posted to the open flow-measurement log.
