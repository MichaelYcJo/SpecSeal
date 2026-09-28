- **A backslash at the end of a line inside an unquoted heredoc joins the
  next line, as it does in the shell (#635's round 3, carried by #642).**
  `session-cost` read `cat <<EOF⏎body \⏎EOF⏎git push` as a heredoc closed
  at the `EOF` line and charged the `git push` to `git`. Bash joins
  `body \` to the next line, so that line closes nothing and the `git push`
  is part of the document. The family now reads it the same way. A quoted
  delimiter keeps its backslashes, and so does an escaped one (`\\`).
  Measured by #635's round 3, the fix moved no call in the corpus it was
  read against.
