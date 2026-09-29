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
  whole hook group (issue #661).** `null`, a number, a string, `true` or an
  array raised inside the merge, after every gate had run. So did an object
  whose `hookSpecificOutput` is set but is not an object, whose decision or
  reason is not text, or, with no decision, whose message is not text. The group exited 1, and a neighbour's `deny` or message
  was lost with it. That output is now dropped, the rest of the group
  decides, and the gate is named at the end of the turn like any gate that
  failed while running.
