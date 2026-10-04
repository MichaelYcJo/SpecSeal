### Fixed

- The commit gate no longer stops a command that writes a file, or feeds a
  Python program on stdin, through one exact heredoc shape whose body only
  mentions a commit (#739, #763). It used to read every heredoc body as shell,
  so a pull request body or a memory note that quoted a commit cost an
  unattended run the whole Bash call, three times in one session. The shape is
  matched byte for byte by a new reader that shares nothing with the
  command-line splitter: a first line of an optional `cd` to one word, then
  `cat` or `tee` writing one file or `python3 -` with plain arguments, then a
  delimiter of letters, digits and underscores in single quotes, and nothing
  else on that line. The body ends at the first line equal to the delimiter.
  The command may hold no carriage return, NUL, backslash before a newline or
  second heredoc, and nothing may follow a file's terminator. Lines after a
  Python program's terminator are read as before, so a commit there is judged
  where it lands. Every other heredoc, including an unquoted or double-quoted
  delimiter, an assignment or a substitution on the first line, a parameter as
  the target, and a program after a written file, is read exactly as before.
  This replaces the approach of PR #760, which trusted the splitter's idea of
  where a body ends; four review passes each found a place where that idea and
  the shell disagreed, and every one was a commit nobody judged. A new test
  runs a generated corpus of the admitted shape through bash and zsh, directly
  and through `eval`, and checks that each shell cuts the body where the reader
  does. `docs/commit-review-gate-spec.md` and the agent contract's §9 state the
  shape and what stays read.
