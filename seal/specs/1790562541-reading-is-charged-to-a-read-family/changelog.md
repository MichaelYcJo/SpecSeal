- **A backslash at the end of a line inside an unquoted heredoc joins the
  next line, as it does in the shell (#635's round 3, carried by #642).**
  `session-cost` read `cat <<EOF⏎body \⏎EOF⏎git push` as a heredoc closed
  at the `EOF` line and charged the `git push` to `git`. Bash joins
  `body \` to the next line, so that line closes nothing and the `git push`
  is part of the document. The family now reads it the same way. A quoted
  delimiter keeps its backslashes, and so does an escaped one (`\\`).
  Over the 374 transcripts on one machine, 2026-09-28, the fix moves no
  call.
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
- **Readings published before the release carrying #642 are affected in
  their `by family` rows and the `other` note, and nowhere else.** In each,
  there is no `read` row, `other` holds those calls, and the note under the
  table may fire where it would not now and name a read command. The `git`,
  `test`, `lint/type` and `build` rows, the two repeats figures, span,
  command time, model time, idle, tokens, tools per turn, the `slowest` list
  and every `--spawns` and `--segments` span do not move. `--segments` now
  says so on the page, naming #642. Measured on 2026-09-28 over the 374
  transcripts on one machine (24,223 Bash calls, 172,386 seconds): 7,819
  calls and 5,221 seconds move from `other` to `read`, and no other call
  moves. `other` falls from 57.0% of the Bash calls to 24.7%, and from 34.7%
  of their seconds to 31.7%, because a read is fast. It led the Bash seconds
  in 170 of the 363 transcripts holding a Bash call and leads in 123. The
  words that most often keep an otherwise-read line in `other` are `cut`
  (777 lines), `python3` (578) and this repository's own `evidence-check`
  (429); a heredoc keeps 2,502 lines out and a substitution 630.
