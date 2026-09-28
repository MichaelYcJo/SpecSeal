- **`session-cost` charges a `git` or `gh` call to `git` wherever it runs on
  the line, not only at its start (issue #377).** The family was the one
  pattern anchored at position 0, so `cd /x && git status`, a `gh` call in a
  `for` loop, `FOO=1 git …` and `(cd /x && git …)` were all charged to
  `other`. It is now read by command word, from a POSIX tokenisation of the
  line: the first word after a separator, a newline, a subshell's `(`, a
  reserved word or a leading assignment, by basename. A word inside quotes,
  inside `$( … )`, `<( … )` or `>( … )`, inside a `#` comment or behind a
  wrapper such as `timeout` is not a command word, so `grep -rn git`,
  `cat .git/config`, `echo 'a; git b'` and `x=$(cd a && git log)` stay out.
  A backtick substitution's first word is not one either, but a separator
  inside backticks is read as the line's. A line the tokeniser refuses, on an unmatched quote, is judged by
  the words it read before refusing, and by the old anchored pattern where
  it read none. A line that runs a test and a `git` is still the test's.
- **The family reads the command as it ran, and a heredoc loses only its
  body (issue #377).** `load` flattened every newline before the family was
  judged, and the heredoc rule dropped everything from the operator to the
  end. So a command on a line of its own was read as arguments of the line
  before, and a `gh issue create` after `cat > body.md <<'EOF' … EOF`, or a
  `bin/test` after a `python3 - <<'EOF'` script, was charged to `other`. The
  body is now removed up to its closing line, which `<<-` lets carry leading
  tabs, and what follows is read by every family. A heredoc with no closing
  line is cut to the end as before. Every printed command still reads the
  flattened text.
- **Readings published before 0.15.6 are affected in their `by family`
  rows, the `other` note and the two repeats figures.** In each, `git` and
  `test` read low and `other` reads high by the same calls, the note may name
  a command that was a `git` run, and the repeats figures may read low,
  because a test run after a heredoc was not counted. Span, command time,
  model time, idle, tokens, tools per turn and the `slowest` list do not
  move. `--segments` now says so on the page, naming #377. Measured on
  2026-09-28 over the 353 transcripts on one machine (23,285 Bash calls,
  165,888 seconds): 3,691 calls and 32,257 seconds move from `other` to
  `git`, 819 calls and 10,649 seconds from `other` to `test`, 90 calls to
  `lint/type` and 9 to `build`, and 10 calls move to `test` from `git` or
  `build` because a test ran after a heredoc on the same command. 18,666
  calls do not move. `other` led the Bash seconds in 260 of the 342
  transcripts holding a Bash call, and leads in 159. Keeping every word of
  a `$( … )` out of command position, and removing comments first, moved
  one more call, from `git` to `other`, over the 358 transcripts there were
  by then.
