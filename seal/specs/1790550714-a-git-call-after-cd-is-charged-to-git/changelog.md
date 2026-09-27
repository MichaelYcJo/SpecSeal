- **`session-cost` charges a `git` or `gh` call to `git` wherever it runs on
  the line, not only at its start (issue #377).** The family was the one
  pattern anchored at position 0, so `cd /x && git status`, a `gh` call in a
  `for` loop, `FOO=1 git …` and `(cd /x && git …)` were all charged to
  `other`. It is now read by command word, from a POSIX tokenisation of the
  line: the first word after a separator, a subshell's `(`, a reserved word
  or a leading assignment, by basename. A word inside quotes, inside a
  command substitution or behind a wrapper such as `timeout` is not a
  command word, so `grep -rn git`, `cat .git/config` and `echo 'a; git b'`
  stay out. A line the tokeniser refuses, on an unmatched quote, is judged
  by the old anchored pattern. A line that runs a test and a `git` is still
  the test's. Measured over the 349 transcripts on the machine that found
  it: 2,703 calls and 21,179 seconds were charged to `other` in this shape.
  **Readings published before 0.15.6 are affected in their `by family` rows
  and the `other` note**: `git` reads low and `other` reads high by the same
  calls, and the note may name a command that was a `git` run. `--segments`
  now says so on the page. Span, command time, model time, tokens, tools per
  turn, the `slowest` list and the repeats figures do not move.
