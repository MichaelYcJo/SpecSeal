- **A backslash at the end of a line inside an unquoted heredoc joins the
  next line, as it does in the shell (#635's round 3, carried by #642).**
  `session-cost` read `cat <<EOF⏎body \⏎EOF⏎git push` as a heredoc closed
  at the `EOF` line and charged the `git push` to `git`. Bash joins
  `body \` to the next line, so that line closes nothing and the `git push`
  is part of the document. The family now reads it the same way. A quoted
  delimiter keeps its backslashes, and so does an escaped one (`\\`).
  Measured by #635's round 3, the fix moved no call in the corpus it was
  read against.
- **`session-cost` charges a call that only reads to a `read` family
  (issue #642).** A call that read a file or listed a directory was charged
  to `other`, so `other` led nearly every reading and the note under it
  named a `sed -n` or a `cat`. A call is now `read` when every command on
  the line is a read word (`sed`, `grep`, `rg`, `cat`, `head`, `tail`, `ls`,
  `find`, `wc`, `awk`, `nl`, `sort`, `diff`) or a word that touches no file
  (`cd`, `echo`, `printf`, `test`, `[`, `read`, the loop words), and at
  least one is a read word. A line that writes is never `read`: a
  redirection into anything but `/dev/null`, `sed -i` in any spelling,
  `sort -o`, `find`'s `-delete` and `-exec` actions, and `awk -i inplace`
  keep it `other`. So does anything the walk cannot see: a heredoc, a
  here-string, a `$( … )`, a backtick, a process substitution, a `case` and
  a line the tokeniser refuses. A script handed to `python3 -` by heredoc
  gets no family, by the owner's answer. `read` is judged after the four
  families before it, so `grep -rn pytest docs/` stays `test` and
  `ls && git status` stays `git`.
