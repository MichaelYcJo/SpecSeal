- **A gate that fails to load is said once per session at the end of the
  turn, and the call it failed on still goes ahead (issue #28).** The
  dispatcher skips a gate that raises, so the rest of its group still
  decides and nothing is blocked. That skip used to read exactly like an
  allow. A broken `cmdline.py` silenced the worktree guard's `isolation:
  "worktree"` check with nobody told. Now each skip writes a record under
  `<git-common-dir>/specseal-gate-failure/<session>/`, keyed by gate, in an
  opted-in repository. The `stop` group says every pending record once, at
  the end of the main session's turn, as a `systemMessage`. Its first line
  counts the gates, and each gate gets a line naming whether it failed to
  load or while running, where, and the exception's class and first line. A
  gate that failed to load is named in every group that loads it, so a
  broken worktree guard reads as `pre-bash` and `pre-agent` both. It goes before the sealer's stamp when both arrive, so the stamp
  stays last. A subagent's failure is said at the main session's turn end.
  A broken `optin.py` is reported rather than read as "not opted in". A
  failure the dispatcher cannot write down, in a git directory it cannot
  write to, is as silent as before. Every group's stdout is unchanged
  whenever its gates all run.
- **A gate whose module body calls `sys.exit` no longer ends its group
  (issue #28).** The dispatcher caught `Exception` alone around the import,
  so a `SystemExit` raised while loading one gate ended the process, and
  every gate after it in the group never decided. It is caught now and
  recorded as a load failure. A `SystemExit` from a gate's `main()` is still
  a gate finishing, as `worktree-guard.py` uses it.
- **A gate that prints JSON the dispatcher cannot read no longer ends its
  whole hook group (issue #661).** `null`, a number, a string, `true`, an
  array, or an object whose `hookSpecificOutput` is not an object or whose
  decision, reason or message is not text raised inside the merge, after
  every gate had run. The group exited 1, and a neighbour's `deny` or message
  was lost with it. That output is now dropped, the rest of the group
  decides, and the gate is named at the end of the turn like any gate that
  failed while running.
- **A `cd` on one line now carries a commit on the next line to where the
  `cd` went (issue #662).** The commit gate judged such a commit in the `cd`'s
  target and also in the session's own directory, because a newline, like
  `;`, runs the next line whether the `cd` worked or not. So a session whose
  own repository had no routing declaration was asked about a commit landing
  in a worktree that had one, in the middle of an `automation` run. A `cd`
  into a directory that is there and can be entered does not fail, so that
  second directory is now dropped, but only where every command before the
  `cd` is itself a `cd`. The hook reads the filesystem before the command
  runs, and an earlier `mv` or `chmod` could make the `cd` fail. `||`, which
  runs only when the `cd` fails, still reaches it. So does a `cd` to a
  missing directory, to one without the execute bit, or from a shell the
  reader could not follow. The worktree guard reads the same walk.
- **A heredoc fed to `python3 -`, `node`, `ruby` or `perl` is no longer read
  as shell by the commit gate (issue #665).** A patch written as
  `python3 - <<'EOF' … EOF` whose Python held `git commit` inside test
  strings and a `for` loop was stopped as a command the gate could not read,
  four times in one `automation` run, with no commit in it. The body of a
  known non-shell interpreter reading its program from stdin is that
  program, and is now left out, in one exact shape: the interpreter with
  nothing or only `-` before `<<`, and nothing after the heredoc's word. Any
  other word in that command (a flag, a script, a redirect, an assignment),
  a quoted separator, and any other consumer are still read as shell, so
  `bash <<'EOF'` with a commit inside is still judged.
